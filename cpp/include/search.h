#ifndef SEARCH_H
#define SEARCH_H

#include "bitboard.h"
#include "player/player.h"
#include "types.h"
#include <string>
#include <vector>

namespace search {

using Bitboard = types::Bitboard;
using Coordinates = types::Coordinates;
using Move = types::Move;
using Board = types::Board;
using Player = player::Player;

Move minimax(Board board, int maxDepth, bool maximizing);
float minValue(Board board, int depthToGo);
float maxValue(Board board, int depthToGo);
float evaluate(Board board);

} // namespace search

#endif // !SEARCH_H
