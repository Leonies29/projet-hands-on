import { DataSection } from './components/DataSection.jsx'
import { PoemSection } from './components/PoemSection.jsx'
import { USE_MOCK } from './config.js'

export default function App() {
  return (
    <>
      {USE_MOCK && (
        <p className="mock-banner" role="status">
          Données simulées
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
