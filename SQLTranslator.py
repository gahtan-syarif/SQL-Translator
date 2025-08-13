import tkinter as tk
from tkinter import ttk
import sqlglot

root = tk.Tk()
root.title("SQL Translator")
root.geometry("950x550")

# Persistent settings
identify_var = tk.BooleanVar(value=True)
pretty_var = tk.BooleanVar(value=True)
pad_var = tk.IntVar(value=4)
indent_var = tk.IntVar(value=4)

# Helpers
def make_context_menu(widget):
    menu = tk.Menu(widget, tearoff=0)
    menu.add_command(label="Cut", command=lambda: widget.event_generate("<<Cut>>"))
    menu.add_command(label="Copy", command=lambda: widget.event_generate("<<Copy>>"))
    menu.add_command(label="Paste", command=lambda: widget.event_generate("<<Paste>>"))
    widget.bind("<Button-3>", lambda e: menu.tk_popup(e.x_root, e.y_root))

# Advanced settings popup
def open_advanced_settings():
    win = tk.Toplevel(root)
    win.title("Advanced Settings")
    win.resizable(False, False)
    win.grab_set()  # modal feel

    ttk.Checkbutton(win, text="Identify (quote identifiers)", variable=identify_var).pack(anchor="w", padx=12, pady=(12, 6))
    ttk.Checkbutton(win, text="Pretty print", variable=pretty_var).pack(anchor="w", padx=12, pady=6)

    frm_pad = ttk.Frame(win); frm_pad.pack(anchor="w", padx=12, pady=(8, 2))
    ttk.Label(frm_pad, text="Pad:").pack(side=tk.LEFT)
    tk.Spinbox(frm_pad, from_=0, to=16, width=5, textvariable=pad_var).pack(side=tk.LEFT, padx=(6, 0))

    frm_indent = ttk.Frame(win); frm_indent.pack(anchor="w", padx=12, pady=(8, 12))
    ttk.Label(frm_indent, text="Indent:").pack(side=tk.LEFT)
    tk.Spinbox(frm_indent, from_=0, to=16, width=5, textvariable=indent_var).pack(side=tk.LEFT, padx=(6, 0))


# Transpile
def transpile_sql(query, in_dialect, out_dialect):
    try:
        result = sqlglot.transpile(
            query,
            read=in_dialect.lower(),
            write=out_dialect.lower(),
            pretty=pretty_var.get(),
            identify=identify_var.get(),
            pad=pad_var.get(),
            indent=indent_var.get(),
        )[0]
        return result
    except Exception:
        return "Error: Invalid SQL query. Please review your input."

def on_transpile():
    input_sql = left_text.get("1.0", tk.END)
    in_dialect = input_dialect_var.get()
    out_dialect = output_dialect_var.get()
    output_sql = transpile_sql(input_sql, in_dialect, out_dialect)
    right_text.delete("1.0", tk.END)
    right_text.insert(tk.END, output_sql)

# UI
main_frame = ttk.Frame(root, padding=10)
main_frame.pack(fill=tk.BOTH, expand=True)

dialects = [
    "Athena", "BigQuery", "ClickHouse", "Databricks", "Doris", "Dremio", "Drill",
    "Druid", "DuckDB", "Dune", "Fabric", "Hive", "Materialize", "MySQL", "Oracle",
    "Postgres", "Presto", "PRQL", "Redshift", "RisingWave", "SingleStore", "Snowflake",
    "Spark", "Spark2", "SQLite", "StarRocks", "Tableau", "Teradata", "Trino", "TSQL", "Exasol"
]

default_input_dialect = "Postgres"
default_output_dialect = "MySQL"

# Labels
ttk.Label(main_frame, text="Input", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky="w", pady=(0, 2))
ttk.Label(main_frame, text="Output", font=("Segoe UI", 10, "bold")).grid(row=0, column=2, sticky="w", pady=(0, 2))

# Dropdowns
input_dialect_var = tk.StringVar(value=default_input_dialect)
input_dropdown = ttk.Combobox(main_frame, textvariable=input_dialect_var, values=dialects, state="readonly")
input_dropdown.grid(row=1, column=0, sticky="ew", padx=(0, 5), pady=(0, 5))

output_dialect_var = tk.StringVar(value=default_output_dialect)
output_dropdown = ttk.Combobox(main_frame, textvariable=output_dialect_var, values=dialects, state="readonly")
output_dropdown.grid(row=1, column=2, sticky="ew", padx=(5, 0), pady=(0, 5))

# Text panes (word wrap + context menu)
left_text = tk.Text(main_frame, wrap=tk.WORD)
left_text.grid(row=2, column=0, sticky="nsew", padx=(0, 5))
make_context_menu(left_text)

right_text = tk.Text(main_frame, wrap=tk.WORD)
right_text.grid(row=2, column=2, sticky="nsew", padx=(5, 0))
make_context_menu(right_text)

# Middle column with centered buttons
button_frame = ttk.Frame(main_frame)
button_frame.grid(row=2, column=1, padx=6, sticky="ns")
# spacer rows to center vertically
button_frame.rowconfigure(0, weight=1)
button_frame.rowconfigure(3, weight=1)

ttk.Button(button_frame, text="Translate ->", command=on_transpile).grid(row=1, column=0, pady=6)
ttk.Button(button_frame, text="Advanced Settings", command=open_advanced_settings).grid(row=2, column=0, pady=6)

# Resizing behavior
main_frame.columnconfigure(0, weight=1)   # left expands
main_frame.columnconfigure(1, weight=0)   # middle stays compact
main_frame.columnconfigure(2, weight=1)   # right expands
main_frame.rowconfigure(2, weight=1)      # text row expands

root.mainloop()
