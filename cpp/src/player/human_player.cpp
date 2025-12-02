#include "../../include/player/human_player.h"
#include "../../include/board.h"
#include "../../include/utils.h"
#include <iostream>
#include <string>

using namespace types;

namespace player {

Move Human::getMove(const Board &board) {
  while (true) {
    std::cout << "Enter your move (e.g., 'a1 a2'): ";
    std::string moveStr;
    std::getline(std::cin, moveStr);

    Move move = parseMove(moveStr);
    if (move.from.x >= 0 && move.from.y >= 0 && move.to.x >= 0 &&
        move.to.y >= 0 && board::isMoveLegal(board, move)) {
      return move;
    }
    std::cout << "Please try again." << std::endl;
    std::cout << "Available moves: " << board::possibleMoves(board)
              << std::endl;
  }
}

Move Human::parseMove(const std::string &moveStr) {
  std::string trimmed = moveStr;
  // Remove leading whitespace
  size_t start = trimmed.find_first_not_of(" \t");
  if (start != std::string::npos) {
    trimmed = trimmed.substr(start);
  }
  // Remove trailing whitespace
  size_t end = trimmed.find_last_not_of(" \t");
  if (end != std::string::npos) {
    trimmed = trimmed.substr(0, end + 1);
  }

  if (trimmed.length() < 4) {
    return {{-1, -1}, {-1, -1}}; // Invalid move marker
  }

  // Parse format: "a1 a2" or "a1a2"
  std::string fromTile, toTile;

  if (trimmed.length() == 5 && trimmed[2] == ' ') {
    // Format: "a1 a2"
    fromTile = trimmed.substr(0, 2);
    toTile = trimmed.substr(3, 2);
  } else if (trimmed.length() == 4) {
    // Format: "a1a2"
    fromTile = trimmed.substr(0, 2);
    toTile = trimmed.substr(2, 2);
  } else {
    return {{-1, -1}, {-1, -1}}; // Invalid move marker
  }

  Coordinates from = utils::tileToCoords(fromTile);
  Coordinates to = utils::tileToCoords(toTile);

  return {from, to};
}

} // namespace player
