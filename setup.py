try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'name': 'zbar-ctypes',
    'description': 'Python wrapper for the ZBar barcode scanner library.',
    'author': 'Brett',
    'url': 'http://github.com/brettatoms/zbar-ctypes',
    'download_url': 'https://github.com/brettatoms/zbar-ctypes.',
    'author_email': 'brettatoms@gmail.comMy email.',
    'version': '0.1',
    'license': 'MIT',
    'packages': ['zbar'],
    'scripts': [],
    'keywords': ['barcode', 'zbar', 'zxing', 'upc', 'qr'],
    'classifiers': [
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Multimedia :: Graphics :: Capture :: Scanners',
        'Topic :: Scientific/Engineering :: Image Recognition',


        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ]
}

setup(**config)
