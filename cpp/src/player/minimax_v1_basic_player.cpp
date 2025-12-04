#include "../../include/player/minimax_v1_basic_player.h"
#include "../../include/board.h"
#include "../../include/search.h"
#include <random>
#include <vector>

using namespace types;

namespace player {

Move MinimaxV1::getMove(const Board& board) {
  return search::minimax(board,1 );
}

} // namespace player
