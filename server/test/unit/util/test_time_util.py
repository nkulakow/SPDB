from datetime import time, timedelta
from src.util.time_util import time_diff, add_time
import pytest


@pytest.mark.parametrize(
    "t1, t2, expected_diff",
    [
        (time(10, 0), time(12, 0), timedelta(hours=2)),
        (time(10, 32), time(14, 16), timedelta(hours=3, minutes=44)),
    ]
)
def test_time_diff_t1_before_t2(t1: time, t2: time, expected_diff: timedelta):
    assert time_diff(t1, t2) == expected_diff


@pytest.mark.parametrize(
    "t1, t2, expected_diff",
    [
        (time(12, 0), time(10, 0), timedelta(hours=22)),
        (time(14, 16), time(10, 32), timedelta(hours=20, minutes=16)),
    ]
)
def test_add_time_changing_day(t1: time, t2: time, expected_diff: timedelta):
    assert time_diff(t1, t2) == expected_diff


@pytest.mark.parametrize(
    "t1, t2, expected_t",
    [
        (time(12, 0), timedelta(hours=2), time(14, 0)),
        (time(14, 17), timedelta(hours=7, minutes=17), time(21, 34)),
        (time(14, 17), timedelta(hours=7, minutes=52), time(22, 9)),
    ]
)
def test_add_time_changing_day(t1: time, t2: time, expected_t: time):
    assert add_time(t1, t2) == expected_t


@pytest.mark.parametrize(
    "t1, t2, expected_t",
    [
        (time(12, 0), timedelta(hours=12), time(0, 0)),
        (time(12, 17), timedelta(hours=13, minutes=17), time(1, 34)),
        (time(12, 17), timedelta(hours=11, minutes=52), time(0, 9)),
    ]
)
def test_add_time_changing_day(t1: time, t2: timedelta, expected_t: time):
    assert add_time(t1, t2) == expected_t
