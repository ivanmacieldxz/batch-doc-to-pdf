import os
import threading
import customtkinter as ctk
from tkinter import filedialog, messagebox
from converter import batch_convert_to_pdf

# Setup appearance
ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Batch Doc to PDF Converter")
        self.geometry("600x400")
        self.resizable(False, False)
        
        self.input_dir = ""
        self.output_dir = ""
        
        self.create_widgets()
        
    def create_widgets(self):
        # Title Label
        self.title_label = ctk.CTkLabel(self, text="Convert Word Documents to PDF", font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.pack(pady=(20, 10))
        
        # Frame for Input
        self.input_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.input_frame.pack(pady=10, padx=20, fill="x")
        
        self.input_btn = ctk.CTkButton(self.input_frame, text="Select Input Folder", command=self.select_input_dir)
        self.input_btn.pack(side="left", padx=(0, 10))
        
        self.input_label = ctk.CTkLabel(self.input_frame, text="No folder selected", text_color="gray")
        self.input_label.pack(side="left")
        
        # Frame for Output
        self.output_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.output_frame.pack(pady=10, padx=20, fill="x")
        
        self.output_btn = ctk.CTkButton(self.output_frame, text="Select Output Folder (Optional)", command=self.select_output_dir)
        self.output_btn.pack(side="left", padx=(0, 10))
        
        self.output_label = ctk.CTkLabel(self.output_frame, text="Default: ~/batch-doc-to-pdf-out", text_color="gray")
        self.output_label.pack(side="left")
        
        # Progress Bar and Label
        self.progress_label = ctk.CTkLabel(self, text="Ready", font=ctk.CTkFont(size=12))
        self.progress_label.pack(pady=(30, 5))
        
        self.progressbar = ctk.CTkProgressBar(self, width=400)
        self.progressbar.pack(pady=(0, 20))
        self.progressbar.set(0)
        
        # Convert Button
        self.convert_btn = ctk.CTkButton(self, text="Start Conversion", font=ctk.CTkFont(size=15, weight="bold"), command=self.start_conversion)
        self.convert_btn.pack(pady=10)
        
    def select_input_dir(self):
        directory = filedialog.askdirectory(title="Select Input Folder")
        if directory:
            self.input_dir = directory
            self.input_label.configure(text=self.input_dir, text_color="white")
            
    def select_output_dir(self):
        directory = filedialog.askdirectory(title="Select Output Folder")
        if directory:
            self.output_dir = directory
            self.output_label.configure(text=self.output_dir, text_color="white")
            
    def update_progress(self, current, total, filename):
        # This callback can be called from the worker thread, so we schedule UI updates safely
        # Note: customtkinter/tkinter allows some calls from threads, but using after is safer.
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
                self.convert_btn.configure(state="normal")
                self.input_btn.configure(state="normal")
                self.output_btn.configure(state="normal")
                messagebox.showinfo("Conversion Complete", f"Successfully converted {successful} out of {total} files.")
                
            self.after(0, finalize_ui)
            
        except Exception as e:
            def error_ui():
                self.progress_label.configure(text="Error occurred during conversion.")
                self.convert_btn.configure(state="normal")
                self.input_btn.configure(state="normal")
                self.output_btn.configure(state="normal")
                messagebox.showerror("Error", f"An unexpected error occurred:\n{str(e)}")
                
            self.after(0, error_ui)

    def start_conversion(self):
        if not self.input_dir:
            messagebox.showwarning("Warning", "Please select an input folder first.")
            return
            
        # Disable buttons during conversion
        self.convert_btn.configure(state="disabled")
        self.input_btn.configure(state="disabled")
        self.output_btn.configure(state="disabled")
        
        self.progressbar.set(0)
        self.progress_label.configure(text="Starting conversion...")
        
        # Start conversion in a separate thread to keep UI responsive
        threading.Thread(target=self.conversion_thread, daemon=True).start()

def run_gui():
    app = App()
    app.mainloop()

if __name__ == "__main__":
    run_gui()
