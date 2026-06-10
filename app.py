from flask import Flask, render_template, request, redirect, url_for
from db import get_table, add_product, get_all_products, get_product, update_product, delete_product

app = Flask(__name__)

@app.route('/')
def home():
    products = get_all_products()
    return render_template('index.html', products=products)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        add_product(
            name=request.form['name'],
            description=request.form['description'],
            category=request.form['category'],
            price=request.form['price'],
            stock=request.form['stock'],
            image_url=request.form['image_url']
        )
        return redirect(url_for('home'))
    return render_template('add_product.html')

@app.route('/product/<product_id>')
def product_detail(product_id):
    product = get_product(product_id)
    return render_template('product.html', product=product)

@app.route('/edit/<product_id>', methods=['GET', 'POST'])
def edit(product_id):
    product = get_product(product_id)
    if request.method == 'POST':
        update_product(
            product_id=product_id,
            name=request.form['name'],
            description=request.form['description'],
            category=request.form['category'],
            price=request.form['price'],
            stock=request.form['stock'],
            image_url=request.form['image_url']
        )
        return redirect(url_for('product_detail', product_id=product_id))
    return render_template('edit_product.html', product=product)

@app.route('/delete/<product_id>')
def delete(product_id):
    delete_product(product_id)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)