import { MapContainer, TileLayer, Polyline, Marker, Popup, CircleMarker } from 'react-leaflet'
import { useRoute } from "../context/RouteContext";

export default function MapView() {
  const { route } = useRoute();

  return (
    <MapContainer
      center={[52.25, 21.02]}
      zoom={10}
      style={{ height: '100%', width: '100%' }}
    >
      <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />

      {/* START */}
      {route && (
        <Marker position={[route.start.latitude, route.start.longitude]}>
          <Popup>{route.start.name}</Popup>
        </Marker>
      )}

      {/* ROUTES */}
      {route?.routes.map((r, i) => {
        const points: [number, number][] = [
          [route.start.latitude, route.start.longitude],
          ...r.nodes.map(n => [n.latitude, n.longitude] as [number, number]),
          [r.destination.latitude, r.destination.longitude],
        ];

        return (
          <Polyline
            key={i}
            positions={points}
            color={r.color}
            weight={4}
            opacity={0.9}
          />
        );
      })}

      {/* DESTINATIONS */}
      {route?.routes.map((r, i) => (
        <Marker key={i} position={[r.destination.latitude, r.destination.longitude]}>
          <Popup>{r.destination.name}</Popup>
        </Marker>
      ))}

      {/* NODES */}
      {route?.routes.map((r, i) =>
        r.nodes.map((node, j) => (
          <CircleMarker
            key={`node-${i}-${j}`}
            center={[node.latitude, node.longitude]}
            radius={3}
            weight={0.3}
            color={r.color}
            fillColor="white"
            fillOpacity={0.8}
          >
          </CircleMarker>
        ))
      )}
    </MapContainer>
  );
}
