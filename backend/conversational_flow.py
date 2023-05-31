import requests

conversational_flow = {
    "intents": {
        "speed_improvement": {
            "questions": [
                "What are some effective running drills for speed improvement?",
                "How can I increase my running speed?",
                "Any tips for getting faster in running?"
            ],
            "responses": [
                "Interval training and hill repeats can improve speed.",
                "Incorporating sprints and tempo runs into your training can help with speed improvement.",
                "Consider working with a running coach for personalized speed training."
            ]
        },
        "injury_prevention": {
            "questions": [
                "How can I prevent running injuries?",
                "Any tips to avoid getting injured while running?",
                "What are some common running injuries and how to prevent them?"
            ],
            "responses": [
                "Make sure to warm up before your runs and cool down afterward.",
                "Gradually increase your mileage and incorporate strength training for injury prevention.",
                "Listen to your body, take rest days when needed, and invest in proper running shoes."
            ]
        },
        # Add more intents and their corresponding questions and responses
    }
}

def get_intent_response(intent):
    if intent in conversational_flow["intents"]:
        responses = conversational_flow["intents"][intent]["responses"]
        return responses[0] if responses else None
    return None

def process_question(question):
    intent = None
    # Implement your logic to determine the intent based on the question
    # You can use natural language processing techniques or pattern matching

    if intent:
        response = get_intent_response(intent)
        if response:
            return response

    # If no matching intent or response found, return a default response
    return "I'm sorry, I don't have the information you're looking for."

def run_conversational_flow():
    question = input("Enter your question: ")
    response = process_question(question)
    # print("Response:", response)

    # Make a request to the virtual_coach endpoint using the provided question
    payload = {"query": question}
    url = "http://127.0.0.1:8000/virtual_coach"
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()
        print("Virtual Coach Response:", data["response"])
    else:
        print("Error occurred while requesting virtual_coach endpoint.")

if __name__ == "__main__":
    run_conversational_flow()