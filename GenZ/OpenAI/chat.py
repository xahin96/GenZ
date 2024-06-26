import os
import sys
import time
import uuid

import openai
import openai.embeddings_utils
import pinecone
from dotenv import load_dotenv
import logging
from PyPDF2 import PdfReader

load_dotenv()

openai.api_key = "sk-proj-1yFkH3wOlBhkDY7xwWyyT3BlbkFJXoUpo2iJQbJplPN8665L"
pinecone.init(api_key="1b57b796-e343-477e-a1f8-5534ba5153a6", environment='gcp-starter')

pinecone_index_name = 'document-search-index'


#
# def remove_non_utf8_chars(content):
#     if isinstance(content, bytes):
#         content = content.decode('utf-8', 'ignore')
#     return content.encode('utf-8', 'ignore').decode('utf-8', 'ignore')
def load_documents():
    documents = []
    documents_path = './'
    for filename in os.listdir(documents_path):
        if filename.split('.')[-1] == "pdf":
            file_path = os.path.join(documents_path, filename)
            with open(file_path, 'rb') as file:
                reader = PdfReader(file)
                content = ""
                for page in reader.pages:
                    content += page.extract_text()
            clean_content = content
            documents.append({'title': filename.split('.')[0], 'content': clean_content})
            # print(clean_content[:1000])
    return documents


def load_document_content(title):
    documents_path = './'
    file_path = os.path.join(documents_path, title + '.pdf')
    with open(file_path, 'rb') as file:
        reader = PdfReader(file)
        content = ""
        for page in reader.pages:
            content += page.extract_text()
    clean_content = content
    return clean_content


def create_pinecone_index():
    pinecone.create_index(pinecone_index_name, metric='cosine', dimension=1536)


def fill_pinecone_index(documents):
    index = pinecone.Index(pinecone_index_name)
    for doc in documents:
        try:
            embedding_vector = get_embedding_vector_from_openai(doc['content'])
            # embedding_vector = embedding_vector.data[0].embedding
            # print(embedding_vector)
            data = pinecone.Vector(
                id=str(uuid.uuid4()),
                values=embedding_vector,
                metadata={'title': doc['title']}
            )
            index.upsert([data])
            print(f'Embedded and inserted document with title ' + doc['title'])
            time.sleep(1)
        except Exception as e:
            print(f'Could not embed and insert document with title ' + doc['title'])
            print(f'Error: {e}')


def query_pinecone_index(query):
    index = pinecone.Index(pinecone_index_name)
    query_embedding_vector = get_embedding_vector_from_openai(query)
    response = index.query(
        vector=query_embedding_vector,
        top_k=1,
        include_metadata=True
    )
    return response['matches'][0]['metadata']['title']


def get_embedding_vector_from_openai(text):
    # print(text)
    try:
        # Assuming 'openai.embeddings_utils.get_embedding' is a valid function
        # embedding = openai.embeddings_utils.get_embedding(text, engine='text-embedding-ada-002')
        embedding = openai.Embedding.create(input=text[:1000],engine='text-embedding-3-small')
        embedding_vector = embedding.data[0].embedding
        return embedding_vector
    except openai.error.InvalidRequestError as ire:
        logging.error(f"InvalidRequestError: {ire}")
        raise
    except openai.error.OpenAIError as oae:
        logging.error(f"OpenAIError: {oae}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise


def get_answer_from_openai(question):
    relevant_document_title = query_pinecone_index(question)
    print(f'Relevant document title: {relevant_document_title}')
    document_content = load_document_content(relevant_document_title)[:1000]
    prompt = create_prompt(question, document_content)
    print(f'Prompt:\n\n{prompt}\n\n')
    completion = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[{
            'role': 'user',
            'content': prompt
        }]
    )
    return completion.choices[0].message.content


def create_prompt(question, document_content):
    return 'You are given a document and a question. Your task is to answer the question based on the document.\n\n' \
           'Document:\n\n' \
           f'{document_content}\n\n' \
           f'Question: {question}'


if __name__ == "__main__":
    arg = sys.argv[1]
    if arg == 'create_index':
        create_pinecone_index()
    elif arg == 'fill_index':
        documents = load_documents()
        fill_pinecone_index(documents)
    elif arg == 'get_answer':
        question = input('Enter a question: ')
        answer = get_answer_from_openai(question)
        print(answer)
    else:
        print('Invalid argument')
