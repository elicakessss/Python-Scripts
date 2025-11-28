import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import base64
import binascii
import html
import urllib.parse
import uu
import io

def decode_ascii(data):
    return ''.join(chr(int(x)) for x in data.split())

def decode_base64(data):
    return base64.b64decode(data).decode(errors="ignore")

def decode_base32(data):
    return base64.b32decode(data).decode(errors="ignore")

def decode_url(data):
    return urllib.parse.unquote(data)

def decode_hex(data):
    return bytes.fromhex(data).decode(errors="ignore")

def decode_binary(data):
    return ''.join(chr(int(b, 2)) for b in data.split())

def decode_html_entities(data):
    return html.unescape(data)

def decode_uu(data):
    # Wrap UUencoded text with minimal UU structure if not provided
    wrapper = f"begin 644 dummy\n{data}\n`\nend\n"
    encoded = io.BytesIO(wrapper.encode())
    decoded = io.BytesIO()
    try:
        uu.decode(encoded, decoded, quiet=True)
        return decoded.getvalue().decode(errors="ignore")
    except:
        raise ValueError("Invalid or incomplete UUencoded data")

# Dictionary of decoders
decoders = {
    "ASCII": decode_ascii,
    "Base64": decode_base64,
    "Base32": decode_base32,
    "URL Encoding": decode_url,
    "Hex": decode_hex,
    "Binary (8-bit)": decode_binary,
    "HTML Entities": decode_html_entities,
    "UUencoding": decode_uu
}

# GUI Setup
window = tk.Tk()
window.title("Universal Decoder Tool")
window.geometry("600x500")

ttk.Label(window, text="Select Encoding:").pack(pady=5)

encoding_var = tk.StringVar()
encoding_menu = ttk.Combobox(window, textvariable=encoding_var, state="readonly")
encoding_menu["values"] = list(decoders.keys())
encoding_menu.current(0)
encoding_menu.pack(pady=5)

ttk.Label(window, text="Input Encoded Text:").pack(pady=5)
input_box = scrolledtext.ScrolledText(window, height=8)
input_box.pack(fill="both", padx=10)

ttk.Label(window, text="Decoded Output:").pack(pady=5)
output_box = scrolledtext.ScrolledText(window, height=8)
output_box.pack(fill="both", padx=10)

def run_decode():
    output_box.delete("1.0", tk.END)
    encoding = encoding_var.get()
    data = input_box.get("1.0", tk.END).strip()

    if not data:
        messagebox.showerror("Error", "Please enter encoded text.")
        return

    try:
        result = decoders[encoding](data)
        output_box.insert(tk.END, result)
    except Exception as e:
        messagebox.showerror("Decode Error", str(e))

ttk.Button(window, text="Decode", command=run_decode).pack(pady=10)

window.mainloop()
