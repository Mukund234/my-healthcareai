'use client'

import Link from 'next/link'
import { useState } from 'react'

export default function Home() {
    const [language, setLanguage] = useState('en')

    const content = {
        en: {
            heroTitle: 'The Future of Health Intelligence',
            heroSubtitle: 'Arogya AI — Your Intelligent Healthcare Companion',
            heroDesc: 'Get AI-powered health insights based on WHO guidelines. Predict risks early, receive personalized recommendations, and take proactive steps toward a healthier life.',
            ctaPrimary: 'Start Health Assessment',
            ctaSecondary: 'Watch Demo',
            howTitle: 'How It Works',
            steps: [
                {
                    number: '1',
                    icon: '📋',
                    title: 'Upload & Enter',
                    desc: 'Upload medical reports or answer a short health questionnaire about your lifestyle and symptoms.'
                },
                {
                    number: '2',
                    icon: '🤖',
                    title: 'AI Analysis',
                    desc: 'Our AI evaluates your data against WHO guidelines and advanced machine learning models.'
                },
                {
                    number: '3',
                    icon: '💡',
                    title: 'Personalized Insights',
                    desc: 'Receive personalized risk scores, health recommendations, and action steps tailored for you.'
                }
            ],
            featuresTitle: 'Why Choose Arogya AI?',
            features: [
                { icon: '🎯', title: 'Predictive Analysis', desc: 'AI-powered risk assessment for diabetes, hypertension, and heart disease.' },
                { icon: '🏥', title: 'WHO-Aligned Guidelines', desc: 'Based on validated World Health Organization clinical protocols.' },
                { icon: '💡', title: 'Personalized Recommendations', desc: 'Age-specific guidance tailored to your unique health profile and lifestyle.' },
                { icon: '🔒', title: 'Privacy & Security', desc: 'Your health data is encrypted and never shared without your explicit consent.' },
                { icon: '🌍', title: 'Multilingual Support', desc: 'Available in English and Hindi for broader accessibility.' },
                { icon: '⚡', title: 'Instant Results', desc: 'Get your risk assessment in seconds — no lab tests or appointments needed.' }
            ],
            safetyTitle: 'Safety & Ethics',
            safetyPoints: [
                'No diagnosis or prescriptions — prevention focused only',
                'Evidence-based recommendations from WHO guidelines',
                'Clear disclaimers displayed on every page',
                'Doctor consultation suggested for high-risk cases',
                'Your explicit consent required before any data processing'
            ],
            disclaimer: 'This tool is for informational and preventive purposes only. It does not replace professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare provider.'
        },
        hi: {
            heroTitle: 'स्वास्थ्य बुद्धिमत्ता का भविष्य',
            heroSubtitle: 'आरोग्य AI — आपका बुद्धिमान स्वास्थ्य साथी',
            heroDesc: 'WHO दिशानिर्देशों पर आधारित AI-संचालित स्वास्थ्य जानकारी प्राप्त करें। जोखिम का जल्दी पता लगाएं और एक स्वस्थ जीवन की ओर कदम बढ़ाएं।',
            ctaPrimary: 'स्वास्थ्य मूल्यांकन शुरू करें',
            ctaSecondary: 'डेमो देखें',
            howTitle: 'यह कैसे काम करता है',
            steps: [
                { number: '1', icon: '📋', title: 'अपलोड और दर्ज करें', desc: 'मेडिकल रिपोर्ट अपलोड करें या अपनी जीवनशैली के बारे में एक छोटी स्वास्थ्य प्रश्नावली भरें।' },
                { number: '2', icon: '🤖', title: 'AI विश्लेषण', desc: 'हमारा AI WHO दिशानिर्देशों और उन्नत ML मॉडल का उपयोग करके आपके डेटा का मूल्यांकन करता है।' },
                { number: '3', icon: '💡', title: 'व्यक्तिगत जानकारी', desc: 'आपके लिए अनुकूलित जोखिम स्कोर, स्वास्थ्य सुझाव और कार्य योजना प्राप्त करें।' }
            ],
            featuresTitle: 'आरोग्य AI क्यों चुनें?',
            features: [
                { icon: '🎯', title: 'भविष्यवाणी विश्लेषण', desc: 'मधुमेह, उच्च रक्तचाप और हृदय रोग के लिए AI-संचालित जोखिम मूल्यांकन।' },
                { icon: '🏥', title: 'WHO-संरेखित दिशानिर्देश', desc: 'विश्व स्वास्थ्य संगठन के मान्य नैदानिक प्रोटोकॉल पर आधारित।' },
                { icon: '💡', title: 'व्यक्तिगत सुझाव', desc: 'आपकी अनूठी स्वास्थ्य प्रोफ़ाइल के अनुरूप आयु-विशिष्ट मार्गदर्शन।' },
                { icon: '🔒', title: 'गोपनीयता और सुरक्षा', desc: 'आपका स्वास्थ्य डेटा एन्क्रिप्टेड है और बिना सहमति के साझा नहीं किया जाता।' },
                { icon: '🌍', title: 'बहुभाषी सहायता', desc: 'व्यापक पहुंच के लिए अंग्रेजी और हिंदी में उपलब्ध।' },
                { icon: '⚡', title: 'तत्काल परिणाम', desc: 'सेकंड में जोखिम मूल्यांकन प्राप्त करें — कोई लैब टेस्ट या अपॉइंटमेंट नहीं।' }
            ],
            safetyTitle: 'सुरक्षा और नैतिकता',
            safetyPoints: [
                'कोई निदान या नुस्खे नहीं — केवल रोकथाम पर केंद्रित',
                'WHO दिशानिर्देशों से साक्ष्य-आधारित सिफारिशें',
                'प्रत्येक पृष्ठ पर स्पष्ट अस्वीकरण',
                'उच्च जोखिम वाले मामलों के लिए डॉक्टर परामर्श का सुझाव',
                'किसी भी डेटा प्रोसेसिंग से पहले आपकी सहमति आवश्यक'
            ],
            disclaimer: 'यह टूल केवल सूचनात्मक और निवारक उद्देश्यों के लिए है। यह पेशेवर चिकित्सा सलाह, निदान या उपचार का विकल्प नहीं है।'
        }
    }

    const t = content[language]

    return (
        <div style={{ background: 'var(--bg-primary)', color: 'var(--text-primary)', fontFamily: "'Inter', sans-serif" }}>

            {/* Navigation */}
            <nav style={{
                position: 'sticky',
                top: 0,
                zIndex: 50,
                background: 'rgba(255, 255, 255, 0.95)',
                backdropFilter: 'blur(8px)',
                borderBottom: '1px solid var(--border-light)',
                padding: '0 2rem',
            }}>
                <div style={{ maxWidth: '1280px', margin: '0 auto', display: 'flex', alignItems: 'center', justifyContent: 'space-between', height: '64px' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                        <span style={{ fontSize: '1.5rem' }}>🏥</span>
                        <span style={{ fontWeight: '800', fontSize: '1.25rem', color: 'var(--emerald-green)' }}>Arogya AI</span>
                    </div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                        {/* Language Toggle */}
                        <div style={{ display: 'flex', gap: '0.5rem' }}>
                            <button
                                onClick={() => setLanguage('en')}
                                style={{
                                    padding: '0.375rem 0.875rem',
                                    borderRadius: 'var(--radius-md)',
                                    border: language === 'en' ? 'none' : '1px solid var(--border-medium)',
                                    background: language === 'en' ? 'var(--emerald-green)' : 'transparent',
                                    color: language === 'en' ? 'white' : 'var(--text-secondary)',
                                    fontWeight: '500',
                                    fontSize: '0.875rem',
                                    cursor: 'pointer',
                                    transition: 'all 0.2s'
                                }}
                            >EN</button>
                            <button
                                onClick={() => setLanguage('hi')}
                                style={{
                                    padding: '0.375rem 0.875rem',
                                    borderRadius: 'var(--radius-md)',
                                    border: language === 'hi' ? 'none' : '1px solid var(--border-medium)',
                                    background: language === 'hi' ? 'var(--emerald-green)' : 'transparent',
                                    color: language === 'hi' ? 'white' : 'var(--text-secondary)',
                                    fontWeight: '500',
                                    fontSize: '0.875rem',
                                    cursor: 'pointer',
                                    transition: 'all 0.2s'
                                }}
                            >हि</button>
                        </div>
                        <Link href="/login" style={{ textDecoration: 'none', color: 'var(--text-secondary)', fontWeight: '500', fontSize: '0.9375rem' }}>Sign In</Link>
                        <Link
                            href="/chat"
                            style={{
                                textDecoration: 'none',
                                background: 'var(--emerald-green)',
                                color: 'white',
                                padding: '0.5rem 1.25rem',
                                borderRadius: 'var(--radius-md)',
                                fontWeight: '600',
                                fontSize: '0.9375rem',
                                transition: 'background 0.2s'
                            }}
                        >Get Started</Link>
                    </div>
                </div>
            </nav>

            {/* Hero Section */}
            <section style={{
                background: 'linear-gradient(135deg, rgba(16,185,129,0.06) 0%, rgba(37,99,235,0.06) 100%)',
                padding: '6rem 2rem 5rem',
                textAlign: 'center'
            }}>
                <div style={{ maxWidth: '800px', margin: '0 auto' }} className="fade-in">
                    <div style={{
                        display: 'inline-block',
                        background: 'var(--emerald-green-light)',
                        color: 'var(--emerald-green-hover)',
                        padding: '0.375rem 1rem',
                        borderRadius: '9999px',
                        fontSize: '0.875rem',
                        fontWeight: '600',
                        marginBottom: '1.5rem'
                    }}>
                        🌿 AI-Powered Preventive Healthcare
                    </div>
                    <h1 style={{
                        fontSize: 'clamp(2.5rem, 5vw, 3.5rem)',
                        fontWeight: '800',
                        color: 'var(--text-primary)',
                        lineHeight: '1.15',
                        marginBottom: '1.5rem'
                    }}>
                        {t.heroTitle}
                    </h1>
                    <p style={{ fontSize: '1.25rem', color: 'var(--emerald-green)', fontWeight: '600', marginBottom: '1rem' }}>
                        {t.heroSubtitle}
                    </p>
                    <p style={{ fontSize: '1.0625rem', color: 'var(--text-secondary)', lineHeight: '1.8', marginBottom: '2.5rem', maxWidth: '640px', margin: '0 auto 2.5rem' }}>
                        {t.heroDesc}
                    </p>
                    <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center', flexWrap: 'wrap' }}>
                        <Link
                            href="/chat"
                            style={{
                                textDecoration: 'none',
                                display: 'inline-flex',
                                alignItems: 'center',
                                gap: '0.5rem',
                                background: 'var(--emerald-green)',
                                color: 'white',
                                padding: '0.875rem 2rem',
                                borderRadius: 'var(--radius-lg)',
                                fontWeight: '600',
                                fontSize: '1rem',
                                transition: 'all 0.2s',
                                boxShadow: 'var(--shadow-md)'
                            }}
                        >
                            {t.ctaPrimary} →
                        </Link>
                        <Link
                            href="#how-it-works"
                            style={{
                                textDecoration: 'none',
                                display: 'inline-flex',
                                alignItems: 'center',
                                gap: '0.5rem',
                                background: 'white',
                                color: 'var(--emerald-green)',
                                padding: '0.875rem 2rem',
                                borderRadius: 'var(--radius-lg)',
                                fontWeight: '600',
                                fontSize: '1rem',
                                border: '2px solid var(--emerald-green)',
                                transition: 'all 0.2s'
                            }}
                        >
                            ▶ {t.ctaSecondary}
                        </Link>
                    </div>

                    {/* Dashboard Preview Mockup */}
                    <div style={{
                        marginTop: '4rem',
                        background: 'white',
                        borderRadius: 'var(--radius-xl)',
                        boxShadow: 'var(--shadow-xl)',
                        border: '1px solid var(--border-light)',
                        overflow: 'hidden',
                        maxWidth: '700px',
                        margin: '4rem auto 0'
                    }}>
                        <div style={{ background: 'var(--bg-secondary)', padding: '0.75rem 1rem', borderBottom: '1px solid var(--border-light)', display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
                            <div style={{ width: '12px', height: '12px', borderRadius: '50%', background: '#EF4444' }}></div>
                            <div style={{ width: '12px', height: '12px', borderRadius: '50%', background: '#F59E0B' }}></div>
                            <div style={{ width: '12px', height: '12px', borderRadius: '50%', background: '#10B981' }}></div>
                            <span style={{ marginLeft: '0.5rem', fontSize: '0.75rem', color: 'var(--text-tertiary)' }}>Arogya AI Dashboard</span>
                        </div>
                        <div style={{ padding: '2rem', display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '1rem' }}>
                            {[
                                { label: 'Health Score', value: '87/100', color: '#10B981' },
                                { label: 'Risk Level', value: 'Low', color: '#2563EB' },
                                { label: 'Last Check', value: 'Today', color: '#F59E0B' }
                            ].map((stat, i) => (
                                <div key={i} style={{ textAlign: 'center', padding: '1rem', background: 'var(--bg-secondary)', borderRadius: 'var(--radius-md)' }}>
                                    <div style={{ fontSize: '1.5rem', fontWeight: '800', color: stat.color }}>{stat.value}</div>
                                    <div style={{ fontSize: '0.75rem', color: 'var(--text-tertiary)', marginTop: '0.25rem' }}>{stat.label}</div>
                                </div>
                            ))}
                        </div>
                        <div style={{ padding: '0 2rem 2rem', display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                            {['Cardiovascular Health', 'Blood Glucose Risk', 'Blood Pressure'].map((item, i) => (
                                <div key={i} style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                                    <span style={{ fontSize: '0.8125rem', color: 'var(--text-secondary)', width: '170px', textAlign: 'left' }}>{item}</span>
                                    <div style={{ flex: 1, height: '8px', background: 'var(--bg-tertiary)', borderRadius: '9999px', overflow: 'hidden' }}>
                                        <div style={{ width: `${[72, 45, 60][i]}%`, height: '100%', background: 'var(--emerald-green)', borderRadius: '9999px' }}></div>
                                    </div>
                                    <span style={{ fontSize: '0.8125rem', fontWeight: '600', color: 'var(--text-primary)', width: '35px', textAlign: 'right' }}>{[72, 45, 60][i]}%</span>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </section>

            {/* How It Works */}
            <section id="how-it-works" style={{ padding: '5rem 2rem', background: 'white' }}>
                <div style={{ maxWidth: '1100px', margin: '0 auto' }}>
                    <h2 style={{ textAlign: 'center', fontSize: '2rem', fontWeight: '700', color: 'var(--text-primary)', marginBottom: '0.75rem' }}>{t.howTitle}</h2>
                    <p style={{ textAlign: 'center', color: 'var(--text-secondary)', marginBottom: '3.5rem', fontSize: '1.0625rem' }}>
                        Three simple steps to better health insights
                    </p>
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '2rem' }}>
                        {t.steps.map((step, index) => (
                            <div key={index} style={{ textAlign: 'center', padding: '2.5rem 2rem', background: 'var(--bg-secondary)', borderRadius: 'var(--radius-xl)', border: '1px solid var(--border-light)', position: 'relative' }}>
                                <div style={{
                                    width: '56px',
                                    height: '56px',
                                    borderRadius: '50%',
                                    background: 'var(--emerald-green)',
                                    color: 'white',
                                    display: 'flex',
                                    alignItems: 'center',
                                    justifyContent: 'center',
                                    fontSize: '1.25rem',
                                    fontWeight: '800',
                                    margin: '0 auto 1.25rem',
                                    boxShadow: '0 4px 12px rgba(16,185,129,0.3)'
                                }}>
                                    {step.number}
                                </div>
                                <div style={{ fontSize: '2.5rem', marginBottom: '1rem' }}>{step.icon}</div>
                                <h3 style={{ fontSize: '1.25rem', fontWeight: '600', color: 'var(--text-primary)', marginBottom: '0.75rem' }}>{step.title}</h3>
                                <p style={{ color: 'var(--text-secondary)', lineHeight: '1.7', fontSize: '0.9375rem' }}>{step.desc}</p>
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            {/* Features Grid */}
            <section style={{ padding: '5rem 2rem', background: 'var(--bg-secondary)' }}>
                <div style={{ maxWidth: '1100px', margin: '0 auto' }}>
                    <h2 style={{ textAlign: 'center', fontSize: '2rem', fontWeight: '700', color: 'var(--text-primary)', marginBottom: '0.75rem' }}>{t.featuresTitle}</h2>
                    <p style={{ textAlign: 'center', color: 'var(--text-secondary)', marginBottom: '3.5rem', fontSize: '1.0625rem' }}>
                        Comprehensive tools designed for your health journey
                    </p>
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '1.5rem' }}>
                        {t.features.map((feature, index) => (
                            <div key={index} className="glass-card-premium" style={{ padding: '2rem', display: 'flex', gap: '1.25rem', alignItems: 'flex-start' }}>
                                <div style={{
                                    width: '48px',
                                    height: '48px',
                                    borderRadius: 'var(--radius-md)',
                                    background: 'var(--emerald-green-light)',
                                    display: 'flex',
                                    alignItems: 'center',
                                    justifyContent: 'center',
                                    fontSize: '1.5rem',
                                    flexShrink: 0
                                }}>
                                    {feature.icon}
                                </div>
                                <div>
                                    <h3 style={{ fontSize: '1.0625rem', fontWeight: '600', color: 'var(--text-primary)', marginBottom: '0.5rem' }}>{feature.title}</h3>
                                    <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: '1.6', margin: 0 }}>{feature.desc}</p>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            {/* Trust & Safety Section */}
            <section style={{ padding: '5rem 2rem', background: 'white' }}>
                <div style={{ maxWidth: '800px', margin: '0 auto' }}>
                    <div style={{ textAlign: 'center', marginBottom: '3rem' }}>
                        <div style={{ fontSize: '2.5rem', marginBottom: '1rem' }}>🛡️</div>
                        <h2 style={{ fontSize: '2rem', fontWeight: '700', color: 'var(--text-primary)', marginBottom: '0.75rem' }}>{t.safetyTitle}</h2>
                        <p style={{ color: 'var(--text-secondary)', fontSize: '1.0625rem' }}>
                            We are committed to responsible, ethical AI in healthcare
                        </p>
                    </div>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', marginBottom: '2.5rem' }}>
                        {t.safetyPoints.map((point, index) => (
                            <div key={index} style={{ display: 'flex', alignItems: 'flex-start', gap: '0.875rem', padding: '1rem 1.25rem', background: 'var(--emerald-green-light)', borderRadius: 'var(--radius-md)', border: '1px solid rgba(16,185,129,0.2)' }}>
                                <span style={{ color: 'var(--emerald-green)', fontWeight: '700', fontSize: '1.125rem', flexShrink: 0 }}>✓</span>
                                <span style={{ color: 'var(--text-primary)', fontSize: '0.9375rem', lineHeight: '1.6' }}>{point}</span>
                            </div>
                        ))}
                    </div>
                    {/* Disclaimer */}
                    <div style={{
                        background: 'rgba(245,158,11,0.06)',
                        border: '1px solid rgba(245,158,11,0.2)',
                        borderLeft: '3px solid var(--warning)',
                        padding: '1.25rem',
                        borderRadius: 'var(--radius-md)',
                        fontSize: '0.875rem',
                        color: 'var(--text-secondary)',
                        lineHeight: '1.6'
                    }}>
                        <strong style={{ color: '#92400E' }}>⚠️ Medical Disclaimer: </strong>
                        {t.disclaimer}
                    </div>
                </div>
            </section>

            {/* Bottom CTA */}
            <section style={{ padding: '5rem 2rem', background: 'linear-gradient(135deg, var(--emerald-green) 0%, var(--royal-blue) 100%)', textAlign: 'center' }}>
                <div style={{ maxWidth: '600px', margin: '0 auto' }}>
                    <h2 style={{ fontSize: 'clamp(1.75rem, 4vw, 2.5rem)', fontWeight: '800', color: 'white', marginBottom: '1rem' }}>
                        Ready to Take Control of Your Health?
                    </h2>
                    <p style={{ color: 'rgba(255,255,255,0.85)', fontSize: '1.0625rem', marginBottom: '2.5rem', lineHeight: '1.7' }}>
                        Start your personalized health assessment in just a few minutes. No lab tests needed.
                    </p>
                    <Link
                        href="/chat"
                        style={{
                            textDecoration: 'none',
                            display: 'inline-flex',
                            alignItems: 'center',
                            gap: '0.5rem',
                            background: 'white',
                            color: 'var(--emerald-green)',
                            padding: '0.875rem 2.5rem',
                            borderRadius: 'var(--radius-lg)',
                            fontWeight: '700',
                            fontSize: '1rem',
                            transition: 'all 0.2s',
                            boxShadow: 'var(--shadow-lg)'
                        }}
                    >
                        {t.ctaPrimary} →
                    </Link>
                </div>
            </section>
        </div>
    )
}
