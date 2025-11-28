# Implementation

## Board representation

The idea is to represent the board as 2 `long long`'s (2 * 64 bits)

One for each "bitboard", black and white.
Each bitboard will need 36 bits to store the positions of the pieces.
There are a lot of unused bits (because we can't do 32) that could store other stuff.

So the suggested representation is:

- CURRENT_PLAYER (64 bit)
  - [0-35] currentBitboard (36 bit)
- NEXT_PLAYER (64 bit)
  - [0-35] nextBitboard (36 bit)

We do not encode in the bitboards if it is white or black, we only encore the first player and the second.

This means that there are always 4 states that map to the same state in our representation, by mirroring on both axes:

- Vertical axis: This is obvious, because the game is symmetrical along the vertical axis (going right is the same as going left in the starting position)
- Horizontal axis: This is a bit more difficult to understand, but basically the for each position where white has to play, there exists a position that is fundamentally equal just that black has to play and that the board is mirrored horizontally.

We will call the state to which we map the 4 variations the "base state". The 4 variations are following:

- White to play, right version (base state)
- White to play, left version
- Black to play, right version
- Black to play, left version

This means we can map each state to a base state, dividing the actual state space by four.

## Basic functions

### Get the value of a position

Example: get value from 3 (1000), bitboard = (1001)

1   = ( 1001 & 0001 << 3 ) >> 3
... = (1001 & 1000) >> 3
... = 1000 >> 3
... = 0001

```cpp
value = ( bitboard & ( 1 << position ) ) >> position
```

### Toggle value at position

Example: remove from 0 (0001), bitboard = (1001)

1000 = 1001 ^ 0001 << 0
...  = 1000

```cpp
newBitboard = bitboard ^ ( 1 << position ) 
```

### Move a piece

Example: move from 0 (0001) to 2 (0100), bitboard = (1001)

1100 = 1001 ^ ( 0001 << 0 ) ^ (0001 << 2)
...  = 1001 ^ 0001 ^ 0100
...  = 1000 ^ 0100
...  = 1100

```cpp
newBitboard = bitboard ^ ( 1 << from ) ^ ( 1 << to )
```

## Important functions

### State to base state mapping

To map a state (actual board position + current player) to a base state (current & next bitboard) we need to do 2 things:

#### Map 'black to play' to 'white to play'

If black to play, we need to mirror the position along the horizontal axis and switch the current player.

### Map 'left' to 'right' version

Compute the vertical mirror of the current state and take the smallest of both states bitboards representation, to always map to the 'right' version.

### Get neighbour count

This is necessary when we want to calculate moves. This should be implemented first, as eit is probably quite simple and teach the basics of bit manipulation.

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
// TODO: see ## Basic functions
```
