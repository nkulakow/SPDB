import { useState } from 'react'
import {
  TextField,
  Button,
  MenuItem,
  Select,
  FormControl,
  InputLabel,
  Box,
  Typography,
  Stack,
  IconButton,
} from '@mui/material'
import AddIcon from '@mui/icons-material/Add'
import PlaceIcon from "@mui/icons-material/Place"
import TripOriginIcon from '@mui/icons-material/TripOrigin';
import { planRoute } from '../api/roadService';
import { toast } from "react-toastify";
import { useRoute } from "../context/RouteContext";
import { APIError } from '../api/fetchAPI';
import type { PlannedRoute } from '../types';
import Grid from "@mui/material/Grid";
import RemoveCircleIcon from "@mui/icons-material/RemoveCircle";




class TimeSlotOption {
  time: number;
  timeStr: string;
  constructor(time: number, timeStr: string) {
    this.time = time;
    this.timeStr = timeStr;
  }
}

function randomColor() {
  const hue = Math.floor(Math.random() * 360);
  return `hsl(${hue}, 90%, 38%)`;
}


export default function RouteForm() {
  const [start, setStart] = useState('')
  const [destinations, setDestinations] = useState<string[]>([''])
  const [timeSlotStart, setTimeSlotStart] = useState(9)
  const [timeSlotEnd, setTimeSlotEnd] = useState(11)
  const { setRoute } = useRoute();
  const [errors, setErrors] = useState<{ start?: string; destinations?: string[]; timeSlot?: string }>({});

  const timeOptions = Array.from({ length: 25 }, (_, i) =>
    new TimeSlotOption(i, `${i.toString().padStart(2, '0')}:00`)
  )

  const addDestination = () => {
    setDestinations([...destinations, ''])
  }

  const removeDestination = (index: number) => {
    setDestinations(destinations.filter((_, i) => i !== index));
    setErrors(prev => ({ ...prev, destinations: prev.destinations?.filter((_, i) => i !== index) }));
  };

  const updateDestination = (index: number, value: string) => {
    const copy = [...destinations]
    copy[index] = value
    setDestinations(copy)
  }

  const validate = () => {
    let valid = true;
    const newErrors: { start?: string; destinations?: string[]; timeSlot?: string } = {};
    if (!start.trim()) {
      newErrors.start = "Required";
      valid = false;
    }
    const destErrors = destinations.map(d => (!d.trim() ? "Required" : ""));
    if (destErrors.some(e => e)) valid = false;
    newErrors.destinations = destErrors;

    if (timeSlotStart >= timeSlotEnd) {
      newErrors.timeSlot = "Start time must be less than End time";
      valid = false;
    }

    setErrors(newErrors);
    return valid;
  };

  const search = async () => {
    if (!validate()) return;

    try {
      const result = await planRoute(start, destinations, timeSlotStart, timeSlotEnd);
      const colored: PlannedRoute = {
        ...result,
        routes: result.routes.map(r => ({
          ...r,
          color: randomColor()
        }))
      };
      setRoute(colored);
      toast.success("Routes planned");
    } catch (e: any) {
      if (e instanceof APIError) {
        toast.error(`Failed to plan routes: ${e.message}`);
        return;
      }
      toast.error("Failed to plan routes");
    }
  };


  const selectMenuProps = {
    PaperProps: {
      style: {
        maxHeight: 48 * 6,
        backgroundColor: '#7a7a7aff',
      },
    },
  }

  return (
    <Box className="route-form">
      <Typography variant="h5" gutterBottom>Route Planner</Typography>

      <Stack direction="row" alignItems="center" spacing={1} mb={2}>
        <TripOriginIcon sx={{ color: 'white' }} />
        <TextField
          className="white-textfield"
          placeholder={start ? '' : 'Start location'}
          value={start}
          onChange={(e) => setStart(e.target.value)}
          fullWidth
          variant="outlined"
          error={!!errors.start}
          helperText={errors.start}
        />
      </Stack>

      <Stack spacing={2} mb={2}>
        {destinations.map((d, i) => (
          <Stack key={i} direction="row" alignItems="center" spacing={1}>
            <PlaceIcon sx={{ color: 'white' }} />
            <TextField
              className="white-textfield"
              placeholder={d ? '' : `Destination ${i + 1}`}
              value={d}
              onChange={(e) => updateDestination(i, e.target.value)}
              fullWidth
              error={!!errors.destinations?.[i]}
              helperText={errors.destinations?.[i]}
            />
            {i > 0 && (
              <IconButton size="small" onClick={() => removeDestination(i)}>
                <RemoveCircleIcon sx={{ color: 'white' }} />
              </IconButton>
            )}
          </Stack>
        ))}

        <Button
          startIcon={<AddIcon />}
          onClick={addDestination}
          variant="outlined"
          sx={{ alignSelf: 'flex-start', color: 'white', borderColor: 'white' }}
        >
          Add Destination
        </Button>
      </Stack>

      <Typography variant="h6" gutterBottom>Time Slot</Typography>
      <Grid container spacing={2} mb={3}>
        <Grid size={{ xs: 6 }}>
          <FormControl fullWidth>
            <InputLabel>Start</InputLabel>
            <Select
              value={timeSlotStart}
              label="Start"
              onChange={(e) => setTimeSlotStart(e.target.value)}
              MenuProps={selectMenuProps}
            >
              {timeOptions.map(time => (
                <MenuItem key={time.time} value={time.time}>{time.timeStr}</MenuItem>
              ))}
            </Select>

          </FormControl>
        </Grid>

        <Grid size={{ xs: 6 }}>
          <FormControl fullWidth>
            <InputLabel>End</InputLabel>
            <Select
              value={timeSlotEnd}
              label="End"
              onChange={(e) => setTimeSlotEnd(e.target.value)}
              MenuProps={selectMenuProps}
            >
              {timeOptions.map(time => (
                <MenuItem key={time.time} value={time.time}>{time.timeStr}</MenuItem>
              ))}
            </Select>
          </FormControl>
        </Grid>
        {errors.timeSlot && (
          <Typography variant="caption" color="error">{errors.timeSlot}</Typography>
        )}
      </Grid>


      <Button variant="outlined" onClick={search} sx={{ color: 'white', borderColor: 'white' }}>
        Search
      </Button>
    </Box>
  )
}
