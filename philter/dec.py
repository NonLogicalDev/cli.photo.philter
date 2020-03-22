import sys
import base64


# Z85MAP = dict([(c, idx) for idx, c in enumerate(Z85CHARS)])
# _85s = [ 85**i for i in range(5) ][::-1]
#
# def decode(z85bytes):
#     """decode Z85 bytes to raw bytes, accepts ASCII string"""
#     if isinstance(z85bytes, str):
#         try:
#             z85bytes = z85bytes.encode('ascii')
#         except UnicodeEncodeError:
#             raise ValueError('string argument should contain only ASCII characters')
#
#     if len(z85bytes) % 5:
#         raise ValueError("Z85 length must be multiple of 5, not %i" % len(z85bytes))
#
#     nvalues = len(z85bytes) / 5
#     values = []
#     for i in range(0, len(z85bytes), 5):
#         value = 0
#         for j, offset in enumerate(_85s):
#             c = z85bytes[i+j]
#             value += Z85MAP[c] * offset
#         values.append(value)
#
#     return struct.pack('>%dI' % nvalues, *values)

Z85CHARSinn = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.-:+=^!`*?'/|()[]{}@%$#\n"
Z85CHARSout = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ~-`+=^!;*?&<>()[]{}@%$#\n"

TR = dict([
    (c, Z85CHARSout[i]) for i, c in enumerate(Z85CHARSinn)
])

if __name__ == '__main__':
    print(TR)
    instr = sys.stdin.read()

    st = ""
    for c in instr:
        st += TR[c]
    print(st[79])
    print(base64.b85decode(st))
