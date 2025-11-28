#ifndef BITBOARD_H
#define BITBOARD_H

#include <cstdint>

using Bitboard = uint64_t;

int getBit(Bitboard bitboard, int position);
Bitboard setBit(Bitboard bitboard, int position);
Bitboard clearBit(Bitboard bitboard, int position);

#endif // !BITBOARD_H
