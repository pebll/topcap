#include "../include/bitboard.h"

int getBit(Bitboard bitboard, int position) {
  return (bitboard & (1ULL << position)) >> position;
}

Bitboard setBit(Bitboard bitboard, int position) {
  return bitboard | (1ULL << position);
}

Bitboard clearBit(Bitboard bitboard, int position) {
  return bitboard & ~(1ULL << position);
}
