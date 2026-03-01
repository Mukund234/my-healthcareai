'use client';

import { useState, useEffect, useRef } from 'react';
import { useRouter } from 'next/navigation';

export default function ChatPage() {
    const [messages, setMessages] = useState([]);
    const [inputValue, setInputValue] = useState('');
    const [conversationId, setConversationId] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [quickReplies, setQuickReplies] = useState(null);
    const [isComplete, setIsComplete] = useState(false);
    const [sidebarOpen, setSidebarOpen] = useState(true);
    const [isCyberMode, setIsCyberMode] = useState(true);
    const [conversations, setConversations] = useState([
        { id: 1, title: 'Health Assessment - Today', date: 'Today' },
        { id: 2, title: 'Previous Assessment', date: 'Yesterday' },
    ]);
    const messagesEndRef = useRef(null);
    const router = useRouter();

    const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    useEffect(() => {
        startConversation();
    }, []);

    const startConversation = async () => {
        setIsLoading(true);
        try {
            const response = await fetch(`${API_URL}/api/conversation/start`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ user_id: 'anonymous' })
            });

            const data = await response.json();
            setConversationId(data.conversation_id);
            setMessages([{ role: 'assistant', content: data.message }]);
            setQuickReplies(data.quick_replies);
        } catch (error) {
            console.error('Error starting conversation:', error);
            setMessages([{
                role: 'assistant',
                content: 'Unable to connect to the server. Please try again later.'
            }]);
        } finally {
            setIsLoading(false);
        }
    };

    const sendMessage = async (message) => {
        if (!message.trim() || !conversationId || isLoading) return;

        const userMessage = { role: 'user', content: message };
        setMessages(prev => [...prev, userMessage]);
        setInputValue('');
        setQuickReplies(null);
        setIsLoading(true);

        try {
            const response = await fetch(`${API_URL}/api/conversation/message`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    conversation_id: conversationId,
                    message: message
                })
            });

            const data = await response.json();
            setMessages(prev => [...prev, {
                role: 'assistant',
                content: data.message,
                isDiagnostic: data.action === 'analyze'
            }]);

            setQuickReplies(data.quick_replies);
            if (data.action === 'analyze') {
                setIsComplete(true);
            }
        } catch (error) {
            console.error('Error sending message:', error);
            setMessages(prev => [...prev, {
                role: 'assistant',
                content: 'Sorry, there was an error processing your message. Please try again.'
            }]);
        } finally {
            setIsLoading(false);
        }
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        sendMessage(inputValue);
    };

    const renderAssistantMessage = (content, isDiagnostic) => {
        if (!isDiagnostic) return <p className="whitespace-pre-wrap text-base leading-relaxed">{content}</p>;

        const parts = content.split('\n\n');
        return (
            <div className="space-y-4">
                {parts.map((part, i) => {
                    if (part.toLowerCase().includes('assessment')) {
                        return (
                            <div key={i} className="diagnostic-block assessment-block">
                                <div className="diagnostic-header">
                                    <span className="text-lg">🔍</span> Possible Assessment
                                </div>
                                <div className="diagnostic-content">{part.replace(/assessment/i, '').trim()}</div>
                            </div>
                        );
                    }
                    if (part.toLowerCase().includes('next steps') || part.toLowerCase().includes('recommendation')) {
                        return (
                            <div key={i} className="diagnostic-block steps-block">
                                <div className="diagnostic-header">
                                    <span className="text-lg">📋</span> Suggested Next Steps
                                </div>
                                <div className="diagnostic-content">{part.replace(/next steps|recommendation/i, '').trim()}</div>
                            </div>
                        );
                    }
                    if (part.toLowerCase().includes('disclaimer')) {
                        return (
                            <div key={i} className="diagnostic-block disclaimer-block">
                                <div className="diagnostic-header">
                                    <span className="text-lg">⚠️</span> Medical Disclaimer
                                </div>
                                <div className="diagnostic-content">{part.replace(/disclaimer/i, '').trim()}</div>
                            </div>
                        );
                    }
                    return <p key={i} className="whitespace-pre-wrap text-base leading-relaxed">{part}</p>;
                })}
            </div>
        );
    };

    return (
        <div className={`min-h-screen ${isCyberMode ? 'bg-bg-primary' : 'bg-white text-black'} flex transition-colors duration-500`}>
            {/* Sidebar / Command Center */}
            <aside className={`${sidebarOpen ? 'w-72' : 'w-0'} bg-bg-elevated border-r border-border-subtle transition-all duration-300 overflow-hidden flex flex-col relative z-20`}>
                <div className="p-6 border-b border-border-subtle">
                    <div className="flex items-center gap-2 mb-6">
                        <div className="w-8 h-8 rounded-lg bg-cyber-cyan shadow-cyber flex items-center justify-center text-bg-primary font-bold">A</div>
                        <h2 className="text-xl font-bold tracking-tight text-white">AROGYA <span className="text-cyber-cyan">AI</span></h2>
                    </div>
                    <button
                        onClick={() => { startConversation(); setMessages([]); setIsComplete(false); }}
                        className="btn-primary w-full py-3 rounded-lg text-sm flex items-center justify-center gap-2"
                    >
                        <span>+</span> New Consultation
                    </button>
                </div>

                <div className="flex-1 overflow-y-auto p-4 space-y-6">
                    <div>
                        <p className="text-[10px] text-text-tertiary mb-3 px-2 font-bold uppercase tracking-[0.2em]">Medical Records</p>
                        {conversations.map((conv) => (
                            <button key={conv.id} className="sidebar-item w-full text-left mb-1 group">
                                <p className="text-sm text-text-primary group-hover:text-cyber-cyan transition-colors truncate">{conv.title}</p>
                                <p className="text-[10px] text-text-tertiary">{conv.date}</p>
                            </button>
                        ))}
                    </div>

                    <div>
                        <p className="text-[10px] text-text-tertiary mb-3 px-2 font-bold uppercase tracking-[0.2em]">Emergency</p>
                        <button className="btn-emergency w-full py-3 rounded-lg text-xs flex items-center justify-center gap-2 mb-2">
                            <span>🚑</span> Ambulance (102)
                        </button>
                        <button className="w-full py-2 text-xs text-text-secondary hover:text-white transition-colors border border-dashed border-border-subtle rounded-lg">
                            💊 Order Medicines
                        </button>
                    </div>
                </div>

                <div className="p-6 border-t border-border-subtle space-y-4">
                    <div 
                        className={`cyber-toggle ${isCyberMode ? 'active' : ''}`}
                        onClick={() => setIsCyberMode(!isCyberMode)}
                    >
                        <div className="toggle-track">
                            <div className="toggle-thumb"></div>
                        </div>
                        <span className="text-xs font-bold text-text-secondary uppercase tracking-widest">
                            {isCyberMode ? 'Cyber Mode' : 'Light Mode'}
                        </span>
                    </div>
                    <button onClick={() => router.push('/dashboard')} className="w-full py-2 text-xs text-text-secondary hover:text-cyber-cyan transition-colors text-left font-bold uppercase tracking-widest px-2">
                        Admin Dashboard
                    </button>
                </div>
            </aside>

            {/* Main Content */}
            <div className="flex-1 flex flex-col relative overflow-hidden">
                {/* Header */}
                <header className="bg-bg-elevated/50 backdrop-blur-xl border-b border-border-subtle sticky top-0 z-10">
                    <div className="mx-auto px-6 py-4 flex items-center justify-between">
                        <div className="flex items-center gap-4">
                            <button onClick={() => setSidebarOpen(!sidebarOpen)} className="text-text-secondary hover:text-cyber-cyan transition-colors">
                                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                                </svg>
                            </button>
                            <div className="trust-badge">
                                <div className="trust-badge-icon"></div>
                                <span>INDIA'S TRUSTED MEDICAL AI</span>
                            </div>
                        </div>
                        <div className="px-3 py-1 bg-cyber-red/10 border border-cyber-red/20 rounded-md">
                            <span className="text-[10px] font-bold text-cyber-red uppercase tracking-tighter pulse">● LIVE DIAGNOSTIC ENGINE</span>
                        </div>
                    </div>
                </header>

                {/* Chat Area */}
                <main className="flex-1 overflow-y-auto chat-container relative">
                    <div className="max-w-4xl mx-auto px-6 py-12 space-y-8 relative z-10">
                        {messages.map((message, index) => (
                            <div key={index} className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'} animate-fade-in`}>
                                <div className={`message-bubble max-w-[85%] rounded-xl px-6 py-5 ${
                                    message.role === 'user' 
                                    ? 'bg-gradient-cyber text-bg-primary font-medium' 
                                    : 'bg-bg-elevated/80 border border-border-subtle text-text-primary backdrop-blur-md'
                                }`}>
                                    {message.role === 'assistant' 
                                        ? renderAssistantMessage(message.content, message.isDiagnostic)
                                        : <p className="text-base leading-relaxed">{message.content}</p>
                                    }
                                </div>
                            </div>
                        ))}
                        {isLoading && (
                            <div className="flex justify-start">
                                <div className="typing-indicator bg-bg-elevated/80 border border-border-subtle">
                                    <div className="typing-dot bg-cyber-cyan"></div>
                                    <div className="typing-dot bg-cyber-cyan opacity-60"></div>
                                    <div className="typing-dot bg-cyber-cyan opacity-30"></div>
                                </div>
                            </div>
                        )}
                        <div ref={messagesEndRef} />
                    </div>
                </main>

                {/* Quick Tools & Input */}
                <div className="border-t border-border-subtle bg-bg-secondary/80 backdrop-blur-xl p-6">
                    <div className="max-w-4xl mx-auto space-y-4">
                        {!isComplete && (
                            <>
                                {/* Quick Tools */}
                                <div className="flex gap-2 pb-2 overflow-x-auto no-scrollbar">
                                    <button className="quick-reply-btn whitespace-nowrap">🤒 Symptoms</button>
                                    <button className="quick-reply-btn whitespace-nowrap">📂 Upload Reports</button>
                                    <button className="quick-reply-btn whitespace-nowrap">🎙️ Voice Input</button>
                                </div>

                                {quickReplies && (
                                    <div className="flex flex-wrap gap-2 py-2">
                                        {quickReplies.map((reply, index) => (
                                            <button key={index} onClick={() => sendMessage(reply)} className="quick-reply-btn border-cyber-cyan/30 text-cyber-cyan hover:bg-cyber-cyan/10">
                                                {reply}
                                            </button>
                                        ))}
                                    </div>
                                )}

                                <form onSubmit={handleSubmit} className="flex gap-3">
                                    <input
                                        type="text"
                                        value={inputValue}
                                        onChange={(e) => setInputValue(e.target.value)}
                                        placeholder="Describe your health concern..."
                                        disabled={isLoading}
                                        className="input-enhanced flex-1 border-border-subtle focus:border-cyber-cyan/50"
                                    />
                                    <button
                                        type="submit"
                                        disabled={isLoading || !inputValue.trim()}
                                        className="btn-primary px-8 rounded-lg"
                                    >
                                        TRANSMIT
                                    </button>
                                </form>
                            </>
                        )}

                        {isComplete && (
                            <div className="text-center py-4">
                                <p className="text-text-secondary mb-4 italic">Diagnostic assessment complete. Review findings above.</p>
                                <button onClick={() => router.push('/')} className="btn-primary px-10 py-3 rounded-xl">
                                    RETURN TO COMMAND CENTER
                                </button>
                            </div>
                        )}
                        <p className="text-[10px] text-text-tertiary text-center uppercase tracking-widest opacity-50">
                            Powered by Arogya AI Engine | WHO Protocol Version 4.2.1
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
}
