#include "../include/game.h"
#include "../include/board.h"
#include "../include/utils.h"
#include <iostream>

using namespace types;

namespace game {

int runGame(int N, Player *white, Player *black, bool verbose) {
  Board board = board::initialBoard(N);
  white->setIsWhite(true);
  black->setIsWhite(false);

  if (verbose) {
    std::cout << "Here begins the game of topcap!\n" << std::endl;
    std::cout << white->getName() << " vs " << black->getName() << std::endl;
  }

  int step = 0;
  bool gameOver = false;

  while (!gameOver) {
    Player *currentPlayer = (step % 2 == 0) ? white : black;

    if (verbose) {
      std::cout << "\n\nGame round: " << (step / 2 + 1) << ", "
                << currentPlayer->getName() << "'s turn" << std::endl;
      std::cout << board::boardToString(board) << std::endl;
    }

    Move move = currentPlayer->getMove(board);

    if (verbose) {
      std::string fromTile = utils::coordsToTile(move.from, board.N);
      std::string toTile = utils::coordsToTile(move.to, board.N);
      std::cout << currentPlayer->getName() << " moved from " << fromTile
                << " to " << toTile << std::endl;
    }

    board = board::makeMove(board, move);
    step++;

    auto terminal = board::terminalState(board);
    gameOver = terminal.first;

    if (gameOver && verbose) {
      std::cout << board::boardToString(board) << std::endl;
      if (terminal.second) {
        std::cout << white->getName() << " wins!" << std::endl;
      } else {
        std::cout << black->getName() << " wins!" << std::endl;
      }
    }
  }
  return step;
}

} // namespace game
