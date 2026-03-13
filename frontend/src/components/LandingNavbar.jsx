import { useNavigate } from 'react-router-dom';
import '../styles/landing-navbar.css';

function LandingNavbar() {
  const navigate = useNavigate();

  const scrollToSection = (sectionId) => {
    const element = document.getElementById(sectionId);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <nav className="landing-navbar">
      <div className="landing-navbar-container">
        {/* Logo */}
        <div className="landing-navbar-logo" onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}>
          <div className="logo-icon">🏥</div>
          <span className="logo-text">Healthcare Blockchain</span>
        </div>

        {/* Navigation Links */}
        <div className="landing-navbar-links">
          <button className="nav-link" onClick={() => scrollToSection('features')}>
            Features
          </button>
          <button className="nav-link" onClick={() => scrollToSection('how-it-works')}>
            How It Works
          </button>
          <button className="nav-link" onClick={() => scrollToSection('stats')}>
            Stats
          </button>
        </div>

        {/* Sign In Button */}
        <div className="landing-navbar-actions">
          <button className="nav-signin-btn" onClick={() => navigate('/login')}>
            <svg className="signin-icon" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12.545,10.239v3.821h5.445c-0.712,2.315-2.647,3.972-5.445,3.972c-3.332,0-6.033-2.701-6.033-6.032s2.701-6.032,6.033-6.032c1.498,0,2.866,0.549,3.921,1.453l2.814-2.814C17.503,2.988,15.139,2,12.545,2C7.021,2,2.543,6.477,2.543,12s4.478,10,10.002,10c8.396,0,10.249-7.85,9.426-11.748L12.545,10.239z"/>
            </svg>
            Sign In
          </button>
        </div>

        {/* Mobile Menu Toggle */}
        <button className="mobile-menu-toggle" onClick={() => {
          document.querySelector('.landing-navbar-links').classList.toggle('active');
          document.querySelector('.landing-navbar-actions').classList.toggle('active');
        }}>
          <span></span>
          <span></span>
          <span></span>
        </button>
      </div>
    </nav>
  );
}

export default LandingNavbar;
