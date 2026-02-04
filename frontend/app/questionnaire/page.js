'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export default function Questionnaire() {
    const router = useRouter()
    const [step, setStep] = useState(1)
    const [loading, setLoading] = useState(false)
    const [formData, setFormData] = useState({
        age: '',
        gender: 'male',
        height_cm: '',
        weight_kg: '',
        activity_level: 'moderate',
        sleep_hours: '7',
        smoking: false,
        alcohol_consumption: 'none',
        diet_type: 'balanced',
        water_intake_liters: '2',
        fast_food_frequency: 'rarely',
        family_history: {},
        existing_conditions: [],
        medications: [],
        symptoms: [],
        stress_level: '5',
        blood_pressure_systolic: '',
        blood_pressure_diastolic: '',
        language: 'en',
        consent_given: false
    })

    const totalSteps = 5

    const handleChange = (e) => {
        const { name, value, type, checked } = e.target
        setFormData(prev => ({
            ...prev,
            [name]: type === 'checkbox' ? checked : value
        }))
    }

    const handleFamilyHistory = (condition) => {
        setFormData(prev => ({
            ...prev,
            family_history: {
                ...prev.family_history,
                [condition]: !prev.family_history[condition]
            }
        }))
    }

    const handleArrayToggle = (field, value) => {
        setFormData(prev => ({
            ...prev,
            [field]: prev[field].includes(value)
                ? prev[field].filter(item => item !== value)
                : [...prev[field], value]
        }))
    }

    const nextStep = () => {
        if (step < totalSteps) setStep(step + 1)
    }

    const prevStep = () => {
        if (step > 1) setStep(step - 1)
    }

    const handleSubmit = async (e) => {
        e.preventDefault()

        if (!formData.consent_given) {
            alert('Please provide consent to proceed')
            return
        }

        setLoading(true)

        try {
            // Convert string values to numbers
            const payload = {
                ...formData,
                age: parseInt(formData.age),
                height_cm: parseFloat(formData.height_cm),
                weight_kg: parseFloat(formData.weight_kg),
                sleep_hours: parseFloat(formData.sleep_hours),
                water_intake_liters: parseFloat(formData.water_intake_liters),
                stress_level: parseInt(formData.stress_level),
                blood_pressure_systolic: formData.blood_pressure_systolic ? parseInt(formData.blood_pressure_systolic) : null,
                blood_pressure_diastolic: formData.blood_pressure_diastolic ? parseInt(formData.blood_pressure_diastolic) : null
            }

            const response = await axios.post(`${API_URL}/api/assessment/submit`, payload)

            // Redirect to dashboard with assessment ID
            router.push(`/dashboard?id=${response.data.assessment_id}`)
        } catch (error) {
            console.error('Error submitting assessment:', error)
            alert('Failed to submit assessment. Please try again.')
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="container" style={{ maxWidth: '800px', padding: '2rem 1rem' }}>
            <h1 style={{ textAlign: 'center', marginBottom: '2rem' }}>Health Assessment Questionnaire</h1>

            {/* Progress Bar */}
            <div className="progress-bar">
                <div className="progress-fill" style={{ width: `${(step / totalSteps) * 100}%` }}></div>
            </div>
            <p style={{ textAlign: 'center', color: 'var(--text-secondary)', marginBottom: '2rem' }}>
                Step {step} of {totalSteps}
            </p>

            <form onSubmit={handleSubmit}>
                <div className="glass-card" style={{ padding: '2rem' }}>

                    {/* Step 1: Basic Information */}
                    {step === 1 && (
                        <div className="fade-in">
                            <h2>Basic Information</h2>

                            <div className="input-group">
                                <label>Age *</label>
                                <input
                                    type="number"
                                    name="age"
                                    value={formData.age}
                                    onChange={handleChange}
                                    required
                                    min="0"
                                    max="120"
                                    placeholder="Enter your age"
                                />
                            </div>

                            <div className="input-group">
                                <label>Gender *</label>
                                <select name="gender" value={formData.gender} onChange={handleChange} required>
                                    <option value="male">Male</option>
                                    <option value="female">Female</option>
                                    <option value="other">Other</option>
                                </select>
                            </div>

                            <div className="grid grid-2">
                                <div className="input-group">
                                    <label>Height (cm) *</label>
                                    <input
                                        type="number"
                                        name="height_cm"
                                        value={formData.height_cm}
                                        onChange={handleChange}
                                        required
                                        min="50"
                                        max="300"
                                        step="0.1"
                                        placeholder="e.g., 170"
                                    />
                                </div>

                                <div className="input-group">
                                    <label>Weight (kg) *</label>
                                    <input
                                        type="number"
                                        name="weight_kg"
                                        value={formData.weight_kg}
                                        onChange={handleChange}
                                        required
                                        min="10"
                                        max="500"
                                        step="0.1"
                                        placeholder="e.g., 70"
                                    />
                                </div>
                            </div>
                        </div>
                    )}

                    {/* Step 2: Lifestyle */}
                    {step === 2 && (
                        <div className="fade-in">
                            <h2>Lifestyle Habits</h2>

                            <div className="input-group">
                                <label>Physical Activity Level *</label>
                                <select name="activity_level" value={formData.activity_level} onChange={handleChange}>
                                    <option value="sedentary">Sedentary (little or no exercise)</option>
                                    <option value="light">Light (exercise 1-3 days/week)</option>
                                    <option value="moderate">Moderate (exercise 3-5 days/week)</option>
                                    <option value="active">Active (exercise 6-7 days/week)</option>
                                    <option value="very_active">Very Active (intense exercise daily)</option>
                                </select>
                            </div>

                            <div className="input-group">
                                <label>Average Sleep Hours per Night *</label>
                                <input
                                    type="number"
                                    name="sleep_hours"
                                    value={formData.sleep_hours}
                                    onChange={handleChange}
                                    min="0"
                                    max="24"
                                    step="0.5"
                                    placeholder="e.g., 7"
                                />
                            </div>

                            <div className="input-group">
                                <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                                    <input
                                        type="checkbox"
                                        name="smoking"
                                        checked={formData.smoking}
                                        onChange={handleChange}
                                        style={{ width: 'auto' }}
                                    />
                                    Do you smoke?
                                </label>
                            </div>

                            <div className="input-group">
                                <label>Alcohol Consumption *</label>
                                <select name="alcohol_consumption" value={formData.alcohol_consumption} onChange={handleChange}>
                                    <option value="none">None</option>
                                    <option value="occasional">Occasional (1-2 times/month)</option>
                                    <option value="moderate">Moderate (1-2 times/week)</option>
                                    <option value="heavy">Heavy (3+ times/week)</option>
                                </select>
                            </div>

                            <div className="input-group">
                                <label>Stress Level (1-10) *</label>
                                <input
                                    type="range"
                                    name="stress_level"
                                    value={formData.stress_level}
                                    onChange={handleChange}
                                    min="1"
                                    max="10"
                                    style={{ width: '100%' }}
                                />
                                <p style={{ textAlign: 'center', color: 'var(--accent-purple)', fontWeight: 'bold' }}>
                                    {formData.stress_level}
                                </p>
                            </div>
                        </div>
                    )}

                    {/* Step 3: Diet */}
                    {step === 3 && (
                        <div className="fade-in">
                            <h2>Diet & Nutrition</h2>

                            <div className="input-group">
                                <label>Diet Type *</label>
                                <select name="diet_type" value={formData.diet_type} onChange={handleChange}>
                                    <option value="balanced">Balanced</option>
                                    <option value="vegetarian">Vegetarian</option>
                                    <option value="vegan">Vegan</option>
                                    <option value="high_protein">High Protein</option>
                                    <option value="low_carb">Low Carb</option>
                                    <option value="other">Other</option>
                                </select>
                            </div>

                            <div className="input-group">
                                <label>Daily Water Intake (liters) *</label>
                                <input
                                    type="number"
                                    name="water_intake_liters"
                                    value={formData.water_intake_liters}
                                    onChange={handleChange}
                                    min="0"
                                    max="10"
                                    step="0.1"
                                    placeholder="e.g., 2"
                                />
                            </div>

                            <div className="input-group">
                                <label>Fast Food Frequency *</label>
                                <select name="fast_food_frequency" value={formData.fast_food_frequency} onChange={handleChange}>
                                    <option value="never">Never</option>
                                    <option value="rarely">Rarely (once a month)</option>
                                    <option value="monthly">Monthly (2-3 times/month)</option>
                                    <option value="weekly">Weekly (1-2 times/week)</option>
                                    <option value="daily">Daily</option>
                                </select>
                            </div>
                        </div>
                    )}

                    {/* Step 4: Medical History */}
                    {step === 4 && (
                        <div className="fade-in">
                            <h2>Medical History</h2>

                            <div className="input-group">
                                <label>Family History (select all that apply)</label>
                                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', marginTop: '0.5rem' }}>
                                    {['diabetes', 'hypertension', 'heart_disease', 'stroke', 'cancer'].map(condition => (
                                        <label key={condition} style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                                            <input
                                                type="checkbox"
                                                checked={formData.family_history[condition] || false}
                                                onChange={() => handleFamilyHistory(condition)}
                                                style={{ width: 'auto' }}
                                            />
                                            {condition.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                                        </label>
                                    ))}
                                </div>
                            </div>

                            <div className="grid grid-2">
                                <div className="input-group">
                                    <label>Blood Pressure - Systolic (optional)</label>
                                    <input
                                        type="number"
                                        name="blood_pressure_systolic"
                                        value={formData.blood_pressure_systolic}
                                        onChange={handleChange}
                                        placeholder="e.g., 120"
                                        min="60"
                                        max="250"
                                    />
                                </div>

                                <div className="input-group">
                                    <label>Blood Pressure - Diastolic (optional)</label>
                                    <input
                                        type="number"
                                        name="blood_pressure_diastolic"
                                        value={formData.blood_pressure_diastolic}
                                        onChange={handleChange}
                                        placeholder="e.g., 80"
                                        min="40"
                                        max="150"
                                    />
                                </div>
                            </div>
                        </div>
                    )}

                    {/* Step 5: Consent */}
                    {step === 5 && (
                        <div className="fade-in">
                            <h2>Consent & Language</h2>

                            <div className="input-group">
                                <label>Preferred Language for Results *</label>
                                <select name="language" value={formData.language} onChange={handleChange}>
                                    <option value="en">English</option>
                                    <option value="hi">हिंदी (Hindi)</option>
                                </select>
                            </div>

                            <div className="disclaimer">
                                <h3 style={{ color: 'var(--accent-red)', marginBottom: '1rem' }}>Important Disclaimer</h3>
                                <p><strong>This assessment is for educational and preventive purposes only.</strong></p>
                                <p>It does NOT provide medical diagnosis or treatment advice. Always consult qualified healthcare professionals for medical decisions.</p>
                                <p>By proceeding, you acknowledge that you understand this is a risk prediction tool, not a medical service.</p>
                            </div>

                            <div className="input-group">
                                <label style={{ display: 'flex', alignItems: 'flex-start', gap: '0.5rem' }}>
                                    <input
                                        type="checkbox"
                                        name="consent_given"
                                        checked={formData.consent_given}
                                        onChange={handleChange}
                                        required
                                        style={{ width: 'auto', marginTop: '0.25rem' }}
                                    />
                                    <span>I understand and consent to the processing of my health data for risk assessment purposes. I acknowledge this is not medical advice. *</span>
                                </label>
                            </div>
                        </div>
                    )}

                    {/* Navigation Buttons */}
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '2rem', gap: '1rem' }}>
                        {step > 1 && (
                            <button
                                type="button"
                                onClick={prevStep}
                                className="btn"
                                style={{ background: 'var(--bg-card)' }}
                            >
                                ← Previous
                            </button>
                        )}

                        {step < totalSteps ? (
                            <button
                                type="button"
                                onClick={nextStep}
                                className="btn btn-primary"
                                style={{ marginLeft: 'auto' }}
                            >
                                Next →
                            </button>
                        ) : (
                            <button
                                type="submit"
                                className="btn btn-success"
                                disabled={loading || !formData.consent_given}
                                style={{ marginLeft: 'auto' }}
                            >
                                {loading ? 'Analyzing...' : 'Submit Assessment →'}
                            </button>
                        )}
                    </div>
                </div>
            </form>
        </div>
    )
}
