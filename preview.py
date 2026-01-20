import subprocess
import webbrowser
import time
import sys
import socket



def GetAvailablePort(StartPort=8000):
    port = StartPort
    while port < StartPort + 100:  
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(('127.0.0.1', port))
            sock.close()
            return port
        except OSError:
            port += 1 
    
    return StartPort


def PreviewDocs():
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
        print("mkdocs.yml not founder pleased see and hear and ensures you are within internally inside the corrected directorate")

if __name__ == "__main__":
    PreviewDocs()