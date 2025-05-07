# 🌾 Agri Market

Agri Market is a Django-based e-commerce platform tailored for agricultural products. It connects farmers and consumers, offering features like product browsing, cart management, and admin analytics.

---

## 📁 Project Structure

```
AgriECommerce/
├── AgriECommerce/      # Django project settings
├── homepage/           # Homepage app
├── users/              # Authentication and user profile
├── templates/          # HTML templates
├── static/             # CSS, JS, images
├── media/              # User uploaded files
├── locale/             # Translation files
├── requirements.txt    # Python dependencies
├── manage.py           # Django management script
└── db.sqlite3          # SQLite database
```

---

## 🔧 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/techg/AgriECommerce.git
cd AgriECommerce
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

### 3. Activate the Virtual Environment

- **On Windows:**

```bash
.venv\Scripts\activate
```

- **On macOS/Linux:**

```bash
source .venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create a Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

### 7. Run the Development Server

```bash
python manage.py runserver
```

### 8. Open in Browser

Visit: [http://localhost:8000](http://localhost:8000)

### 9. Access Admin Panel

Visit: [http://localhost:8000/admin](http://localhost:8000/admin)  
Login using the superuser credentials you just created.

---

## 🤖 Features

- User authentication and profile management
- Product browsing and search
- Shopping cart functionality
- Order management
- Admin dashboard for analytics
- Multi-language support
- Responsive design for mobile and desktop

---

## 🤝 Contributing

We welcome contributions!

1. Fork the repository
2. Create a new branch:
   ```bash
   git checkout -b feature-branch
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add new feature"
   ```
4. Push your branch:
   ```bash
   git push origin feature-branch
   ```
5. Open a Pull Request

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

**Made with ❤️ to empower farmers and digitize agriculture.**
