# json_playground.py

import json

# --------------------------------
# 1. Python Dict -> JSON String
# --------------------------------

user = {
    "name": "Ahmed",
    "age": 22,
    "skills": ["Python", "FastAPI", "LangGraph"],
    "active": True
}

json_string = json.dumps(user, indent=4)

print("JSON String:")
print(json_string)

# --------------------------------
# 2. JSON String -> Python Dict
# --------------------------------

data = json.loads(json_string)

print("\nName:", data["name"])
print("First Skill:", data["skills"][0])

# --------------------------------
# 3. Save JSON to File
# --------------------------------

with open("user.json", "w") as file:
    json.dump(user, file, indent=4)

print("\nJSON saved to user.json")

# --------------------------------
# 4. Read JSON from File
# --------------------------------

with open("user.json", "r") as file:
    loaded_data = json.load(file)

print("\nLoaded from file:")
print(loaded_data)

# --------------------------------
# 5. Nested JSON
# --------------------------------

api_response = {
    "user": {
        "profile": {
            "name": "Ahmed",
            "email": "ahmed@example.com"
        },
        "projects": [
            {"name": "RAG System"},
            {"name": "AI Agent"}
        ]
    }
}

print("\nNested JSON Access:")
print(api_response["user"]["profile"]["name"])
print(api_response["user"]["projects"][1]["name"])
