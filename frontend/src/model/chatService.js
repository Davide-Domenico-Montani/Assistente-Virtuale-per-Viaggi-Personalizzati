export const sendChatMessage = async (userMessage, chatHistory, userId) => {
    const payload = {
        message: userMessage,
        history: chatHistory,
        user_id: userId
    };

    const response = await fetch("http://127.0.0.1:8000/api/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(payload)
    });

    if (!response.ok) {
        throw new Error("Errore di comunicazione con il server AI");
    }

    return await response.json();
};