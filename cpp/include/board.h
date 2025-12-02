#ifndef BOARD_H
#define BOARD_H

#include "bitboard.h"
#include "types.h"
#include <string>
#include <utility>
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
std::vector<Move> possibleMoves(Board board);
Coordinates forbiddenCoords(Board board);
bool isMoveLegal(Board board, Move move);
Board makeMove(Board board, Move move);
std::pair<bool, bool> terminalState(Board board); // (isTerminal, isWinnerWhite)

} // namespace board

#endif // !BOARD_H
