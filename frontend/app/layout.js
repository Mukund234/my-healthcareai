import './globals.css'
import { AuthProvider } from '../contexts/AuthContext'

export const metadata = {
    title: 'Early Health Risk Predictor - AI-Powered Prevention',
    description: 'Predict and prevent health risks with AI-powered analysis. Get personalized recommendations for diabetes, hypertension, and cardiovascular health.',
}

export default function RootLayout({ children }) {
    return (
        <html lang="en">
            <head>
                <link rel="preconnect" href="https://fonts.googleapis.com" />
                <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
                <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet" />
            </head>
            <body style={{ background: 'var(--bg-primary)', color: 'var(--text-primary)' }}>
                <AuthProvider>
                    {/* Medical Disclaimer Banner - Cyber Style */}
                    <div style={{
                        background: 'rgba(255, 42, 42, 0.05)',
                        borderBottom: '1px solid rgba(255, 42, 42, 0.2)',
                        padding: '0.5rem',
                        textAlign: 'center',
                        fontSize: '0.75rem',
                        color: 'var(--cyber-red)',
                        textTransform: 'uppercase',
                        letterSpacing: '0.1em',
                        fontWeight: 'bold'
                    }}>
                        ⚠️ Medical Disclaimer: This is not medical advice or diagnosis. Consult a professional provider.
                    </div>

                    {children}

                    {/* Footer - Cyber Style */}
                    <footer style={{
                        marginTop: '4rem',
                        padding: '3rem 2rem',
                        textAlign: 'center',
                        borderTop: '1px solid var(--border-subtle)',
                        background: 'var(--bg-secondary)',
                        color: 'var(--text-tertiary)'
                    }}>
                        <div style={{ maxWidth: '600px', margin: '0 auto' }}>
                            <p style={{ fontSize: '0.875rem', fontWeight: 'bold', color: 'var(--text-secondary)', marginBottom: '0.5rem' }}>
                                AROGYA AI - CYBER DIAGNOSTIC SYSTEM v4.2.1
                            </p>
                            <p style={{ fontSize: '0.75rem' }}>
                                Developed for early risk prediction & preventive oversight.
                                Built upon WHO-validated clinical protocols.
                            </p>
                        </div>
                    </footer>
                </AuthProvider>
            </body>
        </html>
    )
}
