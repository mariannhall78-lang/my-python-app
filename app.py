import os
from flask import Flask, render_template, send_from_directory, request, redirect, url_for, flash, jsonify
from extensions import db
from models import Product
from sqlalchemy import func

AZURE_ROOT = "/home/site/wwwroot"
BASE_DIR = AZURE_ROOT if os.path.isdir(AZURE_ROOT) else os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'products.db')}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = os.environ.get("SECRET_KEY", "change-me-in-production")

db.init_app(app)


@app.before_request
def _init_db():
    db.create_all()
    seed_data()
    app.before_request_funcs[None].remove(_init_db)


def seed_data():
    if Product.query.count() == 0:
        samples = [
            Product(barcode="5000112637922", name="Heinz Tomato Ketchup", brand="Heinz", category="Condiments", calories=101, weight_g=570),
            Product(barcode="0016000275522", name="Cheerios", brand="General Mills", category="Cereals", calories=367, weight_g=340),
            Product(barcode="0041196898698", name="Organic Whole Milk", brand="Horizon", category="Dairy", calories=149, weight_g=946),
            Product(barcode="7622210449283", name="Oreo Original", brand="Nabisco", category="Biscuits", calories=471, weight_g=154),
            Product(barcode="4006381333931", name="Haribo Gold-Bears", brand="Haribo", category="Confectionery", calories=343, weight_g=200),
            Product(barcode="5010477348678", name="Coca-Cola Classic 330ml", brand="Coca-Cola", category="Beverages", calories=139, weight_g=330),
            Product(barcode="0037600101882", name="Del Monte Sweet Peas", brand="Del Monte", category="Canned Goods", calories=62, weight_g=425),
            Product(barcode="0011110872456", name="Simple Truth Almonds", brand="Simple Truth", category="Nuts & Seeds", calories=579, weight_g=227),
        ]
        db.session.add_all(samples)
        db.session.commit()


@app.route("/")
def home():
    total = Product.query.count()
    categories = db.session.query(Product.category, func.count(Product.id)).group_by(Product.category).all()
    recent = Product.query.order_by(Product.created_at.desc()).limit(5).all()
    return render_template("dashboard.html", total=total, categories=categories, recent=recent)


@app.route("/products")
def products():
    q = request.args.get("q", "").strip()
    if q:
        like = f"%{q}%"
        results = Product.query.filter(
            (Product.name.ilike(like)) | (Product.barcode.ilike(like)) | (Product.brand.ilike(like))
        ).order_by(Product.name).all()
    else:
        results = Product.query.order_by(Product.name).all()
    return render_template("products.html", products=results, q=q)


@app.route("/products/<barcode>")
def product_detail(barcode):
    product = Product.query.filter_by(barcode=barcode).first_or_404()
    return render_template("product_detail.html", product=product)


@app.route("/products/add", methods=["GET", "POST"])
def add_product():
    if request.method == "POST":
        barcode = request.form.get("barcode", "").strip()
        name = request.form.get("name", "").strip()
        if not barcode or not name:
            flash("Barcode and name are required.", "danger")
            return render_template("add_product.html", form=request.form)
        if Product.query.filter_by(barcode=barcode).first():
            flash("A product with that barcode already exists.", "warning")
            return render_template("add_product.html", form=request.form)
        product = Product(
            barcode=barcode,
            name=name,
            brand=request.form.get("brand", "").strip() or None,
            category=request.form.get("category", "").strip() or None,
            calories=float(request.form["calories"]) if request.form.get("calories") else None,
            weight_g=float(request.form["weight_g"]) if request.form.get("weight_g") else None,
        )
        db.session.add(product)
        db.session.commit()
        flash(f"Product '{name}' added successfully.", "success")
        return redirect(url_for("product_detail", barcode=barcode))
    return render_template("add_product.html", form=request.args)


@app.route("/scan")
def scan():
    return render_template("scan.html")


@app.route("/api/barcode/<barcode>")
def api_barcode(barcode):
    product = Product.query.filter_by(barcode=barcode).first()
    if product:
        return jsonify({"found": True, "product": product.to_dict()})
    return jsonify({"found": False, "barcode": barcode}), 404


@app.route("/files/<path:filename>")
def files(filename):
    return send_from_directory(BASE_DIR, filename)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        seed_data()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
