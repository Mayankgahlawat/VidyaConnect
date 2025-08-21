from dotenv import load_dotenv
load_dotenv()

from app import create_app, db
# Make sure Job is imported here
from app.models import User, JobCategory, UserPreference, Job 

app = create_app()

@app.shell_context_processor
def make_shell_context():
    # Add 'Job': Job to this dictionary
    return {'db': db, 'User': User, 'JobCategory': JobCategory, 'UserPreference': UserPreference, 'Job': Job}

if __name__ == '__main__':
    app.run(debug=True)