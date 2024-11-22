from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def connect_to_db(username='postgres', password='123456'):
    try:
        connection = psycopg2.connect(
            dbname="quanly_quanao",
            user=username,
            password=password,
            host="localhost"
        )
        return connection
    except psycopg2.OperationalError as e:
        return None

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        connection = connect_to_db(username, password)
        if connection:
            flash("Đăng nhập thành công!")
            return redirect(url_for('menu'))
        else:
            flash("Tên đăng nhập hoặc mật khẩu sai!")
    return render_template('login.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/search_product', methods=['GET', 'POST'])
def search_product():
    products = []
    if request.method == 'POST':
        product_name = request.form['product_name']
        connection = connect_to_db()
        if connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM products WHERE product_name ILIKE %s", ('%' + product_name + '%',))
                products = cursor.fetchall()
    return render_template('search_product.html', products=products)

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        product_name = request.form['product_name']
        product_price = request.form['product_price']
        category_id = request.form['category_id']
        connection = connect_to_db()
        if connection:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO products (product_name, product_price, category_id) VALUES (%s, %s, %s)", (product_name, product_price, category_id))
                connection.commit()
            flash("Thêm sản phẩm thành công!")
            return redirect(url_for('menu'))
        else:
            flash("Không thể kết nối đến cơ sở dữ liệu!")
    return render_template('add_product.html')

if __name__ == '__main__':
    app.run(debug=True)
