#ifndef BOARD_H
#define BOARD_H

#include "bitboard.h"
#include "types.h"
#include <string>
#include <vector>

namespace board {

using Bitboard = types::Bitboard;
using Coordinates = types::Coordinates;
using Move = types::Move;
using Board = types::Board;

const int STRING_SPACE_LENGTH = 6;

Board initialBoard(int N);
std::string boardToString(Board board);
std::string mStringHeader(int N);

int neighbourCount(Board board, Coordinates coords);
std::vector<Move> possibleMoves(Board board, bool whiteToPlay);
Board makeMove(Board board, Move move);

} // namespace board

#endif // !BOARD_H
