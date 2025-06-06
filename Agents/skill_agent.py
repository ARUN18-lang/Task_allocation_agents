from pydantic import BaseModel, Field
from Agents.model import get_model
from Agents.data import get_available_roles
from PyPDF2 import PdfReader


class RolesGeneratorResponse(BaseModel):
    roles: list[str] = Field(description="List of roles for the job.")

custom_prompt = """
    You are an AI-powered career advisor with knowledge of relevant job roles based on the given database.  
    Extract only the most relevant job roles from the database that match the following project description.  
    Return the roles in a numbered list format.

    ### Available Roles:
    {roles_db}  

    ### Project Description:
    {input}

    ### Output Format:
    1. Role 1  
    2. Role 2  
    ...
"""


llm = get_model()

def get_roles(query: str) -> list[str]:
    roles_db = get_available_roles()
    try:
        response = llm.invoke(custom_prompt.format(input=query, roles_db=roles_db))
        print("Raw LLM response:", response)
        if hasattr(response, "content"):
            response_text = response.content.strip().split("\n")
        else:
            raise ValueError("Unexpected response format from LLM")
    except Exception as e:
        print(f"Error invoking LLM: {e}")
        return []  
    roles = []
    for line in response_text:
        line = line.strip().replace("**", "")
        if line and line[0].isdigit():
            role = line.split(". ", 1)[-1]
            roles.append(role)
    return roles

def pdf_to_text_pypdf2(pdf_path):
    """
    Extracts text from a PDF file.
    """
    text = ""
    try:
        with open(pdf_path, 'rb') as pdf_file:
            reader = PdfReader(pdf_file)
            for page in reader.pages:
                text += page.extract_text() + "\n"
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text




