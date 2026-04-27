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

