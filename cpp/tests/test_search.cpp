#include "../include/board.h"
#include "../include/search.h"
#include "catch.hpp"
#include <string>
#include <vector>

using namespace board; // Board operations
using namespace types; // Types

// Board of size 4
//         a b c d
//       4 · · ● · 4
//       3 · · · ○ 3
//       2 ○ · · ● 2
//       1 · · · · 1
//         a b c d
//
TEST_CASE("Minimax returns mate in 1", "[board]") {
  bitboard::Bitboard white = 0b0100'0000'1000'0000;
  bitboard::Bitboard black = 0b0000'1000'0001'0000;
  Board board = {white, black, 4, true};
  Move expectedMove = {{2, 3}, {3, 3}};
  Move minimaxMove = search::minimax(board, 1, true);
  REQUIRE(minimaxMove == expectedMove);
}
