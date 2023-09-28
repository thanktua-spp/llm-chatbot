import win32com.client
import csv

def access_outlook_email(target_sender_email):
    # Create an instance of the Outlook application
    outlook = win32com.client.Dispatch("Outlook.Application")

    # Get the MAPI namespace
    namespace = outlook.GetNamespace("MAPI")

    # Get the Inbox folder
    inbox = namespace.GetDefaultFolder(6)  # 6 corresponds to the Inbox folder

    # Access emails in the Inbox
    messages = inbox.Items

    # Create a list to store filtered emails
    sender_emails = []

    # Loop through emails and filter by sender
    for message in messages:
        sender_email = message.SenderEmailAddress
        if sender_email.lower() == target_sender_email.lower():
            sender_emails.append(message)

    return sender_emails

def email_body_search(term, inbox):
    relevant_messages = [(message.Subject, message.Body) for message in inbox.Items if term.lower() in message.Body.lower()]
    return relevant_messages

if __name__ == "__main__":
    # Specify the target sender's email address
    target_sender_email = 'franklinobasy@outlook.com'  # Replace with the desired sender's email

    # Call access_outlook_email to filter and retrieve relevant email messages
    filtered_emails = access_outlook_email(target_sender_email)

    # Specify the search term
    search_term = "youtube"  # Replace with your desired search term

    # Call email_body_search to search for the specified term in email bodies
    relevant_messages = email_body_search(search_term, inbox)

    # Write the relevant email subjects and bodies to a CSV file
    with open('search_results.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Subject', 'Body'])
        for subject, body in relevant_messages:
            writer.writerow([subject, body])
