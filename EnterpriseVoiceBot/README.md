# Corporate RAG Assistant

Welcome to the Corporate RAG Assistant, a chatbot built in Python/Flask that uses Amazon Kendra, Langchain, and a large language model (AI21 Jurassic-2 Mid) hosted on SageMaker to answer questions by providing trusted sources in combination with a user's prompt to a generative language model.

The bot has two modes, 'Internal Data Bot' which uses RAG orchestration to gather trusted data, and a 'General Assistant' which simply routes users questions directly to the LLM, bypassing the RAG orchestrator. The inclusion of these two interfaces are intended to demonstrate an internal/trusted knowledge search alongside a general purpose productivity assistant functionality (ex: help write this email), all within the same infrastructure.

In order for the RAG functionality of this bot to work, you will need to upload data to your S3 bucket and index the bucket data via Kendra (both resources are deployed via the cloudformation script). You can upload all text formats that Kendra supports indexing on (PDF, txt, doc etc.) to the bucket either manually, or with the included web crawler.

## Chatbot Setup

To get started with the chatbot, follow these steps:

1. Subscribe to the 'AI21 Jurassic-2 Mid' in SageMaker Jumpstart (if you don't have access, you will need to request it) - https://us-east-1.console.aws.amazon.com/sagemaker/playground?region=us-east-1#/foundation-models/playground/prodview-bzjpjkgd542au - The instance you will be deploying on is a ml.g5.12xlarge - if you don't have access to this instance type you will need to request an instance limit increase request - https://docs.aws.amazon.com/sagemaker/latest/dg/data-wrangler-increase-instance-limit.html.

2. Run the CloudFormation script to set up the: Kendra Index, S3 bucket, IAM roles, and SageMaker Endpoint. This is located under EnterpriseVoiceBot/cloudformation/
   **Note:** cost can be significant depending on the instance size chosen. Delete it when you are done testing.

3. Note the 'Outputs' of the CloudFormation stack (Kendra ID, Sagemaker Endpoint name, etc.) and set them in your .env file at the top level of the /EnterpriseVoiceBot directory.

4. Create (or re-use) an existing AWS API access key and set the public and secret key values in your .env file.

### Prerequisites

- Python 3.8 or later
- [pip](https://pip.pypa.io/en/stable/installation/)
- [Homebrew](https://brew.sh/) (for macOS users)

### Installation

1. Clone the repository:

   ```
   git clone https://gitlab.aws.dev/knowledge-base-automation/llm-scrape/-/tree/main
   cd *your-path-root*/llm-scrape/EnterpriseVoiceBot

   -OR-

   Download the code package from GitLab manually and then open a terminal to the /EnterpriseVoiceBot directory
   ```

2. Set up AWS credentials and other environment variables in a `.env` file inside the /EnterpriseVoiceBot directory (you will need data from the output of the CloudFormation script above):

   ```
   AWS_REGION=your-aws-region
   SAGEMAKER_ENDPOINT=your-sagemaker-endpoint
   KENDRA_INDEX_ID=your-kendra-index-id
   AWS_ACCESS_KEY_ID=your-aws-access-key-id
   AWS_SECRET_ACCESS_KEY=your-aws-secret-access-key
   ```

3. Create a virtual environment and activate it:

   ```
   python3 -m venv venv
   source venv/bin/activate
   ```

4. Install Python package dependencies:

   ```
   pip install -r requirements.txt
   ```

5. Run the Flask application:

   ```
   python app.py
   ```

   The application should now be accessible at [http://localhost:5000](http://localhost:5000).

### Usage

To use the chatbot, follow these steps:

1. Open your browser and navigate to [http://localhost:5000](http://localhost:5000).
2. Type your question.
3. The application will display the AI's response in the chat window.

Thank you for using Corporate RAG Assistant!
