'use client';

import React from 'react';
import { TrendingUp, Users, Award, ArrowRight } from 'lucide-react';

interface SimilarTransition {
    from_role: string;
    to_role: string;
    success_rate: number;
    avg_duration_months: number;
    sample_size: number;
}

export default function SimilarTransitionsSidebar() {
    // Mock data for similar transitions
    const transitions: SimilarTransition[] = [
        {
            from_role: 'Junior Developer',
            to_role: 'Senior Full Stack',
            success_rate: 78,
            avg_duration_months: 18,
            sample_size: 245
        },
        {
            from_role: 'Frontend Developer',
            to_role: 'Full Stack Developer',
            success_rate: 85,
            avg_duration_months: 12,
            sample_size: 412
        },
        {
            from_role: 'Backend Developer',
            to_role: 'DevOps Engineer',
            success_rate: 72,
            avg_duration_months: 15,
            sample_size: 189
        },
        {
            from_role: 'Mid-Level Developer',
            to_role: 'Senior Developer',
            success_rate: 82,
            avg_duration_months: 14,
            sample_size: 567
        },
    ];

    const getSuccessRateColor = (rate: number) => {
        if (rate >= 80) return 'text-success-600 bg-success-100';
        if (rate >= 60) return 'text-primary-600 bg-primary-100';
        return 'text-warning-600 bg-warning-100';
    };

    return (
        <div className="card animate-fade-in sticky top-6">
            <div className="flex items-center gap-3 mb-6">
                <div className="p-3 bg-gradient-to-br from-emerald-500 to-teal-600 rounded-xl">
                    <TrendingUp className="w-6 h-6 text-white" />
                </div>
                <div>
                    <h2 className="text-xl font-bold text-slate-800">Similar Transitions</h2>
                    <p className="text-sm text-slate-600">Success rates from peers</p>
                </div>
            </div>

            <div className="space-y-4">
                {transitions.map((transition, index) => (
                    <div
                        key={index}
                        className="p-4 bg-gradient-to-br from-slate-50 to-blue-50 border border-slate-200 rounded-lg hover:shadow-md transition-all"
                    >
                        <div className="flex items-start gap-2 mb-3">
                            <div className="flex-1">
                                <div className="text-sm font-medium text-slate-700">{transition.from_role}</div>
                                <div className="flex items-center gap-2 my-1">
                                    <ArrowRight className="w-4 h-4 text-blue-600" />
                                </div>
                                <div className="text-sm font-semibold text-slate-800">{transition.to_role}</div>
                            </div>
                        </div>

                        <div className="space-y-2">
                            <div className="flex items-center justify-between">
                                <span className="text-xs text-slate-600">Success Rate</span>
                                <span className={`badge text-xs font-bold ${getSuccessRateColor(transition.success_rate)}`}>
                                    {transition.success_rate}%
                                </span>
                            </div>

                            <div className="flex items-center justify-between">
                                <span className="text-xs text-slate-600">Avg. Duration</span>
                                <span className="text-xs font-semibold text-slate-800">
                                    {transition.avg_duration_months} months
                                </span>
                            </div>

                            <div className="flex items-center justify-between pt-2 border-t border-slate-200">
                                <div className="flex items-center gap-1">
                                    <Users className="w-3 h-3 text-slate-500" />
                                    <span className="text-xs text-slate-600">{transition.sample_size} transitions</span>
                                </div>
                            </div>
                        </div>
                    </div>
                ))}
            </div>

            <div className="mt-6 p-4 bg-gradient-to-r from-blue-500 to-indigo-600 rounded-lg text-white">
                <div className="flex items-center gap-2 mb-2">
                    <Award className="w-5 h-5" />
                    <h3 className="font-semibold">Pro Tip</h3>
                </div>
                <p className="text-sm opacity-90">
                    Focus on high-priority skills first. Completing foundational skills early accelerates your progress.
                </p>
            </div>
        </div>
    );
}
