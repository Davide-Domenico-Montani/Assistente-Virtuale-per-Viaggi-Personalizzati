import { useEffect, useRef, useState } from 'react';
import { useChatViewModel } from '../viewModel/useChatViewModel';
import { useLogoutViewModel } from '../viewModel/useLogoutViewModel';
import './ChatView.css';
import {Link} from "react-router-dom";
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

const ChatView = () => {
    const { messages, isLoading, error, sendMessage } = useChatViewModel();
    const { logout, isLoggingOut } = useLogoutViewModel();
    const [input, setInput] = useState('');
    const scrollRef = useRef(null);
    const textareaRef = useRef(null);

    useEffect(() => {
        scrollRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages, isLoading]);

    const handleSubmit = (e) => {
        e.preventDefault();
        if (!input.trim() || isLoading) return;
        sendMessage(input);
        setInput('');
        if (textareaRef.current) textareaRef.current.style.height = 'auto';
    };

    const handleKeyDown = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSubmit(e);
        }
    };

    const handleInputChange = (e) => {
        setInput(e.target.value);
        const el = textareaRef.current;
        if (el) {
            el.style.height = 'auto';
            el.style.height = `${Math.min(el.scrollHeight, 160)}px`;
        }
    };

    return (
        <div className="chat-view">
            <header className="chat-header">
                <div className="chat-header__brand">
                    <span className="chat-header__dot" aria-hidden="true" />
                    <h1 className="chat-header__title">Assistente per viaggi</h1>
                </div>
                <div className="chat-header__actions">
                    <Link to="/bookings" className="chat-header__link">I miei viaggi</Link>
                    <button className="chat-header__logout" onClick={logout} disabled={isLoggingOut}>
                        {isLoggingOut ? 'Uscita...' : 'Esci'}
                    </button>
                </div>
            </header>

            <div className="chat-log">
                {messages.length === 0 && !isLoading && (
                    <div className="chat-empty">
                        <p>Scrivi un messaggio per iniziare la conversazione.</p>
                    </div>
                )}

                {messages.map((msg, i) => (
                    <div key={i} className={`chat-row chat-row--${msg.role}`}>
                        <div className="chat-bubble">
                            <ReactMarkdown remarkPlugins={[remarkGfm]}>
                                {msg.content}
                            </ReactMarkdown>

                        </div>
                    </div>
                ))}

                {isLoading && (
                    <div className="chat-row chat-row--assistant">
                        <div className="chat-bubble chat-bubble--pending">
                            <span className="typing">
                                <span />
                                <span />
                                <span />
                            </span>
                        </div>
                    </div>
                )}

                {error && (
                    <div className="chat-row chat-row--error">
                        <div className="chat-bubble chat-bubble--error">
                            Non sono riuscito a rispondere: {error}
                        </div>
                    </div>
                )}

                <div ref={scrollRef} />
            </div>

            <form className="chat-composer" onSubmit={handleSubmit}>
                <textarea
                    ref={textareaRef}
                    className="chat-composer__input"
                    placeholder="Scrivi un messaggio..."
                    value={input}
                    onChange={handleInputChange}
                    onKeyDown={handleKeyDown}
                    rows={1}
                    disabled={isLoading}
                />
                <button
                    type="submit"
                    className="chat-composer__send"
                    disabled={isLoading || !input.trim()}
                    aria-label="Invia messaggio"
                >
                    <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" strokeWidth="2">
                        <path d="M4 12h15M13 6l6 6-6 6" strokeLinecap="round" strokeLinejoin="round" />
                    </svg>
                </button>
            </form>
        </div>
    );
};

export default ChatView;