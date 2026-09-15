import { useState } from 'react';
import { logoutUser } from '../model/authService';

export const useLogoutViewModel = () => {
    const [isLoggingOut, setIsLoggingOut] = useState(false);
    const [error, setError] = useState(null);

    const logout = async () => {
        setIsLoggingOut(true);
        setError(null);
        try {
            await logoutUser();
        } catch (err) {
            setError('Non sono riuscito a disconnetterti. Riprova.');
        } finally {
            setIsLoggingOut(false);
        }
    };

    return { logout, isLoggingOut, error };
};