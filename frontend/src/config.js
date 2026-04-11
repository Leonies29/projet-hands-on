const raw = import.meta.env.VITE_API_BASE_URL ?? ''

export const API_BASE_URL = typeof raw === 'string' ? raw.replace(/\/$/, '') : ''

export const USE_MOCK = import.meta.env.VITE_USE_MOCK === 'true'
