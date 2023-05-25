import openai

openai.api_key = "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"
model_engine = "gpt-3.5-turbo"

response = openai.ChatCompletion.create(
    model='gpt-3.5-turbo',
    messages=[{"role":"system",
              "content":"WHats the name of the Indian PM?"},
              {"role":"user",
               "content": "Hello",},
               ]
)

message = response.choices[0]['message']
print("{}:{}".format(message['role'], message['content']))