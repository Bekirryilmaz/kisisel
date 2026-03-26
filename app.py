import os
import json
import logging
from datetime import datetime
from functools import wraps
from flask import (
    Flask, render_template, request, flash, redirect, url_for, session, abort
)
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

_secret_key = os.environ.get("SECRET_KEY")
if not _secret_key:
    import secrets
    _secret_key = secrets.token_hex(32)
app.secret_key = _secret_key

# Database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "sqlite:///" + os.path.join(basedir, "portfolio.db")
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Mail
app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
app.config["MAIL_PORT"] = int(os.environ.get("MAIL_PORT", 587))
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME", "captain.cook.023@gmail.com")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD", "")
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_USERNAME", "captain.cook.023@gmail.com")
mail = Mail(app)

# File uploads
UPLOAD_FOLDER = os.path.join(basedir, "static", "uploads")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Admin credentials
ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "superadmin")
_raw_admin_password = os.environ.get("ADMIN_PASSWORD", "Admin@2026!")
if not os.environ.get("ADMIN_PASSWORD"):
    logging.warning("ADMIN_PASSWORD env var not set; using default password. Set it in production.")
if not os.environ.get("MAIL_PASSWORD"):
    logging.warning("MAIL_PASSWORD env var not set; contact form emails will not be sent.")
ADMIN_PASSWORD_HASH = generate_password_hash(_raw_admin_password)

CONTACT_INFO = {
    "whatsapp": "905414312769",
    "whatsapp_display": "+90 541 431 27 69",
    "phone": "05414312769",
    "email": "captain.cook.023@gmail.com",
    "location": "Samsun, Türkiye",
}


# ── Models ──────────────────────────────────────────────────────────────────

class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    short_desc = db.Column(db.String(300), nullable=False)
    description = db.Column(db.Text, nullable=False)
    url = db.Column(db.String(300), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    tags_json = db.Column(db.Text, default="[]")
    color_from = db.Column(db.String(20), default="#1a1a2e")
    color_to = db.Column(db.String(20), default="#e94560")
    client = db.Column(db.String(200))
    year = db.Column(db.String(10))
    duration = db.Column(db.String(50))
    client_needs = db.Column(db.Text)
    solution = db.Column(db.Text)
    design_approach = db.Column(db.Text)
    features_json = db.Column(db.Text, default="[]")
    technologies_json = db.Column(db.Text, default="[]")
    results_json = db.Column(db.Text, default="[]")
    screenshot_url = db.Column(db.String(500))
    screenshot_file = db.Column(db.String(300))
    order = db.Column(db.Integer, default=0)

    @property
    def tags(self):
        return json.loads(self.tags_json or "[]")

    @tags.setter
    def tags(self, value):
        self.tags_json = json.dumps(value, ensure_ascii=False)

    @property
    def features(self):
        return json.loads(self.features_json or "[]")

    @features.setter
    def features(self, value):
        self.features_json = json.dumps(value, ensure_ascii=False)

    @property
    def technologies(self):
        return json.loads(self.technologies_json or "[]")

    @technologies.setter
    def technologies(self, value):
        self.technologies_json = json.dumps(value, ensure_ascii=False)

    @property
    def results(self):
        return json.loads(self.results_json or "[]")

    @results.setter
    def results(self, value):
        self.results_json = json.dumps(value, ensure_ascii=False)

    @property
    def screenshot(self):
        if self.screenshot_file:
            return url_for("static", filename="uploads/" + self.screenshot_file)
        return self.screenshot_url

    def to_dict(self):
        return {
            "slug": self.slug,
            "name": self.name,
            "short_desc": self.short_desc,
            "description": self.description,
            "url": self.url,
            "category": self.category,
            "tags": self.tags,
            "color_from": self.color_from,
            "color_to": self.color_to,
            "client": self.client,
            "year": self.year,
            "duration": self.duration,
            "client_needs": self.client_needs,
            "solution": self.solution,
            "design_approach": self.design_approach,
            "features": self.features,
            "technologies": self.technologies,
            "results": self.results,
            "screenshot": self.screenshot,
        }


SEED_PROJECTS = [
    {
        "slug": "hayder-insaat",
        "name": "Hayder İnşaat",
        "short_desc": "İnşaat sektöründe güçlü kurumsal kimlik ve dijital varlık",
        "description": "Hayder İnşaat için modern, kurumsal bir web sitesi tasarlanarak şirketin dijital varlığı güçlendirildi.",
        "url": "https://hayderinsaat.com/",
        "category": "Kurumsal Web Sitesi",
        "tags": ["HTML5", "CSS3", "JavaScript", "Flask", "SEO"],
        "color_from": "#1a1a2e",
        "color_to": "#e94560",
        "client": "Hayder İnşaat A.Ş.",
        "year": "2026",
        "duration": "1 Hafta",
        "client_needs": "Müşteri, inşaat sektöründe güvenilir ve profesyonel bir imaj oluşturmak, tamamlanan projelerini sergilemek ve potansiyel müşterilere ulaşmak istiyordu.",
        "solution": "Kurumsal kimliği yansıtan, güçlü görseller ve etkileyici proje galerisi içeren bir web sitesi tasarlandı. SEO optimizasyonu ile arama motorlarında görünürlük artırıldı.",
        "design_approach": "İnşaat sektörünün güçlü ve sağlam imajını yansıtmak için koyu tonlar ve altın renkler tercih edildi.",
        "features": [
            "Duyarlı (Responsive) Mobil Tasarım",
            "Proje Galerisi ve Filtreleme",
            "WhatsApp Entegrasyonu",
            "Google Maps Entegrasyonu",
            "SEO Optimizasyonu",
            "İletişim Formu",
        ],
        "technologies": ["Python", "Flask", "HTML5", "CSS3", "JavaScript", "SQLite"],
        "results": [
            "Profesyonel kurumsal dijital varlık oluşturuldu",
            "Mobil uyumlu, hızlı yüklenen site",
            "İletişim formu ile müşteri talebi alımı",
        ],
        "order": 1,
    },
    {
        "slug": "ayildiz-nakliyat",
        "name": "Ay Yıldız Nakliyat",
        "short_desc": "Nakliyat firması için dijital dönüşüm ve online teklif sistemi",
        "description": "Ay Yıldız Nakliyat için online teklif sistemi ve kurumsal web sitesi geliştirilerek müşteri kazanımı dijitalleştirildi.",
        "url": "https://ayildiznakliyat.com/",
        "category": "Kurumsal Web Sitesi",
        "tags": ["Flask", "Python", "JavaScript", "CSS3", "SEO"],
        "color_from": "#0f3460",
        "color_to": "#f4a261",
        "client": "Ay Yıldız Nakliyat Ltd. Şti.",
        "year": "2025",
        "duration": "1 Hafta",
        "client_needs": "Nakliyat firması, telefon trafiğini azaltmak, online teklif alabilmek ve hizmetlerini daha geniş kitlelere ulaştırmak istiyordu.",
        "solution": "Ziyaretçilerin kolayca nakliyat teklifi talep edebildiği, hizmet bölgelerinin gösterildiği ve müşteri yorumlarının ön plana çıktığı bir web sitesi geliştirildi.",
        "design_approach": "Güven ve profesyonelliği ön plana çıkaran temiz bir tasarım benimsendi. Mavi tonlar ve turuncu aksanlar hem kurumsal hem de dinamik bir görünüm sağladı.",
        "features": [
            "Online Teklif Talep Formu",
            "Müşteri Yorumları Bölümü",
            "WhatsApp Anlık İletişim",
            "Mobil Öncelikli Tasarım",
            "SEO & Yerel Arama Optimizasyonu",
        ],
        "technologies": ["Python", "Flask", "HTML5", "CSS3", "JavaScript", "SQLite"],
        "results": [
            "Online teklif talepleriyle müşteri erişimi artırıldı",
            "Mobil uyumlu, hızlı yüklenen site",
            "SEO optimizasyonuyla yerel arama görünürlüğü kazanıldı",
        ],
        "order": 2,
    },
]


def seed_db():
    """Seed the database with initial projects if empty."""
    if Project.query.count() == 0:
        for data in SEED_PROJECTS:
            p = Project(
                slug=data["slug"],
                name=data["name"],
                short_desc=data["short_desc"],
                description=data["description"],
                url=data["url"],
                category=data["category"],
                color_from=data["color_from"],
                color_to=data["color_to"],
                client=data.get("client"),
                year=data.get("year"),
                duration=data.get("duration"),
                client_needs=data.get("client_needs"),
                solution=data.get("solution"),
                design_approach=data.get("design_approach"),
                order=data.get("order", 0),
            )
            p.tags = data.get("tags", [])
            p.features = data.get("features", [])
            p.technologies = data.get("technologies", [])
            p.results = data.get("results", [])
            db.session.add(p)
        db.session.commit()


# ── Helpers ──────────────────────────────────────────────────────────────────

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("admin_logged_in"):
            return redirect(url_for("admin_login"))
        return f(*args, **kwargs)
    return decorated


@app.context_processor
def inject_contact():
    return {"contact": CONTACT_INFO}


# ── Public Routes ─────────────────────────────────────────────────────────────

@app.route("/")
def index():
    projects = Project.query.order_by(Project.order).limit(2).all()
    return render_template("index.html", projects=[p.to_dict() for p in projects])


@app.route("/portfolio")
def portfolio():
    projects = Project.query.order_by(Project.order).all()
    return render_template("portfolio.html", projects=[p.to_dict() for p in projects])


@app.route("/portfolio/<slug>")
def project_detail(slug):
    project = Project.query.filter_by(slug=slug).first()
    if not project:
        return render_template("404.html"), 404
    return render_template("project_detail.html", project=project.to_dict())


@app.route("/hakkimizda")
def about():
    return render_template("about.html")


@app.route("/iletisim", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("isim", "").strip()
        email = request.form.get("eposta", "").strip()
        message = request.form.get("mesaj", "").strip()

        if not name or not email or not message:
            flash("Lütfen tüm alanları doldurun.", "error")
        elif "@" not in email or "." not in email:
            flash("Geçerli bir e-posta adresi girin.", "error")
        else:
            # Send email
            try:
                msg = Message(
                    subject=f"Yeni İletişim Mesajı: {name}",
                    recipients=["captain.cook.023@gmail.com"],
                    body=(
                        f"Gönderen: {name}\n"
                        f"E-Posta: {email}\n"
                        f"Tarih: {datetime.now().strftime('%d.%m.%Y %H:%M')}\n\n"
                        f"Mesaj:\n{message}"
                    ),
                    reply_to=email,
                )
                mail.send(msg)
            except Exception:
                logging.exception("Mail sending failed")
                pass  # Mail gönderimi başarısız olsa bile kullanıcıya başarı mesajı göster

            flash(
                f"Teşekkürler {name}! Mesajınız alındı, en kısa sürede size dönüş yapacağım.",
                "success",
            )
            return redirect(url_for("contact"))

    return render_template("contact.html")


# ── Admin Routes ──────────────────────────────────────────────────────────────

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if session.get("admin_logged_in"):
        return redirect(url_for("admin_dashboard"))
    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        if username == ADMIN_USERNAME and check_password_hash(ADMIN_PASSWORD_HASH, password):
            session["admin_logged_in"] = True
            session["admin_username"] = username
            return redirect(url_for("admin_dashboard"))
        error = "Kullanıcı adı veya şifre hatalı."
    return render_template("admin/login.html", error=error)


@app.route("/admin/logout")
def admin_logout():
    session.clear()
    return redirect(url_for("admin_login"))


@app.route("/admin")
@app.route("/admin/dashboard")
@login_required
def admin_dashboard():
    projects = Project.query.order_by(Project.order).all()
    return render_template("admin/dashboard.html", projects=projects)


@app.route("/admin/projects/new", methods=["GET", "POST"])
@login_required
def admin_project_new():
    if request.method == "POST":
        project = Project()
        _save_project_from_form(project, request)
        db.session.add(project)
        db.session.commit()
        flash("Proje başarıyla eklendi.", "success")
        return redirect(url_for("admin_dashboard"))
    return render_template("admin/project_form.html", project=None, action="new")


@app.route("/admin/projects/<int:pid>/edit", methods=["GET", "POST"])
@login_required
def admin_project_edit(pid):
    project = Project.query.get_or_404(pid)
    if request.method == "POST":
        _save_project_from_form(project, request)
        db.session.commit()
        flash("Proje başarıyla güncellendi.", "success")
        return redirect(url_for("admin_dashboard"))
    return render_template("admin/project_form.html", project=project, action="edit")


@app.route("/admin/projects/<int:pid>/delete", methods=["POST"])
@login_required
def admin_project_delete(pid):
    project = Project.query.get_or_404(pid)
    # Delete uploaded file if exists
    if project.screenshot_file:
        try:
            os.remove(os.path.join(app.config["UPLOAD_FOLDER"], project.screenshot_file))
        except OSError:
            pass
    db.session.delete(project)
    db.session.commit()
    flash("Proje silindi.", "success")
    return redirect(url_for("admin_dashboard"))


def _save_project_from_form(project, req):
    project.slug = req.form.get("slug", "").strip()
    project.name = req.form.get("name", "").strip()
    project.short_desc = req.form.get("short_desc", "").strip()
    project.description = req.form.get("description", "").strip()
    project.url = req.form.get("url", "").strip()
    project.category = req.form.get("category", "").strip()
    project.color_from = req.form.get("color_from", "#1a1a2e").strip()
    project.color_to = req.form.get("color_to", "#e94560").strip()
    project.client = req.form.get("client", "").strip()
    project.year = req.form.get("year", "").strip()
    project.duration = req.form.get("duration", "").strip()
    project.client_needs = req.form.get("client_needs", "").strip()
    project.solution = req.form.get("solution", "").strip()
    project.design_approach = req.form.get("design_approach", "").strip()
    project.order = int(req.form.get("order", 0) or 0)

    # JSON list fields (one item per line)
    project.tags = [t.strip() for t in req.form.get("tags", "").splitlines() if t.strip()]
    project.features = [f.strip() for f in req.form.get("features", "").splitlines() if f.strip()]
    project.technologies = [t.strip() for t in req.form.get("technologies", "").splitlines() if t.strip()]
    project.results = [r.strip() for r in req.form.get("results", "").splitlines() if r.strip()]

    # Screenshot URL
    screenshot_url = req.form.get("screenshot_url", "").strip()
    if screenshot_url:
        project.screenshot_url = screenshot_url

    # Screenshot file upload
    file = req.files.get("screenshot_file")
    if file and file.filename and allowed_file(file.filename):
        # Remove old file
        if project.screenshot_file:
            try:
                os.remove(os.path.join(app.config["UPLOAD_FOLDER"], project.screenshot_file))
            except OSError:
                pass
        filename = secure_filename(file.filename)
        # Make unique
        unique_filename = f"{project.slug}_{filename}"
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], unique_filename))
        project.screenshot_file = unique_filename
        project.screenshot_url = None  # prefer file over URL


# ── Init ──────────────────────────────────────────────────────────────────────

with app.app_context():
    db.create_all()
    seed_db()


if __name__ == "__main__":
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(debug=debug)
