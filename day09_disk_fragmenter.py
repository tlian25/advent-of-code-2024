# Day 9: Disk Fragmenter
# https://adventofcode.com/2024/day/9

from typing import List

from utils.input import read_input_file_lines

SPACE = "."


def parse_inputs():
    lines = read_input_file_lines("day09_input.txt")
    return [int(x) for x in lines[0]]


def construct_disk_from_disk_map(disk_map: List[int]) -> List[int]:
    file_idx = 0
    disk = []
    for i, n in enumerate(disk_map):
        if i % 2:  # space
            disk += [SPACE] * n
        else:  # num
            disk += [file_idx] * n
            file_idx += 1
    return disk


def find_next_space(disk: List[int], offset) -> int:
    while disk[offset] != SPACE:
        offset += 1
    return offset


def swap(disk: List[int], i: int, j: int) -> None:
    disk[i], disk[j] = disk[j], disk[i]


def compress_disk(disk: List[int]):
    i = find_next_space(disk, 0)
    j = len(disk) - 1
    while i < j:
        if disk[j] != SPACE:
            swap(disk, i, j)
            i = find_next_space(disk, i + 1)
        else:
            j -= 1


def calculate_checksum(disk: List[int]):
    checksum = 0
    for i, n in enumerate(disk):
        if n == SPACE:
            return checksum
        checksum += i * n


# Implement Part 2 with a double linked list
class Slot:
    def __init__(self, val="", count=1):
        self.val = val
        self.count = count
        self.next = None
        self.prev = None

    def __str__(self):
        return str(self.val) * self.count


class Disk:
    def __init__(self, disk_map: List[int]):
        self.head = Slot("HEAD", 1)
        self.tail = Slot("TAIL", 1)

        curr = self.head
        prev = None
        file_idx = 0
        for i, n in enumerate(disk_map):
            if i % 2:  # space
                curr.next = Slot(val=SPACE, count=n)
            else:
                curr.next = Slot(val=file_idx, count=n)
                file_idx += 1
            prev = curr
            curr = curr.next
            curr.prev = prev

        curr.next = self.tail
        self.tail.prev = curr

    def compress_node(self, node) -> bool:
        """return True if we were able to compress"""
        curr = self.head.next
        while curr != node:
            if curr.val != SPACE or node.count > curr.count:
                curr = curr.next
                continue

            # Merge front and back of node if both SPACEs
            next_node = node.next
            prev_node = node.prev
            prev_node.next = next_node
            if next_node.val == SPACE and prev_node.val == SPACE:
                # Merge together into prev and remove next
                prev_node.count += node.count + next_node.count
                prev_node.next = next_node.next
                next_node.next.prev = prev_node
            elif next_node.val == SPACE:
                # Add space counts to next node
                next_node.count += node.count
                next_node.prev = prev_node
                prev_node.next = next_node
            elif prev_node.val == SPACE:
                # Add space counts to prev node
                prev_node.count += node.count
                prev_node.next = next_node
                next_node.prev = prev_node
            else:
                # Create new space slot in place of moved node
                newspace = Slot(SPACE, node.count)
                prev_node.next = newspace
                next_node.prev = newspace
                newspace.prev = prev_node
                newspace.next = next_node

            # Insert node into space
            # If node doesn't take full space, leave remaining space
            curr_prev = curr.prev
            remaining_spaces = curr.count - node.count
            if remaining_spaces:
                curr.count = remaining_spaces
            else:
                curr = curr.next

            curr_prev.next = node
            node.prev = curr_prev
            node.next = curr
            curr.prev = node

            return prev_node

        # Unable to compress, return prev node working backwards
        return node.prev

    def compress_all(self):
        curr_node = self.tail.prev
        while curr_node != self.head.next:
            if curr_node.val == SPACE:
                curr_node = curr_node.prev
            else:
                curr_node = self.compress_node(curr_node)

    def calculate_checksum(self):
        i = 0
        checksum = 0
        curr = self.head.next
        while curr != self.tail:
            for _ in range(curr.count):
                if curr.val != SPACE:
                    checksum += i * curr.val
                i += 1

            curr = curr.next
        return checksum

    def __str__(self):
        s = []
        curr = self.head.next
        while curr != self.tail:
            s.append(str(curr))
            curr = curr.next
        return "".join(s)


def part1():
    disk_map = parse_inputs()
    disk = construct_disk_from_disk_map(disk_map)
    compress_disk(disk)
    return calculate_checksum(disk)


def part2():
    disk_map = parse_inputs()
    disk = Disk(disk_map)
    disk.compress_all()
    return disk.calculate_checksum()


s1 = part1()
print("Solution Part 1:", s1)
s2 = part2()
print("Solution Part 2:", s2)
