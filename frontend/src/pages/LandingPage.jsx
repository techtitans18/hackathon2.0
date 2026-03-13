import { useNavigate } from 'react-router-dom';
import LandingNavbar from '../components/LandingNavbar';
import '../styles/landing.css';

function LandingPage() {
  const navigate = useNavigate();

  const handleSignIn = () => {
    navigate('/login');
  };

  return (
    <div className="landing-page">
      {/* Navbar */}
      <LandingNavbar />
      
      {/* Hero Section */}
      <section className="hero-section">
        <div className="hero-overlay"></div>
        <div className="hero-content">
          <div className="hero-text">
            <h1 className="hero-title">
              Secure Healthcare Records
              <span className="hero-subtitle">Powered by Blockchain</span>
            </h1>
            <p className="hero-description">
              A revolutionary healthcare management system that ensures data integrity, 
              cross-hospital access, and AI-powered medical summaries.
            </p>
            <div className="hero-buttons">
              <button className="btn-primary" onClick={handleSignIn}>
                <svg className="btn-icon" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12.545,10.239v3.821h5.445c-0.712,2.315-2.647,3.972-5.445,3.972c-3.332,0-6.033-2.701-6.033-6.032s2.701-6.032,6.033-6.032c1.498,0,2.866,0.549,3.921,1.453l2.814-2.814C17.503,2.988,15.139,2,12.545,2C7.021,2,2.543,6.477,2.543,12s4.478,10,10.002,10c8.396,0,10.249-7.85,9.426-11.748L12.545,10.239z"/>
                </svg>
                Sign In with Google
              </button>
              <button className="btn-secondary" onClick={() => document.getElementById('features').scrollIntoView({ behavior: 'smooth' })}>
                Learn More
              </button>
            </div>
          </div>
          <div className="hero-image">
            <div className="floating-card card-1">
              <div className="card-icon">🏥</div>
              <div className="card-text">Cross-Hospital Access</div>
            </div>
            <div className="floating-card card-2">
              <div className="card-icon">🔒</div>
              <div className="card-text">Blockchain Security</div>
            </div>
            <div className="floating-card card-3">
              <div className="card-icon">🤖</div>
              <div className="card-text">AI Summaries</div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="features-section">
        <div className="container">
          <h2 className="section-title">Powerful Features</h2>
          <p className="section-subtitle">Everything you need for modern healthcare management</p>
          
          <div className="features-grid">
            <div className="feature-card">
              <div className="feature-icon blockchain-icon">⛓️</div>
              <h3>Blockchain Integrity</h3>
              <p>Immutable record-keeping with SHA-256 hashing ensures data cannot be tampered with.</p>
            </div>

            <div className="feature-card">
              <div className="feature-icon ai-icon">🤖</div>
              <h3>AI Summarization</h3>
              <p>Automatic medical report summaries using BART model running completely offline.</p>
            </div>

            <div className="feature-card">
              <div className="feature-icon hospital-icon">🏥</div>
              <h3>Cross-Hospital Access</h3>
              <p>Any hospital can access patient records via OTP verification for better care coordination.</p>
            </div>

            <div className="feature-card">
              <div className="feature-icon emergency-icon">🚨</div>
              <h3>Emergency Access</h3>
              <p>Quick patient lookup with critical information display for emergency situations.</p>
            </div>

            <div className="feature-card">
              <div className="feature-icon security-icon">🔐</div>
              <h3>Role-Based Security</h3>
              <p>Admin, hospital, and patient roles with granular permissions and access control.</p>
            </div>

            <div className="feature-card">
              <div className="feature-icon otp-icon">📧</div>
              <h3>OTP Verification</h3>
              <p>Secure patient access with email OTP verification for privacy protection.</p>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section id="how-it-works" className="how-it-works-section">
        <div className="container">
          <h2 className="section-title">How It Works</h2>
          <p className="section-subtitle">Simple and secure healthcare record management</p>
          
          <div className="steps-container">
            <div className="step">
              <div className="step-number">1</div>
              <div className="step-content">
                <h3>Sign In</h3>
                <p>Use your Google account to securely sign in to the platform.</p>
              </div>
            </div>

            <div className="step-connector"></div>

            <div className="step">
              <div className="step-number">2</div>
              <div className="step-content">
                <h3>Register Patients</h3>
                <p>Hospitals register patients with deterministic Health IDs for consistency.</p>
              </div>
            </div>

            <div className="step-connector"></div>

            <div className="step">
              <div className="step-number">3</div>
              <div className="step-content">
                <h3>Upload Records</h3>
                <p>Upload medical reports with automatic AI summarization and blockchain verification.</p>
              </div>
            </div>

            <div className="step-connector"></div>

            <div className="step">
              <div className="step-number">4</div>
              <div className="step-content">
                <h3>Access Anywhere</h3>
                <p>Patients and authorized hospitals can access records securely from anywhere.</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section id="stats" className="stats-section">
        <div className="container">
          <div className="stats-grid">
            <div className="stat-card">
              <div className="stat-number">100%</div>
              <div className="stat-label">Blockchain Secured</div>
            </div>
            <div className="stat-card">
              <div className="stat-number">24/7</div>
              <div className="stat-label">Access Availability</div>
            </div>
            <div className="stat-card">
              <div className="stat-number">AI</div>
              <div className="stat-label">Powered Summaries</div>
            </div>
            <div className="stat-card">
              <div className="stat-number">∞</div>
              <div className="stat-label">Cross-Hospital Access</div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="cta-section">
        <div className="container">
          <h2 className="cta-title">Ready to Get Started?</h2>
          <p className="cta-description">
            Join the future of healthcare record management with blockchain security and AI intelligence.
          </p>
          <button className="btn-cta" onClick={handleSignIn}>
            <svg className="btn-icon" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12.545,10.239v3.821h5.445c-0.712,2.315-2.647,3.972-5.445,3.972c-3.332,0-6.033-2.701-6.033-6.032s2.701-6.032,6.033-6.032c1.498,0,2.866,0.549,3.921,1.453l2.814-2.814C17.503,2.988,15.139,2,12.545,2C7.021,2,2.543,6.477,2.543,12s4.478,10,10.002,10c8.396,0,10.249-7.85,9.426-11.748L12.545,10.239z"/>
            </svg>
            Sign In Now
          </button>
        </div>
      </section>

      {/* Footer */}
      <footer className="footer">
        <div className="container">
          <div className="footer-content">
            <div className="footer-section">
              <h3>Healthcare Blockchain</h3>
              <p>Secure, transparent, and intelligent healthcare record management.</p>
            </div>
            <div className="footer-section">
              <h4>Features</h4>
              <ul>
                <li>Blockchain Security</li>
                <li>AI Summarization</li>
                <li>Cross-Hospital Access</li>
                <li>Emergency Access</li>
              </ul>
            </div>
            <div className="footer-section">
              <h4>Technology</h4>
              <ul>
                <li>FastAPI Backend</li>
                <li>MongoDB Database</li>
                <li>React Frontend</li>
                <li>BART AI Model</li>
              </ul>
            </div>
            <div className="footer-section">
              <h4>Security</h4>
              <ul>
                <li>Google OAuth</li>
                <li>JWT Tokens</li>
                <li>OTP Verification</li>
                <li>SHA-256 Hashing</li>
              </ul>
            </div>
          </div>
          <div className="footer-bottom">
            <p>&copy; 2024 Healthcare Blockchain. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default LandingPage;
