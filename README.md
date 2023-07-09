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
git clone https://github.com/andyshahbazian/LLM.git
```


3. Update the URL on line 13 and 15 of scrapy/kb/kb/spiders/knowledge_base.py to be your companies parent knowledge base index URL. Something like this for line 14 https://docs.aws.amazon.com/index.html where downstream links are aggregated and this for line 13 docs.aws.amazon.com.

4. From terminal, execute scrapy crawl kb from the scrapy/kb/ directory. This may take a while to complete, so feel free to stop the crawler after ~10mins or enough files are collected.

   ```
   scrapy crawl kb
   ```
if you get this error: 
╔══════════════════════════════════════════════════════╗
║ Host system is missing dependencies to run browsers. ║
║ Please install them with the following command:      ║
║                                                      ║
║     sudo playwright install-deps                     ║
║                                                      ║
║ Alternatively, use apt:                              ║
║     sudo apt-get install libgbm1\                    ║
║         libasound2                                   ║
║                                                      ║
║ <3 Playwright Team                                   ║
╚══════════════════════════════════════════════════════╝

then dont use sudo - (make sure you have the latest nvm)  use this instead : sudo will use a different vnm
```
playwright install-deps
```
if you get this error: 
how can I fix this: You are running Node.js 12.22.9.
Playwright requires Node.js 14 or higher. 
Please update your version of Node.js.


then To fix the issue, you need to update your Node.js version to meet the minimum requirement of Playwright (Node.js 14 or higher). Here's how you can do it:

Uninstall existing Node.js:
If you have an older version of Node.js installed, it's recommended to uninstall it first. The process to uninstall Node.js depends on your operating system. You can refer to the official Node.js documentation or use the appropriate method for your system.

Install Node Version Manager (NVM):
Node Version Manager (NVM) is a tool that allows you to manage multiple Node.js versions on your system. Install NVM by following the instructions specific to your operating system from the official NVM repository: https://github.com/nvm-sh/nvm

Install Node.js 14:
Once you have NVM installed, open a new terminal and run the following command to install Node.js 14:

```
nvm install 14

```

his command will install Node.js version 14.x.x on your system.

Set Node.js 14 as the default version:
To make Node.js 14 the default version on your system, run the following command:

```
nvm alias default 14
```

This command sets Node.js 14 as the default version to be used in new terminal sessions.

Verify the Node.js version:
To ensure that the Node.js version is updated successfully, run the following command:
```
node --version
```

It should output a version that starts with v14.x.x, indicating that Node.js 14 is now installed and active.

After updating Node.js to version 14, you should be able to use Playwright without encountering the version mismatch error.

if you get this error:getting this errot: Command 'nvm' not found, did you mean:

Close and reopen your terminal:
Sometimes, the changes made during the NVM installation process may not take effect immediately. Closing and reopening your terminal can help ensure that NVM is loaded properly.

Verify NVM installation:
After reopening your terminal, run the following command to check if NVM is installed correctly:

```
command -v nvm
```

how to fix this: Unsupported engine for playwright@1.35.1: wanted: {"node":">=16"} (current: {"node":"14.21.3","npm":"6.14.18"})
ChatGPT
The error message "Unsupported engine for playwright" indicates that the current version of Node.js installed on your system is not compatible with the version of Playwright you are trying to use.

To resolve this issue, you have two options:

Update Node.js:
The error message suggests that the minimum required version of Node.js for Playwright is Node.js 16 or higher. You can update your Node.js version to meet this requirement. Here's how you can do it:

Install Node Version Manager (NVM) if you haven't already. Follow the installation instructions specific to your operating system from the official NVM repository: https://github.com/nvm-sh/nvm

Use NVM to install Node.js version 16:

Copy code
nvm install 16
Set Node.js 16 as the default version:

csharp
Copy code
nvm alias default 16
Close and reopen your terminal to ensure the changes take effect.

Use a compatible Playwright version:
If you prefer not to update Node.js, you can try using a different version of Playwright that is compatible with your current Node.js version. You can install a specific version of Playwright using npm:

css
Copy code
npm install playwright@1.15.0
Replace 1.15.0 with a version that is compatible with your installed Node.js version. You can check the Playwright documentation or release notes to find the compatible version for your Node.js version.

By either updating Node.js or using a compatible Playwright version, you should be able to resolve the "Unsupported engine for playwright" error and use Playwright successfully.





User

still getting this wrror: 
ChatGPT
Apologies for the inconvenience. If you are still encountering the error message after updating Node.js or using a compatible Playwright version, there could be a couple of potential causes and solutions to consider:

Clear npm cache:
Sometimes, the error can be due to a cached version mismatch. Try clearing the npm cache by running the following command:

bash
Copy code
npm cache clean --force
After clearing the cache, attempt to install Playwright again with the appropriate version.

Reinstall npm:
It's possible that the npm installation itself might be causing the issue. You can try reinstalling npm using the following command:

bash
Copy code
npm install -g npm
This command will update npm to the latest version. Once npm is reinstalled, attempt to install Playwright again.

Check for conflicting installations:
Ensure that there are no conflicting installations of Node.js or npm on your system. Multiple installations can sometimes lead to compatibility issues. Verify that you are using the correct Node.js installation and that npm is associated with that version.

If none of the above solutions resolve the issue, it might be helpful to provide more specific details about the steps you followed, the exact error message you are encountering, and any additional information that could assist in troubleshooting the problem.





User
You are running Node.js 12.22.9.
Playwright requires Node.js 14 or higher. 
Please update your version of Node.js.
ChatGPT
Apologies for the confusion. It appears that the Node.js version installed on your system is still not updated to meet the minimum requirement of Playwright (Node.js 14 or higher). To resolve this issue, you need to update your Node.js version. Here's how you can do it:

Update Node.js:
There are different methods to update Node.js depending on the platform you are using. Here are a few common approaches:

a. Using a package manager (recommended):

For Linux/macOS: Use a package manager like nvm or n to manage Node.js versions. You can follow the installation instructions provided by the respective package manager's documentation.
b. Manual installation:

Visit the official Node.js website (https://nodejs.org) and download the latest LTS (Long Term Support) version for your operating system.
Run the installer and follow the prompts to update Node.js on your system.
Verify the Node.js version:
After updating Node.js, open a new terminal and run the following command to verify that the version has been updated:

bash
Copy code
node --version
It should now display a version starting with v14.x.x, indicating that Node.js 14 or higher is installed.

Once you have updated Node.js to version 14 or higher, you should be able to use Playwright without encountering the version mismatch error.





User
node version is 16 but when using  sudo playwright install-deps    it shows I am using node 12
ChatGPT
If you have updated your Node.js version to 16, but the command sudo playwright install-deps still shows that you are using Node.js 12, it indicates that the system-level sudo command is still using the older version of Node.js.

To resolve this issue, you can try the following steps:

Check the sudo version of Node.js:
Run the following command to check the version of Node.js that sudo is using:

bash
Copy code
sudo node --version
If it displays v12.x.x, it confirms that the sudo command is still associated with the older version of Node.js.

Update the sudo configuration:
To update the sudo configuration to use the newer version of Node.js, you can try the following steps:

a. Open a terminal and run the following command to open the sudoers file in a text editor with administrative privileges:

bash
Copy code
sudo visudo
b. Within the sudoers file, look for a line that starts with Defaults env_keep += "PATH". If you find it, add the path to the newer version of Node.js to the env_keep directive. For example:

arduino
Copy code
Defaults env_keep += "PATH:/path/to/new/node"
Replace /path/to/new/node with the actual path to the directory where Node.js 16 is installed.

c. Save the changes and exit the text editor.

Retry the installation command:
After updating the sudo configuration, try running the sudo playwright install-deps command again. It should now use the updated Node.js version.

By updating the sudo configuration to use the newer version of Node.js, you should be able to resolve the issue and successfully install Playwright dependencies.





User
how can I find the path to the newer node 
ChatGPT
To find the path to the newer version of Node.js that you have installed, you can try the following methods:

Use the which command:
Open a terminal and run the following command:

bash
Copy code
which node
This command will display the path to the currently active node executable. If you have multiple versions of Node.js installed, it should point to the one that is being used.

Check the Node.js installation directory:
By default, Node.js is installed in a specific directory. You can check the installation directory to find the path to the newer version. The exact location may vary depending on your operating system and installation method.

For Linux/macOS: The default installation directory for Node.js is /usr/local/bin/node. You can check this directory to find the path.

For Windows: The default installation directory is usually C:\Program Files\nodejs. You can navigate to this directory to find the path.

Use the nvm command (if applicable):
If you have installed Node.js using Node Version Manager (NVM), you can use the nvm command to find the path to the installed version. Run the following command:

bash
Copy code
nvm which <node-version>
Replace <node-version> with the version number of the newer Node.js version (e.g., 16 or 14.17.6). This command will display the path to the specified Node.js version.

Once you have found the path to the newer Node.js version, you can use it to update the sudo configuration or specify the path when running commands that require the newer Node.js version.





User
should I use the whole path :/home/ubuntu/.nvm/versions/node/v16.20.1/bin/node
ChatGPT
If you have installed Node.js using Node Version Manager (NVM) and the path to the newer Node.js version is /home/ubuntu/.nvm/versions/node/v16.20.1/bin/node, you can use that path to specify the newer Node.js version when running commands that require it.

When using the full path to the Node.js executable, make sure to include it in the command as follows:

bash
Copy code
/home/ubuntu/.nvm/versions/node/v16.20.1/bin/node <command>
Replace <command> with the actual command you want to run, such as npm, npx, or any other Node.js-related command.

Using the full path ensures that the specific version of Node.js you want to use is executed. This can be particularly helpful when you have multiple versions of Node.js installed and need to explicitly specify which version to use for a specific task or command.





User
I added this Defaults env_keep += "PATH:/path/to/new/node" but still get version 12
ChatGPT
If you have added the Defaults env_keep += "PATH:/path/to/new/node" line to the sudoers file and are still experiencing the issue where the sudo command continues to use Node.js version 12, there are a few additional steps you can try:

Confirm the changes in the sudoers file:
Double-check that you have saved the changes made to the sudoers file correctly. Ensure that there are no typos or syntax errors in the added line. Save the file and exit the text editor.

Refresh sudo:
Run the following command to reload the sudo configuration and apply the changes:

bash
Copy code
sudo -k
This command clears the cached credentials for sudo, forcing it to read the updated sudoers file.

Test the sudo command:
Run a simple sudo command, such as sudo node --version, to check if the updated Node.js version is now being used. If the correct version is displayed, the configuration has been successfully updated.

Check the user's sudo privileges:
Ensure that the user account you are using has the necessary sudo privileges. Verify that the account is listed in the sudoers file and has the appropriate permissions.

If the issue persists after following these steps, you might consider alternative methods to execute the desired commands without using sudo, such as running the commands as the current user or using a package manager that does not require sudo permissions.
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
