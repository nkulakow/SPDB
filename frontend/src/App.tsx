import MapView from './components/MapView'
import RouteForm from './components/RouteForm'
import './App.css'
import { ToastContainer } from 'react-toastify'
import { useState } from 'react';
import { IconButton } from '@mui/material';
import InfoIcon from "@mui/icons-material/Info";
import RouteDetails from './components/RouteDetails';


export default function App() {
  const [open, setOpen] = useState(false);

  return (
    <div className="layout">
      <RouteForm />

      <MapView />

      <IconButton
        onClick={() => setOpen(true)}
        sx={{
          position: "absolute",
          right: 16,
          top: 16,
          zIndex: 1000,
          background: "white"
        }}
      >
        <InfoIcon />
      </IconButton>

      <RouteDetails open={open} setOpen={setOpen} />


      <ToastContainer position="bottom-right" />
    </div>
  )
}
