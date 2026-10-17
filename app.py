from flask import Flask, render_template, session, redirect
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
# Этот блок создаст базу данных и добавит товары при первом запуске
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