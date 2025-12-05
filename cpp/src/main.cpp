#include "../include/game.h"
#include "../include/player/human_player.h"
#include "../include/player/minimax_v1_basic_player.h"
#include "../include/player/random_player.h"
#include <chrono>
#include <iostream>

int main() {
  int N = 4;
  int games = 50000;

  // std::cout << "Enter your board size (N) [4-8]: ";
  // std::cin >> N;

  player::Human human("Human");
  player::RandomAI randi("Randi");
  player::RandomAI rando("Rando");
  player::MinimaxV1 minimax("Minimax");

  // Start profiling
  auto start = std::chrono::high_resolution_clock::now();

  const int RUN_GAMES = false;
  game::runGame(N, &minimax, &human, true);

  if (RUN_GAMES) {
    int steps = 0;
    for (int i = 0; i < games; i++) {
      if ((i + 1) % 100 == 0) {
        std::cout << "Running game " << i + 1 << std::endl;
      }
      steps += game::runGame(N, &randi, &rando, false);
    }

    // End profiling
    auto end = std::chrono::high_resolution_clock::now();
    auto duration =
        std::chrono::duration_cast<std::chrono::milliseconds>(end - start);

    std::cout << "\n=== Profiling Results ===" << std::endl;
    std::cout << "Total games: " << games << std::endl;
    std::cout << "Total time: " << duration.count() << " ms" << std::endl;
    std::cout << "Average time per game: " << (double)duration.count() / games
              << " ms" << std::endl;
    std::cout << "Games per second: " << int(games / ((double)duration.count()))
              << "k /s" << std::endl;
    std::cout << "Steps per second: " << int(steps / ((double)duration.count()))
              << "k /s" << std::endl;

    return 0;
  }
}
