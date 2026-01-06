import axios from 'axios'

// Determine API base URL based on environment
const getApiBaseUrl = () => {
  // In development, use relative paths (proxied through Vite)
  if (import.meta.env.DEV) {
    return ''
  }
  
  // In production, use the backend URL from environment or default
  const backendUrl = import.meta.env.VITE_API_BASE_URL || 'https://vulnerable-notes-backend.onrender.com'
  return backendUrl
}

// Create axios instance with proper configuration
const apiClient = axios.create({
  baseURL: getApiBaseUrl(),
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Add request interceptor for debugging
apiClient.interceptors.request.use(
  config => {
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.baseURL}${config.url}`)
    return config
  },
  error => Promise.reject(error)
)

// Add response interceptor for error handling
apiClient.interceptors.response.use(
  response => response,
  error => {
    console.error('API Error:', error.response?.status, error.message)
    return Promise.reject(error)
  }
)

export default apiClient
