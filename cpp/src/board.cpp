#include "../include/board.h"
#include <string>
#include <vector>

using namespace types;

namespace board {

Board initialBoard(int N) {
  // TODO: maybe just hardcode the result for the 5 possible Ns
  Bitboard white = 0;
  Bitboard black = 0;
  int n = N - 2;
  for (int i = 0; i < n; i++) {
    white =
        bitboard::setBit(white, bitboard::coordsToPosition({n - 1 - i, i}, N));
    black = bitboard::setBit(
        black, bitboard::coordsToPosition({N - n + i, N - 1 - i}, N));
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
      int position = bitboard::coordsToPosition({x, y}, board.N);
      if (bitboard::getBit(board.white, position)) {
        row += "● ";
      } else if (bitboard::getBit(board.black, position)) {
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

int neighbourCount(Board board, Coordinates coords) {
  return bitboard::neighbourCount(board.white | board.black, coords, board.N);
}

std::vector<Move> possibleMoves(Board board, bool isWhite) {
  std::vector<Move> moves;
  Bitboard allPiecesBitboard = board.white | board.black;

  std::vector<int> positions =
      bitboard::getPositions(getBitboard(board, isWhite));
  Coordinates forbiddenCoords =
      isWhite ? Coordinates{0, 0} : Coordinates{board.N - 1, board.N - 1};
  for (const int &position : positions) {
    std::vector<Move> pieceMoves = bitboard::possibleMovesFrom(
        allPiecesBitboard, bitboard::positionToCoords(position, board.N),
        forbiddenCoords, board.N);
    moves.insert(moves.end(), pieceMoves.begin(), pieceMoves.end());
  }
  return moves;
}

} // namespace board
