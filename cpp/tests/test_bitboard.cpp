#define CATCH_CONFIG_MAIN
#include "../include/bitboard.h"
#include "catch.hpp"
#include <algorithm>
#include <vector>

using namespace bitboard; // Bitboard operations
using namespace types; // Types

TEST_CASE("getBit returns correct bit", "[bitboard]") {
  Bitboard board = 0b1001;

  REQUIRE(getBit(board, 0) == 1);
  REQUIRE(getBit(board, 1) == 0);
  REQUIRE(getBit(board, 2) == 0);
  REQUIRE(getBit(board, 3) == 1);
}

TEST_CASE("setBit correctly sets bit", "[bitboard]") {
  Bitboard board = 0b1001;

  REQUIRE(setBit(board, 0) == 0b1001);
  REQUIRE(setBit(board, 1) == 0b1011);
  REQUIRE(setBit(board, 2) == 0b1101);
  REQUIRE(setBit(board, 3) == 0b1001);
  // Chaining
  REQUIRE(setBit(setBit(board, 1), 2) == 0b1111);
}

TEST_CASE("clearBit correctly clears bit", "[bitboard]") {
  Bitboard board = 0b1001;

  REQUIRE(clearBit(board, 0) == 0b1000);
  REQUIRE(clearBit(board, 1) == 0b1001);
  REQUIRE(clearBit(board, 2) == 0b1001);
  REQUIRE(clearBit(board, 3) == 0b0001);
  // Chaining
  REQUIRE(clearBit(clearBit(board, 0), 3) == 0b0000);
}

TEST_CASE("coordsToPosition works correctly", "[bitboard]") {
  Coordinates coords02 = {0, 2};
  REQUIRE(coordsToPosition(coords02, 4) == 8);
  REQUIRE(coordsToPosition(coords02, 5) == 10);
  Coordinates coords44 = {4, 4};
  REQUIRE(coordsToPosition(coords44, 5) == 24);
  // Out of bounds for N = 4, should not happen
  // coordsToPosition(coords44, 4); -> ERROR
}

TEST_CASE("positionToCoords works correctly", "[bitboard]") {
  Coordinates coords02 = {0, 2};
  REQUIRE(positionToCoords(8, 4) == coords02);
  REQUIRE(positionToCoords(10, 5) == coords02);
  Coordinates coords44 = {4, 4};
  REQUIRE(positionToCoords(24, 5) == coords44);
  // Out of bounds for N = 4, should not happen
  // positionToCoords(24, 4) -> ERROR
}

// Board of size 4 (A)
//             a b c d
//   1100    4 ● ● · · 4
//   0000    3 · · · · 3
//   1000    2 ● · · · 2
//   0100    1 · ● · · 1
//             a b c d
//
TEST_CASE("neighbourCount counts neighbours correctly", "[bitboard]") {
  Bitboard bitboard = 0b0011'0000'0001'0010;
  int N = 4;
  REQUIRE(neighbourCount(bitboard, {3, 0}, N) == 0);
  REQUIRE(neighbourCount(bitboard, {0, 3}, N) == 1);
  REQUIRE(neighbourCount(bitboard, {0, 2}, N) == 3);
  REQUIRE(neighbourCount(bitboard, {1, 1}, N) == 2);
}

TEST_CASE("getPositions extracts positions correctly", "[bitboard]") {
  Bitboard bitboard = 0b0011'0000'0001'0010;
  std::vector<int> positions = {1, 4, 12, 13};
  REQUIRE(getPositions(bitboard) == positions);
  std::vector<int> empty = {};
  REQUIRE(getPositions(0) == empty);
}

// Board of size 4
//             a b c d
//   1100    4 ● ● · · 4
//   0110    3 · ● ● · 3
//   1100    2 ● ● · · 2
//   0100    1 · ● · · 1
//             a b c d
//
TEST_CASE("isPathBlocked works correctly", "[bitboard]") {
  Bitboard bitboard = 0b0011'0110'0011'0010;
  int N = 4;
  REQUIRE(isPathBlocked(bitboard, {{1, 0}, {3, 0}}, N) == false);
  REQUIRE(isPathBlocked(bitboard, {{3, 0}, {1, 0}}, N) == true);
  REQUIRE(isPathBlocked(bitboard, {{1, 0}, {1, 3}}, N) == true);
}

TEST_CASE("isMoveFeasible works correctly", "[bitboard]") {
  // This checks only for out of bounds and blocked path
  // NOT for correct move distance or if target is base!
  // (because this acts on the bitboard level, who is unaware of such things)
  Bitboard bitboard = 0b0011'0110'0011'0010;
  int N = 4;
  // ok move distance 1
  REQUIRE(isMoveFeasible(bitboard, {{0, 1}, {0, 2}}, N) == true);
  // target in occupied
  REQUIRE(isMoveFeasible(bitboard, {{0, 1}, {1, 1}}, N) == false);
  // from is not occupied
  REQUIRE(isMoveFeasible(bitboard, {{0, 0}, {0, 1}}, N) == false);
  // target out of bounds
  REQUIRE(isMoveFeasible(bitboard, {{0, 1}, {-1, 1}}, N) == false);
  // from is out of bounds
  REQUIRE(isMoveFeasible(bitboard, {{-1, 1}, {0, 1}}, N) == false);
  // diagonal path
  REQUIRE(isMoveFeasible(bitboard, {{1, 0}, {2, 1}}, N) == false);
  // from and to are same
  REQUIRE(isMoveFeasible(bitboard, {{0, 0}, {0, 0}}, N) == false);
  // ok move distance 2
  REQUIRE(isMoveFeasible(bitboard, {{1, 1}, {3, 1}}, N) == true);
  // blocked path
  REQUIRE(isMoveFeasible(bitboard, {{1, 2}, {3, 2}}, N) == false);
}

// Board of size 4 (B)
//             a b c d
//   1100    4 ● ● · · 4
//   0000    3 · · · · 3
//   1100    2 ● ● · · 2
//   0100    1 · ● · · 1
//             a b c d
//
TEST_CASE("possibleMovesFrom works", "[bitboard]") {
  Bitboard bitboardB = 0b0011'0000'0011'0010;
  Coordinates blackBase = {3, 3};
  int N = 4;
  std::vector<Move> from11 = {{{1, 1}, {3, 1}}};
  std::vector<Move> from10 = {{{1, 0}, {3, 0}}};
  std::vector<Move> from13 = {{{1, 3}, {1, 2}}, {{1, 3}, {2, 3}}};
  REQUIRE(sameSet(possibleMovesFrom(bitboardB, {1, 1}, blackBase, N), from11));
  REQUIRE(sameSet(possibleMovesFrom(bitboardB, {0, 1}, blackBase, N), {}));
  REQUIRE(sameSet(possibleMovesFrom(bitboardB, {1, 0}, blackBase, N), from10));
  REQUIRE(sameSet(possibleMovesFrom(bitboardB, {1, 3}, blackBase, N), from13));
  REQUIRE(sameSet(possibleMovesFrom(bitboardB, {2, 1}, blackBase, N), {}));
}

// Board of size 4 (A)
//             a b c d
//   1100    4 ● ● · · 4
//   0000    3 · · · · 3
//   1000    2 ● · · · 2
//   0100    1 · ● · · 1
//             a b c d
//
TEST_CASE(
    "possibleMovesFrom prevents from moving into forbidden position (own base)",
    "[bitboard]") {
  Bitboard bitboardA = 0b0011'0000'0001'0010;
  int N = 4;
  std::vector<Move> forbidden00 = {{{1, 0}, {2, 0}}, {{1, 0}, {1, 1}}};
  std::vector<Move> forbidden33 = {
      {{1, 0}, {2, 0}}, {{1, 0}, {1, 1}}, {{1, 0}, {0, 0}}};
  REQUIRE(
      sameSet(possibleMovesFrom(bitboardA, {1, 0}, {0, 0}, N), forbidden00));
  REQUIRE(
      sameSet(possibleMovesFrom(bitboardA, {1, 0}, {3, 3}, N), forbidden33));
}
