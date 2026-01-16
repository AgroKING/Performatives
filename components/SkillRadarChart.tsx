'use client';

import React from 'react';
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, Legend, Tooltip } from 'recharts';
import { Activity } from 'lucide-react';

interface SkillRadarChartProps {
    currentSkills: { [category: string]: number };
    targetSkills: { [category: string]: number };
}

export default function SkillRadarChart({ currentSkills, targetSkills }: SkillRadarChartProps) {
    // Prepare data for radar chart
    const categories = ['Frontend', 'Backend', 'DevOps', 'Database'];

    const data = categories.map(category => ({
        category,
        current: currentSkills[category] || 0,
        target: targetSkills[category] || 0,
    }));

    return (
        <div className="card animate-fade-in">
            <div className="flex items-center gap-3 mb-6">
                <div className="p-3 bg-gradient-to-br from-purple-500 to-pink-600 rounded-xl">
                    <Activity className="w-6 h-6 text-white" />
                </div>
                <div>
                    <h2 className="card-header mb-0">Skills Radar</h2>
                    <p className="text-sm text-slate-600">Current vs Target Proficiency</p>
                </div>
            </div>

            <ResponsiveContainer width="100%" height={400}>
                <RadarChart data={data}>
                    <PolarGrid stroke="#cbd5e1" />
                    <PolarAngleAxis
                        dataKey="category"
                        tick={{ fill: '#475569', fontSize: 14, fontWeight: 500 }}
                    />
                    <PolarRadiusAxis
                        angle={90}
                        domain={[0, 10]}
                        tick={{ fill: '#94a3b8', fontSize: 12 }}
                    />
                    <Radar
                        name="Current Skills"
                        dataKey="current"
                        stroke="#3b82f6"
                        fill="#3b82f6"
                        fillOpacity={0.3}
                        strokeWidth={2}
                    />
                    <Radar
                        name="Target Skills"
                        dataKey="target"
                        stroke="#8b5cf6"
                        fill="#8b5cf6"
                        fillOpacity={0.3}
                        strokeWidth={2}
                    />
                    <Legend
                        wrapperStyle={{ paddingTop: '20px' }}
                        iconType="circle"
                    />
                    <Tooltip
                        contentStyle={{
                            backgroundColor: 'white',
                            border: '1px solid #e2e8f0',
                            borderRadius: '8px',
                            padding: '12px',
                        }}
                    />
                </RadarChart>
            </ResponsiveContainer>

            <div className="mt-4 grid grid-cols-2 gap-3">
                <div className="p-3 bg-blue-50 rounded-lg border border-blue-200">
                    <div className="flex items-center gap-2">
                        <div className="w-3 h-3 rounded-full bg-blue-500"></div>
                        <span className="text-sm font-medium text-slate-700">Current Skills</span>
                    </div>
                </div>
                <div className="p-3 bg-purple-50 rounded-lg border border-purple-200">
                    <div className="flex items-center gap-2">
                        <div className="w-3 h-3 rounded-full bg-purple-500"></div>
                        <span className="text-sm font-medium text-slate-700">Target Skills</span>
                    </div>
                </div>
            </div>
        </div>
    );
}
