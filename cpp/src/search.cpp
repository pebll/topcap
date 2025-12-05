#include "../include/board.h"
#include <iostream>

using namespace types;

namespace search {

float evaluate(Board board) {
  if (board::terminalState(board).first) {
    bool winner = board::terminalState(board).second;
    std::cout << "Found terminalState with " << (winner ? "white" : "black")
              << " as winner!" << std::endl;
    return winner ? 1000 : -1000;
  }
  return 0;
}

float maxValue(Board board, int depthToGo);
float minValue(Board board, int depthToGo) {
  if (depthToGo == 0 || board::terminalState(board).first) {
    return evaluate(board);
  }
  std::vector<Move> moves = board::possibleMoves(board);
  float bestValue = 1000;

  for (const Move &move : moves) {
    Board newBoard = board::makeMove(board, move);
    bestValue = std::min(bestValue, maxValue(newBoard, depthToGo - 1));
  }
  return bestValue;
}

float maxValue(Board board, int depthToGo) {
  if (depthToGo == 0 || board::terminalState(board).first) {
    return evaluate(board);
  }
  std::vector<Move> moves = board::possibleMoves(board);
  float bestValue = -1000;

  for (const Move &move : moves) {
    Board newBoard = board::makeMove(board, move);
    bestValue = std::max(bestValue, minValue(newBoard, depthToGo - 1));
  }
  return bestValue;
}

Move minimax(Board board, int depthToGo, bool maximizing) {
  std::vector<Move> moves = board::possibleMoves(board);
  Move bestMove = moves[0];
  float bestValue = maximizing ? -1000 : 1000;
  for (const Move &move : moves) {
    float newValue =
        maximizing ? maxValue(board, depthToGo) : minValue(board, depthToGo);
    if ((maximizing && newValue > bestValue) ||
        (!maximizing && newValue < bestValue)) {
      bestValue = newValue;
      bestMove = move;
    }
  }
  std::cout << "Chose best move with eval " << bestValue << std::endl;
  return bestMove;
}
} // namespace search
