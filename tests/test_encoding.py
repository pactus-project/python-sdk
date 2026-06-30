import unittest

from pactus.encoding.encoding import (
    append_uint8,
    append_uint16,
    append_uint32,
    append_str,
    append_var_int,
    read_uint8,
    read_uint16,
    read_uint32,
    read_str,
    read_var_int,
)


class TestEncoding(unittest.TestCase):
    def test_uint8(self):
        tests = [
            (0x00, b"\x00"),
            (0x55, b"\x55"),
            (0xFF, b"\xff"),
        ]

        for _, (value, expected_bytes) in enumerate(tests):
            buf = b""
            buf = append_uint8(buf, value)
            self.assertEqual(buf, expected_bytes)

            read, buf = read_uint8(buf)
            self.assertEqual(read, value)
            self.assertEqual(len(buf), 0)

    def test_uint16(self):
        tests = [
            (0x0000, b"\x00\x00"),
            (0x5050, b"\x50\x50"),
            (0x0505, b"\x05\x05"),
            (0x1234, b"\x34\x12"),
            (0xFFFF, b"\xff\xff"),
        ]

        for _, (value, expected_bytes) in enumerate(tests):
            buf = b""
            buf = append_uint16(buf, value)
            self.assertEqual(buf, expected_bytes)

            read, buf = read_uint16(buf)
            self.assertEqual(read, value)
            self.assertEqual(len(buf), 0)

    def test_uint32(self):
        tests = [
            (0x00000000, b"\x00\x00\x00\x00"),
            (0x50505050, b"\x50\x50\x50\x50"),
            (0x05050505, b"\x05\x05\x05\x05"),
            (0x12345678, b"\x78\x56\x34\x12"),
            (0xFFFFFFFF, b"\xff\xff\xff\xff"),
        ]

        for _, (value, expected_bytes) in enumerate(tests):
            buf = b""
            buf = append_uint32(buf, value)
            self.assertEqual(buf, expected_bytes)

            read, buf = read_uint32(buf)
            self.assertEqual(read, value)
            self.assertEqual(len(buf), 0)

    def test_var_int(self):
        tests = [
            (0x0, b"\x00"),
            (0xFF, b"\xff\x01"),
            (0x7FFF, b"\xff\xff\x01"),
            (0x3FFFFF, b"\xff\xff\xff\x01"),
            (0x1FFFFFFF, b"\xff\xff\xff\xff\x01"),
            (0xFFFFFFFFF, b"\xff\xff\xff\xff\xff\x01"),
            (0x7FFFFFFFFFF, b"\xff\xff\xff\xff\xff\xff\x01"),
            (0x3FFFFFFFFFFFF, b"\xff\xff\xff\xff\xff\xff\xff\x01"),
            (0x1FFFFFFFFFFFFFF, b"\xff\xff\xff\xff\xff\xff\xff\xff\x01"),
            (0xFFFFFFFFFFFFFFFF, b"\xff\xff\xff\xff\xff\xff\xff\xff\xff\x01"),
            (0x200, b"\x80\x04"),
            (0x027F, b"\xff\x04"),
            (0xFF00000000, b"\x80\x80\x80\x80\xf0\x1f"),
            (0xFFFFFFFF, b"\xff\xff\xff\xff\x0f"),
            (0x100000000, b"\x80\x80\x80\x80\x10"),
            (0x7FFFFFFFF, b"\xff\xff\xff\xff\x7f"),
            (0x800000000, b"\x80\x80\x80\x80\x80\x01"),
        ]

        for i, (value, expected_bytes) in enumerate(tests):
            buf = b""
            buf = append_var_int(buf, value)
            self.assertEqual(buf, expected_bytes)

            read, buf = read_var_int(buf)
            self.assertEqual(read, value)
            self.assertEqual(len(buf), 0)

    def test_str(self):
        # str256 is a string that takes a 2-byte varint to encode.
        str256 = "test" * 64

        tests = [
            ("", b"\x00"),
            ("Test", b"\x04Test"),
            (str256, b"\x80\x02" + str256.encode("utf-8")),
        ]

        for i, (value, expected_bytes) in enumerate(tests):
            buf = b""
            buf = append_str(buf, value)
            self.assertEqual(buf, expected_bytes)

            read, buf = read_str(buf)
            self.assertEqual(read, value)
            self.assertEqual(len(buf), 0)


if __name__ == "__main__":
    unittest.main()
