from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
from psycopg2 import pool
from datetime import datetime, timedelta
import os
import jwt
from functools import wraps
import hashlib

app = Flask(__name__)
CORS(app)

# Configuration
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'
app.config['JWT_EXPIRATION_HOURS'] = 24

# Database connection pool
db_pool = psycopg2.pool.SimpleConnectionPool(
    1, 20,
    host="localhost",
    database="sweets_shop",
    user="postgres",
    password="Sejal@385",
    port="5432"
)

def get_db_connection():
    return db_pool.getconn()

def release_db_connection(conn):
    db_pool.putconn(conn)

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def generate_token(user_id, username, role):
    """Generate JWT token"""
    payload = {
        'user_id': user_id,
        'username': username,
        'role': role,
        'exp': datetime.utcnow() + timedelta(hours=app.config['JWT_EXPIRATION_HOURS'])
    }
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

def verify_token(token):
    """Verify JWT token"""
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def token_required(f):
    """Decorator to require authentication"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            if token.startswith('Bearer '):
                token = token[7:]
            payload = verify_token(token)
            if not payload:
                return jsonify({'error': 'Token is invalid or expired'}), 401
            request.current_user = payload
        except Exception as e:
            return jsonify({'error': 'Token verification failed'}), 401
        
        return f(*args, **kwargs)
    
    return decorated

def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.current_user.get('role') != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        return f(*args, **kwargs)
    
    return decorated

# ============= AUTHENTICATION API =============
@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.json
    conn = get_db_connection()
    
    try:
        # Validate input
        if not data.get('username') or not data.get('password'):
            return jsonify({'error': 'Username and password are required'}), 400
        
        if len(data['password']) < 6:
            return jsonify({'error': 'Password must be at least 6 characters'}), 400
        
        cur = conn.cursor()
        
        # Check if username already exists
        cur.execute("SELECT user_id FROM users WHERE username = %s", (data['username'],))
        if cur.fetchone():
            cur.close()
            return jsonify({'error': 'Username already exists'}), 400
        
        # Hash password and insert user
        hashed_password = hash_password(data['password'])
        role = data.get('role', 'customer')  # Default to customer
        
        # Validate role
        if role not in ['admin', 'customer']:
            role = 'customer'
        
        cur.execute("""
            INSERT INTO users (username, password_hash, role, full_name, email, phone)
            VALUES (%s, %s, %s, %s, %s, %s) RETURNING user_id
        """, (data['username'], hashed_password, role, 
              data.get('full_name', ''), data.get('email', ''), data.get('phone', '')))
        
        user_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        
        # Generate token
        token = generate_token(user_id, data['username'], role)
        
        return jsonify({
            'message': 'User registered successfully',
            'token': token,
            'user': {
                'id': user_id,
                'username': data['username'],
                'role': role,
                'full_name': data.get('full_name', '')
            }
        }), 201
        
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        release_db_connection(conn)

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json
    conn = get_db_connection()
    
    try:
        if not data.get('username') or not data.get('password'):
            return jsonify({'error': 'Username and password are required'}), 400
        
        cur = conn.cursor()
        cur.execute("""
            SELECT user_id, username, password_hash, role, full_name, email, phone
            FROM users WHERE username = %s
        """, (data['username'],))
        
        user = cur.fetchone()
        cur.close()
        
        if not user:
            return jsonify({'error': 'Invalid username or password'}), 401
        
        # Verify password
        hashed_password = hash_password(data['password'])
        if hashed_password != user[2]:
            return jsonify({'error': 'Invalid username or password'}), 401
        
        # Generate token
        token = generate_token(user[0], user[1], user[3])
        
        return jsonify({
            'message': 'Login successful',
            'token': token,
            'user': {
                'id': user[0],
                'username': user[1],
                'role': user[3],
                'full_name': user[4],
                'email': user[5],
                'phone': user[6]
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        release_db_connection(conn)

@app.route('/api/auth/verify', methods=['GET'])
@token_required
def verify():
    """Verify if token is valid"""
    return jsonify({
        'valid': True,
        'user': {
            'id': request.current_user['user_id'],
            'username': request.current_user['username'],
            'role': request.current_user['role']
        }
    }), 200

# ============= PRODUCTS API =============
@app.route('/api/products', methods=['GET'])
def get_products():
    """Get all products (public access)"""
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        
        # Get search and filter parameters
        search = request.args.get('search', '')
        category = request.args.get('category', '')
        
        query = """
            SELECT product_id, product_name, category, price, 
                   stock_quantity, unit, description 
            FROM products WHERE 1=1
        """
        params = []
        
        if search:
            query += " AND (product_name ILIKE %s OR description ILIKE %s)"
            params.extend([f'%{search}%', f'%{search}%'])
        
        if category:
            query += " AND category = %s"
            params.append(category)
        
        query += " ORDER BY product_name"
        
        cur.execute(query, params)
        products = cur.fetchall()
        cur.close()
        
        result = []
        for p in products:
            result.append({
                'id': p[0],
                'name': p[1],
                'category': p[2],
                'price': float(p[3]),
                'stock': p[4],
                'unit': p[5],
                'description': p[6]
            })
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        release_db_connection(conn)

@app.route('/api/products/categories', methods=['GET'])
def get_categories():
    """Get all unique categories"""
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT category FROM products ORDER BY category")
        categories = cur.fetchall()
        cur.close()
        
        return jsonify([c[0] for c in categories]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        release_db_connection(conn)

@app.route('/api/products', methods=['POST'])
@token_required
@admin_required
def add_product():
    """Add product (admin only)"""
    data = request.json
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO products (product_name, category, price, stock_quantity, unit, description)
            VALUES (%s, %s, %s, %s, %s, %s) RETURNING product_id
        """, (data['name'], data['category'], data['price'], 
              data['stock'], data['unit'], data.get('description', '')))
        product_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        return jsonify({'id': product_id, 'message': 'Product added successfully'}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        release_db_connection(conn)

@app.route('/api/products/<int:product_id>', methods=['PUT'])
@token_required
@admin_required
def update_product(product_id):
    """Update product (admin only)"""
    data = request.json
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            UPDATE products 
            SET product_name=%s, category=%s, price=%s, 
                stock_quantity=%s, unit=%s, description=%s, updated_at=CURRENT_TIMESTAMP
            WHERE product_id=%s
        """, (data['name'], data['category'], data['price'], 
              data['stock'], data['unit'], data.get('description', ''), product_id))
        conn.commit()
        cur.close()
        return jsonify({'message': 'Product updated successfully'}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        release_db_connection(conn)

@app.route('/api/products/<int:product_id>', methods=['DELETE'])
@token_required
@admin_required
def delete_product(product_id):
    """Delete product (admin only)"""
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM products WHERE product_id=%s", (product_id,))
        conn.commit()
        cur.close()
        return jsonify({'message': 'Product deleted successfully'}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        release_db_connection(conn)

# ============= CUSTOMERS API =============
@app.route('/api/customers', methods=['GET'])
@token_required
@admin_required
def get_customers():
    """Get all customers (admin only)"""
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT customer_id, customer_name, phone, email, address 
            FROM customers ORDER BY customer_name
        """)
        customers = cur.fetchall()
        cur.close()
        
        result = []
        for c in customers:
            result.append({
                'id': c[0],
                'name': c[1],
                'phone': c[2],
                'email': c[3],
                'address': c[4]
            })
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        release_db_connection(conn)

@app.route('/api/customers', methods=['POST'])
@token_required
@admin_required
def add_customer():
    """Add customer (admin only)"""
    data = request.json
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO customers (customer_name, phone, email, address)
            VALUES (%s, %s, %s, %s) RETURNING customer_id
        """, (data['name'], data['phone'], data.get('email', ''), data.get('address', '')))
        customer_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        return jsonify({'id': customer_id, 'message': 'Customer added successfully'}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        release_db_connection(conn)

# ============= ORDERS API =============
@app.route('/api/orders', methods=['GET'])
@token_required
def get_orders():
    """Get orders - all for admin, own for customers"""
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        
        if request.current_user['role'] == 'admin':
            # Admin sees all orders
            cur.execute("""
                SELECT o.order_id, o.order_date, c.customer_name, 
                       o.total_amount, o.payment_method, o.status
                FROM orders o
                JOIN customers c ON o.customer_id = c.customer_id
                ORDER BY o.order_date DESC
            """)
        else:
            # Customer sees only their orders
            cur.execute("""
                SELECT o.order_id, o.order_date, c.customer_name, 
                       o.total_amount, o.payment_method, o.status
                FROM orders o
                JOIN customers c ON o.customer_id = c.customer_id
                WHERE o.user_id = %s
                ORDER BY o.order_date DESC
            """, (request.current_user['user_id'],))
        
        orders = cur.fetchall()
        cur.close()
        
        result = []
        for o in orders:
            result.append({
                'id': o[0],
                'date': o[1].isoformat(),
                'customerName': o[2],
                'total': float(o[3]),
                'paymentMethod': o[4],
                'status': o[5]
            })
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        release_db_connection(conn)

@app.route('/api/orders', methods=['POST'])
@token_required
def create_order():
    """Create order (authenticated users)"""
    data = request.json
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        
        # Calculate total and validate stock
        total_amount = 0
        order_items = []
        
        for item in data['items']:
            cur.execute("""
                SELECT price, stock_quantity, product_name FROM products WHERE product_id=%s
            """, (item['productId'],))
            result = cur.fetchone()
            
            if not result:
                raise Exception(f"Product {item['productId']} not found")
            
            price, stock, product_name = result
            if stock < item['quantity']:
                raise Exception(f"Insufficient stock for {product_name}. Available: {stock}")
            
            if stock == 0:
                raise Exception(f"{product_name} is out of stock")
            
            subtotal = float(price) * item['quantity']
            total_amount += subtotal
            order_items.append((item['productId'], item['quantity'], price, subtotal))
        
        # Get or create customer
        customer_id = data.get('customerId')
        if not customer_id:
            # Create anonymous customer from user info
            cur.execute("""
                INSERT INTO customers (customer_name, phone, email)
                VALUES (%s, %s, %s) RETURNING customer_id
            """, (data.get('customerName', 'Customer'), 
                  data.get('customerPhone', ''), 
                  data.get('customerEmail', '')))
            customer_id = cur.fetchone()[0]
        
        # Create order
        cur.execute("""
            INSERT INTO orders (customer_id, user_id, total_amount, payment_method, status)
            VALUES (%s, %s, %s, %s, 'completed') RETURNING order_id
        """, (customer_id, request.current_user['user_id'], total_amount, data['paymentMethod']))
        order_id = cur.fetchone()[0]
        
        # Add order items and update stock
        for product_id, quantity, price, subtotal in order_items:
            cur.execute("""
                INSERT INTO order_items (order_id, product_id, quantity, unit_price, subtotal)
                VALUES (%s, %s, %s, %s, %s)
            """, (order_id, product_id, quantity, price, subtotal))
            
            cur.execute("""
                UPDATE products SET stock_quantity = stock_quantity - %s 
                WHERE product_id = %s
            """, (quantity, product_id))
        
        conn.commit()
        cur.close()
        return jsonify({'id': order_id, 'message': 'Order created successfully'}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        release_db_connection(conn)

@app.route('/api/orders/<int:order_id>', methods=['GET'])
@token_required
def get_order_details(order_id):
    """Get order details"""
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        
        # Check authorization
        if request.current_user['role'] != 'admin':
            cur.execute("SELECT user_id FROM orders WHERE order_id = %s", (order_id,))
            order_user = cur.fetchone()
            if not order_user or order_user[0] != request.current_user['user_id']:
                return jsonify({'error': 'Unauthorized'}), 403
        
        cur.execute("""
            SELECT o.order_id, o.order_date, c.customer_name, c.phone,
                   p.product_name, oi.quantity, oi.unit_price, oi.subtotal,
                   o.total_amount, o.payment_method, o.status, p.unit
            FROM orders o
            JOIN customers c ON o.customer_id = c.customer_id
            JOIN order_items oi ON o.order_id = oi.order_id
            JOIN products p ON oi.product_id = p.product_id
            WHERE o.order_id = %s
        """, (order_id,))
        details = cur.fetchall()
        cur.close()
        
        if not details:
            return jsonify({'error': 'Order not found'}), 404
        
        items = []
        for d in details:
            items.append({
                'productName': d[4],
                'quantity': float(d[5]),
                'unitPrice': float(d[6]),
                'subtotal': float(d[7]),
                'unit': d[11]
            })
        
        result = {
            'id': details[0][0],
            'date': details[0][1].isoformat(),
            'customerName': details[0][2],
            'customerPhone': details[0][3],
            'items': items,
            'total': float(details[0][8]),
            'paymentMethod': details[0][9],
            'status': details[0][10]
        }
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        release_db_connection(conn)

# ============= DASHBOARD API =============
@app.route('/api/dashboard', methods=['GET'])
@token_required
@admin_required
def get_dashboard():
    """Get dashboard stats (admin only)"""
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        
        # Total sales today
        cur.execute("""
            SELECT COALESCE(SUM(total_amount), 0) 
            FROM orders 
            WHERE DATE(order_date) = CURRENT_DATE
        """)
        today_sales = float(cur.fetchone()[0])
        
        # Total orders today
        cur.execute("""
            SELECT COUNT(*) FROM orders 
            WHERE DATE(order_date) = CURRENT_DATE
        """)
        today_orders = cur.fetchone()[0]
        
        # Low stock products
        cur.execute("""
            SELECT COUNT(*) FROM products WHERE stock_quantity < 10
        """)
        low_stock = cur.fetchone()[0]
        
        # Total customers
        cur.execute("SELECT COUNT(*) FROM customers")
        total_customers = cur.fetchone()[0]
        
        cur.close()
        
        return jsonify({
            'todaySales': today_sales,
            'todayOrders': today_orders,
            'lowStock': low_stock,
            'totalCustomers': total_customers
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        release_db_connection(conn)

if __name__ == '__main__':
    app.run(debug=True, port=5000)