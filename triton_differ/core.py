"""
Core functionality for triton_differ.
"""

import os
import sys
import difflib
from pathlib import Path

# Import the HTML utilities
from triton_differ.html_utils import create_github_style_diff, generate_index_html_content

def read_file(file_path):
    """Read the content of a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.readlines()
    except UnicodeDecodeError:
        # If UTF-8 fails, try with ISO-8859-1 which can read any byte sequence
        with open(file_path, 'r', encoding='ISO-8859-1') as file:
            return file.readlines()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        sys.exit(1)

def generate_html_diff(file1_path, file2_path, output_path=None):
    """Generate an HTML diff between two files."""
    # If no output path specified, create a temporary one
    if output_path is None:
        file1_name = os.path.basename(file1_path)
        file2_name = os.path.basename(file2_path)
        output_path = f"comparison_{file1_name}_vs_{file2_name}.html"

    # Use the new create_github_style_diff function
    result_path = create_github_style_diff(file1_path, file2_path, output_path)
    return result_path

def list_ir_files(directory):
    """List all IR files in the given directory."""
    valid_extensions = ['.llir', '.ptx', '.ttgir', '.ttir']
    ir_files = []

    try:
        for file in os.listdir(directory):
            file_path = os.path.join(directory, file)
            if os.path.isfile(file_path):
                _, ext = os.path.splitext(file)
                if ext in valid_extensions:
                    ir_files.append(file_path)
    except Exception as e:
        print(f"Error listing files in directory {directory}: {e}")
        sys.exit(1)

    return ir_files

def compare_directories(dir1, dir2, output_dir=None):
    """Compare IR files with matching names between two directories."""
    # Get lists of IR files in both directories
    ir_files1 = list_ir_files(dir1)
    ir_files2 = list_ir_files(dir2)

    # Print found files for debugging
    print(f"Found {len(ir_files1)} IR files in {dir1}:")
    for f in ir_files1:
        print(f"  - {os.path.basename(f)}")
    print(f"Found {len(ir_files2)} IR files in {dir2}:")
    for f in ir_files2:
        print(f"  - {os.path.basename(f)}")

    # Extract basenames for easier matching
    basenames1 = {os.path.basename(f): f for f in ir_files1}
    basenames2 = {os.path.basename(f): f for f in ir_files2}

    # Find common filenames with same extension
    common_files = []
    for name1, path1 in basenames1.items():
        if name1 in basenames2:
            common_files.append((name1, path1, basenames2[name1]))

    if not common_files:
        print("No matching IR files found between the directories")
        return []

    # Create output directory if specified
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    # Generate comparisons for matching files
    comparisons = []
    for basename, path1, path2 in common_files:
        if output_dir:
            output_path = os.path.join(output_dir, f"comparison_{basename}.html")
        else:
            output_path = None

        result_path = generate_html_diff(path1, path2, output_path)
        dir1_name = os.path.basename(dir1)
        dir2_name = os.path.basename(dir2)
        comparisons.append((f"{dir1_name}/{basename}", f"{dir2_name}/{basename}", result_path))

    return comparisons

def generate_all_comparisons(directory, output_dir=None):
    """Generate HTML comparisons for IR files with matching suffixes in the directory."""
    ir_files = list_ir_files(directory)

    # Group files by their suffix
    suffix_groups = {}
    for file_path in ir_files:
        _, suffix = os.path.splitext(file_path)
        if suffix not in suffix_groups:
            suffix_groups[suffix] = []
        suffix_groups[suffix].append(file_path)

    # Create output directory if it doesn't exist
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    # Generate comparison for each pair of files with the same suffix
    comparisons = []
    for suffix, files in suffix_groups.items():
        for i in range(len(files)):
            for j in range(i+1, len(files)):
                file1 = files[i]
                file2 = files[j]

                file1_name = os.path.basename(file1)
                file2_name = os.path.basename(file2)

                if output_dir:
                    output_path = os.path.join(output_dir, f"comparison_{file1_name}_vs_{file2_name}.html")
                else:
                    output_path = None

                result_path = generate_html_diff(file1, file2, output_path)
                comparisons.append((file1_name, file2_name, result_path))
    return comparisons

def generate_index_html(comparisons, output_dir=None):
    """Generate an index HTML file that links to all comparisons."""
    html_content = generate_index_html_content(comparisons)

    # Save the index HTML
    if output_dir:
        index_path = os.path.join(output_dir, "index.html")
    else:
        index_path = "ir_comparisons_index.html"

    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    return index_path