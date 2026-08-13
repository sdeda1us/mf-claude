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

  if (sent) {
    return (
      <div className="centered-card">
        <h1>Check your email</h1>
        <p>If {email} is a league member, a login link is on its way.</p>
      </div>
    );
  }

  return (
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
  );
}
