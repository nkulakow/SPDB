import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'
import 'leaflet/dist/leaflet.css'
import { RouteProvider } from './context/RouteContext.tsx'

createRoot(document.getElementById('root')!).render(
  <RouteProvider>
    <App />
  </RouteProvider>
)
