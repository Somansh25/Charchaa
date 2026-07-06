import os
from flask import Flask, render_template, request, jsonify, abort
from dotenv import load_dotenv
from db import seed_initial_menu, get_grouped_menu, create_reservation, get_all_reservations, get_all_menu_flat, toggle_menu_item

# Initialize and load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev_charchaa_secure_key_2026')
ADMIN_TOKEN = os.getenv('ADMIN_SECRET_TOKEN', 'charchaa_admin_2026')

# Seed the database on startup
seed_initial_menu()

@app.route('/')
def index():
    """Renders the dynamic SPA with MongoDB menu data."""
    menu_data = get_grouped_menu()
    return render_template('index.html', menu=menu_data)

@app.route('/api/reserve', methods=['POST'])
def reserve():
    """API endpoint for seat & session bookings."""
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Invalid request payload"}), 400
    
    success, message = create_reservation(data)
    if success:
        return jsonify({"success": True, "message": message})
    else:
        return jsonify({"success": False, "message": message}), 400

@app.route('/admin')
def admin():
    """Secure Micro-Admin Dashboard."""
    token = request.args.get('token')
    if token != ADMIN_TOKEN:
        abort(403) # Forbidden if token doesn't match
    
    reservations = get_all_reservations()
    menu_items = get_all_menu_flat()
    return render_template('admin.html', reservations=reservations, menu_items=menu_items, token=token)

@app.route('/api/menu/toggle', methods=['POST'])
def toggle_availability():
    """Toggles item availability for the live menu."""
    data = request.get_json()
    token = data.get('token')
    
    if token != ADMIN_TOKEN:
        return jsonify({"success": False, "message": "Unauthorized"}), 401
        
    item_id = data.get('id')
    new_status = data.get('available')
    
    try:
        toggle_menu_item(item_id, new_status)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

if __name__ == '__main__':
    # Standard production-ready local execution entrypoint
    app.run(host='0.0.0.0', port=5003, debug=True)
