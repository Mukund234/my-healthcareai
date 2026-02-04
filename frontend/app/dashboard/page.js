'use client';

import { useAuth } from '../../contexts/AuthContext';
import { useRouter } from 'next/navigation';
import ProtectedRoute from '../../components/ProtectedRoute';

function DashboardContent() {
    const { user, signOut } = useAuth();
    const router = useRouter();

    const handleSignOut = async () => {
        await signOut();
        router.push('/');
    };

    return (
        <div className="min-h-screen bg-bg-primary">
            {/* Header */}
            <header className="bg-bg-elevated border-b border-border-subtle">
                <div className="container mx-auto px-4 py-4 flex items-center justify-between">
                    <div className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-full bg-gradient-primary flex items-center justify-center">
                            <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                            </svg>
                        </div>
                        <div>
                            <h1 className="text-lg font-semibold text-text-primary">
                                Welcome, {user?.displayName || 'User'}
                            </h1>
                            <p className="text-sm text-text-secondary">{user?.email}</p>
                        </div>
                    </div>
                    <button
                        onClick={handleSignOut}
                        className="px-4 py-2 text-text-secondary hover:text-text-primary transition-colors"
                    >
                        Sign Out
                    </button>
                </div>
            </header>

            {/* Main Content */}
            <main className="container mx-auto px-4 py-8 max-w-6xl">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {/* Start Assessment Card */}
                    <div className="glass-card-premium p-8 cursor-pointer group" onClick={() => router.push('/chat')}>
                        <div className="w-16 h-16 rounded-full bg-gradient-accent flex items-center justify-center mb-5 group-hover:scale-110 transition-transform duration-300" style={{ boxShadow: '0 8px 24px rgba(99, 102, 241, 0.3)' }}>
                            <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                            </svg>
                        </div>
                        <h3 className="text-xl font-semibold text-text-primary mb-3">New Assessment</h3>
                        <p className="text-text-secondary text-sm leading-relaxed">Start a new health risk assessment with our AI-powered system</p>
                        <div className="mt-4 text-accent-primary font-medium text-sm flex items-center gap-2 group-hover:gap-3 transition-all">
                            Get Started <span>→</span>
                        </div>
                    </div>

                    {/* History Card */}
                    <div className="glass-card-premium p-8">
                        <div className="w-16 h-16 rounded-full bg-bg-tertiary flex items-center justify-center mb-5 border border-border-medium">
                            <svg className="w-8 h-8 text-text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                        </div>
                        <h3 className="text-xl font-semibold text-text-primary mb-3">Assessment History</h3>
                        <p className="text-text-secondary text-sm leading-relaxed">View your past assessments and track your progress</p>
                        <p className="text-text-tertiary text-xs mt-4 italic">Coming soon</p>
                    </div>

                    {/* Recommendations Card */}
                    <div className="glass-card-premium p-8">
                        <div className="w-16 h-16 rounded-full bg-bg-tertiary flex items-center justify-center mb-5 border border-border-medium">
                            <svg className="w-8 h-8 text-text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                        </div>
                        <h3 className="text-xl font-semibold text-text-primary mb-3">My Recommendations</h3>
                        <p className="text-text-secondary text-sm leading-relaxed">Personalized health tips based on your assessments</p>
                        <p className="text-text-tertiary text-xs mt-4 italic">Coming soon</p>
                    </div>
                </div>

                {/* Info Section */}
                <div className="mt-10 glass-card-premium p-8">
                    <h2 className="text-2xl font-semibold text-text-primary mb-6">About Your Account</h2>
                    <div className="space-y-4">
                        <div className="flex justify-between py-3 border-b border-border-subtle">
                            <span className="text-text-secondary font-medium">Account Type</span>
                            <span className="text-text-primary font-semibold">Email Account</span>
                        </div>
                        <div className="flex justify-between py-3 border-b border-border-subtle">
                            <span className="text-text-secondary font-medium">Email</span>
                            <span className="text-text-primary">{user?.email}</span>
                        </div>
                        <div className="flex justify-between py-3 border-b border-border-subtle">
                            <span className="text-text-secondary font-medium">Account Status</span>
                            <span className="text-accent-success font-semibold flex items-center gap-2">
                                <span className="w-2 h-2 bg-accent-success rounded-full"></span>
                                Active
                            </span>
                        </div>
                        <div className="flex justify-between py-3">
                            <span className="text-text-secondary font-medium">Data Storage</span>
                            <span className="text-text-primary">Firebase Cloud</span>
                        </div>
                    </div>
                </div>
            </main>
        </div>
    );
}

export default function DashboardPage() {
    return (
        <ProtectedRoute>
            <DashboardContent />
        </ProtectedRoute>
    );
}
