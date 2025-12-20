from datetime import time
from dataclasses import dataclass


class VelociyModifier:
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
        left_child: "VelociyModifier.TimeSlot | None" = None
        right_child: "VelociyModifier.TimeSlot | None" = None

    root: TimeSlot

    def __init__(self, time_slots: list[tuple[time, float]]) -> None:
        self.root = self.__build_tree(time_slots, 0, len(time_slots) - 1)

    def __build_tree(self, slots: list[tuple[time, float]], start_index: int, end_index: int) -> "VelociyModifier.TimeSlot | None":
        middle_index = (end_index - start_index) // 2 + start_index
        start, modifier = slots[middle_index]
        end = slots[middle_index + 1][0] if middle_index + 1 < len(slots) else time()

        current_slot = VelociyModifier.TimeSlot(start=start, end=end, modifier=modifier)

        if end_index - start_index >= 1:
            if middle_index > start_index:
                current_slot.left_child = self.__build_tree(slots, start_index, middle_index - 1)
            if middle_index < end_index:
                current_slot.right_child = self.__build_tree(slots, middle_index + 1, end_index)

        return current_slot
