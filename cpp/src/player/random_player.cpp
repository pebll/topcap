#include "../../include/player/random_player.h"
#include "../../include/board.h"
#include <random>
#include <vector>

using namespace types;

namespace player {

Move RandomAI::getMove(const Board& board) {
    std::vector<Move> moves = board::possibleMoves(board);
    
    if (moves.empty()) {
        // Should not happen in normal gameplay, but return a dummy move
        return {{0, 0}, {0, 0}};
    }
    
    static std::random_device rd;
    static std::mt19937 gen(rd());
    std::uniform_int_distribution<> dis(0, moves.size() - 1);
    
    return moves[dis(gen)];
}

} // namespace player
