import { useState } from "react";
import { useAuth } from "../auth/AuthContext";

export default function Login() {
  const { requestLink } = useAuth();
  const [email, setEmail] = useState("");
  const [sent, setSent] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    try {
      await requestLink(email);
      setSent(true);
    } catch {
      setError("Something went wrong. Try again.");
    }
  };

  const gallery = (
    <div className="login-gallery">
      <div className="login-gallery-item">
        <img src="/images/nfl.webp" alt="NFL running back breaking a tackle" />
      </div>
      <div className="login-gallery-item">
        <img src="/images/wnba.webp" alt="WNBA guard driving past a defender" />
      </div>
      <div className="login-gallery-item">
        <img src="/images/tennis.webp" alt="Tennis player stretching for a backhand" />
      </div>
      <div className="login-gallery-item">
        <img src="/images/rugby.webp" alt="Rugby scrum" />
      </div>
    </div>
  );

  if (sent) {
    return (
      <div className="login-page">
        <div className="centered-card">
          <h1>Check your email</h1>
          <p>If {email} is a league member, a login link is on its way.</p>
        </div>
        {gallery}
      </div>
    );
  }

  return (
    <div className="login-page">
      <div className="centered-card">
        <h1 className="wordmark login-wordmark">
          <span className="mega">Mega</span>Fantasy
        </h1>
        <form onSubmit={submit}>
          <input
            type="email"
            required
            placeholder="you@example.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <button type="submit" className="btn-primary">
            Send login link
          </button>
        </form>
        {error && <p className="error">{error}</p>}
      </div>
      {gallery}
    </div>
  );
}
