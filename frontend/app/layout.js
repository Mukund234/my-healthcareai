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
            <body>
                <AuthProvider>
                    {/* Medical Disclaimer Banner */}
                    <div style={{
                        background: 'rgba(255, 107, 157, 0.1)',
                        borderBottom: '2px solid rgba(255, 107, 157, 0.3)',
                        padding: '0.75rem',
                        textAlign: 'center',
                        fontSize: '0.875rem',
                        color: '#ff6b9d'
                    }}>
                        ⚠️ <strong>Medical Disclaimer:</strong> This is not medical advice or diagnosis. Consult a qualified healthcare provider for medical decisions.
                    </div>

                    {children}

                    {/* Footer */}
                    <footer style={{
                        marginTop: '4rem',
                        padding: '2rem',
                        textAlign: 'center',
                        borderTop: '1px solid rgba(255, 255, 255, 0.1)',
                        color: 'var(--text-muted)'
                    }}>
                        <p>Early Health Risk Predictor v1.0 | For Educational & Preventive Purposes Only</p>
                        <p style={{ fontSize: '0.875rem', marginTop: '0.5rem' }}>
                            Always consult with qualified healthcare professionals for medical advice
                        </p>
                    </footer>
                </AuthProvider>
            </body>
        </html>
    )
}
