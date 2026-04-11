import { useState } from 'react'
import { getData, postData } from '../services/api.js'

export function DataSection() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [newLine, setNewLine] = useState('')

  async function load() {
    setError(null)
    setLoading(true)
    try {
      setData(await getData())
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  async function add() {
    setError(null)
    setLoading(true)
    try {
      // Exemple : si l’API attend { line: "..." } — adapte au contrat réel de POST /data
      await postData({ line: newLine })
      setNewLine('')
      await load()
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <section>
      <h2>Données (GET /data, POST /data)</h2>
      <div className="row">
        <button type="button" onClick={load} disabled={loading}>
          Charger les données
        </button>
      </div>
      <div className="row" style={{ marginTop: '0.75rem' }}>
        <input
          type="text"
          value={newLine}
          onChange={(e) => setNewLine(e.target.value)}
          placeholder="Texte à ajouter (exemple)"
          aria-label="Nouvelle entrée"
        />
        <button type="button" onClick={add} disabled={loading || !newLine.trim()}>
          Envoyer (POST)
        </button>
      </div>
      {error && <p className="error">{error}</p>}
      {data != null && (
        <pre>{typeof data === 'string' ? data : JSON.stringify(data, null, 2)}</pre>
      )}
    </section>
  )
}
