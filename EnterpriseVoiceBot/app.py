from flask import Flask, render_template, request, jsonify, session
import boto3
import json
import os
import urllib.parse

from aws_langchain.kendra_index_retriever import KendraIndexRetriever
from langchain import SagemakerEndpoint
from langchain.chains import RetrievalQA
from langchain.llms.sagemaker_endpoint import LLMContentHandler
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
load_dotenv()

from general_assistant import generate_response

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "mysecretkey")

# Your AWS credentials, SageMaker endpoint, and Kendra index information
aws_region = os.environ["AWS_REGION"]
sagemaker_endpoint = os.environ["SAGEMAKER_ENDPOINT"]
kendra_index_id = os.environ["KENDRA_INDEX_ID"]

# Configure the Boto3 session with your AWS credentials
boto3.setup_default_session(
    aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
    region_name=aws_region,
)


class ContentHandler(LLMContentHandler):
    content_type = "application/json"
    accepts = "application/json"

    def transform_input(self, prompt: str, model_kwargs: dict) -> bytes:
        input_str = json.dumps({"prompt": prompt, **model_kwargs})

        print(f"Prompt length: {len(prompt)}")
        print(f"Input string to SageMaker: {input_str}")

        return input_str.encode('utf-8')

    def transform_output(self, output: bytes) -> str:
        response_json = json.loads(output.read().decode("utf-8"))

        # Add this print statement
        print("Response text from SageMaker: " + response_json["completions"][0]["data"]["text"])

        # Access the generated text using the "generations" key
        return response_json["completions"][0]["data"]["text"]


# Kendra retriever
retriever = KendraIndexRetriever(
    kendraindex=kendra_index_id,
    awsregion=aws_region,
    return_source_documents=False
)

# Sagemaker endpoint
content_handler = ContentHandler()

llm_internal_data_search = SagemakerEndpoint(
    endpoint_name=sagemaker_endpoint,
    region_name=aws_region,
    model_kwargs={"temperature": 0.2, "maxTokens": 500, "numResults": 1},
    content_handler=content_handler,
)

llm_general_assistant = SagemakerEndpoint(
    endpoint_name=sagemaker_endpoint,
    region_name=aws_region,
    model_kwargs={"temperature": 0.7, "maxTokens": 500, "numResults": 1},
    content_handler=content_handler,
)

# Prompt template for internal data bot interface
template = """You are a talkative AI Retrieval Augmented knowledge bot who answers questions with only the data provided as context. You give lots of detail in your answers, and if the answer to the question is not present in the context section at the bottom, you say "I don't know".  

  Now read this context and answer the question at the bottom:
Context: "{context}"

Question: {question}
Answer:"""

PROMPT = PromptTemplate(
    template=template, input_variables=["context", "question"]
)

# Prompt template for the General Assistant tab
GENERAL_ASSISTANT_PROMPT = PromptTemplate(
    template="{system_prompt}\n\n{task}:",
    input_variables=["system_prompt", "task"]
)

def generate_response_general_assistant(user_input):
    input_variables = {
        "system_prompt": "The AI is a helpful assistant that closely follows a users instructions and/or answers their questions. "
                         "If the AI does not know the answer to a question, it truthfully says so.",
        "task": user_input,
    }

    prompt = GENERAL_ASSISTANT_PROMPT.format(**input_variables)

    llm_general_assistant.model_kwargs = {"temperature": 0.7, "maxTokens": 500, "numResults": 1}

    result = llm_general_assistant(prompt)

    return result.strip()

# RetrievalQA instance with custom prompt template
chain_type_kwargs = {"prompt": PROMPT}
qa = RetrievalQA.from_chain_type(
    llm=llm_internal_data_search,
    chain_type="stuff",
    retriever=retriever,
    chain_type_kwargs=chain_type_kwargs,
    return_source_documents=True,
)

# Route for Internal Data Bot prompt - First searches Kendra Index for context based on user input before routing to SageMaker endpoint
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_input = request.form.get("user_input")
        input_type = request.form.get("input_type", "text")

        if user_input.strip() == "":
            result = {"answer": "Please provide a question."}
        else:

            print(f"User input: {user_input}")

            input_variables = {
                "question": user_input,
            }

            print(f"Input variables: {input_variables}")

            result = qa(user_input)

        if("I don't know" not in result["result"] and len(result['source_documents']) > 0):
            source_url = result['source_documents'][0].metadata['source']
            safe_source_url = urllib.parse.quote_plus(source_url)
            response_text = result["result"].strip() + "<br><br>ref: <a href=" + safe_source_url + ">" + source_url + "</a>"
        else:
            response_text = "I don't know"

        return jsonify({"response": response_text})
    return render_template("index.html")

# Route for General Assitant prompt input - bypasses Kendra and sends user prompt directly to the SageMaker endpoint
@app.route("/general_assistant", methods=["POST"])
def general_assistant():
    user_input = request.form.get("user_input")
    input_type = request.form.get("input_type", "text")

    if user_input.strip() == "":
        response_text = "Please provide some text."
    else:
        response_text = generate_response_general_assistant(user_input)

    return jsonify({"response": response_text})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)