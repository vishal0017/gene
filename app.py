import os
import openai
from openai import OpenAI
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_recipe_and_image', methods=['POST'])
def generate_recipe_and_image():
    try:
        ingredients = request.form.get('ingredients').split(',')
        num_people = request.form.get('num_people')
        allergies = request.form.get('allergies', '').split(',')
        lifestyle = request.form.get('lifestyle', '')

        if not ingredients or not num_people:
            return jsonify({'error': 'Ingredients and number of people are required'}), 400

        prompt = (f"Generate a recipe for {num_people} people with the following ingredients: "
                  f"{', '.join(ingredients)}. Do not add any other ingredients and provide the nutrition values "
                  f"of the recipe without explanation.")

        response = client.completions.create(model="gpt-3.5-turbo-instruct",
                                             prompt=prompt,
                                             max_tokens=500)

        if not response.choices:
            return jsonify({'error': 'Failed to generate recipe'}), 500

        recipe = response.choices[0].text.strip()
        image_url = ""  # Image generation code commented out for now

        return render_template('index.html', recipe=recipe, image_url=image_url)

    except openai.OpenAIError as e:
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred: ' + str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
