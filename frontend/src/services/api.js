import { API_BASE_URL, USE_MOCK } from '../config.js'
import * as mock from './mockApi.js'

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
  if (USE_MOCK) return mock.mockGetData()
  return fetch(url('/data')).then(handle)
}

export function postData(body) {
  if (USE_MOCK) return mock.mockPostData(body)
  return fetch(url('/data'), {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  }).then(handle)
}

export function getPoem() {
  if (USE_MOCK) return mock.mockGetPoem()
  return fetch(url('/poem')).then(handle)
}
