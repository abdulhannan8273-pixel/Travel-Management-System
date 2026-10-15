import { Link } from "react-router-dom";
import "./Navbar.css";

function Navbar() {
  return (
    <nav className="navbar">
      <div className="navbar-logo">
        Travel<span>Hub</span>
      </div>

      <ul className="navbar-links">
        <li><Link to="/">Home</Link></li>
        <li><Link to="/destinations">Destinations</Link></li>
        <li><Link to="/packages">Packages</Link></li>
        <li><Link to="/hotels">Hotels</Link></li>
        <li><Link to="/flights">Flights</Link></li>
      </ul>

      <div className="navbar-actions">
        <Link to="/login">
          <button className="login-btn">Login</button>
        </Link>

      <Link to="/register">
        <button className="signup-btn">Sign Up</button>
      </Link>
      </div>
    </nav>
  );
}

export default Navbar;