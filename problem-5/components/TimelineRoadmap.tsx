'use client';

import React, { useState } from 'react';
import { MapPin, Clock, BookOpen, ExternalLink, ChevronDown, ChevronUp } from 'lucide-react';

interface LearningPathStep {
    order: number;
    skill_id: string;
    skill_name: string;
    difficulty?: number;
    estimated_weeks: number;
    prerequisites?: string[];
    prerequisites_met?: boolean;
    reason?: string;
}

interface LearningPhase {
    phase_number: number;
    phase_name: string;
    estimated_weeks: number;
    skills: LearningPathStep[];
}

interface Resource {
    type: 'course' | 'documentation' | 'tutorial' | 'book' | 'video';
    title: string;
    url: string;
    duration?: string;
    difficulty: 'Beginner' | 'Intermediate' | 'Advanced';
}

interface TimelineRoadmapProps {
    phases: LearningPhase[];
    recommendedResources: Array<{
        skill_id: string;
        skill_name: string;
        resources: Resource[];
    }>;
}

export default function TimelineRoadmap({ phases, recommendedResources }: TimelineRoadmapProps) {
    const [expandedSkill, setExpandedSkill] = useState<string | null>(null);

    const getPhaseColor = (phaseName: string) => {
        if (phaseName.includes('Fundamental')) return 'from-green-500 to-emerald-600';
        if (phaseName.includes('Intermediate')) return 'from-blue-500 to-indigo-600';
        if (phaseName.includes('Advanced')) return 'from-purple-500 to-pink-600';
        return 'from-slate-500 to-slate-600';
    };

    const getDifficultyColor = (difficulty?: number) => {
        if (!difficulty) return 'bg-slate-100 text-slate-700';
        if (difficulty <= 3) return 'bg-success-100 text-success-700';
        if (difficulty <= 6) return 'bg-primary-100 text-primary-700';
        return 'bg-danger-100 text-danger-700';
    };

    const getResourceIcon = (type: string) => {
        switch (type) {
            case 'course': return '🎓';
            case 'documentation': return '📚';
            case 'tutorial': return '📝';
            case 'book': return '📖';
            case 'video': return '🎥';
            default: return '📄';
        }
    };

    const toggleSkillExpansion = (skillId: string) => {
        setExpandedSkill(expandedSkill === skillId ? null : skillId);
    };

    const getSkillResources = (skillId: string) => {
        return recommendedResources.find(r => r.skill_id === skillId)?.resources || [];
    };

    return (
        <div className="card animate-fade-in">
            <div className="flex items-center gap-3 mb-6">
                <div className="p-3 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-xl">
                    <MapPin className="w-6 h-6 text-white" />
                </div>
                <div>
                    <h2 className="card-header mb-0">Learning Roadmap</h2>
                    <p className="text-sm text-slate-600">
                        {phases.length} phases • {phases.reduce((sum, p) => sum + p.estimated_weeks, 0)} weeks total
                    </p>
                </div>
            </div>

            <div className="relative">
                {/* Vertical Timeline Line */}
                <div className="absolute left-8 top-0 bottom-0 w-0.5 bg-gradient-to-b from-blue-200 via-purple-200 to-pink-200"></div>

                <div className="space-y-8">
                    {phases.map((phase, phaseIndex) => (
                        <div key={phase.phase_number} className="relative animate-slide-up" style={{ animationDelay: `${phaseIndex * 100}ms` }}>
                            {/* Phase Header */}
                            <div className="flex items-start gap-4 mb-4">
                                <div className={`relative z-10 flex-shrink-0 w-16 h-16 rounded-full bg-gradient-to-br ${getPhaseColor(phase.phase_name)} flex items-center justify-center shadow-lg`}>
                                    <span className="text-white font-bold text-lg">{phase.phase_number}</span>
                                </div>
                                <div className="flex-1 pt-2">
                                    <h3 className="text-xl font-bold text-slate-800">{phase.phase_name}</h3>
                                    <div className="flex items-center gap-4 mt-1 text-sm text-slate-600">
                                        <div className="flex items-center gap-1">
                                            <Clock className="w-4 h-4" />
                                            <span>{phase.estimated_weeks} weeks</span>
                                        </div>
                                        <div className="flex items-center gap-1">
                                            <BookOpen className="w-4 h-4" />
                                            <span>{phase.skills.length} skills</span>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            {/* Skills in Phase */}
                            <div className="ml-20 space-y-3">
                                {phase.skills.map((skill, skillIndex) => {
                                    const resources = getSkillResources(skill.skill_id);
                                    const isExpanded = expandedSkill === skill.skill_id;

                                    return (
                                        <div
                                            key={skill.skill_id}
                                            className="bg-white border border-slate-200 rounded-lg shadow-sm hover:shadow-md transition-all overflow-hidden"
                                        >
                                            {/* Skill Header */}
                                            <div
                                                className="p-4 cursor-pointer hover:bg-slate-50 transition-colors"
                                                onClick={() => toggleSkillExpansion(skill.skill_id)}
                                            >
                                                <div className="flex items-center justify-between">
                                                    <div className="flex-1">
                                                        <div className="flex items-center gap-3">
                                                            <span className="text-sm font-semibold text-slate-500">#{skill.order}</span>
                                                            <h4 className="text-lg font-semibold text-slate-800">{skill.skill_name}</h4>
                                                            {skill.difficulty && (
                                                                <span className={`badge text-xs ${getDifficultyColor(skill.difficulty)}`}>
                                                                    Level {skill.difficulty}
                                                                </span>
                                                            )}
                                                        </div>
                                                        <div className="flex items-center gap-4 mt-2 text-sm text-slate-600">
                                                            <div className="flex items-center gap-1">
                                                                <Clock className="w-4 h-4" />
                                                                <span>{skill.estimated_weeks} weeks</span>
                                                            </div>
                                                            {resources.length > 0 && (
                                                                <div className="flex items-center gap-1">
                                                                    <BookOpen className="w-4 h-4" />
                                                                    <span>{resources.length} resources</span>
                                                                </div>
                                                            )}
                                                        </div>
                                                    </div>
                                                    <button className="p-2 hover:bg-slate-100 rounded-lg transition-colors">
                                                        {isExpanded ? (
                                                            <ChevronUp className="w-5 h-5 text-slate-600" />
                                                        ) : (
                                                            <ChevronDown className="w-5 h-5 text-slate-600" />
                                                        )}
                                                    </button>
                                                </div>
                                            </div>

                                            {/* Expanded Resources */}
                                            {isExpanded && resources.length > 0 && (
                                                <div className="px-4 pb-4 border-t border-slate-100 bg-slate-50">
                                                    <h5 className="text-sm font-semibold text-slate-700 mt-3 mb-2 flex items-center gap-2">
                                                        <BookOpen className="w-4 h-4" />
                                                        Recommended Resources
                                                    </h5>
                                                    <div className="space-y-2">
                                                        {resources.map((resource, idx) => (
                                                            <a
                                                                key={idx}
                                                                href={resource.url}
                                                                target="_blank"
                                                                rel="noopener noreferrer"
                                                                className="flex items-center justify-between p-3 bg-white border border-slate-200 rounded-lg hover:border-blue-300 hover:shadow-sm transition-all group"
                                                            >
                                                                <div className="flex items-center gap-3">
                                                                    <span className="text-2xl">{getResourceIcon(resource.type)}</span>
                                                                    <div>
                                                                        <div className="font-medium text-slate-800 group-hover:text-blue-600 transition-colors">
                                                                            {resource.title}
                                                                        </div>
                                                                        <div className="flex items-center gap-2 mt-1">
                                                                            <span className="text-xs text-slate-500 capitalize">{resource.type}</span>
                                                                            {resource.duration && (
                                                                                <>
                                                                                    <span className="text-xs text-slate-400">•</span>
                                                                                    <span className="text-xs text-slate-500">{resource.duration}</span>
                                                                                </>
                                                                            )}
                                                                            <span className="text-xs text-slate-400">•</span>
                                                                            <span className={`text-xs ${resource.difficulty === 'Beginner' ? 'text-success-600' :
                                                                                resource.difficulty === 'Intermediate' ? 'text-primary-600' :
                                                                                    'text-danger-600'
                                                                                }`}>
                                                                                {resource.difficulty}
                                                                            </span>
                                                                        </div>
                                                                    </div>
                                                                </div>
                                                                <ExternalLink className="w-4 h-4 text-slate-400 group-hover:text-blue-600 transition-colors" />
                                                            </a>
                                                        ))}
                                                    </div>
                                                </div>
                                            )}
                                        </div>
                                    );
                                })}
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}
