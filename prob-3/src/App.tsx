import React, { useState, useEffect } from 'react';
import { useJobDiscovery, JobFilters, SortOption, useUrlFilters } from './useJobDiscovery';
import { Job } from './types';
import JobCard from './components/JobCard';
import JobCardSkeleton from './components/JobCardSkeleton';
import FilterPanel from './components/FilterPanel';
import { Search, Grid, List as ListIcon, Filter, X } from 'lucide-react';
import jobsData from './jobs.json';

// Cast imports if necessary or let resolveJsonModule handle it
const allJobs = jobsData as unknown as Job[];

const App: React.FC = () => {
    // 1. URL Sync Filters
    const [filters, setFilters] = useUrlFilters({
        searchTerm: '',
        salaryRange: { min: 0, max: 200000 },
        experienceLevel: 0,
        selectedSkills: [],
        jobTypes: [],
        postedAfter: null
    });

    const [sortOption, setSortOption] = useState<SortOption>('matchScore');
    const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');
    const [isMobileFilterOpen, setIsMobileFilterOpen] = useState(false);
    const [isLoading, setIsLoading] = useState(true);

    // 2. LocalStorage for Saved Jobs
    const [savedJobIds, setSavedJobIds] = useState<Set<string>>(new Set());

    useEffect(() => {
        // Simulate Fetch Delay
        const timer = setTimeout(() => setIsLoading(false), 500);

        // Restore Saved Jobs
        const saved = localStorage.getItem('savedJobs');
        if (saved) {
            try {
                setSavedJobIds(new Set(JSON.parse(saved)));
            } catch (e) { console.error("Failed to parse saved jobs", e); }
        }

        return () => clearTimeout(timer);
    }, []);

    const toggleSaveJob = (id: string) => {
        setSavedJobIds(prev => {
            const next = new Set(prev);
            if (next.has(id)) next.delete(id);
            else next.add(id);

            localStorage.setItem('savedJobs', JSON.stringify(Array.from(next)));
            return next;
        });
    };

    const filteredJobs = useJobDiscovery(allJobs, filters, sortOption);

    return (
        <div className="min-h-screen bg-gray-50 text-gray-900 font-sans">
            {/* Mobile Header */}
            <div className="sticky top-0 z-30 bg-white border-b p-4 md:hidden flex justify-between items-center shadow-sm">
                <h1 className="text-xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">JobMatch</h1>
                <button
                    onClick={() => setIsMobileFilterOpen(true)}
                    className="p-2 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
                >
                    <Filter size={20} />
                </button>
            </div>

            <div className="max-w-7xl mx-auto p-4 md:p-6 lg:p-8 flex gap-6">
                {/* Sidebar Filters (Desktop) & Mobile Drawer */}
                <FilterPanel
                    filters={filters}
                    setFilters={setFilters}
                    isOpen={isMobileFilterOpen}
                    onClose={() => setIsMobileFilterOpen(false)}
                />

                {/* Main Content */}
                <div className="flex-1 flex flex-col gap-6">

                    {/* Top Bar: Search, Sort, View Toggle */}
                    <div className="flex flex-col md:flex-row gap-4 justify-between items-center">
                        {/* Search */}
                        <div className="relative w-full md:max-w-md">
                            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={18} />
                            <input
                                type="text"
                                placeholder="Search jobs, companies, skills..."
                                className="w-full pl-10 pr-4 py-2 rounded-lg border border-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500 shadow-sm"
                                value={filters.searchTerm}
                                onChange={(e) => setFilters(prev => ({ ...prev, searchTerm: e.target.value }))}
                            />
                        </div>

                        <div className="flex w-full md:w-auto gap-3 justify-between md:justify-end">
                            {/* Sort */}
                            <select
                                value={sortOption}
                                onChange={(e) => setSortOption(e.target.value as SortOption)}
                                className="p-2 bg-white border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 shadow-sm"
                            >
                                <option value="matchScore">Best Match</option>
                                <option value="salary">Highest Salary</option>
                                <option value="date">Newest</option>
                            </select>

                            {/* View Toggle */}
                            <div className="flex items-center bg-gray-100 rounded-lg p-1 border border-gray-200">
                                <button
                                    onClick={() => setViewMode('grid')}
                                    className={`p-1.5 rounded-md transition-colors ${viewMode === 'grid' ? 'bg-white shadow-sm text-blue-600' : 'text-gray-400 hover:text-gray-600'}`}
                                >
                                    <Grid size={18} />
                                </button>
                                <button
                                    onClick={() => setViewMode('list')}
                                    className={`p-1.5 rounded-md transition-colors ${viewMode === 'list' ? 'bg-white shadow-sm text-blue-600' : 'text-gray-400 hover:text-gray-600'}`}
                                >
                                    <ListIcon size={18} />
                                </button>
                            </div>
                        </div>
                    </div>

                    {/* Results Info */}
                    <div className="text-sm text-gray-500 font-medium h-5">
                        {!isLoading && `Showing ${filteredJobs.length} jobs based on your preferences`}
                    </div>

                    {/* Job List */}
                    {isLoading ? (
                        /* 3. Skeleton Loading */
                        <div className="grid gap-4 grid-cols-1 md:grid-cols-2 lg:grid-cols-2 xl:grid-cols-3">
                            {[...Array(6)].map((_, i) => <JobCardSkeleton key={i} />)}
                        </div>
                    ) : (
                        filteredJobs.length > 0 ? (
                            <div className={`grid gap-4 ${viewMode === 'grid' ? 'grid-cols-1 md:grid-cols-2 lg:grid-cols-2 xl:grid-cols-3' : 'grid-cols-1'}`}>
                                {filteredJobs.map(job => (
                                    <JobCard
                                        key={job.id}
                                        job={job}
                                        viewMode={viewMode}
                                        isSaved={savedJobIds.has(job.id)}
                                        onToggleSave={() => toggleSaveJob(job.id)}
                                    />
                                ))}
                            </div>
                        ) : (
                            /* Empty State */
                            <div className="flex flex-col items-center justify-center py-20 text-center bg-white rounded-xl border border-dashed border-gray-300">
                                <div className="bg-gray-100 p-4 rounded-full mb-4">
                                    <Search size={32} className="text-gray-400" />
                                </div>
                                <h3 className="text-lg font-bold text-gray-800">No jobs found</h3>
                                <p className="text-gray-500 max-w-xs mt-2 mb-6">We couldn't find any positions matching your specific criteria. Try adjusting your filters.</p>
                                <button
                                    onClick={() => setFilters({
                                        searchTerm: '',
                                        salaryRange: { min: 0, max: 200000 },
                                        experienceLevel: 0,
                                        selectedSkills: [],
                                        jobTypes: [],
                                        postedAfter: null
                                    })}
                                    className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
                                >
                                    Clear all filters
                                </button>
                            </div>
                        )
                    )}
                </div>
            </div>
        </div>
    );
};

export default App;
