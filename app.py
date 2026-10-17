from flask import Flask, render_template, session, redirect, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'super_secret_key_123'
# Настройка базы данных SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Модель товара
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=True)
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    total = db.Column(db.Integer, nullable=False)
@app.route('/')
def home():
    # Получаем все товары из базы
    products = Product.query.all()
    return render_template('index.html', products=products)

@app.route('/catalog')
def catalog():
    products = Product.query.all()
    return render_template('catalog.html', products=products)
@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    # Инициализируем корзину в сессии, если её нет
    if 'cart' not in session:
        session['cart'] = []
    
    # Добавляем ID товара в корзину
    cart = session['cart']
    cart.append(product_id)
    session['cart'] = cart
    
    return redirect('/cart')

@app.route('/cart')
def cart():
    # Получаем список ID товаров из сессии
    cart_ids = session.get('cart', [])
    # Находим эти товары в базе данных
    products = Product.query.filter(Product.id.in_(cart_ids)).all()
    # Считаем общую сумму
    total = sum(p.price for p in products)
    
    return render_template('cart.html', products=products, total=total)
@app.route('/checkout', methods=['GET', 'POST'])
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        name = request.form.get('name')
        address = request.form.get('address')
        phone = request.form.get('phone')
        
        cart_ids = session.get('cart', [])
        products = Product.query.filter(Product.id.in_(cart_ids)).all()
        total = sum(p.price for p in products)
        
        # Сохраняем заказ в базе
        new_order = Order(user_name=name, address=address, phone=phone, total=total)
        db.session.add(new_order)
        db.session.commit()
        
        session.pop('cart', None)
        return "<h1>Спасибо за заказ! Мы свяжемся с вами.</h1><a href='/'>На главную</a>"
    
    cart_ids = session.get('cart', [])
    products = Product.query.filter(Product.id.in_(cart_ids)).all()
    total = sum(p.price for p in products)
    return render_template('checkout.html', total=total)
@app.route('/profile')
def profile():
    orders = Order.query.all()
    return render_template('profile.html', orders=orders)
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        name = request.form.get('name')
        price = int(request.form.get('price'))
        description = request.form.get('description')
        
        new_product = Product(name=name, price=price, description=description)
        db.session.add(new_product)
        db.session.commit()
        return redirect('/admin')
        
    return render_template('add_product.html')
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Если товаров нет, добавим пару штук для теста
        if not Product.query.first():
            p1 = Product(name="Смартфон", price=25000, description="Хороший телефон")
            p2 = Product(name="Ноутбук", price=60000, description="Для учебы и работы")
            db.session.add(p1)
            db.session.add(p2)
            db.session.commit()
    app.run(debug=True)