from velocity_modifier import VelocityModifier
from datetime import time, datetime, timedelta
import pytest


@pytest.fixture
def velocity_modifier():
    VELOCITY_MODIFIER = [
        (datetime.strptime("00:00", "%H:%M").time(), 1.0),
        (datetime.strptime("02:00", "%H:%M").time(), 1.2),
        (datetime.strptime("04:00", "%H:%M").time(), 0.8),
        (datetime.strptime("06:00", "%H:%M").time(), 1.5),
        (datetime.strptime("08:00", "%H:%M").time(), 0.5),
        (datetime.strptime("10:00", "%H:%M").time(), 1.0),
        (datetime.strptime("12:00", "%H:%M").time(), 1.3),
        (datetime.strptime("14:00", "%H:%M").time(), 1.0),
        (datetime.strptime("16:00", "%H:%M").time(), 0.9),
        (datetime.strptime("18:00", "%H:%M").time(), 1.1),
        (datetime.strptime("20:00", "%H:%M").time(), 1.0),
        (datetime.strptime("22:00", "%H:%M").time(), 0.7)
    ]
    return VelocityModifier(VELOCITY_MODIFIER)


def test_get_modifier_time_equal_to_slot_start(velocity_modifier):
    assert velocity_modifier.get_velocity_modifier(time(0, 0)) == 1.0
    assert velocity_modifier.get_velocity_modifier(time(2, 0)) == 1.2
    assert velocity_modifier.get_velocity_modifier(time(22, 0)) == 0.7


def test_get_modifier_time_equal_to_slot_end(velocity_modifier):
    assert velocity_modifier.get_velocity_modifier(time(1, 59)) == 1.0
    assert velocity_modifier.get_velocity_modifier(time(3, 59)) == 1.2
    assert velocity_modifier.get_velocity_modifier(time(23, 59)) == 0.7


def test_get_modifier_time_in_between_slot(velocity_modifier):
    assert velocity_modifier.get_velocity_modifier(time(5, 0)) == 0.8
    assert velocity_modifier.get_velocity_modifier(time(9, 30)) == 0.5
    assert velocity_modifier.get_velocity_modifier(time(15, 15)) == 1.0


def test_get_max_time_in_slot_time_equal_to_slot_start(velocity_modifier):
    assert velocity_modifier.get_max_time_in_slot(time(0, 0)) == timedelta(hours=2)
    assert velocity_modifier.get_max_time_in_slot(time(2, 0)) == timedelta(hours=2)
    assert velocity_modifier.get_max_time_in_slot(time(22, 0)) == timedelta(hours=2)


def test_get_max_time_in_slot_time_equal_to_slot_end(velocity_modifier):
    assert velocity_modifier.get_max_time_in_slot(time(1, 59)) == timedelta(minutes=1)
    assert velocity_modifier.get_max_time_in_slot(time(3, 59)) == timedelta(minutes=1)
    assert velocity_modifier.get_max_time_in_slot(time(23, 59)) == timedelta(minutes=1)


def test_get_max_time_in_slot_time_in_between_slot(velocity_modifier):
    assert velocity_modifier.get_max_time_in_slot(time(5, 0)) == timedelta(hours=1)
    assert velocity_modifier.get_max_time_in_slot(time(9, 30)) == timedelta(hours=0, minutes=30)
    assert velocity_modifier.get_max_time_in_slot(time(15, 15)) == timedelta(hours=0, minutes=45)
