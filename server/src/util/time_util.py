from datetime import datetime, time, timedelta


def time_diff(t1: time, t2: time) -> timedelta:
    """
    Calculates difference between t2 and t1. Assumes t2 is after t1.
    """
    dt1 = datetime.combine(datetime.today(), t1)
    dt2 = datetime.combine(datetime.today(), t2)

    if dt2 < dt1:
        dt2 += timedelta(days=1)

    return dt2 - dt1


def add_time(t: time, delta: timedelta) -> time:
    """
    Adds a timedelta to a time, wrapping around midnight if necessary.
    """
    dt = datetime.combine(datetime.today(), t) + delta
    return dt.time()
