#ifndef GAME_H
#define GAME_H

#include "bitboard.h"
#include "player/player.h"
#include "types.h"
#include <string>
#include <vector>

namespace game {

using Bitboard = types::Bitboard;
using Coordinates = types::Coordinates;
using Move = types::Move;
using Board = types::Board;
using Player = player::Player;

// TODO: return useful stuff
int runGame(int N, Player *white, Player *black, bool verbose);

} // namespace game

#endif // !GAME_H
