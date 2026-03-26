# Bekir Yılmaz — Kişisel Portfolio Web Sitesi

Freelance web geliştirici Bekir Yılmaz için geliştirilmiş kişisel portföy ve servis tanıtım sitesi.

## 🚀 Özellikler

- Modern, mobil öncelikli tasarım
- Flask tabanlı Python backend
- SEO meta etiketleri (og, twitter card)
- İletişim formu (flash mesajları ile)
- Proje detay sayfaları
- Scroll animasyonları
- WhatsApp entegrasyonu
- Hamburger menü

## 🛠 Teknoloji Yığını

- **Backend:** Python 3, Flask
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
- **Font:** Inter (Google Fonts)
- **İkonlar:** Font Awesome 6

## 📦 Kurulum

```bash
# Bağımlılıkları yükle
pip install -r requirements.txt

# Uygulamayı başlat
python app.py
```

Tarayıcıda `http://localhost:5000` adresini açın.

## 📁 Proje Yapısı

```
kisisel/
├── app.py                  # Flask uygulaması ve route'lar
├── requirements.txt
├── templates/
│   ├── base.html           # Ana şablon (navbar, footer)
│   ├── index.html          # Ana sayfa
│   ├── portfolio.html      # Portföy listesi
│   ├── project_detail.html # Proje detay sayfası
│   ├── about.html          # Hakkımda
│   ├── contact.html        # İletişim formu
│   └── 404.html
└── static/
    ├── css/style.css
    ├── js/main.js
    └── images/favicon.svg
```

## 🔗 Sayfalar

| URL | Sayfa |
|-----|-------|
| `/` | Ana Sayfa |
| `/portfolio` | Portföy |
| `/portfolio/hayder-insaat` | Hayder İnşaat Projesi |
| `/portfolio/ayildiz-nakliyat` | Ayıldız Nakliyat Projesi |
| `/hakkimizda` | Hakkımda |
| `/iletisim` | İletişim |
