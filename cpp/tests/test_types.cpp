#include "../include/types.h"
#include "catch.hpp"
#include <vector>

using namespace types;

TEST_CASE("Coordinates operator== works correctly", "[test_types]") {
  Coordinates c1 = {1, 2};
  Coordinates c2 = {1, 2};
  Coordinates c3 = {1, 3};
  Coordinates c4 = {2, 2};

  REQUIRE(c1 == c2);
  REQUIRE_FALSE(c1 == c3);
  REQUIRE_FALSE(c1 == c4);
  REQUIRE_FALSE(c3 == c4);
}

TEST_CASE("Move operator== works correctly", "[test_types]") {
  Move m1 = {{1, 2}, {3, 4}};
  Move m2 = {{1, 2}, {3, 4}};
  Move m3 = {{1, 2}, {3, 5}};
  Move m4 = {{1, 3}, {3, 4}};

  REQUIRE(m1 == m2);
  REQUIRE_FALSE(m1 == m3);
  REQUIRE_FALSE(m1 == m4);
}

TEST_CASE("Coordinates operator+ works correctly", "[test_types]") {
  Coordinates c1 = {1, 2};
  Coordinates c2 = {3, 4};
  Coordinates result = c1 + c2;

  REQUIRE(result.x == 4);
  REQUIRE(result.y == 6);

  Coordinates c3 = {-1, 5};
  Coordinates c4 = {2, -3};
  Coordinates result2 = c3 + c4;

  REQUIRE(result2.x == 1);
  REQUIRE(result2.y == 2);
}

TEST_CASE("Coordinates operator* works correctly", "[test_types]") {
  Coordinates c1 = {2, 3};
  Coordinates result = c1 * 2;

  REQUIRE(result.x == 4);
  REQUIRE(result.y == 6);

  Coordinates c2 = {-1, 5};
  Coordinates result2 = c2 * 3;

  REQUIRE(result2.x == -3);
  REQUIRE(result2.y == 15);

  Coordinates result3 = c1 * 0;
  REQUIRE(result3.x == 0);
  REQUIRE(result3.y == 0);
}

TEST_CASE("Move operator< works correctly for sorting", "[test_types]") {
  Move m1 = {{0, 0}, {1, 1}};
  Move m2 = {{0, 0}, {1, 2}};
  Move m3 = {{0, 1}, {1, 1}};
  Move m4 = {{1, 0}, {1, 1}};
  Move m5 = {{0, 0}, {1, 1}}; // Same as m1

  REQUIRE(m1 < m2);       // Same from, different to.y
  REQUIRE(m1 < m3);       // Different from.y
  REQUIRE(m1 < m4);       // Different from.x
  REQUIRE_FALSE(m1 < m5); // Equal moves
  REQUIRE_FALSE(m5 < m1); // Equal moves (both ways)
}

TEST_CASE("sameSet works correctly", "[test_types]") {
  std::vector<Move> v1 = {{{1, 0}, {2, 0}}, {{0, 1}, {0, 2}}};
  std::vector<Move> v2 = {{{0, 1}, {0, 2}},
                          {{1, 0}, {2, 0}}}; // Same, different order
  std::vector<Move> v3 = {{{1, 0}, {2, 0}}}; // Different size
  std::vector<Move> v4 = {{{1, 0}, {2, 0}}, {{0, 1}, {0, 3}}}; // Different move
  std::vector<Move> v5 = {};                                   // Empty

  REQUIRE(sameSet(v1, v2));       // Same elements, different order
  REQUIRE_FALSE(sameSet(v1, v3)); // Different sizes
  REQUIRE_FALSE(sameSet(v1, v4)); // Different elements
  REQUIRE(sameSet(v5, {}));       // Both empty
  REQUIRE_FALSE(sameSet(v1, v5)); // One empty, one not
}

TEST_CASE("Board operator== works correctly", "[test_types]") {
  Board board1 = {0b1001, 0b0110, 4, true};
  Board board2 = {0b1001, 0b0110, 4, true};
  Board board3 = {0b1001, 0b0110, 5, true};  // Different N
  Board board4 = {0b1000, 0b0110, 4, true};  // Different white
  Board board5 = {0b1001, 0b0100, 4, true};  // Different black
  Board board6 = {0b1001, 0b0110, 4, false}; // Different whiteToPlay

  REQUIRE(board1 == board2);
  REQUIRE_FALSE(board1 == board3); // Different N
  REQUIRE_FALSE(board1 == board4); // Different white
  REQUIRE_FALSE(board1 == board5); // Different black
  REQUIRE_FALSE(board1 == board6); // Different whiteToPlay
}

TEST_CASE("getCurrentColorBitboard returns correct bitboard", "[test_types]") {
  Bitboard white = 0b1001;
  Bitboard black = 0b0110;
  Board boardWTP = {white, black, 4, true};
  Board boardBTP = {white, black, 4, false};

  REQUIRE(getCurrentColorBitboard(boardWTP) == white);
  REQUIRE(getCurrentColorBitboard(boardBTP) == black);
}

TEST_CASE("getTotalBitboard returns correct bitboard", "[test_types]") {
  Bitboard white = 0b1001;
  Bitboard black = 0b0110;
  Board board = {white, black, 4, true};
  REQUIRE(getTotalBitboard(board) == 0b1111);
}
