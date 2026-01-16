/**
 * Test requests for the Skill Gap Analysis API
 * Use these examples to test the API endpoints
 */

// ============================================================================
// Test 1: GET /api/taxonomy
// ============================================================================

export const testGetTaxonomy = async () => {
    console.log('Testing GET /api/taxonomy...\n');

    const response = await fetch('http://localhost:3000/api/taxonomy');
    const data = await response.json();

    console.log('Response Status:', response.status);
    console.log('Total Skills:', data.data.metadata.total_skills);
    console.log('Total Roles:', data.data.metadata.total_roles);
    console.log('\nFirst 3 skills:');
    data.data.taxonomy.skills.slice(0, 3).forEach((skill: any) => {
        console.log(`  - ${skill.name} (${skill.category}, difficulty: ${skill.difficulty})`);
    });

    return data;
};

// ============================================================================
// Test 2: POST /api/analyze - Junior Developer → Senior Full Stack
// ============================================================================

export const testAnalyzeJuniorToSenior = async () => {
    console.log('\n\nTesting POST /api/analyze (Junior → Senior Full Stack)...\n');

    const requestBody = {
        candidate: {
            id: 'cand-001',
            name: 'Alice Johnson',
            email: 'alice.johnson@example.com',
            experience_years: 2,
            created_at: '2024-01-15T10:00:00Z',
            updated_at: '2026-01-17T00:00:00Z',
            current_skills: [
                { skill_id: 'fe-001', proficiency_level: 8, years_of_experience: 2, certified: false },
                { skill_id: 'fe-002', proficiency_level: 7, years_of_experience: 2, certified: false },
                { skill_id: 'fe-003', proficiency_level: 6, years_of_experience: 1.5, certified: false },
                { skill_id: 'fe-005', proficiency_level: 5, years_of_experience: 1, certified: false },
                { skill_id: 'do-001', proficiency_level: 6, years_of_experience: 2, certified: false },
                { skill_id: 'db-001', proficiency_level: 5, years_of_experience: 1, certified: false },
            ]
        },
        target_role: 'role-001' // Senior Full Stack Developer
    };

    const response = await fetch('http://localhost:3000/api/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(requestBody)
    });

    const data = await response.json();

    console.log('Response Status:', response.status);
    console.log('Readiness Score:', data.data.analysis.readiness_score + '/100');
    console.log('Missing Skills:', data.data.analysis.missing_skills_count);
    console.log('Total Learning Time:', data.data.learning_roadmap.estimated_total_weeks, 'weeks');
    console.log('Estimated Duration:', data.data.learning_roadmap.estimated_months, 'months');

    console.log('\nLearning Phases:');
    data.data.learning_roadmap.phases.forEach((phase: any) => {
        console.log(`  Phase ${phase.phase_number}: ${phase.phase_name} (${phase.estimated_weeks} weeks)`);
        phase.skills.forEach((skill: any) => {
            console.log(`    ${skill.order}. ${skill.skill_name} - ${skill.estimated_weeks} weeks`);
        });
    });

    console.log('\nTop 3 Skill Gaps:');
    data.data.analysis.skill_gaps.slice(0, 3).forEach((gap: any) => {
        console.log(`  [${gap.priority}] Gap: ${gap.gap_score} points (${gap.current_proficiency} → ${gap.required_proficiency})`);
    });

    return data;
};

// ============================================================================
// Test 3: POST /api/analyze - Backend Developer → DevOps Engineer
// ============================================================================

export const testAnalyzeBackendToDevOps = async () => {
    console.log('\n\nTesting POST /api/analyze (Backend → DevOps)...\n');

    const requestBody = {
        candidate: {
            id: 'cand-002',
            name: 'Bob Smith',
            email: 'bob.smith@example.com',
            experience_years: 4,
            created_at: '2023-06-10T10:00:00Z',
            updated_at: '2026-01-17T00:00:00Z',
            current_skills: [
                { skill_id: 'be-003', proficiency_level: 8, years_of_experience: 4, certified: true },
                { skill_id: 'be-004', proficiency_level: 7, years_of_experience: 3, certified: false },
                { skill_id: 'be-006', proficiency_level: 7, years_of_experience: 3, certified: false },
                { skill_id: 'db-001', proficiency_level: 7, years_of_experience: 3, certified: false },
                { skill_id: 'db-002', proficiency_level: 6, years_of_experience: 2, certified: false },
                { skill_id: 'do-001', proficiency_level: 7, years_of_experience: 4, certified: false },
                { skill_id: 'do-002', proficiency_level: 6, years_of_experience: 2, certified: false },
            ]
        },
        target_role: 'role-002' // DevOps Engineer
    };

    const response = await fetch('http://localhost:3000/api/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(requestBody)
    });

    const data = await response.json();

    console.log('Response Status:', response.status);
    console.log('Readiness Score:', data.data.analysis.readiness_score + '/100');
    console.log('Missing Skills:', data.data.analysis.missing_skills_count);
    console.log('Total Learning Time:', data.data.learning_roadmap.estimated_total_weeks, 'weeks');

    console.log('\nLearning Path (First 5 Skills):');
    data.data.learning_roadmap.full_learning_path.slice(0, 5).forEach((step: any) => {
        console.log(`  ${step.order}. ${step.skill_name} - ${step.estimated_weeks} weeks`);
    });

    return data;
};

// ============================================================================
// Test 4: Error Handling - Missing Required Fields
// ============================================================================

export const testErrorHandling = async () => {
    console.log('\n\nTesting Error Handling (Missing Fields)...\n');

    const response = await fetch('http://localhost:3000/api/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ candidate: {} }) // Missing target_role
    });

    const data = await response.json();

    console.log('Response Status:', response.status);
    console.log('Error:', data.error);
    console.log('Message:', data.message);

    return data;
};

// ============================================================================
// Run all tests
// ============================================================================

export const runAllTests = async () => {
    try {
        await testGetTaxonomy();
        await testAnalyzeJuniorToSenior();
        await testAnalyzeBackendToDevOps();
        await testErrorHandling();

        console.log('\n\n✅ All tests completed successfully!');
    } catch (error) {
        console.error('\n\n❌ Test failed:', error);
    }
};

// If running directly with Node.js or tsx
if (require.main === module) {
    runAllTests();
}
