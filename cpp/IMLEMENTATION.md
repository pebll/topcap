# Implementation

## Board representation

The idea is to represent the board as 2 `long long`'s (2 * 64 bits)

One for each "bitboard", black and white.
Each bitboard will need 36 bits to store the positions of the pieces.
There are a lot of unused bits (because we can't do 32) that could store other stuff.
We must store at least the color that has to currently play (1 bit)

So the suggested representation is:

- WHITE_BITBOARD (64 bit)
  - [0-35] whiteBitboard (36 bit)
  - [36] current player (1 bit)
- BLACK_BITBOARD (64 bit)
  - [0-35] blackBitboard (36 bit)

## Important functions

### Get neighbour count

This is necessary when we want to calculate moves. This should be implemented first, as it is probably quite simple and teach the basics of bit manipulation.

### Step 1: Get the pieceBitboard

Color does not make a difference for neighbour count
-> just OR the to original bitboards

```cpp
pieceBitboard = whiteBitboard | blackBitboard
```

### Step 2: Get the actual counts

This should filter out the 9 positions around the given position and sum the values
First we should maybe calculate neighbour positions:

- Right: pos + 1
- Left: pos - 1
- Up: pos + 6
- Down: pos - 6
- Up Right: pos + 7
- Down Right: pos - 5
- Up Left: pos + 5
- Down Left: pos - 7

```cpp
// This has to be implemented with bit shifts, idk how this works yet
```
