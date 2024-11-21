import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


def get_incremented_filename(base_name, extension=".txt"):
    """
    Generates an incremented file name.
    Combines `base_name` with incrementing numbers (e.g., ChatName.txt, ChatName1.txt, etc.).
    """
    i = 0
    while True:
        file_name = f"{base_name}{i if i > 0 else ''}{extension}"
        if not os.path.exists(file_name):
            return file_name
        i += 1

def attach_to_running_chrome():
    options = webdriver.ChromeOptions()
    options.debugger_address = "127.0.0.1:7777"  # Matches the debugging port

    # Connect to the existing Chrome instance
    driver = webdriver.Chrome(options=options)

    try:
        while True:
            # Check input
            user_input = input("Open the chat you wish to download. Press Enter to continue, type anything to exit:")
            if user_input != "":
                print("Exiting loop")
                break
            # Retrieve the chat name
            try:
                chat_name = driver.title
            except Exception:
                chat_name = "ChatGPT_Chat"  # Fallback name if chat name is not found
            # Sanitize the chat name for file systems
            chat_name = "".join(c if c.isalnum() or c in " _-" else "_" for c in chat_name)
            # Find user messages
            user_messages = driver.find_elements(By.CSS_SELECTOR, "div.whitespace-pre-wrap")
            # Find assistant messages
            assistant_messages = driver.find_elements(By.CSS_SELECTOR, "div.markdown.prose.w-full.break-words.dark\\:prose-invert")

            # Extract text from both user and assistant messages
            user_texts = [msg.text.strip() for msg in user_messages]
            assistant_texts = [msg.text.strip() for msg in assistant_messages]

            # Combine the messages in a readable format
            combined_data = []
            for user, assistant in zip(user_texts, assistant_texts):
                combined_data.append(f"User:\n\n{user}\n")
                combined_data.append(f"ChatGPT:\n\n{assistant}\n\n\n" + "=" * 100 + "\n")
                
            file_name = get_incremented_filename(chat_name)

            # Save combined data to a file
            with open(file_name, "w", encoding="utf-8") as file:
                file.write("ChatGPT Chat Export\n")
                file.write("=" * 50 + "\n\n")
                file.write("\n".join(combined_data))

            print(f"Chat content saved to {file_name}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

attach_to_running_chrome()
