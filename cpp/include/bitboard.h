#ifndef BITBOARD_H
#define BITBOARD_H

#include "types.h"

namespace bitboard {

using Bitboard = types::Bitboard;
using Coordinates = types::Coordinates;
using Move = types::Move;

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

#endif // !BITBOARD_H
