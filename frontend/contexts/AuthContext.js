'use client';

import { createContext, useContext, useEffect, useState } from 'react';
import {
    onAuthStateChanged,
    signOut as firebaseSignOut
} from 'firebase/auth';
import { auth } from '../lib/firebase';

const AuthContext = createContext({
    user: null,
    loading: true,
    signOut: async () => { },
    dummyLogin: (profile) => { },
});

export function AuthProvider({ children }) {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // Check for dummy session in localStorage first
        if (typeof window !== 'undefined') {
            const dummySession = localStorage.getItem('dummyUser');
            if (dummySession) {
                setUser(JSON.parse(dummySession));
                setLoading(false);
                return;
            }
        }

        const unsubscribe = onAuthStateChanged(auth, async (firebaseUser) => {
            if (firebaseUser) {
                try {
                    // Fetch auth token
                    const token = await firebaseUser.getIdToken();

                    // Fetch our backend profile using the token
                    // Assuming port 8000 for backend based on main.py
                    const response = await fetch('http://localhost:8000/api/auth/me', {
                        headers: {
                            'Authorization': `Bearer ${token}`
                        }
                    });

                    if (response.ok) {
                        const profileData = await response.json();
                        // Merge Firebase user with our DB profile
                        setUser({ ...firebaseUser, ...profileData });
                    } else {
                        // If backend fails, just use Firebase user (or might be first login needing registration)
                        setUser(firebaseUser);
                    }
                } catch (error) {
                    console.error("Error fetching user profile:", error);
                    setUser(firebaseUser);
                }
            } else {
                setUser(null);
            }
            setLoading(false);
        });

        return unsubscribe;
    }, []);

    const signOut = async () => {
        try {
            if (typeof window !== 'undefined') {
                localStorage.removeItem('dummyUser');
            }
            await firebaseSignOut(auth);
            setUser(null);
        } catch (error) {
            console.error('Error signing out:', error);
            // If firebase fails (e.g. not configured), just clear local state
            setUser(null);
        }
    };

    const dummyLogin = (profile) => {
        const dummyUser = { ...profile, uid: 'dummy-123' };
        if (typeof window !== 'undefined') {
            localStorage.setItem('dummyUser', JSON.stringify(dummyUser));
        }
        setUser(dummyUser);
    };

    return (
        <AuthContext.Provider value={{ user, loading, signOut, dummyLogin }}>
            {children}
        </AuthContext.Provider>
    );
}

export function useAuth() {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
}
