CXX = g++
CXXFLAGS = -std=c++17 -Wall -Iinclude
BUILDDIR = build

# Object files
BITBOARD_OBJ = $(BUILDDIR)/bitboard.o
BOARD_OBJ = $(BUILDDIR)/board.o
TEST_BITBOARD_OBJ = $(BUILDDIR)/test_bitboard.o
TEST_BOARD_OBJ = $(BUILDDIR)/test_board.o

game: src/main.cpp $(BITBOARD_OBJ) $(BOARD_OBJ)
	@mkdir -p $(BUILDDIR)
	$(CXX) $(CXXFLAGS) src/main.cpp $(BITBOARD_OBJ) $(BOARD_OBJ) -o $(BUILDDIR)/game

test: $(BITBOARD_OBJ) $(BOARD_OBJ) $(TEST_BITBOARD_OBJ) $(TEST_BOARD_OBJ)
	@mkdir -p $(BUILDDIR)
	$(CXX) $(CXXFLAGS) $(BITBOARD_OBJ) $(BOARD_OBJ) $(TEST_BITBOARD_OBJ) $(TEST_BOARD_OBJ) -o $(BUILDDIR)/test_game
	./$(BUILDDIR)/test_game

# Compile bitboard.cpp to object file
$(BITBOARD_OBJ): src/bitboard.cpp include/bitboard.h | $(BUILDDIR)
	$(CXX) $(CXXFLAGS) -c src/bitboard.cpp -o $@

# Compile board.cpp to object file
$(BOARD_OBJ): src/board.cpp include/board.h include/bitboard.h | $(BUILDDIR)
	$(CXX) $(CXXFLAGS) -c src/board.cpp -o $@

# Compile test_bitboard.cpp to object file
$(TEST_BITBOARD_OBJ): tests/test_bitboard.cpp include/bitboard.h | $(BUILDDIR)
	$(CXX) $(CXXFLAGS) -c tests/test_bitboard.cpp -o $@

# Compile test_board.cpp to object file
$(TEST_BOARD_OBJ): tests/test_board.cpp include/board.h include/bitboard.h | $(BUILDDIR)
	$(CXX) $(CXXFLAGS) -c tests/test_board.cpp -o $@

$(BUILDDIR):
	mkdir -p $(BUILDDIR)

clean:
	rm -rf $(BUILDDIR)

.PHONY: test clean game
