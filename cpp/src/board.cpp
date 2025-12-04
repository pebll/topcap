#include "../include/board.h"
#include <cassert>
#include <string>
#include <utility>
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

std::string boardToString(const Board &board) {
  std::string spaces = std::string(STRING_SPACE_LENGTH, ' ');
  std::string str = std::string();
  str += mStringHeader(board.N);
  for (int y = board.N - 1; y >= 0; y--) {
    std::string row = spaces + std::to_string(y + 1) + " ";
    for (int x = 0; x < board.N; x++) {
      int position = bitboard::coordsToPosition({x, y}, board.N);
      if (bitboard::getBit(getColorBitboard(board, true), position)) {
        row += "● ";
      } else if (bitboard::getBit(getColorBitboard(board, false), position)) {
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

int neighbourCount(const Board &board, Coordinates coords) {
  return bitboard::neighbourCount(getTotalBitboard(board), coords, board.N);
}

std::vector<Move> possibleMoves(const Board &board) {
  if (board.possibleMovesValid) {
    return board.possibleMovesCache;
  }
  std::vector<Move> moves;
  std::vector<int> positions =
      bitboard::getPositions(getCurrentColorBitboard(board));
  for (const int &position : positions) {
    std::vector<Move> pieceMoves = bitboard::possibleMovesFrom(
        getTotalBitboard(board), bitboard::positionToCoords(position, board.N),
        forbiddenCoords(board), board.N);
    moves.insert(moves.end(), pieceMoves.begin(), pieceMoves.end());
  }
  board.possibleMovesCache = moves;
  board.possibleMovesValid = true;
  return moves;
}

bool isMoveLegal(const Board &board, Move move) {
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
  setColorBitboardInPlace(
      board, board.whiteToPlay,
      bitboard::makeMove(getCurrentColorBitboard(board), move, board.N));
  board.whiteToPlay = !board.whiteToPlay;
  board.possibleMovesValid = false; // invalidate cache!
  return board;
}

std::pair<bool, bool> terminalState(const Board &board) {
  // be sure that current player is not in opponent goal
  assert(!bitboard::getBit(getCurrentColorBitboard(board),
                           colorBaseCoords(board, !board.whiteToPlay),
                           board.N));
  Bitboard opponent = getNextColorBitboard(board);
  if (bitboard::getBit(opponent, forbiddenCoords(board), board.N)) {
    return {true, !board.whiteToPlay}; // opponent reached base
  }
  if (possibleMoves(board).size() == 0) {
    return {true, !board.whiteToPlay}; // no moves left
  }
  return {false, false};
}

} // namespace board
