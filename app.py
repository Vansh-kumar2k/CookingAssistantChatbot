# # from flask import Flask, request, jsonify, render_template, send_from_directory
# # import google.generativeai as genai
# # import json
# # import os

# # app = Flask(__name__)

# # # Configure Gemini API key
# # genai.configure(api_key="YOUR_API_KEY_HERE")

# # # Serve index
# # @app.route("/")
# # def home():
# #     return render_template("index.html")

# # # Serve recipes.json dynamically
# # @app.route("/recipes.json")
# # def recipes_file():
# #     return send_from_directory(os.getcwd(), "recipes.json")

# # # Chatbot route
# # @app.route("/chat", methods=["POST"])
# # def chat():
# #     with open("recipes.json", "r", encoding="utf-8") as f:
# #         recipes = json.load(f)

# #     user_input = request.json.get("message", "").lower()
# #     if not user_input:
# #         return jsonify({"reply": "Please type something!"})

# #     # Check recipes first
# #     for recipe in recipes:
# #         recipe_name = recipe["name"].lower()
# #         ingredients = [i.lower() for i in recipe["ingredients"]]

# #         if recipe_name in user_input:
# #             reply = f"You asked about {recipe['name']}!\nSteps: {recipe['steps']}"
# #             return jsonify({"reply": reply})

# #         matched_ings = [i for i in ingredients if i in user_input]
# #         if matched_ings:
# #             missing_ings = [i for i in ingredients if i not in matched_ings]
# #             reply = f"You can make {recipe['name']} using {', '.join(matched_ings)}"
# #             if missing_ings:
# #                 reply += f". You will also need: {', '.join(missing_ings)}"
# #             reply += f"\nSteps: {recipe['steps']}"
# #             return jsonify({"reply": reply})

# #     # Fallback to Gemini AI
# #     try:
# #         model = genai.GenerativeModel("gemini-2.5-flash-lite")
# #         response = model.generate_content(user_input)
# #         bot_reply = response.text
# #     except Exception as e:
# #         bot_reply = f"Error: {e}"

# #     return jsonify({"reply": bot_reply})


# # if __name__ == "__main__":
# #     app.run(debug=True, port=5000)
# from flask import Flask, request, jsonify, render_template, send_from_directory
# import google.generativeai as genai
# import json
# import os

# app = Flask(__name__)

# # -----------------------------
# # Configure Gemini API (replace with your own key)
# # -----------------------------
# genai.configure(api_key="AIzaSyBk30rRCrmK4Vfiu9TBI6LFSUDqsCRUIvw")

# # Load recipes from JSON
# def load_recipes():
#     with open("recipes.json", "r", encoding="utf-8") as f:
#         return json.load(f)

# recipes = load_recipes()

# @app.route("/")
# def home():
#     return render_template("index.html", recipes=recipes)

# # Cache-busting route for recipes.json
# @app.route("/recipes.json")
# def recipes_json():
#     global recipes
#     recipes = load_recipes()  # reload from disk
#     response = jsonify(recipes)
#     response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
#     return response

# @app.route("/chat", methods=["POST"])
# def chat():
#     user_input = request.json.get("message", "").lower()
#     if not user_input:
#         return jsonify({"reply": "Please type something!"})

#     # Check recipes first
#     for recipe in recipes:
#         recipe_name = recipe["name"].lower()
#         ingredients = [i.lower() for i in recipe["ingredients"]]

#         # If user asks about recipe name
#         if recipe_name in user_input:
#             reply = f"You asked about {recipe['name']}!\nSteps: {recipe['steps']}"
#             return jsonify({"reply": reply})

#         # If user mentions ingredients
#         matched_ings = [i for i in ingredients if i in user_input]
#         if matched_ings:
#             missing_ings = [i for i in ingredients if i not in matched_ings]
#             reply = f"You can make {recipe['name']} using {', '.join(matched_ings)}"
#             if missing_ings:
#                 reply += f". You will also need: {', '.join(missing_ings)}"
#             reply += f"\nSteps: {recipe['steps']}"
#             return jsonify({"reply": reply})

#     # Fallback to Gemini AI
#     try:
#         model = genai.GenerativeModel("gemini-2.5-flash-lite")
#         response = model.generate_content(user_input)
#         bot_reply = response.text
#     except Exception as e:
#         bot_reply = f"Error: {e}"

#     return jsonify({"reply": bot_reply})

# if __name__ == "__main__":
#     app.run(debug=True, port=5000)
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import json
import os

app = Flask(__name__)

# -----------------------------
# Configure Gemini API
# -----------------------------
genai.configure(api_key="AIzaSyBk30rRCrmK4Vfiu9TBI6LFSUDqsCRUIvw")

# Load recipes from JSON
def load_recipes():
    with open("recipes.json", "r", encoding="utf-8") as f:
        return json.load(f)

@app.route("/")
def home():
    recipes = load_recipes()  # load fresh recipes
    return render_template("index.html", recipes=recipes)

@app.route("/recipes.json")
def recipes_json():
    recipes = load_recipes()  # reload from disk
    response = jsonify(recipes)
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "").lower()
    if not user_input:
        return jsonify({"reply": "Please type something!"})

    # Reload recipes each time for fresh data
    recipes = load_recipes()
    matched_replies = []

    for recipe in recipes:
        recipe_name = recipe["name"].lower()
        ingredients = [i.lower() for i in recipe["ingredients"]]

        # Match recipe name
        if recipe_name in user_input:
            matched_replies.append(f"You asked about {recipe['name']}!\nSteps: {recipe['steps']}")
            continue

        # Match ingredients mentioned
        matched_ings = [i for i in ingredients if i in user_input]
        if matched_ings:
            missing_ings = [i for i in ingredients if i not in matched_ings]
            reply = f"You can make {recipe['name']} using {', '.join(matched_ings)}"
            if missing_ings:
                reply += f". You will also need: {', '.join(missing_ings)}"
            reply += f"\nSteps: {recipe['steps']}"
            matched_replies.append(reply)

    # Return matched recipes if any
    if matched_replies:
        return jsonify({"reply": "\n\n".join(matched_replies)})

    # Fallback to Gemini AI
    try:
        model = genai.GenerativeModel("gemini-2.5-flash-lite")
        response = model.generate_content(user_input)
        bot_reply = response.text
    except Exception as e:
        bot_reply = f"Error: {e}"

    return jsonify({"reply": bot_reply})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
