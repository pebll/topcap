#include "../../include/player/minimax_v1_basic_player.h"
#include "../../include/board.h"
#include "../../include/search.h"
#include <random>
#include <vector>

using namespace types;

namespace player {

Move MinimaxV1::getMove(const Board &board) {
  // Use board.whiteToPlay to determine if we should maximize (white) or
  // minimize (black)
  return search::minimax(board, 5,
                         board.whiteToPlay); // TODO: do not hardcode depth!
}

} // namespace player
