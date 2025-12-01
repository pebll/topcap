#include "../include/bitboard.h"
#include "catch.hpp"
#include <vector>

using namespace bb;

TEST_CASE("Coordinates operator== works correctly", "[test_utils]") {
  Coordinates c1 = {1, 2};
  Coordinates c2 = {1, 2};
  Coordinates c3 = {1, 3};
  Coordinates c4 = {2, 2};

  REQUIRE(c1 == c2);
  REQUIRE_FALSE(c1 == c3);
  REQUIRE_FALSE(c1 == c4);
  REQUIRE_FALSE(c3 == c4);
}

TEST_CASE("Move operator== works correctly", "[test_utils]") {
  Move m1 = {{1, 2}, {3, 4}};
  Move m2 = {{1, 2}, {3, 4}};
  Move m3 = {{1, 2}, {3, 5}};
  Move m4 = {{1, 3}, {3, 4}};

  REQUIRE(m1 == m2);
  REQUIRE_FALSE(m1 == m3);
  REQUIRE_FALSE(m1 == m4);
}

TEST_CASE("Coordinates operator+ works correctly", "[test_utils]") {
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

TEST_CASE("Coordinates operator* works correctly", "[test_utils]") {
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

TEST_CASE("Move operator< works correctly for sorting", "[test_utils]") {
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

TEST_CASE("sameSet works correctly", "[test_utils]") {
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
