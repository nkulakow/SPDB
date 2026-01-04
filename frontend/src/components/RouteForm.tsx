import { useState } from 'react'
import {
  TextField,
  Button,
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
import RemoveCircleIcon from "@mui/icons-material/RemoveCircle";
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { DateTimePicker } from '@mui/x-date-pickers/DateTimePicker';
import dayjs, { Dayjs } from 'dayjs';
import { createTheme, ThemeProvider } from '@mui/material/styles';


function randomColor() {
  const hue = Math.floor(Math.random() * 360);
  return `hsl(${hue}, 90%, 38%)`;
}

export const theme = createTheme({
  palette: { mode: "dark" },
});

const darkDateTimePickerSlots = (hasError?: boolean) => ({
  textField: {
    fullWidth: true,
    error: hasError,
  },

  popper: {
    sx: {
      '& .MuiPickersDay-root.Mui-selected': {
        backgroundColor: '#00c853 !important',
        color: '#fff',
      },

      '& .MuiClockNumber-root, & .MuiMenuItem-root': {
        color: '#fff',
      },

      '& .MuiMenuItem-root.Mui-selected': {
        backgroundColor: '#00c853 !important',
        color: '#fff',
      },

      '& .MuiButton-root': {
        color: '#fff',
      },
      '& .MuiYearCalendar-button.Mui-selected': {
        backgroundColor: '#00c853 !important',
        color: '#fff',
      },
    },
  },
});


export default function RouteForm() {
  const [start, setStart] = useState('')
  const [destinations, setDestinations] = useState<string[]>([''])
  const [startDateTime, setStartDateTime] = useState<Dayjs | null>(dayjs());
  const [endDateTime, setEndDateTime] = useState<Dayjs | null>(
    dayjs().add(2, 'hour')
  );

  const { setRoute } = useRoute();
  const [errors, setErrors] = useState<{ start?: string; destinations?: string[]; timeSlot?: string }>({});

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

    if (!startDateTime || !endDateTime || startDateTime.isAfter(endDateTime)) {
      newErrors.timeSlot = "Start date/time must be before End date/time";
      valid = false;
    }


    setErrors(newErrors);
    return valid;
  };

  const search = async () => {
    if (!validate()) return;

    try {
      const result = await planRoute(start, destinations, startDateTime!, endDateTime!);
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

      <ThemeProvider theme={theme}>
        <LocalizationProvider dateAdapter={AdapterDayjs}>
          <Stack spacing={2} mb={3}>

            <DateTimePicker
              label="Start"
              value={startDateTime}
              onChange={(newValue) => setStartDateTime(newValue)}
              slotProps={darkDateTimePickerSlots(
                !!errors.timeSlot,
              )}
            />

            <DateTimePicker
              label="End"
              value={endDateTime}
              onChange={(newValue) => setEndDateTime(newValue)}
              minDateTime={startDateTime ?? undefined}
              slotProps={darkDateTimePickerSlots(
                !!errors.timeSlot,
              )}
            />


            {errors.timeSlot && (
              <Typography variant="caption" color="error">
                {errors.timeSlot}
              </Typography>
            )}
          </Stack>
        </LocalizationProvider>
      </ThemeProvider>



      <Button variant="outlined" onClick={search} sx={{ color: 'white', borderColor: 'white' }}>
        Search
      </Button>
    </Box>
  )
}
