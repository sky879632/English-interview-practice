from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
import PyPDF2
from docx import Document
import google.generativeai as genai
from dotenv import load_dotenv
import logging
import traceback
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'json'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
    logger.info(f"Created upload directory: {UPLOAD_FOLDER}")

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Configure Google Gemini API
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
    logger.error("GOOGLE_API_KEY not found in environment variables")
    raise ValueError("GOOGLE_API_KEY is required")

# Configure Gemini API
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize the model
try:
    # 使用之前测试通过的模型名称
    model = genai.GenerativeModel('gemini-1.5-pro')
    logger.info("Successfully initialized Gemini model")
except Exception as e:
    logger.error(f"Error initializing Gemini model: {str(e)}")
    logger.error(traceback.format_exc())
    raise

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(file_path):
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ''
            for page in reader.pages:
                text += page.extract_text()
        return text
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {str(e)}")
        logger.error(traceback.format_exc())
        raise

def extract_text_from_docx(file_path):
    try:
        doc = Document(file_path)
        text = ''
        for paragraph in doc.paragraphs:
            text += paragraph.text + '\n'
        return text
    except Exception as e:
        logger.error(f"Error extracting text from DOCX: {str(e)}")
        logger.error(traceback.format_exc())
        raise

def extract_text_from_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            
            # Extract all available fields
            text_parts = []
            
            # Basic Information
            if data.get('basics'):
                basics = data['basics']
                text_parts.append(f"Name: {basics.get('name', '')}")
                text_parts.append(f"Title: {basics.get('title', '')}")
                text_parts.append(f"Location: {basics.get('location', '')}")
                if basics.get('summary'):
                    text_parts.append(f"Summary: {basics['summary']}")
            
            # Contact Information
            if data.get('contact'):
                contact = data['contact']
                text_parts.append("\nContact Information:")
                for key, value in contact.items():
                    text_parts.append(f"{key}: {value}")
            
            # Experience
            if data.get('experience'):
                text_parts.append("\nExperience:")
                for exp in data['experience']:
                    text_parts.append(f"\nCompany: {exp.get('company', '')}")
                    text_parts.append(f"Position: {exp.get('position', '')}")
                    text_parts.append(f"Duration: {exp.get('startDate', '')} - {exp.get('endDate', '')}")
                    if exp.get('summary'):
                        text_parts.append(f"Summary: {exp['summary']}")
            
            # Skills
            if data.get('skills'):
                text_parts.append("\nSkills:")
                skills = data['skills']
                if isinstance(skills, list):
                    text_parts.append(", ".join(skills))
                elif isinstance(skills, dict):
                    for category, skill_list in skills.items():
                        text_parts.append(f"\n{category}:")
                        text_parts.append(", ".join(skill_list))
            
            # Education
            if data.get('education'):
                text_parts.append("\nEducation:")
                for edu in data['education']:
                    text_parts.append(f"\nInstitution: {edu.get('institution', '')}")
                    text_parts.append(f"Degree: {edu.get('degree', '')}")
                    text_parts.append(f"Field: {edu.get('field', '')}")
                    text_parts.append(f"Duration: {edu.get('startDate', '')} - {edu.get('endDate', '')}")
            
            # Projects
            if data.get('projects'):
                text_parts.append("\nProjects:")
                for project in data['projects']:
                    text_parts.append(f"\nProject: {project.get('name', '')}")
                    text_parts.append(f"Description: {project.get('description', '')}")
                    if project.get('technologies'):
                        text_parts.append(f"Technologies: {', '.join(project['technologies'])}")
            
            # Join all parts with newlines
            return "\n".join(text_parts)
            
    except Exception as e:
        logger.error(f"Error extracting text from JSON: {str(e)}")
        logger.error(traceback.format_exc())
        raise

@app.route('/api/upload-resume', methods=['POST'])
def upload_resume():
    try:
        logger.info("Received resume upload request")
        
        if 'file' not in request.files:
            logger.error("No file part in the request")
            return jsonify({'success': False, 'error': 'No file part'}), 400
        
        file = request.files['file']
        job_description = request.form.get('jobDescription', '')
        
        logger.info(f"File received: {file.filename}")
        logger.info(f"Job description received: {job_description[:100]}...")
        
        if file.filename == '':
            logger.error("No selected file")
            return jsonify({'success': False, 'error': 'No selected file'}), 400
        
        if not job_description.strip():
            logger.error("No job description provided")
            return jsonify({'success': False, 'error': 'Please provide a job description'}), 400
        
        if not allowed_file(file.filename):
            logger.error(f"Invalid file type: {file.filename}")
            return jsonify({'success': False, 'error': 'Invalid file type. Please upload a PDF, Word document, or JSON file.'}), 400
        
        try:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            logger.info(f"Saving file to: {filepath}")
            file.save(filepath)
            logger.info(f"File saved successfully at: {filepath}")
            
            # Extract text based on file type
            try:
                if filename.endswith('.pdf'):
                    logger.info("Extracting text from PDF")
                    text = extract_text_from_pdf(filepath)
                elif filename.endswith('.json'):
                    logger.info("Extracting text from JSON")
                    text = extract_text_from_json(filepath)
                else:
                    logger.info("Extracting text from DOCX")
                    text = extract_text_from_docx(filepath)
                
                if not text.strip():
                    logger.error("No text extracted from file")
                    return jsonify({'success': False, 'error': 'No text could be extracted from the file'}), 400
                
                logger.info(f"Successfully extracted text: {text[:100]}...")
            except Exception as e:
                logger.error(f"Error extracting text: {str(e)}")
                logger.error(traceback.format_exc())
                return jsonify({'success': False, 'error': f'Error extracting text: {str(e)}'}), 500
            
            try:
                # Generate interview content using Gemini
                prompt = f"""
                Based on the following resume and job description, generate a realistic interview scenario:

                Resume content: {text}

                Job Description: {job_description}

                Please provide:
                1. A brief introduction about the candidate and how their background aligns with the job requirements
                2. 5 relevant technical questions based on the job requirements and candidate's experience
                3. 3 behavioral questions that assess the candidate's fit for the role
                4. Expected answers for each question, including what to look for in the responses
                
                Format the response as JSON with the following structure:
                {{
                    "introduction": "string",
                    "technical_questions": ["string"],
                    "behavioral_questions": ["string"],
                    "expected_answers": {{
                        "technical": ["string"],
                        "behavioral": ["string"]
                    }}
                }}
                """
                
                logger.info("Generating interview content using Gemini")
                response = model.generate_content(prompt)
                
                if not response.text:
                    raise ValueError("Empty response from Gemini API")
                    
                interview_content = response.text
                
                # Remove markdown code block markers if they exist
                if interview_content.startswith('```json') and interview_content.endswith('```'):
                    interview_content = interview_content.replace('```json', '').replace('```', '').strip()
                
                # Ensure we have valid JSON
                try:
                    # Parse and re-stringify to ensure valid JSON
                    json_content = json.loads(interview_content)
                    interview_content = json.dumps(json_content)
                except json.JSONDecodeError:
                    logger.error(f"Invalid JSON in response: {interview_content[:100]}...")
                    return jsonify({'success': False, 'error': 'Received invalid JSON from AI service'}), 500
                
                logger.info("Successfully generated interview content")
                logger.info(f"Interview content preview: {interview_content[:100]}...")
                
                return jsonify({
                    'success': True,
                    'interview_content': interview_content
                })
                
            except Exception as e:
                logger.error(f"Error generating interview content: {str(e)}")
                logger.error(traceback.format_exc())
                return jsonify({'success': False, 'error': f'Error generating interview content: {str(e)}'}), 500
                
        except Exception as e:
            logger.error(f"Error saving file: {str(e)}")
            logger.error(traceback.format_exc())
            return jsonify({'success': False, 'error': f'Error saving file: {str(e)}'}), 500
            
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'success': False, 'error': f'Unexpected error: {str(e)}'}), 500

@app.route('/api/analyze-interview', methods=['POST'])
def analyze_interview():
    try:
        data = request.json
        question = data.get('question')
        expected_answer = data.get('expected_answer')
        candidate_response = data.get('candidate_response')
        
        if not all([question, expected_answer, candidate_response]):
            return jsonify({
                'success': False,
                'error': 'Missing required fields'
            }), 400
            
        prompt = f"""
        As an experienced interviewer, analyze the candidate's response to the following interview question:

        Question: {question}
        Expected Answer: {expected_answer}
        Candidate's Response: {candidate_response}

        Please provide feedback on:
        1. Content relevance and completeness
        2. Communication clarity and structure
        3. Areas of strength
        4. Areas for improvement
        5. Specific suggestions for better answers

        Format your response in a clear, constructive manner.
        """
        
        response = model.generate_content(prompt)
        feedback = response.text
        
        return jsonify({
            'success': True,
            'feedback': feedback
        })
        
    except Exception as e:
        logger.error(f"Error analyzing interview: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    logger.info("Starting Flask server...")
    app.run(debug=True, port=5001) 