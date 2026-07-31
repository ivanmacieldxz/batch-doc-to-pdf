# Batch Doc to PDF Converter

A simple tool to batch convert `.doc` and `.docx` files to `.pdf` within a selected folder.

## Features
- **Command Line Interface (CLI):** Automate conversions in scripts or use it quickly from the terminal.
- **Graphical User Interface (GUI):** A modern, easy-to-use interface to select folders and track conversion progress.
- **Robust Conversion:** Uses LibreOffice under the hood for accurate formatting preservation.

## Prerequisites
- **Python 3.x**
- **LibreOffice:** Must be installed on your system.

## Usage

### Command Line Interface (CLI)

To run the converter from the terminal, provide the input directory containing your `.doc` or `.docx` files:

```bash
python main.py /path/to/input/directory
```

By default, the converted `.pdf` files will be saved in `~/batch-doc-to-pdf-out`. You can specify a different output directory using the `-o` or `--output-dir` flag:

```bash
python main.py /path/to/input/directory -o /path/to/output/directory
```

### Graphical User Interface (GUI)

To use the graphical interface, you need to install the dependencies first. We use `customtkinter` for a modern look:

```bash
pip install -r requirements.txt
```

Once installed, simply run the main script without any arguments:

```bash
python main.py
```

This will open a window where you can select the input folder, optionally choose an output folder, and track the conversion progress visually.
