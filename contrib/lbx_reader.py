#!/usr/bin/env python
""" Open and pull out stuff from LBX files """

import os.path
import struct
import sys


##############################################################################
def main():
    """Do the stuff"""
    for fname in sys.argv[1:]:
        with open(fname, "rb") as infh:
            data = infh.read()
        sfname = os.path.basename(fname)
        print(f"Processing {sfname}")
        try:
            if data[2] != 0xAD or data[3] != 0xFE or data[4] != 0x00 or data[5] != 0x00:
                print("No an LBX file")
                continue
        except (struct.error, IndexError):
            print("Definitely not an LBX file")
            continue
        num_files = struct.unpack("<H", data[0:2])[0]
        print(f"{num_files=}")
        file_starts = []
        index = 8
        for fnum in range(num_files):
            file_starts.append(struct.unpack("<I", data[index : index + 4])[0])
            index += 4
        file_starts.append(struct.unpack("<I", data[index : index + 4])[0])
        print(f"{file_starts=}")
        for fnum, start_index in enumerate(file_starts[:-1]):
            print(f"{fnum=} {start_index=}")
            print(f"{file_starts[fnum]=} {file_starts[fnum+1]=}")
            file_data = data[file_starts[fnum] : file_starts[fnum + 1]]
            with open(f"{sfname}_{fnum}", "wb") as outfh:
                outfh.write(file_data)


##############################################################################
if __name__ == "__main__":
    main()

# EOF
