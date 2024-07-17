import openai
import pickle
import os

from dotenv import load_dotenv
from pinecone import Pinecone

# Load your API key from an environment variable or secret management service
pc = Pinecone(api_key='cbce143e-7f60-4ba2-8b50-cb10eb3004a8')
load_dotenv()
openai.api_key = "sk-proj-1yFkH3wOlBhkDY7xwWyyT3BlbkFJXoUpo2iJQbJplPN8665L"

EMBEDDINGS_FILE = "embeddings.pkl"


def get_embeddings(text):
    response = openai.Embedding.create(
        model="text-embedding-ada-002",
        input=text
    )
    return response['data'][0]['embedding']


def save_embeddings(embeddings):
    with open(EMBEDDINGS_FILE, 'wb') as file:
        pickle.dump(embeddings, file)


def load_embeddings():
    if os.path.exists(EMBEDDINGS_FILE):
        with open(EMBEDDINGS_FILE, 'rb') as file:
            return pickle.load(file)
    return {}


def answer_question(question, context, embeddings_cache):
    context_key = f"context:{context}"

    if context_key not in embeddings_cache:
        context_embedding = get_embeddings(context)
        embeddings_cache[context_key] = context_embedding
        save_embeddings(embeddings_cache)
    else:
        context_embedding = embeddings_cache[context_key]

    question_embedding = get_embeddings(question)

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"Context: {context}\nQuestion: {question}"}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0,
        max_tokens=100
    )

    answer = response["choices"][0]["message"]["content"]

    return answer


# Example usage
question = "Which semester is running for zahin?"
context = """
I'm Zahin. I have finished 18 credits in my University of Windsor Master of Applied Computing degree.
My current CGPA is 3.30/4.00
This is his 3rd semester running
"""

embeddings_cache = load_embeddings()
answer = answer_question(question, context, embeddings_cache)
print(answer)
