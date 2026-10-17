from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
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
    return "<h1>Страница каталога в разработке</h1>"

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