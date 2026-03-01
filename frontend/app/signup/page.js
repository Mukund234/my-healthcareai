'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { createUserWithEmailAndPassword, updateProfile, signInWithPopup, GoogleAuthProvider } from 'firebase/auth';
import { auth } from '../../lib/firebase';
import { useAuth } from '../../contexts/AuthContext';
import Link from 'next/link';

export default function SignupPage() {
    const [fullName, setFullName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [age, setAge] = useState('');
    const [gender, setGender] = useState('');
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(false);
    const router = useRouter();
    const { dummyLogin } = useAuth();

    const handleSignup = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
        try {
            // 1. Create user in Firebase
            const userCredential = await createUserWithEmailAndPassword(auth, email, password);
            const user = userCredential.user;

            // 2. Update Firebase Profile
            await updateProfile(user, {
                displayName: fullName
            });

            // 3. (Future) Sync with our backend to save age & gender
            console.log('User created:', user.uid);

            router.push('/chat');
        } catch (err) {
            console.warn('Firebase Auth failed, falling back to dummy register for UI testing.', err);
            // Fallback for UI testing
            dummyLogin({
                email: email,
                full_name: fullName || 'New Patient',
                avatar_url: `https://ui-avatars.com/api/?name=${encodeURIComponent(fullName || 'New Patient')}&background=00f2ff&color=fff`,
                is_premium: false,
                age: age,
                gender: gender
            });
            router.push('/chat');
        } finally {
            setLoading(false);
        }
    };

    const handleGoogleSignup = async () => {
        const provider = new GoogleAuthProvider();
        try {
            await signInWithPopup(auth, provider);
            router.push('/chat');
        } catch (err) {
            console.warn('Firebase Google Auth failed, falling back to dummy register for UI testing.', err);
            // Fallback for UI testing when Firebase keys are missing
            dummyLogin({
                email: 'googleuser@example.com',
                full_name: 'Google Test User',
                avatar_url: 'https://ui-avatars.com/api/?name=Google+User&background=00f2ff&color=fff',
                is_premium: true,
                age: 'N/A',
                gender: 'N/A'
            });
            router.push('/chat');
        }
    };

    return (
        <div style={{
            minHeight: '100vh',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            padding: '2rem',
            background: 'var(--bg-primary)',
            color: 'var(--text-primary)',
            fontFamily: "'Inter', sans-serif"
        }}>
            <div className="glass-card" style={{
                width: '100%',
                maxWidth: '450px',
                padding: '2.5rem',
                display: 'flex',
                flexDirection: 'column',
                gap: '1.5rem',
                borderTop: '2px solid var(--cyber-cyan)',
            }}>
                <div style={{ textAlign: 'center', marginBottom: '0.5rem' }}>
                    <h1 style={{
                        fontSize: '1.5rem',
                        fontWeight: '700',
                        margin: 0,
                        background: 'linear-gradient(90deg, #ffffff 0%, var(--cyber-cyan) 100%)',
                        WebkitBackgroundClip: 'text',
                        WebkitTextFillColor: 'transparent',
                        textShadow: '0 0 20px rgba(0, 242, 255, 0.3)'
                    }}>Patient Registration</h1>
                    <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', marginTop: '0.5rem' }}>
                        Create your health intelligence profile
                    </p>
                </div>

                {error && (
                    <div className="diagnostic-block disclaimer-block" style={{ padding: '0.75rem', fontSize: '0.875rem' }}>
                        {error}
                    </div>
                )}

                <form onSubmit={handleSignup} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                        <label style={{ fontSize: '0.75rem', fontWeight: 'bold', color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                            Full Name
                        </label>
                        <input
                            type="text"
                            value={fullName}
                            onChange={(e) => setFullName(e.target.value)}
                            required
                            placeholder="Dr. Shreyas Gupta"
                            style={{
                                padding: '0.875rem',
                                background: 'rgba(0, 0, 0, 0.5)',
                                border: '1px solid var(--border-subtle)',
                                borderRadius: '8px',
                                color: 'white',
                                outline: 'none',
                                transition: 'all 0.2s',
                                width: '100%'
                            }}
                            onFocus={(e) => e.target.style.border = '1px solid var(--cyber-cyan)'}
                            onBlur={(e) => e.target.style.border = '1px solid var(--border-subtle)'}
                        />
                    </div>

                    <div style={{ display: 'flex', gap: '1rem' }}>
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', flex: 1 }}>
                            <label style={{ fontSize: '0.75rem', fontWeight: 'bold', color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                                Age
                            </label>
                            <input
                                type="number"
                                value={age}
                                onChange={(e) => setAge(e.target.value)}
                                required
                                min="1"
                                max="120"
                                placeholder="35"
                                style={{
                                    padding: '0.875rem',
                                    background: 'rgba(0, 0, 0, 0.5)',
                                    border: '1px solid var(--border-subtle)',
                                    borderRadius: '8px',
                                    color: 'white',
                                    outline: 'none',
                                    transition: 'all 0.2s',
                                    width: '100%'
                                }}
                                onFocus={(e) => e.target.style.border = '1px solid var(--cyber-cyan)'}
                                onBlur={(e) => e.target.style.border = '1px solid var(--border-subtle)'}
                            />
                        </div>
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', flex: 2 }}>
                            <label style={{ fontSize: '0.75rem', fontWeight: 'bold', color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                                Biological Sex
                            </label>
                            <select
                                value={gender}
                                onChange={(e) => setGender(e.target.value)}
                                required
                                style={{
                                    padding: '0.875rem',
                                    background: 'rgba(0, 0, 0, 0.5)',
                                    border: '1px solid var(--border-subtle)',
                                    borderRadius: '8px',
                                    color: 'white',
                                    outline: 'none',
                                    transition: 'all 0.2s',
                                    cursor: 'pointer',
                                    width: '100%'
                                }}
                                onFocus={(e) => e.target.style.border = '1px solid var(--cyber-cyan)'}
                                onBlur={(e) => e.target.style.border = '1px solid var(--border-subtle)'}
                            >
                                <option value="" disabled>Select</option>
                                <option value="male">Male</option>
                                <option value="female">Female</option>
                                <option value="other">Other</option>
                            </select>
                        </div>
                    </div>

                    <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                        <label style={{ fontSize: '0.75rem', fontWeight: 'bold', color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                            Secure Protocol (Email)
                        </label>
                        <input
                            type="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                            placeholder="patient@example.com"
                            style={{
                                padding: '0.875rem',
                                background: 'rgba(0, 0, 0, 0.5)',
                                border: '1px solid var(--border-subtle)',
                                borderRadius: '8px',
                                color: 'white',
                                outline: 'none',
                                transition: 'all 0.2s',
                                width: '100%'
                            }}
                            onFocus={(e) => e.target.style.border = '1px solid var(--cyber-cyan)'}
                            onBlur={(e) => e.target.style.border = '1px solid var(--border-subtle)'}
                        />
                    </div>

                    <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                        <label style={{ fontSize: '0.75rem', fontWeight: 'bold', color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                            Access Key (Password)
                        </label>
                        <input
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                            placeholder="Minimum 6 characters"
                            style={{
                                padding: '0.875rem',
                                background: 'rgba(0, 0, 0, 0.5)',
                                border: '1px solid var(--border-subtle)',
                                borderRadius: '8px',
                                color: 'white',
                                outline: 'none',
                                transition: 'all 0.2s',
                                width: '100%'
                            }}
                            onFocus={(e) => e.target.style.border = '1px solid var(--cyber-cyan)'}
                            onBlur={(e) => e.target.style.border = '1px solid var(--border-subtle)'}
                        />
                    </div>

                    <button
                        type="submit"
                        disabled={loading}
                        className="btn-primary"
                        style={{ marginTop: '0.5rem', width: '100%', padding: '0.875rem', justifyContent: 'center' }}
                    >
                        {loading ? 'Initializing...' : 'Create Profile'}
                    </button>
                </form>

                <div style={{ display: 'flex', alignItems: 'center', margin: '0.5rem 0' }}>
                    <div style={{ flex: 1, height: '1px', background: 'var(--border-subtle)' }}></div>
                    <span style={{ padding: '0 1rem', fontSize: '0.75rem', color: 'var(--text-tertiary)' }}>OR</span>
                    <div style={{ flex: 1, height: '1px', background: 'var(--border-subtle)' }}></div>
                </div>

                <button
                    type="button"
                    onClick={handleGoogleSignup}
                    style={{
                        padding: '0.875rem',
                        background: 'transparent',
                        border: '1px solid var(--border-subtle)',
                        borderRadius: '8px',
                        color: 'white',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        gap: '0.5rem',
                        cursor: 'pointer',
                        transition: 'background 0.2s',
                        fontWeight: '500'
                    }}
                    onMouseOver={(e) => e.currentTarget.style.background = 'rgba(255,255,255,0.05)'}
                    onMouseOut={(e) => e.currentTarget.style.background = 'transparent'}
                >
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4" />
                        <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853" />
                        <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05" />
                        <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335" />
                    </svg>
                    Continue with Google
                </button>

                <div style={{ textAlign: 'center', fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
                    Already registered? <Link href="/login" style={{ color: 'var(--cyber-cyan)', textDecoration: 'none', fontWeight: 'bold' }}>Initiate Login</Link>
                </div>
            </div>
        </div>
    );
}
