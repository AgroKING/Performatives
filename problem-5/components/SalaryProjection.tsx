'use client';

import React from 'react';
import { DollarSign, TrendingUp, Calendar, Award } from 'lucide-react';

interface SalaryRange {
    min: number;
    max: number;
    currency: string;
}

interface SalaryProjectionProps {
    currentRole: string;
    targetRole: string;
    currentSalary?: SalaryRange;
    targetSalary?: SalaryRange;
    estimatedMonths: number;
    readinessScore: number;
}

export default function SalaryProjection({
    currentRole,
    targetRole,
    currentSalary,
    targetSalary,
    estimatedMonths,
    readinessScore
}: SalaryProjectionProps) {
    // Mock salary data if not provided
    const getCurrentSalary = (): SalaryRange => {
        if (currentSalary) return currentSalary;

        // Mock data based on role keywords
        if (currentRole.toLowerCase().includes('junior')) {
            return { min: 50000, max: 70000, currency: 'USD' };
        } else if (currentRole.toLowerCase().includes('mid')) {
            return { min: 70000, max: 95000, currency: 'USD' };
        } else if (currentRole.toLowerCase().includes('senior')) {
            return { min: 100000, max: 140000, currency: 'USD' };
        }
        return { min: 60000, max: 80000, currency: 'USD' };
    };

    const getTargetSalary = (): SalaryRange => {
        if (targetSalary) return targetSalary;

        // Mock data based on target role
        if (targetRole.toLowerCase().includes('senior')) {
            return { min: 100000, max: 150000, currency: 'USD' };
        } else if (targetRole.toLowerCase().includes('lead') || targetRole.toLowerCase().includes('principal')) {
            return { min: 140000, max: 200000, currency: 'USD' };
        } else if (targetRole.toLowerCase().includes('architect')) {
            return { min: 130000, max: 180000, currency: 'USD' };
        } else if (targetRole.toLowerCase().includes('devops')) {
            return { min: 90000, max: 130000, currency: 'USD' };
        }
        return { min: 85000, max: 120000, currency: 'USD' };
    };

    const current = getCurrentSalary();
    const target = getTargetSalary();

    const currentAvg = (current.min + current.max) / 2;
    const targetAvg = (target.min + target.max) / 2;
    const salaryGrowth = targetAvg - currentAvg;
    const growthPercentage = Math.round((salaryGrowth / currentAvg) * 100);

    const formatCurrency = (amount: number, currency: string): string => {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: currency,
            minimumFractionDigits: 0,
            maximumFractionDigits: 0,
        }).format(amount);
    };

    const estimatedYears = Math.ceil(estimatedMonths / 12);

    return (
        <div className="card animate-fade-in">
            <div className="flex items-center gap-3 mb-6">
                <div className="p-3 bg-gradient-to-br from-green-500 to-emerald-600 rounded-xl">
                    <DollarSign className="w-6 h-6 text-white" />
                </div>
                <div>
                    <h2 className="text-2xl font-bold text-slate-800">Salary Projection</h2>
                    <p className="text-sm text-slate-600">Estimated earnings growth</p>
                </div>
            </div>

            {/* Current vs Target Salary */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                {/* Current Salary */}
                <div className="p-4 bg-gradient-to-br from-slate-50 to-blue-50 border border-slate-200 rounded-lg">
                    <div className="text-sm font-medium text-slate-600 mb-2">Current Role</div>
                    <div className="text-lg font-bold text-slate-800 mb-1">{currentRole}</div>
                    <div className="text-3xl font-bold text-blue-600 mb-2">
                        {formatCurrency(currentAvg, current.currency)}
                    </div>
                    <div className="text-xs text-slate-500">
                        Range: {formatCurrency(current.min, current.currency)} - {formatCurrency(current.max, current.currency)}
                    </div>
                </div>

                {/* Target Salary */}
                <div className="p-4 bg-gradient-to-br from-green-50 to-emerald-50 border border-green-200 rounded-lg">
                    <div className="text-sm font-medium text-slate-600 mb-2">Target Role</div>
                    <div className="text-lg font-bold text-slate-800 mb-1">{targetRole}</div>
                    <div className="text-3xl font-bold text-green-600 mb-2">
                        {formatCurrency(targetAvg, target.currency)}
                    </div>
                    <div className="text-xs text-slate-500">
                        Range: {formatCurrency(target.min, target.currency)} - {formatCurrency(target.max, target.currency)}
                    </div>
                </div>
            </div>

            {/* Growth Metrics */}
            <div className="grid grid-cols-3 gap-4 mb-6">
                <div className="text-center p-4 bg-gradient-to-br from-green-50 to-emerald-50 rounded-lg border border-green-200">
                    <TrendingUp className="w-6 h-6 text-green-600 mx-auto mb-2" />
                    <div className="text-2xl font-bold text-green-600">+{growthPercentage}%</div>
                    <div className="text-xs text-slate-600 mt-1">Growth Rate</div>
                </div>

                <div className="text-center p-4 bg-gradient-to-br from-blue-50 to-indigo-50 rounded-lg border border-blue-200">
                    <DollarSign className="w-6 h-6 text-blue-600 mx-auto mb-2" />
                    <div className="text-2xl font-bold text-blue-600">
                        {formatCurrency(salaryGrowth, current.currency)}
                    </div>
                    <div className="text-xs text-slate-600 mt-1">Salary Increase</div>
                </div>

                <div className="text-center p-4 bg-gradient-to-br from-purple-50 to-pink-50 rounded-lg border border-purple-200">
                    <Calendar className="w-6 h-6 text-purple-600 mx-auto mb-2" />
                    <div className="text-2xl font-bold text-purple-600">{estimatedYears}y</div>
                    <div className="text-xs text-slate-600 mt-1">Est. Timeline</div>
                </div>
            </div>

            {/* Projection Timeline */}
            <div className="p-4 bg-gradient-to-r from-blue-500 to-green-500 rounded-lg text-white">
                <div className="flex items-center gap-2 mb-3">
                    <Award className="w-5 h-5" />
                    <h3 className="font-semibold">Earning Potential</h3>
                </div>
                <p className="text-sm opacity-90 mb-3">
                    Based on your {readinessScore}% readiness score and {estimatedMonths}-month learning roadmap,
                    you could increase your earning potential by <strong>{formatCurrency(salaryGrowth, current.currency)}</strong> annually.
                </p>
                <div className="flex items-center gap-2 text-sm">
                    <div className="flex-1 bg-white/20 rounded-full h-2 overflow-hidden">
                        <div
                            className="bg-white h-full rounded-full transition-all duration-1000"
                            style={{ width: `${readinessScore}%` }}
                        ></div>
                    </div>
                    <span className="font-semibold">{readinessScore}%</span>
                </div>
            </div>

            {/* Additional Insights */}
            <div className="mt-4 p-3 bg-slate-50 rounded-lg border border-slate-200">
                <p className="text-xs text-slate-600">
                    💡 <strong>Note:</strong> Salary ranges are estimates based on industry averages.
                    Actual compensation varies by location, company size, and individual negotiation.
                </p>
            </div>
        </div>
    );
}
