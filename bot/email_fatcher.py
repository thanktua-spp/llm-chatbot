import win32com.client as client
import yaml

def access_outlook_email(target_sender_email):
    # Create an instance of the Outlook application
    outlook = client.Dispatch("Outlook.Application")
    # Get the MAPI namespace
    namespace = outlook.GetNamespace("MAPI")
    # Get the Inbox folder
    inbox = namespace.GetDefaultFolder(6)  # 6 corresponds to the Inbox folder
    # Access emails in the Inbox
    messages = inbox.Items
    # Create a list to store filtered emails
    all_message_info = ""
    # Loop through emails and filter by sender
    filtered_messages = messages.Restrict(f"[SenderEmailAddress]='{target_sender_email}'")
    #filtered_messages = messages.Restrict(f"SenderEmailAddress = '{target_sender_email}'")
    for message in filtered_messages:
        message_info = f"Subject: {message.Subject}\nSender: {message.SenderName}\nBody:{message.Body}\n"
        all_message_info += message_info
    return all_message_info

if __name__ == "__main__":
    # Specify the target sender's email address
    target_sender_email = 'hellonigeria@getreliancehealth.com'  # hellonigeria@getreliancehealth.com michael.aku@cyphercrescent.com Replace with the desired sender's email
    # Call access_outlook_email to filter and retrieve relevant email messages
    sender_email_history = access_outlook_email(target_sender_email)
    print(sender_email_history)

