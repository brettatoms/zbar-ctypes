from enum import Enum

from ._ctypes import *

fourcc_parse = lambda s: ord(s[0]) | ord(s[1]) << 8 | ord(s[2]) << 16 | ord(s[3]) << 24

class SymbolType(int, Enum):
    NONE = 0  # < no symbol decoded */
    PARTIAL = 1  # < intermediate status */
    EAN2 = 2  # < GS1 2-digit add-on */
    EAN5 = 5  # < GS1 5-digit add-on */
    EAN8 = 8  # < EAN-8 */
    UPCE = 9  # < UPC-E */
    ISBN10 = 10  # < ISBN-10 (from EAN-13). @since 0.4 */
    UPCA = 12  # < UPC-A */
    EAN13 = 13  # < EAN-13 */
    ISBN13 =  14  # < ISBN-13 (from EAN-13). @since 0.4 */
    COMPOSITE = 15  # < EAN/UPC composite */
    I25 = 25  # < Interleaved 2 of 5. @since 0.4 */
    DATABAR = 34  # < GS1 DataBar (RSS). @since 0.11 */
    DATABAR_EXP = 35  # < GS1 DataBar Expanded. @since 0.11 */
    CODABAR = 38  # < Codabar. @since 0.11 */
    CODE39 = 39  # < Code 39. @since 0.4 */
    PDF417 = 57  # < PDF417. @since 0.6 */
    QRCODE = 64  # < QR Code. @since 0.10 */
    CODE93 = 93  # < Code 93. @since 0.11 */
    CODE128 = 128  # < Code 128 */

    #  mask for base symbol type.
    #  @deprecated in 0.11, remove this from existing code
    #
    SYMBOL = 0x00ff
    #  2-digit add-on flag.
    # @deprecated in 0.11, a ::EAN2 component is used for
    # 2-digit GS1 add-ons
    #
    ADDON2 = 0x0200
    #  5-digit add-on flag.
    # @deprecated in 0.11, a ::EAN5 component is used for
    # 5-digit GS1 add-ons
    #
    ADDON5 = 0x0500
    #  add-on flag mask.
    # @deprecated in 0.11, GS1 add-ons are represented using composite
    # symbols of type ::COMPOSITE; add-on components use ::EAN2
    # or ::EAN5
    #
    ADDON = 0x0700


class Config(int, Enum):
    ENABLE = 0            # < enable symbology/feature */
    ADD_CHECK = 1         # < enable check digit when optional */
    EMIT_CHECK = 2       # < return check digit when present */
    ASCII = 3            # < enable full ASCII character set */
    NUM = 4              # < number of boolean decoder configs */
    MIN_LEN = 32         # < minimum data length for valid decode */
    MAX_LEN = 33         # < maximum data length for valid decode */
    UNCERTAINTY = 64     # < required video consistency frames */
    POSITION = 128       # < enable scanner to collect position data */
    X_DENSITY = 256      # < image scanner vertical scan density */
    Y_DENSITY = 257      # < image scanner horizontal scan density */


class Symbol:
    def __init__(self, data):
        self.data


class Image:
    def __init__(self, data=None, width=None, height=None, format=None):
        self.image_ptr = libzbar.zbar_image_create()
        if data:
            self.set_data(data)
        if width and height:
            self.set_size(width, height)
        if format:
            self.set_format(format)

    def set_format(self, format):
        if isinstance(format, str):
            format = fourcc_parse(format)
        libzbar.zbar_image_set_format(self.image_ptr, format)

    def set_size(self, width, height):
        libzbar.zbar_image_set_size(self.image_ptr, width, height)

    def set_data(self, data):
        libzbar.zbar_image_set_data(self.image_ptr, data, len(data), None)

    def get_symbols(self):
        symbols = libzbar.zbar_image_get_symbols(self.image_ptr)
        return symbols

    def __del__(self):
        libzbar.zbar_image_destroy(self.image_ptr)


class ImageScanner:
    def __init__(self):
        self.scanner_ptr = libzbar.zbar_image_scanner_create()

    def set_config(self, symbol, config, value):
        libzbar.zbar_image_scanner_set_config(self.scanner_ptr, int(symbol), int(config),
                                              value)

    def scan(self, data, width, height, format):
        image = Image(data, width, height, format)
        decoded = libzbar.zbar_scan_image(self.scanner_ptr, image.image_ptr)
        if decoded != 1:
            return []

        codes = []
        symbol = libzbar.zbar_image_first_symbol(image.image_ptr)
        while symbol:
            code = libzbar.zbar_symbol_get_data(symbol)
            codes.append(code)
            symbol = libzbar.zbar_symbol_next(symbol)
        return codes


    def scan_pil_image(self, image):
        """
        """
        image = image.convert('L')  # Convert image to gray scale (8 bits per pixel).
        raw = image.tobytes()  # Get image data.
        width, height = image.size  # Get image size.
        return self.scan(raw, width, height, 'Y800')


    def __del__(self):
        libzbar.zbar_image_scanner_destroy(self.scanner_ptr)
