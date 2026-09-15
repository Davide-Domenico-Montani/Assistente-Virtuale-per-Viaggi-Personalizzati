import { useState } from 'react';
import { loginUser, registerUser } from '../model/authService';

const ERROR_MESSAGES = {
    'auth/invalid-email': 'L\'indirizzo email non è valido.',
    'auth/user-disabled': 'Questo account è stato disabilitato.',
    'auth/user-not-found': 'Email o password non corretti.',
    'auth/wrong-password': 'Email o password non corretti.',
    'auth/invalid-credential': 'Email o password non corretti.',
    'auth/email-already-in-use': 'Esiste già un account con questa email.',
    'auth/weak-password': 'La password deve avere almeno 6 caratteri.',
};

const getErrorMessage = (err) => ERROR_MESSAGES[err.code] || 'Qualcosa è andato storto. Riprova.';

export const useAuthViewModel = () => {
    const [mode, setMode] = useState('login'); // 'login' | 'register'
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [error, setError] = useState(null);
    const [isSubmitting, setIsSubmitting] = useState(false);

    const isRegister = mode === 'register';

    const switchMode = () => {
        setMode(isRegister ? 'login' : 'register');
        setError(null);
        setPassword('');
        setConfirmPassword('');
    };

    const submit = async () => {
        setError(null);

        if (isRegister && password !== confirmPassword) {
            setError('Le password non coincidono.');
            return;
        }

        setIsSubmitting(true);
        try {
            if (isRegister) {
                await registerUser(email, password);
            } else {
                await loginUser(email, password);
            }
        } catch (err) {
            setError(getErrorMessage(err));
        } finally {
            setIsSubmitting(false);
        }
    };

    return {
        isRegister,
        email,
        setEmail,
        password,
        setPassword,
        confirmPassword,
        setConfirmPassword,
        error,
        isSubmitting,
        switchMode,
        submit
    };
};