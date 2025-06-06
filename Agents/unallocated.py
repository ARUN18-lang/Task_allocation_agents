import json
from datetime import datetime
import ast

def get_unallocated_members_json(allocated_data, all_members):
    """Generate JSON output for unallocated members"""
    if isinstance(all_members, str):
        all_members = ast.literal_eval(all_members)
    
    processed_members = [
        {
            "id": m[0],
            "name": m[1],
            "experience": m[2],
            "roles": [r.strip() for r in ''.join(m[3]).split(',')],
            "preference": m[4],
            "projects": m[5],
            "allocation_status": "unallocated"
        }
        for m in all_members
    ]
    
    allocated_ids = {m["id"] for role_mems in allocated_data.values() for m in role_mems}
    unallocated = [m for m in processed_members if m["id"] not in allocated_ids]
    
    return {
        "unallocated_members": unallocated,
        "count": len(unallocated),
        "generated_at": datetime.now().isoformat()
    }