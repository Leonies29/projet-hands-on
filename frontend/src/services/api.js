import { API_BASE_URL } from '../config.js'

function url(path) {
  const p = path.startsWith('/') ? path : `/${path}`
  if (API_BASE_URL) return `${API_BASE_URL}${p}`
  return `/api${p}`
}

async function handle(res) {
  if (!res.ok) {
    const text = await res.text()
    throw new Error(text || res.statusText)
  }
  const ct = res.headers.get('content-type') || ''
  if (ct.includes('application/json')) return res.json()
  return res.text()
}

export function getData() {
  return fetch(url('/data')).then(handle)
}

/**
 * @param {object} body — objet sérialisé en JSON (doit correspondre au contrat de ton API)
 */
export function postData(body) {
  return fetch(url('/data'), {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  }).then(handle)
}

export function getPoem() {
  return fetch(url('/poem')).then(handle)
}
