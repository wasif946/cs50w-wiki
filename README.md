## 📚 Project 1: Wiki

A Wikipedia-like encyclopedia web app using Django and Markdown.

### ✨ Features
- View encyclopedia entries rendered from Markdown
- Create new entries with Markdown content
- Edit existing pages
- Search with both exact and partial matches
- Random page button
- Markdown to HTML rendering

### 🛠️ Technologies
- Django (Python)
- HTML/CSS
- Markdown2 package

### 🚀 How to Run
pip install -r requirements.txt
python manage.py runserver
wiki/
├── entries/         # Markdown files
├── encyclopedia/    # Django app
│   ├── views.py
│   ├── urls.py
│   └── templates/
├── manage.py
└── README.md
