import requests
import time
import json

config_file = 'config.json'

def save_config(token, channel, author):
    config = {
        'Token': token,
        'Channel': channel,
        'Author': author
    }
    with open(config_file, 'w') as file:
        json.dump(config, file)

def load_config():
    with open(config_file, 'r') as file:
        config = json.load(file)
    token = config['Token']
    channel = config['Channel']
    author = config['Author']
    return token, channel, author

load_new_config = input("Do you want to load a new config? (Y/N): ")
if load_new_config.lower() == 'y':
    token = input("[!] Enter Discord Token: ")
    channel = input("[!] Enter A Channel ID: ")
    author_input = input("[!] Your User ID: ")
    save_config(token, channel, author_input)
else:
    token, channel, author_input = load_config()


# Set the variables
headers = {"Authorization": token}
link1 = f"https://discord.com/api/v9/channels/{channel}/messages?limit=50"

while True:
    # Run code
    response = requests.get(link1, headers=headers)
    messages = response.json()

    if not messages:
        print("No more messages to delete.")
        break

    # Parse the messages
    last_message_id = None
    for message in messages:
        message_author = message["author"]
        if message_author["id"] == author_input:
            message_id = message["id"]
            message_content = message.get("content", "")
            print(f"Deleting {message_id}, {message_content}")
            link2 = f"https://discord.com/api/v9/channels/{channel}/messages/{message_id}"
            requests.delete(link2, headers=headers)
            time.sleep(1)
        last_message_id = message["id"]

    print("Fetching 50 More Messages")
    link1 = f"https://discord.com/api/v9/channels/{channel}/messages?before={last_message_id}&limit=50"
    time.sleep(1)

print("Message deletion completed.")
