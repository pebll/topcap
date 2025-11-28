#include "../include/bitboard.h"

int getValue(Bitboard bitboard, int position) {
    return (bitboard & (1ULL << position)) >> position;
}
