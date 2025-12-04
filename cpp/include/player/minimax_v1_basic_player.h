
#ifndef MINIMAX_V1_BASIC_PLAYER_H
#define MINIMAX_V1_BASIC_PLAYER_H

#include "player.h"

namespace player {

class MinimaxV1 : public Player {
public:
    MinimaxV1(const std::string& name) : Player(name) {}
    
    types::Move getMove(const types::Board& board) override;
};

} // namespace player

#endif // MINIMAX_V1_BASIC_PLAYER_H
