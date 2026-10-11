import "./Footer.css";

function Footer() {
  return (
    <footer className="footer">

      <div className="footer-container">

        {/* Brand */}
        <div className="footer-column footer-brand">
          <h2>Travel Hub</h2>

          <p>
            Discover amazing destinations, hotels, flights and
            unforgettable travel experiences.
          </p>
        </div>


        {/* Quick Links */}
        <div className="footer-column">
          <h3>Quick Links</h3>

          <ul>
            <li><a href="/">Home</a></li>
            <li><a href="/destinations">Destinations</a></li>
            <li><a href="/packages">Packages</a></li>
            <li><a href="/hotels">Hotels</a></li>
            <li><a href="/flights">Flights</a></li>
          </ul>
        </div>


        {/* Support */}
        <div className="footer-column">
          <h3>Support</h3>

          <ul>
            <li><a href="/about">About Us</a></li>
            <li><a href="/contact">Contact Us</a></li>
            <li><a href="/reviews">Reviews</a></li>
            <li><a href="/faq">FAQ</a></li>
          </ul>
        </div>


        {/* Contact */}
        <div className="footer-column">
          <h3>Contact</h3>

          <p>Email: support@travelhub.com</p>
          <p>Phone: +91 98765 43210</p>
          <p>India</p>
        </div>

      </div>


      <div className="footer-bottom">
        <p>
          © 2026 Travel Hub. All rights reserved.
        </p>
      </div>

    </footer>
  );
}

export default Footer;