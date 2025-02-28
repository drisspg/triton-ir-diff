"""
Command line interface for triton-ir-diff.
"""

import os
import sys
import argparse
import webbrowser

from triton_differ.core import (
    generate_html_diff,
    generate_all_comparisons,
    generate_index_html
)

def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description='Generate HTML comparisons of Triton IR files.')

    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    # Compare two files
    compare_parser = subparsers.add_parser('compare', help='Compare two files')
    compare_parser.add_argument('file1', help='First file to compare')
    compare_parser.add_argument('file2', help='Second file to compare')
    compare_parser.add_argument('-o', '--output', help='Output HTML file path')

    # Compare all files in a directory
    all_parser = subparsers.add_parser('all', help='Generate comparisons for all IR files in a directory')
    all_parser.add_argument('directory', help='Directory containing IR files')
    all_parser.add_argument('-o', '--output-dir', help='Output directory for HTML files')

    args = parser.parse_args()

    if args.command == 'compare':
        output_path = generate_html_diff(args.file1, args.file2, args.output)
        print(f"Comparison saved to: {output_path}")
        webbrowser.open(f"file://{os.path.abspath(output_path)}")

    elif args.command == 'all':
        comparisons = generate_all_comparisons(args.directory, args.output_dir)
        if comparisons:
            index_path = generate_index_html(comparisons, args.output_dir)
            print(f"Generated {len(comparisons)} comparisons")
            print(f"Index page saved to: {index_path}")
            webbrowser.open(f"file://{os.path.abspath(index_path)}")
        else:
            print("No IR files found for comparison")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()