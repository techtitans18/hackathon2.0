import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000';

const patientAccessAPI = {
  sendOTP: async (searchType, searchValue) => {
    const token = localStorage.getItem('access_token');
    return axios.post(
      `${API_BASE_URL}/patient_access/send_otp`,
      {
        search_type: searchType,
        search_value: searchValue
      },
      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    );
  },

  verifyOTP: async (searchType, searchValue, otp) => {
    const token = localStorage.getItem('access_token');
    return axios.post(
      `${API_BASE_URL}/patient_access/verify_otp`,
      {
        search_type: searchType,
        search_value: searchValue,
        otp: otp
      },
      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    );
  }
};

export default patientAccessAPI;
