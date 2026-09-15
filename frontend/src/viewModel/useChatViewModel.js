import { useState } from 'react';
import { sendChatMessage } from '../model/chatService';
import { useAuth } from '../context/AuthContext'; // <-- Importa il context

export const useChatViewModel = () => {
    const [messages, setMessages] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);

    const { currentUser } = useAuth();

    const sendMessage = async (text) => {
        if (!text.trim()) return;

        const newUserMsg = { role: "user", content: text };
        const currentHistory = [...messages];

        setMessages((prev) => [...prev, newUserMsg]);
        setIsLoading(true);
        setError(null);

        try {
            const uid = currentUser ? currentUser.uid : "guest";

            const response = await sendChatMessage(text, currentHistory, uid);

            const newAiMsg = { role: "assistant", content: response.reply };
            setMessages((prev) => [...prev, newAiMsg]);
        } catch (err) {
            setError(err.message);
        } finally {
            setIsLoading(false);
        }
    };

    return { messages, isLoading, error, sendMessage };
};