#include "catch.hpp"

#include "../include/bitboard.h"

TEST_CASE("getValue returns correct bit", "[bitboard]") {
  Bitboard board = 0b1001;

  REQUIRE(getValue(board, 0) == 1);
  REQUIRE(getValue(board, 1) == 0);
  REQUIRE(getValue(board, 2) == 0);
  REQUIRE(getValue(board, 3) == 1);
}
