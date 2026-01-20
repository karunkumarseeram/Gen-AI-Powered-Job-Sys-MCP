import fitz
import os
from openai import OpenAI
from dotenv import load_dotenv
from apify_client import ApifyClient
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY


client = OpenAI(api_key=OPENAI_API_KEY)
apify_client = ApifyClient(os.getenv("APIFY_API_TOKEN"))

def extract_text_from_pdf(uploaded_file):
    """
    Extracts text from a PDF file.
    
    Args:
        uploaded_file (file-like object): The uploaded PDF file object.
        
    Returns:
        str: The extracted text.
    """
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text


def ask_openai(prompt, max_tokens = 500):
    """
        Send a prompt to the OpenAI API and return the response
    

    Args:
        prompt (str): The prompt to send to the openai API
        model (str): The model to use for the request

        temperature (float): The temp for the response
        
    Return:
        str: The response from the OpenAI API.
    """
    
    response = client.chat.completions.create(
        model= "gpt-4o",
        messages=[
            {
                "role":"user",
                "content": prompt
                }
        ],
        temperature=0.5,
        max_tokens=max_tokens
    )
    
    return response.choices[0].message.content

def fetch_likedin_jobs(search_query,location="india",rows=30):
    run_input = {
        "keyword": search_query,
        "maxJobs": 30,
        "freshness":"all",
        "sortBy":"relevance",
        "experience":"all"
    }
    # Run the Actor and wait for it to finish
    run = apify_client.actor("BHzefUZlZRKWxkTck").call(run_input=run_input)
    jobs = list(apify_client.dataset(run["defaultDatasetId"]).iterate_items())
    return jobs

def fetch_naukri_jobs(search_query,location="india",rows=30):
    pass    