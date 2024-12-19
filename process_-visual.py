import tkinter as tk
from tkinter import ttk, messagebox
import gmpy2


class VisualCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Progress")

        # Fixing window width
        self.root.resizable(False, False)

        # Dark theme
        style = ttk.Style()
        style.theme_use('alt')
        style.map('TButton',
                  foreground=[('active', 'white')],
                  background=[('active', 'darkblue')])

        # Range input
        self.range_label = tk.Label(root, text="Диапазон:")
        self.range_label.grid(row=0, column=0, padx=10, pady=5)

        self.start_range_entry = ttk.Entry(root)
        self.start_range_entry.grid(row=0, column=1, padx=10, pady=5)

        self.end_range_entry = ttk.Entry(root)
        self.end_range_entry.grid(row=0, column=2, padx=10, pady=5)

        # Processes
        self.process_label = tk.Label(root, text="Процесс:")
        self.process_label.grid(row=1, column=0, padx=10, pady=5)

        self.start_process_entries = []
        self.end_process_entries = []
        self.current_row = 1

        self.add_button = tk.Button(root, text="Add Process", command=self.add_range)
        self.add_button.grid(row=1, column=3, padx=10, pady=5)

        self.del_button = tk.Button(root, text="Del Process", command=self.del_range)
        self.del_button.grid(row=2, column=3, padx=10, pady=5)

        # Progress Bar
        self.progress_canvas = tk.Canvas(root, width=800, height=20, bg="white")
        self.progress_canvas.grid(row=40, columnspan=4, padx=10, pady=5)

        self.process_rectangles = []

        # Buttons
        self.calculate_button = tk.Button(root, text="Calculate", command=self.calculate_progress)
        self.calculate_button.grid(row=30, column=0, padx=10, pady=5)

        self.clear_button = tk.Button(root, text="Clear", command=self.clear_canvas)
        self.clear_button.grid(row=30, column=1, padx=10, pady=5)

        # Free ranges
        self.free_ranges_label = tk.Label(root, text="Свободные Диапазоны:")
        self.free_ranges_label.grid(row=60, column=0, padx=10, pady=5)

        self.free_ranges_tree = ttk.Treeview(root, columns=("Start", "End"), show="headings")
        self.free_ranges_tree.heading("Start", text="Начало")
        self.free_ranges_tree.heading("End", text="Конец")
        self.free_ranges_tree.grid(row=70, columnspan=4, padx=10, pady=5)

        self.copy_button = tk.Button(root, text="Copy Ranges", command=self.copy_free_ranges)
        self.copy_button.grid(row=80, columnspan=4, padx=10, pady=5)

        # Number system toggle
        self.system_var = tk.StringVar(value='dec')
        hex_radio = ttk.Radiobutton(root, text="HEX", variable=self.system_var, value='hex', command=self.update_entry_formats)
        dec_radio = ttk.Radiobutton(root, text="DEC", variable=self.system_var, value='dec', command=self.update_entry_formats)

        hex_radio.grid(row=0, column=3, padx=10, pady=5)
        dec_radio.grid(row=0, column=4, padx=10, pady=5)

    def add_range(self):
        start_process_entry = ttk.Entry(self.root)
        end_process_entry = ttk.Entry(self.root)

        start_process_entry.grid(row=self.current_row, column=1, padx=10, pady=5)
        end_process_entry.grid(row=self.current_row, column=2, padx=10, pady=5)

        self.start_process_entries.append(start_process_entry)
        self.end_process_entries.append(end_process_entry)

        self.current_row += 1

    def del_range(self):
        if self.start_process_entries and self.end_process_entries:
            self.start_process_entries[-1].grid_forget()
            self.end_process_entries[-1].grid_forget()
            self.start_process_entries.pop()
            self.end_process_entries.pop()
            self.current_row -= 1

    def calculate_progress(self):
        try:
            # Clear previous progress and free ranges
            self.clear_canvas()

            start_range = gmpy2.mpz(int(self.start_range_entry.get(), 16) if self.system_var.get() == 'hex' else int(self.start_range_entry.get()))
            end_range = gmpy2.mpz(int(self.end_range_entry.get(), 16) if self.system_var.get() == 'hex' else int(self.end_range_entry.get()))
            total_range = end_range - start_range + 1

            if total_range <= 0:
                raise ValueError("Invalid range. Ensure the end range is greater than the start range.")

            scale_factor = 800 / total_range  # Масштабирование в ширину 800px

            free_ranges = []
            current_start = start_range

            for start_process_entry, end_process_entry in zip(self.start_process_entries, self.end_process_entries):
                start_process = gmpy2.mpz(int(start_process_entry.get(), 16) if self.system_var.get() == 'hex' else int(start_process_entry.get()))
                end_process = gmpy2.mpz(int(end_process_entry.get(), 16) if self.system_var.get() == 'hex' else int(end_process_entry.get()))

                if start_process < current_start:
                    start_process = current_start
                if end_process > end_range:
                    end_process = end_range

                if start_process > end_range or end_process < start_range:
                    continue

                # Отображаем "заполненные" участки
                x1 = (start_process - start_range) * scale_factor
                x2 = (end_process - start_range + 1) * scale_factor
                self.progress_canvas.create_rectangle(x1, 0, x2, 20, fill="green", outline="black")

                if current_start < start_process:
                    free_ranges.append((current_start, start_process - 1))
                current_start = max(current_start, end_process + 1)

            if current_start <= end_range:
                free_ranges.append((current_start, end_range))

            for start, end in free_ranges:
                self.free_ranges_tree.insert("", "end", values=(f"{start:x}" if self.system_var.get() == 'hex' else start,
                                                                    f"{end:x}" if self.system_var.get() == 'hex' else end))

        except ValueError as e:
            tk.messagebox.showwarning("Warning", f"Invalid input: {e}")

    def clear_canvas(self):
        self.progress_canvas.delete("all")
        self.free_ranges_tree.delete(*self.free_ranges_tree.get_children())

    def copy_free_ranges(self):
        free_ranges_str = "\n".join([f"Start: {self.free_ranges_tree.item(item, 'values')[0]}, End: {self.free_ranges_tree.item(item, 'values')[1]}" for item in self.free_ranges_tree.get_children()])
        self.root.clipboard_clear()
        self.root.clipboard_append(free_ranges_str)
        messagebox.showinfo("Info", "Free ranges copied to clipboard.")

    def update_entry_formats(self):
        current_system = self.system_var.get()
        entries = [self.start_range_entry, self.end_range_entry] + self.start_process_entries + self.end_process_entries

        for entry in entries:
            try:
                value = int(entry.get(), 16) if current_system == 'hex' else int(entry.get())
                entry.delete(0, tk.END)
                entry.insert(0, f"{value:x}" if current_system == 'hex' else str(value))
            except ValueError:
                pass


if __name__ == "__main__":
    root = tk.Tk()
    app = VisualCalculator(root)
    root.mainloop()
