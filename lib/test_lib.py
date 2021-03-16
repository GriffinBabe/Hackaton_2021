import ctypes, os

lib_path = os.path.join(os.getcwd(), 'list_moves_windows.dll')
lib = ctypes.CDLL(lib_path)

board = bytes([ 1, 0, 0, 0 ])
width = 2
height = 2
is_black = False
moves = [ -1 for _ in range(2 * 4) ]

print(board)

board_arr = (ctypes.c_char * len(board))(*board)
moves_arr = (ctypes.c_int * len(moves))(*moves)

print(lib.list_moves(board_arr, moves_arr, is_black, width, height))

moves = list(moves_arr)
print(moves)
