
from flask import Flask, render_template, request, redirect, url_for
from db import get_table, add_product, get_all_products, get_product, update_product, delete_product, add_review, get_reviews, get_products_by_category

app = Flask(__name__)

def validate_product_form(form):
    name = form.get('name', '').strip()
    description = form.get('description', '').strip()
    category = form.get('category', '').strip()
    price = form.get('price', '').strip()
    stock = form.get('stock', '').strip()

    if not name or not description or not category or not price or not stock:
        return "Name, description, category, price, and stock are required."

    try:
        price_value = float(price)
        stock_value = int(stock)

        if price_value < 0 or stock_value < 0:
            return "Price and stock cannot be negative."

    except ValueError:
        return "Price must be a number and stock must be a whole number."

    return None


def validate_review_form(form):
    customer_name = form.get('customer_name', '').strip()
    rating = form.get('rating', '').strip()
    comment = form.get('comment', '').strip()

    if not customer_name or not rating or not comment:
        return "Customer name, rating, and comment are required."

    try:
        rating_value = int(rating)

        if rating_value < 1 or rating_value > 5:
            return "Rating must be between 1 and 5."

    except ValueError:
        return "Rating must be a number."

    return None

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
        error = validate_product_form(request.form)

        if error:
            return render_template('add_product.html', error=error)

        add_product(
            name=request.form['name'].strip(),
            description=request.form['description'].strip(),
            category=request.form['category'].strip(),
            price=request.form['price'].strip(),
            stock=request.form['stock'].strip(),
            image_url=request.form['image_url'].strip()
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

    if product is None:
        return "Product not found", 404

    if request.method == 'POST':
        error = validate_product_form(request.form)

        if error:
            return render_template('edit_product.html', product=product, error=error)

        update_product(
            product_id=product_id,
            name=request.form['name'].strip(),
            description=request.form['description'].strip(),
            category=request.form['category'].strip(),
            price=request.form['price'].strip(),
            stock=request.form['stock'].strip(),
            image_url=request.form['image_url'].strip()
        )

        return redirect(url_for('product_detail', product_id=product_id))

    return render_template('edit_product.html', product=product)

@app.route('/delete/<product_id>')
def delete(product_id):
    product = get_product(product_id)

    if product is None:
        return "Product not found", 404

    delete_product(product_id)
    return redirect(url_for('home'))

@app.route('/review/<product_id>', methods=['POST'])
def add_review_route(product_id):
    product = get_product(product_id)

    if product is None:
        return "Product not found", 404

    error = validate_review_form(request.form)

    if error:
        return error, 400

    add_review(
        product_id=product_id,
        customer_name=request.form['customer_name'].strip(),
        rating=request.form['rating'].strip(),
        comment=request.form['comment'].strip()
    )

    return redirect(url_for('product_detail', product_id=product_id))
if __name__ == '__main__':
    app.run(debug=True)