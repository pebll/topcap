#ifndef BITBOARD_H
#define BITBOARD_H

#include <algorithm>
#include <cstdint>
#include <iostream>
#include <vector>

namespace bitboard {

using Bitboard = uint64_t;

struct Coordinates {
  int x;
  int y;
};

struct Move {
  Coordinates from;
  Coordinates to;
};

inline bool operator==(const Coordinates &lhs, const Coordinates &rhs) {
  return lhs.x == rhs.x && lhs.y == rhs.y;
}

inline bool operator==(const Move &lhs, const Move &rhs) {
  return lhs.to == rhs.to && lhs.from == rhs.from;
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
  std::sort(lshSorted.begin(), lshSorted.end());
  return lshSorted == lshSorted;
}

// bitboard operations
int getBit(Bitboard bitboard, int position);
Bitboard setBit(Bitboard bitboard, int position);
Bitboard clearBit(Bitboard bitboard, int position);
int getBit(Bitboard bitboard, Coordinates coords, int N);
Bitboard setBit(Bitboard bitboard, Coordinates coords, int N);
Bitboard clearBit(Bitboard bitboard, Coordinates coords, int N);

// coords & position operations
int coordsToPosition(Coordinates coords, int N);
Coordinates positionToCoords(int position, int N);

// utility functions
int neighbourCount(Bitboard bitboard, Coordinates coords, int N);
std::vector<int> getPositions(Bitboard bitboard);
bool isMoveFeasible(Bitboard bitboard, Move move, int N);
// ^ only checks bounds and if is not blocked
bool isPathBlocked(Bitboard bitboard, Move move, int N);
// forbiddenPosition is the own base (white can't move into white base!)
std::vector<Move> possibleMovesFrom(Bitboard bitboard, Coordinates coords,
                                    Coordinates forbiddenCoords, int N);

} // namespace bitboard

// Namespace alias for convenience
namespace bb = bitboard;

#endif // !BITBOARD_H
