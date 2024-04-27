#!/usr/bin/env python3
""" Convert Moo2 files to useful images
    Useful info taken from http://www.karoltomala.com/blog/?p=39
"""

import struct
import sys
from typing import Optional, Any
from dataclasses import dataclass, field


##############################################################################
##############################################################################
@dataclass
class Line:
    """Handle a line of pixels, possibly indented"""

    pixels: bytearray = field(default_factory=bytearray)
    indent: int = 0
    special: int = 0


##############################################################################
##############################################################################
@dataclass
class Frame:
    """Handle number of lines"""

    indent: int = 0
    lines: list[Line] = field(default_factory=list)
    special: int = 0


##############################################################################
def image_flags(flag_seq: int) -> dict[str, bool]:
    """Pull out image flags"""
    return {
        "uncompressed": bool(flag_seq & 0x0100),
        "background": bool(flag_seq & 0x0400),
        "functional": bool(flag_seq & 0x0800),
        "internal": bool(flag_seq & 0x1000),
        "junction": bool(flag_seq & 0x2000),
    }


##############################################################################
def process_frame(fd) -> Optional[Frame]:
    """Process the frame data"""
    frame_indicator = dread(fd)

    if frame_indicator != 1:
        return None
    frame_y_indent = dread(fd)
    frame = Frame(indent=frame_y_indent)
    while True:
        pixels = dread(fd)
        if pixels == 0:
            y_indent = dread(fd)
            if y_indent == 1000:  # End of Data
                line = Line(special=2, indent=y_indent)
                frame.lines.append(line)
                break
            line = Line(special=1, indent=y_indent)
            frame.lines.append(line)
        else:
            x_indent = dread(fd)
            byte_fmt = "<" + "B" * pixels
            colour_array = dread(fd, byte_fmt, pixels)
            line = Line(indent=x_indent, pixels=colour_array)
            if pixels % 2:
                fd.read(1)
        frame.lines.append(line)
    return frame


##############################################################################
def dread(fd, format: str = "<H", bytes: int = 2) -> Any:
    return struct.unpack(format, fd.read(bytes))[0]


##############################################################################
def process(fd) -> None:
    """Process the filename"""
    width = dread(fd)
    height = dread(fd)
    _ = fd.read(2)  # Nothing in the next two chars

    frames = dread(fd)
    frame_delay = dread(fd)
    flags = image_flags(dread(fd))
    print(f"{width} x {height} @ {frames} frames {frame_delay} delay")
    print(f"Flags {flags}")
    frame_offsets = []
    for _ in range(frames + 1):
        offset = dread(fd, "<L", 4)
        frame_offsets.append(offset)
    print(f"Offsets = {frame_offsets}")
    for offset in frame_offsets[:-1]:
        fd.seek(offset)
        x = process_frame(fd)
        print(x)


##############################################################################
def main() -> None:
    """Do the stuff"""
    file = sys.argv[1]
    with open(file, "rb") as fd:
        process(fd)


##############################################################################
if __name__ == "__main__":
    main()

# EOF
