import { useState } from 'react';
import { recordAPI, aiAPI } from '../services/api';

export default function UploadRecord({ hospitalId, onRecordUploaded }) {
  const [formData, setFormData] = useState({
    HealthID: '',
    HospitalID: hospitalId,
    record_type: '',
    description: '',
  });
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [uploadProgress, setUploadProgress] = useState(0);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setSuccess(null);
    setUploadProgress(0);

    if (!file) {
      setError('Please select a file');
      setLoading(false);
      return;
    }

    try {
      const multipartFormData = new FormData();
      multipartFormData.append('HealthID', formData.HealthID);
      multipartFormData.append('HospitalID', formData.HospitalID);
      multipartFormData.append('record_type', formData.record_type);
      multipartFormData.append('description', formData.description);
      multipartFormData.append('file', file);

      setUploadProgress(30);

      const response = await recordAPI.addRecord(multipartFormData);

      setUploadProgress(100);
      let successMsg = `Record uploaded successfully! Record ID: ${response.data.record_id}`;
      if (response.data.summary_file_name) {
        successMsg += `\nAI Summary: ${response.data.summary_file_name}`;
      }
      setSuccess(successMsg);

      setFormData({
        HealthID: '',
        HospitalID: hospitalId,
        record_type: '',
        description: '',
      });
      setFile(null);
      onRecordUploaded();
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to upload record');
      console.error('Error:', err);
    } finally {
      setLoading(false);
      setTimeout(() => setUploadProgress(0), 1000);
    }
  };

  return (
    <div className="upload-container">
      <h3>Upload Medical Record</h3>
      {error && <div className="error-message">{error}</div>}
      {success && <div className="success-message">{success}</div>}

      <form onSubmit={handleSubmit} className="upload-form">
        <div className="form-group">
          <label>Patient Health ID *</label>
          <input
            type="text"
            name="HealthID"
            value={formData.HealthID}
            onChange={handleInputChange}
            required
            placeholder="Patient's Health ID"
          />
        </div>

        <div className="form-group">
          <label>Record Type *</label>
          <input
            type="text"
            name="record_type"
            value={formData.record_type}
            onChange={handleInputChange}
            required
            placeholder="e.g., X-Ray, Blood Test, ECG"
          />
        </div>

        <div className="form-group">
          <label>Description *</label>
          <textarea
            name="description"
            value={formData.description}
            onChange={handleInputChange}
            required
            placeholder="Clinical notes and findings"
            rows="4"
          />
        </div>

        <div className="form-group">
          <label>Upload File *</label>
          <input
            type="file"
            onChange={handleFileChange}
            required
            accept=".pdf,.doc,.docx,.txt,.jpg,.png"
          />
          {file && <p className="file-selected">Selected: {file.name}</p>}
        </div>

        {uploadProgress > 0 && uploadProgress < 100 && (
          <div className="progress-bar">
            <div className="progress-fill" style={{ width: `${uploadProgress}%` }} />
          </div>
        )}

        <button type="submit" disabled={loading} className="btn-primary">
          {loading ? `Uploading... ${uploadProgress}%` : 'Upload Record'}
        </button>
      </form>
    </div>
  );
}
