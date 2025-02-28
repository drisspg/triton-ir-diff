# Triton IR Diff

A command-line tool for generating HTML comparisons of Triton IR files.

## Installation

```bash
pip install triton-ir-diff
```

Or install directly from the repository:

```bash
git clone https://github.com/yourusername/triton-ir-diff.git
cd triton-ir-diff
pip install -e .
```

## Usage

### Compare two files

```bash
triton-ir-diff compare path/to/file1.ttir path/to/file2.llir
```

### Generate comparisons for all IR files in a directory

```bash
triton-ir-diff all path/to/directory
```

This will:
- Find all your IR files (.llir, .ptx, .ttgir, .ttir) in the specified directory
- Generate HTML comparisons for each pair
- Create an index page
- Open the index in your browser

### Options

- `-o, --output`: Specify the output HTML file path (for `compare` command)
- `-o, --output-dir`: Specify the output directory for HTML files (for `all` command)

## Supported File Types

The tool supports the following Triton IR file types:
- `.llir` - LLVM IR
- `.ptx` - NVIDIA PTX
- `.ttgir` - Triton Graph IR
- `.ttir` - Triton IR

Note: `.cubin` files are excluded from comparisons.

## License

MIT