from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory data stores
items = []
cart = {}

# Utility function to generate new item IDs
def generate_id():
    return len(items) + 1

# Item class definition
class Item:
    def __init__(self, item_id, name, description, price):
        self.item_id = item_id
        self.name = name
        self.description = description
        self.price = price

    # Convert object to dictionary for JSON response
    def to_dict(self):
        return {
            "id": self.item_id,
            "name": self.name,
            "description": self.description,
            "price": self.price
        }

# Preload some food items
def preload_items():
    item1 = Item(generate_id(), "Vegemite", "Iconic Aussie spread.", 5.99)
    items.append(item1)

    item2 = Item(generate_id(), "Tim Tam", "Classic chocolate biscuit.", 3.50)
    items.append(item2)

    item3 = Item(generate_id(), "Lamingtons", "Square sponge cakes coated in chocolate and coconut.", 4.00)
    items.append(item3)

# GET /items - return all available items
@app.route('/items', methods=['GET'])
def get_items():
    return jsonify([item.to_dict() for item in items])

# GET /cart - return current shopping cart
@app.route('/cart', methods=['GET'])
def get_cart():
    return jsonify(cart)

# POST /items - add a new item to the list
@app.route('/items', methods=['POST'])
def create_item():
    data = request.json
    new_item = Item(generate_id(), data['name'], data['description'], data['price'])
    items.append(new_item)
    return jsonify(new_item.to_dict()), 201

# POST /cart - add an item to the cart
@app.route('/cart', methods=['POST'])
def add_to_cart():
    data = request.json
    item_id = data.get('id')
    for item in items:
        if item.item_id == item_id:
            if item_id in cart:
                cart[item_id]['quantity'] += 1
            else:
                cart[item_id] = {'item': item.to_dict(), 'quantity': 1}
            return jsonify(cart[item_id])
    return jsonify({'error': 'Item not found'}), 404

# Run the app
if __name__ == '__main__':
    preload_items()
    app.run(debug=True)
