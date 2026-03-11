import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

const API = 'http://localhost:8000'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || null)
  const user = ref(null)
  const profile = ref(null)
  const loading = ref(false)
  const error = ref(null)

  const isAuthenticated = computed(() => !!token.value)

  function setToken(t) {
    token.value = t
    if (t) localStorage.setItem('token', t)
    else localStorage.removeItem('token')
  }

  function authHeaders() {
    return {
      'Content-Type': 'application/json',
      Authorization: `Token ${token.value}`,
    }
  }

  async function login(username, password) {
    loading.value = true
    error.value = null
    try {
      const res = await fetch(`${API}/auth/token/login/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
      })
      const data = await res.json()
      if (!res.ok) throw new Error(data.non_field_errors?.[0] || 'Неверные данные')
      setToken(data.auth_token)
      await fetchProfile()
      return true
    } catch (e) {
      error.value = e.message
      return false
    } finally {
      loading.value = false
    }
  }

  async function register(username, email, password) {
    loading.value = true
    error.value = null
    try {
      const res = await fetch(`${API}/auth/users/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, email, password, re_password: password }),
      })
      const data = await res.json()
      if (!res.ok) {
        const msg = Object.values(data).flat().join(' ')
        throw new Error(msg)
      }
      // Auto-login after register
      return await login(username, password)
    } catch (e) {
      error.value = e.message
      return false
    } finally {
      loading.value = false
    }
  }

  async function logout() {
    try {
      await fetch(`${API}/auth/token/logout/`, {
        method: 'POST',
        headers: authHeaders(),
      })
    } catch {}
    setToken(null)
    user.value = null
    profile.value = null
  }

  async function fetchProfile() {
    try {
      const [userRes, profileRes] = await Promise.all([
        fetch(`${API}/auth/users/me/`, { headers: authHeaders() }),
        fetch(`${API}/api/profiles/me/`, { headers: authHeaders() }),
      ])
      if (userRes.ok) user.value = await userRes.json()
      if (profileRes.ok) profile.value = await profileRes.json()
    } catch {}
  }

  async function updateProfile(data) {
    loading.value = true
    error.value = null
    try {
      const res = await fetch(`${API}/api/profiles/me/`, {
        method: 'PATCH',
        headers: authHeaders(),
        body: JSON.stringify(data),
      })
      const updated = await res.json()
      if (!res.ok) throw new Error(Object.values(updated).flat().join(' '))
      profile.value = updated
      return true
    } catch (e) {
      error.value = e.message
      return false
    } finally {
      loading.value = false
    }
  }

  // Init: load profile if token exists
  if (token.value) {
    fetchProfile()
  }

  return {
    token, user, profile, loading, error,
    isAuthenticated,
    login, register, logout, fetchProfile, updateProfile,
  }
})