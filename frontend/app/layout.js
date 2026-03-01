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
                    {/* Medical Disclaimer Banner */}
                    <div style={{
                        background: 'rgba(245, 158, 11, 0.06)',
                        borderBottom: '1px solid rgba(245, 158, 11, 0.2)',
                        padding: '0.5rem',
                        textAlign: 'center',
                        fontSize: '0.75rem',
                        color: '#92400E',
                        letterSpacing: '0.02em',
                        fontWeight: '500'
                    }}>
                        ⚠️ Medical Disclaimer: This tool does not provide medical advice or diagnosis. Always consult a qualified healthcare professional.
                    </div>

                    {children}

                    {/* Footer */}
                    <footer style={{
                        marginTop: '4rem',
                        padding: '3rem 2rem',
                        textAlign: 'center',
                        borderTop: '1px solid var(--border-light)',
                        background: 'var(--bg-secondary)',
                        color: 'var(--text-tertiary)'
                    }}>
                        <div style={{ maxWidth: '600px', margin: '0 auto' }}>
                            <p style={{ fontSize: '0.9375rem', fontWeight: '700', color: 'var(--emerald-green)', marginBottom: '0.5rem' }}>
                                Arogya AI
                            </p>
                            <p style={{ fontSize: '0.8125rem' }}>
                                Intelligent healthcare companion for early risk prediction &amp; preventive care.
                                Built upon WHO-validated clinical protocols.
                            </p>
                        </div>
                    </footer>
                </AuthProvider>
            </body>
        </html>
    )
}
