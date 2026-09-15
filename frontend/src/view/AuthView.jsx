import { useAuthViewModel } from '../viewModel/useAuthViewModel';
import './AuthView.css';

const AuthView = () => {
    const {
        isRegister,
        email, setEmail,
        password, setPassword,
        confirmPassword, setConfirmPassword,
        error, isSubmitting,
        switchMode, submit
    } = useAuthViewModel();

    const handleSubmit = (e) => {
        e.preventDefault();
        submit();
    };

    return (
        <div className="auth-view">
            <div className="auth-card">
                <div className="auth-card__header">
                    <span className="auth-card__dot" aria-hidden="true" />
                    <h1 className="auth-card__title">
                        {isRegister ? 'Crea un account' : 'Accedi'}
                    </h1>
                </div>

                <form className="auth-form" onSubmit={handleSubmit}>
                    <label className="auth-field">
                        <span>Email</span>
                        <input
                            type="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            placeholder="nome@esempio.com"
                            autoComplete="email"
                            required
                        />
                    </label>

                    <label className="auth-field">
                        <span>Password</span>
                        <input
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            placeholder="••••••••"
                            autoComplete={isRegister ? 'new-password' : 'current-password'}
                            minLength={6}
                            required
                        />
                    </label>

                    {isRegister && (
                        <label className="auth-field">
                            <span>Conferma password</span>
                            <input
                                type="password"
                                value={confirmPassword}
                                onChange={(e) => setConfirmPassword(e.target.value)}
                                placeholder="••••••••"
                                autoComplete="new-password"
                                minLength={6}
                                required
                            />
                        </label>
                    )}

                    {error && <p className="auth-error">{error}</p>}

                    <button type="submit" className="auth-submit" disabled={isSubmitting}>
                        {isSubmitting ? 'Attendere...' : isRegister ? 'Registrati' : 'Accedi'}
                    </button>
                </form>

                <p className="auth-switch">
                    {isRegister ? 'Hai già un account?' : 'Non hai un account?'}{' '}
                    <button type="button" className="auth-switch__btn" onClick={switchMode}>
                        {isRegister ? 'Accedi' : 'Registrati'}
                    </button>
                </p>
            </div>
        </div>
    );
};

export default AuthView;