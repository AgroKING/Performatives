import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
    title: 'Skill Gap Analysis & Learning Roadmap',
    description: 'Analyze your skill gaps and get personalized learning roadmaps',
};

export default function RootLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <html lang="en">
            <body>{children}</body>
        </html>
    );
}
