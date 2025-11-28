#ifndef BOARD_H
#define BOARD_H

#include "bitboard.h"

struct Board {
  Bitboard white;
  Bitboard black;
};

inline bool operator==(const Board &lhs, const Board &rhs) {
  return lhs.white == rhs.white && lhs.black == rhs.black;
}

Board initialBoard(int N);

#endif // !BOARD_H
