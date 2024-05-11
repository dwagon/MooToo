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
            alpha = struct.unpack("B", infd.read(1))[0]
            if alpha not in (0, 1):
                sys.exit(1)
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
    palette: dict[int, tuple[int, int, int]] = field(default_factory=dict)
    frames: list[Frame] = field(default_factory=list)

    ##############################################################################
    def load(self, fd, palette) -> None:
        """Process the filename"""
        try:
            self.width = dread(fd)
        except struct.error:
            raise UserWarning("Empty file")
        self.height = dread(fd)
        self.palette = palette
        _ = fd.read(2)  # Nothing in the next two chars

        self.num_frames = dread(fd)
        self.delay = dread(fd)
        self.flags = self.image_flags(dread(fd))
        print(f"{fd.name}: {self.width} x {self.height} frames={self.num_frames} {self.flags}")
        frame_offsets = []
        try:
            for _ in range(self.num_frames + 1):
                offset = dread(fd, "<L", 4)
                frame_offsets.append(offset)
        except struct.error:
            raise UserWarning("Not an image file")
        if self.flags["internal"]:
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
        for offset in frame_offsets[:-1]:
            fd.seek(offset)
            if frame := self.process_frame(fd):
                self.frames.append(frame)

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
    def save_frame(self, filename: str, frame: int = 0) -> None:
        """Same frame as an image"""
        try:
            f = self.frames[frame]
        except IndexError:
            print(f"{filename}: Unknown frame {frame}")
            return
        image = Image.new("RGBA", (self.width, self.height), (255, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        rel_x = 0
        rel_y = f.indent

        for line in f.lines:
            if line.special == LineType.NORMAL:
                rel_x += line.indent
                for x in range(len(line.pixels)):
                    colour = self.palette[line.pixels[x]]
                    draw.point((rel_x + x, rel_y), fill=colour)
            else:
                rel_y += line.indent
                rel_x = 0
        with open(filename, "wb") as outfh:
            image.save(outfh, "PNG")


##############################################################################
def dread(fd, format: str = "<H", bytes: int = 2) -> Any:
    return struct.unpack(format, fd.read(bytes))[0]


##############################################################################
def main() -> None:
    """Do the stuff"""
    palettes = ["FONTS.LBX_1"]
    # palettes = [f"FONTS.LBX_{_}" for _ in range(1, 14)] + [f"IFONTS.LBX_{_}" for _ in range(1, 4)]
    for num, palfile in enumerate(palettes):
        palette = load_palette(palfile)
        for filename in sys.argv[1:]:
            try:
                g = Graphic()
                with open(filename, "rb") as fd:
                    try:
                        g.load(fd, palette.copy())
                    except UserWarning:
                        continue
                if g.frames:
                    dirname = os.path.basename(os.path.splitext(filename)[0])
                    suffix = os.path.basename(os.path.splitext(filename)[1]).replace(".", "")
                    try:
                        os.mkdir(dirname)
                    except IOError:
                        pass
                    for frame in range(g.num_frames):
                        save_file = f"{dirname}/{dirname}_{suffix}_{g.width}x{g.height}_f{frame}_p{num}.png"
                        g.save_frame(save_file, frame=frame)
            except Exception as exc:
                print(f"Failure on {filename}: {exc}")
                raise


##############################################################################
if __name__ == "__main__":
    main()

# EOF
