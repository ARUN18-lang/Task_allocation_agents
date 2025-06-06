# Task Allocation Agents

## Overview

**Task Allocation Agents** is an innovative AI-powered system designed to automate and optimize the allocation of tasks and project roles to team members based on their experience, preferences, and project requirements. The platform utilizes advanced language models and database integration to match employees to roles efficiently, improving project success and resource utilization.

## Features

- **AI-Driven Task Allocation:** Uses large language models (LLMs) to analyze employee data and project requirements for optimal task and role assignments.
- **PDF Project Upload:** Project managers can upload PDF descriptions of new projects, which are then parsed for relevant information.
- **Automated Role Extraction:** The system automatically extracts roles from project requirements and matches them to available team members.
- **Experience & Preference Matching:** Allocates tasks based on team members' experience, skills, preferences, and current workload.
- **Interactive Approval Workflow:** Managers can approve or reject suggested allocations via the web interface.
- **Unallocated Member Reporting:** Generates reports for members who could not be allocated to any role.
- **Modern Web Interface:** Built with Flask and Bootstrap for a responsive and user-friendly experience.

## Tech Stack

- **Backend:** Python, Flask, LangChain, MySQL
- **Frontend:** HTML5, Bootstrap, JavaScript
- **AI/LLM:** NVIDIA Llama 3.1 via LangChain
- **PDF Parsing:** PyPDF2
- **Other:** dotenv, pandas

## Project Structure

```
Agents/
  model.py            # LLM integration (NVIDIA)
  sql_agent.py        # Database access and SQL utilities
  task_agent.py       # Core logic for task allocation
  unallocated.py      # Reporting for unallocated members
  utils.py            # Utility functions (API keys, etc.)
frontend/
  static/
    script.js         # Frontend logic (file upload, approval/rejection)
    styles.css        # Custom styles
  templates/
    index.html        # Landing page
    login.html        # Login for project managers/employees
    upload.html       # Project PDF upload
    task_allocation.html # Allocation results and approval
requirements.txt      # Python dependencies
```

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ARUN18-lang/Task_allocation_agents.git
   cd Task_allocation_agents
   ```

2. **Set up Python environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   - Create a `.env` file in the root directory.
   - Add your NVIDIA and GROQ API keys:
     ```
     NVIDIA_API_KEY=your_nvidia_api_key
     GROQ_API_KEY=your_groq_api_key
     ```

5. **Configure MySQL Database:**
   - Update the connection details in `Agents/engine.py` (host, user, password, database).
   - Ensure your employee records are present in the expected schema.

6. **Run the application:**
   ```bash
   flask run
   ```
   Access the app at [http://localhost:5000](http://localhost:5000)

## Usage

1. **Login:** Start as a Project Manager or Employee.
2. **Upload Project:** Managers upload a PDF describing the project requirements.
3. **Review Allocations:** The AI system processes the project and team data, recommending optimal allocations.
4. **Approve/Reject:** Managers interactively approve or reject allocations.
5. **Proceed:** Finalize allocations and generate reports.

## Contributing

Contributions are welcome! Please fork this repository, submit pull requests, and open issues for bugs/feature requests.

## License

[MIT License](LICENSE)

## Acknowledgements

- [LangChain](https://github.com/langchain-ai/langchain)
- [NVIDIA AI Endpoints](https://integrate.api.nvidia.com)
- [Bootstrap](https://getbootstrap.com/)

---

*Empower your project teams with AI-driven task allocation!*
