#include <stdio.h>
#include <iostream>
#include <vector>

typedef unsigned char uchar; 

#ifdef _WIN32
#define DLLEXP __declspec(dllexport)
#else
#define DLLEXP
#endif

int delta_moves[] = {1, 0, -1, 0, 0, 1, 0, -1, 1, 1, -1, 1, 1, -1, -1, -1};

struct Queen {
    int x = 0;
    int y = 0;
};

enum Piece {
	IS_QUEEN = 1,
	IS_BLACK = 2
};

bool are_same_team(char piece_1, char piece_2)
{
	return ((piece_1 & Piece::IS_BLACK) == (piece_2 & Piece::IS_BLACK));
}

float distance(int x_1, int y_1, int x_2, int y_2)
{
    return sqrt((x_2 - x_1) * (x_2 - x_1) + (y_2 - y_1) * (y_2 - y_1));
}

extern "C" DLLEXP int test_array(char* array)
{
	array[0] = 1;
	array[1] = 2;
	array[2] = 4;
	array[3] = 8;
	array[4] = 16;
	array[5] = 32;
	array[6] = 64;
	array[7] = 127;
	return 0;
}

extern "C" DLLEXP int list_moves(char* board, int* moves_ptr, bool is_black, int width, int height)
{
 	std::vector<int> moves;
 	Queen black_queen;
 	Queen white_queen;

 	// search for queen
 	for (int y = 0; y < height; y++) {
        for (int x = 0; x < width; x++) {
            char piece = board[y * width + x];
            if ((piece != 64) && (piece & Piece::IS_QUEEN)) {
                if (piece & Piece::IS_BLACK) {
                    black_queen.x = x;
                    black_queen.y = y;
                }
                else {
                    white_queen.x = x;
                    white_queen.y = y;
                }
            }
        }
 	}

	for (int y = 0; y < height; y++) {
		for (int x = 0; x < width; x++) {
			// get piece at cell
			char piece = board[y * width + x];
			if (piece != 64 && (is_black == ((piece & Piece::IS_BLACK) >> 1))) {
			    // retrieve enemy queen
			    Queen* enemy_queen = nullptr;
                if (piece & IS_BLACK) {
                    enemy_queen = &(white_queen);
                }
                else {
                    enemy_queen = &(black_queen);
                }

				for (int i = 0; i < 8; i++) {
					int shift_x = delta_moves[2 * i];
					int shift_y = delta_moves[2 * i + 1];
					int _x = x;
					int _y = y;

					_x += shift_x;
					_y += shift_y;
					while (_x >= 0 && _x < width && _y >= 0 && _y < height) {
                        // monkey cannot move further from enemy queen
					    if (!(piece & IS_QUEEN)) {
                            float old_distance = distance(x, y, enemy_queen->x, enemy_queen->y);
                            float new_distance = distance(_x, _y, enemy_queen->x, enemy_queen->y);
                            if (new_distance >= old_distance) {
                                break; //TODO check this out, I'm 99% sure, but might cause trouble if wrong
                            }
					    }

						char other_piece = board[_y * width + _x];
						if (other_piece != 64) {
							if (!are_same_team(piece, other_piece)) {
                                moves.push_back(x);
                                moves.push_back(y);
								moves.push_back(_x);
								moves.push_back(_y);
							}
							break;
						}
						else {
						    moves.push_back(x);
						    moves.push_back(y);
							moves.push_back(_x);
							moves.push_back(_y);
							_x += shift_x;
							_y += shift_y;
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