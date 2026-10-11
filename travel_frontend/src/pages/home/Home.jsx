import "./Home.css";

function Home() {
  return (
    <main className="home">

      {/* Hero Section */}
      <section className="hero">
        <div className="hero-content">
          <p className="hero-subtitle">
            EXPLORE THE WORLD
          </p>

          <h1>
            Your Journey,
            <br />
            Our <span>Passion.</span>
          </h1>

          <p className="hero-description">
            Discover amazing destinations, hotels, flights and travel
            experiences with Travel Hub.
          </p>

          <button className="hero-btn">
            Explore Now
          </button>
        </div>
      </section>


      {/* Search Section */}
      <section className="search-section">
        <div className="search-box">

          <div className="search-field">
            <label>Where to?</label>
            <input
              type="text"
              placeholder="Search destination"
            />
          </div>

          <div className="search-field">
            <label>Check-in</label>
            <input type="date" />
          </div>

          <div className="search-field">
            <label>Check-out</label>
            <input type="date" />
          </div>

          <div className="search-field">
            <label>Travelers</label>
            <input
              type="number"
              min="1"
              placeholder="1"
            />
          </div>

          <button className="search-btn">
            Search
          </button>

        </div>
      </section>


      {/* Popular Destinations */}
      <section className="destinations-section">

        <div className="section-heading">
          <p>DISCOVER</p>

          <h2>Popular Destinations</h2>

          <span>
            Explore some of the world's most beautiful destinations.
          </span>
        </div>


        <div className="destination-grid">

          <div className="destination-card">
            <img
              src="https://images.unsplash.com/photo-1502602898657-3e91760cbb34"
              alt="Paris"
            />

            <div className="destination-info">
              <h3>Paris</h3>
              <p>France</p>
            </div>
          </div>


          <div className="destination-card">
            <img
              src="https://images.unsplash.com/photo-1533105079780-92b9be482077"
              alt="Santorini"
            />

            <div className="destination-info">
              <h3>Santorini</h3>
              <p>Greece</p>
            </div>
          </div>


          <div className="destination-card">
            <img
              src="https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e"
              alt="Kyoto"
            />

            <div className="destination-info">
              <h3>Kyoto</h3>
              <p>Japan</p>
            </div>
          </div>


          <div className="destination-card">
            <img
              src="https://images.unsplash.com/photo-1518548419970-58e3b4079ab2"
              alt="Bali"
            />

            <div className="destination-info">
              <h3>Bali</h3>
              <p>Indonesia</p>
            </div>
          </div>

        </div>
      </section>


      {/* Popular Packages */}
      <section className="packages-section">

        <div className="section-heading">
          <p>TRAVEL WITH US</p>

          <h2>Popular Packages</h2>

          <span>
            Choose from our most popular travel experiences.
          </span>
        </div>


        <div className="package-grid">

          {/* Maldives */}
          <div className="package-card">

            <img
              src="https://images.unsplash.com/photo-1507525428034-b723cf961d3e"
              alt="Maldives"
            />

            <div className="package-info">

              <span className="package-location">
                Maldives
              </span>

              <h3>Maldives Paradise</h3>

              <p>
                Enjoy beautiful beaches, crystal-clear water and
                unforgettable experiences.
              </p>

              <div className="package-bottom">
                <strong>$899</strong>

                <button>
                  View Details
                </button>
              </div>

            </div>
          </div>


          {/* Switzerland */}
          <div className="package-card">

            <img
              src="https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1"
              alt="Switzerland"
            />

            <div className="package-info">

              <span className="package-location">
                Switzerland
              </span>

              <h3>Swiss Adventure</h3>

              <p>
                Explore breathtaking mountains, lakes and beautiful
                Swiss cities.
              </p>

              <div className="package-bottom">
                <strong>$1,299</strong>

                <button>
                  View Details
                </button>
              </div>

            </div>
          </div>


          {/* Dubai */}
          <div className="package-card">

            <img
              src="https://images.unsplash.com/photo-1530789253388-582c481c54b0"
              alt="Dubai"
            />

            <div className="package-info">

              <span className="package-location">
                Dubai
              </span>

              <h3>Dubai Experience</h3>

              <p>
                Experience luxury, adventure, shopping and
                unforgettable city views.
              </p>

              <div className="package-bottom">
                <strong>$699</strong>

                <button>
                  View Details
                </button>
              </div>

            </div>
          </div>

        </div>
      </section>


      {/* Testimonials */}
      <section className="testimonials-section">

        <div className="section-heading">
          <p>TRAVELER STORIES</p>

          <h2>What Our Travelers Say</h2>

          <span>
            Real experiences from people who traveled with Travel Hub.
          </span>
        </div>


        <div className="testimonial-grid">

          {/* Testimonial 1 */}
          <div className="testimonial-card">

            <div className="stars">
              ★★★★★
            </div>

            <p>
              "Travel Hub made planning my trip incredibly easy.
              Everything was simple and well organized."
            </p>

            <div className="traveler">

              <div className="traveler-avatar">
                A
              </div>

              <div>
                <h4>Alex Johnson</h4>
                <span>United States</span>
              </div>

            </div>

          </div>


          {/* Testimonial 2 */}
          <div className="testimonial-card">

            <div className="stars">
              ★★★★★
            </div>

            <p>
              "The hotel and destination options were excellent.
              I found exactly what I was looking for."
            </p>

            <div className="traveler">

              <div className="traveler-avatar">
                S
              </div>

              <div>
                <h4>Sarah Williams</h4>
                <span>United Kingdom</span>
              </div>

            </div>

          </div>


          {/* Testimonial 3 */}
          <div className="testimonial-card">

            <div className="stars">
              ★★★★★
            </div>

            <p>
              "Booking my vacation through Travel Hub was smooth
              and stress-free. Highly recommended!"
            </p>

            <div className="traveler">

              <div className="traveler-avatar">
                R
              </div>

              <div>
                <h4>Rahul Sharma</h4>
                <span>India</span>
              </div>

            </div>

          </div>

        </div>

      </section>

    </main>
  );
}

export default Home;