from flask import Flask, request, jsonify,render_template
from getpass import getpass
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_community.llms import HuggingFaceEndpoint
from dotenv import dotenv_values
from flask_cors import CORS
import os
import re

app = Flask(__name__)
CORS(app)
config = dotenv_values(".env")

HUGGINGFACEHUB_API_TOKEN=config.get("HUGGINGFACEHUB_API_TOKEN")

question_template = """Question: {question}\n\nAnswer: Let's think step by step."""

@app.route("/")
def home():
    print("HOME ENTERED")
    return jsonify({'answer':"answer"})


@app.route('/question', methods=['POST'])
def ask_question():
    os.environ["HUGGINGFACEHUB_API_TOKEN"] = HUGGINGFACEHUB_API_TOKEN
    subject = request.args.get('subject')
    topic = request.args.get('topic')
    repo_id = "mistralai/Mistral-7B-Instruct-v0.2"
    question = f'Tell me only one question from {subject} of topic {topic}'
    template = """Question: {question}

    Answer: Let's think step by step."""
    prompt = PromptTemplate.from_template(template)
    repo_id = "mistralai/Mistral-7B-Instruct-v0.2"

    llm = HuggingFaceEndpoint(
      repo_id=repo_id, max_length=128, temperature=0.5, token=HUGGINGFACEHUB_API_TOKEN
    )
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    print(llm_chain.run(question))
    answer=llm_chain.run(question)
    pattern = r'\b(?:What|Which|Who|Whom|Whose|How|Where|When|Why)\b.*?\?'
    match = re.search(pattern, answer, re.DOTALL)
    if match:
      first_question = match.group().strip()
      return jsonify({'question': first_question})
    else:
      return jsonify({'question': "NO QUESTION FOUND"})
    
@app.route('/answer', methods=['POST'])
def ask_answer():
    os.environ["HUGGINGFACEHUB_API_TOKEN"] = HUGGINGFACEHUB_API_TOKEN
    question = request.args.get('question')
    repo_id = "mistralai/Mistral-7B-Instruct-v0.2"
    question = f'{question}'
    template = """Question: {question}

    Answer: Let's think step by step."""
    prompt = PromptTemplate.from_template(template)
    repo_id = "mistralai/Mistral-7B-Instruct-v0.2"

    llm = HuggingFaceEndpoint(
      repo_id=repo_id, max_length=128, temperature=0.5, token=HUGGINGFACEHUB_API_TOKEN
    )
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    print(llm_chain.run(question))
    answer=llm_chain.run(question)
    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(debug=True)
