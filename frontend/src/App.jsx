import ChatView  from './view/ChatView.jsx';
import {useAuth} from "./context/AuthContext.jsx";
import AuthView from "./view/AuthView.jsx";
import {Navigate, Route, Routes} from "react-router-dom";
import {BookingsView} from "./view/BookingsView.jsx";
import {ProtectedRoute} from "./routes/ProtectedRoute.jsx";

function App() {
  const { currentUser } = useAuth();

  return (
    <Routes>
      <Route
        path="/login"
        element={currentUser ? <Navigate to="/" replace /> : <AuthView />}
      />

      <Route
        path="/"
        element={
          <ProtectedRoute>
            <ChatView />
          </ProtectedRoute>
        }
      />

      <Route
        path="/bookings"
        element={
          <ProtectedRoute>
            <BookingsView />
          </ProtectedRoute>
        }
      />

      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}
export default App
