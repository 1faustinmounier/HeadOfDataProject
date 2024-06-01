import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Part 1: posts to the Slack channel
# #assignment a message with your name (“Hello world, this is xx”)
client = WebClient(token='xoxb-7180027320434-7199302937398-2879EXDNXLP6RJD1OkQLCYUw')

channel_name = "assignment"
conversation_id = None
try:
    # Call the conversations.list method using the WebClient
    for result in client.conversations_list():
        if conversation_id is not None:
            break
        for channel in result["channels"]:
            if channel["name"] == channel_name:
                conversation_id = channel["id"]
                #Print result
                print(f"Found conversation ID: {conversation_id}")
                break

except SlackApiError as e:
    print(f"Error: {e}")


# ID of channel you want to post message to
channel_id = "C0753CH4V7G"

try:
    # Call the conversations.list method using the WebClient
    result = client.chat_postMessage(
        channel=channel_id,
        text="Hello world, this is Group 7's Bot!"
        # You could also use a blocks[] array to send richer content
    )
    # Print result, which includes information about the message (like TS)
    print(result)

except SlackApiError as e:
    print(f"Error: {e}")
    


# Part 2: download at least 3 images in a folder and write a loop that posts all images of the folder to the channel
# (you need to assume that you do not know in advance how many images you will have in the folder)

folder_path = '/Users/zhongkesun/PycharmProjects/pythonProject/Head of Data 101/API/images/'  # Path to the folder containing images
def upload_file(channel_id, file_path, message):
    try:
        response = client.files_upload_v2(
            channels = channel_id,
            file = file_path,
            initial_comment = message,
            title = os.path.basename(file_path)
    )
    except SlackApiError as e:
        # Print error response
        print(f"Error uploading file:{e.response['error']}") 

for i, file in enumerate(os.listdir('images'),1):
    path = os.path.join('images',file)
    upload_file(channel_id, path, f"Guanyu Zhou n {i}")