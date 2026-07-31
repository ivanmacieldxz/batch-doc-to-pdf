import os
import threading
import customtkinter as ctk
from tkinter import filedialog, messagebox
from converter import batch_convert_to_pdf

# Setup appearance
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Batch Doc to PDF Converter")
        self.geometry("750x550")
        self.resizable(False, False)
        
        self.input_dir = ""
        self.output_dir = ""
        
        # Define fonts
        self.title_font = ctk.CTkFont(family="Roboto", size=32, weight="bold")
        self.btn_font = ctk.CTkFont(family="Roboto", size=18, weight="bold")
        self.label_font = ctk.CTkFont(family="Roboto", size=16)
        self.path_font = ctk.CTkFont(family="Roboto", size=14, slant="italic")
        
        self.create_widgets()
        
    def create_widgets(self):
        # Title
        self.title_label = ctk.CTkLabel(self, text="Doc to PDF Converter", font=self.title_font)
        self.title_label.pack(pady=(40, 30))
        
        # Main Card Frame for Inputs
        self.card_frame = ctk.CTkFrame(self, corner_radius=15)
        self.card_frame.pack(pady=10, padx=40, fill="both", expand=True)
        
        # Input Section
        self.input_frame = ctk.CTkFrame(self.card_frame, fg_color="transparent")
        self.input_frame.pack(pady=(30, 15), padx=30, fill="x")
        
        self.input_btn = ctk.CTkButton(self.input_frame, text="Select Input Folder", font=self.btn_font, height=45, width=220, command=self.select_input_dir)
        self.input_btn.pack(side="left", padx=(0, 20))
        
        self.input_label = ctk.CTkLabel(self.input_frame, text="No folder selected", text_color="gray", font=self.path_font, wraplength=350, justify="left")
        self.input_label.pack(side="left")
        
        # Output Section
        self.output_frame = ctk.CTkFrame(self.card_frame, fg_color="transparent")
        self.output_frame.pack(pady=(15, 30), padx=30, fill="x")
        
        self.output_btn = ctk.CTkButton(self.output_frame, text="Output Folder (Opt)", font=self.btn_font, height=45, width=220, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.select_output_dir)
        self.output_btn.pack(side="left", padx=(0, 20))
        
        self.output_label = ctk.CTkLabel(self.output_frame, text="Default: ~/batch-doc-to-pdf-out", text_color="gray", font=self.path_font, wraplength=350, justify="left")
        self.output_label.pack(side="left")
        
        # Progress Section
        self.progress_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.progress_frame.pack(pady=(10, 30), padx=40, fill="x")
        
        self.progress_label = ctk.CTkLabel(self.progress_frame, text="Ready to convert", font=self.label_font)
        self.progress_label.pack(pady=(0, 10))
        
        self.progressbar = ctk.CTkProgressBar(self.progress_frame, height=15, corner_radius=10)
        self.progressbar.pack(fill="x")
        self.progressbar.set(0)
        
        # Convert Button
        self.convert_btn = ctk.CTkButton(self, text="Start Conversion", font=ctk.CTkFont(family="Roboto", size=22, weight="bold"), height=60, width=300, fg_color="#28a745", hover_color="#218838", command=self.start_conversion)
        self.convert_btn.pack(pady=(0, 40))
        
    def ask_directory(self, title):
        import platform
        import subprocess
        if platform.system() == "Linux":
            try:
                # Use native GTK dialog on Linux via zenity for a modern look
                result = subprocess.run(["zenity", "--file-selection", "--directory", f"--title={title}"], capture_output=True, text=True)
                if result.returncode == 0:
                    return result.stdout.strip()
                elif result.returncode == 1:
                    return "" # User cancelled
            except FileNotFoundError:
                pass # Zenity not found, fallback to tkinter
                
        # Fallback to default tkinter dialog
        return filedialog.askdirectory(title=title)

    def select_input_dir(self):
        directory = self.ask_directory("Select Input Folder")
        if directory:
            self.input_dir = directory
            self.input_label.configure(text=self.input_dir, text_color=("black", "white"))
            
    def select_output_dir(self):
        directory = self.ask_directory("Select Output Folder")
        if directory:
            self.output_dir = directory
            self.output_label.configure(text=self.output_dir, text_color=("black", "white"))
            
    def update_progress(self, current, total, filename):
        def update_ui():
            progress = current / total
            self.progressbar.set(progress)
            self.progress_label.configure(text=f"Converting: {filename} ({current}/{total})")
            
        self.after(0, update_ui)
        
    def conversion_thread(self):
        out_dir = self.output_dir if self.output_dir else None
        
        try:
            successful, total = batch_convert_to_pdf(self.input_dir, out_dir, progress_callback=self.update_progress)
            
            def finalize_ui():
                self.progress_label.configure(text=f"Done! Successfully converted {successful}/{total} files.")
                self.convert_btn.configure(state="normal", fg_color="#28a745")
                self.input_btn.configure(state="normal")
                self.output_btn.configure(state="normal")
                messagebox.showinfo("Conversion Complete", f"Successfully converted {successful} out of {total} files.")
                
            self.after(0, finalize_ui)
            
        except Exception as e:
            def error_ui():
                self.progress_label.configure(text="Error occurred during conversion.")
                self.convert_btn.configure(state="normal", fg_color="#28a745")
                self.input_btn.configure(state="normal")
                self.output_btn.configure(state="normal")
                messagebox.showerror("Error", f"An unexpected error occurred:\n{str(e)}")
                
            self.after(0, error_ui)

    def start_conversion(self):
        if not self.input_dir:
            messagebox.showwarning("Warning", "Please select an input folder first.")
            return
            
        # Disable buttons during conversion
        self.convert_btn.configure(state="disabled", fg_color="gray")
        self.input_btn.configure(state="disabled")
        self.output_btn.configure(state="disabled")
        
        self.progressbar.set(0)
        self.progress_label.configure(text="Starting conversion...")
        
        threading.Thread(target=self.conversion_thread, daemon=True).start()

def run_gui():
    app = App()
    app.mainloop()

if __name__ == "__main__":
    run_gui()
