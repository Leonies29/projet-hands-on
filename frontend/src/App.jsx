import { DataSection } from './components/DataSection.jsx'
import { PoemSection } from './components/PoemSection.jsx'
import { USE_MOCK } from './config.js'

export default function App() {
  return (
    <>
      {USE_MOCK && (
        <p className="mock-banner" role="status">
          Mode mock : aucun appel réseau vers l’API — à désactiver (
          <code>VITE_USE_MOCK=false</code>) quand le backend est prêt.
        </p>
      )}
      <main>
        <h1>Mini projet — consommation de l’API</h1>
        <DataSection />
        <PoemSection />
      </main>
    </>
  )
}
