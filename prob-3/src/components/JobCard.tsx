import React, { useState } from 'react';
import { Job } from '../types';
import MatchRing from './MatchRing';
import { Heart, Briefcase, MapPin, DollarSign, Clock } from 'lucide-react';

interface JobCardProps {
    job: Job;
    viewMode: 'grid' | 'list';
    isSaved: boolean;
    onToggleSave: () => void;
}

const JobCard: React.FC<JobCardProps> = ({ job, viewMode, isSaved, onToggleSave }) => {
    // const [isSaved, setIsSaved] = useState(false);

    const containerClass = viewMode === 'grid'
        ? 'flex flex-col p-4 bg-white rounded-xl shadow-md border border-gray-100 hover:shadow-lg transition-shadow'
        : 'flex flex-row p-4 bg-white rounded-xl shadow-md border border-gray-100 hover:shadow-lg transition-shadow items-center gap-4';

    return (
        <div className={containerClass}>
            {/* Header / Top Section */}
            <div className={`flex justify-between items-start ${viewMode === 'grid' ? 'mb-4' : 'flex-1'}`}>
                <div className="flex gap-3">
                    {/* Company Logo Placeholder */}
                    <div className="w-10 h-10 bg-gray-100 rounded-lg flex items-center justify-center text-gray-500 font-bold text-xs">
                        {job.company.substring(0, 2).toUpperCase()}
                    </div>
                    <div>
                        <h3 className="font-bold text-gray-800 text-lg leading-tight truncate max-w-[200px]" title={job.title}>{job.title}</h3>
                        <p className="text-sm text-gray-500 font-medium">{job.company}</p>
                    </div>
                </div>

                {/* Match Ring */}
                <div className="shrink-0">
                    <MatchRing score={job.matchScore} size={40} />
                </div>
            </div>

            {/* Details Section */}
            <div className={`flex flex-col gap-2 text-sm text-gray-600 ${viewMode === 'grid' ? 'mb-4' : 'flex-1 grid grid-cols-2 gap-x-4'}`}>
                <div className="flex items-center gap-1.5">
                    <MapPin size={14} className="text-gray-400" />
                    <span>{job.location.city}, {job.location.country}</span>
                </div>
                <div className="flex items-center gap-1.5">
                    <DollarSign size={14} className="text-gray-400" />
                    <span>${(job.salary.min / 1000).toFixed(0)}k - ${(job.salary.max / 1000).toFixed(0)}k</span>
                </div>
                <div className="flex items-center gap-1.5">
                    <Briefcase size={14} className="text-gray-400" />
                    <span>{job.type}</span>
                </div>
                <div className="flex items-center gap-1.5">
                    <Clock size={14} className="text-gray-400" />
                    <span>{new Date(job.postedAt).toLocaleDateString()}</span>
                </div>
            </div>

            {/* Skills & Actions */}
            <div className={`flex justify-between items-end ${viewMode === 'grid' ? '' : 'shrink-0 flex-col items-end gap-2'}`}>
                <div className="flex flex-wrap gap-1 max-w-[200px] max-h-[48px] overflow-hidden">
                    {job.skills.slice(0, 3).map(skill => (
                        <span key={skill} className="px-2 py-0.5 bg-gray-100 text-gray-600 text-xs rounded-full">{skill}</span>
                    ))}
                    {job.skills.length > 3 && <span className="px-2 py-0.5 text-gray-400 text-xs">+{job.skills.length - 3}</span>}
                </div>

                <button
                    onClick={onToggleSave}
                    className={`p-2 rounded-full transition-colors ${isSaved ? 'text-red-500 bg-red-50' : 'text-gray-400 hover:bg-gray-100'}`}
                >
                    <Heart size={20} fill={isSaved ? "currentColor" : "none"} />
                </button>
            </div>
        </div>
    );
};

export default JobCard;
