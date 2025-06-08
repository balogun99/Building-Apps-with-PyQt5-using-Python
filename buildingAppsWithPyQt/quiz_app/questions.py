import json

def load_questions():
    try:
        with open("quiz_app/questions.json", "r") as file:
            data = json.load(file)
            return data['questions']
    except Exception as e:
        print(f"Error loading questions: {e}")
        return []