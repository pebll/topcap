#include "../include/game.h"
#include "../include/board.h"
#include "../include/utils.h"
#include <iostream>

using namespace types;


namespace search {

float evaluate(Board board){
  return 0.0;
}

float minValue(Board board, int depthToGo){
  if (depthToGo == 0){
    return evaluate(board);
  }
  if (board::terminalState(board)[0]){


  }
  std::vector<Move> moves = board::possibleMoves(board);
  float value = 1000; // TODO: how to do inf?
  Move move = 
  for(const Move &move : moves){
    v

}

Move minimax(Board board, int depthToGo){
  if (depthToGo == 0){
    return evaluate(board);
  }
  std::vector<Move> moves = board::possibleMoves(board);
  for(const Move &move : moves){


  }
  return moves[0];
}
} // namespace search
