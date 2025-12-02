#ifndef UTILS_H
#define UTILS_H

#include "types.h"
#include <string>

namespace utils {

// Convert tile string (e.g., "a1") to Coordinates
// "a1" -> {0, 0}, "b2" -> {1, 1}, etc.
types::Coordinates tileToCoords(const std::string& tile);

// Convert Coordinates to tile string
// {0, 0} -> "a1", {1, 1} -> "b2", etc.
std::string coordsToTile(const types::Coordinates& coords, int N);

} // namespace utils

#endif // UTILS_H
