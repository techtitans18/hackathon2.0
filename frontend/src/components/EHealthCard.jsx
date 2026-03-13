import { useState, useEffect } from 'react';
import QRCode from 'qrcode';
import '../styles/ehealth-card.css';

function EHealthCard({ patient }) {
  const [qrCodeUrl, setQrCodeUrl] = useState('');

  useEffect(() => {
    if (patient?.health_id) {
      generateQRCode(patient.health_id);
    }
  }, [patient]);

  const generateQRCode = async (healthId) => {
    try {
      const qrData = JSON.stringify({
        health_id: healthId,
        name: patient.name,
        blood_group: patient.blood_group,
        phone: patient.phone,
      });
      const url = await QRCode.toDataURL(qrData, {
        width: 80,
        margin: 0,
        color: {
          dark: '#000000',
          light: '#FFFFFF',
        },
      });
      setQrCodeUrl(url);
    } catch (err) {
      console.error('QR Code generation failed:', err);
    }
  };

  const getBloodGroupClass = (bloodGroup) => {
    if (!bloodGroup) return '';
    const bg = bloodGroup.toLowerCase().replace(/\+/g, '-positive').replace(/-/g, '-negative');
    return bg;
  };

  const downloadCard = () => {
    const card = document.querySelector('.ehealth-card-container');
    if (!card) return;

    // Use html2canvas for better quality
    import('html2canvas').then((html2canvas) => {
      html2canvas.default(card, {
        scale: 2,
        backgroundColor: '#ffffff',
      }).then((canvas) => {
        const link = document.createElement('a');
        link.download = `ehealth-card-${patient.health_id}.png`;
        link.href = canvas.toDataURL('image/png');
        link.click();
      });
    }).catch(() => {
      alert('Download feature requires html2canvas library. Install: npm install html2canvas');
    });
  };

  const printCard = () => {
    window.print();
  };

  if (!patient) {
    return <div className="ehealth-card-loading">Loading e-Health Card...</div>;
  }

  return (
    <div className="ehealth-card-wrapper">
      <div className="ehealth-card-actions">
        <button className="card-action-btn download-btn" onClick={downloadCard}>
          <svg width="20" height="20" fill="currentColor" viewBox="0 0 16 16">
            <path d="M.5 9.9a.5.5 0 0 1 .5.5v2.5a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-2.5a.5.5 0 0 1 1 0v2.5a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2v-2.5a.5.5 0 0 1 .5-.5z"/>
            <path d="M7.646 11.854a.5.5 0 0 0 .708 0l3-3a.5.5 0 0 0-.708-.708L8.5 10.293V1.5a.5.5 0 0 0-1 0v8.793L5.354 8.146a.5.5 0 1 0-.708.708l3 3z"/>
          </svg>
          Download Card
        </button>
        <button className="card-action-btn print-btn" onClick={printCard}>
          <svg width="20" height="20" fill="currentColor" viewBox="0 0 16 16">
            <path d="M2.5 8a.5.5 0 1 0 0-1 .5.5 0 0 0 0 1z"/>
            <path d="M5 1a2 2 0 0 0-2 2v2H2a2 2 0 0 0-2 2v3a2 2 0 0 0 2 2h1v1a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2v-1h1a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-1V3a2 2 0 0 0-2-2H5zM4 3a1 1 0 0 1 1-1h6a1 1 0 0 1 1 1v2H4V3zm1 5a2 2 0 0 0-2 2v1H2a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h12a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1h-1v-1a2 2 0 0 0-2-2H5zm7 2v3a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1v-3a1 1 0 0 1 1-1h6a1 1 0 0 1 1 1z"/>
          </svg>
          Print Card
        </button>
      </div>

      <div className="ehealth-card-container">
        {/* Card Header */}
        <div className="ehealth-card-header">
          <div className="header-logo">
            <div className="logo-emblem">🏥</div>
            <div className="header-text">
              <h3>Government of Healthcare</h3>
              <h2>e-Health Card</h2>
            </div>
          </div>
          <div className="header-flag">
            <div className="flag-stripe orange"></div>
            <div className="flag-stripe white"></div>
            <div className="flag-stripe green"></div>
          </div>
        </div>

        {/* Card Body */}
        <div className="ehealth-card-body">
          {/* Left Section - Patient Details */}
          <div className="card-left-section">
            <div className="detail-row">
              <span className="detail-label">Name</span>
              <span className="detail-value">{patient.name || 'N/A'}</span>
            </div>
            <div className="detail-row">
              <span className="detail-label">Health ID</span>
              <span className="detail-value health-id">{patient.health_id || 'N/A'}</span>
            </div>
            <div className="detail-row">
              <span className="detail-label">Blood Group</span>
              <span className={`detail-value blood-group ${getBloodGroupClass(patient.blood_group)}`}>
                {patient.blood_group || 'N/A'}
              </span>
            </div>
            <div className="detail-row">
              <span className="detail-label">Phone</span>
              <span className="detail-value">{patient.phone || 'N/A'}</span>
            </div>
            <div className="detail-row">
              <span className="detail-label">Date of Birth</span>
              <span className="detail-value">{patient.dob || 'N/A'}</span>
            </div>
          </div>

          {/* Right Section - Photo and QR */}
          <div className="card-right-section">
            <div className="patient-photo">
              {patient.photo_url ? (
                <img src={patient.photo_url} alt={patient.name} />
              ) : (
                <div className="photo-placeholder">
                  <svg width="30" height="30" fill="currentColor" viewBox="0 0 16 16">
                    <path d="M11 6a3 3 0 1 1-6 0 3 3 0 0 1 6 0z"/>
                    <path d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8zm8-7a7 7 0 0 0-5.468 11.37C3.242 11.226 4.805 10 8 10s4.757 1.225 5.468 2.37A7 7 0 0 0 8 1z"/>
                  </svg>
                </div>
              )}
            </div>
            <div className="qr-code-section">
              {qrCodeUrl ? (
                <img src={qrCodeUrl} alt="QR Code" className="qr-code" />
              ) : (
                <div className="qr-placeholder">QR</div>
              )}
            </div>
          </div>
        </div>

        {/* Card Footer */}
        <div className="ehealth-card-footer">
          <div className="footer-left">
            <p className="footer-note">This is a digitally generated e-Health Card</p>
          </div>
          <div className="footer-right">
            <div className="hologram">
              <div className="hologram-shine"></div>
              <span>SECURE</span>
            </div>
          </div>
        </div>

        {/* Decorative Elements */}
        <div className="card-pattern card-pattern-top"></div>
        <div className="card-pattern card-pattern-bottom"></div>
      </div>

      {/* Card Back Side (for print) */}
      <div className="ehealth-card-back print-only">
        <div className="back-header">
          <h3>Important Information</h3>
        </div>
        <div className="back-content">
          <div className="back-section">
            <h4>Emergency Contact</h4>
            <p>{patient.emergency_contact || patient.phone || 'N/A'}</p>
          </div>
          <div className="back-section">
            <h4>Address</h4>
            <p>{patient.address || 'Not provided'}</p>
          </div>
          <div className="back-section">
            <h4>Medical Alerts</h4>
            <ul>
              {patient.allergies && patient.allergies.length > 0 ? (
                patient.allergies.map((allergy, idx) => (
                  <li key={idx}>Allergy: {allergy}</li>
                ))
              ) : (
                <li>No known allergies</li>
              )}
            </ul>
          </div>
          <div className="back-footer">
            <p>For medical emergencies, scan QR code or contact: 108</p>
            <p className="helpline">Healthcare Helpline: 1800-XXX-XXXX</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default EHealthCard;
