import { create } from 'zustand'
import { jwtDecode } from 'jwt-decode'

interface User {
  id: number
  email: string
  firstName: string
  lastName: string
  roles: string[]
}

interface AuthState {
  token: string | null
  user: User | null
  isAuthenticated: boolean
  setAuth: (token: string) => void
  logout: () => void
  updateUser: (user: Partial<User>) => void
}

export const useAuthStore = create<AuthState>((set) => ({
  token: localStorage.getItem('token'),
  user: null,
  isAuthenticated: false,

  setAuth: (token: string) => {
    localStorage.setItem('token', token)
    const decoded = jwtDecode<{ user: User }>(token)
    set({
      token,
      user: decoded.user,
      isAuthenticated: true,
    })
  },

  logout: () => {
    localStorage.removeItem('token')
    set({
      token: null,
      user: null,
      isAuthenticated: false,
    })
  },

  updateUser: (userData: Partial<User>) => {
    set((state) => ({
      user: state.user ? { ...state.user, ...userData } : null,
    }))
  },
})) 