CXX = g++
CXXFLAGS = -std=c++17 -Wall -Iinclude

game: src/main.cpp src/bitboard.cpp
	$(CXX) $(CXXFLAGS) $^ -o build/game

test: src/bitboard.cpp tests/test_bitboard.cpp
	@mkdir -p build
	$(CXX) $(CXXFLAGS) src/bitboard.cpp tests/test_bitboard.cpp -o build/test_game
	./build/test_game

clean:
	rm -rf  build

.PHONY: test clean
