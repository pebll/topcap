#include "../include/board.h"

Board initialBoard(int N) {
  // TODO: maybe just hardcode the result for the 5 possible Ns
  Bitboard white = 0;
  Bitboard black = 0;
  int n = N - 2;
  for (int i = 0; i < n; i++) {
    white = setBit(white, coordsToPosition({n - 1 - i, i}, N));
    black = setBit(black, coordsToPosition({N - n + i, N - 1 - i}, N));
  }
  return {white, black};
}
