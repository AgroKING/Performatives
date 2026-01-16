'use client';

import React, { useState, useEffect } from 'react';
import AnalysisForm from '@/components/AnalysisForm';
import ReadinessScoreCard from '@/components/ReadinessScoreCard';
import SkillRadarChart from '@/components/SkillRadarChart';
import SkillGapList from '@/components/SkillGapList';
import TimelineRoadmap from '@/components/TimelineRoadmap';
import SimilarTransitionsSidebar from '@/components/SimilarTransitionsSidebar';
import SalaryProjection from '@/components/SalaryProjection';
import FuturePaths from '@/components/FuturePaths';
import { Sparkles, AlertCircle } from 'lucide-react';
import { Skill, TargetRole } from '@/types/skill-taxonomy';

interface AnalysisData {
    analysis: {
        readiness_score: number;
        target_role_title: string;
        target_role_id: string;
        missing_skills_count: number;
        matched_skills: Array<{
            skill_id: string;
            current_proficiency: number;
            required_proficiency: number;
            meets_requirement: boolean;
        }>;
        skill_gaps: Array<{
            skill_id: string;
            current_proficiency: number;
            required_proficiency: number;
            gap_score: number;
            priority: 'Critical' | 'High' | 'Medium' | 'Low';
        }>;
        experience_match: {
            candidate_years: number;
            required_years: number;
            meets_requirement: boolean;
        };
    };
    learning_roadmap: {
        estimated_total_weeks: number;
        estimated_months: number;
        phases: Array<{
            phase_number: number;
            phase_name: string;
            estimated_weeks: number;
            skills: Array<{
                order: number;
                skill_id: string;
                skill_name: string;
                difficulty?: number;
                estimated_weeks: number;
                prerequisites_met: boolean;
                prerequisites?: string[];
            }>;
        }>;
    };
    recommended_resources: Array<{
        skill_id: string;
        skill_name: string;
        resources: Array<{
            type: 'course' | 'documentation' | 'tutorial' | 'book' | 'video';
            title: string;
            url: string;
            duration?: string;
            difficulty: 'Beginner' | 'Intermediate' | 'Advanced';
        }>;
    }>;
}

export default function DashboardPage() {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [targetRoles, setTargetRoles] = useState<TargetRole[]>([]);
    const [allSkills, setAllSkills] = useState<Skill[]>([]);
    const [analysisResult, setAnalysisResult] = useState<AnalysisData | null>(null);

    // Fetch taxonomy on mount
    useEffect(() => {
        fetchTaxonomy();
    }, []);

    const fetchTaxonomy = async () => {
        try {
            const response = await fetch('/api/taxonomy');
            const data = await response.json();

            if (data.success) {
                setTargetRoles(data.data.target_roles);
                setAllSkills(data.data.taxonomy.skills);
            }
        } catch (err) {
            console.error('Failed to fetch taxonomy:', err);
            setError('Failed to load taxonomy data');
        }
    };

    const handleAnalyze = async (candidate: unknown, targetRoleId: string) => {
        setLoading(true);
        setError(null);
        setAnalysisResult(null);

        try {
            const response = await fetch('/api/analyze', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    candidate,
                    target_role: targetRoleId
                })
            });

            const data = await response.json();

            if (data.success) {
                setAnalysisResult(data.data as AnalysisData);
            } else {
                setError(data.message || 'Analysis failed');
            }
        } catch (err) {
            console.error('Analysis error:', err);
            setError('Failed to analyze. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    // Calculate category-wise proficiency for radar chart
    const calculateCategoryProficiency = (skills: Array<{ skill_id: string; proficiency_level: number }>) => {
        const categories: { [key: string]: { total: number; count: number } } = {
            Frontend: { total: 0, count: 0 },
            Backend: { total: 0, count: 0 },
            DevOps: { total: 0, count: 0 },
            Database: { total: 0, count: 0 },
        };

        skills.forEach(skill => {
            const skillData = allSkills.find(s => s.id === skill.skill_id);
            if (skillData && categories[skillData.category]) {
                categories[skillData.category].total += skill.proficiency_level;
                categories[skillData.category].count += 1;
            }
        });

        const result: { [key: string]: number } = {};
        Object.keys(categories).forEach(cat => {
            result[cat] = categories[cat].count > 0
                ? Math.round(categories[cat].total / categories[cat].count)
                : 0;
        });

        return result;
    };

    // Enrich matched skills with names
    const enrichSkillsWithNames = <T extends { skill_id: string }>(skills: T[]) => {
        return skills.map(skill => ({
            ...skill,
            skill_name: allSkills.find(s => s.id === skill.skill_id)?.name || skill.skill_id
        }));
    };

    // Enrich gap skills with names
    const enrichGapsWithNames = <T extends { skill_id: string }>(gaps: T[]) => {
        return gaps.map(gap => ({
            ...gap,
            skill_name: allSkills.find(s => s.id === gap.skill_id)?.name || gap.skill_id
        }));
    };

    return (
        <div className="min-h-screen py-8 px-4">
            <div className="max-w-7xl mx-auto">
                {/* Header */}
                <div className="text-center mb-12 animate-fade-in">
                    <div className="flex items-center justify-center gap-3 mb-4">
                        <Sparkles className="w-10 h-10 text-blue-600" />
                        <h1 className="text-5xl font-bold text-gradient">
                            Skill Gap Analyzer
                        </h1>
                    </div>
                    <p className="text-xl text-slate-600 max-w-2xl mx-auto">
                        Discover your skill gaps and get a personalized learning roadmap to achieve your career goals
                    </p>
                </div>

                {/* Input Form */}
                <div className="mb-8">
                    <AnalysisForm
                        onAnalyze={handleAnalyze}
                        loading={loading}
                        targetRoles={targetRoles}
                    />
                </div>

                {/* Error Message */}
                {error && (
                    <div className="mb-8 p-4 bg-danger-50 border border-danger-200 rounded-lg flex items-center gap-3 animate-fade-in">
                        <AlertCircle className="w-5 h-5 text-danger-600 flex-shrink-0" />
                        <p className="text-danger-700">{error}</p>
                    </div>
                )}

                {/* Analysis Results */}
                {analysisResult && (
                    <div className="space-y-8">
                        {/* Top Section: Readiness Score */}
                        <ReadinessScoreCard
                            score={analysisResult.analysis.readiness_score}
                            targetRole={analysisResult.analysis.target_role_title}
                            experienceMatch={analysisResult.analysis.experience_match}
                        />

                        {/* Salary Projection & Future Paths */}
                        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                            <SalaryProjection
                                currentRole="Current Role"
                                targetRole={analysisResult.analysis.target_role_title}
                                estimatedMonths={analysisResult.learning_roadmap.estimated_months}
                                readinessScore={analysisResult.analysis.readiness_score}
                                targetSalary={targetRoles.find(r => r.id === analysisResult.analysis.target_role_id)?.salary_range}
                            />
                            <FuturePaths
                                currentTargetRole={analysisResult.analysis.target_role_title}
                                targetRoleSeniority={targetRoles.find(r => r.id === analysisResult.analysis.target_role_id)?.seniority_level || 'Senior'}
                            />
                        </div>

                        {/* Main Grid Layout */}
                        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                            {/* Left Column: Charts and Gaps */}
                            <div className="lg:col-span-2 space-y-8">
                                {/* Radar Chart */}
                                <SkillRadarChart
                                    currentSkills={calculateCategoryProficiency(
                                        analysisResult.analysis.matched_skills
                                            .filter(s => s.current_proficiency > 0)
                                            .map(s => ({ skill_id: s.skill_id, proficiency_level: s.current_proficiency }))
                                    )}
                                    targetSkills={calculateCategoryProficiency(
                                        analysisResult.analysis.matched_skills.map(s => ({
                                            skill_id: s.skill_id,
                                            proficiency_level: s.required_proficiency
                                        }))
                                    )}
                                />

                                {/* Skill Gap List */}
                                <SkillGapList
                                    matchedSkills={enrichSkillsWithNames(analysisResult.analysis.matched_skills)}
                                    missingSkills={enrichGapsWithNames(analysisResult.analysis.skill_gaps)}
                                />

                                {/* Timeline Roadmap */}
                                <TimelineRoadmap
                                    phases={analysisResult.learning_roadmap.phases}
                                    recommendedResources={analysisResult.recommended_resources}
                                />
                            </div>

                            {/* Right Column: Sidebar */}
                            <div className="lg:col-span-1">
                                <SimilarTransitionsSidebar />
                            </div>
                        </div>
                    </div>
                )}

                {/* Empty State */}
                {!analysisResult && !loading && !error && (
                    <div className="text-center py-16 animate-fade-in">
                        <div className="w-24 h-24 mx-auto mb-6 bg-gradient-to-br from-blue-100 to-indigo-100 rounded-full flex items-center justify-center">
                            <Sparkles className="w-12 h-12 text-blue-600" />
                        </div>
                        <h3 className="text-2xl font-bold text-slate-800 mb-2">Ready to Analyze</h3>
                        <p className="text-slate-600 max-w-md mx-auto">
                            Select a candidate and target role above to generate a personalized skill gap analysis and learning roadmap
                        </p>
                    </div>
                )}
            </div>
        </div>
    );
}
