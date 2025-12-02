#ifndef RANDOM_PLAYER_H
#define RANDOM_PLAYER_H

#include "player.h"

namespace player {

class RandomAI : public Player {
public:
    RandomAI(const std::string& name) : Player(name) {}
    
    types::Move getMove(const types::Board& board) override;
};

} // namespace player

#endif // RANDOM_PLAYER_H
