import { useState, useMemo, useEffect, useCallback } from 'react';
import { Job, JobType, SalaryRange } from './types';

export interface JobFilters {
    searchTerm: string;
    salaryRange: { min: number; max: number };
    experienceLevel: number; // Minimum years
    selectedSkills: string[];
    jobTypes: JobType[];
    postedAfter: Date | null;
}

export type SortOption = 'matchScore' | 'salary' | 'date';

// Simple debounce hook for internal use
function useDebounce<T>(value: T, delay: number): T {
    const [debouncedValue, setDebouncedValue] = useState(value);

    useEffect(() => {
        const handler = setTimeout(() => {
            setDebouncedValue(value);
        }, delay);

        return () => {
            clearTimeout(handler);
        };
    }, [value, delay]);

    return debouncedValue;
}

export function useJobDiscovery(jobs: Job[], filters: JobFilters, sortOption: SortOption = 'matchScore') {
    const debouncedSearchTerm = useDebounce(filters.searchTerm, 300);

    const filteredJobs = useMemo(() => {
        return jobs.filter(job => {
            // 1. Search (Debounced)
            if (debouncedSearchTerm) {
                const term = debouncedSearchTerm.toLowerCase();
                const matchesTitle = job.title.toLowerCase().includes(term);
                const matchesCompany = job.company.toLowerCase().includes(term);
                if (!matchesTitle && !matchesCompany) return false;
            }

            // 2. Job Type
            if (filters.jobTypes.length > 0 && !filters.jobTypes.includes(job.type)) {
                return false;
            }

            // 3. Salary Range (Overlap Check)
            // Check if [job.min, job.max] overlaps with [filter.min, filter.max]
            // Overlap if: (JobMin <= FilterMax) && (JobMax >= FilterMin)
            if (job.salary.min > filters.salaryRange.max || job.salary.max < filters.salaryRange.min) {
                return false;
            }

            // 4. Experience Level (Min requirements)
            if (job.experienceLevel < filters.experienceLevel) {
                return false;
            }

            // 5. Skills (All selected skills must be present)
            if (filters.selectedSkills.length > 0) {
                const hasAllSkills = filters.selectedSkills.every(skill => job.skills.includes(skill));
                if (!hasAllSkills) return false;
            }

            // 6. Time Range
            if (filters.postedAfter) {
                const jobDate = new Date(job.postedAt);
                if (jobDate < filters.postedAfter) {
                    return false;
                }
            }

            return true;
        });
    }, [jobs, debouncedSearchTerm, filters.jobTypes, filters.salaryRange, filters.experienceLevel, filters.selectedSkills, filters.postedAfter]);

    const sortedJobs = useMemo(() => {
        // Clone to avoid mutating filteredJobs if we were doing in-place sort, usually .sort mutates.
        // map to new array first.
        const sorted = [...filteredJobs];

        sorted.sort((a, b) => {
            switch (sortOption) {
                case 'salary':
                    // Sort by Max Salary Descending
                    return b.salary.max - a.salary.max;
                case 'date':
                    return new Date(b.postedAt).getTime() - new Date(a.postedAt).getTime();
                case 'matchScore':
                default:
                    return b.matchScore - a.matchScore;
            }
        });

        return sorted;
    }, [filteredJobs, sortOption]);

    return sortedJobs;
}

export function useUrlFilters(initialFilters: JobFilters): [JobFilters, React.Dispatch<React.SetStateAction<JobFilters>>] {
    const [filters, setFilters] = useState<JobFilters>(() => {
        // Initialize from URL
        if (typeof window === 'undefined') return initialFilters;

        const params = new URLSearchParams(window.location.search);

        return {
            searchTerm: params.get('q') || initialFilters.searchTerm,
            salaryRange: {
                min: Number(params.get('minSalary')) || initialFilters.salaryRange.min,
                max: Number(params.get('maxSalary')) || initialFilters.salaryRange.max
            },
            experienceLevel: Number(params.get('exp')) || initialFilters.experienceLevel,
            selectedSkills: params.get('skills')?.split(',').filter(Boolean) || initialFilters.selectedSkills,
            jobTypes: params.get('type')?.split(',').filter(t => Object.values(JobType).includes(t as JobType)) as JobType[] || initialFilters.jobTypes,
            postedAfter: params.get('postedAfter') ? new Date(params.get('postedAfter')!) : initialFilters.postedAfter
        };
    });

    // Sync to URL
    useEffect(() => {
        if (typeof window === 'undefined') return;

        const params = new URLSearchParams();
        if (filters.searchTerm) params.set('q', filters.searchTerm);
        if (filters.salaryRange.min > 0) params.set('minSalary', filters.salaryRange.min.toString());
        if (filters.salaryRange.max < 200000) params.set('maxSalary', filters.salaryRange.max.toString());
        if (filters.experienceLevel > 0) params.set('exp', filters.experienceLevel.toString());
        if (filters.selectedSkills.length > 0) params.set('skills', filters.selectedSkills.join(','));
        if (filters.jobTypes.length > 0) params.set('type', filters.jobTypes.join(','));
        if (filters.postedAfter) params.set('postedAfter', filters.postedAfter.toISOString());

        const newUrl = `${window.location.pathname}?${params.toString()}`;
        window.history.replaceState(null, '', newUrl);
    }, [filters]);

    return [filters, setFilters];
}
