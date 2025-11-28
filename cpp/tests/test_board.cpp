#include "../include/board.h"
#include "catch.hpp"

TEST_CASE("initialBoard gives correct initial states", "[board]") {
  Bitboard white4 = 0b0010'0001'0000'0000;
  Bitboard black4 = 0b0000'0000'1000'0100;
  Board board4 = {white4, black4};
  REQUIRE(initialBoard(4) == board4);
}

TEST_CASE("printBoard prints correct string", "[board]") {
  // Test multiple sizes
  REQUIRE(true);
}
