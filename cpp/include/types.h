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
  Bitboard white;
  Bitboard black;
  int N;
};

inline bool operator==(const Coordinates &lhs, const Coordinates &rhs) {
  return lhs.x == rhs.x && lhs.y == rhs.y;
}

inline bool operator==(const Move &lhs, const Move &rhs) {
  return lhs.to == rhs.to && lhs.from == rhs.from;
}

inline bool operator==(const Board &lhs, const Board &rhs) {
  return lhs.white == rhs.white && lhs.black == rhs.black;
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

inline Bitboard getBitboard(const Board &board, const bool isWhite) {
  return isWhite ? board.white : board.black;
}

} // namespace types

#endif // !TYPES_H
