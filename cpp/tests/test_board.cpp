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

TEST_CASE("Neighbour count works", "[board]") {
  Board board = initialBoard(6);
  REQUIRE(neighbourCount(board, {0, 0}) == 0);
  REQUIRE(neighbourCount(board, {3, 2}) == 2);
  REQUIRE(neighbourCount(board, {1, 3}) == 2);
  REQUIRE(neighbourCount(board, {3, 0}) == 1);
}

#ifndef TEST_ALL

// Board of size 4
//         a b c d
//       4 · · ○ · 4
//       3 · · · ○ 3
//       2 ● · · · 2
//       1 · ● · · 1
//         a b c d

TEST_CASE("moveIsValid works correctly", "[board]"){... maybe put into bitboard}

TEST_CASE("Piece Move generation works", "[board]") {
  ... maybe put into bitboard Board board = initialBoard(4);
  REQUIRE(piecePossibleMoves(board, {0, 0}) == EMPTY_LIST); // no piece here
  REQUIRE(piecePossibleMoves(board, {1, 0}) == LIST_OF_3)
}

TEST_CASE("Full Move generation works", "[board]") {
  Board board = initialBoard(4);
  REQUIRE(possibleMoves(board, true) == 0);
}

#endif // TEST_ALL
