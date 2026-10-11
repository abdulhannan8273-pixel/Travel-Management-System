import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import "./Register.css";

function Register() {
  const navigate = useNavigate();

  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [password, setPassword] = useState("");

  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [loading, setLoading] = useState(false);

  const handleRegister = async (event) => {
    event.preventDefault();

    setError("");
    setSuccess("");
    setLoading(true);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/api/accounts/register/",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            username,
            email,
            phone,
            password,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        console.log("REGISTER ERROR:", data);

        let errorMessage = "Registration failed.";

        if (data.errors) {
          errorMessage = Object.entries(data.errors)
            .map(([field, messages]) => {
              return `${field}: ${messages.join(" ")}`;
            })
            .join(" ");
        } else if (data.message) {
          errorMessage = data.message;
        } else if (data.detail) {
          errorMessage = data.detail;
        }

        setError(errorMessage);

        return;
      }

      setSuccess(
        "Account created successfully! Please verify your email before logging in."
      );

      setUsername("");
      setEmail("");
      setPhone("");
      setPassword("");

      setTimeout(() => {
        navigate("/login");
      }, 3000);
    } catch (error) {
      console.error("REGISTER CONNECTION ERROR:", error);

      setError(
        "Unable to connect to the server. Please make sure Django is running."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="register-page">
      <div className="register-card">

        <div className="register-header">
          <h1>Create Account</h1>

          <p>
            Join Travel Hub and start planning your next journey.
          </p>
        </div>

        <form
          className="register-form"
          onSubmit={handleRegister}
        >

          <div className="form-group">
            <label htmlFor="username">
              Username
            </label>

            <input
              id="username"
              type="text"
              placeholder="Enter your username"
              value={username}
              onChange={(event) =>
                setUsername(event.target.value)
              }
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="email">
              Email Address
            </label>

            <input
              id="email"
              type="email"
              placeholder="Enter your email"
              value={email}
              onChange={(event) =>
                setEmail(event.target.value)
              }
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="phone">
              Phone Number
            </label>

            <input
              id="phone"
              type="tel"
              placeholder="Enter 10-digit mobile number"
              value={phone}
              onChange={(event) =>
                setPhone(event.target.value)
              }
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">
              Password
            </label>

            <input
              id="password"
              type="password"
              placeholder="Create a password"
              value={password}
              onChange={(event) =>
                setPassword(event.target.value)
              }
              required
            />
          </div>

          {error && (
            <p className="form-error">
              {error}
            </p>
          )}

          {success && (
            <p className="form-success">
              {success}
            </p>
          )}

          <button
            type="submit"
            className="register-btn"
            disabled={loading}
          >
            {loading
              ? "Creating Account..."
              : "Create Account"}
          </button>

        </form>

        <div className="login-link">
          <p>
            Already have an account?{" "}
            <Link to="/login">
              Login
            </Link>
          </p>
        </div>

      </div>
    </main>
  );
}

export default Register;