/**
 * Skill Gap Analysis & Learning Roadmap System
 * Data Model Definitions
 */

export type SkillCategory = 'Frontend' | 'Backend' | 'DevOps' | 'Database';

export type DifficultyLevel = 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10;

/**
 * Represents a single skill in the taxonomy
 */
export interface Skill {
  id: string;
  name: string;
  category: SkillCategory;
  difficulty: DifficultyLevel;
  typical_learning_time_weeks: number;
  prerequisites: string[]; // Array of skill IDs
  description: string;
  tags?: string[];
}

/**
 * Represents a candidate's current skill profile
 */
export interface Candidate {
  id: string;
  name: string;
  email: string;
  current_skills: CandidateSkill[];
  experience_years: number;
  created_at: string;
  updated_at: string;
}

/**
 * Represents a skill that a candidate possesses with proficiency level
 */
export interface CandidateSkill {
  skill_id: string;
  proficiency_level: number; // 1-10 scale
  years_of_experience: number;
  last_used?: string; // ISO date string
  certified?: boolean;
}

/**
 * Represents a target role with required skills
 */
export interface TargetRole {
  id: string;
  title: string;
  description: string;
  seniority_level: 'Junior' | 'Mid' | 'Senior' | 'Lead' | 'Principal';
  required_skills: RoleSkillRequirement[];
  optional_skills: RoleSkillRequirement[];
  min_experience_years: number;
  salary_range?: {
    min: number;
    max: number;
    currency: string;
  };
}

/**
 * Represents a skill requirement for a specific role
 */
export interface RoleSkillRequirement {
  skill_id: string;
  minimum_proficiency: number; // 1-10 scale
  importance: 'Critical' | 'High' | 'Medium' | 'Low';
}

/**
 * Complete skill taxonomy structure
 */
export interface SkillTaxonomy {
  version: string;
  last_updated: string;
  categories: {
    [key in SkillCategory]: {
      name: string;
      description: string;
      skill_count: number;
    };
  };
  skills: Skill[];
}

/**
 * Learning roadmap generated for a candidate
 */
export interface LearningRoadmap {
  candidate_id: string;
  target_role_id: string;
  generated_at: string;
  skill_gaps: SkillGap[];
  estimated_total_weeks: number;
  learning_path: LearningPathStep[];
}

/**
 * Represents a gap between current and required skill level
 */
export interface SkillGap {
  skill_id: string;
  current_proficiency: number;
  required_proficiency: number;
  gap_score: number;
  priority: 'Critical' | 'High' | 'Medium' | 'Low';
}

/**
 * Represents a step in the learning path
 */
export interface LearningPathStep {
  order: number;
  skill_id: string;
  estimated_weeks: number;
  prerequisites_met: boolean;
  reason: string;
}
