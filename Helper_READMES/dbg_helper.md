## Python pdb Cheat Sheet

#### Start Debugger
```
python -m pdb script.py       # Run script in debugger
```
#### Execution Control
```
c           # Continue execution until next breakpoint or program ends
n           # Next line (don’t step into functions)
s           # Step into function
r           # Step out of current function
until       # Run until a specific line
```
#### Breakpoints
```
b 25                    # Set breakpoint at line 25
b analyze_logs           # Set breakpoint at function analyze_logs
b 30, log_level == "ERROR"  # Conditional breakpoint
b                        # List all breakpoints
cl 1                     # Clear breakpoint #1
cl                       # Clear all breakpoints
```

#### Inspecting Data
```
p variable               # Print variable value
pp variable              # Pretty-print variable (good for JSON/YAML)
p len(meta)              # Evaluate expression
locals()                  # Show local variables
globals()                 # Show global variables
```

#### Navigation
```
l                        # List current lines of code
l 20                     # List lines around line 20
w / where                # Show current stack position
u                        # Move up the stack
d                        # Move down the stack
```

#### Advanced
```
j 50                     # Jump to line 50 (dangerous)
run                      # Restart script
run newfile.log          # Restart script with arguments
q                        # Quit debugger
```

#### Example Workflow (Log Parsing)
```
b analyze_logs            # Break at function
c                         # Continue to breakpoint
n                         # Step line-by-line
p line                    # Inspect current line
p parts                   # Inspect split parts
p meta                    # Inspect meta information
until                      # Run until next point of interest
b 30, "ERROR" in line      # Break only on ERROR lines
```