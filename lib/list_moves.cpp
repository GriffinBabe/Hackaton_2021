#include <iostream>
#include <vector>

typedef unsigned char uchar; 

#ifdef _WIN32
#define DLLEXP __declspec(dllexport)
#else
#define DLLEXP
#endif

int delta_moves[] = {1, 0, -1, 0, 0, 1, 0, -1, 1, 1, -1, 1, 1, -1, -1, -1};

enum Piece {
	IS_QUEEN = 1,
	IS_BLACK = 2
};

bool are_same_team(uchar piece_1, uchar piece_2)
{
	return ((piece_1 & Piece::IS_BLACK) == (piece_2 & Piece::IS_BLACK));
}

extern "C" DLLEXP int test_array(uchar* array)
{
	array[0] = 1;
	array[1] = 2;
	array[2] = 4;
	array[3] = 8;
	array[4] = 16;
	array[5] = 32;
	array[6] = 64;
	array[7] = 128;
	return 0;
}

extern "C" DLLEXP int list_moves(uchar* board, int* moves_ptr, bool is_black, int width, int height)
{
	std::vector<int> moves;

	for (int y = 0; y < height; y++) {
		for (int x = 0; x < width; x++) {
			// get piece at cell
			uchar piece = board[y * width + x];
			std::cout << "Piece " << piece << " found in x: " << x << " y: " << y << std::endl;

			if (piece != 0 && (is_black == (piece & IS_BLACK))) {
				std::cout << "Entering search " << std::endl;

				for (int i = 0; i < 8; i++) {
					int shift_x = delta_moves[2 * i];
					int shift_y = delta_moves[2 * i + 1];
					int _x = x;
					int _y = y;

					_x += shift_x;
					_y += shift_y;
					while (_x >= 0 && _x < width && _y >= 0 && _y < height) {
						uchar other_piece = board[_y * width + _x];
						if (other_piece == 0) {
							moves.push_back(_x);
							moves.push_back(_y);
							_x += shift_x;
							_y += shift_y;
						}
						else {
							if (!are_same_team(piece, other_piece)) {
								moves.push_back(_x);
								moves.push_back(_y);
							}
							break;
						}
					}
				}

			}
		}
	}

	for (int idx = 0; idx < moves.size(); idx++) {
		moves_ptr[idx] = moves[idx];
	}

	return 0;
}