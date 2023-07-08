import os
import json
from langchain import SagemakerEndpoint
from langchain.llms.sagemaker_endpoint import LLMContentHandler


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
        print("Response text from SageMaker: " + response_json["generations"][0]["text"])

        # Access the generated text using the "generations" key
        return response_json["generations"][0]["text"]


content_handler = ContentHandler()
llm = SagemakerEndpoint(
    endpoint_name=os.environ["SAGEMAKER_ENDPOINT"],
    region_name=os.environ["AWS_REGION"],
    model_kwargs={"temperature": 0.7, "max_tokens": 200},
    content_handler=content_handler,
)


def generate_response(prompt):
    return llm(prompt)
