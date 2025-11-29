#ifndef BOARD_H
#define BOARD_H

#include "bitboard.h"
#include <string>

namespace board {

const int STRING_SPACE_LENGTH = 6;

struct Board {
  bitboard::Bitboard white;
  bitboard::Bitboard black;
  int N;
};

inline bool operator==(const Board &lhs, const Board &rhs) {
  return lhs.white == rhs.white && lhs.black == rhs.black;
}

Board initialBoard(int N);
std::string boardToString(Board board);
std::string mStringHeader(int N);

int neighbourCount(Board board, bitboard::Coordinates coords);

} // namespace board

// Namespace alias for convenience
namespace b = board;

#endif // !BOARD_H
