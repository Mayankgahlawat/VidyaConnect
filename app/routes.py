# All imports must be at the top of the file
from flask import Blueprint, request, jsonify, current_app, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta, timezone
import jwt
import requests
import os
from .models import User, Job
from . import db

# --- Blueprint for serving HTML pages ---
main_bp = Blueprint('main_bp', __name__)

@main_bp.route('/')
def index():
    """Renders the main news dashboard page."""
    return render_template('index.html')

@main_bp.route('/login')
def login_page():
    """Renders the login page."""
    return render_template('login.html')

@main_bp.route('/register')
def register_page():
    """Renders the registration page."""
    return render_template('register.html')

# --- Blueprint for API endpoints (handling data) ---
api_bp = Blueprint('api_bp', __name__)
# In app/routes.py, inside the 'api_bp' blueprint

@api_bp.route('/jobs', methods=['GET'])
def get_jobs():
    """
    Endpoint to fetch scraped job listings from the database.
    """
    # For now, we fetch all jobs. Later, we can filter by user preference.
    jobs = Job.query.all()

    # Convert the list of job objects into a list of dictionaries
    jobs_list = []
    for job in jobs:
        jobs_list.append({
            'id': job.id,
            'title': job.title,
            'company': job.company,
            'location': job.location,
            'url': job.url,
            'category': job.category
        })

    return jsonify(jobs_list) 

@api_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    # ... (rest of registration logic is the same)
    if not data or not 'username' in data or not 'password' in data:
        return jsonify({'message': 'Username and password are required!'}), 400
    username = data['username']
    password = data['password']
    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'Username already exists!'}), 409
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    new_user = User(username=username, password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully!'}), 201

@api_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    # ... (rest of login logic is the same)
    if not data or not 'username' in data or not 'password' in data:
        return jsonify({'message': 'Username and password are required!'}), 400
    username = data['username']
    password = data['password']
    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({'message': 'Invalid username or password!'}), 401
    token = jwt.encode({
        'user_id': user.id,
        'exp': datetime.now(timezone.utc) + timedelta(hours=24)
    }, current_app.config['SECRET_KEY'], algorithm='HS256')
    return jsonify({'token': token})

@api_bp.route('/news/top-headlines', methods=['GET'])
def get_top_headlines():
    api_key = os.getenv('MEDIASTACK_API_KEY')
    # ... (rest of news fetching logic is the same)
    if not api_key:
        return jsonify({'message': 'MediaStack API key is missing!'}), 500
    url = f"http://api.mediastack.com/v1/news?access_key={api_key}&countries=in"
    try:
        response = requests.get(url)
        response.raise_for_status()
        news_data = response.json()
        return jsonify(news_data)
    except requests.exceptions.RequestException as e:
        return jsonify({'message': f'Error fetching news: {e}'}), 500