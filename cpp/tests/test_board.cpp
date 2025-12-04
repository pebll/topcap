#include "../include/board.h"
#include "catch.hpp"
#include <string>
#include <vector>

using namespace board; // Board operations
using namespace types; // Types

#define TEST_ALL

TEST_CASE("initialBoard gives correct initial states", "[board]") {
  Bitboard white4 = 0b0000'0000'0001'0010;
  Bitboard black4 = 0b0100'1000'0000'0000;
  REQUIRE(initialBoard(4).bitboards[0] == white4);
  REQUIRE(initialBoard(4).bitboards[1] == black4);
  REQUIRE(initialBoard(4).N == 4);

  Bitboard white5 = 0b00000'00000'00001'00010'00100;
  Bitboard black5 = 0b00100'01000'10000'00000'00000;
  REQUIRE(initialBoard(5).bitboards[0] == white5);
  REQUIRE(initialBoard(5).bitboards[1] == black5);
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

// Board of size 4
//         a b c d
//       4 · · ○ · 4
//       3 · · · ○ 3
//       2 ● · · · 2
//       1 · ● · · 1
//         a b c d

TEST_CASE("Initial 4x4 possibleMoves works", "[board]") {
  Board board = initialBoard(4);
  std::vector<Move> whitePossibleMoves = {
      {{1, 0}, {2, 0}}, {{1, 0}, {1, 1}}, {{0, 1}, {0, 2}}, {{0, 1}, {1, 1}}};
  REQUIRE(sameSet(possibleMoves(board), whitePossibleMoves));
}

TEST_CASE("forbiddenCoords works", "[board]") {
  Board board5 = initialBoard(5);
  Board board8 = initialBoard(8);
  REQUIRE(forbiddenCoords(board5) == Coordinates{0, 0});
  REQUIRE(forbiddenCoords(board8) == Coordinates{0, 0});
  board5.whiteToPlay = false;
  board8.whiteToPlay = false;
  REQUIRE(forbiddenCoords(board5) == Coordinates{4, 4});
  REQUIRE(forbiddenCoords(board8) == Coordinates{7, 7});
}

// Board of size 4
//         a b c d
//       4 · · ○ · 4
//       3 · · ● ○ 3
//       2 ○ · · ● 2
//       1 · ● · · 1
//         a b c d

TEST_CASE("Complex 4x4 possibleMoves works", "[board]") {
  bitboard::Bitboard white = 0b0000'0100'1000'0010;
  bitboard::Bitboard black = 0b0100'1000'0001'0000;
  Board boardWhiteToPlay = Board(white, black, 4, true);
  Board boardBlackToPlay = Board(white, black, 4, false);
  std::vector<Move> whitePossibleMoves = {
      {{1, 0}, {1, 1}}, {{1, 0}, {2, 0}}, {{3, 1}, {1, 1}}};
  std::vector<Move> blackPossibleMoves = {
      {{0, 1}, {0, 0}}, {{0, 1}, {1, 1}}, {{0, 1}, {0, 2}}, {{2, 3}, {0, 3}}};
  REQUIRE(sameSet(possibleMoves(boardWhiteToPlay), whitePossibleMoves));
  REQUIRE(sameSet(possibleMoves(boardBlackToPlay), blackPossibleMoves));
}

TEST_CASE("isMoveLegal works") {
  bitboard::Bitboard white = 0b0000'0100'1000'0010;
  bitboard::Bitboard black = 0b0100'1000'0001'0000;
  Board boardWhiteToPlay = Board(white, black, 4, true);
  REQUIRE(isMoveLegal(boardWhiteToPlay, {{1, 0}, {1, 1}}));
  REQUIRE_FALSE(isMoveLegal(boardWhiteToPlay, {{2, 0}, {1, 0}}));
  REQUIRE(isMoveLegal(boardWhiteToPlay, {{3, 1}, {1, 1}}));
  REQUIRE_FALSE(isMoveLegal(boardWhiteToPlay, {{0, 1}, {2, 1}}));
  REQUIRE_FALSE(isMoveLegal(boardWhiteToPlay, {{0, 1}, {1, 1}}));
  REQUIRE_FALSE(isMoveLegal(boardWhiteToPlay, {{2, 3}, {0, 3}}));
  Board boardBlackToPlay = Board(white, black, 4, false);
  REQUIRE_FALSE(isMoveLegal(boardBlackToPlay, {{1, 0}, {1, 1}}));
  REQUIRE_FALSE(isMoveLegal(boardBlackToPlay, {{2, 0}, {1, 0}}));
  REQUIRE_FALSE(isMoveLegal(boardBlackToPlay, {{3, 1}, {1, 1}}));
  REQUIRE_FALSE(isMoveLegal(boardBlackToPlay, {{0, 1}, {2, 1}}));
  REQUIRE(isMoveLegal(boardBlackToPlay, {{0, 1}, {1, 1}}));
  REQUIRE(isMoveLegal(boardBlackToPlay, {{2, 3}, {0, 3}}));
}

// Board of size 4
//         a b c d
//       4 · · ○ · 4
//       3 · · ● ○ 3
//       2 ○ · · ● 2
//       1 · ● · · 1
//         a b c d

TEST_CASE("board::makeMove works") {
  bitboard::Bitboard white = 0b0000'0100'1000'0010;
  bitboard::Bitboard black = 0b0100'1000'0001'0000;
  Board boardWTP = Board(white, black, 4, true);
  REQUIRE(makeMove(boardWTP, {{1, 0}, {1, 1}}).bitboards[0] == 0b0000'0100'1010'0000);
  REQUIRE(makeMove(boardWTP, {{1, 0}, {1, 1}}).bitboards[1] == black);
  REQUIRE(makeMove(boardWTP, {{1, 0}, {1, 1}}).whiteToPlay == false);
  Board boardBTP = Board(white, black, 4, false);
  REQUIRE(makeMove(boardBTP, {{0, 1}, {0, 0}}).bitboards[0] == white);
  REQUIRE(makeMove(boardBTP, {{0, 1}, {0, 0}}).bitboards[1] == 0b0100'1000'0000'0001);
  REQUIRE(makeMove(boardBTP, {{0, 1}, {0, 0}}).whiteToPlay == true);
}

// Board of size 4
//         a b c d
//       4 · · ○ · 4
//       3 · · ● ○ 3
//       2 ○ · · ● 2
//       1 · ● · · 1
//         a b c d

TEST_CASE("isTerminal & isWinnerWhite detects base Reached", "[board]") {
  bitboard::Bitboard white = 0b0000'0100'1000'0010;
  bitboard::Bitboard blackNotReached = 0b0100'1000'0001'0000;
  bitboard::Bitboard blackReached = 0b0100'1000'0000'0001;
  Board boardNotReached = Board(white, blackNotReached, 4, true);
  Board boardReached = Board(white, blackReached, 4, true);
  REQUIRE_FALSE(terminalState(boardNotReached).first);
  REQUIRE(terminalState(boardReached).first);
  REQUIRE_FALSE(terminalState(boardReached).second);
}

// Board of size 4
//         a b c d
//       4 · ● ○ · 4
//       3 · · ● ○ 3
//       2 ○ · · ● 2
//       1 · · · · 1
//         a b c d

TEST_CASE("isTerminal & isWinnerWhite detects no moves left", "[board]") {
  bitboard::Bitboard white = 0b0010'0100'1000'0000;
  bitboard::Bitboard black = 0b0100'1000'0001'0000;
  Board boardWTP = Board(white, black, 4, true);
  Board boardBTP = Board(white, black, 4, false);
  REQUIRE_FALSE(terminalState(boardWTP).first);
  REQUIRE(terminalState(boardBTP).first);
  REQUIRE(terminalState(boardBTP).second);
}

#ifndef TEST_ALL
#endif // TEST_ALL
