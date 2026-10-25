import os
from flask import Flask, render_template, send_from_directory, jsonify

app = Flask(__name__, static_folder="static", template_folder="templates")
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0


@app.after_request
def add_no_cache_headers(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


@app.route("/")
@app.route("/beranda")
@app.route("/index.html")
def beranda():
    return render_template(
        "index.html",
        active_slide=0,
        page_title="LYQU VISUAL — Studio Fotografi & Visual Kreatif Yogyakarta",
    )


@app.route("/portofolio")
@app.route("/portofolio.html")
@app.route("/showcase.html")
def portofolio():
    return render_template(
        "index.html",
        active_slide=1,
        page_title="Koleksi Karya & Portofolio — LYQU VISUAL Yogyakarta",
    )


@app.route("/tentang-gear")
@app.route("/tentang-gear.html")
@app.route("/mind-gear.html")
def tentang_gear():
    return render_template(
        "index.html",
        active_slide=2,
        page_title="Filosofi Kreatif, Tim & Gear Kamera — LYQU VISUAL Yogyakarta",
    )


@app.route("/paket-booking")
@app.route("/paket-booking.html")
@app.route("/rates-booking.html")
def paket_booking():
    return render_template(
        "index.html",
        active_slide=3,
        page_title="Paket Harga, Kalender Jadwal & Booking DP — LYQU VISUAL Yogyakarta",
    )


@app.route("/portal-proofing")
@app.route("/portal-proofing.html")
@app.route("/client-portal.html")
def portal_proofing():
    return render_template(
        "index.html",
        active_slide=4,
        page_title="Portal Klien: Proofing RAW & Google Drive — LYQU VISUAL Yogyakarta",
    )


@app.route("/faq-kontak")
@app.route("/faq-kontak.html")
@app.route("/faq-connect.html")
def faq_kontak():
    return render_template(
        "index.html",
        active_slide=5,
        page_title="FAQ Operasional, Kebijakan Studio & Kontak — LYQU VISUAL Yogyakarta",
    )


@app.route("/assets/<path:filename>")
def legacy_assets(filename):
    return send_from_directory(app.static_folder, filename)


@app.route("/health")
def health():
    return jsonify({"status": "ok", "studio": "LYQU VISUAL YOGYAKARTA"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="127.0.0.1", port=port)
