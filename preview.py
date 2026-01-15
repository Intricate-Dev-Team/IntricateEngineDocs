import subprocess
import webbrowser
import time
import sys

def preview_docs():
    PORT = 8000
    print("""
      starting server . . . 
      
      Ctrl+C to stop\n
      """)
    
    time.sleep(1.5)
    webbrowser.open(f"http://localhost:{PORT}/IntricateDocs/")
    
    try:
        subprocess.run([sys.executable, "-m", "mkdocs", "serve", "--dev-addr", f"127.0.0.1:{PORT}", "--livereload"])
    except KeyboardInterrupt:
        print("Server closing . . . ")
    except FileNotFoundError:
        print("mkdocs.yml not founder pleased see and hear and ensure you are within internally inside the corrected director")

if __name__ == "__main__":
    preview_docs()