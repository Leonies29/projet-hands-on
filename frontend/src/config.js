/**
 * Base URL pour les appels API.
 * - Si VITE_API_BASE_URL est défini → utilisé tel quel (production / API distante).
 * - Sinon → chaîne vide : api.js utilisera des chemins relatifs /api (proxy Vite en dev).
 */
const raw = import.meta.env.VITE_API_BASE_URL ?? ''

export const API_BASE_URL = typeof raw === 'string' ? raw.replace(/\/$/, '') : ''
