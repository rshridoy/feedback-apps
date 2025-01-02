from flask import Flask, request, jsonify
import os
import vertexai
from vertexai.generative_models import GenerativeModel, SafetySetting
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Set up Google Application Credentials for authentication
current_dir = os.path.dirname(os.path.realpath(__file__))
service_account_path = os.path.join(current_dir, 'cred', 'service-account.json')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = service_account_path

# Vertex AI settings
PROJECT_ID = "numeric-datum-444816-e0"
LOCATION = "us-central1"

# Initialize Vertex AI
vertexai.init(project=PROJECT_ID, location=LOCATION)

# Safety settings for the model
safety_settings = [
    SafetySetting(category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH, threshold="BLOCK_NONE"),
    SafetySetting(category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT, threshold="BLOCK_NONE"),
    SafetySetting(category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT, threshold="BLOCK_NONE"),
    SafetySetting(category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT, threshold="BLOCK_NONE"),
]

generation_config = {
    "max_output_tokens": 8192,
    "temperature": 1,
    "top_p": 0.95,
}

def generate_solution(bug_description):
    # Define the model to use (e.g., Gemini model)
    model = GenerativeModel("gemini-1.5-flash-002", system_instruction="Suggest a solution for this bug:")
    # Generate content based on the bug description
    response = model.generate_content(
        [bug_description],
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=False  # Disable streaming for simplicity
    )

    # Access the generated content from the response
    if response and hasattr(response, "text"):
        return response.text  # Return the generated text

    return "No suggestion available."  # Return a default message if no solution is found

@app.route("/api/feedback", methods=["POST"])
def feedback():
    try:
        # Get the feedback data from the request
        data = request.json
        feedback_text = data.get("feedbackText", "")
        feedback_type = data.get("feedbackType", "")

        if feedback_type == "Bug":
            # If feedback type is 'Bug', generate a suggestion using AI
            suggestion = generate_solution(feedback_text)
            return jsonify({"suggestion": suggestion})
        
        # If the feedback type is not 'Bug', return a thank you message
        return jsonify({"suggestion": "Thank you for your feedback!"})

    except Exception as e:
        # Handle errors and return the error message
        app.logger.error(f"Error in feedback route: {str(e)}")
        return jsonify({"error": f"Failed to process feedback: {str(e)}"}), 500

if __name__ == "__main__":
    # Run the Flask app on port 3000 in debug mode
    app.run(debug=True, port=3000)
