import os
import platform
import ctypes


def load_library():
    print('Loading C functions.')
    platform_system = platform.system()
    lib_name = None

    # Retrieves the appropriate library for your system
    if platform_system.upper() == 'WINDOWS':
        lib_name = 'list_moves_windows.dll'
    elif platform_system.upper() == 'DARWIN':
        lib_name = 'list_moves_macos.so'
    elif platform_system.upper() == 'LINUX':
        lib_name = 'list_moves_linux.so'
    else:
        raise Exception('Couldn\'t find the appropriate C library for your system: {}.'.format(platform_system))

    lib_path = os.path.join(os.getcwd(), 'lib', lib_name)
    library = ctypes.CDLL(lib_path)
    return library


# Called when the file gets imported
LIB = load_library()


def list_moves_c(entities_matrix, cols, rows, is_black):
    moves = [-1 for _ in range(cols * rows * 4)]
    entities_arr = (ctypes.c_char * len(entities_matrix))(*entities_matrix)
    moves_arr = (ctypes.c_int32 * len(moves))(*moves)

    LIB.list_moves(entities_arr, moves_arr, is_black, cols, rows)

    moves = list(moves_arr)
    return moves

