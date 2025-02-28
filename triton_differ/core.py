"""
Core functionality for triton_differ.
"""

import os
import sys
import difflib
from pathlib import Path

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
    # Get file names for display
    file1_name = os.path.basename(file1_path)
    file2_name = os.path.basename(file2_path)

    # Read file contents
    file1_lines = read_file(file1_path)
    file2_lines = read_file(file2_path)

    # Generate diff
    diff = difflib.HtmlDiff(tabsize=4)
    html_diff = diff.make_file(file1_lines, file2_lines,
                              file1_name, file2_name,
                              context=True, numlines=3)

    # Enhance the HTML with better styling
    enhanced_html = enhance_html_styling(html_diff, file1_name, file2_name)

    # Save or return the HTML
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(enhanced_html)
        return output_path
    else:
        # Create a temporary file
        temp_path = f"comparison_{file1_name}_vs_{file2_name}.html"
        with open(temp_path, 'w', encoding='utf-8') as f:
            f.write(enhanced_html)
        return temp_path

def enhance_html_styling(html_content, file1_name, file2_name):
    """Enhance the styling of the HTML diff output."""
    # Add a more modern style and responsive design
    style = """
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }

        .header {
            background-color: #333;
            color: white;
            padding: 15px;
            text-align: center;
            border-radius: 5px 5px 0 0;
            margin-bottom: 20px;
        }

        .container {
            max-width: 95%;
            margin: 0 auto;
            background-color: white;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            border-radius: 5px;
            padding: 20px;
        }

        table.diff {
            width: 100%;
            border-collapse: collapse;
            font-family: 'Courier New', Courier, monospace;
            font-size: 14px;
        }

        .diff_header {
            background-color: #f8f8f8;
            font-weight: bold;
            position: sticky;
            top: 0;
            z-index: 1;
        }

        td.diff_header {
            text-align: center;
        }

        .diff_next {
            background-color: #f8f8f8;
            border: 1px solid #ddd;
        }

        td {
            padding: 5px;
            border: 1px solid #ddd;
            vertical-align: top;
            white-space: pre-wrap;
            word-wrap: break-word;
            max-width: 50%;
        }

        /* Changed lines */
        .diff_add {
            background-color: #e6ffed;
        }

        .diff_chg {
            background-color: #fff5b1;
        }

        .diff_sub {
            background-color: #ffeef0;
        }

        /* Line numbers */
        .line-num {
            color: #999;
            background-color: #f8f8f8;
            text-align: right;
            width: 40px;
            padding-right: 10px;
        }

        /* Responsive */
        @media screen and (max-width: 768px) {
            body {
                padding: 10px;
            }

            table.diff {
                font-size: 12px;
            }

            td {
                padding: 3px;
            }
        }
    </style>
    """

    # Add a custom header
    header = f"""
    <div class="header">
        <h1>File Comparison</h1>
        <p>Comparing <strong>{file1_name}</strong> with <strong>{file2_name}</strong></p>
    </div>
    <div class="container">
    """

    # Add a closing div for the container
    footer = "</div>"

    # Find the position to insert our custom styles (after the existing style tag)
    style_end_pos = html_content.find("</style>") + 8
    modified_html = html_content[:style_end_pos] + style + html_content[style_end_pos:]

    # Find where to insert our header (after the body tag)
    body_start_pos = modified_html.find("<body>") + 6
    modified_html = modified_html[:body_start_pos] + header + modified_html[body_start_pos:]

    # Insert the footer before the closing body tag
    body_end_pos = modified_html.find("</body>")
    modified_html = modified_html[:body_end_pos] + footer + modified_html[body_end_pos:]

    return modified_html

def list_ir_files(directory):
    """List all IR files in the given directory (excluding .cubin files)."""
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

def generate_all_comparisons(directory, output_dir=None):
    """Generate HTML comparisons for all combinations of IR files in the directory."""
    ir_files = list_ir_files(directory)

    # Create output directory if it doesn't exist
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    # Generate comparison for each pair of files
    comparisons = []
    for i in range(len(ir_files)):
        for j in range(i+1, len(ir_files)):
            file1 = ir_files[i]
            file2 = ir_files[j]

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
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>IR File Comparisons</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                margin: 0;
                padding: 20px;
                background-color: #f5f5f5;
            }

            .header {
                background-color: #333;
                color: white;
                padding: 15px;
                text-align: center;
                border-radius: 5px 5px 0 0;
            }

            .container {
                max-width: 800px;
                margin: 0 auto;
                background-color: white;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                border-radius: 5px;
                padding: 20px;
            }

            .comparison-list {
                list-style: none;
                padding: 0;
            }

            .comparison-item {
                margin-bottom: 10px;
                padding: 10px;
                background-color: #f8f8f8;
                border-radius: 5px;
                transition: background-color 0.3s;
            }

            .comparison-item:hover {
                background-color: #eaeaea;
            }

            .comparison-item a {
                color: #0366d6;
                text-decoration: none;
                display: block;
            }

            .comparison-item a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>IR File Comparisons</h1>
            <p>Select a comparison to view</p>
        </div>
        <div class="container">
            <ul class="comparison-list">
    """

    for file1, file2, path in comparisons:
        relative_path = os.path.basename(path)
        html_content += f"""
                <li class="comparison-item">
                    <a href="{relative_path}">{file1} vs {file2}</a>
                </li>
        """

    html_content += """
            </ul>
        </div>
    </body>
    </html>
    """

    # Save the index HTML
    if output_dir:
        index_path = os.path.join(output_dir, "index.html")
    else:
        index_path = "ir_comparisons_index.html"

    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    return index_path