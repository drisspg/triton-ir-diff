"""
Command line interface for triton_differ.
"""

import os
import sys
import argparse
import webbrowser

from triton_differ.core import (
    generate_html_diff,
    compare_directories,
    generate_index_html,
)


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Generate HTML comparisons of Triton IR files."
    )

    # Simplified interface with just two positional arguments
    parser.add_argument("path1", help="First file or directory to compare")
    parser.add_argument("path2", help="Second file or directory to compare")
    parser.add_argument(
        "-o", "--output", help="Output file or directory for HTML files"
    )

    args = parser.parse_args()

    # Check if the paths exist
    if not os.path.exists(args.path1):
        print(f"Error: '{args.path1}' does not exist")
        sys.exit(1)

    if not os.path.exists(args.path2):
        print(f"Error: '{args.path2}' does not exist")
        sys.exit(1)

    # Determine if the arguments are files or directories
    is_path1_dir = os.path.isdir(args.path1)
    is_path2_dir = os.path.isdir(args.path2)

    # Case 1: Both are files - compare them directly
    if not is_path1_dir and not is_path2_dir:
        output_path = generate_html_diff(args.path1, args.path2, args.output)
        print(f"Comparison saved to: {output_path}")
        webbrowser.open(f"file://{os.path.abspath(output_path)}")

    # Case 2: Both are directories - compare matching files between them
    elif is_path1_dir and is_path2_dir:
        # Create output directory if specified and doesn't exist
        if args.output:
            os.makedirs(args.output, exist_ok=True)

        comparisons = compare_directories(args.path1, args.path2, args.output)

        if comparisons:
            index_path = generate_index_html(comparisons, args.output)
            print(f"Generated {len(comparisons)} comparisons")
            print(f"Index page saved to: {index_path}")
            webbrowser.open(f"file://{os.path.abspath(index_path)}")
        else:
            print("No matching IR files found for comparison")

    # Case 3: One is a file, one is a directory - not supported
    else:
        print("Error: Cannot compare a file with a directory")
        print("Please provide either two files or two directories")
        sys.exit(1)


if __name__ == "__main__":
    main()