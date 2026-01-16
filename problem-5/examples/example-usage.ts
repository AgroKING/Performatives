/**
 * Example usage of Gap Analysis & Roadmap Generation
 */

import { Candidate, TargetRole, Skill } from '../types/skill-taxonomy';
import { generateAnalysis, getLearningPhases } from '../utils/gap-analysis';
import seedData from '../data/seed-data.json';

// Load skills and roles from seed data
const allSkills: Skill[] = seedData.taxonomy.skills as Skill[];
const targetRoles: TargetRole[] = seedData.target_roles as TargetRole[];

// Example Candidate 1: Junior Developer wanting to become Senior Full Stack
const candidateJunior: Candidate = {
    id: 'cand-001',
    name: 'Alice Johnson',
    email: 'alice.johnson@example.com',
    experience_years: 2,
    created_at: '2024-01-15T10:00:00Z',
    updated_at: '2026-01-17T00:00:00Z',
    current_skills: [
        { skill_id: 'fe-001', proficiency_level: 8, years_of_experience: 2, certified: false }, // HTML
        { skill_id: 'fe-002', proficiency_level: 7, years_of_experience: 2, certified: false }, // CSS
        { skill_id: 'fe-003', proficiency_level: 6, years_of_experience: 1.5, certified: false }, // JavaScript
        { skill_id: 'fe-005', proficiency_level: 5, years_of_experience: 1, certified: false }, // React
        { skill_id: 'do-001', proficiency_level: 6, years_of_experience: 2, certified: false }, // Git
        { skill_id: 'db-001', proficiency_level: 5, years_of_experience: 1, certified: false }, // SQL
    ]
};

// Example Candidate 2: Mid-level Backend Developer
const candidateMid: Candidate = {
    id: 'cand-002',
    name: 'Bob Smith',
    email: 'bob.smith@example.com',
    experience_years: 4,
    created_at: '2023-06-10T10:00:00Z',
    updated_at: '2026-01-17T00:00:00Z',
    current_skills: [
        { skill_id: 'be-003', proficiency_level: 8, years_of_experience: 4, certified: true }, // Python
        { skill_id: 'be-004', proficiency_level: 7, years_of_experience: 3, certified: false }, // Django
        { skill_id: 'be-006', proficiency_level: 7, years_of_experience: 3, certified: false }, // REST API
        { skill_id: 'db-001', proficiency_level: 7, years_of_experience: 3, certified: false }, // SQL
        { skill_id: 'db-002', proficiency_level: 6, years_of_experience: 2, certified: false }, // PostgreSQL
        { skill_id: 'do-001', proficiency_level: 7, years_of_experience: 4, certified: false }, // Git
        { skill_id: 'do-002', proficiency_level: 6, years_of_experience: 2, certified: false }, // Linux
    ]
};

// Example 1: Junior Developer → Senior Full Stack Developer
console.log('='.repeat(80));
console.log('EXAMPLE 1: Junior Developer → Senior Full Stack Developer');
console.log('='.repeat(80));

const seniorFullStackRole = targetRoles.find(r => r.id === 'role-001')!;
const analysis1 = generateAnalysis(candidateJunior, seniorFullStackRole, allSkills);

console.log('\n📊 GAP ANALYSIS');
console.log(`Readiness Score: ${analysis1.gap_analysis.readiness_score}/100`);
console.log(`Missing Skills: ${analysis1.gap_analysis.missing_skills.length}`);
console.log(`Experience: ${analysis1.gap_analysis.experience_match.candidate_years}/${analysis1.gap_analysis.experience_match.required_years} years`);

console.log('\n🎯 SKILL GAPS (Priority Order):');
analysis1.gap_analysis.missing_skills
    .sort((a, b) => {
        const priorityOrder = { 'Critical': 0, 'High': 1, 'Medium': 2, 'Low': 3 };
        return priorityOrder[a.priority] - priorityOrder[b.priority];
    })
    .forEach(gap => {
        const skill = allSkills.find(s => s.id === gap.skill_id);
        console.log(`  [${gap.priority}] ${skill?.name}: ${gap.current_proficiency} → ${gap.required_proficiency} (gap: ${gap.gap_score})`);
    });

console.log('\n🗺️ LEARNING ROADMAP');
console.log(`Total Duration: ${analysis1.learning_roadmap.estimated_total_weeks} weeks (~${Math.ceil(analysis1.learning_roadmap.estimated_total_weeks / 4)} months)`);

const phases1 = getLearningPhases(analysis1.learning_roadmap, allSkills);
console.log(`\nLearning Phases: ${phases1.length}`);
phases1.forEach(phase => {
    console.log(`\n  Phase ${phase.phase_number}: ${phase.phase_name} (${phase.estimated_weeks} weeks)`);
    phase.skills.forEach(step => {
        const skill = allSkills.find(s => s.id === step.skill_id);
        console.log(`    ${step.order}. ${skill?.name} - ${step.estimated_weeks} weeks`);
    });
});

// Example 2: Mid-level Backend → DevOps Engineer
console.log('\n\n' + '='.repeat(80));
console.log('EXAMPLE 2: Mid-level Backend Developer → DevOps Engineer');
console.log('='.repeat(80));

const devOpsRole = targetRoles.find(r => r.id === 'role-002')!;
const analysis2 = generateAnalysis(candidateMid, devOpsRole, allSkills);

console.log('\n📊 GAP ANALYSIS');
console.log(`Readiness Score: ${analysis2.gap_analysis.readiness_score}/100`);
console.log(`Missing Skills: ${analysis2.gap_analysis.missing_skills.length}`);
console.log(`Experience: ${analysis2.gap_analysis.experience_match.candidate_years}/${analysis2.gap_analysis.experience_match.required_years} years`);

console.log('\n🎯 SKILL GAPS (Priority Order):');
analysis2.gap_analysis.missing_skills
    .sort((a, b) => {
        const priorityOrder = { 'Critical': 0, 'High': 1, 'Medium': 2, 'Low': 3 };
        return priorityOrder[a.priority] - priorityOrder[b.priority];
    })
    .forEach(gap => {
        const skill = allSkills.find(s => s.id === gap.skill_id);
        console.log(`  [${gap.priority}] ${skill?.name}: ${gap.current_proficiency} → ${gap.required_proficiency} (gap: ${gap.gap_score})`);
    });

console.log('\n🗺️ LEARNING ROADMAP');
console.log(`Total Duration: ${analysis2.learning_roadmap.estimated_total_weeks} weeks (~${Math.ceil(analysis2.learning_roadmap.estimated_total_weeks / 4)} months)`);

const phases2 = getLearningPhases(analysis2.learning_roadmap, allSkills);
console.log(`\nLearning Phases: ${phases2.length}`);
phases2.forEach(phase => {
    console.log(`\n  Phase ${phase.phase_number}: ${phase.phase_name} (${phase.estimated_weeks} weeks)`);
    phase.skills.forEach(step => {
        const skill = allSkills.find(s => s.id === step.skill_id);
        console.log(`    ${step.order}. ${skill?.name} - ${step.estimated_weeks} weeks`);
    });
});

// Export JSON output for Example 1
console.log('\n\n' + '='.repeat(80));
console.log('JSON OUTPUT (Example 1)');
console.log('='.repeat(80));
console.log(JSON.stringify(analysis1, null, 2));

// Export the functions for use in other modules
export { candidateJunior, candidateMid, seniorFullStackRole, devOpsRole };
