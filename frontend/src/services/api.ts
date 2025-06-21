import axios, { AxiosInstance, AxiosResponse, AxiosError } from 'axios'
import { useAuthStore } from '@/stores/authStore'

const baseURL = import.meta.env.VITE_API_URL || 'http://localhost:5000'

const api: AxiosInstance = axios.create({
  baseURL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor
api.interceptors.request.use(
  (config) => {
    const token = useAuthStore.getState().token
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error: AxiosError) => {
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  (response: AxiosResponse) => response,
  async (error: AxiosError) => {
    if (error.response?.status === 401) {
      useAuthStore.getState().logout()
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export interface LoginCredentials {
  email: string
  password: string
}

export interface RegisterData extends LoginCredentials {
  firstName: string
  lastName: string
}

export interface Grant {
  id: number
  name: string
  funder: string
  sourceUrl?: string
  dueDate?: string
  amountString?: string
  description?: string
  status: string
  eligibilityAnalysis?: Record<string, any>
  createdAt: string
  updatedAt: string
}

export const authAPI = {
  login: (credentials: LoginCredentials) =>
    api.post('/api/auth/login', credentials),
  register: (data: RegisterData) =>
    api.post('/api/auth/register', data),
  logout: () =>
    api.post('/api/auth/logout'),
  getCurrentUser: () =>
    api.get('/api/auth/me'),
}

export const grantsAPI = {
  getGrants: (params?: Record<string, any>) =>
    api.get('/api/grants', { params }),
  getGrant: (id: number) =>
    api.get(`/api/grants/${id}`),
  createGrant: (data: Partial<Grant>) =>
    api.post('/api/grants', data),
  updateGrant: (id: number, data: Partial<Grant>) =>
    api.put(`/api/grants/${id}`, data),
  deleteGrant: (id: number) =>
    api.delete(`/api/grants/${id}`),
  analyzeEligibility: (id: number) =>
    api.post(`/api/grants/${id}/analyze-eligibility`),
  generateDraft: (id: number) =>
    api.post(`/api/grants/${id}/generate-draft`),
}

export default api 