import os
from openai import OpenAI
from PyPDF2 import PdfReader
from docx import Document
import colorama

# Initialize colorama
colorama.init()

# Initialize the OpenAI client
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")  # Ensure the API key is set in the environment
)

def extract_pdf_content(file_path):
    """Extracts text content from a PDF file."""
    try:
        reader = PdfReader(file_path)
        content = ""
        for page in reader.pages:
            content += page.extract_text()
        return content.strip()
    except Exception as e:
        return f"Error reading PDF file: {e}"

def extract_docx_content(file_path):
    """Extracts text content from a DOCX file."""
    try:
        document = Document(file_path)
        content = "\n".join([para.text for para in document.paragraphs])
        return content.strip()
    except Exception as e:
        return f"Error reading DOCX file: {e}"

def extract_txt_content(file_path):
    """Extracts text content from a TXT file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except Exception as e:
        return f"Error reading TXT file: {e}"

def get_document_content(file_path):
    """Determines file type and extracts content."""
    if file_path.endswith(".pdf"):
        return extract_pdf_content(file_path)
    elif file_path.endswith(".docx"):
        return extract_docx_content(file_path)
    elif file_path.endswith(".txt"):
        return extract_txt_content(file_path)
    else:
        return "Unsupported file type. Please upload a PDF, DOCX, or TXT file."

def query_openai(messages):
    """
    Send the messages to OpenAI and get a response.
    
    Note that the messages should be a list of dictionaries, where each
    dictionary has a "role" and a "content". The "role" should be either
    "system" or "user", and the "content" should be the message itself.
    
    The response is a dictionary with a single key, "choices". The value
    of this key is a list of dictionaries, each of which has a single key,
    "message". The value of this key is a dictionary with a single key,
    "content", which is the response text.
    """
    try:
        # The request to OpenAI
        response = client.chat.completions.create(
            # The list of messages to send to OpenAI
            messages=messages,
            # The model to use for generating the response
            model="gpt-4o",
            # The temperature to use for generating the response.
            # This controls how creative the response is.
            # A higher temperature will result in more creative
            # responses, but may also result in less accurate
            # responses.
            temperature=0.4
        )
        # Get the response text from the response
        return response.choices[0].message.content
    except Exception as e:
        # If there is an error, return an error message
        return f"Error querying OpenAI: {e}"

def summarize_document(content):
    """Generates a summary of the document using OpenAI."""
    messages = [
        {"role": "system", "content": "You are a helpful assistant that summarizes documents."},
        {"role": "user", "content": f"Summarize this document: {content}"}
    ]
    return query_openai(messages)

def main():
    """
    The main entry point of the chatbot. This function is responsible for
    running the chatbot in the console.
    """
    print(colorama.Fore.GREEN + "Welcome to the Multi-Purpose Chatbot!" + colorama.Style.RESET_ALL)
    print("You can upload a document (PDF, DOCX, or TXT) and ask questions about it, or just ask regular questions.")
    print("Commands: \n - 'upload': Upload a document.\n - 'exit': Quit the chatbot.\n")
    
    # The conversation history is a list of dictionaries. Each dictionary has a
    # "role" and a "content". The "role" should be either "system", "user", or
    # "assistant", and the "content" should be the message itself.
    conversation_history = [{"role": "system", "content": "You are a helpful assistant."}]
    
    # The contents of the document, if the user has uploaded one.
    document_content = None

    while True:
        # Get the user's input
        user_input = input(colorama.Fore.BLUE + "You: " + colorama.Style.RESET_ALL).strip()
        
        if user_input.lower() == "exit":
            # If the user has typed "exit", print a goodbye message and break out
            # of the loop.
            print(colorama.Fore.GREEN + "Chatbot: Goodbye!" + colorama.Style.RESET_ALL)
            break
        
        if user_input.lower() == "upload":
            # If the user has typed "upload", ask them for the file path of the
            # document, and then try to upload the document.
            file_path = input("Enter the file path of the document: ").strip()
            if not os.path.exists(file_path):
                # If the file doesn't exist, print an error message and continue
                # to the next iteration of the loop.
                print(colorama.Fore.GREEN + "Chatbot: File does not exist. Please check the path and try again." + colorama.Style.RESET_ALL)
                continue
            
            document_content = get_document_content(file_path)
            if document_content.startswith("Error") or "Unsupported" in document_content:
                # If there was an error uploading the document, print an error
                # message and continue to the next iteration of the loop.
                print(colorama.Fore.GREEN + f"Chatbot: {document_content}" + colorama.Style.RESET_ALL)
                document_content = None
                continue
            
            print(colorama.Fore.GREEN + "Chatbot: Document uploaded and processed successfully!" + colorama.Style.RESET_ALL)
            
            # If the user has uploaded a document, ask them if they want a summary
            # of the document.
            summarize_input = input("Would you like a summary of the document? (yes/no): ").strip().lower()
            if summarize_input in ["yes", "y"]:
                print(colorama.Fore.GREEN + "Chatbot: Generating summary..." + colorama.Style.RESET_ALL)
                # If the user wants a summary, generate one and print it.
                summary = summarize_document(document_content)
                print(colorama.Fore.GREEN + f"Chatbot: Summary:\n{summary}" + colorama.Style.RESET_ALL)
            else:
                print(colorama.Fore.GREEN + "Chatbot: Okay, you can now ask questions about the document." + colorama.Style.RESET_ALL)
            continue
        
        # Add the user's input to the conversation history
        conversation_history.append({"role": "user", "content": user_input})
        
        # If the user has uploaded a document, add the document content to the
        # conversation history.
        if document_content:
            conversation_history.append({"role": "user", "content": f"Document content: {document_content}"})
        
        # Ask OpenAI for a response to the user's input
        assistant_reply = query_openai(conversation_history)
        
        # Add the response to the conversation history
        conversation_history.append({"role": "assistant", "content": assistant_reply})
        # Print the response to the console
        print(colorama.Fore.GREEN + f"Chatbot: {assistant_reply}" + colorama.Style.RESET_ALL)

if __name__ == "__main__":
    main()