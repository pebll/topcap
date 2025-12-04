# C++ Primer for Topcap Game Engine

## Table of Contents

1. [C++ Project Structure](#cpp-project-structure)
2. [Header Files (.h/.hpp)](#header-files-hhpp)
3. [Source Files (.cpp)](#source-files-cpp)
4. [Compilation Basics](#compilation-basics)
5. [Makefiles](#makefiles)
6. [Testing in C++](#testing-in-c)
7. [Bit Manipulation Basics](#bit-manipulation-basics)
8. [TDD Workflow Example](#tdd-workflow-example)

---

## C++ Project Structure

A typical C++ project has this structure:

```
project/
├── src/              # Source files (.cpp)
│   ├── main.cpp
│   └── game.cpp
├── include/          # Header files (.h or .hpp)
│   └── game.h
├── tests/            # Test files
│   └── test_game.cpp
├── Makefile          # Build configuration
└── README.md
```

**Key Concepts:**

- **Header files (.h/.hpp)**: Declarations (what functions/classes exist)
- **Source files (.cpp)**: Implementations (how functions/classes work)
- **Separation**: Headers declare, sources implement

---

## Header Files (.h/.hpp)

Headers contain:

- Function declarations
- Class definitions
- Type definitions
- Constants
- Includes of other headers

### Example: `include/bitboard.h`

```cpp
#ifndef BITBOARD_H  // Header guard - prevents multiple includes
#define BITBOARD_H

#include <cstdint>  // For uint64_t, int types

// Type alias for clarity
using Bitboard = uint64_t;

// Function declarations (no implementation here!)
int getValue(Bitboard bitboard, int position);
Bitboard toggleValue(Bitboard bitboard, int position);
Bitboard movePiece(Bitboard bitboard, int from, int to);
int getNeighborCount(Bitboard pieceBitboard, int position);

#endif  // BITBOARD_H
```

**Important:**

- **Header guards** (`#ifndef`/`#define`/`#endif`) prevent including the same header twice
- Only **declarations**, no function bodies (except inline functions)
- Include what you need (like `<cstdint>` for `uint64_t`)

---

## Source Files (.cpp)

Source files contain:

- Function implementations
- Includes of corresponding headers

### Example: `src/bitboard.cpp`

```cpp
#include "../include/bitboard.h"  // Include the header

// Implementation of getValue
int getValue(Bitboard bitboard, int position) {
    return (bitboard & (1ULL << position)) >> position;
}

// Implementation of toggleValue
Bitboard toggleValue(Bitboard bitboard, int position) {
    return bitboard ^ (1ULL << position);
}

// Implementation of movePiece
Bitboard movePiece(Bitboard bitboard, int from, int to) {
    return bitboard ^ (1ULL << from) ^ (1ULL << to);
}

// Implementation of getNeighborCount
int getNeighborCount(Bitboard pieceBitboard, int position) {
    // Implementation here
    return 0;  // Placeholder
}
```

**Notes:**

- Use `1ULL` (unsigned long long literal) for bit shifts on 64-bit values
- Include the corresponding header first
- Implement all functions declared in the header

---

## Compilation Basics

### Manual Compilation

```bash
# Compile a single file
g++ -c src/bitboard.cpp -o build/bitboard.o -Iinclude

# Link object files into executable
g++ build/bitboard.o build/main.o -o build/game

# Or compile and link in one step
g++ src/bitboard.cpp src/main.cpp -Iinclude -o build/game
```

**Flags:**

- `-c`: Compile only (create object file, don't link)
- `-Iinclude`: Add `include/` to include path
- `-o`: Output file name
- `-std=c++17`: Use C++17 standard (or `-std=c++11`, `-std=c++20`, etc.)
- `-Wall -Wextra`: Enable warnings
- `-g`: Include debug symbols
- `-O2` or `-O3`: Optimization level

---

## Makefiles

**Recommendation: Use plain Makefiles** (not CMake) for this project. See `BUILD_SYSTEMS.md` for a detailed comparison.

**Why Makefiles:**

- ✅ Minimal and simple - no extra tools needed
- ✅ Direct control - you see exactly what happens
- ✅ Fast for TDD workflow
- ✅ Perfect for small-to-medium projects
- ✅ `make` comes pre-installed on Linux

Makefiles automate compilation. They define:

- **Targets**: What to build (executables, object files)
- **Dependencies**: What files a target depends on
- **Rules**: How to build targets

### Minimal Makefile (Recommended for Small Projects)

```makefile
CXX = g++
CXXFLAGS = -std=c++17 -Wall -Iinclude

# Build the game
game: src/main.cpp src/bitboard.cpp
 $(CXX) $(CXXFLAGS) $^ -o game

# Run tests
test: src/bitboard.cpp tests/test_bitboard.cpp
 $(CXX) $(CXXFLAGS) $^ -o test_game
 ./test_game

# Clean
clean:
 rm -f game test_game

.PHONY: test clean
```

**That's it!** Just 12 lines. This compiles everything together in one step - perfect for small projects and TDD.

**Usage:**

```bash
make game    # Build
make test    # Build and run tests
make clean   # Remove executables
```

---

### Slightly Better Version (Optional)

If you want to keep executables in a `build/` folder:

```makefile
CXX = g++
CXXFLAGS = -std=c++17 -Wall -Iinclude
BUILDDIR = build

game: src/main.cpp src/bitboard.cpp
 @mkdir -p $(BUILDDIR)
 $(CXX) $(CXXFLAGS) $^ -o $(BUILDDIR)/game

test: src/bitboard.cpp tests/test_bitboard.cpp
 @mkdir -p $(BUILDDIR)
 $(CXX) $(CXXFLAGS) $^ -o $(BUILDDIR)/test_game
 ./$(BUILDDIR)/test_game

clean:
 rm -rf $(BUILDDIR)

.PHONY: test clean
```

**When to use the complex version:**

- Only if you have many files (>10) and want faster rebuilds (separate object files)
- For now, the minimal version is perfect!

**Usage:**

```bash
make              # Build the game
make test         # Build and run tests
make clean        # Remove build files
```

**Key Makefile Syntax:**

- `$(VARIABLE)`: Use a variable
- `$@`: Target name
- `$<`: First dependency
- `$^`: All dependencies
- `| $(BUILDDIR)`: Order-only dependency (create dir if needed)
- `.PHONY`: Targets that aren't files

---

## Testing in C++

### Testing Framework Options

1. **Catch2** (Recommended for beginners)
   - Header-only, easy to set up
   - Modern C++ syntax
   - Good documentation

2. **Google Test (gtest)**
   - More features, but requires installation
   - Industry standard

3. **Doctest**
   - Lightweight, fast compilation
   - Similar to Catch2

### Example with Catch2: `tests/test_bitboard.cpp`

```cpp
#define CATCH_CONFIG_MAIN  // This tells Catch to provide a main()
#include "catch.hpp"        // Download catch.hpp to tests/
#include "../include/bitboard.h"

TEST_CASE("getValue returns correct bit", "[bitboard]") {
    Bitboard board = 0b1001;  // Binary literal
    
    REQUIRE(getValue(board, 0) == 1);
    REQUIRE(getValue(board, 1) == 0);
    REQUIRE(getValue(board, 2) == 0);
    REQUIRE(getValue(board, 3) == 1);
}

TEST_CASE("toggleValue flips bit", "[bitboard]") {
    Bitboard board = 0b1001;
    
    Bitboard result = toggleValue(board, 1);
    REQUIRE(result == 0b1011);
    
    // Toggle again should restore
    REQUIRE(toggleValue(result, 1) == board);
}

TEST_CASE("movePiece moves bit from one position to another", "[bitboard]") {
    Bitboard board = 0b1001;  // Bits at positions 0 and 3
    
    Bitboard result = movePiece(board, 0, 2);
    REQUIRE(result == 0b1100);  // Bits at positions 2 and 3
}
```

**Catch2 Setup:**

1. Download `catch.hpp` from <https://github.com/catchorg/Catch2/releases>
2. Place in `tests/catch.hpp`
3. Compile test file with Catch2 included

**Test Structure:**

- `TEST_CASE("description", "[tags]")`: Define a test
- `REQUIRE(condition)`: Assert condition (stops on failure)
- `CHECK(condition)`: Assert condition (continues on failure)

---

## Bit Manipulation Basics

### Common Operations

```cpp
// Set bit at position
bitboard |= (1ULL << position);

// Clear bit at position
bitboard &= ~(1ULL << position);

// Toggle bit at position
bitboard ^= (1ULL << position);

// Get bit at position
int value = (bitboard >> position) & 1;
// Or: int value = (bitboard & (1ULL << position)) >> position;

// Check if bit is set
bool isSet = (bitboard & (1ULL << position)) != 0;

// Count set bits (population count)
int count = __builtin_popcountll(bitboard);  // GCC/Clang
// Or use std::popcount in C++20: int count = std::popcount(bitboard);
```

### Important Notes for Your Project

- Use `1ULL` (unsigned long long) for 64-bit shifts
- `long long` is typically 64 bits, but `uint64_t` is guaranteed 64 bits
- Bit positions: 0 = rightmost (least significant), 63 = leftmost (most significant)
- For 36-bit positions (0-35), you only use bits 0-35 of the 64-bit integer

### Example: Neighbor Positions

For a 6x6 grid (36 positions), positions are:

```
 0  1  2  3  4  5
 6  7  8  9 10 11
12 13 14 15 16 17
18 19 20 21 22 23
24 25 26 27 28 29
30 31 32 33 34 35
```

Neighbors of position `pos`:

```cpp
int right = pos + 1;      // If not on right edge (pos % 6 != 5)
int left = pos - 1;       // If not on left edge (pos % 6 != 0)
int up = pos - 6;         // If not on top row (pos >= 6)
int down = pos + 6;       // If not on bottom row (pos < 30)
int upRight = pos - 5;    // If not on top row and not right edge
int downRight = pos + 7;  // If not on bottom row and not right edge
int upLeft = pos - 7;     // If not on top row and not left edge
int downLeft = pos + 5;   // If not on bottom row and not left edge
```

---

## TDD Workflow Example

Following TDD for your project:

### Step 1: Write a Failing Test

```cpp
// tests/test_bitboard.cpp
TEST_CASE("getValue returns 1 for set bit", "[bitboard]") {
    Bitboard board = 0b1001;
    REQUIRE(getValue(board, 0) == 1);
}
```

### Step 2: Write Minimal Implementation

```cpp
// include/bitboard.h
int getValue(Bitboard bitboard, int position);

// src/bitboard.cpp
int getValue(Bitboard bitboard, int position) {
    return (bitboard & (1ULL << position)) >> position;
}
```

### Step 3: Run Test

```bash
make test
```

### Step 4: Refactor (if needed)

Once test passes, you can improve the code while keeping tests green.

### Step 5: Repeat

Add next test, implement, test, refactor.

---

## Quick Reference: Common C++ Types

```cpp
#include <cstdint>

uint8_t   // 8-bit unsigned (0 to 255)
uint16_t  // 16-bit unsigned
uint32_t  // 32-bit unsigned
uint64_t  // 64-bit unsigned (your bitboards!)

int8_t    // 8-bit signed
int16_t   // 16-bit signed
int32_t   // 32-bit signed
int64_t   // 64-bit signed

long long // Usually 64-bit, but not guaranteed
```

**Recommendation:** Use `uint64_t` for your bitboards (guaranteed 64 bits).

---

## Next Steps

1. Set up project structure (src/, include/, tests/, build/)
2. Create a basic Makefile
3. Download Catch2 header to tests/
4. Write your first test (e.g., `getValue`)
5. Implement minimal code to pass
6. Repeat!

Good luck with your bitboard-based game engine! 🎮
