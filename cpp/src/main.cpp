#include "../include/board.h"
#include <iostream>

int main() {
  int N = 8;
  std::cout << "Board of size " << std::to_string(N) << "\n";
  std::cout << board::boardToString(board::initialBoard(N));
  return 0;
}
