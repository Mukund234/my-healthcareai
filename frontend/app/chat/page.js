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
    const [conversations, setConversations] = useState([
        { id: 1, title: 'Health Assessment - Today', date: 'Today' },
        { id: 2, title: 'Previous Assessment', date: 'Yesterday' },
    ]);
    const messagesEndRef = useRef(null);
    const router = useRouter();

    const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

    // Auto-scroll to bottom
    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    // Start conversation on mount
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

        // Add user message
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

            // Add AI response
            setMessages(prev => [...prev, {
                role: 'assistant',
                content: data.message
            }]);

            setQuickReplies(data.quick_replies);

            // Check if conversation is complete
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

    const handleQuickReply = (reply) => {
        sendMessage(reply);
    };

    return (
        <div className="min-h-screen bg-bg-primary flex">
            {/* Sidebar */}
            <aside className={`${sidebarOpen ? 'w-64' : 'w-0'} bg-bg-elevated border-r border-border-subtle transition-all duration-300 overflow-hidden flex flex-col`}>
                <div className="p-4 border-b border-border-subtle">
                    <button
                        onClick={() => {
                            startConversation();
                            setMessages([]);
                        }}
                        className="btn-gradient w-full px-4 py-3 rounded-lg font-semibold text-sm"
                    >
                        ✨ New Chat
                    </button>
                </div>

                <div className="flex-1 overflow-y-auto p-3">
                    <p className="text-xs text-text-tertiary mb-3 px-2 font-medium uppercase tracking-wider">Recent Conversations</p>
                    {conversations.map((conv) => (
                        <button
                            key={conv.id}
                            className="sidebar-item w-full text-left mb-1"
                        >
                            <p className="text-sm text-text-primary truncate font-medium">{conv.title}</p>
                            <p className="text-xs text-text-tertiary mt-0.5">{conv.date}</p>
                        </button>
                    ))}
                </div>

                <div className="p-4 border-t border-border-subtle">
                    <button
                        onClick={() => router.push('/dashboard')}
                        className="w-full px-4 py-2 text-sm text-text-secondary hover:text-text-primary hover:bg-bg-tertiary rounded-lg transition-all"
                    >
                        Dashboard
                    </button>
                </div>
            </aside>

            {/* Main Content */}
            <div className="flex-1 flex flex-col">
                {/* Header */}
                <header className="bg-bg-elevated border-b border-border-subtle">
                    <div className="container mx-auto px-4 py-4 flex items-center justify-between">
                        <div className="flex items-center gap-3">
                            <button
                                onClick={() => setSidebarOpen(!sidebarOpen)}
                                className="text-text-secondary hover:text-text-primary transition-colors"
                            >
                                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                                </svg>
                            </button>
                            <div>
                                <h1 className="text-lg font-semibold text-text-primary">Health Assessment</h1>
                                <p className="text-sm text-text-secondary">WHO-Aligned Risk Analysis</p>
                            </div>
                        </div>
                        <button
                            onClick={() => router.push('/')}
                            className="text-text-secondary hover:text-text-primary transition-colors text-sm"
                        >
                            Close
                        </button>
                    </div>
                </header>

                {/* Chat Messages */}
                <main className="flex-1 overflow-y-auto chat-container">
                    <div className="container mx-auto px-4 py-6 max-w-4xl relative z-10">
                        <div className="space-y-6">
                            {messages.map((message, index) => (
                                <div
                                    key={index}
                                    className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                                >
                                    {/* Message Bubble */}
                                    <div
                                        className={`message-bubble max-w-[80%] rounded-2xl px-6 py-4 ${message.role === 'user'
                                            ? 'message-user text-white'
                                            : 'message-assistant text-text-primary'
                                            }`}
                                    >
                                        <p className="whitespace-pre-wrap text-base leading-relaxed">
                                            {message.content}
                                        </p>
                                    </div>
                                </div>
                            ))}

                            {isLoading && (
                                <div className="flex justify-start">
                                    <div className="typing-indicator">
                                        <div className="typing-dot"></div>
                                        <div className="typing-dot"></div>
                                        <div className="typing-dot"></div>
                                    </div>
                                </div>
                            )}

                            <div ref={messagesEndRef} />
                        </div>
                    </div>
                </main>

                {/* Quick Replies */}
                {quickReplies && !isLoading && (
                    <div className="border-t border-border-subtle bg-bg-secondary">
                        <div className="container mx-auto px-4 py-4 max-w-4xl">
                            <p className="text-xs text-text-tertiary mb-3 font-medium">Suggested responses:</p>
                            <div className="flex flex-wrap gap-2">
                                {quickReplies.map((reply, index) => (
                                    <button
                                        key={index}
                                        onClick={() => handleQuickReply(reply)}
                                        className="quick-reply-btn"
                                    >
                                        {reply}
                                    </button>
                                ))}
                            </div>
                        </div>
                    </div>
                )}

                {/* Input Area */}
                {!isComplete && (
                    <div className="border-t border-border-subtle bg-bg-secondary">
                        <div className="container mx-auto px-4 py-5 max-w-4xl">
                            <form onSubmit={handleSubmit} className="flex gap-3">
                                <input
                                    type="text"
                                    value={inputValue}
                                    onChange={(e) => setInputValue(e.target.value)}
                                    placeholder="Type your message..."
                                    disabled={isLoading}
                                    className="input-enhanced flex-1 disabled:opacity-50 disabled:cursor-not-allowed"
                                />
                                <button
                                    type="submit"
                                    disabled={isLoading || !inputValue.trim()}
                                    className="btn-gradient px-8 py-4 rounded-lg font-semibold disabled:opacity-50 disabled:cursor-not-allowed text-base"
                                >
                                    Send
                                </button>
                            </form>
                            <p className="text-xs text-text-tertiary mt-3 text-center">
                                💡 This assessment is based on WHO guidelines and is not a substitute for professional medical advice.
                            </p>
                        </div>
                    </div>
                )}

                {/* Completion Message */}
                {isComplete && (
                    <div className="border-t border-border-subtle bg-bg-secondary">
                        <div className="container mx-auto px-4 py-6 max-w-4xl text-center">
                            <p className="text-text-secondary mb-4">Assessment complete. Your results have been saved.</p>
                            <button
                                onClick={() => router.push('/')}
                                className="px-6 py-3 bg-accent-primary text-white rounded-lg font-medium hover:bg-accent-primary-hover transition-all"
                            >
                                Return to Home
                            </button>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}
