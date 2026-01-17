# gui.py

import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2
from business import BusinessLayer, BusinessLayerError


class AppGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("IN450 Unit 3 Shermaine Kerford Database Viewer")
        self.geometry("1000x650")

        # Business layer starts as None until login succeeds
        self.bl = None

        # For row limit
        self.limit_var = tk.IntVar(value=50)

        # Build login UI first
        self.login_frame = None
        self.main_frame = None
        self.text = None

        self.build_login_ui()

    # ---------- Login UI ----------

    def build_login_ui(self):
        """Create the login screen to collect connection info."""
        self.login_frame = ttk.Frame(self, padding=20)
        self.login_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(self.login_frame, text="Database Login", font=("Arial", 14, "bold")).grid(
            row=0, column=0, columnspan=2, pady=(0, 15)
        )

        # Labels and entries
        ttk.Label(self.login_frame, text="Server (host):").grid(row=1, column=0, sticky=tk.E, pady=5)
        ttk.Label(self.login_frame, text="Database:").grid(row=2, column=0, sticky=tk.E, pady=5)
        ttk.Label(self.login_frame, text="User:").grid(row=3, column=0, sticky=tk.E, pady=5)
        ttk.Label(self.login_frame, text="Password:").grid(row=4, column=0, sticky=tk.E, pady=5)

        self.entry_server = ttk.Entry(self.login_frame, width=30)
        self.entry_db = ttk.Entry(self.login_frame, width=30)
        self.entry_user = ttk.Entry(self.login_frame, width=30)
        self.entry_password = ttk.Entry(self.login_frame, width=30, show="*")

        self.entry_server.grid(row=1, column=1, pady=5, sticky=tk.W)
        self.entry_db.grid(row=2, column=1, pady=5, sticky=tk.W)
        self.entry_user.grid(row=3, column=1, pady=5, sticky=tk.W)
        self.entry_password.grid(row=4, column=1, pady=5, sticky=tk.W)

        # Default values to save typing
        self.entry_server.insert(0, "localhost")
        self.entry_db.insert(0, "in450db")

        btn_connect = ttk.Button(self.login_frame, text="Connect", command=self.on_connect_clicked)
        btn_connect.grid(row=5, column=0, columnspan=2, pady=(15, 0))

    def on_connect_clicked(self):
        """Attempt to create a BusinessLayer with the supplied credentials."""
        host = self.entry_server.get().strip()
        dbname = self.entry_db.get().strip()
        user = self.entry_user.get().strip()
        password = self.entry_password.get().strip()

        if not host or not dbname or not user or not password:
            messagebox.showerror("Login error", "All fields are required.")
            return

        try:
            # Create business layer with credentials from the login form
            bl = BusinessLayer(host, dbname, user, password)
            # *** IMPORTANT ***
            # Explicitly try to open a connection here.
            # If username/password or server/db are wrong, this will raise
            # psycopg2.OperationalError and we will treat it as a bad login.
            bl.connect()

            # If we get here, the connection worked.
            self.bl = bl

        except psycopg2.OperationalError as e:
            # This is a real login/connection failure
            messagebox.showerror("Login failed", f"Could not connect:\n{e}")
            return
        except Exception as e:
            # Any other unexpected error during login
            messagebox.showerror("Login failed", f"Unexpected error:\n{e}")
            return

        # If we reach here, login succeeded
        messagebox.showinfo("Connected", f"Connected as user '{user}'")
        self.login_frame.destroy()
        self.build_main_ui()



    # ---------- Main UI (after login) ----------

    def build_main_ui(self):
        """Create the main GUI once the user has logged in."""
        self.main_frame = ttk.Frame(self, padding=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Top controls
        top = ttk.Frame(self.main_frame)
        top.pack(side=tk.TOP, fill=tk.X)

        btn_count_a = ttk.Button(
            top, text="Count rows in IN450a", command=self.on_count_in450a
        )
        btn_count_a.pack(side=tk.LEFT, padx=5)

        btn_show_a_rows = ttk.Button(
            top, text="Show rows from IN450a", command=self.on_show_in450a_rows
        )
        btn_show_a_rows.pack(side=tk.LEFT, padx=5)

        btn_show_b_names = ttk.Button(
            top, text="Show names from IN450b", command=self.on_show_in450b_names
        )
        btn_show_b_names.pack(side=tk.LEFT, padx=5)

        btn_show_b_rows = ttk.Button(
            top, text="Show full rows from IN450b", command=self.on_show_in450b_rows
        )
        btn_show_b_rows.pack(side=tk.LEFT, padx=5)

        btn_count_c = ttk.Button(
            top, text="Count rows in IN450c", command=self.on_count_in450c
        )
        btn_count_c.pack(side=tk.LEFT, padx=5)

        # Row limit
        ttk.Label(top, text="Row limit:").pack(side=tk.LEFT, padx=(20, 5))
        ttk.Entry(top, textvariable=self.limit_var, width=6).pack(side=tk.LEFT)

        # Text area
        text_frame = ttk.Frame(self.main_frame)
        text_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.text = tk.Text(text_frame, wrap=tk.NONE, font=("Courier New", 10))
        self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        yscroll = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.text.yview)
        yscroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.text.configure(yscrollcommand=yscroll.set)

    # ---------- Helper to display table ----------

    def display_table(self, title, column_names, rows):
        self.text.delete("1.0", tk.END)

        if title:
            self.text.insert(tk.END, title + "\n\n")

        if not rows:
            self.text.insert(tk.END, "No data found.\n")
            return

        fixed_widths = {
            "first_name": 14,
            "last_name": 14,
            "email": 32,
            "source": 16,
            "destination": 16,
            "col1": 6,
            "col2": 16,
            "col3": 16,
            "col4": 10,
            "col5": 8,
            "col6": 32,
        }

        header_parts = []
        for name in column_names:
            width = fixed_widths.get(name, 18)
            header_parts.append(name.ljust(width))
        header_line = " ".join(header_parts)
        sep_line = "-" * len(header_line)

        self.text.insert(tk.END, header_line + "\n")
        self.text.insert(tk.END, sep_line + "\n")

        for row in rows:
            line_parts = []
            for i, name in enumerate(column_names):
                value = "" if row[i] is None else str(row[i])
                width = fixed_widths.get(name, 18)
                line_parts.append(value.ljust(width))
            self.text.insert(tk.END, " ".join(line_parts) + "\n")

    # ---------- Button handlers ----------

    def on_count_in450a(self):
        try:
            count = self.bl.get_in450a_count()
            messagebox.showinfo("IN450a count", f"Rows in IN450a: {count}")
        except psycopg2.Error as e:
            messagebox.showerror("Error", f"Database error:\n{e}")
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error:\n{e}")

    def on_show_in450a_rows(self):
        try:
            limit = self.limit_var.get()
            rows = self.bl.get_in450a_rows(limit=limit)
            col_names = ["col1", "col2", "col3", "col4", "col5", "col6"]
            title = f"IN450a rows (up to {limit})"
            self.display_table(title, col_names, rows)
        except psycopg2.Error as e:
            messagebox.showerror("Error", f"Database error:\n{e}")
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error:\n{e}")
        except Exception:
            messagebox.showerror("Error", "Something unexpected happened. Please try again.")

    def on_show_in450b_names(self):
        try:
            limit = self.limit_var.get()
            rows = self.bl.get_in450b_names(limit=limit)
            col_names = ["first_name", "last_name"]
            title = f"IN450b first/last names (up to {limit})"
            self.display_table(title, col_names, rows)
        except psycopg2.Error as e:
            messagebox.showerror("Error", f"Database error:\n{e}")
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error:\n{e}")

    def on_show_in450b_rows(self):
        try:
            limit = self.limit_var.get()
            rows = self.bl.get_in450b_rows(limit=limit)
            col_names = ["first_name", "last_name", "email", "source", "destination"]
            title = f"IN450b full rows (up to {limit})"
            self.display_table(title, col_names, rows)
        except psycopg2.Error as e:
            messagebox.showerror("Error", f"Database error:\n{e}")
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error:\n{e}")

    def on_count_in450c(self):
        try:
            count = self.bl.get_in450c_count()
            messagebox.showinfo("IN450c count", f"Rows in IN450c: {count}")
        except psycopg2.Error as e:
            messagebox.showerror("Error", f"Database error:\n{e}")
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error:\n{e}")

    # ---------- Clean shutdown ----------

    def on_close(self):
        try:
            if self.bl:
                self.bl.close()
        finally:
            self.destroy()


if __name__ == "__main__":
    app = AppGUI()
    app.protocol("WM_DELETE_WINDOW", app.on_close)
    app.mainloop()
