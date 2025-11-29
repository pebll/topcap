#include "../include/bitboard.h"
#include <cassert>

namespace bitboard {

int getBit(Bitboard bitboard, int position) {
  assert(position >= 0 && position < 64);
  return (bitboard & (1ULL << position)) >> position;
}

int getBit(Bitboard bitboard, Coordinates coords, int N) {
  int position = coordsToPosition(coords, N);
  return getBit(bitboard, position);
}

Bitboard setBit(Bitboard bitboard, int position) {
  assert(position >= 0 && position < 64);
  return bitboard | (1ULL << position);
}

Bitboard setBit(Bitboard bitboard, Coordinates coords, int N) {
  int position = coordsToPosition(coords, N);
  return setBit(bitboard, position);
}

Bitboard clearBit(Bitboard bitboard, int position) {
  assert(position >= 0 && position < 64);
  return bitboard & ~(1ULL << position);
}

Bitboard clearBit(Bitboard bitboard, Coordinates coords, int N) {
  int position = coordsToPosition(coords, N);
  return clearBit(bitboard, position);
}

int coordsToPosition(Coordinates coords, int N) {
  assert(N >= 4 && N <= 8);
  assert(coords.x >= 0 && coords.x < N);
  assert(coords.y >= 0 && coords.y < N);
  return coords.x + coords.y * N;
}

Coordinates positionToCoords(int position, int N) {
  assert(N >= 4 && N <= 8);
  assert(position >= 0 && position < N * N);
  Coordinates coords = {position % N, position / N};
  return coords;
}

int neighbourCount(Bitboard bitboard, Coordinates coords, int N) {
  int count = 0;
  int x = coords.x, y = coords.y;
  count += (x < N - 1) && getBit(bitboard, {x + 1, y}, N);
  count += (x > 0) && getBit(bitboard, {x - 1, y}, N);
  count += (y < N - 1) && getBit(bitboard, {x, y + 1}, N);
  count += (y > 0) && getBit(bitboard, {x, y - 1}, N);
  count += (x < N - 1 && y < N - 1) && getBit(bitboard, {x + 1, y + 1}, N);
  count += (x > 0 && y < N - 1) && getBit(bitboard, {x - 1, y + 1}, N);
  count += (x > 0 && y > 0) && getBit(bitboard, {x - 1, y - 1}, N);
  count += (x < N - 1 && y > 0) && getBit(bitboard, {x + 1, y - 1}, N);
  return count;
}

} // namespace bitboard
