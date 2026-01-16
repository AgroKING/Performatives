/**
 * Gap Analysis & Roadmap Generation Algorithms
 * Core utility module for skill gap analysis and learning path generation
 */

import {
    Skill,
    Candidate,
    TargetRole,
    SkillGap,
    LearningPathStep,
    LearningRoadmap,
    CandidateSkill,
    RoleSkillRequirement
} from '../types/skill-taxonomy';

/**
 * Result of gap analysis
 */
export interface GapAnalysisResult {
    readiness_score: number; // 0-100
    missing_skills: SkillGap[];
    matched_skills: Array<{
        skill_id: string;
        current_proficiency: number;
        required_proficiency: number;
        meets_requirement: boolean;
    }>;
    experience_match: {
        candidate_years: number;
        required_years: number;
        meets_requirement: boolean;
    };
}

/**
 * Complete analysis output
 */
export interface CompleteAnalysis {
    candidate_id: string;
    target_role_id: string;
    generated_at: string;
    gap_analysis: GapAnalysisResult;
    learning_roadmap: LearningRoadmap;
}

/**
 * Learning phase grouping
 */
export interface LearningPhase {
    phase_number: number;
    phase_name: string;
    skills: LearningPathStep[];
    estimated_weeks: number;
}

/**
 * Calculate readiness score based on skill matching and experience
 */
function calculateReadinessScore(
    candidate: Candidate,
    targetRole: TargetRole,
    matchedSkills: Array<{ skill_id: string; current_proficiency: number; required_proficiency: number; meets_requirement: boolean }>
): number {
    // Weight factors
    const SKILL_WEIGHT = 0.7;
    const EXPERIENCE_WEIGHT = 0.3;

    // Edge case: No required skills
    const totalRequiredSkills = targetRole.required_skills.length;
    if (totalRequiredSkills === 0) return 100;

    // Edge case: No matched skills (candidate has zero skills)
    if (matchedSkills.length === 0) return 0;

    let skillScore = 0;
    matchedSkills.forEach(match => {
        const requirement = targetRole.required_skills.find(r => r.skill_id === match.skill_id);
        if (!requirement) return;

        // Calculate how well the candidate meets this skill requirement
        const proficiencyRatio = Math.min(match.current_proficiency / match.required_proficiency, 1);

        // Weight by importance
        let importanceMultiplier = 1.0;
        switch (requirement.importance) {
            case 'Critical': importanceMultiplier = 1.5; break;
            case 'High': importanceMultiplier = 1.2; break;
            case 'Medium': importanceMultiplier = 1.0; break;
            case 'Low': importanceMultiplier = 0.8; break;
        }

        skillScore += (proficiencyRatio * importanceMultiplier);
    });

    // Normalize skill score
    const totalImportanceWeight = targetRole.required_skills.reduce((sum, req) => {
        switch (req.importance) {
            case 'Critical': return sum + 1.5;
            case 'High': return sum + 1.2;
            case 'Medium': return sum + 1.0;
            case 'Low': return sum + 0.8;
            default: return sum + 1.0;
        }
    }, 0);

    // Edge case: Prevent division by zero
    const normalizedSkillScore = totalImportanceWeight > 0
        ? (skillScore / totalImportanceWeight) * 100
        : 0;

    // Calculate experience score
    // Edge case: Prevent division by zero for min_experience_years
    const experienceRatio = targetRole.min_experience_years > 0
        ? Math.min(candidate.experience_years / targetRole.min_experience_years, 1)
        : 1;
    const experienceScore = experienceRatio * 100;

    // Weighted final score
    const finalScore = (normalizedSkillScore * SKILL_WEIGHT) + (experienceScore * EXPERIENCE_WEIGHT);

    // Edge case: Ensure result is a valid number
    const validScore = isNaN(finalScore) ? 0 : finalScore;
    return Math.round(Math.min(Math.max(validScore, 0), 100));
}

/**
 * Perform gap analysis comparing candidate skills vs target role requirements
 */
export function analyzeGap(
    candidate: Candidate,
    targetRole: TargetRole,
    allSkills: Skill[]
): GapAnalysisResult {
    // Edge case: Ensure current_skills array exists
    const currentSkills = candidate.current_skills || [];

    const candidateSkillMap = new Map<string, CandidateSkill>();
    currentSkills.forEach(cs => {
        candidateSkillMap.set(cs.skill_id, cs);
    });

    const matchedSkills: Array<{
        skill_id: string;
        current_proficiency: number;
        required_proficiency: number;
        meets_requirement: boolean;
    }> = [];

    const missingSkills: SkillGap[] = [];

    // Analyze each required skill
    targetRole.required_skills.forEach(requirement => {
        const candidateSkill = candidateSkillMap.get(requirement.skill_id);
        const currentProficiency = candidateSkill?.proficiency_level || 0;

        const meetsRequirement = currentProficiency >= requirement.minimum_proficiency;

        matchedSkills.push({
            skill_id: requirement.skill_id,
            current_proficiency: currentProficiency,
            required_proficiency: requirement.minimum_proficiency,
            meets_requirement: meetsRequirement
        });

        // If skill is missing or below required proficiency, it's a gap
        if (!meetsRequirement) {
            missingSkills.push({
                skill_id: requirement.skill_id,
                current_proficiency: currentProficiency,
                required_proficiency: requirement.minimum_proficiency,
                gap_score: requirement.minimum_proficiency - currentProficiency,
                priority: requirement.importance
            });
        }
    });

    const readinessScore = calculateReadinessScore(candidate, targetRole, matchedSkills);

    return {
        readiness_score: readinessScore,
        missing_skills: missingSkills,
        matched_skills: matchedSkills,
        experience_match: {
            candidate_years: candidate.experience_years,
            required_years: targetRole.min_experience_years,
            meets_requirement: candidate.experience_years >= targetRole.min_experience_years
        }
    };
}

/**
 * Topological sort to order skills by prerequisites
 * Returns skills in an order where all prerequisites come before dependents
 */
function topologicalSort(
    skillIds: string[],
    allSkills: Skill[],
    candidateSkillMap: Map<string, CandidateSkill>
): string[] {
    const skillMap = new Map<string, Skill>();
    allSkills.forEach(s => skillMap.set(s.id, s));

    // Build adjacency list and in-degree map
    const graph = new Map<string, string[]>();
    const inDegree = new Map<string, number>();

    // Initialize
    skillIds.forEach(id => {
        graph.set(id, []);
        inDegree.set(id, 0);
    });

    // Build graph edges (prerequisite -> dependent)
    skillIds.forEach(skillId => {
        const skill = skillMap.get(skillId);
        if (!skill) return;

        skill.prerequisites.forEach(prereqId => {
            // Only consider prerequisites that are also in our learning list
            // or that the candidate doesn't already have
            const candidateHasPrereq = candidateSkillMap.has(prereqId) &&
                (candidateSkillMap.get(prereqId)?.proficiency_level || 0) >= 5;

            if (skillIds.includes(prereqId) || !candidateHasPrereq) {
                if (!skillIds.includes(prereqId) && !candidateHasPrereq) {
                    // Add missing prerequisite to the learning path
                    skillIds.push(prereqId);
                    graph.set(prereqId, []);
                    inDegree.set(prereqId, 0);
                }

                if (skillIds.includes(prereqId)) {
                    graph.get(prereqId)?.push(skillId);
                    inDegree.set(skillId, (inDegree.get(skillId) || 0) + 1);
                }
            }
        });
    });

    // Kahn's algorithm for topological sort
    const queue: string[] = [];
    const result: string[] = [];

    // Start with nodes that have no prerequisites
    inDegree.forEach((degree, skillId) => {
        if (degree === 0) {
            queue.push(skillId);
        }
    });

    while (queue.length > 0) {
        // Sort queue by difficulty to learn easier skills first when there's a choice
        queue.sort((a, b) => {
            const skillA = skillMap.get(a);
            const skillB = skillMap.get(b);
            return (skillA?.difficulty || 0) - (skillB?.difficulty || 0);
        });

        const current = queue.shift()!;
        result.push(current);

        // Process neighbors
        const neighbors = graph.get(current) || [];
        neighbors.forEach(neighbor => {
            const newDegree = (inDegree.get(neighbor) || 0) - 1;
            inDegree.set(neighbor, newDegree);

            if (newDegree === 0) {
                queue.push(neighbor);
            }
        });
    }

    return result;
}

/**
 * Group skills into learning phases based on difficulty and dependencies
 */
function groupIntoPhases(
    orderedSkills: string[],
    allSkills: Skill[]
): LearningPhase[] {
    const skillMap = new Map<string, Skill>();
    allSkills.forEach(s => skillMap.set(s.id, s));

    const phases: LearningPhase[] = [];
    let currentPhase: string[] = [];
    let currentMaxDifficulty = 0;

    orderedSkills.forEach((skillId, index) => {
        const skill = skillMap.get(skillId);
        if (!skill) return;

        // Start a new phase if:
        // 1. Difficulty jumps significantly (3+ levels)
        // 2. Current phase has 4+ skills
        const difficultyJump = skill.difficulty - currentMaxDifficulty >= 3;
        const phaseFull = currentPhase.length >= 4;

        if ((difficultyJump || phaseFull) && currentPhase.length > 0) {
            // Finalize current phase
            phases.push(createPhase(phases.length + 1, currentPhase, skillMap));
            currentPhase = [];
            currentMaxDifficulty = 0;
        }

        currentPhase.push(skillId);
        currentMaxDifficulty = Math.max(currentMaxDifficulty, skill.difficulty);
    });

    // Add remaining skills as final phase
    if (currentPhase.length > 0) {
        phases.push(createPhase(phases.length + 1, currentPhase, skillMap));
    }

    return phases;
}

/**
 * Create a learning phase from skill IDs
 */
function createPhase(
    phaseNumber: number,
    skillIds: string[],
    skillMap: Map<string, Skill>
): LearningPhase {
    const skills = skillIds.map(id => skillMap.get(id)).filter(s => s !== undefined) as Skill[];

    // Determine phase name based on average difficulty
    const avgDifficulty = skills.reduce((sum, s) => sum + s.difficulty, 0) / skills.length;
    let phaseName = 'Fundamentals';
    if (avgDifficulty >= 7) phaseName = 'Advanced';
    else if (avgDifficulty >= 4) phaseName = 'Intermediate';

    const learningSteps: LearningPathStep[] = skillIds.map((skillId, index) => {
        const skill = skillMap.get(skillId)!;
        return {
            order: index + 1,
            skill_id: skillId,
            estimated_weeks: skill.typical_learning_time_weeks,
            prerequisites_met: true, // By design of topological sort
            reason: `Phase ${phaseNumber}: ${phaseName} - ${skill.name}`
        };
    });

    const totalWeeks = skills.reduce((sum, s) => sum + s.typical_learning_time_weeks, 0);

    return {
        phase_number: phaseNumber,
        phase_name: phaseName,
        skills: learningSteps,
        estimated_weeks: totalWeeks
    };
}

/**
 * Generate learning roadmap from skill gaps
 */
export function generateRoadmap(
    candidate: Candidate,
    targetRole: TargetRole,
    skillGaps: SkillGap[],
    allSkills: Skill[]
): LearningRoadmap {
    // Edge case: Ensure current_skills array exists
    const currentSkills = candidate.current_skills || [];

    const candidateSkillMap = new Map<string, CandidateSkill>();
    currentSkills.forEach(cs => {
        candidateSkillMap.set(cs.skill_id, cs);
    });

    // Extract skill IDs that need to be learned
    const skillsToLearn = skillGaps.map(gap => gap.skill_id);

    // Edge case: If no skills to learn, return empty roadmap
    if (skillsToLearn.length === 0) {
        return {
            candidate_id: candidate.id,
            target_role_id: targetRole.id,
            generated_at: new Date().toISOString(),
            skill_gaps: [],
            estimated_total_weeks: 0,
            learning_path: []
        };
    }

    // Sort skills respecting prerequisites
    const orderedSkills = topologicalSort(skillsToLearn, allSkills, candidateSkillMap);

    // Group into phases
    const phases = groupIntoPhases(orderedSkills, allSkills);

    // Flatten phases into learning path
    let globalOrder = 1;
    const learningPath: LearningPathStep[] = [];

    phases.forEach(phase => {
        phase.skills.forEach(step => {
            learningPath.push({
                ...step,
                order: globalOrder++
            });
        });
    });

    const totalWeeks = learningPath.reduce((sum, step) => sum + step.estimated_weeks, 0);

    return {
        candidate_id: candidate.id,
        target_role_id: targetRole.id,
        generated_at: new Date().toISOString(),
        skill_gaps: skillGaps,
        estimated_total_weeks: totalWeeks,
        learning_path: learningPath
    };
}

/**
 * Main function: Generate complete analysis
 */
export function generateAnalysis(
    candidate: Candidate,
    targetRole: TargetRole,
    allSkills: Skill[]
): CompleteAnalysis {
    // Step 1: Analyze gaps
    const gapAnalysis = analyzeGap(candidate, targetRole, allSkills);

    // Step 2: Generate roadmap
    const learningRoadmap = generateRoadmap(
        candidate,
        targetRole,
        gapAnalysis.missing_skills,
        allSkills
    );

    return {
        candidate_id: candidate.id,
        target_role_id: targetRole.id,
        generated_at: new Date().toISOString(),
        gap_analysis: gapAnalysis,
        learning_roadmap: learningRoadmap
    };
}

/**
 * Helper: Get learning phases from roadmap
 */
export function getLearningPhases(
    roadmap: LearningRoadmap,
    allSkills: Skill[]
): LearningPhase[] {
    const skillMap = new Map<string, Skill>();
    allSkills.forEach(s => skillMap.set(s.id, s));

    return groupIntoPhases(
        roadmap.learning_path.map(step => step.skill_id),
        allSkills
    );
}
