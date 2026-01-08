class LocationNotFoundError(ValueError):
    """Exception raised when a location cannot be found in the graph."""

    location: str
    def __init__(self, location_name: str):
        super().__init__(f"Location '{location_name}' not found.")
        self.location = location_name
