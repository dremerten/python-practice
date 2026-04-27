# Tutorial: File Renamer Script

We'll build this script one small piece at a time. At each step, read the explanation,
then type the code into `argparse.py` yourself before moving on.

---

## Step 1 — Imports

Open `argparse.py` and type these two lines:

```python
import argparse
import os
```

**What these do:**

- `argparse` — Python's built-in library for reading command-line arguments. Without it,
  you'd have to manually parse `sys.argv`, which gets messy fast.
- `os` — gives you tools to work with the filesystem: list directories, rename files,
  check if paths exist.

Save the file before moving on.

---

## Step 2 — The `main()` function shell

Below your imports, add this:

```python
def main():
    pass
```

And at the very bottom of the file, add:

```python
if __name__ == "__main__":
    main()
```

**Why `if __name__ == "__main__"`?**

When Python runs a file directly (`python argparse.py`), it sets `__name__` to `"__main__"`.
If someone *imports* your file from another script, `__name__` becomes the filename instead,
so `main()` won't accidentally run. This guard is standard on every Python script.

Your file should now look like this:

```python
import argparse
import os

def main():
    pass

if __name__ == "__main__":
    main()
```

---

## Step 3 — Create the parser

Inside `main()`, replace `pass` with:

```python
def main():
    parser = argparse.ArgumentParser(
        description="Rename files in a directory by adding a prefix or suffix"
    )
```

`ArgumentParser` is the object that will read your command-line arguments. The `description`
shows up when the user runs `python argparse.py --help`.

**Try it now:** run this in your terminal to see the help output:

```bash
python argparse.py --help
```

---

## Step 4 — Add the `directory` argument

Still inside `main()`, after creating the parser, add:

```python
    parser.add_argument(
        "directory",
        help="Path to the directory containing files to rename"
    )
```

**Key concept — positional vs optional arguments:**

| Syntax        | Type       | Required? | Usage example                       |
|---------------|------------|-----------|-------------------------------------|
| `"directory"` | positional | always    | `python argparse.py test_files`     |
| `"--prefix"`  | optional   | no        | `python argparse.py --prefix 2024_` |

No `--` means positional. The user must provide it, and the order matters.

---

## Step 5 — Add `--prefix` and `--suffix`

After the `directory` argument, add:

```python
    parser.add_argument(
        "--prefix",
        help="Text to add to the beginning of each filename"
    )
    parser.add_argument(
        "--suffix",
        help="Text to add before the file extension of each filename"
    )
```

If the user doesn't pass `--prefix`, `args.prefix` will be `None` by default.
Same for `--suffix`. That's fine — you'll check for `None` later.

---

## Step 6 — Parse the arguments

After all your `add_argument` calls, add:

```python
    args = parser.parse_args()
```

This is the line that actually reads what the user typed in the terminal and stores the values.
After this line:

- `args.directory` → the directory path they typed
- `args.prefix`   → the prefix text, or `None` if not provided
- `args.suffix`   → the suffix text, or `None` if not provided

Now add a temporary print so you can see it working:

```python
    print(args)
```

Your full file should now look like this:

```python
import argparse
import os

def main():
    parser = argparse.ArgumentParser(
        description="Rename files in a directory by adding a prefix or suffix"
    )

    parser.add_argument(
        "directory",
        help="Path to the directory containing files to rename"
    )
    parser.add_argument(
        "--prefix",
        help="Text to add to the beginning of each filename"
    )
    parser.add_argument(
        "--suffix",
        help="Text to add before the file extension of each filename"
    )

    args = parser.parse_args()
    print(args)

if __name__ == "__main__":
    main()
```

**Try running it several ways and observe the output each time:**

```bash
python argparse.py test_files
python argparse.py test_files --prefix 2024_
python argparse.py test_files --suffix _backup
python argparse.py test_files --prefix 2024_ --suffix _final
python argparse.py --help
```

You should see `args` print something like:
`Namespace(directory='test_files', prefix='2024_', suffix=None)`

---

## Step 7 — Validate the directory

Now that you can read arguments, the first thing to do before touching any files is make sure
the directory actually exists. Add this after `print(args)`:

```python
    if not os.path.isdir(args.directory):
        print(f"Error: '{args.directory}' is not a valid directory.")
        return
```

**What's happening here:**

- `os.path.isdir()` returns `True` if the path exists and is a directory, `False` otherwise.
- If it's invalid, you print a helpful message and `return` early — no need to go further.
- This is called a **guard clause**: handle the bad case first so the rest of the function
  can assume the happy path.

**Try it:**

```bash
python argparse.py fake_directory --prefix 2024_
```

You should see your error message instead of a crash.

---

## Step 8 — List the files

Now list all the files in the directory. Add this after your validation:

```python
    files = [
        f for f in os.listdir(args.directory)
        if os.path.isfile(os.path.join(args.directory, f))
    ]
    print(files)
```

**Breaking this down:**

- `os.listdir(args.directory)` — returns a list of every name in the directory
  (files AND subdirectories).
- `os.path.isfile(os.path.join(args.directory, f))` — filters to files only.
- `os.path.join()` — safely combines the directory path and filename into a full path.
  Always use this instead of string concatenation like `dir + "/" + file`.

**Try it:**

```bash
python argparse.py test_files
```

You should see a list of the five filenames in `test_files/`.

---

## Step 9 — Build the new filename

Now write a separate function that takes a filename and returns the renamed version.
Add this **above** `main()`:

```python
def build_new_name(filename, prefix, suffix):
    name, ext = os.path.splitext(filename)
    new_name = filename

    if prefix:
        new_name = prefix + new_name
    if suffix:
        new_name = name + suffix + ext

    return new_name
```

**What's happening here:**

- `os.path.splitext("report.txt")` → returns `("report", ".txt")` — it splits the name
  from the extension so you can insert the suffix in the right place.
- You handle prefix and suffix independently — the user might pass one, both, or neither.
- `if prefix:` is a clean way to check — `None` and `""` are both falsy, so this handles
  both cases.

**Think about it:** what happens if the user passes both `--prefix` and `--suffix`?
Trace through the function with `filename="report.txt"`, `prefix="2024_"`, `suffix="_final"`.
What should the result be?

---

## Step 10 — Rename the files

Now put it all together. Replace your `print(files)` with a loop that renames each file:

```python
    for filename in files:
        new_name = build_new_name(filename, args.prefix, args.suffix)

        if new_name == filename:
            print(f"Skipped: '{filename}' (no change)")
            continue

        old_path = os.path.join(args.directory, filename)
        new_path = os.path.join(args.directory, new_name)

        os.rename(old_path, new_path)
        print(f"Renamed: '{filename}' -> '{new_name}'")
```

**What's happening here:**

- You build the new name for each file using your function from Step 9.
- If nothing changed (user passed neither prefix nor suffix), you skip it.
- `os.rename(old_path, new_path)` does the actual renaming.
- You print what happened so the user has a clear log of changes.

**Try it:**

```bash
python argparse.py test_files --prefix 2024_
```

Then check `test_files/` to see the renamed files.

---

## Final file

Your completed script should look like this:

```python
import argparse
import os

def build_new_name(filename, prefix, suffix):
    name, ext = os.path.splitext(filename)
    new_name = filename

    if prefix:
        new_name = prefix + new_name
    if suffix:
        new_name = name + suffix + ext

    return new_name

def main():
    parser = argparse.ArgumentParser(
        description="Rename files in a directory by adding a prefix or suffix"
    )

    parser.add_argument(
        "directory",
        help="Path to the directory containing files to rename"
    )
    parser.add_argument(
        "--prefix",
        help="Text to add to the beginning of each filename"
    )
    parser.add_argument(
        "--suffix",
        help="Text to add before the file extension of each filename"
    )

    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print(f"Error: '{args.directory}' is not a valid directory.")
        return

    files = [
        f for f in os.listdir(args.directory)
        if os.path.isfile(os.path.join(args.directory, f))
    ]

    for filename in files:
        new_name = build_new_name(filename, args.prefix, args.suffix)

        if new_name == filename:
            print(f"Skipped: '{filename}' (no change)")
            continue

        old_path = os.path.join(args.directory, filename)
        new_path = os.path.join(args.directory, new_name)

        os.rename(old_path, new_path)
        print(f"Renamed: '{filename}' -> '{new_name}'")

if __name__ == "__main__":
    main()
```

---

## Challenges to try on your own

Once it's working, push yourself further:

1. **Dry run mode** — add a `--dry-run` flag that prints what *would* happen without
   actually renaming anything. Hint: `add_argument("--dry-run", action="store_true")`.

2. **Require at least one** — right now the script runs even if neither `--prefix` nor
   `--suffix` is given. Add a check after `parse_args()` that prints an error if both are `None`.

3. **Undo support** — save a log of renames to a file so you could write a second script
   to reverse them.
