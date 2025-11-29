#include "../include/bitboard.h"
#include <cassert>

int getBit(Bitboard bitboard, int position) {
  assert(position >= 0 && position < 64);
  return (bitboard & (1ULL << position)) >> position;
}

Bitboard setBit(Bitboard bitboard, int position) {
  assert(position >= 0 && position < 64);
  return bitboard | (1ULL << position);
}

Bitboard clearBit(Bitboard bitboard, int position) {
  assert(position >= 0 && position < 64);
  return bitboard & ~(1ULL << position);
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
