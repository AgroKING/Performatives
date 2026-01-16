import Link from 'next/link';
import { Sparkles, ArrowRight, Target, TrendingUp, Map } from 'lucide-react';

export default function HomePage() {
    return (
        <main className="min-h-screen flex items-center justify-center p-4">
            <div className="max-w-4xl w-full text-center space-y-8 animate-fade-in">
                {/* Hero Section */}
                <div className="space-y-6">
                    <div className="flex items-center justify-center gap-4 mb-6">
                        <Sparkles className="w-16 h-16 text-blue-600" />
                    </div>

                    <h1 className="text-6xl font-bold text-gradient mb-4">
                        Skill Gap Analyzer
                    </h1>

                    <p className="text-xl text-slate-600 max-w-2xl mx-auto leading-relaxed">
                        Discover your skill gaps, get personalized learning roadmaps, and accelerate your career growth with data-driven insights
                    </p>
                </div>

                {/* Features Grid */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 my-12">
                    <div className="card text-left">
                        <div className="p-3 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-xl w-fit mb-4">
                            <Target className="w-6 h-6 text-white" />
                        </div>
                        <h3 className="text-lg font-bold text-slate-800 mb-2">Gap Analysis</h3>
                        <p className="text-sm text-slate-600">
                            Compare your current skills against target roles with weighted readiness scoring
                        </p>
                    </div>

                    <div className="card text-left">
                        <div className="p-3 bg-gradient-to-br from-purple-500 to-pink-600 rounded-xl w-fit mb-4">
                            <Map className="w-6 h-6 text-white" />
                        </div>
                        <h3 className="text-lg font-bold text-slate-800 mb-2">Learning Roadmap</h3>
                        <p className="text-sm text-slate-600">
                            Get prerequisite-aware learning paths with curated resources and time estimates
                        </p>
                    </div>

                    <div className="card text-left">
                        <div className="p-3 bg-gradient-to-br from-emerald-500 to-teal-600 rounded-xl w-fit mb-4">
                            <TrendingUp className="w-6 h-6 text-white" />
                        </div>
                        <h3 className="text-lg font-bold text-slate-800 mb-2">Success Insights</h3>
                        <p className="text-sm text-slate-600">
                            See success rates and timelines from similar career transitions
                        </p>
                    </div>
                </div>

                {/* CTA Button */}
                <div className="space-y-4">
                    <Link href="/dashboard" className="inline-block">
                        <button className="btn-primary text-lg px-8 py-4 group">
                            <span className="flex items-center gap-3">
                                Launch Dashboard
                                <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                            </span>
                        </button>
                    </Link>

                    <p className="text-sm text-slate-500">
                        No signup required • Instant analysis • Free to use
                    </p>
                </div>

                {/* API Info */}
                <div className="mt-16 p-6 bg-slate-900 rounded-xl text-left">
                    <h3 className="text-white font-semibold mb-3">🚀 API Endpoints Available</h3>
                    <div className="space-y-2 text-sm font-mono">
                        <div className="text-green-400">GET /api/taxonomy</div>
                        <div className="text-blue-400">POST /api/analyze</div>
                    </div>
                    <p className="text-slate-400 text-xs mt-3">
                        See API documentation for details
                    </p>
                </div>
            </div>
        </main>
    );
}
