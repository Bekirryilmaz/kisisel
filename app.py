from flask import Flask, render_template, request, flash, redirect, url_for

app = Flask(__name__)
app.secret_key = "bekir-yilmaz-web-dev-2024"

PROJECTS = {
    "hayder-insaat": {
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
        "year": "2024",
        "duration": "3 Hafta",
        "client_needs": "Müşteri, inşaat sektöründe güvenilir ve profesyonel bir imaj oluşturmak, tamamlanan projelerini sergilemek ve potansiyel müşterilere ulaşmak istiyordu. Mevcut dijital varlıkları yoktu ve sektörde öne çıkmak için modern bir web sitesine ihtiyaç duydular.",
        "solution": "Kurumsal kimliği yansıtan, güçlü görseller ve etkileyici proje galerisi içeren bir web sitesi tasarlandı. SEO optimizasyonu ile arama motorlarında görünürlük artırıldı. Mobil uyumlu tasarım sayesinde her cihazdan erişilebilir hale getirildi.",
        "design_approach": "İnşaat sektörünün güçlü ve sağlam imajını yansıtmak için koyu tonlar ve altın renkler tercih edildi. Net tipografi ve geniş beyaz alanlar profesyonel bir görünüm sağladı. Animasyonlu proje kartları ziyaretçilerin dikkatini projelere çekiyor.",
        "features": [
            "Duyarlı (Responsive) Mobil Tasarım",
            "Proje Galerisi ve Filtreleme",
            "WhatsApp Entegrasyonu",
            "Google Maps Entegrasyonu",
            "Hızlı Yükleme (90+ PageSpeed Skoru)",
            "SEO Optimizasyonu",
            "İletişim Formu",
            "Admin Paneli (Proje Yönetimi)",
        ],
        "technologies": ["Python", "Flask", "HTML5", "CSS3", "JavaScript", "SQLite", "Bootstrap"],
        "results": [
            "Organik arama trafiğinde %180 artış",
            "Aylık 500+ benzersiz ziyaretçi",
            "İletişim formu ile aylık 20+ yeni müşteri adayı",
            "Mobil kullanıcı oranı %65",
        ],
    },
    "ayildiz-nakliyat": {
        "slug": "ayildiz-nakliyat",
        "name": "Ayıldız Nakliyat",
        "short_desc": "Nakliyat firması için dijital dönüşüm ve online teklif sistemi",
        "description": "Ayıldız Nakliyat için online teklif sistemi ve kurumsal web sitesi geliştirilerek müşteri kazanımı dijitalleştirildi.",
        "url": "https://ayildiznakliyat.com/",
        "category": "Kurumsal Web Sitesi",
        "tags": ["Flask", "Python", "JavaScript", "CSS3", "SEO"],
        "color_from": "#0f3460",
        "color_to": "#f4a261",
        "client": "Ayıldız Nakliyat Ltd. Şti.",
        "year": "2024",
        "duration": "2 Hafta",
        "client_needs": "Nakliyat firması, telefon trafiğini azaltmak, online teklif alabilmek ve hizmetlerini daha geniş kitlelere ulaştırmak istiyordu. Rakiplerine karşı dijital avantaj elde etmek temel hedeflerinden biriydi.",
        "solution": "Ziyaretçilerin kolayca nakliyat teklifi talep edebildiği, hizmet bölgelerinin harita üzerinde gösterildiği ve müşteri yorumlarının ön plana çıktığı dinamik bir web sitesi geliştirildi. Anlık fiyat hesaplama modülü ile kullanıcı deneyimi üst seviyeye taşındı.",
        "design_approach": "Güven ve profesyonelliği ön plana çıkaran temiz bir tasarım benimsendi. Mavi tonlar ve turuncu aksanlar hem kurumsal hem de dinamik bir görünüm sağladı. Net CTA butonları ve iletişim bilgilerinin öne çıkarılması dönüşüm oranını artırdı.",
        "features": [
            "Online Teklif Talep Formu",
            "Hizmet Bölgeleri Haritası",
            "Müşteri Yorumları Bölümü",
            "WhatsApp Anlık İletişim",
            "Fiyat Hesaplama Modülü",
            "Mobil Öncelikli Tasarım",
            "SEO & Yerel Arama Optimizasyonu",
            "Hızlı Yükleme Optimizasyonu",
        ],
        "technologies": ["Python", "Flask", "HTML5", "CSS3", "JavaScript", "SQLite"],
        "results": [
            "Online teklif talepleri ile telefon yükü %60 azaldı",
            "Google'da yerel arama sonuçlarında ilk 3'e girdi",
            "Aylık 300+ benzersiz ziyaretçi",
            "Müşteri dönüşüm oranı %12'ye ulaştı",
        ],
    },
}


@app.route("/")
def index():
    featured = list(PROJECTS.values())[:2]
    return render_template("index.html", projects=featured)


@app.route("/portfolio")
def portfolio():
    return render_template("portfolio.html", projects=PROJECTS.values())


@app.route("/portfolio/<slug>")
def project_detail(slug):
    project = PROJECTS.get(slug)
    if not project:
        return render_template("404.html"), 404
    return render_template("project_detail.html", project=project)


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
            flash(
                f"Teşekkürler {name}! Mesajınız alındı, en kısa sürede size dönüş yapacağım.",
                "success",
            )
            return redirect(url_for("contact"))

    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True)
