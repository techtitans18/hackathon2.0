import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor to attach Authorization header
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Handle response errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Only redirect if user was previously authenticated (token exists)
      const hadToken = localStorage.getItem('access_token');
      localStorage.removeItem('access_token');
      localStorage.removeItem('user');
      
      // Only redirect if user was logged in before (not on initial session check)
      if (hadToken) {
        window.location.href = '/';
      }
    }
    return Promise.reject(error);
  }
);

export const authAPI = {
  getConfig: () => api.get('/auth/google/config'),
  googleLogin: (credential) =>
    api.post('/auth/google', { credential }),
  getSession: () => api.get('/auth/session'),
  logout: () => api.post('/auth/logout'),
};

export const adminAPI = {
  listUsers: () => api.get('/admin/users'),
  upsertUser: (userData) => api.post('/admin/users', userData),
};

export const hospitalAPI = {
  registerHospital: (data) =>
    api.post('/register_hospital', data),
  listHospitals: () =>
    api.get('/hospitals'),
  updateHospital: (hospital_id, data) =>
    api.put(`/hospitals/${hospital_id}`, data),
  getBlockchain: () => api.get('/blockchain'),
};

export const patientAPI = {
  registerPatient: (data) =>
    api.post('/register_patient', data),
  getProfile: () => api.get('/patient/me'),
  getEHealthCard: () => api.get('/patient/me/e-healthcard'),
  getPatientByID: (healthID) =>
    api.get(`/patient/${healthID}`),
};

export const recordAPI = {
  addRecord: (formData) =>
    api.post('/add_record', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    }),
  downloadFile: (fileName) =>
    api.get(`/record/file/${fileName}`, {
      responseType: 'blob',
    }),
  downloadSummary: (fileName) =>
    api.get(`/record/summary/${fileName}`, {
      responseType: 'text',
    }),
  getRecordByHash: (hash) =>
    api.get(`/record/hash/${hash}`),
};

export const aiAPI = {
  getHealth: () => api.get('/ai/health'),
  generateSummary: (data) =>
    api.post('/ai/summary', data),
};

export const emergencyAPI = {
  searchPatient: (data) =>
    api.post('/emergency/search', data),
  getProfile: (data) =>
    api.post('/emergency/profile', data),
  upsertData: (data) =>
    api.post('/emergency/upsert', data),
};

export default api;
