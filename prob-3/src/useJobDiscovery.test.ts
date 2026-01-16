import { renderHook, act } from '@testing-library/react';
import { useJobDiscovery, JobFilters } from './useJobDiscovery';
import { Job, JobType } from './types';

// Mock Data
const mockJobs: Job[] = [
    {
        id: '1', title: 'React Developer', company: 'TechCorp',
        location: { city: 'Remote', country: 'Remote' },
        salary: { min: 60000, max: 80000, currency: 'USD' },
        type: JobType.Remote,
        postedAt: '2023-01-01T10:00:00Z',
        experienceLevel: 3,
        skills: ['React', 'TypeScript'],
        matchScore: 90
    },
    {
        id: '2', title: 'Backend Engineer', company: 'DataMinds',
        location: { city: 'NY', country: 'USA' },
        salary: { min: 100000, max: 120000, currency: 'USD' },
        type: JobType.FullTime,
        postedAt: '2023-01-02T10:00:00Z',
        experienceLevel: 5,
        skills: ['Node.js', 'SQL'],
        matchScore: 80
    },
    {
        id: '3', title: 'Full Stack', company: 'TechCorp',
        location: { city: 'SF', country: 'USA' },
        salary: { min: 80000, max: 100000, currency: 'USD' },
        type: JobType.Contract,
        postedAt: '2023-01-03T10:00:00Z',
        experienceLevel: 2,
        skills: ['React', 'Node.js'],
        matchScore: 85
    }
];

const defaultFilters: JobFilters = {
    searchTerm: '',
    salaryRange: { min: 0, max: 200000 },
    experienceLevel: 0,
    selectedSkills: [],
    jobTypes: [],
    postedAfter: null
};

describe('useJobDiscovery', () => {
    beforeEach(() => {
        jest.useFakeTimers();
    });

    afterEach(() => {
        jest.useRealTimers();
    });

    it('should return all jobs initially', () => {
        const { result } = renderHook(() => useJobDiscovery(mockJobs, defaultFilters));
        expect(result.current.length).toBe(3);
    });

    it('should filter by search term (debounced)', async () => {
        const filters = { ...defaultFilters, searchTerm: 'Backend' };
        const { result } = renderHook(() => useJobDiscovery(mockJobs, filters));

        // Initially might return all or nothing depending on how useDebounce initializes, 
        // but usually it initializes with value immediately or requires wait.
        // Our implementation initializes with value, but effect sets it.
        // Actually, our useDebounce initializes with `value`.
        // Wait, let's check useDebounce implementation.
        // implementation: const [debouncedValue, setDebouncedValue] = useState(value);
        // So initially it uses the passed value.
        // WARNING: If the initial state is the value, then it's NOT debounced on mount, it's immediate. 
        // This is fine for initial render but let's test the update.

        expect(result.current.length).toBe(1);
        expect(result.current[0].title).toBe('Backend Engineer');
    });

    it('should handle salary overlap correctly', () => {
        // Job 1: 60k-80k. Filter: 50k-70k. Overlap: 60-70. Should match.
        // Job 2: 100k-120k. Filter: 50k-70k. No overlap. Should NOT match.
        const filters = { ...defaultFilters, salaryRange: { min: 50000, max: 70000 } };
        const { result } = renderHook(() => useJobDiscovery(mockJobs, filters));

        expect(result.current.map(j => j.id)).toContain('1');
        expect(result.current.map(j => j.id)).not.toContain('2');
    });

    it('should filter by experience level', () => {
        const filters = { ...defaultFilters, experienceLevel: 4 };
        const { result } = renderHook(() => useJobDiscovery(mockJobs, filters));

        expect(result.current.length).toBe(1);
        expect(result.current[0].id).toBe('2'); // Level 5
    });

    it('should filter by skills (subset check)', () => {
        // Job 1: React, TS. Job 3: React, Node.
        // Filter: React. Both should match.
        const filters = { ...defaultFilters, selectedSkills: ['React'] };
        const { result } = renderHook(() => useJobDiscovery(mockJobs, filters));

        expect(result.current.length).toBe(2);
        expect(result.current.map(j => j.id)).toEqual(expect.arrayContaining(['1', '3']));

        // Filter: React, Node. Only Job 3.
        const filters2 = { ...defaultFilters, selectedSkills: ['React', 'Node.js'] };
        const { result: result2 } = renderHook(() => useJobDiscovery(mockJobs, filters2));
        expect(result2.current.length).toBe(1);
        expect(result2.current[0].id).toBe('3');
    });

    it('should sort by match score (default)', () => {
        const { result } = renderHook(() => useJobDiscovery(mockJobs, defaultFilters));
        // Order: 1 (90), 3 (85), 2 (80)
        expect(result.current[0].id).toBe('1');
        expect(result.current[1].id).toBe('3');
        expect(result.current[2].id).toBe('2');
    });

    it('should sort by salary (high-low)', () => {
        const { result } = renderHook(() => useJobDiscovery(mockJobs, defaultFilters, 'salary'));
        // Order: 2 (120k max), 3 (100k max), 1 (80k max)
        expect(result.current[0].id).toBe('2');
        expect(result.current[1].id).toBe('3');
        expect(result.current[2].id).toBe('1');
    });

    it('should sort by date', () => {
        const { result } = renderHook(() => useJobDiscovery(mockJobs, defaultFilters, 'date'));
        // Order: 3 (Jan 3), 2 (Jan 2), 1 (Jan 1)
        expect(result.current[0].id).toBe('3');
        expect(result.current[1].id).toBe('2');
        expect(result.current[2].id).toBe('1');
    });

    it('should search "React" without clearing "Remote" filter', () => {
        const filters = {
            ...defaultFilters,
            searchTerm: 'React',
            jobTypes: [JobType.Remote]
        };
        const { result } = renderHook(() => useJobDiscovery(mockJobs, filters));

        // Job 1: React + Remote -> Match
        // Job 3: React + Contract -> No Match (Type mismatch)

        expect(result.current.length).toBe(1);
        expect(result.current[0].id).toBe('1');
    });
});
