from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
import os
import pandas as pd
import pickle
import subprocess
app = Flask(__name__)
app.secret_key = os.urandom(24)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

def recommend(recipes):
    index = recipe[recipe['title'] == recipes].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    recommended_recipes = []  # Correct variable name to plural
    for i in distances[1:13]:
        recommended_recipe = {
            'title': recipe.iloc[i[0]]['title'],
            'image_url': recipe.iloc[i[0]]['image-url'],
            'link': recipe.iloc[i[0]]['link']
        }
        recommended_recipes.append(recommended_recipe)  # Append to list correctly

    return recommended_recipes

# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.email

# Routes
@app.route('/')
def index():
    signup_success = session.pop('signup_success', False)
    return render_template('index.html', signup_success=signup_success)

@app.route('/signup', methods=['POST'])
def signup():
    full_name = request.form['full_name']
    email = request.form['email']
    password = request.form['password']

    with app.app_context():
        # Check if the user already exists
        if User.query.filter_by(email=email).first() is not None:
            return "Email already exists. Please use a different email address."

        # Create a new user
        new_user = User(full_name=full_name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        session['signup_success'] = True
        return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    with app.app_context():
        # Check if user exists and password matches
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            session['email'] = email
            return redirect('/options')  # Redirect to options page upon successful login
        else:
            # Render index.html with error message
            return render_template('index.html', login_error=True)

@app.route('/options')
def options():
    if 'email' in session:
        return render_template("options.html")
    else:
        return redirect('/')

@app.route('/redirect_option1')
def redirect_option1():
    return redirect('/dashboard')


@app.route('/add_recipe', methods=['GET', 'POST'])
def add_recipe():
    if request.method == 'POST':
        # Get form inputs and convert them to strings
        title = str(request.form['title'])
        ingredients = str(request.form['ingredients'])
        directions = str(request.form['directions'])
        link = str(request.form['link'])
        image_url = str(request.form['image_url'])

        # Create DataFrame with user inputs
        user_data = pd.DataFrame({
            'title': [title],
            'ingredients': [ingredients],
            'directions': [directions],
            'link': [link],
            'image-url': [image_url]
        })

        # Append user data to existing dataset
        dataset_path = 'artifacts/processed_data.csv'
        existing_data = pd.read_csv(dataset_path)
        updated_data = pd.concat([existing_data, user_data], ignore_index=True)

        # Write updated dataset to CSV
        updated_data.to_csv(dataset_path, index=False)

        return "Recipe added to dataset successfully."

    # If GET request, render the form
    return render_template('adder.html')

@app.route('/execute_pipeline')
def execute_pipeline():
    python_interpreter = 'E:\\RECIPE RECOMMENDER MLOPS\\venv\\Scripts\\python.exe'
    script_path = 'E:\\RECIPE RECOMMENDER MLOPS\\src\\pipeline\\training_pipeline.py'

    # Run the script
    process = subprocess.Popen([python_interpreter, script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if process.returncode == 0:
        # Script executed successfully
        return 'Training completed successfully'
    else:
        # An error occurred
        return f'Error: {stderr.decode()}'

@app.route('/dashboard')
def dashboard():
    return render_template('home.html' , recipe_list=recipe["title"].values)


@app.route('/recommend', methods=['GET', 'POST'])
def recommendation():
    if request.method == 'POST':
        selected_recipe = request.form['selected_recipe']
        recommended_recipe = recommend(selected_recipe)
        return render_template('home.html', recommended_recipe=recommended_recipe)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    recipe = pickle.load(open('artifacts/recipes.pkl', 'rb'))
    similarity = pickle.load(open('artifacts/similarity.pkl', 'rb'))
    app.run(debug=True)
