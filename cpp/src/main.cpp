#include "../include/game.h"
#include "../include/player/human_player.h"
#include "../include/player/minimax_v1_basic_player.h"
#include "../include/player/random_player.h"
#include <chrono>
#include <iostream>
#include <utility>

int main() {
  int N = 4;
  int games = 500;

  // std::cout << "Enter your board size (N) [4-8]: ";
  // std::cin >> N;

  player::Human human("Human");
  player::RandomAI randi("Randi");
  player::RandomAI rando("Rando");
  player::MinimaxV1 minimax("Minimax");
  player::MinimaxV1 maximin("Maximin");

  // Start profiling
  auto start = std::chrono::high_resolution_clock::now();

  // game::runGame(N, &randi, &maximin, true);

  const int RUN_GAMES = true;
  player::Player &PLAYER_1 = randi;
  player::Player &PLAYER_2 = maximin;

  if (!RUN_GAMES)
    game::runGame(N, &maximin, &randi, true);

  if (RUN_GAMES) {
    std::pair<int, int> wins = {0, 0};
    int steps = 0;
    for (int i = 0; i < games; i++) {
      if ((i + 1) % 100 == 0) {
        std::cout << "Running game " << i + 1 << std::endl;
      }

      game::GameResult result =
          game::runGame(N, i % 2 == 0 ? &PLAYER_1 : &PLAYER_2,
                        i % 2 == 0 ? &PLAYER_2 : &PLAYER_1, false);
      steps += result.gameSteps;
      if ((int)result.winner % 2 == i % 2) {
        wins.first += 1;
      } else {
        wins.second += 1;
      }
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
    std::cout << "Wins player 1 / 2: " << wins.first << " / " << wins.second
              << std::endl;
    std::cout << "Winrate player 1 / 2: "
              << int(100 * wins.first / (double)games) << "% / "
              << int(100 * wins.second / (double)games) << "%" << std::endl;

    return 0;
  }
}
