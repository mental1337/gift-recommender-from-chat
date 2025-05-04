from datetime import datetime
from typing import List, Tuple

def parse_whatsapp_messages(message: str, name: str) -> List[Tuple[datetime, str]]:
    """
    Parse WhatsApp messages and return messages from the specified person with their dates.
    
    Args:
        message: WhatsApp conversation history
        name: Name of the person whose messages you want to extract
    
    Returns:
        List of tuples containing (date, message) for each message from the specified person
    """
    messages = []
    for line in message.split("\n"):
        # Skip empty lines and system messages
        if not line.strip() or "Messages and calls are end-to-end encrypted" in line:
            continue
            
        # Split on the first occurrence of " - " to separate timestamp from content
        parts = line.split(" - ", 1)
        if len(parts) != 2:
            continue
            # raise ValueError(f"Invalid line: {line}")
            
        # Parse the date
        try:
            date_str = parts[0].split(", ")[0]  # Get just the date part before the comma
            date = datetime.strptime(date_str, "%m/%d/%y").date()
        except ValueError:
            continue  # Skip if date parsing fails
            
        # Get the content part and check if it starts with the name
        content = parts[1]
        if content.startswith(name + ":"):
            # Extract just the message content after the name
            message_content = content[len(name) + 1:].strip()
            if message_content:  # Only add non-empty messages
                messages.append((date, message_content))
    
    return messages

def parse_instagram_messages(message: str, name: str) -> list[str]:
    """
    Message: Instagram conversation history.
    Name: Name of the person you want to get messages from.
    """
    messages = []
    for line in message.split("\n"):
        if line.startswith(name):
            messages.append(line)
    return messages

if __name__ == "__main__":
    # Sample WhatsApp chat
    with open("../Sample WhatsApp Chat.txt", "r") as f:
        sample_chat = f.read()

    # Test parsing messages from Pritam
    print("Messages from Pritam Bhattacharya:")
    pritam_messages = parse_whatsapp_messages(sample_chat, "Pritam Bhattacharya")
    for date, msg in pritam_messages:
        print(f"- [{date}] {msg}")

    print("\nMessages from 𝔖𝔞𝔤𝔞𝔯:")
    sagar_messages = parse_whatsapp_messages(sample_chat, "𝔖𝔞𝔤𝔞𝔯")
    for date, msg in sagar_messages:
        print(f"- [{date}] {msg}")