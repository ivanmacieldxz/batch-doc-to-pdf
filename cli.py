import argparse
import os
import sys
from converter import batch_convert_to_pdf

def parse_args():
    parser = argparse.ArgumentParser(
        description="Batch convert .doc and .docx files to .pdf"
    )
    
    parser.add_argument(
        "input_dir",
        type=str,
        nargs="?", # Optional to allow running without args to trigger GUI
        help="The directory containing the Word documents. If omitted, the GUI will launch."
    )
    
    parser.add_argument(
        "-o", "--output-dir",
        type=str,
        help="The directory to save the PDF files. Defaults to ~/batch-doc-to-pdf-out",
        default=None
    )
    
    return parser.parse_args()

def run_cli(args):
    """
    Executes the command-line interface logic.
    """
    input_dir = args.input_dir
    
    if not os.path.isdir(input_dir):
        print(f"Error: The directory '{input_dir}' does not exist or is not a directory.")
        sys.exit(1)
        
    print(f"Starting batch conversion in: {input_dir}")
    if args.output_dir:
        print(f"Output directory: {args.output_dir}")
        
    successful, total = batch_convert_to_pdf(input_dir, args.output_dir)
    
    print("-" * 30)
    print(f"Conversion complete!")
    print(f"Successfully converted {successful} out of {total} files.")
    
    if successful < total:
        sys.exit(1)
    else:
        sys.exit(0)
