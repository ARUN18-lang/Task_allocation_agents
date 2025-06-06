from langchain_community.utilities import SQLDatabase
from Agents.model import get_model
from langchain_core.prompts import ChatPromptTemplate
from Agents.skill_agent import get_roles
from urllib.parse import quote_plus
from tabulate import tabulate
import ast

llm = get_model()

class Roles:
    def __init__(self, query):
        self.roles = get_roles(query)  

    def get_roles(self):
        return self.roles  
    

def connect_database(username, port, host, password, database):
    encoded_password = quote_plus(password)
    mysql_uri = f"mysql+mysqlconnector://{username}:{encoded_password}@{host}:{port}/{database}"
    
    try:
        db = SQLDatabase.from_uri(mysql_uri)
        print("✅ Connected to MySQL Database")
        return db
    except Exception as e:
        print(f"❌ Database Connection Failed: {e}")
        return None

def run_query(query, db):
    if db:
        try:
            return db.run(query)
        except Exception as e:
            return f"❌ Query Execution Failed: {e}"
    return "❌ Please connect to the database"


def get_database_schema(db):
    if db:
        try:
            return db.get_table_info()
        except Exception as e:
            return f"❌ Error retrieving schema: {e}"
    return "❌ Please connect to the database"

def get_query_from_llm(roles, db):
    if not roles:
        print("❌ No roles found before passing to LLM")
        return "❌ Invalid input: No roles provided."
    
    schema = get_database_schema(db)
    if not schema:
        print("❌ Failed to retrieve database schema")
        return "❌ Invalid input: Unable to retrieve database schema."
    
    print(f"🔍 Database Schema:\n{schema}")

    template = """
        Below is the schema of a MySQL database. Read the schema carefully.

        {schema}

        Based on the following job roles, generate an SQL query to retrieve all columns of members who match these roles.

        Job Roles:
        {roles}

        Please return only the SQL query.
    """

    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | llm

    response = chain.invoke({"roles": ", ".join(roles), "schema": schema}).content.strip()
    response = response.replace("```sql", "").replace("```", "").strip()

    print(f"✅ Generated SQL Query:\n{response}")
    return response

def get_members_from_table(query):
    db = connect_database("root", 3306, "127.0.0.1", "Arun@mysql2004", "empdb")

    roles_instance = Roles(query)
    roles_list = roles_instance.get_roles()

    if roles_list:
        sql_query = get_query_from_llm(roles_list, db)
        result = run_query(sql_query, db)
        if result:
            return result, sql_query
        else:
            return f"No matching records found!"
    else:
        return f"❌ No roles found. Cannot generate SQL query."
    
    
def get_all_members_direct():
    """Directly fetches all members from database with proper column names"""
    db = connect_database("root", 3306, "127.0.0.1", "Arun@mysql2004", "empdb")
    if not db:
        return None, "❌ Database connection failed"
    
    query = """
    SELECT 
        `Member ID`, 
        `Name`, 
        `Experience (Years)`, 
        `Roles`, 
        `Preferences`, 
        `Projects`
    FROM employeerecords
    ORDER BY `Experience (Years)` DESC
    """
    
    try:
        result = db.run(query)
        if not result:
            return None, "No members found in database"
        return result
    except Exception as e:
        return None, f"Query failed: {str(e)}"
    


#print("all_members_list" ,all_members_list)

