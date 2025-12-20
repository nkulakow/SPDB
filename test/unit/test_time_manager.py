from time_manager import VelociyModifier


VELOCITY_MODIFIER = [
    ("00:00", 1.0),
    ("02:00", 1.2),
    ("04:00", 0.8),
    ("06:00", 1.5),
    ("08:00", 0.5),
    ("10:00", 1.0),
    ("12:00", 1.3),
    ("14:00", 1.0),
    ("16:00", 0.9),
    ("18:00", 1.1),
    ("20:00", 1.0),
    ("22:00", 0.7)
]

def test_create_time_manager():
    tm = VelociyModifier(VELOCITY_MODIFIER)
