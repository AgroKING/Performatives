'use client';

import React from 'react';
import { CheckCircle2, AlertCircle, TrendingUp, Award } from 'lucide-react';

interface SkillGapListProps {
    matchedSkills: Array<{
        skill_id: string;
        skill_name?: string;
        current_proficiency: number;
        required_proficiency: number;
        meets_requirement: boolean;
    }>;
    missingSkills: Array<{
        skill_id: string;
        skill_name?: string;
        current_proficiency: number;
        required_proficiency: number;
        gap_score: number;
        priority: 'Critical' | 'High' | 'Medium' | 'Low';
    }>;
}

export default function SkillGapList({ matchedSkills, missingSkills }: SkillGapListProps) {
    const getPriorityColor = (priority: string) => {
        switch (priority) {
            case 'Critical': return 'text-danger-600 bg-danger-50 border-danger-200';
            case 'High': return 'text-warning-600 bg-warning-50 border-warning-200';
            case 'Medium': return 'text-primary-600 bg-primary-50 border-primary-200';
            case 'Low': return 'text-slate-600 bg-slate-50 border-slate-200';
            default: return 'text-slate-600 bg-slate-50 border-slate-200';
        }
    };

    const matchingSkills = matchedSkills.filter(s => s.meets_requirement);
    const improvementSkills = matchedSkills.filter(s => !s.meets_requirement);

    return (
        <div className="card animate-fade-in">
            <h2 className="card-header flex items-center gap-2">
                <TrendingUp className="w-6 h-6 text-blue-600" />
                Skill Gap Analysis
            </h2>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Matching Skills */}
                <div>
                    <div className="flex items-center gap-2 mb-4">
                        <CheckCircle2 className="w-5 h-5 text-success-600" />
                        <h3 className="text-lg font-semibold text-slate-800">
                            Matching Skills ({matchingSkills.length})
                        </h3>
                    </div>

                    <div className="space-y-2 max-h-96 overflow-y-auto pr-2">
                        {matchingSkills.length === 0 ? (
                            <p className="text-sm text-slate-500 italic">No skills meet the requirements yet</p>
                        ) : (
                            matchingSkills.map((skill, index) => (
                                <div
                                    key={skill.skill_id}
                                    className="flex items-center justify-between p-3 bg-success-50 border border-success-200 rounded-lg hover:shadow-md transition-all"
                                >
                                    <div className="flex items-center gap-3">
                                        <CheckCircle2 className="w-5 h-5 text-success-600 flex-shrink-0" />
                                        <div>
                                            <div className="font-medium text-slate-800">
                                                {skill.skill_name || skill.skill_id}
                                            </div>
                                            <div className="text-xs text-slate-600">
                                                Proficiency: {skill.current_proficiency}/10
                                            </div>
                                        </div>
                                    </div>
                                    {skill.current_proficiency >= skill.required_proficiency + 2 && (
                                        <Award className="w-5 h-5 text-success-600" />
                                    )}
                                </div>
                            ))
                        )}
                    </div>
                </div>

                {/* Missing/Gap Skills */}
                <div>
                    <div className="flex items-center gap-2 mb-4">
                        <AlertCircle className="w-5 h-5 text-danger-600" />
                        <h3 className="text-lg font-semibold text-slate-800">
                            Skills to Learn ({missingSkills.length + improvementSkills.length})
                        </h3>
                    </div>

                    <div className="space-y-2 max-h-96 overflow-y-auto pr-2">
                        {/* Skills needing improvement */}
                        {improvementSkills.map((skill, index) => (
                            <div
                                key={skill.skill_id}
                                className="flex items-center justify-between p-3 bg-warning-50 border border-warning-200 rounded-lg hover:shadow-md transition-all"
                            >
                                <div className="flex items-center gap-3 flex-1">
                                    <AlertCircle className="w-5 h-5 text-warning-600 flex-shrink-0" />
                                    <div className="flex-1">
                                        <div className="font-medium text-slate-800">
                                            {skill.skill_name || skill.skill_id}
                                        </div>
                                        <div className="text-xs text-slate-600">
                                            {skill.current_proficiency}/10 → {skill.required_proficiency}/10 required
                                        </div>
                                    </div>
                                </div>
                                <span className="badge badge-warning text-xs">Improve</span>
                            </div>
                        ))}

                        {/* Missing skills */}
                        {missingSkills
                            .sort((a, b) => {
                                const priorityOrder = { 'Critical': 0, 'High': 1, 'Medium': 2, 'Low': 3 };
                                return priorityOrder[a.priority] - priorityOrder[b.priority];
                            })
                            .map((skill, index) => (
                                <div
                                    key={skill.skill_id}
                                    className={`flex items-center justify-between p-3 border rounded-lg hover:shadow-md transition-all ${getPriorityColor(skill.priority)}`}
                                >
                                    <div className="flex items-center gap-3 flex-1">
                                        <AlertCircle className="w-5 h-5 flex-shrink-0" />
                                        <div className="flex-1">
                                            <div className="font-medium text-slate-800">
                                                {skill.skill_name || skill.skill_id}
                                            </div>
                                            <div className="text-xs text-slate-600">
                                                Gap: {skill.gap_score} points ({skill.current_proficiency} → {skill.required_proficiency})
                                            </div>
                                        </div>
                                    </div>
                                    <span className={`badge text-xs ${getPriorityColor(skill.priority)}`}>
                                        {skill.priority}
                                    </span>
                                </div>
                            ))}
                    </div>
                </div>
            </div>

            {/* Summary */}
            <div className="mt-6 p-4 bg-gradient-to-r from-slate-50 to-blue-50 rounded-lg border border-slate-200">
                <div className="grid grid-cols-3 gap-4 text-center">
                    <div>
                        <div className="text-2xl font-bold text-success-600">{matchingSkills.length}</div>
                        <div className="text-xs text-slate-600 mt-1">Skills Met</div>
                    </div>
                    <div>
                        <div className="text-2xl font-bold text-warning-600">{improvementSkills.length}</div>
                        <div className="text-xs text-slate-600 mt-1">Need Improvement</div>
                    </div>
                    <div>
                        <div className="text-2xl font-bold text-danger-600">{missingSkills.length}</div>
                        <div className="text-xs text-slate-600 mt-1">To Learn</div>
                    </div>
                </div>
            </div>
        </div>
    );
}
