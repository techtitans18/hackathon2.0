// Utility helper functions

export const formatDate = (dateString) => {
  if (!dateString) return '-';
  return new Date(dateString).toLocaleString();
};

export const formatDateShort = (dateString) => {
  if (!dateString) return '-';
  return new Date(dateString).toLocaleDateString();
};

export const truncateHash = (hash, length = 12) => {
  if (!hash) return '-';
  return hash.substring(0, length) + '...';
};

export const getStatusBadgeColor = (status) => {
  const colors = {
    active: '#27ae60',
    inactive: '#e74c3c',
    pending: '#f39c12',
    approved: '#27ae60',
    rejected: '#e74c3c',
  };
  return colors[status] || '#3498db';
};

export const formatHealthID = (healthID) => {
  if (!healthID) return 'N/A';
  return healthID.substring(0, 8) + '...';
};

export const downloadFile = (blob, filename) => {
  const url = window.URL.createObjectURL(new Blob([blob]));
  const link = document.createElement('a');
  link.href = url;
  link.setAttribute('download', filename);
  document.body.appendChild(link);
  link.click();
  link.parentElement.removeChild(link);
  window.URL.revokeObjectURL(url);
};

export const validateEmail = (email) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

export const validatePhone = (phone) => {
  const phoneRegex = /^[\d\s\-\+\(\)]{7,}$/;
  return phoneRegex.test(phone);
};

export const validateDate = (dateString) => {
  const date = new Date(dateString);
  return date instanceof Date && !isNaN(date);
};

export const getBloodGroupList = () => [
  'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'
];

export const getRecordTypeOptions = () => [
  'X-Ray',
  'Blood Test',
  'ECG',
  'MRI',
  'CT Scan',
  'Ultrasound',
  'Lab Report',
  'Prescription',
  'Clinical Notes',
  'Other'
];

export const calculateAge = (dob) => {
  if (!dob) return null;
  const today = new Date();
  const birthDate = new Date(dob);
  let age = today.getFullYear() - birthDate.getFullYear();
  const monthDiff = today.getMonth() - birthDate.getMonth();
  if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
    age--;
  }
  return age;
};

export const isValidDOB = (dob) => {
  const age = calculateAge(dob);
  return age && age >= 0 && age <= 150;
};

export const getRoleDisplayName = (role) => {
  const roleNames = {
    admin: 'Administrator',
    hospital: 'Hospital',
    patient: 'Patient',
    doctor: 'Doctor',
  };
  return roleNames[role] || role;
};

export const getInitials = (name) => {
  if (!name) return '?';
  return name
    .split(' ')
    .map((n) => n[0])
    .join('')
    .toUpperCase()
    .substring(0, 2);
};
