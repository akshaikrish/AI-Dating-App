import openai

openai.api_key = "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"
# endpoint_url = "https://api.openai.com/v1/chat/completions"

# prompt = "Hi, I am Akshai."
# model = "text-davinci-003"
# response =  openai.Completion.create(engine = model, prompt = prompt, max_tokens = 50)

# generated_response = response.choices[0].text

# print(generated_response)


# context = "Albert Einstein was a German-born theoretical physicist who developed the theory of relativity."
# question = "Where was Albert Einstein born?"
# response = openai.Completion.create(
#   engine="gpt-3.5-turbo",
#   prompt=f"Question answering:\nContext: {context}\nQuestion: {question}",
#   max_tokens=50
# )

# answer = response.choices[0].text.strip()
# print(answer)

import os

# openai.api_key = os.getenv('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')

completion = openai.ChatCompletion.create(
  model = 'gpt-3.5-turbo',
  messages = [
    {'role': 'user', 'content': 'I am Akshai. Nice to meet you'}
  ],
  temperature = 0  
)

print(completion['choices'][0]['message']['content'])

