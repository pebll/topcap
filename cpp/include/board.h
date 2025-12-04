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
std::string boardToString(const Board &board);
std::string mStringHeader(int N);

int neighbourCount(const Board &board, Coordinates coords);
std::vector<Move> possibleMoves(const Board &board);
bool isMoveLegal(
    const Board &board,
    Move move); // TODO: can i use shorts (1 byte) or smth for coords?
Board makeMove(Board board, Move move);
Board makeMoveInPlace(Board &board, Move move);
std::pair<bool, bool>
terminalState(const Board &board); // (isTerminal, isWinnerWhite)

inline Coordinates colorBaseCoords(const Board &board, bool white) {
  return white ? Coordinates{0, 0} : Coordinates{board.N - 1, board.N - 1};
}

inline Coordinates forbiddenCoords(const Board &board) {
  return colorBaseCoords(board, board.whiteToPlay);
}
} // namespace board

#endif // !BOARD_H
