import { Link } from 'react-router-dom';
import { useBookingsViewModel } from '../viewModel/useBookingViewModel';
import './BookingsView.css';

export const BookingsView = () => {
    const { bookings, loading, error, deletingId, handleDelete } = useBookingsViewModel();

    return (
        <div className="bookings-view">
            <header className="bookings-header">
                <h1 className="bookings-header__title">I Tuoi Viaggi 🌍</h1>
                <Link to="/" className="bookings-header__back">
                    ← Torna alla Chat
                </Link>
            </header>

            <div className="bookings-content">
                {loading && (
                    <p className="bookings-status">Caricamento prenotazioni in corso...</p>
                )}

                {error && (
                    <p className="bookings-status bookings-status--error">⚠️ {error}</p>
                )}

                {!loading && !error && bookings.length === 0 && (
                    <div className="bookings-empty">
                        <p className="bookings-empty__title">Nessun viaggio prenotato</p>
                        <p className="bookings-empty__text">
                            Torna nella chat e chiedi all'assistente di organizzare la tua prossima avventura!
                        </p>
                    </div>
                )}

                {!loading && !error && bookings.length > 0 && (
                    <div className="bookings-list">
                        {bookings.map((booking) => (
                            <div className="booking-card" key={booking.id}>
                                <div className="booking-card__body">
                                    <h2 className="booking-card__destination">
                                        Destinazione: {booking.destination}
                                    </h2>
                                    <p className="booking-card__details">{booking.details}</p>
                                </div>
                                <button
                                    className="booking-card__delete"
                                    onClick={() => handleDelete(booking.id)}
                                    disabled={deletingId === booking.id}
                                    aria-label="Annulla prenotazione"
                                    title="Annulla prenotazione"
                                >
                                    {deletingId === booking.id ? (
                                        <span className="booking-card__spinner" />
                                    ) : (
                                        <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" strokeWidth="1.8">
                                            <path d="M4 7h16" strokeLinecap="round" />
                                            <path d="M9 7V4.5a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1V7" strokeLinecap="round" strokeLinejoin="round" />
                                            <path d="M6 7l1 12.5a1.5 1.5 0 0 0 1.5 1.5h7a1.5 1.5 0 0 0 1.5-1.5L18 7" strokeLinecap="round" strokeLinejoin="round" />
                                            <path d="M10 11v6M14 11v6" strokeLinecap="round" />
                                        </svg>
                                    )}
                                </button>
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
};