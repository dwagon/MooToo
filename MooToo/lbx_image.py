""" Convert original MOO2 weird media format into something useful"""

import io
import os
import struct
import sys
from dataclasses import dataclass, field
from typing import Any, Optional
from enum import Enum, auto

from PIL import Image, ImageDraw


##############################################################################
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


#####################################################################################################
#####################################################################################################
# lbx_file="BUFFER0.LBX", lbx_index=1, palette=1, moo_path="..."
class LBXImage:
    def __init__(self, lbx_file: str, lbx_index: int, moo_path: str, frame: int = 0, palette_file: str = "FONTS.LBX"):
        self.width: int = 0
        self.height: int = 0
        self.palette = load_palette(moo_path, palette_file)
        file_data = load_lbx(moo_path, lbx_file, lbx_index)
        if not file_data:
            raise UserWarning("Couldn't load LBX file")
        frames = self.load_frames(io.BytesIO(file_data))
        self.pil_image = self.save_frame(frames[frame])

    ##############################################################################
    def png_image(self) -> io.BytesIO:
        """Export image and a PNG filestream"""
        x = io.BytesIO()
        self.pil_image.save(x, format="png")
        x.seek(0)
        return x

    ##############################################################################
    def load_frames(self, fd) -> list[Frame]:
        """Extract image frames"""
        frames: list[Frame] = []
        try:
            self.width = dread(fd)
        except struct.error as e:
            raise UserWarning("Empty file") from e
        self.height = dread(fd)
        _ = fd.read(2)  # Nothing in the next two chars

        num_frames = dread(fd)
        delay = dread(fd)
        flags = self.image_flags(dread(fd))
        # print(f"{self.width} x {self.height} frames={num_frames} delay={delay} {flags}")
        frame_offsets = []
        try:
            for _ in range(num_frames + 1):
                offset = dread(fd, "<L", 4)
                frame_offsets.append(offset)
        except struct.error as exc:
            raise UserWarning("Not an image file") from exc
        if flags["internal"]:
            self.load_internal_palette(fd)
        for offset in frame_offsets[:-1]:
            fd.seek(offset)
            if frame := self.process_frame(fd):
                frames.append(frame)
        return frames

    ##############################################################################
    def load_internal_palette(self, fd):
        """Load the palette internal to the image"""
        colour_shift = dread(fd)
        num_colours = dread(fd)
        for colour in range(num_colours):
            alpha = struct.unpack("B", fd.read(1))[0]
            if alpha not in (0, 1):
                print(f"Alpha badness ({alpha}) {fd.name} {colour}")
                continue
            red = struct.unpack("B", fd.read(1))[0]
            green = struct.unpack("B", fd.read(1))[0]
            blue = struct.unpack("B", fd.read(1))[0]
            self.palette[colour + colour_shift] = (red * 4, green * 4, blue * 4)

    ##############################################################################
    def process_frame(self, fd) -> Optional[Frame]:
        """Process the frame data"""
        try:
            frame_indicator = dread(fd)
        except struct.error:
            return None

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
            else:
                x_indent = dread(fd)
                byte_fmt = "<" + "B" * pixels
                try:
                    colour_array = struct.unpack(byte_fmt, fd.read(pixels))
                except struct.error:
                    print(f"{fd.name} Couldn't read colour array")
                    return None
                line = Line(indent=x_indent, pixels=colour_array)
                if pixels % 2:
                    fd.read(1)
            frame.lines.append(line)
        return frame

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
    def save_frame(self, frame: Frame) -> Image:
        """Same frame as an image"""
        image = Image.new("RGBA", (self.width, self.height), (255, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        rel_x = 0
        rel_y = frame.indent

        for line in frame.lines:
            if line.special == LineType.NORMAL:
                rel_x += line.indent
                for x in range(len(line.pixels)):
                    colour = self.palette[line.pixels[x]]
                    draw.point((rel_x + x, rel_y), fill=colour)
            else:
                rel_y += line.indent
                rel_x = 0
        return image


##############################################################################
def load_palette(moo_path: str, fname: str) -> dict[int, tuple[int, int, int]]:
    font_data = load_lbx(moo_path, fname, 1)
    infd = io.BytesIO(font_data)
    palette: dict[int, tuple[int, int, int]] = {}
    for counter in range(256):
        alpha = struct.unpack("B", infd.read(1))[0]
        if alpha not in (0, 1):
            print(f"Alpha badness ({alpha})")
            sys.exit(1)
        red = struct.unpack("B", infd.read(1))[0]
        green = struct.unpack("B", infd.read(1))[0]
        blue = struct.unpack("B", infd.read(1))[0]
        palette[counter] = (red * 4, green * 4, blue * 4)
    return palette


##############################################################################
def dread(fd, format: str = "<H", bytes: int = 2) -> Any:
    return struct.unpack(format, fd.read(bytes))[0]


#####################################################################################################
def load_lbx(moo_path: str, lbx_file: str, lbx_index: int) -> Optional[bytes]:
    """Extract a specific sub-file from and LBX file"""
    fname = os.path.join(moo_path, lbx_file)
    with open(fname, "rb") as infh:
        data = infh.read()
    if data[2] != 0xAD or data[3] != 0xFE or data[4] != 0x00 or data[5] != 0x00:
        print(f"{fname}: Not an LBX file")
        return None
    num_files = struct.unpack("<H", data[:2])[0]
    file_starts = []
    index = 8
    for _ in range(num_files):
        file_starts.append(struct.unpack("<I", data[index : index + 4])[0])
        index += 4
    file_starts.append(struct.unpack("<I", data[index : index + 4])[0])
    return data[file_starts[lbx_index] : file_starts[lbx_index + 1]]


# EOF
