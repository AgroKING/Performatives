'use client';

import React from 'react';
import { RadialBarChart, RadialBar, PolarAngleAxis, ResponsiveContainer } from 'recharts';
import { Target, TrendingUp } from 'lucide-react';

interface ReadinessScoreCardProps {
    score: number;
    targetRole: string;
    experienceMatch: {
        candidate_years: number;
        required_years: number;
        meets_requirement: boolean;
    };
}

export default function ReadinessScoreCard({ score, targetRole, experienceMatch }: ReadinessScoreCardProps) {
    const data = [
        {
            name: 'Readiness',
            value: score,
            fill: score >= 75 ? '#22c55e' : score >= 50 ? '#eab308' : '#ef4444',
        },
    ];

    const getScoreLabel = (score: number) => {
        if (score >= 80) return { text: 'Excellent', color: 'text-success-600' };
        if (score >= 60) return { text: 'Good', color: 'text-primary-600' };
        if (score >= 40) return { text: 'Fair', color: 'text-warning-600' };
        return { text: 'Needs Work', color: 'text-danger-600' };
    };

    const scoreLabel = getScoreLabel(score);

    return (
        <div className="card animate-fade-in">
            <div className="flex items-center justify-between mb-6">
                <div className="flex items-center gap-3">
                    <div className="p-3 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-xl">
                        <Target className="w-6 h-6 text-white" />
                    </div>
                    <div>
                        <h2 className="text-2xl font-bold text-slate-800">Readiness Score</h2>
                        <p className="text-sm text-slate-600">for {targetRole}</p>
                    </div>
                </div>
            </div>

            <div className="flex items-center justify-between gap-8">
                {/* Radial Progress Chart */}
                <div className="relative flex-shrink-0">
                    <ResponsiveContainer width={200} height={200}>
                        <RadialBarChart
                            cx="50%"
                            cy="50%"
                            innerRadius="70%"
                            outerRadius="100%"
                            barSize={20}
                            data={data}
                            startAngle={90}
                            endAngle={-270}
                        >
                            <PolarAngleAxis type="number" domain={[0, 100]} angleAxisId={0} tick={false} />
                            <RadialBar
                                background
                                dataKey="value"
                                cornerRadius={10}
                                fill={data[0].fill}
                            />
                        </RadialBarChart>
                    </ResponsiveContainer>
                    <div className="absolute inset-0 flex items-center justify-center flex-col">
                        <div className="text-5xl font-bold text-slate-800">{score}</div>
                        <div className="text-sm text-slate-500">out of 100</div>
                    </div>
                </div>

                {/* Score Details */}
                <div className="flex-1 space-y-4">
                    <div className="flex items-center gap-3">
                        <div className={`text-2xl font-bold ${scoreLabel.color}`}>
                            {scoreLabel.text}
                        </div>
                    </div>

                    <div className="space-y-3">
                        <div className="flex items-center justify-between p-3 bg-slate-50 rounded-lg">
                            <span className="text-sm font-medium text-slate-700">Experience Match</span>
                            <div className="flex items-center gap-2">
                                <TrendingUp className={`w-4 h-4 ${experienceMatch.meets_requirement ? 'text-success-600' : 'text-warning-600'}`} />
                                <span className="text-sm font-semibold">
                                    {experienceMatch.candidate_years} / {experienceMatch.required_years} years
                                </span>
                            </div>
                        </div>

                        <div className="p-4 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg border border-blue-200">
                            <p className="text-sm text-slate-700">
                                {score >= 80 && "You're well-prepared for this role! Focus on the remaining gaps to become fully qualified."}
                                {score >= 60 && score < 80 && "You're on the right track! With focused learning, you can reach this role soon."}
                                {score >= 40 && score < 60 && "You have a solid foundation. A structured learning plan will help you bridge the gaps."}
                                {score < 40 && "This role requires significant upskilling. Follow the roadmap to systematically build required skills."}
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
