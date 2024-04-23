from flask import Flask, request, jsonify,render_template
from getpass import getpass
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_community.llms import HuggingFaceEndpoint
from dotenv import dotenv_values
import os

app = Flask(__name__)

config = dotenv_values(".env2")

HUGGINGFACEHUB_API_TOKEN=config.get("HUGGINGFACEHUB_API_TOKEN")

question_template = """Question: {question}\n\nAnswer: Let's think step by step."""

@app.route("/")
def home():
    print("HOME ENTERED")
    return jsonify({'answer':"answer"})


@app.route('/translate', methods=['POST'])
def translate_text():
    os.environ["HUGGINGFACEHUB_API_TOKEN"] = HUGGINGFACEHUB_API_TOKEN
    print(HUGGINGFACEHUB_API_TOKEN)
    question = request.args.get('question')
    print("ngvjek")
    repo_id = "mistralai/Mistral-7B-Instruct-v0.2"
    print("hell")
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
