import os
import customtkinter as ctk
from tkinter import Listbox, Scrollbar, Toplevel, END, SINGLE

class CustomFileDialog(ctk.CTkToplevel):
    def __init__(
            self, master=None, title="Select a File", 
            start_path='.', mode='open', file_types=None, 
            initialfile=None, on_close=None, scale_factor=1.0
            ):
        super().__init__(master)

        if file_types is None:
            self.file_types = ["All Files"]
        else:
            self.file_types = file_types
        self.scale_factor = scale_factor
        self.geometry("800x900")
        self.title(title)
        self.initialfile = initialfile
        self.on_close_callback = on_close
        self.current_path = os.path.abspath(start_path)
        self.selected_format = self.file_types[0]
        self.mode = mode  # 'open' or 'save'
        self.font = "Roboto"
        self.create_widgets()

    def create_widgets(self):
        self.path_entry = ctk.CTkEntry(self, placeholder_text="Enter path here", font=(self.font, 8*self.scale_factor))
        self.path_entry.pack(pady=(10, 0), padx=10, fill='x')
        self.path_entry.insert(0, self.current_path)
        self.path_entry.bind('<Return>', self.path_entry_updated)  # Update on Enter key

        self.go_up_button = ctk.CTkButton(self, text="Go Up", command=self.go_up_one_level, font=(self.font, 8*self.scale_factor))
        self.go_up_button.pack(pady=(5, 10))
        
        # File format selection (for open mode)
        self.format_combobox = ctk.CTkComboBox(self, values=self.file_types, command=self.format_selected, 
                                                font=(self.font, 8*self.scale_factor), dropdown_font=(self.font, 8*self.scale_factor))
        self.format_combobox.set(self.file_types[0])  # Default selection
        self.format_combobox.pack(pady=(5, 0))
        
        # Filename entry (for save mode)
        self.filename_entry = ctk.CTkEntry(self, placeholder_text="Enter filename", font=(self.font, 8*self.scale_factor))
        self.filename_entry.pack(pady=(5, 0), fill='x')
        self.filename_entry.pack_forget()  # Hide initially

        # Listbox and scrollbar for file and directory listing
        self.listbox_frame = ctk.CTkFrame(self)
        self.listbox_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.scrollbar = Scrollbar(self.listbox_frame)
        self.scrollbar.pack(side="right", fill="y")
        
        self.listbox = Listbox(
                            self.listbox_frame, 
                            yscrollcommand=self.scrollbar.set, 
                            selectmode=SINGLE, 
                            font=("Roboto", int(10*self.scale_factor))
                        )
        self.listbox.pack(side="left", fill="both", expand=True)
        self.scrollbar.config(command=self.listbox.yview)
        
        self.listbox.bind("<<ListboxSelect>>", self.on_select)

        self.update_listbox(self.current_path)

        self.open_button = ctk.CTkButton(self, text="Open", command=self.open_or_save, font=(self.font, 8*self.scale_factor))
        self.open_button.pack(pady=(0, 10))

        self.update_ui_for_mode()

    def change_mode(self, selection):
        self.mode = 'open' if selection == "Open" else 'save'
        self.update_ui_for_mode()

    def update_ui_for_mode(self):
        if self.mode == 'save':
            self.filename_entry.pack(pady=(5, 0), fill='x')
            if self.initialfile:
                self.filename_entry.insert(0, self.initialfile)
            self.format_combobox.pack_forget()
            self.open_button.configure(text="Save")
        else:
            self.filename_entry.pack_forget()
            self.format_combobox.pack(pady=(5, 0))
            self.open_button.configure(text="Open")
        self.update_listbox(self.current_path)

    def format_selected(self, selection):
        self.selected_format = selection
        if self.mode == 'open':
            self.update_listbox(self.current_path)

    def update_listbox(self, path):
        self.listbox.delete(0, END)
        self.path_entry.delete(0, END)
        self.path_entry.insert(0, path)
        self.current_path = path

        if self.mode == 'open':
            for item in sorted(os.listdir(path), key=str.lower):
                full_path = os.path.join(path, item)
                if os.path.isdir(full_path):
                    self.listbox.insert(END, "[D] " + item)
                elif self.selected_format == "All Files" or item.endswith(self.selected_format):
                    self.listbox.insert(END, "[F] " + item)
        else:  # In 'save' mode, list directories only
            for item in sorted(os.listdir(path), key=str.lower):
                full_path = os.path.join(path, item)
                if os.path.isdir(full_path):
                    self.listbox.insert(END, "[D] " + item)

    def go_up_one_level(self):
        parent_path = os.path.dirname(self.current_path)
        if parent_path != self.current_path:  # Prevent going up from the root directory
            self.update_listbox(parent_path)

    def path_entry_updated(self, event=None):
        new_path = self.path_entry.get()
        if os.path.exists(new_path) and os.path.isdir(new_path):
            self.update_listbox(new_path)
        else:
            ctk.CTkMessageBox.show_warning("Invalid Path", "The specified path does not exist or is not a directory.")

    def on_select(self, event):
        selection_index = self.listbox.curselection()
        if selection_index:
            selection = self.listbox.get(selection_index[0])
            if selection.startswith("[D]"):
                directory = selection.split("[D] ")[1]
                self.update_listbox(os.path.join(self.current_path, directory))

    def open_or_save(self):
        if self.mode == 'open':
            selection_index = self.listbox.curselection()
            if selection_index:
                selection = self.listbox.get(selection_index[0])
                if not selection.startswith("[D]"):
                    file_path = os.path.join(self.current_path, selection.split("[F] ")[1])
                    self.on_close_callback(file_path)
                    self.destroy()  # Close dialog after selection
        else:  # 'save' mode
            filename = self.filename_entry.get()
            
            if filename:
                if self.selected_format != "All Files":
                    if not filename.endswith(self.file_types[0]):
                        filename += self.file_types[0]
                        filename = filename.replace(" ", "")
                file_path = os.path.join(self.current_path, filename)
                self.on_close_callback(file_path)

                self.destroy()  # Close dialog after confirmation