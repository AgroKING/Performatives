/**
 * POST /api/analyze
 * Analyzes skill gaps and generates learning roadmap for a candidate targeting a specific role
 */

import { NextRequest, NextResponse } from 'next/server';
import { generateAnalysis, getLearningPhases } from '@/utils/gap-analysis';
import { Candidate, TargetRole, Skill } from '@/types/skill-taxonomy';
import seedData from '@/data/seed-data.json';

/**
 * Learning resource recommendation based on skill
 */
interface LearningResource {
    skill_id: string;
    skill_name: string;
    resources: Array<{
        type: 'course' | 'documentation' | 'tutorial' | 'book' | 'video';
        title: string;
        url: string;
        duration?: string;
        difficulty: 'Beginner' | 'Intermediate' | 'Advanced';
    }>;
}

/**
 * Generate recommended learning resources for skills
 */
function generateRecommendedResources(skillIds: string[], allSkills: Skill[]): LearningResource[] {
    const resourceMap: { [key: string]: LearningResource } = {
        'fe-003': {
            skill_id: 'fe-003',
            skill_name: 'JavaScript',
            resources: [
                {
                    type: 'course',
                    title: 'JavaScript: The Complete Guide',
                    url: 'https://www.udemy.com/course/javascript-the-complete-guide-2020-beginner-advanced/',
                    duration: '52 hours',
                    difficulty: 'Beginner'
                },
                {
                    type: 'documentation',
                    title: 'MDN JavaScript Guide',
                    url: 'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide',
                    difficulty: 'Beginner'
                },
                {
                    type: 'book',
                    title: 'Eloquent JavaScript',
                    url: 'https://eloquentjavascript.net/',
                    difficulty: 'Intermediate'
                }
            ]
        },
        'fe-004': {
            skill_id: 'fe-004',
            skill_name: 'TypeScript',
            resources: [
                {
                    type: 'documentation',
                    title: 'TypeScript Official Handbook',
                    url: 'https://www.typescriptlang.org/docs/handbook/intro.html',
                    difficulty: 'Beginner'
                },
                {
                    type: 'course',
                    title: 'Understanding TypeScript',
                    url: 'https://www.udemy.com/course/understanding-typescript/',
                    duration: '15 hours',
                    difficulty: 'Intermediate'
                }
            ]
        },
        'fe-005': {
            skill_id: 'fe-005',
            skill_name: 'React',
            resources: [
                {
                    type: 'documentation',
                    title: 'React Official Documentation',
                    url: 'https://react.dev/',
                    difficulty: 'Beginner'
                },
                {
                    type: 'course',
                    title: 'React - The Complete Guide',
                    url: 'https://www.udemy.com/course/react-the-complete-guide-incl-redux/',
                    duration: '48 hours',
                    difficulty: 'Intermediate'
                }
            ]
        },
        'fe-008': {
            skill_id: 'fe-008',
            skill_name: 'Next.js',
            resources: [
                {
                    type: 'documentation',
                    title: 'Next.js Official Documentation',
                    url: 'https://nextjs.org/docs',
                    difficulty: 'Intermediate'
                },
                {
                    type: 'tutorial',
                    title: 'Next.js App Router Tutorial',
                    url: 'https://nextjs.org/learn',
                    duration: '8 hours',
                    difficulty: 'Intermediate'
                }
            ]
        },
        'be-001': {
            skill_id: 'be-001',
            skill_name: 'Node.js',
            resources: [
                {
                    type: 'documentation',
                    title: 'Node.js Official Guides',
                    url: 'https://nodejs.org/en/docs/guides/',
                    difficulty: 'Beginner'
                },
                {
                    type: 'course',
                    title: 'Node.js: The Complete Guide',
                    url: 'https://www.udemy.com/course/nodejs-the-complete-guide/',
                    duration: '40 hours',
                    difficulty: 'Intermediate'
                }
            ]
        },
        'do-003': {
            skill_id: 'do-003',
            skill_name: 'Docker',
            resources: [
                {
                    type: 'documentation',
                    title: 'Docker Official Documentation',
                    url: 'https://docs.docker.com/get-started/',
                    difficulty: 'Beginner'
                },
                {
                    type: 'course',
                    title: 'Docker Mastery',
                    url: 'https://www.udemy.com/course/docker-mastery/',
                    duration: '19 hours',
                    difficulty: 'Intermediate'
                }
            ]
        },
        'do-004': {
            skill_id: 'do-004',
            skill_name: 'Kubernetes',
            resources: [
                {
                    type: 'documentation',
                    title: 'Kubernetes Official Documentation',
                    url: 'https://kubernetes.io/docs/home/',
                    difficulty: 'Advanced'
                },
                {
                    type: 'course',
                    title: 'Kubernetes for Developers',
                    url: 'https://www.udemy.com/course/kubernetes-for-developers/',
                    duration: '16 hours',
                    difficulty: 'Advanced'
                }
            ]
        },
        'db-002': {
            skill_id: 'db-002',
            skill_name: 'PostgreSQL',
            resources: [
                {
                    type: 'documentation',
                    title: 'PostgreSQL Official Documentation',
                    url: 'https://www.postgresql.org/docs/',
                    difficulty: 'Beginner'
                },
                {
                    type: 'course',
                    title: 'SQL and PostgreSQL: The Complete Guide',
                    url: 'https://www.udemy.com/course/sql-and-postgresql/',
                    duration: '22 hours',
                    difficulty: 'Intermediate'
                }
            ]
        }
    };

    // Generate resources for requested skills
    const resources: LearningResource[] = [];

    skillIds.forEach(skillId => {
        if (resourceMap[skillId]) {
            resources.push(resourceMap[skillId]);
        } else {
            // Generate generic resource for skills not in map
            const skill = allSkills.find(s => s.id === skillId);
            if (skill) {
                resources.push({
                    skill_id: skillId,
                    skill_name: skill.name,
                    resources: [
                        {
                            type: 'documentation',
                            title: `${skill.name} Official Documentation`,
                            url: `https://www.google.com/search?q=${encodeURIComponent(skill.name + ' documentation')}`,
                            difficulty: skill.difficulty <= 3 ? 'Beginner' : skill.difficulty <= 6 ? 'Intermediate' : 'Advanced'
                        }
                    ]
                });
            }
        }
    });

    return resources;
}

export async function POST(request: NextRequest) {
    try {
        // Parse request body
        const body = await request.json();
        const { candidate, target_role } = body;

        // Validate input
        if (!candidate || !target_role) {
            return NextResponse.json({
                success: false,
                error: 'Missing required fields',
                message: 'Both "candidate" and "target_role" are required in the request body'
            }, { status: 400 });
        }

        // Load all skills from seed data
        const allSkills: Skill[] = seedData.taxonomy.skills as Skill[];

        // Find target role or use provided role object
        let targetRoleObj: TargetRole;
        if (typeof target_role === 'string') {
            // If target_role is a role ID, find it in seed data
            const foundRole = seedData.target_roles.find(r => r.id === target_role);
            if (!foundRole) {
                return NextResponse.json({
                    success: false,
                    error: 'Invalid target role',
                    message: `Role with ID "${target_role}" not found`
                }, { status: 404 });
            }
            targetRoleObj = foundRole as TargetRole;
        } else {
            // Use provided role object
            targetRoleObj = target_role as TargetRole;
        }

        // Generate analysis
        const analysis = generateAnalysis(candidate as Candidate, targetRoleObj, allSkills);

        // Get learning phases
        const phases = getLearningPhases(analysis.learning_roadmap, allSkills);

        // Generate recommended resources
        const skillsToLearn = analysis.learning_roadmap.learning_path.map(step => step.skill_id);
        const recommendedResources = generateRecommendedResources(skillsToLearn, allSkills);

        // Format response according to specification
        const response = {
            success: true,
            data: {
                analysis: {
                    candidate_id: analysis.candidate_id,
                    target_role_id: analysis.target_role_id,
                    target_role_title: targetRoleObj.title,
                    generated_at: analysis.generated_at,
                    readiness_score: analysis.gap_analysis.readiness_score,
                    missing_skills_count: analysis.gap_analysis.missing_skills.length,
                    matched_skills: analysis.gap_analysis.matched_skills,
                    experience_match: analysis.gap_analysis.experience_match,
                    skill_gaps: analysis.gap_analysis.missing_skills
                },
                learning_roadmap: {
                    estimated_total_weeks: analysis.learning_roadmap.estimated_total_weeks,
                    estimated_months: Math.ceil(analysis.learning_roadmap.estimated_total_weeks / 4),
                    phases: phases.map(phase => ({
                        phase_number: phase.phase_number,
                        phase_name: phase.phase_name,
                        estimated_weeks: phase.estimated_weeks,
                        skills: phase.skills.map(step => {
                            const skill = allSkills.find(s => s.id === step.skill_id);
                            return {
                                order: step.order,
                                skill_id: step.skill_id,
                                skill_name: skill?.name || 'Unknown',
                                difficulty: skill?.difficulty || 0,
                                estimated_weeks: step.estimated_weeks,
                                prerequisites_met: step.prerequisites_met,
                                prerequisites: skill?.prerequisites || []
                            };
                        })
                    })),
                    full_learning_path: analysis.learning_roadmap.learning_path.map(step => {
                        const skill = allSkills.find(s => s.id === step.skill_id);
                        return {
                            order: step.order,
                            skill_id: step.skill_id,
                            skill_name: skill?.name || 'Unknown',
                            estimated_weeks: step.estimated_weeks,
                            reason: step.reason
                        };
                    })
                },
                recommended_resources: recommendedResources
            }
        };

        return NextResponse.json(response, { status: 200 });

    } catch (error) {
        console.error('Error analyzing candidate:', error);
        return NextResponse.json({
            success: false,
            error: 'Analysis failed',
            message: error instanceof Error ? error.message : 'Unknown error occurred during analysis'
        }, { status: 500 });
    }
}

// Optional: Support CORS for external API calls
export async function OPTIONS(request: NextRequest) {
    return new NextResponse(null, {
        status: 200,
        headers: {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
        },
    });
}
