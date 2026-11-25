"""Independent checks of the submitted program and the PNG it produces."""
import os
from pathlib import Path
import struct
import subprocess
import tempfile
import unittest
import zlib

ROOT = Path(__file__).resolve().parent


class EntryTest(unittest.TestCase):
    def test_png_is_complete_and_reproducible(self):
        runs = []
        for _ in range(2):
            with tempfile.TemporaryDirectory() as directory:
                output = Path(directory) / 'output'
                result = subprocess.run(['node', str(ROOT / 'main.ts')],
                                        cwd=directory, capture_output=True,
                                        env={**os.environ, 'MAKEFUN_OUTPUT_DIR': str(output)},
                                        timeout=5)
                self.assertEqual(result.returncode, 0, result.stderr.decode())
                self.assertEqual([p.name for p in output.iterdir()], ['entry.png'])
                runs.append((output / 'entry.png').read_bytes())
        self.assertEqual(*runs)
        png = runs[0]
        self.assertLessEqual(len(png), 1_048_576)
        self.assertEqual(png[:8], b'\x89PNG\r\n\x1a\n')
        offset, kinds, pixels = 8, [], bytearray()
        while offset < len(png):
            length, kind = struct.unpack_from('>I4s', png, offset)
            end = offset + 8 + length
            data = png[offset + 8:end]
            checksum, = struct.unpack_from('>I', png, end)
            self.assertEqual(checksum, zlib.crc32(kind + data))
            kinds.append(kind)
            if kind == b'IHDR':
                self.assertEqual(struct.unpack('>IIBBBBB', data), (1024, 1024, 8, 2, 0, 0, 0))
            if kind == b'IDAT':
                pixels.extend(data)
            offset = end + 4
        self.assertEqual(kinds[0], b'IHDR')
        self.assertEqual(kinds[-1], b'IEND')
        self.assertEqual(offset, len(png))
        decoder = zlib.decompressobj()
        raster = decoder.decompress(pixels) + decoder.flush()
        self.assertTrue(decoder.eof)
        self.assertFalse(decoder.unused_data)
        stride = 1 + 3 * 1024
        self.assertEqual(len(raster), stride * 1024)
        self.assertTrue(all(value < 5 for value in raster[::stride]))


if __name__ == '__main__':
    unittest.main()
