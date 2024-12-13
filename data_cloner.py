import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import shutil
import os
import threading
import time
from datetime import datetime

class DataCloner:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Cloner")
        self.root.geometry("600x450")
        
        # Quellpfad
        source_frame = ttk.LabelFrame(root, text="Quellverzeichnis", padding="5")
        source_frame.pack(fill="x", padx=5, pady=5)
        
        self.source_path = tk.StringVar()
        ttk.Entry(source_frame, textvariable=self.source_path, width=50).pack(side="left", padx=5)
        ttk.Button(source_frame, text="Durchsuchen", command=self.browse_source).pack(side="left", padx=5)
        
        # Zielpfad
        dest_frame = ttk.LabelFrame(root, text="Zielverzeichnis", padding="5")
        dest_frame.pack(fill="x", padx=5, pady=5)
        
        self.dest_path = tk.StringVar()
        ttk.Entry(dest_frame, textvariable=self.dest_path, width=50).pack(side="left", padx=5)
        ttk.Button(dest_frame, text="Durchsuchen", command=self.browse_dest).pack(side="left", padx=5)
        
        # Fortschrittsanzeige
        self.progress_var = tk.DoubleVar()
        self.progress = ttk.Progressbar(root, variable=self.progress_var, maximum=100)
        self.progress.pack(fill="x", padx=5, pady=5)
        
        # Zeit Label
        self.time_label = ttk.Label(root, text="Geschätzte Zeit: --:--:--")
        self.time_label.pack(pady=2)
        
        # Status Label
        self.status_label = ttk.Label(root, text="Bereit")
        self.status_label.pack(pady=2)
        
        # Start Button
        self.start_button = ttk.Button(root, text="Kopieren starten", command=self.start_copy)
        self.start_button.pack(pady=5)
        
        # Footer
        footer_frame = ttk.Frame(root)
        footer_frame.pack(side="bottom", fill="x", pady=10)
        footer_label = ttk.Label(footer_frame, text="Powered by chill-zone.xyz", font=("Arial", 8))
        footer_label.pack(side="right", padx=10)
        
        self.start_time = None
        
    def browse_source(self):
        path = filedialog.askdirectory()
        if path:
            self.source_path.set(path)
            
    def browse_dest(self):
        path = filedialog.askdirectory()
        if path:
            self.dest_path.set(path)
    
    def update_progress(self, current, total):
        progress = (current / total) * 100
        self.progress_var.set(progress)
        
        if self.start_time and current > 0:
            elapsed_time = time.time() - self.start_time
            estimated_total_time = (elapsed_time / current) * total
            remaining_time = estimated_total_time - elapsed_time
            
            # Formatiere die verbleibende Zeit
            hours = int(remaining_time // 3600)
            minutes = int((remaining_time % 3600) // 60)
            seconds = int(remaining_time % 60)
            
            self.time_label.config(text=f"Geschätzte Restzeit: {hours:02d}:{minutes:02d}:{seconds:02d}")
        
        self.status_label.config(text=f"Kopiere... {current}/{total} Dateien")
        self.root.update()
    
    def copy_files(self):
        source = self.source_path.get()
        dest = self.dest_path.get()
        
        if not source or not dest:
            messagebox.showerror("Fehler", "Bitte wählen Sie Quell- und Zielverzeichnis aus!")
            return
        
        try:
            # Dateien zählen
            total_files = sum([len(files) for _, _, files in os.walk(source)])
            copied_files = 0
            
            self.start_time = time.time()
            
            # Kopiervorgang
            for root, dirs, files in os.walk(source):
                rel_path = os.path.relpath(root, source)
                dest_dir = os.path.join(dest, rel_path)
                
                if not os.path.exists(dest_dir):
                    os.makedirs(dest_dir)
                
                for file in files:
                    src_file = os.path.join(root, file)
                    dst_file = os.path.join(dest_dir, file)
                    shutil.copy2(src_file, dst_file)
                    copied_files += 1
                    self.update_progress(copied_files, total_files)
            
            end_time = time.time()
            total_time = end_time - self.start_time
            hours = int(total_time // 3600)
            minutes = int((total_time % 3600) // 60)
            seconds = int(total_time % 60)
            
            self.status_label.config(text="Kopiervorgang abgeschlossen!")
            self.time_label.config(text=f"Gesamtzeit: {hours:02d}:{minutes:02d}:{seconds:02d}")
            messagebox.showinfo("Erfolg", f"Alle Dateien wurden erfolgreich kopiert!\nGesamtzeit: {hours:02d}:{minutes:02d}:{seconds:02d}")
            
        except Exception as e:
            messagebox.showerror("Fehler", f"Ein Fehler ist aufgetreten: {str(e)}")
            self.status_label.config(text="Fehler beim Kopieren!")
        
        finally:
            self.start_button.config(state="normal")
    
    def start_copy(self):
        self.start_button.config(state="disabled")
        self.progress_var.set(0)
        self.time_label.config(text="Geschätzte Zeit: Berechne...")
        thread = threading.Thread(target=self.copy_files)
        thread.start()

if __name__ == "__main__":
    root = tk.Tk()
    app = DataCloner(root)
    root.mainloop()
