import openai

# Replace 'your_api_key_here' with your actual OpenAI API key
openai.api_key = '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'

def test_openai_api(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=50,
            n=1,
            temperature=0.7,
        )
        return response.choices[0].message['content']
    except Exception as e:
        print(f"Error: {e}")
        return None
# Test the OpenAI API with a sample prompt
prompt = "What is the capital of France?"
response = test_openai_api(prompt)

if response:
    print(f"API response: {response}")
else:
    print("There was an issue with the API.")
