#include "../include/board.h"
#include <iostream>

using namespace types;

namespace search {

float evaluate(Board board) {
  if (board::terminalState(board).first) {
    bool winner = board::terminalState(board).second;
    // std::cout << "Found terminalState with " << (winner ? "white" : "black")
    //           << " as winner!" << std::endl;
    // std::cout << board::boardToString(board) << std::endl;
    return winner ? 1000 : -1000;
  }
  // std::cout << "Found normal state" << std::endl;
  // std::cout << board::boardToString(board) << std::endl;
  return 0;
}

float maxValue(Board board, int depthToGo);
float minValue(Board board, int depthToGo) {
  if (depthToGo == 0 || board::terminalState(board).first) {
    float eval = evaluate(board) * (depthToGo + 1);
    // std::cout << "DTG " << depthToGo << ": " << eval << std::endl;
    return eval;
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
    float eval = evaluate(board) * (depthToGo + 1);
    // std::cout << "DTG " << depthToGo << ": " << eval << std::endl;
    return eval;
  }
  std::vector<Move> moves = board::possibleMoves(board);
  float bestValue = -1000;

  for (const Move &move : moves) {
    Board newBoard = board::makeMove(board, move);
    bestValue = std::max(bestValue, minValue(newBoard, depthToGo - 1));
  }
  return bestValue;
}

Move minimax(Board board, int maxDepth, bool maximizing) {
  std::vector<Move> moves = board::possibleMoves(board);
  Move bestMove = moves[0];
  float bestValue = maximizing ? -1000 : 1000;
  for (const Move &move : moves) {
    Board newBoard = board::makeMove(board, move);
    float newValue = maximizing ? maxValue(newBoard, maxDepth - 1)
                                : minValue(newBoard, maxDepth - 1);
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
