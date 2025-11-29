# GDB Primer - Quick Reference

## Starting GDB

```bash
# Start GDB with your test executable
gdb ./build/test_game

# Or run specific test tags
gdb --args ./build/test_game [bitboard]
```

## Basic Commands

### Running Programs
```
run                    # Start program (or r)
run [bitboard]         # Run with Catch2 filter
continue               # Continue execution (or c)
quit                   # Exit GDB (or q)
```

### Breakpoints
```
break test_bitboard.cpp:8     # Set breakpoint at line 8 (or b)
break getBit                   # Break at function name
break bitboard.cpp:15          # Break in source file
info breakpoints               # List all breakpoints (or i b)
delete 1                       # Delete breakpoint #1 (or d)
disable 1                      # Disable breakpoint #1
enable 1                       # Enable breakpoint #1
clear test_bitboard.cpp:8      # Clear breakpoint at line
```

### Stepping Through Code
```
step        # Step into function (or s)
next        # Step over function (or n)
finish      # Step out of current function
until       # Continue until next line (or u)
```

### Inspecting Variables
```
print board              # Print variable value (or p)
print/x board           # Print in hexadecimal
print/d board           # Print in decimal
print/t board           # Print in binary
print *ptr              # Dereference pointer
print arr[5]            # Print array element
info locals             # Show all local variables
info args               # Show function arguments
```

### Stack and Frames
```
backtrace               # Show call stack (or bt)
frame 0                 # Switch to frame 0 (or f)
up                      # Move up stack frame
down                    # Move down stack frame
info frame              # Info about current frame
```

### Useful for Catch2 Tests
```
catch throw             # Break on exceptions
break Catch::handleException  # Break on test failures
run [bitboard]          # Run specific test tag
run "getBit returns correct bit"  # Run specific test name
```

## Quick Debugging Workflow

1. **Start GDB:**
   ```bash
   gdb ./build/test_game
   ```

2. **Set breakpoint:**
   ```
   (gdb) break test_bitboard.cpp:8
   ```

3. **Run:**
   ```
   (gdb) run [bitboard]
   ```

4. **Inspect when stopped:**
   ```
   (gdb) print board
   (gdb) info locals
   ```

5. **Step through:**
   ```
   (gdb) next
   (gdb) step
   ```

6. **Continue:**
   ```
   (gdb) continue
   ```

## Tips

- Use `-g -O0` flags when compiling for better debugging
- `list` shows source code around current line
- `watch variable` breaks when variable changes
- `info registers` shows CPU registers
- `set print pretty on` for better struct/class output
- `help command` shows help for any command
