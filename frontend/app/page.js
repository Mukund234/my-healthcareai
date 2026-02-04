'use client'

import Link from 'next/link'
import { useState } from 'react'

export default function Home() {
    const [language, setLanguage] = useState('en')

    const content = {
        en: {
            title: 'Early Health Risk Predictor',
            subtitle: 'AI-Powered Prevention for a Healthier Tomorrow',
            description: 'Predict and prevent health conditions before they develop. Get personalized insights based on WHO guidelines and advanced AI.',
            cta: 'Start Health Assessment',
            features: [
                {
                    icon: '🎯',
                    title: 'Predictive Analysis',
                    desc: 'AI-powered risk assessment for diabetes, hypertension, and heart disease'
                },
                {
                    icon: '🏥',
                    title: 'WHO-Aligned',
                    desc: 'Based on validated World Health Organization guidelines'
                },
                {
                    icon: '💡',
                    title: 'Personalized Tips',
                    desc: 'Age-specific recommendations tailored to your lifestyle'
                },
                {
                    icon: '🔒',
                    title: 'Privacy First',
                    desc: 'Your health data is secure and never shared without consent'
                },
                {
                    icon: '🌍',
                    title: 'Multilingual',
                    desc: 'Available in English and Hindi for wider accessibility'
                },
                {
                    icon: '⚡',
                    title: 'Instant Results',
                    desc: 'Get your risk assessment in seconds, no lab tests needed'
                }
            ],
            howItWorks: 'How It Works',
            steps: [
                {
                    number: '1',
                    title: 'Answer Questions',
                    desc: 'Complete a simple health questionnaire about your lifestyle and symptoms'
                },
                {
                    number: '2',
                    title: 'AI Analysis',
                    desc: 'Our AI evaluates your data using WHO guidelines and ML models'
                },
                {
                    number: '3',
                    title: 'Get Results',
                    desc: 'Receive personalized risk scores and prevention recommendations'
                },
                {
                    number: '4',
                    title: 'Take Action',
                    desc: 'Follow our guidance or consult a doctor if high risk is detected'
                }
            ],
            safety: 'Safety & Ethics',
            safetyPoints: [
                '✅ No diagnosis or prescriptions - prevention focused only',
                '✅ Evidence-based recommendations from WHO guidelines',
                '✅ Clear disclaimers on every page',
                '✅ Doctor consultation suggested for high-risk cases',
                '✅ Your consent required before any data processing'
            ]
        },
        hi: {
            title: 'प्रारंभिक स्वास्थ्य जोखिम भविष्यवक्ता',
            subtitle: 'एक स्वस्थ कल के लिए AI-संचालित रोकथाम',
            description: 'स्वास्थ्य स्थितियों के विकसित होने से पहले उनका पूर्वानुमान और रोकथाम करें। WHO दिशानिर्देशों और उन्नत AI के आधार पर व्यक्तिगत जानकारी प्राप्त करें।',
            cta: 'स्वास्थ्य मूल्यांकन शुरू करें',
            features: [
                {
                    icon: '🎯',
                    title: 'भविष्यवाणी विश्लेषण',
                    desc: 'मधुमेह, उच्च रक्तचाप और हृदय रोग के लिए AI-संचालित जोखिम मूल्यांकन'
                },
                {
                    icon: '🏥',
                    title: 'WHO-संरेखित',
                    desc: 'विश्व स्वास्थ्य संगठन के मान्य दिशानिर्देशों पर आधारित'
                },
                {
                    icon: '💡',
                    title: 'व्यक्तिगत सुझाव',
                    desc: 'आपकी जीवनशैली के अनुरूप आयु-विशिष्ट सिफारिशें'
                },
                {
                    icon: '🔒',
                    title: 'गोपनीयता प्रथम',
                    desc: 'आपका स्वास्थ्य डेटा सुरक्षित है और सहमति के बिना साझा नहीं किया जाता'
                },
                {
                    icon: '🌍',
                    title: 'बहुभाषी',
                    desc: 'व्यापक पहुंच के लिए अंग्रेजी और हिंदी में उपलब्ध'
                },
                {
                    icon: '⚡',
                    title: 'तत्काल परिणाम',
                    desc: 'सेकंड में अपना जोखिम मूल्यांकन प्राप्त करें, कोई लैब टेस्ट की आवश्यकता नहीं'
                }
            ],
            howItWorks: 'यह कैसे काम करता है',
            steps: [
                {
                    number: '1',
                    title: 'प्रश्नों के उत्तर दें',
                    desc: 'अपनी जीवनशैली और लक्षणों के बारे में एक सरल स्वास्थ्य प्रश्नावली पूरी करें'
                },
                {
                    number: '2',
                    title: 'AI विश्लेषण',
                    desc: 'हमारा AI WHO दिशानिर्देशों और ML मॉडल का उपयोग करके आपके डेटा का मूल्यांकन करता है'
                },
                {
                    number: '3',
                    title: 'परिणाम प्राप्त करें',
                    desc: 'व्यक्तिगत जोखिम स्कोर और रोकथाम सिफारिशें प्राप्त करें'
                },
                {
                    number: '4',
                    title: 'कार्रवाई करें',
                    desc: 'हमारे मार्गदर्शन का पालन करें या उच्च जोखिम का पता चलने पर डॉक्टर से परामर्श लें'
                }
            ],
            safety: 'सुरक्षा और नैतिकता',
            safetyPoints: [
                '✅ कोई निदान या नुस्खे नहीं - केवल रोकथाम पर केंद्रित',
                '✅ WHO दिशानिर्देशों से साक्ष्य-आधारित सिफारिशें',
                '✅ प्रत्येक पृष्ठ पर स्पष्ट अस्वीकरण',
                '✅ उच्च जोखिम वाले मामलों के लिए डॉक्टर परामर्श का सुझाव',
                '✅ किसी भी डेटा प्रोसेसिंग से पहले आपकी सहमति आवश्यक'
            ]
        }
    }

    const t = content[language]

    return (
        <div className="container">
            {/* Language Selector */}
            <div style={{ textAlign: 'right', marginBottom: '2rem' }}>
                <button
                    onClick={() => setLanguage('en')}
                    className={language === 'en' ? 'btn-gradient' : ''}
                    style={{
                        padding: '0.625rem 1.5rem',
                        marginRight: '0.75rem',
                        background: language === 'en' ? undefined : 'rgba(31, 31, 31, 0.6)',
                        backdropFilter: 'blur(10px)',
                        border: language === 'en' ? 'none' : '1px solid rgba(255, 255, 255, 0.1)',
                        borderRadius: 'var(--radius-md)',
                        color: 'white',
                        cursor: 'pointer',
                        fontWeight: '500',
                        fontSize: '0.9375rem',
                        transition: 'all 0.2s'
                    }}
                >
                    English
                </button>
                <button
                    onClick={() => setLanguage('hi')}
                    className={language === 'hi' ? 'btn-gradient' : ''}
                    style={{
                        padding: '0.625rem 1.5rem',
                        background: language === 'hi' ? undefined : 'rgba(31, 31, 31, 0.6)',
                        backdropFilter: 'blur(10px)',
                        border: language === 'hi' ? 'none' : '1px solid rgba(255, 255, 255, 0.1)',
                        borderRadius: 'var(--radius-md)',
                        color: 'white',
                        cursor: 'pointer',
                        fontWeight: '500',
                        fontSize: '0.9375rem',
                        transition: 'all 0.2s'
                    }}
                >
                    हिंदी
                </button>
            </div>

            {/* Hero Section */}
            <section className="hero-gradient" style={{ textAlign: 'center', padding: '5rem 0 4rem', marginBottom: '5rem', position: 'relative' }}>
                <div className="fade-in">
                    <h1 className="gradient-text" style={{ marginBottom: '1.5rem', fontSize: 'clamp(2.5rem, 6vw, 4.5rem)' }}>
                        {t.title}
                    </h1>
                    <p style={{ fontSize: '1.5rem', color: 'var(--text-secondary)', marginBottom: '1.5rem', fontWeight: '500' }}>
                        {t.subtitle}
                    </p>
                    <p style={{ fontSize: '1.125rem', maxWidth: '750px', margin: '0 auto 3rem', color: 'var(--text-secondary)', lineHeight: '1.8' }}>
                        {t.description}
                    </p>
                    <Link
                        href="/chat"
                        className="btn-gradient"
                        style={{
                            fontSize: '1.125rem',
                            padding: '1.25rem 3rem',
                            display: 'inline-flex',
                            alignItems: 'center',
                            gap: '0.5rem',
                            borderRadius: 'var(--radius-lg)',
                            textDecoration: 'none'
                        }}
                    >
                        {t.cta}
                        <span style={{ fontSize: '1.25rem' }}>→</span>
                    </Link>
                </div>
            </section>

            {/* Features Grid */}
            <section style={{ marginBottom: '5rem' }}>
                <h2 style={{ textAlign: 'center', marginBottom: '3.5rem' }}>Why Choose Our Platform?</h2>
                <div className="grid grid-3">
                    {t.features.map((feature, index) => (
                        <div key={index} className="glass-card-premium scroll-reveal" style={{ padding: '2.5rem', textAlign: 'center', animationDelay: `${index * 0.1}s` }}>
                            <div className="float" style={{ fontSize: '3.5rem', marginBottom: '1.5rem' }}>{feature.icon}</div>
                            <h3 style={{ fontSize: '1.25rem', marginBottom: '1rem', fontWeight: '600' }}>{feature.title}</h3>
                            <p style={{ color: 'var(--text-secondary)', fontSize: '0.95rem', lineHeight: '1.7' }}>{feature.desc}</p>
                        </div>
                    ))}
                </div>
            </section>

            {/* How It Works */}
            <section style={{ marginBottom: '5rem' }}>
                <h2 style={{ textAlign: 'center', marginBottom: '3.5rem' }}>{t.howItWorks}</h2>
                <div className="grid grid-2">
                    {t.steps.map((step, index) => (
                        <div key={index} className="glass-card-premium scroll-reveal" style={{ padding: '2.5rem', display: 'flex', gap: '1.5rem', animationDelay: `${index * 0.15}s` }}>
                            <div style={{
                                width: '70px',
                                height: '70px',
                                borderRadius: '50%',
                                background: 'var(--gradient-accent)',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                fontSize: '1.75rem',
                                fontWeight: 'bold',
                                flexShrink: 0,
                                boxShadow: '0 8px 24px rgba(99, 102, 241, 0.3)'
                            }}>
                                {step.number}
                            </div>
                            <div>
                                <h3 style={{ marginBottom: '0.75rem', fontSize: '1.375rem' }}>{step.title}</h3>
                                <p style={{ color: 'var(--text-secondary)', lineHeight: '1.7' }}>{step.desc}</p>
                            </div>
                        </div>
                    ))}
                </div>
            </section>

            {/* Safety Section */}
            <section className="glass-card-premium" style={{ padding: '3.5rem', marginBottom: '5rem' }}>
                <h2 style={{ textAlign: 'center', marginBottom: '2.5rem' }}>{t.safety}</h2>
                <div style={{ maxWidth: '750px', margin: '0 auto' }}>
                    {t.safetyPoints.map((point, index) => (
                        <p key={index} style={{ fontSize: '1.125rem', marginBottom: '1.25rem', color: 'var(--text-secondary)', display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                            <span style={{ fontSize: '1.25rem' }}>✓</span>
                            {point.replace('✅ ', '')}
                        </p>
                    ))}
                </div>
            </section>

            {/* CTA Section */}
            <section style={{ textAlign: 'center', padding: '4rem 0' }}>
                <h2 style={{ marginBottom: '1.5rem', fontSize: 'clamp(2rem, 4vw, 3rem)' }}>Ready to Take Control of Your Health?</h2>
                <p style={{ fontSize: '1.125rem', color: 'var(--text-secondary)', marginBottom: '2.5rem', maxWidth: '600px', margin: '0 auto 2.5rem' }}>
                    Start your personalized health assessment in just a few minutes
                </p>
                <Link
                    href="/chat"
                    className="btn-gradient pulse"
                    style={{
                        fontSize: '1.125rem',
                        padding: '1.25rem 3rem',
                        display: 'inline-flex',
                        alignItems: 'center',
                        gap: '0.5rem',
                        borderRadius: 'var(--radius-lg)',
                        textDecoration: 'none'
                    }}
                >
                    {t.cta}
                    <span style={{ fontSize: '1.25rem' }}>→</span>
                </Link>
            </section>
        </div>
    )
}
