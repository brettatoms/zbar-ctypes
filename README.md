# ZBar

The zbar-ctypes package is a wrapper around the ZBar barcode scanner library.

** This package is for Python 3 only. **

### Scanning a PIL Image
```
import zbar
scanner = zbar.ImageScanner()
# disable qr code scanning (all symbol formats on by default)
scanner.set_config(zbar.SymbolType.QRCODE, zbar.Config.ENABLE, 0)
image = Image.open(path)
codes = scanner.scan_pil_image(image)
```
