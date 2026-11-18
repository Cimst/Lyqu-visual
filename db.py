import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # 1. Tabel Portofolio Karya
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS portfolio_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            genre TEXT NOT NULL,
            pill_tab TEXT NOT NULL,
            tab_style TEXT DEFAULT 'bg-cobalt text-white',
            card_style TEXT DEFAULT 'bg-white text-obsidian border-2 border-obsidian/10 shadow-lg',
            btn_style TEXT DEFAULT 'bg-cobalt text-white hover:bg-obsidian hover:text-acid',
            description TEXT NOT NULL,
            image_url TEXT NOT NULL,
            client_name TEXT DEFAULT 'Klien Studio Jogja',
            year TEXT DEFAULT '2026',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    # 2. Tabel Skills & Gear CV
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            level TEXT NOT NULL,
            icon TEXT DEFAULT '⚡',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    # 3. Tabel Profil CV Pengelola
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS cv_profile (
            id INTEGER PRIMARY KEY,
            full_name TEXT NOT NULL,
            role_title TEXT NOT NULL,
            bio TEXT NOT NULL,
            experience_years TEXT NOT NULL,
            completed_projects TEXT NOT NULL,
            location TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            instagram TEXT NOT NULL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    # 4. Tabel Reservasi & Booking Klien
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            package_name TEXT NOT NULL,
            package_price INTEGER NOT NULL,
            location_zone TEXT NOT NULL,
            location_fee INTEGER NOT NULL,
            booking_date INTEGER NOT NULL,
            total_amount INTEGER NOT NULL,
            dp_amount INTEGER NOT NULL,
            status TEXT DEFAULT 'Menunggu Konfirmasi',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    # Seed data awal jika portfolio masih kosong
    cursor.execute("SELECT COUNT(*) FROM portfolio_items")
    if cursor.fetchone()[0] == 0:
        initial_portfolios = [
            (
                "SAKRAL INTIMATE WEDDING MERAPI",
                "Wedding",
                "FULL DAY • 8 JAM",
                "bg-cobalt text-white",
                "bg-white text-obsidian border-2 border-obsidian/10 shadow-lg",
                "bg-cobalt text-white hover:bg-obsidian hover:text-acid",
                "Dokumentasi sakral candid emosional & tone sinematik hangat di Kaliurang.",
                "/static/images/portfolio/wedding-intimate-merapi.jpg",
                "Bagus & Annisa",
                "2026",
            ),
            (
                "PORTRAIT & EVENT",
                "Event",
                "LIFESTYLE • YOUTH PORTRAIT",
                "bg-obsidian text-acid border border-white/20",
                "bg-acid text-obsidian border-2 border-obsidian/15 shadow-lg",
                "bg-obsidian text-acid hover:bg-white hover:text-obsidian",
                "Lifestyle portrait dan dokumentasi event anak muda dengan gaya natural dan ekspresif.",
                "/static/images/shared/portrait-youth-lifestyle-event.webp",
                "Youth Fest Jogja",
                "2026",
            ),
            (
                "KATALOG KOMERSIAL & UMKM JOGJA",
                "Produk",
                "STUDIO • 2 JAM",
                "bg-acid text-obsidian",
                "bg-cobalt text-white border-2 border-white/10 shadow-lg",
                "bg-acid text-obsidian hover:bg-white",
                "Visual produk tajam berstandar iklan komersial untuk kuliner, fashion & brand lokal.",
                "/static/images/portfolio/product-catalogue-umkm.jpg",
                "Brand Lokal Nusantara",
                "2026",
            ),
            (
                "WISUDA, PORTRAIT & STAGE EVENT",
                "Portrait",
                "EXPRESS • 2 JAM",
                "bg-acid text-obsidian",
                "bg-obsidian text-white border-2 border-white/20 shadow-lg",
                "bg-acid text-obsidian hover:bg-white hover:text-obsidian",
                "Abadikan momen kelulusan kampus atau panggung konser dengan draft cepat H+1.",
                "/static/images/portfolio/graduation-portrait.jpg",
                "Wisudawati UGM/UNY",
                "2026",
            ),
        ]
        cursor.executemany(
            """
            INSERT INTO portfolio_items (title, genre, pill_tab, tab_style, card_style, btn_style, description, image_url, client_name, year)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            initial_portfolios,
        )

    # Seed data skills jika masih kosong
    cursor.execute("SELECT COUNT(*) FROM skills")
    if cursor.fetchone()[0] == 0:
        initial_skills = [
            ("Sony Alpha Ecosystem (A7R V & A7 IV)", "Gear & Kamera", "Expert / 61MP RAW", "📷"),
            ("Signature 16-Bit Color Grading", "Post-Processing", "Master LUT & DaVinci", "🎨"),
            ("Editorial & Intimate Wedding Lighting", "Teknik Pemotretan", "Godox & Profoto Pro", "💡"),
            ("G-Master Prime Lenses (35mm & 85mm f/1.4)", "Optik & Lensa", "Signature Bokeh", "🔍"),
            ("High-Speed RAW Proofing Workflow", "Workflow Studio", "H+1 Delivery SLA", "⚡"),
        ]
        cursor.executemany(
            "INSERT INTO skills (name, category, level, icon) VALUES (?, ?, ?, ?)",
            initial_skills,
        )

    # Seed data profile CV jika masih kosong
    cursor.execute("SELECT COUNT(*) FROM cv_profile")
    if cursor.fetchone()[0] == 0:
        cursor.execute(
            """
            INSERT INTO cv_profile (id, full_name, role_title, bio, experience_years, completed_projects, location, email, phone, instagram)
            VALUES (1, 'Muhammad Zaki Mubarok (MzakiM)', 'Informatics Student | UI/UX Designer | Tech Enthusiast', 
            'A highly motivated Informatics undergraduate specializing in UI/UX design, visual communication, and technology leadership. Passionate about bridging creative design with technical implementation. Seeking opportunities to leverage skills in UI/UX, graphic design, and IoT development to create impactful, user-centric solutions.',
            '7+ Tahun', '20+ Proyek Selesai', 'Sidoarjo & UNU Yogyakarta', 'zakimubatok1@gmail.com', '+62 851-9420-2013', '@jecckyy.yy')
            """
        )

    # Seed data bookings jika masih kosong
    cursor.execute("SELECT COUNT(*) FROM bookings")
    if cursor.fetchone()[0] == 0:
        cursor.execute(
            """
            INSERT INTO bookings (client_name, email, phone, package_name, package_price, location_zone, location_fee, booking_date, total_amount, dp_amount, status)
            VALUES 
            ('Annisa Rahmawati', 'annisa.jogja@gmail.com', '081234567890', 'Pre-Wedding Merapi', 2500000, 'Sleman & Kaliurang', 150000, 24, 2650000, 795000, 'Menunggu Konfirmasi'),
            ('Bagus Pratama', 'bagus.pratama@gmail.com', '085799182736', 'Full Wedding Jogja', 4800000, 'Kota Yogyakarta', 0, 28, 4800000, 1440000, 'Dikonfirmasi')
            """
        )

    conn.commit()
    conn.close()


# ==========================================
# QUERY HELPER FUNCTIONS (CRUD)
# ==========================================


def get_all_portfolios(genre=None):
    conn = get_db()
    cursor = conn.cursor()
    if genre and genre != "all":
        cursor.execute(
            "SELECT * FROM portfolio_items WHERE genre LIKE ? ORDER BY id DESC",
            (f"%{genre}%",),
        )
    else:
        cursor.execute("SELECT * FROM portfolio_items ORDER BY id DESC")
    items = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return items


def get_portfolio_by_id(item_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM portfolio_items WHERE id = ?", (item_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def create_portfolio(title, genre, pill_tab, description, image_url, client_name="Klien Studio", year="2026"):
    genre_clean = genre.capitalize()
    if genre_clean == "Wedding":
        tab_style = "bg-cobalt text-white"
        card_style = "bg-white text-obsidian border-2 border-obsidian/10 shadow-lg"
        btn_style = "bg-cobalt text-white hover:bg-obsidian hover:text-acid"
    elif genre_clean == "Event":
        tab_style = "bg-obsidian text-acid border border-white/20"
        card_style = "bg-acid text-obsidian border-2 border-obsidian/15 shadow-lg"
        btn_style = "bg-obsidian text-acid hover:bg-white hover:text-obsidian"
    elif genre_clean == "Produk":
        tab_style = "bg-acid text-obsidian"
        card_style = "bg-cobalt text-white border-2 border-white/10 shadow-lg"
        btn_style = "bg-acid text-obsidian hover:bg-white"
    else:
        tab_style = "bg-acid text-obsidian"
        card_style = "bg-obsidian text-white border-2 border-white/20 shadow-lg"
        btn_style = "bg-acid text-obsidian hover:bg-white hover:text-obsidian"

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO portfolio_items (title, genre, pill_tab, tab_style, card_style, btn_style, description, image_url, client_name, year)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (title, genre_clean, pill_tab, tab_style, card_style, btn_style, description, image_url, client_name, year),
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id


def update_portfolio(item_id, title, genre, pill_tab, description, image_url, client_name, year):
    genre_clean = genre.capitalize()
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE portfolio_items
        SET title = ?, genre = ?, pill_tab = ?, description = ?, image_url = ?, client_name = ?, year = ?
        WHERE id = ?
        """,
        (title, genre_clean, pill_tab, description, image_url, client_name, year, item_id),
    )
    conn.commit()
    conn.close()


def delete_portfolio(item_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM portfolio_items WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()


# Skills CRUD
def get_all_skills():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM skills ORDER BY id ASC")
    items = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return items


def create_skill(name, category, level, icon="⚡"):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO skills (name, category, level, icon) VALUES (?, ?, ?, ?)",
        (name, category, level, icon),
    )
    conn.commit()
    conn.close()


def delete_skill(skill_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM skills WHERE id = ?", (skill_id,))
    conn.commit()
    conn.close()


# Profile Info
def get_cv_profile():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cv_profile WHERE id = 1")
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def update_cv_profile(full_name, role_title, bio, experience_years, completed_projects, location, email, phone, instagram):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE cv_profile
        SET full_name = ?, role_title = ?, bio = ?, experience_years = ?, completed_projects = ?,
            location = ?, email = ?, phone = ?, instagram = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = 1
        """,
        (full_name, role_title, bio, experience_years, completed_projects, location, email, phone, instagram),
    )
    conn.commit()
    conn.close()


# Bookings CRUD
def get_all_bookings():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bookings ORDER BY id DESC")
    items = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return items


def create_booking(client_name, email, phone, package_name, package_price, location_zone, location_fee, booking_date, total_amount, dp_amount):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO bookings (client_name, email, phone, package_name, package_price, location_zone, location_fee, booking_date, total_amount, dp_amount)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (client_name, email, phone, package_name, package_price, location_zone, location_fee, booking_date, total_amount, dp_amount),
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id


def update_booking_status(booking_id, status):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE bookings SET status = ? WHERE id = ?", (status, booking_id))
    conn.commit()
    conn.close()


def delete_booking(booking_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM bookings WHERE id = ?", (booking_id,))
    conn.commit()
    conn.close()
