#!/usr/bin/env python3
""" Convert Moo2 files to useful images
    Useful info taken from http://www.karoltomala.com/blog/?p=39
"""
import os.path
import struct
import sys
from enum import Enum, auto
from typing import Optional, Any
from dataclasses import dataclass, field
from PIL import Image, ImageDraw


class LineType(Enum):
    NORMAL = auto()
    NEW_LINE = auto()
    END_DATA = auto()


##############################################################################
##############################################################################
@dataclass
class Line:
    """Handle a line of pixels, possibly indented"""

    pixels: list[int] = field(default_factory=list)
    indent: int = 0
    special: LineType = LineType.NORMAL


##############################################################################
##############################################################################
@dataclass
class Frame:
    """Handle number of lines"""

    indent: int = 0
    lines: list[Line] = field(default_factory=list)
    special: int = 0


##############################################################################
def load_palette(fname: str) -> dict[int, tuple[int, int, int]]:
    palette: dict[int, tuple[int, int, int]] = {}
    with open(fname, "rb") as infd:
        for counter in range(256):
            _ = struct.unpack("B", infd.read(1))[0]
            red = struct.unpack("B", infd.read(1))[0]
            green = struct.unpack("B", infd.read(1))[0]
            blue = struct.unpack("B", infd.read(1))[0]
            palette[counter] = (red * 4, green * 4, blue * 4)
    return palette


##############################################################################
##############################################################################
@dataclass
class Graphic:
    flags: dict[str, bool] = field(default_factory=dict)
    width: int = 0
    height: int = 0
    num_frames: int = 0
    delay: int = 0
    frames: list[Frame] = field(default_factory=list)

    ##############################################################################
    def load(self, fd) -> None:
        """Process the filename"""
        self.width = dread(fd)
        self.height = dread(fd)
        _ = fd.read(2)  # Nothing in the next two chars

        self.num_frames = dread(fd)
        self.delay = dread(fd)
        self.flags = self.image_flags(dread(fd))
        # print(f"{self.width} x {self.height} frames={self.num_frames} {self.flags}")
        frame_offsets = []
        for _ in range(self.num_frames + 1):
            offset = dread(fd, "<L", 4)
            frame_offsets.append(offset)
        for offset in frame_offsets[:-1]:
            fd.seek(offset)
            self.frames.append(self.process_frame(fd))

    ##############################################################################
    def image_flags(self, flag_seq: int) -> dict[str, bool]:
        """Pull out image flags"""
        return {
            "compressed": bool(flag_seq & 0x0100),
            "background": bool(flag_seq & 0x0400),
            "functional": bool(flag_seq & 0x0800),
            "internal": bool(flag_seq & 0x1000),
            "junction": bool(flag_seq & 0x2000),
        }

    ##############################################################################
    def process_frame(self, fd) -> Optional[Frame]:
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
                    line = Line(special=LineType.END_DATA, indent=y_indent)
                    frame.lines.append(line)
                    break
                line = Line(special=LineType.NEW_LINE, indent=y_indent)
                frame.lines.append(line)
            else:
                x_indent = dread(fd)
                byte_fmt = "<" + "B" * pixels
                colour_array = struct.unpack(byte_fmt, fd.read(pixels))
                line = Line(indent=x_indent, pixels=colour_array)
                if pixels % 2:
                    fd.read(1)
            frame.lines.append(line)
        return frame

    ##############################################################################
    def save_frame(self, filename: str, palette: dict[int, tuple[int, int, int]], frame: int = 0) -> None:
        """Same frame as an image"""
        f = self.frames[frame]
        image = Image.new("P", (self.width, self.height), "white")
        draw = ImageDraw.Draw(image)
        rel_x = 0
        rel_y = f.indent

        for line in f.lines:
            if line.special == LineType.NORMAL:
                rel_x += line.indent
                for x in range(len(line.pixels)):
                    colour = palette[line.pixels[x]]
                    draw.point((rel_x + x, rel_y), fill=colour)
                    print(f"DBG {rel_x+x}, {rel_y}")
            else:
                rel_y += line.indent
                print(f"DBG {rel_y=} {line.indent=}")
                rel_x = 0
        with open(filename, "wb") as outfh:
            image.save(outfh, "PNG")


##############################################################################
def dread(fd, format: str = "<H", bytes: int = 2) -> Any:
    return struct.unpack(format, fd.read(bytes))[0]


##############################################################################
def main() -> None:
    """Do the stuff"""
    palettes = [f"../foo/FONTS.LBX_{_}" for _ in range(1, 14)] + [f"../foo/IFONTS.LBX_{_}" for _ in range(1, 4)]
    for num, palfile in enumerate(palettes):
        palette = load_palette(palfile)
        for file in sys.argv[1:]:
            try:
                g = Graphic()
                with open(file, "rb") as fd:
                    g.load(fd)
                save_file = f"{os.path.basename(file)}_{num}.png"
                g.save_frame(save_file, palette)
            except Exception as exc:
                print(f"Failure on {file}: {exc}")
                raise


##############################################################################
if __name__ == "__main__":
    main()

# EOF
