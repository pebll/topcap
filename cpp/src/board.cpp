#include "../include/board.h"
#include <cassert>
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
  return {white, black, N, true}; // white starts
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
  return bitboard::neighbourCount(getTotalBitboard(board), coords, board.N);
}

std::vector<Move> possibleMoves(Board board) {
  std::vector<Move> moves;
  std::vector<int> positions =
      bitboard::getPositions(getCurrentColorBitboard(board));
  for (const int &position : positions) {
    std::vector<Move> pieceMoves = bitboard::possibleMovesFrom(
        getTotalBitboard(board), bitboard::positionToCoords(position, board.N),
        forbiddenCoords(board), board.N);
    moves.insert(moves.end(), pieceMoves.begin(), pieceMoves.end());
  }
  return moves;
}

Coordinates forbiddenCoords(Board board) {
  return board.whiteToPlay ? Coordinates{0, 0}
                           : Coordinates{board.N - 1, board.N - 1};
}

bool isMoveLegal(Board board, Move move) {
  // TODO: here also create an Optim version
  if (!bitboard::isMoveFeasible(getTotalBitboard(board), move, board.N)) {
    return false;
  }
  if (!bitboard::getBit(getCurrentColorBitboard(board), move.from, board.N)) {
    return false;
  }
  if (std::abs(move.from.x - move.to.x) + std::abs(move.from.y - move.to.y) !=
      neighbourCount(board, move.from)) {
    return false;
  }
  if (move.to == forbiddenCoords(board)) {
    return false;
  }
  return true;
}

Board makeMove(Board board, Move move) {
  assert(isMoveLegal(board, move));
  board.whiteToPlay
      ? board.white = bitboard::makeMove(board.white, move, board.N)
      : board.black = bitboard::makeMove(board.black, move, board.N);
  board.whiteToPlay = !board.whiteToPlay;
  return board;
}

} // namespace board
