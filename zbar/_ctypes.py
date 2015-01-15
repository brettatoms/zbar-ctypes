from ctypes import *
import sys

if sys.platform == 'darwin':
    libzbar = cdll.LoadLibrary('libzbar.dylib')
else:
    libzbar = cdll.LoadLibrary('libzbar.so.0')

refcnt_t = c_long

class rs_gf256(Structure):
    _fields_ = [
        ('log', c_ubyte * 256),
        ('exp', c_ubyte * 511)
    ]

class point_t(Structure):
    _fields_ = [
        ('x', c_int),
        ('y', c_int)
    ]

class zbar_orientation_t(Structure):
    pass

qr_point = c_int

class qr_finder_line(Structure):
    _fields_ = [
        ('pos', qr_point * 2),
        ('len', c_int),
        ('boffs', c_int),
        ('eoffs', c_int)
    ]

class zbar_decoder_t(Structure):
    # NOTE: We haven't filled this out b/c we don't need a pointer to it
    pass

class zbar_scanner_t(Structure):
    _fields_ = [
        ('decoder', POINTER(zbar_decoder_t)),
        ('y1_min_thresh', c_uint),
        ('x', c_uint),
        ('y0', c_uint * 4),
        ('y1_sign', c_int),
        ('y1_thresh', c_uint),
        ('cur_edge', c_uint),
        ('last_edge', c_uint),
        ('width', c_uint),
    ]

ISAAC_SZ_LOG = 8

class isaac_ctx(Structure):
    _fields_ = [
        ('n', c_uint),
        ('r', c_uint * ISAAC_SZ_LOG),
        ('m', c_uint * ISAAC_SZ_LOG),
        ('a', c_uint),
        ('b', c_uint),
        ('c', c_uint),
    ]

class qr_reader(Structure):
    _fields_ = [
        ('gf', rs_gf256),
        ('isaac', isaac_ctx),
        ('finder_lines', qr_finder_line * 2)

    ]

class zbar_image_scanner_t(Structure):
    pass
    # _fields_ = [
    #     ('zbar_scanner_t', POINTER(zbar_scanner_t)),
    #     ('zbar_decoder_t', POINTER(zbar_decoder_t)),
    #     ('qr_reader', POINTER(qr_reader))
    # ]

zbar_symbol_type_t = c_int
zbar_config_t = c_int
errmodule_t = c_int
errsev_t = c_int
zbar_error_t = c_int

class errinfo_t(Structure):
    _fields_ = [
        ('magic', c_uint32),
        ('module', errmodule_t),
        ('buf', c_char_p),
        ('errnum', c_int),
        ('sev', errsev_t),
        ('type', zbar_error_t),
        ('func', c_char_p),
        ('detail', c_char_p),
        ('arg_str', c_char_p),
        ('arg_int', c_int)
    ]

class zbar_mutex_t(Structure):
    # NOTE: This is a placehold for a forward reference
    pass

class zbar_mutex_t(Structure):
    _fields_ = [
        ('count', c_int),
        ('mutex', zbar_mutex_t)
    ]

HANDLE = c_void_p
HWND = HANDLE
pthread_t = c_ulong
zbar_thread_id_t = pthread_t


class zbar_event_t(Structure):
    # NOTE: We haven't filled this out b/c we don't need a pointer to it
    pass


class zbar_thread_t(Structure):
    _fields_ = [
        ('tid', zbar_thread_id_t),
        ('started', c_int),
        ('running', c_int),
        ('notify', zbar_event_t),
        ('activity', zbar_event_t),
    ]

class BITMAPINFOHEADER(Structure):
    _fields_ = [
        ('biSize', c_uint32),
        ('biWidth', c_int),
        ('biHeight', c_int),
        ('biPlanes', c_short),
        ('biBitCount', c_short),
        ('biCompression', c_uint32),
        ('biSizeImage', c_uint32),
        ('biXPelsPerMeter', c_long),
        ('biYPelsPerMeter', c_long),
        ('biClrUsed', c_uint32),
        ('biClrImportant', c_uint32)
    ]

class zbar_symbol_t(Structure):
    # NOTE: This is a placehold for a forward reference
    pass

class zbar_symbol_set_t(Structure):
    _fields_ = [
        ('refcnt', refcnt_t),
        ('nsyms', c_int),
        ('head', POINTER(zbar_symbol_t)),
        ('tail', POINTER(zbar_symbol_t))
    ]

class zbar_symbol_t(Structure):
    _fields_ = [
        ('type', zbar_symbol_type_t),
        ('configs', c_uint),
        ('modifiers', c_uint),
        ('data_alloc', c_uint),
        ('datalen', c_uint),
        ('data', c_char_p),
        ('pts_alloc', c_uint),
        ('npts', c_uint),
        ('pts', POINTER(point_t)),
        ('orient', zbar_orientation_t),
        ('refcnt', refcnt_t),
        ('next', POINTER(zbar_symbol_t)),
        ('syms', POINTER(zbar_symbol_set_t)),
        ('time', c_ulong),
        ('cache_cout', c_int),
        ('quality', c_int)
    ]

class zbar_image_t(Structure):
    # NOTE: This is a placehold for a forward reference
    pass

# TODO: I'm not real sure this is correct
# typedef void (zbar_image_cleanup_handler_t)(zbar_image_t *image);
zbar_image_cleanup_handler_t = CFUNCTYPE(POINTER(zbar_image_t))

class video_state_t(Structure):
    _fields_ = [
        ('thread', zbar_thread_t),
        ('captured', HANDLE),
        ('hwnd', HWND),
        ('notify', HANDLE),
        ('bi_size', c_int),
        ('bih', BITMAPINFOHEADER),
        ('image', POINTER(zbar_image_t))
    ]

video_interface_t = c_int
video_iomode_t = c_int

class zbar_video_t(Structure):
    _fields_ = [
        ('err', errinfo_t),
        ('fd', c_int),
        ('width', c_uint),
        ('height', c_uint),
        ('intf', video_interface_t),
        ('iomode', video_iomode_t), #
        ('initialized', c_uint, 1),
        ('active', c_uint, 1),
        ('format', c_uint32),
        ('palette', c_uint),
        ('formats', POINTER(c_uint32)),
        ('datalen', c_ulong),
        ('buflen', c_ulong),
        ('buf', c_void_p),
        ('frame', c_uint),
        ('qlock', zbar_mutex_t),
        ('num_images', c_int),
        ('images', POINTER(POINTER(zbar_image_t))),
        ('nq_image', POINTER(zbar_image_t)),
        ('dq_image', POINTER(zbar_image_t)),
        ('shadow_image', POINTER(zbar_image_t)),
        ('state', POINTER(video_state_t))
    ]

class zbar_image_t(Structure):
    _fields_ = [
        ('format', c_uint32),
        ('width', c_uint),
        ('height', c_uint),
        ('data', c_void_p),
        ('datalen', c_ulong),
        ('crop_x', c_uint),
        ('crop_y', c_uint),
        ('crop_w', c_uint),
        ('crop_h', c_uint),
        ('userdata', c_void_p),
        ('cleanup', POINTER(zbar_image_cleanup_handler_t)),
        ('refcnt', refcnt_t),
        ('src', POINTER(zbar_video_t)),
        ('srcidx', c_int),
        ('next', POINTER(zbar_image_t)),
        ('seq', c_uint),
        ('syms', POINTER(zbar_symbol_set_t))
    ]


# zbar_image_scanner_t *zbar_image_scanner_create();
libzbar.zbar_image_scanner_create.restype = POINTER(zbar_image_scanner_t)

# void zbar_image_scanner_destroy (zbar_image_scanner_t *iscn);
libzbar.zbar_image_scanner_destroy.argtypes = [POINTER(zbar_image_scanner_t)]

# int zbar_image_scanner_set_config (zbar_image_scanner_t *iscn,
#                                    zbar_symbol_type_t sym,
#                                    zbar_config_t cfg,
#                                    int val);
libzbar.zbar_image_scanner_set_config.argtypes = [POINTER(zbar_image_scanner_t),
                                          zbar_symbol_type_t, zbar_config_t, c_int]

# zbar_image_t *zbar_image_create(void);
libzbar.zbar_image_create.restype = POINTER(zbar_image_t)

# void zbar_image_destroy(zbar_image_t *image);
libzbar.zbar_image_destroy.argtypes = [POINTER(zbar_image_t)]

# void zbar_image_set_format(zbar_image_t *image, unsigned long format);
libzbar.zbar_image_set_format.argtypes = [POINTER(zbar_image_t), c_ulong]

# void zbar_image_set_size(zbar_image_t *image, unsigned width, unsigned height);
libzbar.zbar_image_set_size.argtypes = [POINTER(zbar_image_t), c_uint, c_uint]

# void zbar_image_set_data(zbar_image_t *image, const void *data,
#                          unsigned long data_byte_length,
#                          zbar_image_cleanup_handler_t *cleanup_hndlr);
libzbar.zbar_image_set_data.argtypes = [POINTER(zbar_image_t), c_void_p, c_ulong,
                                        POINTER(zbar_image_cleanup_handler_t)]


libzbar.zbar_scan_image.argtypes = (POINTER(zbar_image_scanner_t), POINTER(zbar_image_t))
libzbar.zbar_scan_image.restype = c_int

libzbar.zbar_image_first_symbol.argtypes = [POINTER(zbar_image_t)]
libzbar.zbar_image_first_symbol.restype = POINTER(zbar_symbol_t)

libzbar.zbar_symbol_get_data.argtypes = [POINTER(zbar_symbol_t)]
libzbar.zbar_symbol_get_data.restype = c_char_p

# const zbar_symbol_set_t *zbar_image_get_symbols (const zbar_image_t *img)
libzbar.zbar_image_get_symbols.argtypes = [POINTER(zbar_image_t)]
libzbar.zbar_image_get_symbols.restype = POINTER(zbar_symbol_set_t)

# unsigned int zbar_symbol_get_data_length(const zbar_symbol_t *symbol)
libzbar.zbar_symbol_get_data_length.argtypes = [POINTER(zbar_symbol_t)]
libzbar.zbar_symbol_get_data_length.restype = c_uint

# const char *zbar_symbol_get_data(const zbar_symbol_t *symbol);
libzbar.zbar_symbol_get_data.argtypes = [POINTER(zbar_symbol_t)]
libzbar.zbar_symbol_get_data.restype = c_char_p
