#ifndef TYPES_H
#define TYPES_H

#include <algorithm>
#include <cstdint>
#include <iostream>
#include <vector>

namespace types {

using Bitboard = uint64_t;

struct Coordinates {
  int x;
  int y;
};

struct Move {
  Coordinates from;
  Coordinates to;
};

struct Board {
  Bitboard bitboards[2];
  int N;
  bool whiteToPlay;
  mutable std::vector<Move> possibleMovesCache;
  mutable bool possibleMovesValid;

  Board(Bitboard w, Bitboard b, int n, bool wtp)
      : bitboards{w, b}, N(n), whiteToPlay(wtp), possibleMovesValid(false) {}
};

inline bool operator==(const Coordinates &lhs, const Coordinates &rhs) {
  return lhs.x == rhs.x && lhs.y == rhs.y;
}

inline bool operator==(const Move &lhs, const Move &rhs) {
  return lhs.to == rhs.to && lhs.from == rhs.from;
}

inline bool operator==(const Board &lhs, const Board &rhs) {
  return lhs.bitboards[0] == rhs.bitboards[0] &&
         lhs.bitboards[1] == rhs.bitboards[1] && lhs.N == rhs.N &&
         lhs.whiteToPlay == rhs.whiteToPlay;
}

inline Coordinates operator+(const Coordinates &lhs, const Coordinates &rhs) {
  return {lhs.x + rhs.x, lhs.y + rhs.y};
}

inline Coordinates operator*(const Coordinates &coords, const int &scalar) {
  return {coords.x * scalar, coords.y * scalar};
}

// for Catch2 printing
inline std::ostream &operator<<(std::ostream &os, const Move &move) {
  return os << "{{" << move.from.x << "," << move.from.y << "}, {" << move.to.x
            << "," << move.to.y << "}}";
}

// for sorting
inline bool operator<(const Move &lhs, const Move &rhs) {
  if (lhs.from.x != rhs.from.x)
    return lhs.from.x < rhs.from.x;
  if (lhs.from.y != rhs.from.y)
    return lhs.from.y < rhs.from.y;
  if (lhs.to.x != rhs.to.x)
    return lhs.to.x < rhs.to.x;
  return lhs.to.y < rhs.to.y;
}

inline bool sameSet(const std::vector<Move> &lhs,
                    const std::vector<Move> &rhs) {
  std::vector<Move> lshSorted = lhs;
  std::vector<Move> rshSorted = rhs;
  std::sort(lshSorted.begin(), lshSorted.end());
  std::sort(rshSorted.begin(), rshSorted.end());
  return lshSorted == rshSorted;
}

inline Bitboard getColorBitboard(const Board &board, bool white) {
  return board.bitboards[!white];
}

inline Bitboard getCurrentColorBitboard(const Board &board) {
  return getColorBitboard(board, board.whiteToPlay);
}

inline Bitboard getNextColorBitboard(const Board &board) {
  return getColorBitboard(board, !board.whiteToPlay);
}

inline void setColorBitboardInPlace(Board &board, bool white,
                                    Bitboard bitboard) {
  board.bitboards[!white] = bitboard;
}

inline Bitboard getTotalBitboard(const Board &board) {
  return board.bitboards[0] | board.bitboards[1];
}

} // namespace types

#endif // !TYPES_H
