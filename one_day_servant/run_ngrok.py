from pyngrok import ngrok

# Connect ngrok to local Flask port 5000
url = ngrok.connect(5000)
print("Public URL:", url)

# Keep the script running so the tunnel stays alive
input("Press Enter to exit and stop ngrok...\n")
