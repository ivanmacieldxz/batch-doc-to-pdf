import os
import subprocess
import glob
from typing import List, Tuple

def convert_file_to_pdf(input_path: str, output_dir: str) -> bool:
    """
    Converts a single .doc or .docx file to PDF using LibreOffice.
    
    :param input_path: The absolute or relative path to the input document.
    :param output_dir: The directory where the PDF should be saved.
    :return: True if conversion succeeded, False otherwise.
    """
    try:
        # Construct the libreoffice headless command
        command = [
            "libreoffice",
            "--headless",
            "--convert-to", "pdf",
            "--outdir", output_dir,
            input_path
        ]
        
        # Run the command and capture output
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        if result.returncode == 0:
            # Libreoffice saves the file replacing the extension with .pdf
            base_name = os.path.splitext(os.path.basename(input_path))[0]
            pdf_path = os.path.join(output_dir, base_name + ".pdf")
            
            # Preserve original timestamps
            if os.path.exists(pdf_path):
                original_stat = os.stat(input_path)
                os.utime(pdf_path, (original_stat.st_atime, original_stat.st_mtime))
                
            return True
        else:
            print(f"Error converting {input_path}:\n{result.stderr}")
            return False
            
    except Exception as e:
        print(f"An unexpected error occurred while converting {input_path}: {e}")
        return False

def get_word_documents(directory: str) -> List[str]:
    """
    Finds all .doc and .docx files in a given directory.
    
    :param directory: The directory to search.
    :return: A list of file paths.
    """
    docs = []
    # Search for .doc and .docx in the directory (case insensitive match on linux requires checking extensions)
    for filename in os.listdir(directory):
        if filename.lower().endswith(('.doc', '.docx')) and not filename.startswith('~'):
            docs.append(os.path.join(directory, filename))
            
    # Sort files by creation date (or modification date as fallback on Linux)
    def get_creation_time(filepath):
        stat = os.stat(filepath)
        try:
            return stat.st_birthtime
        except AttributeError:
            return stat.st_mtime
            
    docs.sort(key=get_creation_time)
    
    return docs

def batch_convert_to_pdf(input_dir: str, output_dir: str = None, progress_callback=None) -> Tuple[int, int]:
    """
    Converts all Word documents in the input directory to PDF.
    
    :param input_dir: Directory containing .doc/.docx files.
    :param output_dir: Directory to save PDFs (defaults to ~/batch-doc-to-pdf-out).
    :param progress_callback: Optional callable func(current_idx, total_files, filename)
    :return: A tuple of (successful_conversions, total_files)
    """
    if output_dir is None:
        output_dir = os.path.join(os.path.expanduser("~"), "batch-doc-to-pdf-out")
        
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
        
    files_to_convert = get_word_documents(input_dir)
    total_files = len(files_to_convert)
    successful = 0
    
    if total_files == 0:
        print(f"No .doc or .docx files found in {input_dir}")
        return 0, 0
        
    for i, file_path in enumerate(files_to_convert, 1):
        filename = os.path.basename(file_path)
        print(f"[{i}/{total_files}] Converting {filename}...")
        
        if progress_callback:
            progress_callback(i, total_files, filename)
            
        if convert_file_to_pdf(file_path, output_dir):
            successful += 1
            
    return successful, total_files
