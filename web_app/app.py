from flask import Flask, render_template, request, redirect, url_for, session, flash, abort
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
from functools import wraps

app = Flask(__name__)
app.secret_key = 'super_secret_key_change_this_in_production'

# Database Configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'billing.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- Models ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='staff') # 'admin' or 'staff'

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50))
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)

class Bill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice_number = db.Column(db.String(20), unique=True, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    customer_name = db.Column(db.String(100))
    subtotal = db.Column(db.Float, nullable=False)
    tax_amount = db.Column(db.Float, nullable=False)
    discount_amount = db.Column(db.Float, default=0.0)
    grand_total = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(20), nullable=False)
    items = db.relationship('BillItem', backref='bill', lazy=True)

class BillItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bill_id = db.Column(db.Integer, db.ForeignKey('bill.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    product_name = db.Column(db.String(100)) # Store name for history even if product deleted
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False) # Price at time of sale

# --- Decorators ---
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'role' not in session or session['role'] != 'admin':
            flash('Access Denied: Admins only', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def staff_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'role' not in session or session['role'] != 'staff':
            # Optionally allow admin to access staff pages too, or restrict strictly.
            # Based on requirements: "Billing staff will have... Admin can monitor..."
            # Strict separation requested by user prompt implication.
            flash('Access Denied: Staff only', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# --- Routes ---

# Authentication
@app.route('/')
def login():
    if 'user_id' in session:
        if session.get('role') == 'admin':
            return redirect(url_for('dashboard'))
        elif session.get('role') == 'staff':
            return redirect(url_for('billing'))
    return render_template('login.html')

@app.route('/login_post', methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']
    
    user = User.query.filter_by(username=username).first()
    
    if user and check_password_hash(user.password, password):
        session['user_id'] = user.id
        session['username'] = user.username
        session['role'] = user.role
        
        if user.role == 'admin':
            return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('billing'))
    else:
        flash('Invalid Credentials', 'error')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Dashboard (Admin Only)
@app.route('/dashboard')
@login_required
@admin_required
def dashboard():
    product_count = Product.query.count()
    bill_count = Bill.query.count()
    total_sales = db.session.query(db.func.sum(Bill.grand_total)).scalar() or 0
    
    recent_bills = Bill.query.order_by(Bill.date.desc()).limit(5).all()
    
    return render_template('dashboard.html', 
                           product_count=product_count, 
                           bill_count=bill_count, 
                           total_sales=total_sales,
                           recent_bills=recent_bills)

# Sales History (Admin Only)
@app.route('/sales_history')
@login_required
@admin_required
def sales_history():
    bills = Bill.query.order_by(Bill.date.desc()).all()
    total_revenue = sum(b.grand_total for b in bills)
    return render_template('sales_history.html', bills=bills, total_revenue=total_revenue)

# Product Management (Staff Only)
@app.route('/products')
@login_required
@staff_required
def products():
    all_products = Product.query.all()
    return render_template('products.html', products=all_products)

@app.route('/add_product', methods=['POST'])
@login_required
@staff_required
def add_product():
    name = request.form['name']
    category = request.form['category']
    price = float(request.form['price'])
    stock = int(request.form['stock'])
    
    new_product = Product(name=name, category=category, price=price, stock=stock)
    db.session.add(new_product)
    db.session.commit()
    flash('Product Added Successfully', 'success')
    return redirect(url_for('products'))

@app.route('/delete_product/<int:id>')
@login_required
@staff_required
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('products'))

@app.route('/edit_product/<int:id>', methods=['GET', 'POST'])
@login_required
@staff_required
def edit_product(id):
    product = Product.query.get_or_404(id)
    
    if request.method == 'POST':
        product.name = request.form['name']
        product.category = request.form['category']
        product.price = float(request.form['price'])
        product.stock = int(request.form['stock'])
        
        db.session.commit()
        flash('Product Updated Successfully', 'success')
        return redirect(url_for('products'))
        
    return render_template('edit_product.html', product=product)

# Billing System (Staff Only)
@app.route('/billing')
@login_required
@staff_required
def billing():
    products = Product.query.all()
    return render_template('billing.html', products=products)

@app.route('/create_bill', methods=['POST'])
@login_required
@staff_required
def create_bill():
    customer_name = request.form['customer_name']
    product_ids = request.form.getlist('product_id[]')
    quantities = request.form.getlist('quantity[]')
    
    discount_val = float(request.form.get('discount', 0))
    discount_type = request.form.get('discount_type', 'flat') # 'flat' or 'percent'
    payment_method = request.form.get('payment_method', 'Cash')
    
    subtotal = 0
    bill_items = []
    
    # First pass: Validation and Subtotal Calculation
    for i in range(len(product_ids)):
        pid = int(product_ids[i])
        qty = int(quantities[i])
        
        product = Product.query.get(pid)
        if product.stock < qty:
            flash(f'Insufficient stock for {product.name}', 'error')
            return redirect(url_for('billing'))
            
        line_total = product.price * qty
        subtotal += line_total
        
        bill_items.append({
            'product': product,
            'qty': qty,
            'price': product.price
        })

    # Output tax calculation (5%)
    tax_rate = 0.05
    tax_amount = subtotal * tax_rate
    
    # Discount calculation
    discount_amount = 0
    if discount_type == 'percent':
        discount_amount = (subtotal * discount_val) / 100
    else:
        discount_amount = discount_val
        
    grand_total = subtotal + tax_amount - discount_amount
    if grand_total < 0: grand_total = 0

    # Generate Invoice Number (INV-YYYY-XXXX)
    year = datetime.utcnow().year
    last_bill = Bill.query.order_by(Bill.id.desc()).first()
    new_id = 1
    if last_bill:
        new_id = last_bill.id + 1
    invoice_number = f"INV-{year}-{new_id:04d}"

    # Second pass: Commit to DB
    new_bill = Bill(
        invoice_number=invoice_number,
        customer_name=customer_name, 
        subtotal=subtotal,
        tax_amount=tax_amount,
        discount_amount=discount_amount,
        grand_total=grand_total,
        payment_method=payment_method
    )
    db.session.add(new_bill)
    db.session.flush() # flush to get bill ID
    
    for item in bill_items:
        # Deduct stock
        item['product'].stock -= item['qty']
        
        # Create Bill Item
        new_item = BillItem(
            bill_id=new_bill.id,
            product_id=item['product'].id,
            product_name=item['product'].name,
            quantity=item['qty'],
            price=item['price']
        )
        db.session.add(new_item)
        
    db.session.commit()
    return redirect(url_for('invoice', id=new_bill.id))

@app.route('/invoice/<int:id>')
@login_required
def invoice(id):
    # Invoice accessible by both roles ideally, or restrict if needed.
    # Letting both view invoice receipt.
    bill = Bill.query.get_or_404(id)
    return render_template('invoice.html', bill=bill)

# Initial Setup
def init_db():
    with app.app_context():
        db.create_all()
        
        # Create default admin
        if not User.query.filter_by(username='admin').first():
            hashed_pw = generate_password_hash('admin123')
            admin = User(username='admin', password=hashed_pw, role='admin')
            db.session.add(admin)
            print("Default admin created (admin/admin123)")

        # Create default staff
        if not User.query.filter_by(username='staff').first():
            hashed_pw = generate_password_hash('staff123')
            staff = User(username='staff', password=hashed_pw, role='staff')
            db.session.add(staff)
            print("Default staff created (staff/staff123)")
            
        db.session.commit()

if __name__ == '__main__':
    if not os.path.exists('billing.db'):
        init_db()
    app.run(debug=True)
