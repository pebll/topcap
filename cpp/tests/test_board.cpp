#include "../include/board.h"
#include "catch.hpp"
#include <string>

using namespace b;  // Use namespace alias for convenience
using namespace bb; // Also need bitboard types

#define TEST_ALL

TEST_CASE("initialBoard gives correct initial states", "[board]") {
  Bitboard white4 = 0b0000'0000'0001'0010;
  Bitboard black4 = 0b0100'1000'0000'0000;
  REQUIRE(initialBoard(4).white == white4);
  REQUIRE(initialBoard(4).black == black4);
  REQUIRE(initialBoard(4).N == 4);

  Bitboard white5 = 0b00000'00000'00001'00010'00100;
  Bitboard black5 = 0b00100'01000'10000'00000'00000;
  REQUIRE(initialBoard(5).white == white5);
  REQUIRE(initialBoard(5).black == black5);
  REQUIRE(initialBoard(7).N == 7);
}

TEST_CASE("printBoard prints correct string", "[board]") {
  // Test multiple sizes and multiple positions
  std::string string6 = "        a b c d e f "
                        "\n      6 · · ○ · · · 6"
                        "\n      5 · · · ○ · · 5"
                        "\n      4 ● · · · ○ · 4"
                        "\n      3 · ● · · · ○ 3"
                        "\n      2 · · ● · · · 2"
                        "\n      1 · · · ● · · 1"
                        "\n        a b c d e f \n";
  REQUIRE(boardToString(initialBoard(6)) == string6);
}

#ifndef TEST_ALL

#endif // TEST_ALL
