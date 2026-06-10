
from flask import Flask, render_template, request, redirect, url_for
from db import get_table, add_product, get_all_products, get_product, update_product, delete_product, add_review, get_reviews, get_products_by_category

app = Flask(__name__)

@app.route('/')
def home():
    category = request.args.get('category')

    if category:
        products = get_products_by_category(category)
    else:
        products = get_all_products()

    return render_template(
        'index.html',
        products=products,
        selected_category=category
    )

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

    if product is None:
        return "Product not found", 404

    reviews = get_reviews(product_id)

    reviews = sorted(reviews, key=lambda r: r['timestamp'], reverse=True)

    if len(reviews) > 0:
        total = sum(int(review['rating']) for review in reviews)
        average_rating = round(total / len(reviews), 1)
    else:
        average_rating = None

    return render_template(
        'product.html',
        product=product,
        reviews=reviews,
        average_rating=average_rating
    )
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

@app.route('/review/<product_id>', methods=['POST'])
def add_review_route(product_id):
    add_review(
        product_id=product_id,
        customer_name=request.form['customer_name'],
        rating=request.form['rating'],
        comment=request.form['comment']
    )
    return redirect(url_for('product_detail', product_id=product_id))

if __name__ == '__main__':
    app.run(debug=True)