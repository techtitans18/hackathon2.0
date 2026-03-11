import { useState } from 'react';
import { patientAPI } from '../services/api';

export default function PatientRegistration({ hospitalId }) {
  const [formData, setFormData] = useState({
    name: '',
    age: '',
    phone: '',
    email: '',
    dob: '',
    blood_group: 'O+',
    photo_url: '',
    emergency_contact: '',
    allergies: [],
    diseases: [],
    surgeries: [],
  });
  const [photoFile, setPhotoFile] = useState(null);
  const [photoPreview, setPhotoPreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleListInputChange = (e, field) => {
    const { value } = e.target;
    const items = value.split(',').map((item) => item.trim()).filter((item) => item);
    setFormData({
      ...formData,
      [field]: items,
    });
  };

  const handlePhotoChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      if (file.size > 2 * 1024 * 1024) {
        setError('Photo size must be less than 2MB');
        return;
      }
      if (!file.type.startsWith('image/')) {
        setError('Please upload an image file');
        return;
      }
      
      // Compress and resize image
      const reader = new FileReader();
      reader.onload = (event) => {
        const img = new Image();
        img.onload = () => {
          // Create canvas for resizing
          const canvas = document.createElement('canvas');
          const ctx = canvas.getContext('2d');
          
          // Resize to max 200x200 to keep base64 small
          const maxSize = 200;
          let width = img.width;
          let height = img.height;
          
          if (width > height) {
            if (width > maxSize) {
              height = (height * maxSize) / width;
              width = maxSize;
            }
          } else {
            if (height > maxSize) {
              width = (width * maxSize) / height;
              height = maxSize;
            }
          }
          
          canvas.width = width;
          canvas.height = height;
          ctx.drawImage(img, 0, 0, width, height);
          
          // Convert to base64 with compression (0.7 quality)
          const compressedBase64 = canvas.toDataURL('image/jpeg', 0.7);
          
          // Check if still too large (base64 should be < 1000 chars for backend)
          // If too large, use empty string
          if (compressedBase64.length > 1000) {
            setPhotoPreview(compressedBase64);
            setFormData({ ...formData, photo_url: '' }); // Don't send to backend
            setError('Photo compressed but still too large. Proceeding without photo.');
          } else {
            setPhotoPreview(compressedBase64);
            setFormData({ ...formData, photo_url: compressedBase64 });
            setError(null);
          }
        };
        img.src = event.target.result;
      };
      reader.readAsDataURL(file);
      setPhotoFile(file);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setSuccess(null);

    try {
      const response = await patientAPI.registerPatient(formData);
      setSuccess(`Patient registered successfully. Health ID: ${response.data.HealthID}`);
      setFormData({
        name: '',
        age: '',
        phone: '',
        email: '',
        dob: '',
        blood_group: 'O+',
        photo_url: '',
        emergency_contact: '',
        allergies: [],
        diseases: [],
        surgeries: [],
      });
      setPhotoFile(null);
      setPhotoPreview(null);
    } catch (err) {
      // Handle validation errors from backend
      if (err.response?.data?.detail) {
        const detail = err.response.data.detail;
        // Check if detail is an array of validation errors
        if (Array.isArray(detail)) {
          const errorMessages = detail.map(e => `${e.loc?.join('.')}: ${e.msg}`).join(', ');
          setError(errorMessages);
        } else if (typeof detail === 'string') {
          setError(detail);
        } else {
          setError('Failed to register patient');
        }
      } else {
        setError('Failed to register patient');
      }
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="registration-container">
      <h3>Register Patient</h3>
      {error && <div className="error-message">{error}</div>}
      {success && <div className="success-message">{success}</div>}

      <form onSubmit={handleSubmit} className="registration-form">
        <div className="form-row">
          <div className="form-group">
            <label>Name *</label>
            <input
              type="text"
              name="name"
              value={formData.name}
              onChange={handleInputChange}
              required
              placeholder="Full name"
            />
          </div>

          <div className="form-group">
            <label>Age *</label>
            <input
              type="number"
              name="age"
              value={formData.age}
              onChange={handleInputChange}
              required
              min="0"
              max="150"
            />
          </div>

          <div className="form-group">
            <label>Blood Group *</label>
            <select
              name="blood_group"
              value={formData.blood_group}
              onChange={handleInputChange}
              required
            >
              <option>A+</option>
              <option>A-</option>
              <option>B+</option>
              <option>B-</option>
              <option>AB+</option>
              <option>AB-</option>
              <option>O+</option>
              <option>O-</option>
            </select>
          </div>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label>Phone *</label>
            <input
              type="tel"
              name="phone"
              value={formData.phone}
              onChange={handleInputChange}
              required
              placeholder="Phone number"
            />
          </div>

          <div className="form-group">
            <label>Email *</label>
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleInputChange}
              required
              placeholder="Email address"
            />
          </div>

          <div className="form-group">
            <label>Date of Birth *</label>
            <input
              type="date"
              name="dob"
              value={formData.dob}
              onChange={handleInputChange}
              required
            />
          </div>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label>Photo</label>
            <input
              type="file"
              accept="image/*"
              onChange={handlePhotoChange}
            />
            {photoPreview && (
              <div className="photo-preview">
                <img src={photoPreview} alt="Preview" />
              </div>
            )}
          </div>

          <div className="form-group">
            <label>Emergency Contact</label>
            <input
              type="tel"
              name="emergency_contact"
              value={formData.emergency_contact}
              onChange={handleInputChange}
              placeholder="Emergency contact phone"
            />
          </div>
        </div>

        <div className="form-group">
          <label>Allergies (comma-separated)</label>
          <textarea
            value={formData.allergies.join(', ')}
            onChange={(e) => handleListInputChange(e, 'allergies')}
            placeholder="e.g., Penicillin, Peanuts, Shellfish"
          />
        </div>

        <div className="form-group">
          <label>Diseases (comma-separated)</label>
          <textarea
            value={formData.diseases.join(', ')}
            onChange={(e) => handleListInputChange(e, 'diseases')}
            placeholder="e.g., Diabetes, Hypertension"
          />
        </div>

        <div className="form-group">
          <label>Surgeries (comma-separated)</label>
          <textarea
            value={formData.surgeries.join(', ')}
            onChange={(e) => handleListInputChange(e, 'surgeries')}
            placeholder="e.g., Appendix, Heart Surgery"
          />
        </div>

        <button type="submit" disabled={loading} className="btn-primary">
          {loading ? 'Registering...' : 'Register Patient'}
        </button>
      </form>
    </div>
  );
}
