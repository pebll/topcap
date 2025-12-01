#include "../include/bitboard.h"
#include <cassert>
#include <cstdlib>
#include <vector>

using namespace types;

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

std::vector<int> getPositions(Bitboard bitboard) {
  std::vector<int> positions;
  positions.reserve(8); // reserve for biggest possible N
  Bitboard temp = bitboard;
  while (temp) {
    int pos = __builtin_ctzll(temp); // calculates position of first 1
    positions.push_back(pos);
    temp &= temp - 1; // clear last 1 bit
  }
  return positions;
}

bool isPathBlocked(Bitboard bitboard, Move move, int N) {
  // TODO: optimize by using bit masks
  int dx = (move.to.x - move.from.x) /
           std::max(1, std::abs(move.to.x - move.from.x));
  int dy = (move.to.y - move.from.y) /
           std::max(1, std::abs(move.to.y - move.from.y));
  for (int x = move.from.x + dx, y = move.from.y + dy;
       x - dx != move.to.x || y - dy != move.to.y; x += dx, y += dy) {
    if (getBit(bitboard, {x, y}, N)) {
      return true;
    }
  }
  return false;
}

bool isMoveFeasible(Bitboard bitboard, Move move, int N) {
  // TODO: create a Optim variant that does only game-relevant checks assuming
  // that no bugs exist (for example do not check for diagonal as this should
  // not happen)

  // in bounds
  if (move.from.x < 0 || move.from.x >= N || move.from.y < 0 ||
      move.from.y >= N || move.to.x < 0 || move.to.x >= N || move.to.y < 0 ||
      move.to.y >= N) {
    return false;
  }
  // from empty
  if (!getBit(bitboard, move.from, N)) {
    return false;
  }
  // path diagonal or same
  if (!(move.from.x != move.to.x) ^ (move.from.y != move.to.y)) {
    return false;
  }
  // path blocked
  return !isPathBlocked(bitboard, move, N);
}

std::vector<Move> possibleMovesFrom(Bitboard bitboard, Coordinates coords,
                                    Coordinates forbiddenCoords, int N) {
  std::vector<Move> moves;
  moves.reserve(4);
  int moveDistance = neighbourCount(bitboard, coords, N);
  const Coordinates DIRECTIONS[] = {{-1, 0}, {0, 1}, {1, 0}, {0, -1}};
  for (const Coordinates &direction : DIRECTIONS) {
    Coordinates toCoords = coords + (direction * moveDistance);
    Move move = {coords, toCoords};
    if (!(toCoords == forbiddenCoords) && isMoveFeasible(bitboard, move, N)) {
      moves.push_back(move);
    }
  }
  return moves;
}

} // namespace bitboard
