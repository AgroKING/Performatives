import * as fs from 'fs';
import * as path from 'path';
import { Job, JobType } from './types';

const TITLES = [
    'Frontend Developer', 'Backend Engineer', 'Full Stack Developer', 'DevOps Engineer',
    'Product Manager', 'UX/UI Designer', 'Data Scientist', 'Machine Learning Engineer',
    'Software Architect', 'QA Engineer', 'Mobile Developer', 'Cloud Engineer',
    'Security Analyst', 'Systems Administrator', 'Database Administrator'
];

const COMPANIES = [
    'TechCorp', 'InnoSys', 'WebSolutions', 'DataMinds', 'CloudNet',
    'FutureTech', 'SoftServe', 'CodeCrafters', 'ByteBuilders', 'AgileSoft',
    'NetWorks', 'Appify', 'LogicGate', 'PixelPerfect', 'QuantumLeap'
];

const CITIES = [
    'San Francisco', 'New York', 'London', 'Berlin', 'Tokyo',
    'Toronto', 'Sydney', 'Bangalore', 'Singapore', 'Austin',
    'Seattle', 'Boston', 'Amsterdam', 'Paris', 'Zurich'
];

const COUNTRIES: { [key: string]: string } = {
    'San Francisco': 'USA', 'New York': 'USA', 'Austin': 'USA', 'Seattle': 'USA', 'Boston': 'USA',
    'London': 'UK', 'Berlin': 'Germany', 'Tokyo': 'Japan', 'Toronto': 'Canada', 'Sydney': 'Australia',
    'Bangalore': 'India', 'Singapore': 'Singapore', 'Amsterdam': 'Netherlands', 'Paris': 'France', 'Zurich': 'Switzerland'
};

const SKILLS = [
    'React', 'Node.js', 'Python', 'TypeScript', 'AWS', 'Docker', 'Kubernetes',
    'Java', 'Go', 'Rust', 'Figma', 'Sketch', 'SQL', 'NoSQL', 'GraphQL',
    'Rest API', 'CI/CD', 'Terraform', 'Ansible', 'Linux'
];

const JOB_TYPES = Object.values(JobType);

function getRandomElement<T>(arr: T[]): T {
    return arr[Math.floor(Math.random() * arr.length)];
}

function getRandomInt(min: number, max: number): number {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

function getRandomSubset<T>(arr: T[], min: number, max: number): T[] {
    const shuffled = arr.slice().sort(() => 0.5 - Math.random());
    return shuffled.slice(0, getRandomInt(min, max));
}

function generateJob(id: string): Job {
    const title = getRandomElement(TITLES);
    const company = getRandomElement(COMPANIES);
    const city = getRandomElement(CITIES);
    const country = COUNTRIES[city];

    // Ensure salary min < max
    const minSalary = getRandomInt(60, 150) * 1000;
    const maxSalary = minSalary + getRandomInt(10, 50) * 1000;

    // Realistic distribution for match score (60-98)
    const matchScore = getRandomInt(60, 98);

    // Weighted Job Type distribution
    // 40% FullTime, 30% Remote, 10% each for others
    const rand = Math.random();
    let type: JobType;
    if (rand < 0.4) type = JobType.FullTime;
    else if (rand < 0.7) type = JobType.Remote;
    else type = getRandomElement(JOB_TYPES.filter(t => t !== JobType.FullTime && t !== JobType.Remote));

    return {
        id,
        title,
        company,
        location: { city, country },
        salary: { min: minSalary, max: maxSalary, currency: 'USD' },
        type,
        postedAt: new Date(Date.now() - getRandomInt(0, 30) * 24 * 60 * 60 * 1000).toISOString(),
        experienceLevel: getRandomInt(1, 10),
        skills: getRandomSubset(SKILLS, 3, 8),
        matchScore
    };
}

function generateJobs(count: number): Job[] {
    const jobs: Job[] = [];
    const ids = new Set<string>();

    for (let i = 0; i < count; i++) {
        let id = Math.random().toString(36).substring(2, 11);
        while (ids.has(id)) {
            id = Math.random().toString(36).substring(2, 11);
        }
        ids.add(id);

        const job = generateJob(id);

        // Self-Correction Protocol
        if (job.salary.min >= job.salary.max) {
            console.warn(`Correction: Salary invalid for job ${id}. Fixing.`);
            job.salary.max = job.salary.min + 10000;
        }

        jobs.push(job);
    }
    return jobs;
}

const jobs = generateJobs(55); // Generating 50+ jobs

// Validation
const uniqueIds = new Set(jobs.map(j => j.id));
if (uniqueIds.size !== jobs.length) {
    throw new Error('Duplicate IDs found!');
}

jobs.forEach(job => {
    if (job.salary.min >= job.salary.max) {
        throw new Error(`Invalid salary range for job ${job.id}`);
    }
});

const outputPath = path.join(process.cwd(), 'jobs.json');
fs.writeFileSync(outputPath, JSON.stringify(jobs, null, 2));

console.log(`Successfully generated ${jobs.length} jobs to ${outputPath}`);
