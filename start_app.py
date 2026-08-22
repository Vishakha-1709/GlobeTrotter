"""
GlobeTrotter One-Click Launcher
Automatically starts the FastAPI server and opens the web application in your browser!
"""

import webbrowser
import threading
import time
import uvicorn


def open_browser():
    # Wait 1.5 seconds for the server to boot up, then open Chrome/Edge
    time.sleep(1.5)
    print("\n🌍 Opening GlobeTrotter web app in your browser at http://localhost:8000 ...")
    webbrowser.open("http://localhost:8000")


if __name__ == "__main__":
    print("=======================================================")
    print("   🚀 Starting GlobeTrotter Full-Stack Application     ")
    print("=======================================================")
    
    # Launch browser opener in a background thread
    threading.Thread(target=open_browser, daemon=True).start()

    # Start the server
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
