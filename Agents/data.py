import pandas as pd

def get_available_roles():
    file_path = "C:\\Users\\arun5\\Desktop\\Honeywell\\Agents\\task_allocation_modified.csv"
    try:
        df = pd.read_csv(file_path)

        if 'Roles' not in df.columns:
            raise KeyError(f"'Roles' column not found in {file_path}")

        roles_set = set()
        for roles in df['Roles'].dropna():
            roles_list = [role.strip() for role in roles.split(',')]
            roles_set.update(roles_list)

        return ', '.join(roles_set)

    except Exception as e:
        print(f"Error: {e}")
        return set()

