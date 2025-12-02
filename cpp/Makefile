# Compiler and flags
CXX = g++
CXXFLAGS = -std=c++17 -Wall -Wextra -Iinclude
DEBUGFLAGS = -g -O0
RELEASEFLAGS = -O3 -DNDEBUG
PROFILEFLAGS = -pg

# Directories
SRCDIR = src
TESTDIR = tests
INCLUDEDIR = include
BUILDDIR = build

# Source files (including subdirectories)
SOURCES = $(wildcard $(SRCDIR)/*.cpp) $(wildcard $(SRCDIR)/*/*.cpp)
TEST_SOURCES = $(wildcard $(TESTDIR)/test_*.cpp)

# Object files (excluding main.cpp for library)
LIB_OBJECTS = $(patsubst $(SRCDIR)/%.cpp,$(BUILDDIR)/%.o,$(filter-out $(SRCDIR)/main.cpp,$(SOURCES)))
TEST_OBJECTS = $(patsubst $(TESTDIR)/%.cpp,$(BUILDDIR)/%.o,$(TEST_SOURCES))

# Dependency files (for automatic header dependency tracking)
LIB_DEPS = $(LIB_OBJECTS:.o=.d)
TEST_DEPS = $(TEST_OBJECTS:.o=.d)

# Executables
GAME = $(BUILDDIR)/game
TEST_GAME = $(BUILDDIR)/test_game

# Default target
all: $(GAME)

# Build the game executable
$(GAME): $(SRCDIR)/main.cpp $(LIB_OBJECTS) | $(BUILDDIR)
	$(CXX) $(CXXFLAGS) $(RELEASEFLAGS) $^ -o $@

# Build and run tests
test: $(TEST_GAME)
	./$(TEST_GAME)

# Build test executable
$(TEST_GAME): $(LIB_OBJECTS) $(TEST_OBJECTS) | $(BUILDDIR)
	$(CXX) $(CXXFLAGS) $(DEBUGFLAGS) $^ -o $@

# Pattern rule: compile source files to object files
# -MMD generates dependency files, -MP adds phony targets for headers
$(BUILDDIR)/%.o: $(SRCDIR)/%.cpp | $(BUILDDIR)
	@mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(DEBUGFLAGS) -MMD -MP -c $< -o $@

# Pattern rule: compile test files to object files
$(BUILDDIR)/%.o: $(TESTDIR)/%.cpp | $(BUILDDIR)
	$(CXX) $(CXXFLAGS) $(DEBUGFLAGS) -MMD -MP -c $< -o $@

# Include dependency files (if they exist)
-include $(LIB_DEPS) $(TEST_DEPS)

# Create build directory
$(BUILDDIR):
	mkdir -p $(BUILDDIR)

# Clean build artifacts
clean:
	rm -rf $(BUILDDIR)

# Debug build (with debug flags)
debug: CXXFLAGS += $(DEBUGFLAGS)
debug: $(GAME)

# Release build (with optimization)
release: CXXFLAGS += $(RELEASEFLAGS)
release: $(GAME)

# Profile build (with gprof)
profile: CXXFLAGS += $(PROFILEFLAGS)
profile: $(GAME)

.PHONY: all test clean debug release profile
