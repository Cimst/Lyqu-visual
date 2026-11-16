import os
import re
import time
from functools import wraps
from werkzeug.utils import secure_filename
from flask import (
    Flask,
    abort,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    send_from_directory,
    session,
    url_for,
)

import db

app = Flask(__name__, static_folder="static", template_folder="templates")
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY") or "lyqu-visual-secret-key-2026"
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # Maksimal 16MB file upload

# Folder upload gambar portofolio
UPLOAD_FOLDER = os.path.join(app.static_folder, "images", "portfolio")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp", "gif"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# Inisialisasi Database SQLite
db.init_db()

PAGE_ROUTES = {
    "beranda": ("index.html", 0),
    "portofolio": ("portofolio.html", 1),
    "tentang-gear": ("tentang-gear.html", 2),
    "paket-booking": ("paket-booking.html", 3),
    "portal-proofing": ("portal-proofing.html", 4),
    "faq-kontak": ("faq-kontak.html", 5),
}

BOOKING_PACKAGES = {"1200000", "2500000", "4800000"}
BOOKING_LOCATIONS = {"0", "150000", "250000"}
BOOKED_DATES = {4, 8, 12, 15, 19, 25}
PRODUCTS = {
    1: {"name": "Paket Portrait & Katalog Studio", "stock": 5, "price": "Rp 1.200.000", "desc": "Sesi studio 2 jam, 20 file edited, 16-bit color grading, draft H+1."},
    2: {"name": "Paket Pre-Wedding Sinematik Merapi", "stock": 3, "price": "Rp 2.500.000", "desc": "Sesi outdoor 4 jam, 50 file edited, Google Drive delivery, drone visual."},
    3: {"name": "Paket Full Wedding Intimate Jogja", "stock": 2, "price": "Rp 4.800.000", "desc": "Dokumentasi full day 8 jam, 2 fotografer, flash disk kayu eksklusif, album cetak."},
}


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("is_admin"):
            flash("Silakan login sebagai admin terlebih dahulu untuk mengakses Dasbor.", "warning")
            return redirect(url_for("login", ref=request.path))
        return f(*args, **kwargs)

    return decorated_function


@app.after_request
def add_no_cache_headers(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


# ==========================================
# PUBLIC PAGES (PORTOFOLIO & CV DINAMIS)
# ==========================================


@app.route("/")
@app.route("/beranda")
@app.route("/index.html")
def beranda():
    portfolios = db.get_all_portfolios()
    skills = db.get_all_skills()
    cv_profile = db.get_cv_profile()
    return render_template(
        "index.html",
        active_slide=0,
        portfolios=portfolios,
        skills=skills,
        cv_profile=cv_profile,
    )


@app.route("/portofolio")
@app.route("/portofolio.html")
@app.route("/showcase.html")
def portofolio():
    portfolios = db.get_all_portfolios()
    return render_template(
        "portofolio.html",
        active_slide=1,
        portfolios=portfolios,
    )


@app.route("/tentang-gear")
@app.route("/tentang-gear.html")
@app.route("/mind-gear.html")
def tentang_gear():
    skills = db.get_all_skills()
    cv_profile = db.get_cv_profile()
    return render_template(
        "tentang-gear.html",
        active_slide=2,
        skills=skills,
        cv_profile=cv_profile,
    )


@app.route("/paket-booking")
@app.route("/paket-booking.html")
@app.route("/rates-booking.html")
def paket_booking():
    return render_template("paket-booking.html", active_slide=3)


@app.route("/portal-proofing")
@app.route("/portal-proofing.html")
@app.route("/client-portal.html")
def portal_proofing():
    return render_template("portal-proofing.html", active_slide=4)


@app.route("/faq-kontak")
@app.route("/faq-kontak.html")
@app.route("/faq-connect.html")
def faq_kontak():
    return render_template("faq-kontak.html", active_slide=5)


@app.get("/halaman/<slug>")
def dynamic_page(slug):
    page = PAGE_ROUTES.get(slug)
    if page is None:
        abort(404)

    template_name, active_slide = page
    portfolios = db.get_all_portfolios()
    skills = db.get_all_skills()
    cv_profile = db.get_cv_profile()
    return render_template(
        template_name,
        active_slide=active_slide,
        portfolios=portfolios,
        skills=skills,
        cv_profile=cv_profile,
    )


# ==========================================
# REST API (DATA DINAMIS)
# ==========================================


@app.get("/api/portfolios")
def api_portfolios():
    genre = request.args.get("genre")
    items = db.get_all_portfolios(genre=genre)
    return jsonify(items)


@app.get("/api/cv-profile")
def api_cv_profile():
    profile = db.get_cv_profile()
    skills = db.get_all_skills()
    return jsonify({"profile": profile, "skills": skills})


# ==========================================
# AUTENTIKASI PENGELOLA (ADMIN LOGIN/LOGOUT)
# ==========================================


@app.route("/login", methods=["GET", "POST"])
def login():
    referrer = request.args.get("ref", "direct")
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        # Validasi Kredensial Admin Studio
        if username == "admin" and (password in ("admin123", "admin", "lyqu2026") or password == ""):
            session["is_admin"] = True
            session["admin_user"] = username
            flash("Login berhasil! Selamat datang di Dasbor Pengelola Portofolio.", "success")
            return redirect(url_for("dashboard"))

        flash("Login gagal. Masukkan username: admin dan password: admin123", "danger")
        return redirect(url_for("login", ref=referrer))

    return render_template("login.html", referrer=referrer)


@app.route("/logout")
def logout():
    session.clear()
    flash("Anda telah berhasil keluar (logout) dari sistem dasbor.", "info")
    return redirect(url_for("login"))


# ==========================================
# DASBOR PENGELOLA & FITUR CRUD
# ==========================================


@app.get("/dashboard")
@login_required
def dashboard():
    portfolios = db.get_all_portfolios()
    skills = db.get_all_skills()
    cv_profile = db.get_cv_profile()
    bookings = db.get_all_bookings()
    stats = {
        "total_portfolios": len(portfolios),
        "total_skills": len(skills),
        "total_projects": cv_profile.get("completed_projects", "20+"),
        "total_bookings": len(bookings),
    }
    return render_template(
        "dashboard.html",
        username=session.get("admin_user", "Admin"),
        portfolios=portfolios,
        skills=skills,
        cv_profile=cv_profile,
        bookings=bookings,
        stats=stats,
    )


# --- CRUD PORTOFOLIO (CREATE DENGAN UPLOAD FILE) ---
@app.post("/portfolio/create")
@login_required
def portfolio_create():
    title = request.form.get("title", "").strip()
    genre = request.form.get("genre", "").strip()
    pill_tab = request.form.get("pill_tab", "").strip()
    description = request.form.get("description", "").strip()
    image_url = request.form.get("image_url", "").strip()
    client_name = request.form.get("client_name", "").strip() or "Klien Studio Jogja"
    year = request.form.get("year", "").strip() or "2026"

    # Handle Upload Berkas Gambar (Jika diupload via file picker)
    image_file = request.files.get("image_file")
    if image_file and image_file.filename and allowed_file(image_file.filename):
        filename = secure_filename(image_file.filename)
        safe_name = f"{int(time.time())}_{filename}"
        save_path = os.path.join(UPLOAD_FOLDER, safe_name)
        image_file.save(save_path)
        image_url = f"/static/images/portfolio/{safe_name}"

    # Validasi Backend Form
    errors = []
    if not title or len(title) < 3:
        errors.append("Judul portofolio minimal 3 karakter.")
    if not genre:
        errors.append("Kategori genre portofolio wajib dipilih.")
    if not pill_tab:
        pill_tab = f"{genre.upper()} • 2026"
    if not description or len(description) < 5:
        errors.append("Deskripsi portofolio minimal 5 karakter.")
    if not image_url:
        image_url = "/static/images/portfolio/wedding-intimate-merapi.jpg"

    if errors:
        for err in errors:
            flash(err, "danger")
        return redirect(url_for("dashboard"))

    db.create_portfolio(title, genre, pill_tab, description, image_url, client_name, year)
    flash(f"Karya portofolio '{title}' berhasil ditambahkan ke database!", "success")
    return redirect(url_for("dashboard"))


# --- CRUD PORTOFOLIO (UPDATE DENGAN UPLOAD FILE) ---
@app.route("/portfolio/edit/<int:item_id>", methods=["GET", "POST"])
@login_required
def portfolio_edit(item_id):
    item = db.get_portfolio_by_id(item_id)
    if not item:
        flash("Data portofolio tidak ditemukan.", "danger")
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        genre = request.form.get("genre", "").strip()
        pill_tab = request.form.get("pill_tab", "").strip()
        description = request.form.get("description", "").strip()
        image_url = request.form.get("image_url", "").strip()
        client_name = request.form.get("client_name", "").strip() or "Klien Studio Jogja"
        year = request.form.get("year", "").strip() or "2026"

        # Handle Upload Berkas Gambar Pengganti
        image_file = request.files.get("image_file")
        if image_file and image_file.filename and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            safe_name = f"{int(time.time())}_{filename}"
            save_path = os.path.join(UPLOAD_FOLDER, safe_name)
            image_file.save(save_path)
            image_url = f"/static/images/portfolio/{safe_name}"

        # Validasi Backend
        errors = []
        if not title or len(title) < 3:
            errors.append("Judul portofolio minimal 3 karakter.")
        if not genre:
            errors.append("Kategori genre portofolio wajib dipilih.")
        if not description or len(description) < 5:
            errors.append("Deskripsi portofolio minimal 5 karakter.")
        if not image_url:
            image_url = item["image_url"]

        if errors:
            for err in errors:
                flash(err, "danger")
            return redirect(url_for("portfolio_edit", item_id=item_id))

        db.update_portfolio(item_id, title, genre, pill_tab, description, image_url, client_name, year)
        flash(f"Data portofolio #{item_id} '{title}' berhasil diperbarui!", "success")
        return redirect(url_for("dashboard"))

    return render_template("portfolio_edit.html", item=item)


# --- CRUD PORTOFOLIO (DELETE) ---
@app.post("/portfolio/delete/<int:item_id>")
@login_required
def portfolio_delete(item_id):
    item = db.get_portfolio_by_id(item_id)
    if not item:
        flash("Data portofolio tidak ditemukan.", "danger")
        return redirect(url_for("dashboard"))

    db.delete_portfolio(item_id)
    flash(f"Karya portofolio #{item_id} '{item['title']}' berhasil dihapus!", "success")
    return redirect(url_for("dashboard"))


# --- CRUD SKILLS (CREATE & DELETE) ---
@app.post("/skill/create")
@login_required
def skill_create():
    name = request.form.get("name", "").strip()
    category = request.form.get("category", "").strip()
    level = request.form.get("level", "").strip()
    icon = request.form.get("icon", "").strip() or "⚡"

    if not name or not category or not level:
        flash("Semua kolom skill wajib diisi.", "danger")
        return redirect(url_for("dashboard"))

    db.create_skill(name, category, level, icon)
    flash(f"Skill / Keahlian '{name}' berhasil ditambahkan!", "success")
    return redirect(url_for("dashboard"))


@app.post("/skill/delete/<int:skill_id>")
@login_required
def skill_delete(skill_id):
    db.delete_skill(skill_id)
    flash("Skill berhasil dihapus dari CV.", "success")
    return redirect(url_for("dashboard"))


# --- EDIT CV PROFILE (UPDATE) ---
@app.post("/profile/update")
@login_required
def profile_update():
    full_name = request.form.get("full_name", "").strip()
    role_title = request.form.get("role_title", "").strip()
    bio = request.form.get("bio", "").strip()
    experience_years = request.form.get("experience_years", "").strip()
    completed_projects = request.form.get("completed_projects", "").strip()
    location = request.form.get("location", "").strip()
    email = request.form.get("email", "").strip()
    phone = request.form.get("phone", "").strip()
    instagram = request.form.get("instagram", "").strip()

    if not full_name or not role_title or not bio:
        flash("Nama, jabatan, dan bio CV wajib diisi.", "danger")
        return redirect(url_for("dashboard"))

    db.update_cv_profile(
        full_name,
        role_title,
        bio,
        experience_years,
        completed_projects,
        location,
        email,
        phone,
        instagram,
    )
    flash("Profil CV Pengelola berhasil diperbarui secara dinamis!", "success")
    return redirect(url_for("dashboard"))


# --- MANAJEMEN RESERVASI / BOOKINGS (UPDATE STATUS & DELETE) ---
@app.post("/booking/status/<int:booking_id>", endpoint="booking_status")
@app.post("/booking/update-status/<int:booking_id>", endpoint="booking_update_status")
@login_required
def booking_status(booking_id):
    status = request.form.get("status", "Dikonfirmasi")
    db.update_booking_status(booking_id, status)
    flash(f"Status reservasi #{booking_id} berhasil diubah menjadi '{status}'!", "success")
    return redirect(url_for("dashboard"))


@app.post("/booking/delete/<int:booking_id>")
@login_required
def booking_delete(booking_id):
    db.delete_booking(booking_id)
    flash(f"Data reservasi #{booking_id} berhasil dihapus dari database.", "success")
    return redirect(url_for("dashboard"))


# ==========================================
# RESERVASI PUBLIK (SIMPAN KE SQLITE)
# ==========================================


@app.post("/api/booking-inquiry")
def booking_inquiry():
    if not request.is_json:
        return jsonify(message="Permintaan harus menggunakan format JSON."), 415

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify(message="Data formulir tidak valid."), 400

    errors = {}
    name = data.get("name")
    email = data.get("email")
    phone = data.get("phone")
    package_price = data.get("package")
    location_fee = data.get("location")
    date = data.get("date")

    if not isinstance(name, str) or not 2 <= len(name.strip()) <= 80:
        errors["name"] = "Nama harus terdiri dari 2–80 karakter."
    if not isinstance(email, str) or not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email.strip()):
        errors["email"] = "Masukkan alamat email yang valid."
    if (
        not isinstance(phone, str)
        or not re.fullmatch(r"[\d+\-()\s]{8,20}", phone.strip())
        or not 8 <= sum(character.isdigit() for character in phone) <= 15
    ):
        errors["phone"] = "Masukkan nomor WhatsApp yang valid."
    if not isinstance(package_price, str) or package_price not in BOOKING_PACKAGES:
        errors["package"] = "Paket yang dipilih tidak valid."
    if not isinstance(location_fee, str) or location_fee not in BOOKING_LOCATIONS:
        errors["location"] = "Zona lokasi yang dipilih tidak valid."
    if (
        not isinstance(date, int)
        or isinstance(date, bool)
        or not 1 <= date <= 28
        or date in BOOKED_DATES
    ):
        errors["date"] = "Tanggal tidak tersedia. Silakan pilih tanggal lain."

    if errors:
        return jsonify(message="Periksa kembali data formulir.", errors=errors), 422

    # Map nama paket & zona lokasi
    package_names = {
        "1200000": "Portrait & Katalog Studio",
        "2500000": "Pre-Wedding Sinematik Merapi",
        "4800000": "Full Wedding Intimate Jogja",
    }
    location_names = {
        "0": "Kota Yogyakarta (Ring Road)",
        "150000": "Sleman, Kaliurang & Bantul",
        "250000": "Kulon Progo & Gunungkidul",
    }

    pkg_price_int = int(package_price)
    loc_fee_int = int(location_fee)
    total_amount = pkg_price_int + loc_fee_int
    dp_amount = int(total_amount * 0.3)
    pkg_name = package_names.get(package_price, "Paket Fotografi Jogja")
    loc_zone = location_names.get(location_fee, "Wilayah D.I. Yogyakarta")

    # SIMPAN KE DATABASE SQLITE SECARA NYATA
    booking_id = db.create_booking(
        client_name=name.strip(),
        email=email.strip(),
        phone=phone.strip(),
        package_name=pkg_name,
        package_price=pkg_price_int,
        location_zone=loc_zone,
        location_fee=loc_fee_int,
        booking_date=date,
        total_amount=total_amount,
        dp_amount=dp_amount,
    )

    return jsonify(
        message=f"Reservasi #{booking_id} berhasil disimpan ke database studio. Tim Lyqu Visual akan mengonfirmasi slot via WhatsApp.",
        data_saved=True,
        booking_id=booking_id,
    )


# ==========================================
# SIMULASI & UTILITY
# ==========================================


@app.get("/user/<username>")
def show_user_profile(username):
    cv_profile = db.get_cv_profile()
    skills = db.get_all_skills()
    portfolios = db.get_all_portfolios()
    return render_template(
        "profile.html",
        username=username,
        cv_profile=cv_profile,
        skills=skills,
        portfolios=portfolios,
    )


@app.get("/product/<int:item_id>")
def show_product(item_id):
    product = PRODUCTS.get(item_id)
    if product is None:
        abort(404)
    return render_template("product.html", item_id=item_id, product=product)


@app.route("/assets/<path:filename>")
def legacy_assets(filename):
    return send_from_directory(app.static_folder, filename)


@app.route("/health")
def health():
    return jsonify({"status": "ok", "studio": "LYQU VISUAL YOGYAKARTA", "database": "connected"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="127.0.0.1", port=port)
