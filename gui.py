# gui.py
import tkinter as tk
from tkinter import ttk, messagebox
from business import BusinessLayer


class AppGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        # Window basics
        self.title("IN450 Unit 2")
        self.geometry("1000x600")

        # Create a single BusinessLayer instance for the whole app
        self.bl = BusinessLayer()

        # ---------- Top controls frame ----------
        top = ttk.Frame(self, padding=10)
        top.pack(side=tk.TOP, fill=tk.X)

        # Button: show row count for in450a
        btn_count_a = ttk.Button(
            top, text="Count rows in in450a", command=self.on_count_in450a
        )
        btn_count_a.pack(side=tk.LEFT, padx=5)

        # Button: show first + last names from in450b
        btn_show_names = ttk.Button(
            top, text="Show names from in450b", command=self.on_show_in450b_names
        )
        btn_show_names.pack(side=tk.LEFT, padx=5)

        # Button: show raw rows from in450a
        btn_show_a_rows = ttk.Button(
            top, text="Show rows from in450a", command=self.on_show_in450a_rows
        )
        btn_show_a_rows.pack(side=tk.LEFT, padx=5)

        # Button: show full rows from in450b
        btn_show_b_rows = ttk.Button(
            top, text="Show full rows from in450b", command=self.on_show_in450b_rows
        )
        btn_show_b_rows.pack(side=tk.LEFT, padx=5)

        # Row limit label + entry
        self.limit_var = tk.IntVar(value=50)
        ttk.Label(top, text="Row limit:").pack(side=tk.LEFT, padx=(20, 5))
        ttk.Entry(top, textvariable=self.limit_var, width=6).pack(side=tk.LEFT)

        # ---------- Text display area with scrollbar ----------
        text_frame = ttk.Frame(self)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Use monospaced font so columns line up
        self.text = tk.Text(text_frame, wrap=tk.NONE, font=("Courier New", 10))
        self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Vertical scrollbar
        yscroll = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.text.yview)
        yscroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.text.configure(yscrollcommand=yscroll.set)

    # ---------- Helper to display a nicely aligned table ----------
    def display_table(self, title, column_names, rows):
        """
        Shows a simple table in the text area with aligned columns.

        title: string shown at the top (can be None)
        column_names: list of column header strings
        rows: list of tuples (one tuple per row)
        """
        self.text.delete("1.0", tk.END)

        if title:
            self.text.insert(tk.END, title + "\n\n")

        if not rows:
            self.text.insert(tk.END, "No data found.\n")
            return

        num_cols = len(column_names)

        # Start with header name lengths
        col_widths = [len(name) for name in column_names]

        # Make sure we don't crash if some rows have None values
        for row in rows:
            for i in range(num_cols):
                if i >= len(row):
                    continue
                value = "" if row[i] is None else str(row[i])
                if len(value) > col_widths[i]:
                    # cap column width a bit to avoid super-wide columns
                    col_widths[i] = min(len(value), 40)

        # Build header line
        header_parts = []
        for i, name in enumerate(column_names):
            header_parts.append(name.ljust(col_widths[i] + 2))
        header_line = "".join(header_parts)

        # Separator line
        sep_line = "-" * len(header_line)

        self.text.insert(tk.END, header_line + "\n")
        self.text.insert(tk.END, sep_line + "\n")

        # Data rows
        for row in rows:
            line_parts = []
            for i in range(num_cols):
                if i < len(row):
                    value = "" if row[i] is None else str(row[i])
                else:
                    value = ""
                line_parts.append(value.ljust(col_widths[i] + 2))
            line = "".join(line_parts)
            self.text.insert(tk.END, line + "\n")

    # ---------- Button handlers ----------

    def on_count_in450a(self):
        """Handle click on 'Count rows in in450a' button."""
        try:
            count = self.bl.get_in450a_count()
            messagebox.showinfo("in450a count", f"Number of rows in in450a: {count}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to get count: {e}")

    def on_show_in450a_rows(self):
        """Handle click on 'Show rows from in450a' button."""
        try:
            limit = self.limit_var.get()
            rows = self.bl.get_in450a_rows(limit=limit)
            col_names = ["col1", "col2", "col3", "col4", "col5", "col6"]
            title = f"in450a rows (showing up to {limit})"
            self.display_table(title, col_names, rows)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load in450a rows: {e}")

    def on_show_in450b_names(self):
        """Handle click on 'Show names from in450b' button."""
        try:
            limit = self.limit_var.get()
            rows = self.bl.get_in450b_names(limit=limit)
            col_names = ["first_name", "last_name"]
            title = f"First and last names from in450b (showing up to {limit})"
            self.display_table(title, col_names, rows)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load in450b names: {e}")

    def on_show_in450b_rows(self):
        """Handle click on 'Show full rows from in450b' button."""
        try:
            limit = self.limit_var.get()
            rows = self.bl.get_in450b_rows(limit=limit)
            col_names = ["first_name", "last_name", "email", "source", "destination"]
            title = f"Full rows from in450b (showing up to {limit})"
            self.display_table(title, col_names, rows)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load in450b rows: {e}")

    # ---------- Clean shutdown ----------
    def on_close(self):
        try:
            self.bl.close()
        finally:
            self.destroy()


if __name__ == "__main__":
    app = AppGUI()
    app.protocol("WM_DELETE_WINDOW", app.on_close)
    app.mainloop()
