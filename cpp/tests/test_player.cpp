#include "catch.hpp"
#include "../include/player/player.h"
#include "../include/player/random_player.h"
#include "../include/player/human_player.h"
#include "../include/board.h"
#include "../include/utils.h"

using namespace player;
using namespace types;

// Test that Player is abstract (cannot be instantiated)
// We'll test this by creating a concrete implementation

class TestPlayer : public Player {
public:
    TestPlayer(const std::string& name) : Player(name) {}
    Move getMove(const Board& board) override {
        auto moves = board::possibleMoves(board);
        return moves.empty() ? Move{{0,0}, {0,0}} : moves[0];
    }
};

TEST_CASE("Player can be instantiated through derived class", "[player]") {
    TestPlayer p("Test");
    REQUIRE(p.getName() == "Test");
    REQUIRE(p.getIsWhite() == false);
}

TEST_CASE("Player setIsWhite works", "[player]") {
    TestPlayer p("Test");
    p.setIsWhite(true);
    REQUIRE(p.getIsWhite() == true);
    p.setIsWhite(false);
    REQUIRE(p.getIsWhite() == false);
}

TEST_CASE("RandomAI can be instantiated", "[random_player]") {
    RandomAI ai("Random");
    REQUIRE(ai.getName() == "Random");
    REQUIRE(ai.getIsWhite() == false);
}

TEST_CASE("RandomAI returns valid move", "[random_player]") {
    RandomAI ai("Random");
    Board board = board::initialBoard(4);
    
    Move move = ai.getMove(board);
    auto allMoves = board::possibleMoves(board);
    
    // Check that the move is in the list of possible moves
    bool found = false;
    for (const auto& m : allMoves) {
        if (m.from.x == move.from.x && m.from.y == move.from.y &&
            m.to.x == move.to.x && m.to.y == move.to.y) {
            found = true;
            break;
        }
    }
    REQUIRE(found);
    REQUIRE(board::isMoveLegal(board, move));
}

TEST_CASE("Human can be instantiated", "[human_player]") {
    Human human("Human");
    REQUIRE(human.getName() == "Human");
    REQUIRE(human.getIsWhite() == false);
}

TEST_CASE("tileToCoords converts correctly", "[utils]") {
    REQUIRE(utils::tileToCoords("a1") == Coordinates{0, 0});
    REQUIRE(utils::tileToCoords("a2") == Coordinates{0, 1});
    REQUIRE(utils::tileToCoords("b1") == Coordinates{1, 0});
    REQUIRE(utils::tileToCoords("d4") == Coordinates{3, 3});
}

TEST_CASE("coordsToTile converts correctly", "[utils]") {
    REQUIRE(utils::coordsToTile(Coordinates{0, 0}, 4) == "a1");
    REQUIRE(utils::coordsToTile(Coordinates{0, 1}, 4) == "a2");
    REQUIRE(utils::coordsToTile(Coordinates{1, 0}, 4) == "b1");
    REQUIRE(utils::coordsToTile(Coordinates{3, 3}, 4) == "d4");
    REQUIRE(utils::coordsToTile(Coordinates{5, 5}, 6) == "f6");
}

TEST_CASE("tileToCoords and coordsToTile are inverse", "[utils]") {
    std::vector<std::string> tiles = {"a1", "a2", "b1", "c3", "d4", "f6"};
    for (const auto& tile : tiles) {
        Coordinates coords = utils::tileToCoords(tile);
        std::string back = utils::coordsToTile(coords, 6);
        REQUIRE(back == tile);
    }
}

TEST_CASE("Human parseMove works", "[human_player]") {
    // Test "a1 a2" format
    Move move1 = Human::parseMove("a1 a2");
    REQUIRE(move1.from == Coordinates{0, 0});
    REQUIRE(move1.to == Coordinates{0, 1});
    
    // Test "a1a2" format
    Move move2 = Human::parseMove("a1a2");
    REQUIRE(move2.from == Coordinates{0, 0});
    REQUIRE(move2.to == Coordinates{0, 1});
    
    // Test "b2 c3" format
    Move move3 = Human::parseMove("b2 c3");
    REQUIRE(move3.from == Coordinates{1, 1});
    REQUIRE(move3.to == Coordinates{2, 2});
    
    // Test invalid format (too short)
    Move move4 = Human::parseMove("a1");
    REQUIRE(move4.from.x == -1); // Invalid marker
}
