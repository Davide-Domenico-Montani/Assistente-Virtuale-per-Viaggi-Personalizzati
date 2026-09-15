export const getUserBookings = async (userId) => {
    const response = await fetch(`http://127.0.0.1:8000/api/bookings/${userId}`);

    if (!response.ok) {
        throw new Error("Errore nel recupero delle prenotazioni");
    }

    return await response.json();
};

export const deleteBooking = async (bookingId, userId) => {
    const response = await fetch(`http://127.0.0.1:8000/api/bookings/${bookingId}?user_id=${userId}`, {
        method: "DELETE"
    });

    if (!response.ok) {
        throw new Error("Errore durante l'eliminazione della prenotazione");
    }

    return await response.json();
};