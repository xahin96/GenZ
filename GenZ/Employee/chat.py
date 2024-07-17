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
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
from django.conf import settings
media_path = settings.MEDIA_ROOT
pc = Pinecone(api_key='')
load_dotenv()

openai.api_key = ""

# pinecone_index_name = 'company1'


def load_documents(company_name):
    documents = []
    documents_path = media_path + '\\' + company_name + '\\'
    if os.path.exists(documents_path) and os.path.isdir(documents_path):
        print(media_path)
        for filename in os.listdir(documents_path):
            if filename.split('.')[-1] == "pdf":
                file_path = os.path.join(documents_path, filename)
                with open(file_path, 'rb') as file:
                    reader = PdfReader(file)
                    content = ""
                    documents_pages = []
                    for page in reader.pages:
                        page_content = page.extract_text()
                        content += page.extract_text()
                        documents_pages.append(page_content)
                clean_content = content
                documents.append({'title': filename.split('.')[0], 'content': documents_pages})
    return documents


def load_document_content(title, pages, company_name):
    clean_content = ""
    documents_path = media_path + '\\' + company_name + '\\'
    print(documents_path)
    if os.path.exists(documents_path) and os.path.isdir(documents_path):
        file_path = os.path.join(documents_path, title + '.pdf')
        count = 1
        with open(file_path, 'rb') as file:
            reader = PdfReader(file)
            content = ""
            for page in reader.pages:
                if (count == pages - 1 or count == pages or count == pages + 1):
                    content += page.extract_text()
                count += 1
        clean_content = content
    return clean_content


def create_pinecone_index(company_name):
    pinecone_index_name = company_name
    if pinecone_index_name not in pc.list_indexes().names():
        pc.create_index(
            name=pinecone_index_name,
            dimension=1536,
            metric="cosine",
            spec=ServerlessSpec(
                cloud='aws',
                region='us-east-1'
            )
        )
        return True
    else:
        return False


def fill_pinecone_index(pinecone_index_name,documents):
    index = pc.Index(pinecone_index_name)
    for doc in documents:
        try:
            count = 1
            for page in doc['content']:
                embedding_vector = get_embedding_vector_from_openai(page)
                data = pinecone.Vector(
                    id=str(uuid.uuid4()),
                    values=embedding_vector,
                    metadata={'title': doc['title'], 'page': count}
                )
                index.upsert([data])
                count += 1
        except Exception as e:
            print(f'Could not embed and insert document with title ' + doc['title'])
            print(f'Error: {e}')


def query_pinecone_index(pinecone_index_name,query):
    index = pc.Index(pinecone_index_name)
    query_embedding_vector = get_embedding_vector_from_openai(query)
    response = index.query(
        vector=query_embedding_vector,
        top_k=1,
        include_metadata=True
    )
    return response['matches'][0]['metadata']['title'], response['matches'][0]['metadata']['page']


def get_embedding_vector_from_openai(text):
    try:
        embedding = openai.Embedding.create(input=text, engine='text-embedding-3-small')
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


def get_answer_from_openai(pinecone_index_name,question):
    relevant_document_title, page = query_pinecone_index(pinecone_index_name,question)
    document_content = load_document_content(relevant_document_title, page,pinecone_index_name)
    if document_content:
        prompt = create_prompt(question, document_content)
        completion = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[{
                'role': 'user',
                'content': prompt
            }]
        )
        return completion.choices[0].message.content
    else:
        return "No content found"


def create_prompt(question, document_content):
    return 'You are given a document and a question. Your task is to answer the question based on the document.If there is no information related to the question in the document just say "nothing found in the document"\n\n' \
           'Document:\n\n' \
           f'{document_content}\n\n' \
           f'Question: {question}'
