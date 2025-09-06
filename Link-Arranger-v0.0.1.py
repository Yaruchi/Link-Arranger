import tkinter as tk
from tkinter import filedialog, messagebox
from urllib.parse import urlparse

def clean_links():
    raw_text = input_box.get("1.0", tk.END).strip().splitlines()
    
    link_count = {}
    for link in raw_text:
        if link:
            link_count[link] = link_count.get(link, 0) + 1

    # Apply sorting
    sort_mode = sort_var.get()
    items = list(link_count.items())

    if sort_mode == "Alphabetical":
        items.sort(key=lambda x: x[0].lower())
    elif sort_mode == "Frequency":
        items.sort(key=lambda x: x[1], reverse=True)
    elif sort_mode == "Domain":
        items.sort(key=lambda x: urlparse(x[0]).netloc)

    # Decide whether to show counts
    show_counts = counts_var.get()
    if show_counts:
        cleaned = [f"{link} ({count})" for link, count in items]
    else:
        cleaned = [link for link, _ in items]

    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, "\n".join(cleaned))

def save_to_file():
    cleaned_text = output_box.get("1.0", tk.END).strip()
    if not cleaned_text:
        messagebox.showwarning("Warning", "Nothing to save!")
        return
    
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(cleaned_text)
        messagebox.showinfo("Success", f"Saved to {file_path}")

# GUI Setup
root = tk.Tk()
root.title("Link Arranger v0.0.1")
root.geometry("800x700")

# Input area
tk.Label(root, text="Paste your links here:").pack(anchor="w")
input_box = tk.Text(root, height=15, width=100)
input_box.pack(padx=10, pady=5)

# Sorting options
sort_var = tk.StringVar(value="Original")
tk.Label(root, text="Sort by:").pack(anchor="w", padx=10)
tk.OptionMenu(root, sort_var, "Original", "Alphabetical", "Frequency", "Domain").pack(anchor="w", padx=10, pady=5)

# Show counts toggle
counts_var = tk.BooleanVar(value=True)
tk.Checkbutton(root, text="Show duplicate counts (n)", variable=counts_var).pack(anchor="w", padx=10, pady=5)

# Buttons
tk.Button(root, text="Clean Links", command=clean_links).pack(pady=5)
tk.Button(root, text="Save to File", command=save_to_file).pack(pady=5)

# Output area
tk.Label(root, text="Cleaned links:").pack(anchor="w")
output_box = tk.Text(root, height=15, width=100)
output_box.pack(padx=10, pady=5)

root.mainloop()
