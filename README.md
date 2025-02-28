# Triton Differ

A command-line tool for generating HTML comparisons of Triton IR files.

## Installation

Or install directly from the repository:

```bash
git clone https://github.com/yourusername/triton-ir-diff.git
cd triton_differ
pip install -e .
```

## Usage

### Compare two files

```bash
triton_differ path/to/file1.ttir path/to/file2.ttir
```

### Generate comparisons for all IR files in a directory

```bash
triton_differ good/ bad/
```

This will:
- Find all your IR files (.llir, .ptx, .ttgir, .ttir) in the specified directory
- Generate HTML comparisons for each pair
- Create an index page
- Open the index in your browser

### Options

- `-o, --output-dir`: Specify the output directory for HTML files

## Supported File Types

The tool supports the following Triton IR file types:
- `.llir` - LLVM IR
- `.ptx` - NVIDIA PTX
- `.ttgir` - Triton Graph IR
- `.ttir` - Triton IR

Note: `.cubin` files are excluded from comparisons.

## License

MIT