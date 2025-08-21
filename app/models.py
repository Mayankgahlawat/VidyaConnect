from . import db  # Import the db instance from __init__.py

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

class JobCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False) # e.g., 'govt_job', 'cs_job'

class UserPreference(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('job_category.id'), primary_key=True)

# In app/models.py

# ... your User, JobCategory, and UserPreference classes are here ...

# In app/models.py

# ... your User, JobCategory, and UserPreference classes are here ...

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    company = db.Column(db.String(150), nullable=False)
    location = db.Column(db.String(150))
    url = db.Column(db.String(500), unique=True, nullable=False)
    category = db.Column(db.String(50))

    def __repr__(self):
        return f'<Job {self.title} at {self.company}>'