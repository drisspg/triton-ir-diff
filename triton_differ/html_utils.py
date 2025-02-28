import os
import difflib
from pathlib import Path
import re

def create_github_style_diff(file1_path, file2_path, output_path):
    """
    Generate a GitHub-style HTML diff between two files using Python's built-in difflib
    with enhanced styling to look more like GitHub's diff view.
    """
    # Read file contents
    with open(file1_path, 'r', encoding='utf-8', errors='replace') as f:
        file1_lines = f.readlines()
    with open(file2_path, 'r', encoding='utf-8', errors='replace') as f:
        file2_lines = f.readlines()

    # Get file names for display
    file1_name = os.path.basename(file1_path)
    file2_name = os.path.basename(file2_path)

    # Generate diff HTML using difflib
    diff = difflib.HtmlDiff(tabsize=4)
    html_diff = diff.make_file(file1_lines, file2_lines, file1_name, file2_name, context=True)

    # Enhance with GitHub-style CSS
    github_styled_html = html_diff

    # Write the result
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(github_styled_html)

    return output_path

def generate_index_html_content(comparisons):
    """
    Generate HTML content for an index page that links to all comparisons.

    Args:
        comparisons: List of tuples (file1_name, file2_name, comparison_path)

    Returns:
        HTML content as a string
    """
    html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>IR Comparisons Index</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
            line-height: 1.5;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        h1 {
            border-bottom: 1px solid #eaecef;
            padding-bottom: 10px;
        }
        table {
            border-collapse: collapse;
            width: 100%;
        }
        th, td {
            text-align: left;
            padding: 12px;
            border: 1px solid #dfe2e5;
        }
        th {
            background-color: #f6f8fa;
        }
        tr:nth-child(even) {
            background-color: #f6f8fa;
        }
        tr:hover {
            background-color: #f0f0f0;
        }
        a {
            color: #0366d6;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <h1>IR Comparisons Index</h1>
    <table>
        <tr>
            <th>File 1</th>
            <th>File 2</th>
            <th>Comparison</th>
        </tr>
"""

    # Add a row for each comparison
    for file1, file2, comp_path in comparisons:
        comp_basename = os.path.basename(comp_path)
        html += f"""
        <tr>
            <td>{file1}</td>
            <td>{file2}</td>
            <td><a href="{comp_basename}" target="_blank">View Diff</a></td>
        </tr>"""

    html += """
    </table>
</body>
</html>
"""
    return html
