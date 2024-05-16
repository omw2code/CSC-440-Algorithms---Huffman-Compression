# Huffman Compression

This repository contains Python code for Huffman compression and decompression algorithms. Huffman coding is a popular lossless data compression algorithm that uses variable-length codes to encode data. It achieves compression by assigning shorter codes to more frequent symbols and longer codes to less frequent symbols.

## Features

- **Compression:** Compresses raw sequence of bytes using Huffman encoding algorithm.
- **Decompression:** Decompresses encoded message using Huffman decoding algorithm.
- **File I/O:** Reads from and writes to files for compression and decompression operations.
- **CLI Interface:** Provides a command-line interface for easy compression and decompression of files.

## Usage

```bash
python huffman.py [OPTIONS] infile outfile
```

### Options

- `-c`: Compress infile and write compressed data to outfile.
- `-d`: Decompress infile and write decompressed data to outfile.
- `-v`: View the encoded message without compression.
- `-w`: View the decoded message without decompression.

### Examples

Compress a file:

```bash
python huffman.py -c input.txt output.bin
```

Decompress a file:

```bash
python huffman.py -d input.bin output.txt
```

## Installation

Clone the repository:

```bash
git clone https://github.com/your_username/huffman-compression.git
```

## Requirements

- Python 3.x


## Support
For any issues or inquiries, please contact brennnanrivera0@gmail.com.
