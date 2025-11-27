import customtkinter as ctk
from datetime import datetime
import tkinter as tk 
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import webbrowser
import sqlite3
import json
import os
import sys


__version__ = "1.0"

my_url = 'https://github.com/soldiers-son/simple-pos'

# Handle database PATH
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Connect to database
if os.path.exists("pos.db"):
    db_path = "pos.db"
else:
    db_path = resource_path("pos.db")

# Create cursor in database
conn = sqlite3.connect(db_path)
c = conn.cursor()

# Current date and time
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Shows specified frame
def show_frame(frame):
    frame.tkraise()

# Queries sql db for table to insert into treeview
c.execute("SELECT item, quantity, price FROM inventory")
rows = c.fetchall()

CURRENT_ORDER = "order.json"

# Selects Treeview item and Subtracts item_q entry from quantity 
def sbmt_crnt_slctn():
    try:
        # Get selected Treeview item
        selected_item = tree.selection()[0]
        if not selected_item:
            messagebox.showwarning("Selection Error", "No row selected.")
            return
        # Get selected item ID
        item_qnty = tree.focus()
        if not item_qnty:
            messagebox.showwarning("Selection Error", "No row selected.")
            return
        item_price = tree.focus()
        if not item_price:
            messagebox.showwarning("Selection Error", "No row selected.")
            return

        # Get the row's data (values is a tuple of column values)
        qnty_data = tree.item(item_qnty, 'values')
        price_data = tree.item(item_price, 'values')

        # Example: Get the value from column index 1 (second column)
        col1_index = 1  # Change this to the column you want
        if col1_index >= len(qnty_data):
            messagebox.showerror("Column Error", f"Column index {col1_index} out of range.")
            return
        
        col2_index = 2  # Change this to the column you want
        if col2_index >= len(price_data):
            messagebox.showerror("Column Error", f"Column index {col2_index} out of range.")
            return

        col1_str = qnty_data[col1_index]
        col2_str = qnty_data[col2_index]

        # Convert to integer safely
        try:
            col1_int = int(col1_str)
        except ValueError:
            messagebox.showerror("Conversion Error", f"Cannot convert '{col1_str}' to int.")
        try:
            col2_int = float(col2_str)
        except ValueError:
            messagebox.showerror("Conversion Error", f"Cannot convert '{col2_str}' to int.")

        if col1_int < 1:
            messagebox.showwarning("Warning", f"{selected_item} is out of stock")
    
        else:
            try:
                # Get entry
                entry = int(item_q.get())
                subtotal = entry * col2_int
                
                # Confirm order
                confirm = messagebox.askokcancel("Confirm", f"Add {entry} {selected_item} to order?")
                
                # Creates and adds to cart 
                def add_to_order():
                    item = ({"cart": [{f"{selected_item}": entry, "subtotal": subtotal}]})
                    append = ({f"{selected_item}": entry, "subtotal": subtotal})
                    if os.path.exists(CURRENT_ORDER):
                        with open(CURRENT_ORDER, "r+") as f:
                            data = json.load(f)
                            data["cart"].append(append)
                            # Write the updated JSON data back to the file
                            f.seek(0)
                            f.truncate()
                            json.dump(data, f, indent=4)

                    else:
                        with open(CURRENT_ORDER, "a") as f:
                            json.dump(item, f, indent=4)

                    

                def add_to_sales():
                    c.execute("""
                            INSERT INTO sales(item, quantity, price, date)
                            VALUES(?,?,?,?)
                            """, (selected_item, entry, subtotal, timestamp))
                    conn.commit()
            
                if confirm:
                    messagebox.showinfo("Confirmed", f"{entry} {selected_item} added to cart" )
                    add_to_order()
                    add_to_sales()

                    # Get task + date from Treeview values
                    item_values = tree.item(selected_item, 'values')

                    # Subtract quantity from the database based on the selected item
                    c.execute(f"UPDATE inventory SET quantity = quantity - {entry} WHERE item = '{item_values[0]}'")
                    conn.commit()

                    # Deletes current item_q entry
                    item_q.delete(0, END)

                    # Refresh TreeView with rowid as iid
                    c.execute("SELECT item, quantity, price FROM inventory")
                    rows = c.fetchall()
                    
                    for child in tree.get_children():
                        tree.delete(child)
                    for row in rows:
                        tree.insert("", tk.END, iid=row[0], values=row[0:3])            
                else:
                    messagebox.showinfo("Cancled", "Add item to order has been cancled.")
            except Exception as e:
                messagebox.showerror('Error', f"An error occurred:\n{e}")
    except Exception as e:
                messagebox.showerror('Error', f"An error occurred:\n{e}")


# View current ourder in cart
def cart():
    try:
        # Checks File for dict/list data, creates nodes for treeview 
        def display_json(data, parent=""):
            if isinstance(data, dict):
                for key, value in data.items():
                    node = tree.insert(parent, "end", text=key)
                    display_json(value, node)
            elif isinstance(data, list):
                for index, value in enumerate(data):
                    node = tree.insert(parent, "end", text=f"[{index}]")
                    display_json(value, node)
            else:
                tree.insert(parent, "end", text=data)

        # Loads formatted data in treeview nodes
        def load_file():
            if os.path.exists(CURRENT_ORDER):
                with open(CURRENT_ORDER, "r") as f:
                    data = json.load(f)
                for item in tree.get_children():
                    tree.delete(item)

                display_json(data)
    


        # Cart UI
        cart = tk.Toplevel()
        cart.title('Cart')
        cart.geometry('640x300')
        cart.tk_setPalette("#1F1F1F")

        tree = ttk.Treeview(cart)
        tree.pack(expand=True, fill='both')
        
        
        load_file()

        
    except Exception as e:
        messagebox.showerror('Error', f"An error occurred:\n{e}")


# Shows order summary, asks for confimation, and then deletes current order 
def finalize_order():
    try:
        if os.path.exists(CURRENT_ORDER):
            with open(CURRENT_ORDER, "r") as f:
                data = json.load(f)
                # Formats json data to pretty print
            formatted_data = json.dumps(data, indent=4, separators=(", ", ": "))
            total = 0
            # Adds subtotal values together to get total sum
            for item in data['cart']:
                if 'subtotal' in item and isinstance(item['subtotal'], (int, float)):
                    total += item['subtotal']
                    # Asks confitmation of order
            comfirm = messagebox.askokcancel("Order Summary", f"Order: \n\n{formatted_data}\n\nTotal: {total:.2f}")
            if comfirm:
                messagebox.showinfo("Order Summary", "Order Complete.")
                # Deletes current order
                os.remove(CURRENT_ORDER)
            else:
                messagebox.showinfo("", "Finalize Cancled")
        else:
            messagebox.showerror("Error", "No order exists, please add items to start order.")
    except Exception as e:
        messagebox.showerror('Error', f"An error occurred:\n{e}")


# Help
def show_help():
    help = ("MAIN WINDOW\n"
            "-Select item and enter item quantity.\n"
            "-Press 'Submit' to add item and quantity to order.\n"
            "-Once order is finished, press 'Finalize' to complete order.\n"
            "-To delete item from in stock, select item in treeview and press the 'X' button\n"
            "-To view current order press 'cart'\n\n"
            "INVENTORY\n"
            "-Click inventory under 'Inv & Sales' menu tab\n" 
            "-Input inventory items to add to your stock treeview\n"
            "-Press the 🔁 button to refresh treeview on main window."
            )
    messagebox.showinfo("Help", help)

# About
def show_about():
        info = ("Project: 🌿Solace POS🌿\n"
                f"Version: {__version__}\n"
                "Author: soldiers_son\n"
                "Github: https://github.com/soldiers-son\n\n")
        messagebox.showinfo("About", info)

def open_source():
    webbrowser.open_new(my_url)

# Sales data
def show_sales():
    try:
        c.execute("SELECT * FROM sales")
        rows = c.fetchall()
        
        sales_window = tk.Toplevel(app)
        sales_window.title('Sales')
        sales_window.geometry('565x350')
        sales_window.configure(bg="#1F1F1F")
        
        label = ctk.CTkLabel(sales_window, font=("Default", 16, "bold"), text="Sales Data").pack(pady=10)
        
        # Create a frame to hold the Treeview and scrollbar
        tree_frame = tk.Frame(sales_window)
        tree_frame.pack(fill="both", expand=True)
        
        # Create the Treeview
        tree = ttk.Treeview(tree_frame, columns=("col1", "col2", "col3", "col4"), show="headings")
        tree.heading("col1", text="Item")
        tree.heading("col2", text="Quantity")
        tree.heading("col3", text="Subtotal")
        tree.heading("col4", text="Date")
        tree.pack(side="left", fill="both", expand=True)
        
        # Create the vertical scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        scrollbar.pack(side="right", fill="y")
        
        # Attach scrollbar to Treeview
        tree.configure(yscrollcommand=scrollbar.set)
       
        # Insert data
        for row in rows:
            tree.insert("", tk.END, values=row)
    except Exception as e:
        messagebox.showerror("Database Error", f"An error occurred:\n{e}")


# POS Inventory
def inventory():
    # Submit entry into inventory
    def inv_submit():
        I = inv_item.get()
        Q = inv_quantity.get()
        P = inv_price.get()

        if len(I) == 0:
            messagebox.showerror("ERROR", "Please enter Item.")
            return
        if len(Q) == 0:
            messagebox.showerror("ERROR", "Please enter Quantity.")
            return
        if len(P) == 0:
            messagebox.showerror("ERROR", "Please enter Price.")
            return
        try:
            c.execute("""
            INSERT INTO inventory(item, quantity, price)
            VALUES(?,?,?)
            """, (I, Q, P))
            conn.commit()
            messagebox.showinfo('Congrats!', f'Data entry successful.\n{I, Q, P}')
            clear_inv()
        except Exception as e:
                messagebox.showerror("Database Error", f"An error occurred:\n{e}")
    
    # Clears curent entries
    def clear_inv():
        inv_item.delete(0, END)
        inv_quantity.delete(0, END)
        inv_price.delete(0, END)

    # Inventory Gui
    Inventory = tk.Toplevel()
    Inventory.title('POS Inventory')
    Inventory.geometry('350x350')


    tk.Label(Inventory, padx=10, text="Inventory").pack()

    i = tk.Label(Inventory, text="Item:")
    i.pack(pady=5)

    inv_item = ctk.CTkEntry(Inventory)
    inv_item.pack(pady=5)

    q = tk.Label(Inventory, text="Quantity:")
    q.pack(pady=5)

    inv_quantity = ctk.CTkEntry(Inventory)
    inv_quantity.pack(pady=5)

    p = tk.Label(Inventory, text="Price:")
    p.pack(pady=5)

    inv_price = ctk.CTkEntry(Inventory)
    inv_price.pack(pady=5)

    submit_button = ctk.CTkButton(Inventory, 
                                text_color="black", 
                                fg_color="white", 
                                hover_color="gray94", 
                                command=inv_submit, text="Submit",)
    submit_button.pack(pady=5)

    clear = ctk.CTkButton(Inventory, 
                                text_color="black", 
                                fg_color="white", 
                                hover_color="gray94", 
                                text='Clear Entries', 
                                command=clear_inv)
    clear.pack(pady=5)


# Refresh Treeview
def refresh():
    try:
        # Refresh TreeView with rowid as iid
        c.execute("SELECT item, quantity, price FROM inventory")
        global rows
        rows = c.fetchall()
        
        for child in tree.get_children():
            tree.delete(child)
        for row in rows:
            tree.insert("", tk.END, iid=row[0], values=row[0:3])
    except Exception as e:
        messagebox.showerror('Error', f"An error occurred:\n{e}")

# Delete current selection from in stock treeview
def delete_selection():
    try:
        # Get selected Treeview item
        selected_item = tree.selection()[0]
        rowid = selected_item 
        if selected_item:
            # Confirm before deleting
            if not messagebox.askyesno("Confirm Delete", f"Delete {selected_item} from inventory?"):
                return

            # Wrap DB operations in transaction
            c.execute("DELETE FROM inventory WHERE item=?", (rowid,))
            conn.commit()

            # Remove from Treeview directly (no full refresh needed)
            tree.delete(selected_item)   

        else:
            messagebox.showwarning('Warning', f"PLease make selection first.\n")

    except Exception as e:
            messagebox.showerror('Error', f"An error occurred:\n{e}")

    
#########################
# POS GUI
#########################

app = tk.Tk()
app.title('Simple POS')
app.geometry('640x300')
app.tk_setPalette("#1F1F1F")

menubar = tk.Menu(app, fg="black")
app.config(menu=menubar, pady=10)

sales = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Inv & Sales", menu=sales)
sales.add_command(label='Inventory', command=inventory)
sales.add_command(label='Sales', command=show_sales)

help = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=help)
help.add_command(label='Help', command=show_help)
help.add_command(label='About', command=show_about)
help.add_command(label='Source Code', command=open_source)

# Item quantity entry
item_q = ctk.CTkEntry(app)
item_q.grid(row=2, column=0, padx=(0, 275), pady=(2.5, 0))

# Buttons
refresh = ctk.CTkButton(app, text="🔁", 
                        fg_color="white", 
                        text_color="black", 
                        hover_color='gray50',
                        command=refresh, width=0)
refresh.grid(row=2, column=0, padx=(335, 0), pady=10)

submit = ctk.CTkButton(app, text='Submit', 
                           fg_color="white", 
                           text_color="black", 
                           hover_color='gray50',
                           command=sbmt_crnt_slctn, width=75)
submit.grid(row=2, column=0, padx=(5, 515), pady=10)

cart = ctk.CTkButton(app, text='Cart', 
                           fg_color="white", 
                           text_color="black", 
                           hover_color='gray50',
                           command=cart, width=65)
cart.grid(row=2, column=0, padx=(5, 50), pady=10)

fnlz_order = ctk.CTkButton(app, text='Finalize', 
                           fg_color="white", 
                           text_color="black", 
                           hover_color='gray50',
                           command=finalize_order, width=75)
fnlz_order.grid(row=2, column=0, padx=(500, 0), pady=10)

dlt_item = ctk.CTkButton(app, text='X', 
                         fg_color="white", 
                         text_color="black", 
                         hover_color='gray50',
                         command=delete_selection, width=3)
dlt_item.grid(row=2, column=0, padx=(395, 0), pady=10)

# Treeview Frame with in-stock items
tree_frame = ttk.Frame(app)
tree_frame.grid(row=0, column=0, padx=10)

tree = ttk.Treeview(tree_frame, columns=("col1", "col2", "col3"), show="headings")
tree.heading("col1", text="Item")
tree.heading("col2", text="Quantity")
tree.heading("col3", text="Price")
tree.grid(row=0, column=0)

scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
scrollbar.grid(row=0, column=1, sticky="ns")

tree.configure(yscrollcommand=scrollbar.set)

# Load initial rows
try:
    for row in rows:
        tree.insert("", tk.END, iid=row[0], values=row[0:3])
except Exception as e:
    messagebox.showerror('Error', f"An error occurred:\n{e}")

conn.commit()
app.mainloop()
conn.close()
