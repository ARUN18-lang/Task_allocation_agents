from flask import Flask, request, render_template, jsonify
import os
import sys
from werkzeug.utils import secure_filename


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from Agents.task_agent import generate_report
from Agents.skill_agent import pdf_to_text_pypdf2, get_roles  
from Agents.sql_agent import get_members_from_table, get_all_members_direct


app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':
        return render_template('upload.html')
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"})
    
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    try:
        query = pdf_to_text_pypdf2(filepath)
        roles = get_roles(query)
        members, sql_query = get_members_from_table(query)
        all_members_list = get_all_members_direct()
        report = generate_report(members, sql_query, all_members_list)
        #os.remove(filepath)
    except Exception as e:
        return jsonify({"error": str(e)})
    
    return jsonify({"message": "File uploaded successfully", "report": report})

@app.route('/dashboard')
def dashboard():
    return render_template('task_allocation.html')

if __name__ == '__main__':
    app.run(debug=True)