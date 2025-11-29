#include "../include/board.h"
#include <string>

namespace board {

Board initialBoard(int N) {
  // TODO: maybe just hardcode the result for the 5 possible Ns
  bb::Bitboard white = 0;
  bb::Bitboard black = 0;
  int n = N - 2;
  for (int i = 0; i < n; i++) {
    white = bb::setBit(white, bb::coordsToPosition({n - 1 - i, i}, N));
    black = bb::setBit(black, bb::coordsToPosition({N - n + i, N - 1 - i}, N));
  }
  return {white, black, N};
}

std::string mStringHeader(int N) {
  std::string header = std::string(STRING_SPACE_LENGTH, ' ') + "  ";
  for (int i = 0; i < N; i++) {
    header += static_cast<char>('a' + i);
    header += ' ';
  }
  header += '\n';
  return header;
}

std::string boardToString(Board board) {
  std::string spaces = std::string(STRING_SPACE_LENGTH, ' ');
  std::string str = std::string();
  str += mStringHeader(board.N);
  for (int y = board.N - 1; y >= 0; y--) {
    std::string row = spaces + std::to_string(y + 1) + " ";
    for (int x = 0; x < board.N; x++) {
      int position = bb::coordsToPosition({x, y}, board.N);
      if (bb::getBit(board.white, position)) {
        row += "● ";
      } else if (bb::getBit(board.black, position)) {
        row += "○ ";
      } else {
        row += "· ";
      }
    }
    str += row + std::to_string(y + 1) + "\n";
  }
  str += mStringHeader(board.N);
  return str;
}

int neighbourCount(Board board, bitboard::Coordinates coords) {
  return bitboard::neighbourCount(board.white | board.black, coords, board.N);
}
} // namespace board
