/**
 * GET /api/taxonomy
 * Returns the complete skill taxonomy including all skills and categories
 */

import { NextRequest, NextResponse } from 'next/server';
import seedData from '@/data/seed-data.json';

export async function GET(request: NextRequest) {
    try {
        // Return the complete taxonomy
        return NextResponse.json({
            success: true,
            data: {
                taxonomy: seedData.taxonomy,
                target_roles: seedData.target_roles,
                metadata: {
                    version: seedData.taxonomy.version,
                    last_updated: seedData.taxonomy.last_updated,
                    total_skills: seedData.taxonomy.skills.length,
                    total_roles: seedData.target_roles.length,
                }
            }
        }, { status: 200 });
    } catch (error) {
        console.error('Error fetching taxonomy:', error);
        return NextResponse.json({
            success: false,
            error: 'Failed to fetch skill taxonomy',
            message: error instanceof Error ? error.message : 'Unknown error'
        }, { status: 500 });
    }
}

// Optional: Support CORS for external API calls
export async function OPTIONS(request: NextRequest) {
    return new NextResponse(null, {
        status: 200,
        headers: {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
        },
    });
}
