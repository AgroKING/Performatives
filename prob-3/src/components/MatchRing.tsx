import React from 'react';

interface MatchRingProps {
    score: number;
    size?: number;
    strokeWidth?: number;
}

const MatchRing: React.FC<MatchRingProps> = ({ score, size = 50, strokeWidth = 4 }) => {
    const radius = (size - strokeWidth) / 2;
    const circumference = 2 * Math.PI * radius;
    const offset = circumference - (score / 100) * circumference;

    let colorClass = 'text-green-500';
    if (score < 60) colorClass = 'text-red-500';
    else if (score < 80) colorClass = 'text-yellow-500';

    return (
        <div className="relative flex items-center justify-center" style={{ width: size, height: size }}>
            <svg width={size} height={size} className="transform -rotate-90">
                {/* Background Ring */}
                <circle
                    cx={size / 2}
                    cy={size / 2}
                    r={radius}
                    stroke="currentColor"
                    strokeWidth={strokeWidth}
                    fill="transparent"
                    className="text-gray-200"
                />
                {/* Progress Ring */}
                <circle
                    cx={size / 2}
                    cy={size / 2}
                    r={radius}
                    stroke="currentColor"
                    strokeWidth={strokeWidth}
                    fill="transparent"
                    strokeDasharray={circumference}
                    strokeDashoffset={offset}
                    strokeLinecap="round"
                    className={colorClass}
                />
            </svg>
            <span className="absolute text-xs font-bold text-gray-700">{score}%</span>
        </div>
    );
};

export default MatchRing;
