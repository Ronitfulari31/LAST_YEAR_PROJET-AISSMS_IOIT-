import os
import sys
import subprocess
import time
import socket
import webbrowser
import signal

def is_node_installed():
    try:
        subprocess.run(['node', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except Exception:
        return False

def is_python_installed():
    try:
        subprocess.run(['python', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except Exception:
        return False

def is_mongo_running():
    # Attempt to ping localhost:27017
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2.0)
        s.connect(('localhost', 27017))
        s.close()
        return True
    except Exception:
        return False

def print_header():
    print("==================================================================")
    print("               InsightPoint AI News Intelligence Platform         ")
    print("                      Desktop Services Launcher                   ")
    print("==================================================================")

def main():
    print_header()
    
    # 1. Environment Verification
    print("Checking system prerequisites...")
    python_ok = is_python_installed()
    node_ok = is_node_installed()
    mongo_ok = is_mongo_running()
    
    print(f"- Python 3: {'[OK] Connected' if python_ok else '[WARNING] Not found in system PATH'}")
    print(f"- Node.js:  {'[OK] Connected' if node_ok else '[ERROR] Node.js is required to run the Frontend!'}")
    print(f"- MongoDB:  {'[OK] Running on localhost' if mongo_ok else '[INFO] Local MongoDB not running (Atlas URI or seeding may be used)'}")
    
    if not node_ok:
        print("\nERROR: Node.js is missing. Please install Node.js (v18+) and try again.")
        input("Press Enter to exit...")
        sys.exit(1)
        
    # Resolve Paths (navigate to sibling folder 1_Project_Code)
    # When compiled to EXE, sys.argv[0] is the EXE path
    launcher_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    project_root = os.path.dirname(launcher_dir)
    
    # Sibling directory check
    code_dir = os.path.join(project_root, '1_Project_Code')
    if not os.path.exists(code_dir):
        # Fallback to current directory for dev mode
        code_dir = os.path.join(launcher_dir, '1_Project_Code')
        if not os.path.exists(code_dir):
            code_dir = launcher_dir # Sibling/direct fallback
            
    backend_dir = os.path.join(code_dir, 'Backend')
    frontend_dir = os.path.join(code_dir, 'Frontend')
    
    if not os.path.exists(backend_dir) or not os.path.exists(frontend_dir):
        print("\nERROR: Could not locate 1_Project_Code folders!")
        print(f"Backend path: {os.path.abspath(backend_dir)}")
        print(f"Frontend path: {os.path.abspath(frontend_dir)}")
        input("Press Enter to exit...")
        sys.exit(1)

    print("\nStarting InsightPoint services...")
    
    # 2. Booting up Backend
    print("\n[1/3] Starting Backend Server (Flask on Port 5000)...")
    
    # Detect or build virtual environment
    venv_path = os.path.join(backend_dir, 'venv311')
    if not os.path.exists(venv_path):
        # Check standard venv fallback
        venv_path = os.path.join(backend_dir, 'venv')
        
    if os.path.exists(venv_path):
        python_executable = os.path.join(venv_path, 'Scripts', 'python.exe')
    else:
        print("INFO: No pre-configured virtual environment found in Backend. Creating a fresh one...")
        try:
            # Use 'python' instead of sys.executable to avoid compiled EXE infinite fork bomb
            subprocess.run(['python', '-m', 'venv', os.path.join(backend_dir, 'venv')], check=True)
            venv_path = os.path.join(backend_dir, 'venv')
            python_executable = os.path.join(venv_path, 'Scripts', 'python.exe')
            print("INFO: Installing backend dependencies silently from requirements.txt...")
            pip_executable = os.path.join(venv_path, 'Scripts', 'pip.exe')
            subprocess.run([pip_executable, 'install', '-r', os.path.join(backend_dir, 'requirements.txt')], check=True)
            print("SUCCESS: Virtual environment set up successfully!")
        except Exception as e:
            print(f"ERROR: Failed to automatically build virtual environment: {e}")
            print("Attempting fall back to system Python...")
            python_executable = 'python'

    backend_process = None
    try:
        backend_process = subprocess.Popen(
            [python_executable, 'run.py'],
            cwd=backend_dir,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0
        )
        print("Backend server started successfully in background.")
    except Exception as e:
        print(f"CRITICAL ERROR: Failed to start Backend: {e}")
        input("Press Enter to exit...")
        sys.exit(1)

    # 3. Booting up Frontend
    print("\n[2/3] Starting Frontend Server (Vite on Port 5173)...")
    
    # Check if node_modules is missing in packaged folder
    node_modules_path = os.path.join(frontend_dir, 'node_modules')
    if not os.path.exists(node_modules_path):
        print("INFO: node_modules folder is missing. Installing frontend packages silently...")
        try:
            subprocess.run(['npm', 'install'], cwd=frontend_dir, shell=True, check=True)
            print("SUCCESS: Frontend packages installed successfully!")
        except Exception as e:
            print(f"ERROR: Failed to run npm install: {e}")
            print("Vite may fail to boot.")

    frontend_process = None
    try:
        frontend_process = subprocess.Popen(
            ['npm', 'run', 'dev'],
            cwd=frontend_dir,
            shell=True,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0
        )
        print("Frontend Vite development server started successfully in background.")
    except Exception as e:
        print(f"CRITICAL ERROR: Failed to start Frontend: {e}")
        if backend_process:
            backend_process.terminate()
        input("Press Enter to exit...")
        sys.exit(1)

    # 4. Auto-launch Browser
    print("\n[3/3] Opening Dashboard in Default Web Browser...")
    time.sleep(3) # Wait for Vite and Flask to establish sockets
    webbrowser.open("http://localhost:5173")
    
    print("\n==================================================================")
    print(" SUCCESS: InsightPoint services are fully active!                  ")
    print("------------------------------------------------------------------")
    print(" - Frontend Dashboard: http://localhost:5173                      ")
    print(" - Backend API Server: http://localhost:5000/api                  ")
    print("==================================================================")
    print("\n[!] IMPORTANT: Keep this terminal window open to keep servers running.")
    print("    To stop both servers gracefully, press [Ctrl + C] or close this window.")
    
    try:
        # Keep launcher running to maintain background processes
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping InsightPoint services gracefully...")
        
        # Safe termination of processes on Windows
        if frontend_process:
            try:
                frontend_process.terminate()
                print("✓ Stopped Frontend server.")
            except Exception:
                pass
                
        if backend_process:
            try:
                backend_process.terminate()
                print("✓ Stopped Backend server.")
            except Exception:
                pass
                
        print("All processes stopped successfully. Goodbye!")
        time.sleep(1.5)

if __name__ == '__main__':
    main()
