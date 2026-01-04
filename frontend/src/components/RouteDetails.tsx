import { Box, Drawer, Typography } from "@mui/material";
import { useRoute } from "../context/RouteContext";

type RouteDetailsProps = {
  open: boolean;
  setOpen: (open: boolean) => void;
};

export default function RouteDetails({ open, setOpen }: RouteDetailsProps) {
  const { route } = useRoute();

  const renderRouteInfo = () => {
    if (!route) return <Typography>No route planned.</Typography>;

    return (
      <Box>
        <Typography variant="h6">Start: {route.start.name}</Typography>

        {route.routes.map((r, i) => (
          <Box
            key={i}
            sx={{
              my: 1,
              borderBottom: "1px solid #444",
              pb: 1,
              display: "flex",
              alignItems: "flex-start",
            }}
          >
            <Box
              sx={{
                width: 6,
                backgroundColor: r.color,
                borderRadius: 1,
                mr: 1,
                alignSelf: "stretch",
              }}
            />

            <Box>
              <Typography fontWeight="bold">{r.destination.name}</Typography>
              <Typography>Best time: {r.plannedStartTime} - {r.plannedEndTime}</Typography>
            </Box>
          </Box>
        ))}
      </Box>
    );
  };

  return (
    <Drawer
      anchor="right"
      open={open}
      onClose={() => setOpen(false)}
      slotProps={{
        paper: {
          sx: {
            width: 300,
            background: "#121212",
            color: "white",
            padding: 2
          }
        }
      }}
    >
      <Box>
        <Typography variant="h5" sx={{ mb: 2 }}>
          Route Information
        </Typography>
        {renderRouteInfo()}
      </Box>
    </Drawer>
  );
}