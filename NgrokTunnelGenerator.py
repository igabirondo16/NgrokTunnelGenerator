import traceback
from pyngrok import ngrok, conf
import re
import sys

DEFAULT_PATH = "./../Juliet/credentials.yml"

def log_event_callback(log):
    print(str(log))

def open_tunnel():
    ssh_tunnel = ngrok.connect(5005, "http")

    conf.get_default().log_event_callback = log_event_callback
    
    for t in ngrok.get_tunnels():
        if "https" in t.public_url:
            tunnel = t.public_url

    with open(DEFAULT_PATH, "r+") as file:
        file_contents = file.read()
        text_pattern = re.compile('http[s]?://[A-Za-z0-9_-]*\.ngrok\.io', 0)
        file_contents = text_pattern.sub(tunnel, file_contents)
        file.seek(0)
        file.truncate()
        file.write(file_contents)
        file.close()

    print("Credentials.yml file updated")
    print("Ngrok server started at: " + tunnel)

    try:
        ngrok_process = ngrok.get_ngrok_process()
        print(ngrok_process)
        ngrok_process.proc.wait()

    except KeyboardInterrupt:
        ngrok.kill()
        print("Shutting down server at: " + str(tunnel))


def update_path():
    global DEFAULT_PATH
    DEFAULT_PATH = str(input("Select path of credentials.yml file: "))

def show_menu():
    print("NGROK TUNNEL OPENER")
    print("1) Update the path of credentials.yml file: ")
    print("2) Open tunnel for selected file")

if __name__ == "__main__":
    try: 
        show_menu()
        choice = int(input("Select your choice: "))
        if choice == 1:
            update_path()

        open_tunnel()

    except Exception as e:
        print(traceback.format_exc())
