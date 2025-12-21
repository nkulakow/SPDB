from datetime import time, datetime, timedelta
from dataclasses import dataclass


class VelocityModifier:
    """
    Stores velocity modifiers based on time in a binary search tree.
    """

    @dataclass
    class TimeSlot:
        """
        Represents a time slot with a start time inclusively, end time exclusively, and velocity modifier.
        """

        start: time
        end: time
        modifier: float
        left_child: "VelocityModifier.TimeSlot | None" = None
        right_child: "VelocityModifier.TimeSlot | None" = None

    root: TimeSlot

    def __init__(self, time_slots: list[tuple[time, float]]) -> None:
        self.root = self.__build_tree(time_slots, 0, len(time_slots) - 1)

    def __build_tree(self, slots: list[tuple[time, float]], start_index: int, end_index: int) -> "VelocityModifier.TimeSlot | None":
        middle_index = (end_index - start_index) // 2 + start_index
        start, modifier = slots[middle_index]
        end = slots[middle_index + 1][0] if middle_index + 1 < len(slots) else time()

        current_slot = VelocityModifier.TimeSlot(start=start, end=end, modifier=modifier)

        if end_index - start_index >= 1:
            if middle_index > start_index:
                current_slot.left_child = self.__build_tree(slots, start_index, middle_index - 1)
            if middle_index < end_index:
                current_slot.right_child = self.__build_tree(slots, middle_index + 1, end_index)

        return current_slot

    def find_time_slot(self, t: time) -> "VelocityModifier.TimeSlot":
        """
        Finds the time slot that contains the given time t.
        """
        current_slot = self.root

        while current_slot:
            if (current_slot.start <= t < current_slot.end) or (current_slot.start <= t and current_slot.end == time()):
                return current_slot
            elif t < current_slot.start:
                current_slot = current_slot.left_child
            else:
                current_slot = current_slot.right_child

        assert False, "unreachable code reached"

    def get_velocity_modifier(self, t: time) -> float:
        """
        Returns the velocity modifier for the given time t.
        The slot includes the start time and excludes the end time.
        """
        return self.find_time_slot(t).modifier

    def get_max_time_in_slot(self, t: time) -> timedelta:
        """
        Returns the maximum time in the slot that contains time t.
        """
        slot = self.find_time_slot(t)
        diff = datetime.combine(datetime.today(), slot.end) - datetime.combine(datetime.today(), t)
        if slot.end == time():
            diff += timedelta(days=1)
        return diff
