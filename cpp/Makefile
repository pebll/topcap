CXX = g++
CXXFLAGS = -std=c++17 -Wall -Iinclude
BUILDDIR = build

# Object files
BITBOARD_OBJ = $(BUILDDIR)/bitboard.o
TEST_OBJ = $(BUILDDIR)/test_bitboard.o

game: src/main.cpp $(BITBOARD_OBJ)
	@mkdir -p $(BUILDDIR)
	$(CXX) $(CXXFLAGS) src/main.cpp $(BITBOARD_OBJ) -o $(BUILDDIR)/game

test: $(BITBOARD_OBJ) $(TEST_OBJ)
	@mkdir -p $(BUILDDIR)
	$(CXX) $(CXXFLAGS) $(BITBOARD_OBJ) $(TEST_OBJ) -o $(BUILDDIR)/test_game
	./$(BUILDDIR)/test_game

# Compile bitboard.cpp to object file
$(BITBOARD_OBJ): src/bitboard.cpp include/bitboard.h | $(BUILDDIR)
	$(CXX) $(CXXFLAGS) -c src/bitboard.cpp -o $@

# Compile test_bitboard.cpp to object file
$(TEST_OBJ): tests/test_bitboard.cpp include/bitboard.h | $(BUILDDIR)
	$(CXX) $(CXXFLAGS) -c tests/test_bitboard.cpp -o $@

$(BUILDDIR):
	mkdir -p $(BUILDDIR)

clean:
	rm -rf $(BUILDDIR)

.PHONY: test clean game
