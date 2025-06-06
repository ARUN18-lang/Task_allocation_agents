from Agents.model import get_model
#from Agents.sql_agent import members, sql_query,all_members_list
from langchain_core.prompts import PromptTemplate
from Agents.unallocated import get_unallocated_members_json
import ast
import re
import json
from datetime import datetime

llm = get_model()

def allocate_members_workload(roles, members_list):
    """
    Allocates members to multiple roles while ensuring fair distribution.
    Args:
        roles: List of job roles
        members_list: List of member dictionaries
    Returns:
        Dictionary with role-wise assigned members
    """
    if not isinstance(members_list, list):
        raise ValueError("Error: members should be a list")
    
    members_sorted = sorted(members_list, 
                          key=lambda x: (-x['experience'], x['projects']))
    
    role_allocations = {role: [] for role in roles}
    assigned_members = set()

    for member in members_sorted:
        if member['preferences'] in member['roles'] and member['preferences'] in roles:
            role = member['preferences']
            role_allocations[role].append(member)
            assigned_members.add(member['id'])
    
    for member in members_sorted:
        if member['id'] not in assigned_members:
            for role in roles:
                if role in member['roles']:
                    role_allocations[role].append(member)
                    assigned_members.add(member['id'])
                    break
    
    for role in roles:
        if not role_allocations[role]:
            for member in members_sorted:
                if member['id'] not in assigned_members:
                    role_allocations[role].append(member)
                    assigned_members.add(member['id'])
                    break
    
    return role_allocations

def extract_roles_from_sql(query):
    """Extracts role names from SQL WHERE clause"""
    try:
        print(f"🔍 Extracting roles from query:\n{query}")
        
        patterns = [
            r"`?Roles`? REGEXP '([^']*)'",  
            r"`?Roles`? LIKE '%(.*?)%'", 
        ]
        
        roles = []
        for pattern in patterns:
            matches = re.findall(pattern, query, re.IGNORECASE)
            for match in matches:
                extracted_roles = [role.strip() for role in match.split('|')]
                roles.extend(extracted_roles)
        
        print(f"✅ Extracted Roles: {roles}")
        return list(set(filter(None, roles)))
    
    except Exception as e:
        print(f"❌ Error extracting roles: {e}")
        return []


def get_allocated_members_for_model(members, sql_query):
    """Processes members data and returns role allocations"""
    try:
        if isinstance(members, str):
            members = ast.literal_eval(members)
        
        print(f'Number of members: {len(members)}')
        
        keys = ["id", "name", "experience", "roles", "preferences", "projects"]
        members_list = []
        
        for values in members:
            try:
                member_dict = dict(zip(keys, values))
                roles_str = (''.join(member_dict["roles"]) 
                           if isinstance(member_dict["roles"], list) 
                           else str(member_dict["roles"]))
                member_dict["roles"] = [r.strip() for r in roles_str.split(',')]
                members_list.append(member_dict)
            except Exception as e:
                print(f"Error processing member {values[:3]}: {e}")
        
        roles = extract_roles_from_sql(sql_query)
        print(f"Extracted roles: {roles}")
        
        if not roles:
            raise ValueError("No roles found in SQL query")
            
        return allocate_members_workload(roles, members_list)
        
    except Exception as e:
        print(f"Error in allocation: {e}")
        return {}

def format_allocated_data_json(allocated_data):
    """Formats allocation data into JSON structure"""
    if not allocated_data:
        return {"error": "No allocation data available"}
    
    output = {
        "allocations": [],
        "total_allocated_members": 0,
        "generated_at": datetime.now().isoformat()
    }
    
    allocated_ids = set()
    
    for role, members in allocated_data.items():
        role_data = {
            "role": role,
            "count": len(members),
            "members": []
        }
        
        for member in members:
            allocated_ids.add(member['id'])
            role_data["members"].append({
                "id": member['id'],
                "name": member['name'],
                "experience": member['experience'],
                "roles": member['roles'],
                "preference": member['preferences'],
                "projects": member['projects'],
                "allocation_score": round(member['experience'] * 0.6 + (10 - member['projects']) * 0.4, 2)
            })
        
        output["allocations"].append(role_data)
    
    output["total_allocated_members"] = len(allocated_ids)
    
    return output

def generate_llm_json_report(allocated_data):
    """Generate JSON report using LLM without statistics"""
    structured_data = format_allocated_data_json(allocated_data)
    
    prompt_template = """Please format this team allocation data into clean JSON:
    {{
      "allocations": [
        {{
          "role": "role_name",
          "count": number,
          "members": [
            {{
              "id": number,
              "name": "string",
              "experience": number,
              "roles": ["list"],
              "preference": "string",
              "projects": number
            }}
          ]
        }}
      ],
      "generated_at": "timestamp"
    }}

    Input Data:
    {input_data}

    Rules:
    1. Return ONLY valid JSON
    2. No additional text/comments
    3. Maintain all original data
    4. Do NOT include any statistics
    """

    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=['input_data']
    )

    try:
        input_str = json.dumps(structured_data, indent=2)
        response = llm.invoke(prompt.format(input_data=input_str))
        
        json_str = response.content if hasattr(response, 'content') else str(response)
        json_str = json_str.strip()
        
        if json_str.startswith("```json"):
            json_str = json_str[7:].rstrip("```").strip()
        elif json_str.startswith("```"):
            json_str = json_str[3:].rstrip("```").strip()
        
        parsed = json.loads(json_str)
        
        if "statistics" in parsed:
            del parsed["statistics"]
            
        return json.dumps(parsed, indent=2)
        
    except json.JSONDecodeError:
        if "statistics" in structured_data:
            del structured_data["statistics"]
        return json.dumps(structured_data, indent=2)
    except Exception as e:
        print(f"Error generating report: {e}")
        return json.dumps({"error": str(e)}, indent=2)

def generate_report(members, sql_query, all_members_list):
    allocated_data = get_allocated_members_for_model(members, sql_query)
    if not allocated_data:
        print("Failed to allocate members")
        return
    
    allocated_json_report = generate_llm_json_report(allocated_data)
    try:
        with open('team_allocation_llm_report.json', 'w', encoding='utf-8') as f:
            if isinstance(allocated_json_report, str):
                f.write(allocated_json_report)
            else:
                f.write(json.dumps(allocated_json_report, indent=2))
    except Exception as e:
        print(f"Error writing allocated report: {e}")
    
    unallocated_json_report = get_unallocated_members_json(allocated_data, all_members_list)
    try:
        with open('team_unallocation_llm_report.json', 'w', encoding='utf-8') as f:
            if isinstance(unallocated_json_report, str):
                f.write(unallocated_json_report)
            else:
                f.write(json.dumps(unallocated_json_report, indent=2))
    except Exception as e:
        print(f"Error writing unallocated report: {e}")
    
    return "Successfully generated both allocation reports"
