import { useState } from 'react'
import { getPoem } from '../services/api.js'

export function PoemSection() {
  const [poem, setPoem] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  async function load() {
    setError(null)
    setLoading(true)
    try {
      const res = await getPoem()
      // Selon l’API : string directe ou { poem: "..." }
      setPoem(typeof res === 'string' ? res : res.poem ?? JSON.stringify(res))
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <section>
      <h2>Poème (GET /poem)</h2>
      <button type="button" onClick={load} disabled={loading}>
        Générer / afficher un poème
      </button>
      {error && <p className="error">{error}</p>}
      {poem != null && <pre style={{ whiteSpace: 'pre-wrap' }}>{poem}</pre>}
    </section>
  )
}
