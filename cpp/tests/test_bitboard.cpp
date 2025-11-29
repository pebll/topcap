#define CATCH_CONFIG_MAIN
#include "../include/bitboard.h"
#include "catch.hpp"

using namespace bb; // Use namespace alias for convenience

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

TEST_CASE("neighbourCount counts neighbours correctly", "[bitboard]") {
  // 1100
  // 0000
  // 1000
  // 0100
  Bitboard bitboard = 0b0011'0000'0001'0010;
  int N = 4;
  REQUIRE(neighbourCount(bitboard, {3, 0}, N) == 0);
  REQUIRE(neighbourCount(bitboard, {0, 3}, N) == 1);
  REQUIRE(neighbourCount(bitboard, {0, 2}, N) == 3);
  REQUIRE(neighbourCount(bitboard, {1, 1}, N) == 2);
}
