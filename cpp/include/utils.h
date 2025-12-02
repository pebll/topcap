#ifndef UTILS_H
#define UTILS_H

#include "types.h"
#include <string>

namespace utils {

// Convert tile string (e.g., "a1") to Coordinates
// "a1" -> {0, 0}, "b2" -> {1, 1}, etc.
types::Coordinates tileToCoords(const std::string& tile);

} // namespace utils

#endif // UTILS_H
