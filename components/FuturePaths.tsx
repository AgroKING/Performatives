'use client';

import React from 'react';
import { Rocket, ArrowRight, Star, Briefcase } from 'lucide-react';

interface CareerPath {
    role: string;
    seniority_level: string;
    typical_years: number;
    key_skills: string[];
    description: string;
}

interface FuturePathsProps {
    currentTargetRole: string;
    targetRoleSeniority: string;
}

export default function FuturePaths({ currentTargetRole, targetRoleSeniority }: FuturePathsProps) {
    // Generate future career paths based on target role
    const getFuturePaths = (): CareerPath[] => {
        const roleLower = currentTargetRole.toLowerCase();

        // Senior Full Stack paths
        if (roleLower.includes('senior') && roleLower.includes('full stack')) {
            return [
                {
                    role: 'Principal Engineer',
                    seniority_level: 'Principal',
                    typical_years: 3,
                    key_skills: ['System Design', 'Technical Leadership', 'Architecture', 'Mentoring'],
                    description: 'Lead complex technical initiatives and mentor senior engineers'
                },
                {
                    role: 'Engineering Manager',
                    seniority_level: 'Lead',
                    typical_years: 2,
                    key_skills: ['People Management', 'Project Planning', 'Stakeholder Communication', 'Team Building'],
                    description: 'Manage engineering teams and drive product delivery'
                },
                {
                    role: 'Solutions Architect',
                    seniority_level: 'Lead',
                    typical_years: 3,
                    key_skills: ['Cloud Architecture', 'Enterprise Patterns', 'Client Engagement', 'Technical Sales'],
                    description: 'Design enterprise-scale solutions for clients'
                }
            ];
        }

        // DevOps paths
        if (roleLower.includes('devops')) {
            return [
                {
                    role: 'Cloud Architect',
                    seniority_level: 'Lead',
                    typical_years: 3,
                    key_skills: ['Multi-cloud Strategy', 'Cost Optimization', 'Security', 'Compliance'],
                    description: 'Design and implement cloud infrastructure at scale'
                },
                {
                    role: 'Site Reliability Engineer (SRE) Lead',
                    seniority_level: 'Lead',
                    typical_years: 2,
                    key_skills: ['Incident Management', 'SLO/SLA Design', 'Automation', 'Observability'],
                    description: 'Ensure system reliability and lead SRE practices'
                },
                {
                    role: 'VP of Engineering',
                    seniority_level: 'Executive',
                    typical_years: 5,
                    key_skills: ['Strategic Planning', 'Budget Management', 'Org Design', 'Executive Leadership'],
                    description: 'Lead engineering organization and set technical strategy'
                }
            ];
        }

        // Frontend Architect paths
        if (roleLower.includes('frontend') && roleLower.includes('architect')) {
            return [
                {
                    role: 'Head of Frontend Engineering',
                    seniority_level: 'Lead',
                    typical_years: 2,
                    key_skills: ['Team Leadership', 'Frontend Strategy', 'Performance Optimization', 'Developer Experience'],
                    description: 'Lead frontend engineering teams and set technical direction'
                },
                {
                    role: 'Principal Engineer (Frontend)',
                    seniority_level: 'Principal',
                    typical_years: 3,
                    key_skills: ['Framework Design', 'Design Systems', 'Web Standards', 'Technical Writing'],
                    description: 'Drive frontend innovation and establish best practices'
                },
                {
                    role: 'CTO (Startup)',
                    seniority_level: 'Executive',
                    typical_years: 4,
                    key_skills: ['Product Vision', 'Tech Stack Selection', 'Hiring', 'Fundraising'],
                    description: 'Lead technology strategy for a startup'
                }
            ];
        }

        // Backend paths
        if (roleLower.includes('backend')) {
            return [
                {
                    role: 'Staff Engineer (Backend)',
                    seniority_level: 'Staff',
                    typical_years: 2,
                    key_skills: ['Distributed Systems', 'Database Optimization', 'API Design', 'Performance Tuning'],
                    description: 'Solve complex backend challenges and mentor teams'
                },
                {
                    role: 'Data Engineering Lead',
                    seniority_level: 'Lead',
                    typical_years: 3,
                    key_skills: ['Data Pipelines', 'ETL', 'Data Warehousing', 'Analytics'],
                    description: 'Build and manage data infrastructure at scale'
                },
                {
                    role: 'Platform Engineer',
                    seniority_level: 'Senior',
                    typical_years: 2,
                    key_skills: ['Internal Tools', 'Developer Productivity', 'Platform APIs', 'Infrastructure'],
                    description: 'Build platforms that empower other engineers'
                }
            ];
        }

        // Database Administrator paths
        if (roleLower.includes('database')) {
            return [
                {
                    role: 'Principal Database Architect',
                    seniority_level: 'Principal',
                    typical_years: 3,
                    key_skills: ['Database Strategy', 'Sharding', 'Replication', 'Disaster Recovery'],
                    description: 'Design database architecture for enterprise systems'
                },
                {
                    role: 'Data Platform Lead',
                    seniority_level: 'Lead',
                    typical_years: 3,
                    key_skills: ['Data Governance', 'Platform Engineering', 'Team Leadership', 'Data Security'],
                    description: 'Lead data platform teams and strategy'
                }
            ];
        }

        // Default paths
        return [
            {
                role: 'Technical Lead',
                seniority_level: 'Lead',
                typical_years: 2,
                key_skills: ['Technical Leadership', 'Architecture', 'Mentoring', 'Project Management'],
                description: 'Lead technical projects and mentor team members'
            },
            {
                role: 'Engineering Manager',
                seniority_level: 'Lead',
                typical_years: 3,
                key_skills: ['People Management', 'Agile Practices', 'Performance Reviews', 'Hiring'],
                description: 'Manage engineering teams and drive delivery'
            },
            {
                role: 'Solutions Architect',
                seniority_level: 'Lead',
                typical_years: 3,
                key_skills: ['System Design', 'Client Engagement', 'Technical Consulting', 'Presales'],
                description: 'Design solutions for enterprise clients'
            }
        ];
    };

    const futurePaths = getFuturePaths();

    const getSeniorityColor = (level: string): string => {
        switch (level.toLowerCase()) {
            case 'staff': return 'from-blue-500 to-indigo-600';
            case 'principal': return 'from-purple-500 to-pink-600';
            case 'lead': return 'from-indigo-500 to-purple-600';
            case 'executive': return 'from-pink-500 to-rose-600';
            default: return 'from-slate-500 to-slate-600';
        }
    };

    return (
        <div className="card animate-fade-in">
            <div className="flex items-center gap-3 mb-6">
                <div className="p-3 bg-gradient-to-br from-pink-500 to-rose-600 rounded-xl">
                    <Rocket className="w-6 h-6 text-white" />
                </div>
                <div>
                    <h2 className="text-2xl font-bold text-slate-800">Future Career Paths</h2>
                    <p className="text-sm text-slate-600">What comes after {currentTargetRole}</p>
                </div>
            </div>

            <div className="space-y-4">
                {futurePaths.map((path, index) => (
                    <div
                        key={index}
                        className="group p-5 bg-gradient-to-br from-slate-50 to-blue-50 border border-slate-200 rounded-lg hover:shadow-lg hover:border-blue-300 transition-all cursor-pointer"
                    >
                        <div className="flex items-start justify-between mb-3">
                            <div className="flex-1">
                                <div className="flex items-center gap-3 mb-2">
                                    <h3 className="text-xl font-bold text-slate-800 group-hover:text-blue-600 transition-colors">
                                        {path.role}
                                    </h3>
                                    <div className={`px-3 py-1 rounded-full text-xs font-semibold text-white bg-gradient-to-r ${getSeniorityColor(path.seniority_level)}`}>
                                        {path.seniority_level}
                                    </div>
                                </div>
                                <p className="text-sm text-slate-600 mb-3">{path.description}</p>
                            </div>
                            <ArrowRight className="w-5 h-5 text-slate-400 group-hover:text-blue-600 group-hover:translate-x-1 transition-all flex-shrink-0 ml-3" />
                        </div>

                        <div className="flex items-center gap-2 mb-3">
                            <Briefcase className="w-4 h-4 text-slate-500" />
                            <span className="text-sm text-slate-600">
                                Typical progression: <strong>{path.typical_years} years</strong> from {currentTargetRole}
                            </span>
                        </div>

                        <div>
                            <div className="flex items-center gap-2 mb-2">
                                <Star className="w-4 h-4 text-amber-500" />
                                <span className="text-sm font-semibold text-slate-700">Key Skills Required:</span>
                            </div>
                            <div className="flex flex-wrap gap-2">
                                {path.key_skills.map((skill, skillIndex) => (
                                    <span
                                        key={skillIndex}
                                        className="px-3 py-1 bg-white border border-slate-200 rounded-full text-xs font-medium text-slate-700 hover:border-blue-300 hover:bg-blue-50 transition-colors"
                                    >
                                        {skill}
                                    </span>
                                ))}
                            </div>
                        </div>
                    </div>
                ))}
            </div>

            <div className="mt-6 p-4 bg-gradient-to-r from-purple-500 to-pink-600 rounded-lg text-white">
                <div className="flex items-center gap-2 mb-2">
                    <Rocket className="w-5 h-5" />
                    <h3 className="font-semibold">Career Growth Tip</h3>
                </div>
                <p className="text-sm opacity-90">
                    Focus on building both technical depth and leadership skills. Many senior roles require
                    a combination of technical excellence and the ability to influence and mentor others.
                </p>
            </div>
        </div>
    );
}
