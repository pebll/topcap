#define CATCH_CONFIG_MAIN
#include "../include/bitboard.h"
#include "catch.hpp"

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
