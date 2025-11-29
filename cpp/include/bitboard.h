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

int getBit(Bitboard bitboard, int position);
Bitboard setBit(Bitboard bitboard, int position);
Bitboard clearBit(Bitboard bitboard, int position);

int coordsToPosition(Coordinates coords, int N);
Coordinates positionToCoords(int position, int N);

} // namespace bitboard

// Namespace alias for convenience
namespace bb = bitboard;

#endif // !BITBOARD_H
