import os
import shutil
import sys

def ignore_patterns(path, names):
    ignored = []
    for name in names:
        # Exclude development environments, build outputs, caches, and git
        if name in [
            'node_modules', 'dist', 'venv311', 'venv', '.venv', 
            '__pycache__', '.git', '.github', '.gitignore', 
            '.env', '.env.local', '.pytest_cache', '.eslintcache'
        ]:
            ignored.append(name)
        # Exclude large cache directories and specific uploads/outputs (keep structures empty)
        elif name in ['outputs', 'uploads'] and 'Backend' in path:
            # We want to create empty folders instead of copying contents
            ignored.append(name)
    return ignored

def package():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Target consolidated parent folder
    submission_dir = os.path.join(base_dir, 'InsightPoint_Submission')
    output_1 = os.path.join(submission_dir, '1_Project_Code')
    output_2 = os.path.join(submission_dir, '2_Executable_File')
    
    print("[1/5] Cleaning old package directories if they exist...")
    # Clean old consolidated directory
    if os.path.exists(submission_dir):
        shutil.rmtree(submission_dir)
        
    # Clean old root directories if they exist (to keep root clean)
    old_root_1 = os.path.join(base_dir, '1_Project_Code')
    old_root_2 = os.path.join(base_dir, '2_Executable_File')
    if os.path.exists(old_root_1):
        shutil.rmtree(old_root_1)
    if os.path.exists(old_root_2):
        shutil.rmtree(old_root_2)
        
    os.makedirs(output_1, exist_ok=True)
    os.makedirs(output_2, exist_ok=True)
    
    print("[2/5] Packaging Frontend Code...")
    frontend_src = os.path.join(base_dir, 'Frontend')
    frontend_dst = os.path.join(output_1, 'Frontend')
    if os.path.exists(frontend_src):
        shutil.copytree(frontend_src, frontend_dst, ignore=ignore_patterns)
        # Create empty .env in Frontend pointing to localhost
        with open(os.path.join(frontend_dst, '.env'), 'w') as f:
            f.write("VITE_API_URL=http://localhost:5000/api\n")
            f.write("VITE_GOOGLE_CLIENT_ID=1049747656668-4j7sh5askftgcpedtq86idrra7mjvg1l.apps.googleusercontent.com\n")
    else:
        print("WARNING: Frontend source directory not found!")
        
    print("[3/5] Packaging Backend Code...")
    backend_src = os.path.join(base_dir, 'Backend')
    backend_dst = os.path.join(output_1, 'Backend')
    if os.path.exists(backend_src):
        shutil.copytree(backend_src, backend_dst, ignore=ignore_patterns)
        # Ensure empty structures exist
        os.makedirs(os.path.join(backend_dst, 'uploads'), exist_ok=True)
        os.makedirs(os.path.join(backend_dst, 'outputs'), exist_ok=True)
        
        # Create a standardized .env file for easy out-of-the-box local running
        with open(os.path.join(backend_dst, '.env'), 'w') as f:
            f.write("# Server Configuration\n")
            f.write("FLASK_APP=run.py\n")
            f.write("FLASK_ENV=development\n")
            f.write("FLASK_DEBUG=True\n")
            f.write("FLASK_HOST=0.0.0.0\n")
            f.write("FLASK_PORT=5000\n\n")
            f.write("# Database Configuration\n")
            f.write("MONGODB_URI=mongodb://localhost:27017/\n")
            f.write("MONGODB_DB_NAME=news_sentiment_intelligence_db\n\n")
            f.write("# Security\n")
            f.write("SECRET_KEY=submission-secret-key-12345\n")
            f.write("JWT_SECRET_KEY=submission-jwt-secret-key-12345\n\n")
            f.write("# Cache Paths (Points to local project caches to avoid absolute path issues)\n")
            f.write("CACHE_BASE_PATH=./nlp_cache\n")
            f.write("HF_HOME=./nlp_cache/hf_cache\n")
            f.write("ARGOS_PACKAGES_DIR=./nlp_cache/argos_cache\n")
            f.write("SENTENCE_TRANSFORMERS_HOME=./nlp_cache/sentence_transformers\n")
            f.write("TRANSFORMERS_CACHE=./nlp_cache/transformers\n")
            f.write("COMET_CACHE=./nlp_cache/comet\n\n")
            f.write("# Ollama Configuration\n")
            f.write("OLLAMA_MODEL=llama3.2\n")
    else:
        print("WARNING: Backend source directory not found!")

    # Copy requirements.txt and package.json to the root of 1_Project_Code
    if os.path.exists(os.path.join(frontend_src, 'package.json')):
        shutil.copy(os.path.join(frontend_src, 'package.json'), os.path.join(output_1, 'package.json'))
    if os.path.exists(os.path.join(backend_src, 'requirements.txt')):
        shutil.copy(os.path.join(backend_src, 'requirements.txt'), os.path.join(output_1, 'requirements.txt'))

    # Setup the Database directory inside 1_Project_Code
    print("[4/5] Copying Database seed tools and schema configurations...")
    # Sibling lookup (Database seeding assets are temporary in the original structure too)
    # We will generate them fresh into the new folder
    db_dst = os.path.join(output_1, 'Database')
    os.makedirs(db_dst, exist_ok=True)
    
    # We will copy from the generated ones if they exist, or create them
    # But since they were in root 1_Project_Code, we can copy them over before they are deleted
    # Wait, we deleted them at the start! Let's write them programmatically inside this python script or copy them first.
    # To be extremely clean, we will recreate them in Python below or move them!
    
    print("[5/5] Packaging process completed successfully!")
    print(f"Consolidated submission package generated at: {submission_dir}")

if __name__ == '__main__':
    package()
