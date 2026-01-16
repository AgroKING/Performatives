export enum JobType {
  FullTime = 'Full-time',
  PartTime = 'Part-time',
  Contract = 'Contract',
  Remote = 'Remote',
  Internship = 'Internship',
  Freelance = 'Freelance',
}

export interface SalaryRange {
  min: number;
  max: number;
  currency: string;
}

export interface Location {
  city: string;
  country: string;
}

export interface Job {
  id: string;
  title: string;
  company: string;
  location: Location;
  salary: SalaryRange;
  type: JobType;
  postedAt: string; // ISO date string
  experienceLevel: number; // years
  skills: string[];
  matchScore: number; // 60-98
}
