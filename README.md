# Retrieval-Augmented Generation (RAG) with Kendra and Sagemaker using AI21 (jurassic) 

I wanted to experiment with building  a chatbot in Python that uses AWS Kendra, Langchain, and a large language model (AI21 Jurassic-2 Grande Instruct) hosted on SageMaker to answer questions by providing trusted sources in combination with a user's prompt to a generative language model.

The bot has two modes, 'Internal Data Bot' which uses RAG orchestration to gather trusted data, and a 'General Assistant' which simply routes users questions directly to the LLM, bypassing the RAG orchestrator. The inclusion of these two interfaces are intended to demonstrate an internal/trusted knowledge search alongside a general purpose productivity assistant functionality (ex: help write this email), all within the same infrastructure.

In order for the RAG functionality of this bot to work, you will need to upload data to your S3 bucket and index the bucket data via Kendra (both resources are deployed via the cloudformation script). You can upload all text formats that Kendra supports indexing on (PDF, txt, doc etc.) to the bucket either manually, or with the included web crawler. We have also created mock company data (AnyCompany) you can use, the WorkDocs zip download link is provided at the bottom of this introduction.

The web crawler has been included in this package to give you the option of customizing the demo environment based on your customer. In many cases, customers have public knowledge article websites that can be crawled for a more impactful demo. You may try the Kendra native crawler first if you would like, but in many cases it can be blocked. In these situations you can take advantage of this project's crawler. After setup, the crawler is configured to crawl 2 pages deep by default.

Mock 'AnyCompany' data zip - https://amazon.awsapps.com/workdocs/index.html#/document/eceffbf6f0888314345ad167eafca83e7a8d9bf8f7fe7873a73c4dc4be0160ee

## Crawler Setup

**Note:** Unfortunately the crawler library doesn't support Windows. However, you can still use the Chatbot portion of this demo.

1. Install scrapy - see documentation https://docs.scrapy.org/en/latest/intro/install.html

   ```
   pip install scrapy
   ```

2. Install scrapy-playwright, a headless browser library that helps with javascript rendering html. https://github.com/scrapy-plugins/scrapy-playwright

   ```
   pip install scrapy-playwright

   playwright install
   ```
if you faced error installing it follwo below steps : 
```
sudo apt update
```
Step 2: Install Python and pip
Check if Python is already installed by running the command:
```
python3 --version

```
If Python is not installed, run the following command to install it:

```
sudo apt install python3
```
Check if pip is installed by running the command:
```
pip3 --version
```
If pip is not installed, run the following command to install it:

```
sudo apt install python3-pip

```

Step 3: Install Dependencies
Scrapy-Playwright requires some additional dependencies. Run the following command to install them:

```
sudo apt install -y curl unzip xvfb libxi6 libgconf-2-4
```

Step 4: Install Playwright
Run the following command to install Playwright:

```
pip3 install playwright
```

Step 5: Install Browser Dependencies
Scrapy-Playwright supports multiple browsers. You can choose the one you prefer. To install Chromium, run the following command:

```
playwright install chromium
```
Step 6: Install Scrapy-Playwright
Finally, install Scrapy-Playwright using pip:
```
pip3 install scrapy-playwright
```
That's it! Scrapy-Playwright should now be successfully installed on your Ubuntu system. You can verify the installation by running the command:

```
scrapy-playwright --version
```
If you get playwright: command not found error: 
If you encounter the "playwright: command not found" error after installing Scrapy-Playwright on Ubuntu, it might be due to the Playwright command-line interface (CLI) not being added to your system's PATH variable. Here's a possible solution:

Verify the Playwright installation:
Run the following command to check if Playwright is installed correctly:
```
pip3 show playwright
```
Ensure that the package details are displayed, confirming that Playwright is installed.

Add Playwright to the PATH variable:
Open your shell profile file (e.g., ~/.bashrc or ~/.bash_profile) in a text editor:

```
nano ~/.bashrc
```
Add the following line at the end of the file:
```
export PATH=$PATH:~/.local/bin
```
Save the file and exit the text editor.

Update the PATH variable:
Run the following command to update the PATH variable in your current shell session:
```
source ~/.bashrc

playwright --version
```
make sure you run this : 
```
git clone 

3. Update the URL on line 13 and 15 of scrapy/kb/kb/spiders/knowledge_base.py to be your companies parent knowledge base index URL. Something like this for line 14 https://docs.aws.amazon.com/index.html where downstream links are aggregated and this for line 13 docs.aws.amazon.com.

4. From terminal, execute scrapy crawl kb from the scrapy/kb/ directory. This may take a while to complete, so feel free to stop the crawler after ~10mins or enough files are collected.

   ```
   scrapy crawl kb
   ```

5. Optional - The bot scrapes 2 levels deep by default. Additionally, it waits for 3 seconds on each web page for loading along with waiting for network connections to stop. Additional tweaks may be required to crawl your customer site successfully.

6. Manually upload crawled files from scrapy/kb/output/ to your S3 bucket and Kendra index. Deploy Kendra/S3 below in Chatbot Setup. (this will be automated in the future)

## Chatbot Setup

To get started with the chatbot, follow these steps:

1. Subscribe to the 'AI21 Jurassic-2 Grande Instruct' in SageMaker Jumpstart (if you don't have access, you will need to request it) - https://us-east-1.console.aws.amazon.com/sagemaker/playground?region=us-east-1#/foundation-models/playground/prodview-bzjpjkgd542au - The instance you will be deploying on is a ml.g5.12xlarge - if you don't have access to this instance type you will need to request an instance limit increase request - https://console.aws.amazon.com/servicequotas/home/services/sagemaker/quotas/L-65C4BD00

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

### Optimizing Responses

There are various methods you can use to optimize the quality of response by the LLM, most of which will focus on refining the prompt template, temperature and context window. For example, in the provided code we are using a template to define the system prompt, but the RAG portion of the bot will still answer questions outside of the scope of the context that it has been provided. Consider adding 'few shot' examples in your own prompt template to improve the quality of responses if you would like the bot to respond in a particular way, or to not answer questions that fall outside of the scope of the context provided by Kendra. For example, adding few shot learning to the prompt template against a Kendra Index on AWS Documentation would look like this:

Example QnA 1:
User: what is bitcoin?
Context: [blank] OR returned data that is not relevant to the users question
AI: I don't know

Example QnA 2:
User: What is the well-architected framework?
Context: The Well- Architected Framework is a scalable mechanism that lets you take advantage of these learnings. By following the approach of a principal engineering community with distributed ownership of architecture, we believe that a Well-Architected enterprise architecture can emerge that is driven by customer need. Technology leaders (such as a CTOs or development managers), carrying out Well- Architected reviews across all your workloads will permit you to better understand the risks in your technology portfolio.
AI: The Well-Architected Framework is a framework from AWS that....

### Contact for Help

If you have any issues or questions, please reach out to @bsseib or @bairdcm

Thank you for using Corporate RAG Assistant!
