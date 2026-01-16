import React from 'react';

const JobCardSkeleton: React.FC = () => {
    return (
        <div className="flex flex-col p-4 bg-white rounded-xl shadow-md border border-gray-100 animate-pulse h-full">
            {/* Header Skeleton */}
            <div className="flex justify-between items-start mb-4">
                <div className="flex gap-3 w-full">
                    {/* Logo Placeholder */}
                    <div className="w-10 h-10 bg-gray-200 rounded-lg"></div>
                    <div className="flex-1 space-y-2">
                        {/* Title Placeholder */}
                        <div className="h-4 bg-gray-200 rounded w-3/4"></div>
                        {/* Company Placeholder */}
                        <div className="h-3 bg-gray-200 rounded w-1/2"></div>
                    </div>
                </div>
                {/* Ring Placeholder */}
                <div className="w-10 h-10 rounded-full bg-gray-200 shrink-0"></div>
            </div>

            {/* Details Skeleton */}
            <div className="flex flex-col gap-2 mb-4">
                <div className="h-3 bg-gray-200 rounded w-1/3"></div>
                <div className="h-3 bg-gray-200 rounded w-1/4"></div>
                <div className="h-3 bg-gray-200 rounded w-1/2"></div>
            </div>

            {/* Footer Skeleton */}
            <div className="flex justify-between items-end mt-auto">
                <div className="flex gap-1">
                    <div className="w-12 h-4 bg-gray-200 rounded-full"></div>
                    <div className="w-12 h-4 bg-gray-200 rounded-full"></div>
                    <div className="w-8 h-4 bg-gray-200 rounded-full"></div>
                </div>
                <div className="w-8 h-8 bg-gray-200 rounded-full"></div>
            </div>
        </div>
    );
};

export default JobCardSkeleton;
