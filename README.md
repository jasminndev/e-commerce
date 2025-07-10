# 🛒 100k – E-Commerce Web Platform

## 🇺🇿 O‘zbekcha

**100k** — bu Django asosida qurilgan zamonaviy e-commerce web platformasi bo‘lib, foydalanuvchilarga onlayn tarzda
mahsulotlarni ko‘rish, xarid qilish va boshqarish imkonini beradi. Ushbu loyiha orqali siz o‘z onlayn do‘koningizni
osongina raqamlashtirishingiz mumkin. Loyiha REST API (opsional) va admin interfeysi orqali biznesingizni boshqarishni
soddalashtiradi.

---

### 🎯 Maqsad

Foydalanuvchilar uchun qulay va soddalashtirilgan e-commerce platformasi yaratish, mahsulotlar va buyurtmalarni
boshqarish imkonini taqdim etish. Loyiha minimalizm, tezkorlik va foydalanuvchi tajribasiga e’tibor qaratadi.

---

### 🧱 Arxitektura

📁 Loyihaning papka tuzilmasi:

```
100k/
├── account/ # Foydalanuvchi autentifikatsiyasi va profilingi
├── cart/ # Savat (cart) funksiyalari
├── checkout/ # Buyurtma tasdiqlash va to‘lov tizimi
├── contact/ # Aloqa formasi va bog‘lanish sahifasi
├── core/ # Asosiy loyiha sozlamalari va funksiyalar
├── home/ # Bosh sahifa va umumiy funksiyalar
├── products/ # Mahsulotlar va katalog boshqaruvi
├── static/ # Statik fayllar (CSS, JS, rasmlar)
├── templates/ # HTML shablonlar
├── manage.py # Django boshqaruv fayli
├── requirements.txt # Kutubxonalar ro‘yxati
└── README.md # Loyihaga oid hujjat
```



---

### 🚀 Ishlatilgan Texnologiyalar

| Texnologiya           | Maqsadi                          |
|-----------------------|----------------------------------|
| Python 3.10+          | Asosiy dasturlash tili           |
| Django 4.x            | Web ilova framework              |
| SQLite                | Ma'lumotlar bazasi (test rejimi) |
| Django Admin          | Tizimni boshqarish interfeysi    |
| Bootstrap 5           | UI dizayn va responsivelik       |
| Pillow                | Rasm fayllar bilan ishlash       |
| Django Rest Framework | API endpointlar (opsional)       |

---

### ⚙️ Ishga tushirish

#### Talablar:

- Python 3.10+
- `virtualenv` yoki `poetry`
- SQLite (test rejimi uchun)

#### O‘rnatish:

```bash
git clone https://github.com/itsjasminn/100k.git
cd 100k
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

#### Superuser yaratish (admin panel uchun):

```
python manage.py createsuperuser
```

### ✅ Asosiy Funksiyalar

##### 🛒 Mahsulotlar katalogini yaratish, tahrirlash va ko‘rish

##### 🛍️ Savat tizimi (cart)

##### 💳 Buyurtma tasdiqlash va to‘lov jarayoni

##### 👤 Foydalanuvchi autentifikatsiyasi va ro‘yxatdan o‘tish

##### 📧 Aloqa formasi orqali foydalanuvchi bilan bog‘lanish

##### 🧾 Django admin orqali to‘liq boshqaruv

### 📈 Kelajakdagi Rejalar

##### 📱 REST API qo‘shish (mobil ilovalar uchun)

##### 💳 To‘lov integratsiyasi (Stripe, Payme, Click)

##### 🧍‍♂️ Foydalanuvchi profilingi va hisob sozlamalari

##### 📱 Responsive dizaynni yanada takomillashtirish

### 👩‍💻 Muallif

#### Made with 🧡 by Jasmina Ochildiyeva

[🔗 GitHub Profilim](https://github.com/itsjasminn)
[📂 FurniWeb Repository](https://github.com/itsjasminn/FurniWeb)


---

## 🇬🇧 English

**100k** — is a modern e-commerce web platform built with Django, enabling users to browse, purchase, and manage
products
online. This project helps digitize your online store with a robust admin panel and optional REST API support.


---

### 🎯 Purpose

To create a user-friendly and streamlined e-commerce platform for managing products and orders efficiently. The project
emphasizes minimalism, speed, and exceptional user experience.

---

### 🧱 Architecture

##### 📁 Project Folder Structure:

```
100k/
├── account/                # User authentication and profiles
├── cart/                   # Shopping cart functionality
├── checkout/               # Order confirmation and payment system
├── contact/                # Contact form and communication page
├── core/                   # Core project settings and utilities
├── home/                   # Homepage and general functionality
├── products/               # Product catalog management
├── static/                 # Static files (CSS, JS, images)
├── templates/              # HTML templates
├── manage.py               # Django management file
├── requirements.txt        # List of dependencies
└── README.md               # Project documentation
```

### 🚀 Technologies Used


| Technology            | Purpose                      |
|-----------------------|------------------------------|
| Python 3.10+          | Main programming language    |
| Django 4.x            | Web application framework    |
| SQLite                | Database (for testing)       |
| Django Admin          | Management interface         |
| Bootstrap 5           | UI design and responsiveness |
| Pillow                | Image handling               |
| Django Rest Framework | API endpoints (optional)     |

---


### ⚙️ Getting Started

###### Requirements:

* Python 3.10+

* virtualenv or poetry

* SQLite (for testing)


### Installation:

```
git clone https://github.com/itsjasminn/100k.git
cd 100k
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```


##### Create superuser (for admin panel):

```
python manage.py createsuperuser
```


### ✅ Key Features

#### 🛒 Create, edit, and view product catalogs

* 🛍️ Shopping cart system

* 💳 Order confirmation and payment processing

* 👤 User authentication and registration

* 📧 Contact form for user communication

* 🧾 Full management via Django admin


### 📈 Future Plans

#### 📱 Add REST API support (for mobile apps)

* 💳 Integrate payment systems (Stripe, Payme, Click)

* 🧍‍♂️ User profiles and account settings

* 📱 Further improvements in responsive design


### 👩‍💻 Author

#### Made with 🧡 by Jasmina Ochildiyeva

🔗 My GitHub Profile
📂 100k Repository

[🔗 My GitHub Profile](https://github.com/itsjasminn)
[📂 100k Repository](https://github.com/itsjasminn/FurniWeb)
