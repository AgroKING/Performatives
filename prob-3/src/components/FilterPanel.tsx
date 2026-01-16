import React, { useState } from 'react';
import { JobFilters } from '../useJobDiscovery';
import { JobType } from '../types';
import { X, Filter as FilterIcon } from 'lucide-react';

interface FilterPanelProps {
    filters: JobFilters;
    setFilters: React.Dispatch<React.SetStateAction<JobFilters>>;
    className?: string;
    isOpen: boolean; // Control for mobile drawer
    onClose: () => void;
}

const FilterPanel: React.FC<FilterPanelProps> = ({ filters, setFilters, className = '', isOpen, onClose }) => {
    const [minSalary, setMinSalary] = useState(filters.salaryRange.min);
    const [maxSalary, setMaxSalary] = useState(filters.salaryRange.max);

    // Handle Salary Change on blur/release to minimize excessive updates or use debounce effects
    const handleSalaryChange = () => {
        setFilters(prev => ({
            ...prev,
            salaryRange: { min: minSalary, max: maxSalary }
        }));
    };

    const toggleJobType = (type: JobType) => {
        setFilters(prev => {
            const current = prev.jobTypes;
            const exists = current.includes(type);
            return {
                ...prev,
                jobTypes: exists ? current.filter(t => t !== type) : [...current, type]
            };
        });
    };

    const content = (
        <div className="space-y-6">
            <div className="flex items-center justify-between md:hidden pb-4 border-b">
                <h2 className="font-bold text-lg">Filters</h2>
                <button onClick={onClose}><X /></button>
            </div>

            {/* Salary Range */}
            <div>
                <h3 className="font-semibold text-gray-700 mb-2">Salary Range</h3>
                <div className="flex gap-2 items-center">
                    <input
                        type="number" value={minSalary}
                        onChange={(e) => setMinSalary(Number(e.target.value))}
                        onBlur={handleSalaryChange}
                        className="w-full p-2 border rounded-md text-sm"
                        placeholder="Min"
                    />
                    <span className="text-gray-400">-</span>
                    <input
                        type="number" value={maxSalary}
                        onChange={(e) => setMaxSalary(Number(e.target.value))}
                        onBlur={handleSalaryChange}
                        className="w-full p-2 border rounded-md text-sm"
                        placeholder="Max"
                    />
                </div>
            </div>

            {/* Experience Level */}
            <div>
                <h3 className="font-semibold text-gray-700 mb-2">Experience (Years)</h3>
                <input
                    type="range" min="0" max="20"
                    value={filters.experienceLevel}
                    onChange={(e) => setFilters(prev => ({ ...prev, experienceLevel: Number(e.target.value) }))}
                    className="w-full accent-blue-600"
                />
                <div className="flex justify-between text-xs text-gray-500">
                    <span>Any</span>
                    <span>{filters.experienceLevel}+ Years</span>
                </div>
            </div>

            {/* Job Type */}
            <div>
                <h3 className="font-semibold text-gray-700 mb-2">Job Type</h3>
                <div className="space-y-2">
                    {[JobType.FullTime, JobType.PartTime, JobType.Contract, JobType.Remote, JobType.Freelance, JobType.Internship].map(type => (
                        <label key={type} className="flex items-center gap-2 cursor-pointer">
                            <input
                                type="checkbox"
                                checked={filters.jobTypes.includes(type)}
                                onChange={() => toggleJobType(type)}
                                className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                            />
                            <span className="text-sm text-gray-600">{type}</span>
                        </label>
                    ))}
                </div>
            </div>
        </div>
    );

    return (
        <>
            {/* Desktop Sidebar */}
            <div className={`hidden md:block w-64 bg-white p-4 rounded-lg shadow-sm border h-fit shrink-0 ${className}`}>
                {content}
            </div>

            {/* Mobile Drawer */}
            {isOpen && (
                <div className="fixed inset-0 z-50 flex md:hidden">
                    <div className="absolute inset-0 bg-black/50" onClick={onClose} />
                    <div className="relative w-4/5 max-w-sm bg-white h-full p-4 shadow-xl overflow-y-auto">
                        {content}
                    </div>
                </div>
            )}
        </>
    );
};

export default FilterPanel;
