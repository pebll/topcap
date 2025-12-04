#include "../include/utils.h"
#include <cassert>

using namespace types;

namespace utils {

Coordinates tileToCoords(const std::string &tile) {
  assert(tile.length() >= 2);
  char col = tile[0];
  std::string rowStr = tile.substr(1);

  int x = col - 'a';
  int y = std::stoi(rowStr) - 1; // Convert from 1-indexed to 0-indexed

  return {x, y};
}

std::string coordsToTile(const Coordinates &coords) {
  char col = 'a' + coords.x;
  int row = coords.y + 1; // Convert from 0-indexed to 1-indexed

  return std::string(1, col) + std::to_string(row);
}

} // namespace utils
