def get_chatbot_response(user_input):
    text = user_input.lower()
    if "traffic" in text:
        return "Traffic data is shown on the Traffic & Mobility page."
    if "pollution" in text:
        return "Air quality is available on the Pollution page."
    if "feedback" in text:
        return "You can submit your feedback on the Citizen Feedback page."
    return "Welcome! Ask me about traffic, pollution or feedback."
