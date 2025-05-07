
# 🌾 Agri Market

Agri Market is a Django-based e-commerce platform tailored for agricultural products. It connects farmers and consumers, offering features like product browsing, cart management, admin analytics, and a basic ML-powered recommendation system.

---

## 📁 Project Structure

```
agri-market/
├── agri_market/         # Django project settings
├── products/            # Product models, views, templates
├── users/               # Authentication and user profile
├── orders/              # Cart, checkout, order tracking
├── ML/                  # Recommendation engine
├── templates/           # HTML templates
├── static/              # CSS, JS, images
├── requirements.txt     # Python dependencies
└── manage.py
```

---

## 🔧 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/agri-market.git
cd agri-market
```

### 2. Create a Virtual Environment

```bash
python -m venv env
```

### 3. Activate the Virtual Environment

- **On Windows:**

```bash
env\Scripts\activate
```

- **On macOS/Linux:**

```bash
source env/bin/activate
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

## 🤖 ML Recommendation Engine

Located in the `ML/` directory, this module uses basic logic to suggest products to users. Future improvements could include collaborative filtering or neural recommendations.

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
