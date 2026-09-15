import { useEffect, useState } from 'react';
import { useAuth } from '../context/AuthContext';
import {deleteBooking, getUserBookings} from '../model/bookingService';

export const useBookingsViewModel = () => {
    const { currentUser } = useAuth();
    const [bookings, setBookings] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [deletingId, setDeletingId] = useState(null);


    useEffect(() => {
        if (!currentUser) {
            setLoading(false);
            return;
        }

        setLoading(true);
        setError(null);

        getUserBookings(currentUser.uid)
            .then((data) => {
                setBookings(data.bookings);
            })
            .catch((err) => {
                setError(err.message);
            })
            .finally(() => {
                setLoading(false);
            });
    }, [currentUser]);

    const handleDelete = async (bookingId) => {
        const isConfirmed = window.confirm("Sei sicuro di voler annullare questo viaggio? L'azione è irreversibile.");
        if (!isConfirmed) return;

        setDeletingId(bookingId);
        try {
            await deleteBooking(bookingId, currentUser.uid);
            setBookings((prev) => prev.filter((b) => b.id !== bookingId));
        } catch (err) {
            alert(err.message);
        } finally {
            setDeletingId(null);
        }
    };

    return { bookings, loading, error, deletingId, handleDelete  };
};