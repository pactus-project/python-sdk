import unittest

from pactus.encoding.encoding import (
    append_str,
    append_var_int,
)


class TestEncoding(unittest.TestCase):
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
            self.assertEqual(buf, expected_bytes, f"WriteVarInt test {i}")

    def test_var_string_encoding(self):
        # str256 is a string that takes a 2-byte varint to encode.
        str256 = "test" * 64

        tests = [
            ("", b"\x00"),
            ("Test", b"\x04Test"),
            (str256, b"\x80\x02" + str256.encode("utf-8")),
        ]

        for i, (value, expected_bytes) in enumerate(tests):
            with self.subTest(i=i):
                buf = bytearray()
                append_str(buf, value)
                self.assertEqual(buf, expected_bytes, f"append_str #{i}")


if __name__ == "__main__":
    unittest.main()
