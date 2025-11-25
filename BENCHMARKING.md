# Benchmarking

This file's purpose is to track benchmark measurements and list improvements. The base benchmark case will always be running a BFS from the start state with depth 3 and 4.

## First Run (25/11)

### Results

- Total time = 3 min
- states/s = 5.7 /s

This is very bad!! Adding a profiler gives us more information:

```
Total time: 179.05s
States processed: 1,027
Throughput: 5.7 states/sec

__eq__ (board comparison)           ██████████████████████████████████████████████ 163.2s (91%)
move operations                     █ 6.3s (3.5%)
bfs loop overhead                   █ 5.9s (3.3%)
...
```

This is very bad, 90% is taken up by Board comparison. Makes sense.
Solution: implement the `__hash__` function that will convert the board to a int representation.

## Hash function implementation (25/11)

### Solution

Encode the position of each piece into 6 bit (36 possible squares, fits in 2^6 = 64)
Pack into a single 64 bit integer (8 * 6 = 48 fits in 64)

Implement `to_hash()` and `from_hash()` to more efficiently store board states

### Results

 ---- DEPTH = 3 ----

- States per second: 531.4 /s
- Time to complete : 1.594 s
- Number of states : 847

-> 100 times BETTER!

   cum(s)    self(s)   calls        %  name
    1.7 s      0.0 s       1     100%  bfs:10
    0.8 s      0.0 s    1162      45%    move:31
    0.6 s      0.1 s    1162      33%      _update_piece_positions:144
    0.5 s      0.1 s   57855      28%        get_tile_content:121
    0.5 s      0.1 s   57855      28%      get_tile_content:121
    0.5 s      0.3 s    3488      29%    to_hash:205

-> now it seems that the `get_tile_content` is very slow..

 ---- DEPTH = 4 ----

- States per second: 367.7 /s
- Time to complete : 11.690 s
- Number of states : 4298
