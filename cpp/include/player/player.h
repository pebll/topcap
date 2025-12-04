#ifndef PLAYER_H
#define PLAYER_H

#include "../types.h"
#include <string>

namespace player {

class Player {
public:
    Player(const std::string& name) : name_(name), isWhite_(false) {}
    virtual ~Player() = default;
    
    virtual types::Move getMove(const types::Board& board) = 0;
    
    void setIsWhite(bool isWhite) { isWhite_ = isWhite; }
    std::string getName() const { return name_; }
    bool getIsWhite() const { return isWhite_; }

protected:
    std::string name_;
    bool isWhite_;
};

} // namespace player

#endif // PLAYER_H
