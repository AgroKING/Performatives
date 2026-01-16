'use client';

import React, { useState } from 'react';
import { Search, User, Target, Code, ChevronDown } from 'lucide-react';

interface CandidatePreset {
    id: string;
    name: string;
    role: string;
    experience_years: number;
    skills: Array<{
        skill_id: string;
        proficiency_level: number;
        years_of_experience: number;
    }>;
}

interface TargetRoleOption {
    id: string;
    title: string;
    seniority_level: string;
}

interface AnalysisFormProps {
    onAnalyze: (candidate: any, targetRoleId: string) => void;
    loading: boolean;
    targetRoles: TargetRoleOption[];
}

export default function AnalysisForm({ onAnalyze, loading, targetRoles }: AnalysisFormProps) {
    const [showDebug, setShowDebug] = useState(false);
    const [selectedPreset, setSelectedPreset] = useState<string>('');
    const [selectedTargetRole, setSelectedTargetRole] = useState<string>('');

    // Preset candidates
    const candidatePresets: CandidatePreset[] = [
        {
            id: 'junior-frontend',
            name: 'Alice Johnson (Junior Frontend)',
            role: 'Junior Frontend Developer',
            experience_years: 2,
            skills: [
                { skill_id: 'fe-001', proficiency_level: 8, years_of_experience: 2 },
                { skill_id: 'fe-002', proficiency_level: 7, years_of_experience: 2 },
                { skill_id: 'fe-003', proficiency_level: 6, years_of_experience: 1.5 },
                { skill_id: 'fe-005', proficiency_level: 5, years_of_experience: 1 },
                { skill_id: 'do-001', proficiency_level: 6, years_of_experience: 2 },
                { skill_id: 'db-001', proficiency_level: 5, years_of_experience: 1 },
            ]
        },
        {
            id: 'mid-backend',
            name: 'Bob Smith (Mid Backend)',
            role: 'Mid-Level Backend Developer',
            experience_years: 4,
            skills: [
                { skill_id: 'be-003', proficiency_level: 8, years_of_experience: 4 },
                { skill_id: 'be-004', proficiency_level: 7, years_of_experience: 3 },
                { skill_id: 'be-006', proficiency_level: 7, years_of_experience: 3 },
                { skill_id: 'db-001', proficiency_level: 7, years_of_experience: 3 },
                { skill_id: 'db-002', proficiency_level: 6, years_of_experience: 2 },
                { skill_id: 'do-001', proficiency_level: 7, years_of_experience: 4 },
                { skill_id: 'do-002', proficiency_level: 6, years_of_experience: 2 },
            ]
        },
        {
            id: 'senior-fullstack',
            name: 'Carol Davis (Senior Full Stack)',
            role: 'Senior Full Stack Developer',
            experience_years: 6,
            skills: [
                { skill_id: 'fe-003', proficiency_level: 9, years_of_experience: 6 },
                { skill_id: 'fe-004', proficiency_level: 8, years_of_experience: 4 },
                { skill_id: 'fe-005', proficiency_level: 9, years_of_experience: 5 },
                { skill_id: 'be-001', proficiency_level: 8, years_of_experience: 5 },
                { skill_id: 'be-002', proficiency_level: 8, years_of_experience: 5 },
                { skill_id: 'db-002', proficiency_level: 7, years_of_experience: 4 },
                { skill_id: 'do-001', proficiency_level: 8, years_of_experience: 6 },
                { skill_id: 'do-003', proficiency_level: 7, years_of_experience: 3 },
            ]
        },
    ];

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();

        if (!selectedPreset || !selectedTargetRole) {
            alert('Please select both a candidate and a target role');
            return;
        }

        const preset = candidatePresets.find(p => p.id === selectedPreset);
        if (!preset) return;

        const candidate = {
            id: `cand-${Date.now()}`,
            name: preset.name,
            email: `${preset.id}@example.com`,
            experience_years: preset.experience_years,
            current_skills: preset.skills,
            created_at: new Date().toISOString(),
            updated_at: new Date().toISOString(),
        };

        onAnalyze(candidate, selectedTargetRole);
    };

    const selectedCandidate = candidatePresets.find(p => p.id === selectedPreset);
    const selectedRole = targetRoles.find(r => r.id === selectedTargetRole);

    return (
        <div className="card animate-fade-in">
            <div className="flex items-center gap-3 mb-6">
                <div className="p-3 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-xl">
                    <Search className="w-6 h-6 text-white" />
                </div>
                <div>
                    <h2 className="text-2xl font-bold text-slate-800">Skill Gap Analyzer</h2>
                    <p className="text-sm text-slate-600">Select a candidate and target role to analyze</p>
                </div>
            </div>

            <form onSubmit={handleSubmit} className="space-y-6">
                {/* Current Role Selection */}
                <div>
                    <label className="flex items-center gap-2 text-sm font-semibold text-slate-700 mb-2">
                        <User className="w-4 h-4" />
                        Current Role / Candidate
                    </label>
                    <div className="relative">
                        <select
                            value={selectedPreset}
                            onChange={(e) => setSelectedPreset(e.target.value)}
                            className="input-field appearance-none pr-10"
                            required
                        >
                            <option value="">Select a candidate...</option>
                            {candidatePresets.map(preset => (
                                <option key={preset.id} value={preset.id}>
                                    {preset.name} - {preset.experience_years} years exp
                                </option>
                            ))}
                        </select>
                        <ChevronDown className="absolute right-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400 pointer-events-none" />
                    </div>
                    {selectedCandidate && (
                        <div className="mt-2 p-3 bg-blue-50 border border-blue-200 rounded-lg">
                            <div className="text-sm text-slate-700">
                                <strong>{selectedCandidate.role}</strong> • {selectedCandidate.skills.length} skills • {selectedCandidate.experience_years} years
                            </div>
                        </div>
                    )}
                </div>

                {/* Target Role Selection */}
                <div>
                    <label className="flex items-center gap-2 text-sm font-semibold text-slate-700 mb-2">
                        <Target className="w-4 h-4" />
                        Target Role
                    </label>
                    <div className="relative">
                        <select
                            value={selectedTargetRole}
                            onChange={(e) => setSelectedTargetRole(e.target.value)}
                            className="input-field appearance-none pr-10"
                            required
                        >
                            <option value="">Select a target role...</option>
                            {targetRoles.map(role => (
                                <option key={role.id} value={role.id}>
                                    {role.title} ({role.seniority_level})
                                </option>
                            ))}
                        </select>
                        <ChevronDown className="absolute right-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400 pointer-events-none" />
                    </div>
                    {selectedRole && (
                        <div className="mt-2 p-3 bg-purple-50 border border-purple-200 rounded-lg">
                            <div className="text-sm text-slate-700">
                                <strong>{selectedRole.title}</strong> • {selectedRole.seniority_level} Level
                            </div>
                        </div>
                    )}
                </div>

                {/* Submit Button */}
                <button
                    type="submit"
                    disabled={loading || !selectedPreset || !selectedTargetRole}
                    className="btn-primary w-full"
                >
                    {loading ? (
                        <span className="flex items-center justify-center gap-2">
                            <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                            Analyzing...
                        </span>
                    ) : (
                        <span className="flex items-center justify-center gap-2">
                            <Code className="w-5 h-5" />
                            Analyze Skill Gap
                        </span>
                    )}
                </button>
            </form>

            {/* Debug View */}
            {selectedCandidate && selectedRole && (
                <div className="mt-6">
                    <button
                        onClick={() => setShowDebug(!showDebug)}
                        className="flex items-center gap-2 text-sm font-medium text-slate-600 hover:text-slate-800 transition-colors"
                    >
                        <Code className="w-4 h-4" />
                        {showDebug ? 'Hide' : 'Show'} Debug View (JSON Input)
                    </button>

                    {showDebug && (
                        <div className="mt-3 p-4 bg-slate-900 rounded-lg overflow-auto max-h-96">
                            <pre className="text-xs text-green-400 font-mono">
                                {JSON.stringify({
                                    candidate: {
                                        id: `cand-${Date.now()}`,
                                        name: selectedCandidate.name,
                                        email: `${selectedCandidate.id}@example.com`,
                                        experience_years: selectedCandidate.experience_years,
                                        current_skills: selectedCandidate.skills,
                                    },
                                    target_role: selectedTargetRole
                                }, null, 2)}
                            </pre>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}
