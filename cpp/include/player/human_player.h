#ifndef HUMAN_PLAYER_H
#define HUMAN_PLAYER_H

#include "player.h"

namespace player {

class Human : public Player {
public:
    Human(const std::string& name) : Player(name) {}
    
    types::Move getMove(const types::Board& board) override;
    static types::Move parseMove(const std::string& moveStr);
};

} // namespace player

#endif // HUMAN_PLAYER_H
