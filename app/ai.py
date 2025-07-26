



def generate_question(topic="Averages", difficulty="medium"):
    prompt = f"Create 1 quantitative reasoning MCQ on the topic {topic} for FSC level NAT test with 4 options, correct answer, and explanation."
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']
