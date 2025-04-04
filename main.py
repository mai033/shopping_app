import tkinter as tk
from tkinter import messagebox
import requests

BASE_URL = "http://127.0.0.1:5000"

class ShoppingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Shopping App")

        self.items = []
        self.fetch_items()

        self.setup_ui()

    def setup_ui(self):
        self.item_frame = tk.Frame(self.root)
        self.item_frame.pack(pady=10)

        # Button to show cart items
        self.cart_button = tk.Button(self.root, text="Show Cart", command=self.show_cart)
        self.cart_button.pack(pady=10)

        # Button to create new item
        self.new_item_button = tk.Button(self.root, text="New Item", command=self.new_item_window)
        self.new_item_button.pack(pady=10)

        self.render_items()

    # Get items from Flask API
    def fetch_items(self):
        response = requests.get(f"{BASE_URL}/items")
        if response.status_code == 200:
            self.items = response.json()

    # Render item list in the GUI
    def render_items(self):
        # Clear previous widgets
        for widget in self.item_frame.winfo_children():
            widget.destroy()

        for item in self.items:
            frame = tk.Frame(self.item_frame)
            frame.pack(padx=10, pady=5)
            
            # Show item name, price, description
            tk.Label(frame, text=item['name']).pack(side=tk.LEFT)
            tk.Label(frame, text=f"${item['price']:.2f} - {item['description']}").pack(side=tk.LEFT)
            # Add to cart button
            tk.Button(frame, text="Add to Cart", command=lambda id=item['id']: self.add_to_cart(id)).pack(side=tk.LEFT)

     # GET /cart from backend and show items
    def show_cart(self):
        response = requests.get(f"{BASE_URL}/cart")
        if response.status_code == 200:
            cart_data = response.json()
            cart_details = "\n".join([
                f"{item['item']['name']} x{item['quantity']} (${item['item']['price']:.2f})"
                for item in cart_data.values()
            ])
            messagebox.showinfo("Shopping Cart", cart_details or "Your cart is empty.")

    # Add item to cart by POST /cart
    def add_to_cart(self, item_id):
        response = requests.post(f"{BASE_URL}/cart", json={'id': item_id})
        if response.status_code == 200:
            messagebox.showinfo("Success", "Item added to cart!")
            self.render_items()
        else:
            messagebox.showerror("Error", "Could not add item to cart.")

    # Open popup window to create a new item
    def new_item_window(self):
        self.new_item_window = tk.Toplevel(self.root)
        self.new_item_window.title("New Item")

        tk.Label(self.new_item_window, text="Name").pack()
        self.name_entry = tk.Entry(self.new_item_window)
        self.name_entry.pack()

        tk.Label(self.new_item_window, text="Description").pack()
        self.description_entry = tk.Entry(self.new_item_window)
        self.description_entry.pack()

        tk.Label(self.new_item_window, text="Price").pack()
        self.price_entry = tk.Entry(self.new_item_window)
        self.price_entry.pack()

        tk.Button(self.new_item_window, text="Create", command=self.create_item).pack(pady=5)

    # POST /items to create new item
    def create_item(self):
        try:
            name = self.name_entry.get()
            description = self.description_entry.get()
            price = float(self.price_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Price must be a valid number.")
            return

        response = requests.post(f"{BASE_URL}/items", json={'name': name, 'description': description, 'price': price})
        if response.status_code == 201:
            messagebox.showinfo("Success", "Item created!")
            self.fetch_items()
            self.new_item_window.destroy()
            self.render_items()
        else:
            messagebox.showerror("Error", "Could not create item.")

# Run the GUI app
if __name__ == '__main__':
    root = tk.Tk()
    app = ShoppingApp(root)
    root.mainloop()
