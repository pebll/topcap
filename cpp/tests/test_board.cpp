#include "../include/board.h"
#include "catch.hpp"

#define TEST_ALL

TEST_CASE("initialBoard gives correct initial states", "[board]") {
  // y
  // -  -  B  -  -
  // -  -  -  B  -
  // W  -  -  -  B
  // -  W  -  -  -
  // -  -  W  -  -  x
  //
  Bitboard white4 = 0b0000'0000'0001'0010;
  Bitboard black4 = 0b0100'1000'0000'0000;
  REQUIRE(initialBoard(4).white == white4);
  REQUIRE(initialBoard(4).black == black4);

  Bitboard white5 = 0b00000'00000'00001'00010'00100;
  Bitboard black5 = 0b00100'01000'10000'00000'00000;
  REQUIRE(initialBoard(5).white == white5);
  REQUIRE(initialBoard(5).black == black5);
}

#ifndef TEST_ALL
TEST_CASE("printBoard prints correct string", "[board]") {
  // Test multiple sizes
  REQUIRE(true);
}

#endif // TEST_ALL
