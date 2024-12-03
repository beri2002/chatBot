# Chatbot Setup Guide

Welcome to the Chatbot project! This guide will help you set up and run the chatbot application that supports regular prompts and document-based queries.

## Prerequisites

1. **Python 3.7 or above**: Ensure Python is installed on your system.
2. **pip**: Ensure pip is installed for managing Python packages.

## Installation Steps

### 1. Install Dependencies

Use the `requirements.txt` file to install the necessary Python packages.

```bash
pip install -r requirements.txt
```

### 2. Set Up OpenAI API Key

The chatbot requires an OpenAI API key to function. Export your API key as an environment variable:

**Linux/macOS**:

```bash
export OPENAI_API_KEY="your_openai_api_key_here"
```

**Windows** (Command Prompt):

```cmd
set OPENAI_API_KEY=your_openai_api_key_here
```

Replace `your_openai_api_key_here` with your actual API key obtained from the [OpenAI website](https://platform.openai.com/).

## Running the Chatbot

Run the chatbot script using Python:

```bash
python3 chatbot.py
```

## Features

- **Regular Chat**: Ask any question or prompt without uploading a document.
- **Document Querying**: Upload a document (PDF, TXT, or DOCX) to extract content and ask questions based on the document.
- **Document Summarization**: Automatically summarize uploaded documents upon request.

## Supported File Types

- PDF
- DOCX
- TXT

## Troubleshooting

- **Missing API Key**: Ensure the OpenAI API key is set correctly as an environment variable.
- **Dependency Issues**: Reinstall dependencies with:
  ```bash
  pip install --force-reinstall -r requirements.txt
  ```
- **Unsupported File Types**: Only PDF, DOCX, and TXT files are supported.

## Contact

If you encounter issues or have suggestions, feel free to reach out to the project maintainer.
