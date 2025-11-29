#ifndef BITBOARD_H
#define BITBOARD_H

#include <cstdint>

namespace bitboard {

using Bitboard = uint64_t;

struct Coordinates {
  int x;
  int y;
};

inline bool operator==(const Coordinates &lhs, const Coordinates &rhs) {
  return lhs.x == rhs.x && lhs.x == rhs.x;
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

} // namespace bitboard

// Namespace alias for convenience
namespace bb = bitboard;

#endif // !BITBOARD_H
