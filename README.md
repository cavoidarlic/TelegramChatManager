# Telegram Manager

A Python-based userbot tool to efficiently manage your Telegram chats and channels, featuring bulk leave functionality and other management options.

## Features

- **Chat/Channel Listing**: View all your groups, channels, and private conversations in an organized manner
- **Bulk Leave**: Easily leave multiple chats or channels at once
- **Category Filtering**: Select to leave only groups, only channels, or both
- **Safe Operation**: Confirmation prompts prevent accidental actions
- **Session Management**: Maintains your authentication for future use

## Requirements

- Python 3.7 or higher
- Active Telegram account
- API credentials from Telegram

## Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/telegram-manager.git
   cd telegram-manager
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file based on `.env.example`:
   ```bash
   cp .env.example .env  # For Linux/Mac
   # OR
   copy .env.example .env  # For Windows
   ```

4. Obtain your API credentials:
   - Visit [https://my.telegram.org/apps](https://my.telegram.org/apps)
   - Log in with your phone number
   - Create a new application with the following details:
     - **App title**: TelegramChatManager (or any name you prefer)
     - **Short name**: tchatmanager (alphanumeric, 5-32 characters)
     - **Platform**: Desktop
     - **Description**: Personal tool for managing Telegram chats
   - Copy the generated API ID and API Hash

5. Edit the `.env` file with your credentials:
   ```
   API_ID=your_api_id_here
   API_HASH=your_api_hash_here
   PHONE_NUMBER=+1234567890  # Include country code
   ```

## Usage

### Running the Manager

Execute the main script:

```bash
python telegram_manager.py
```

On first run, you'll be prompted to enter a verification code sent to your Telegram account.

### Available Commands

The menu-driven interface offers these options:

1. **List all chats**
   - View a categorized list of all your Telegram conversations
   - Groups, channels, and private chats are shown separately with IDs

2. **Bulk leave chats**
   - Choose which type of conversations to leave:
     - Groups only
     - Channels only
     - Both groups and channels
   - Confirm before performing the action

3. **Exit**
   - Properly disconnects from Telegram API

### Example Session

```
=== TELEGRAM MANAGER ===
1. List all chats
2. Bulk leave chats
3. Exit
Select an option: 1

=== GROUPS ===
1. Family Group (ID: 1234567890)
2. Work Team (ID: 9876543210)

=== CHANNELS ===
1. News Channel (ID: 1122334455)
2. Tech Updates (ID: 5566778899)

=== PRIVATE CHATS ===
1. John Doe (ID: 1212121212)
2. Jane Smith (ID: 3434343434)
```

## Technical Details

- Uses the [Telethon](https://github.com/LonamiWebs/Telethon) library to interact with Telegram's API
- Session data is stored in `telegram_manager_session.session` file
- Rate limiting measures are implemented to prevent API abuse

## Troubleshooting

### Common Issues:

1. **Authentication Failed**:
   - Ensure your API credentials are correct
   - Check that your phone number is in the correct format (+1234567890)

2. **FloodWaitError**:
   - You're leaving too many chats too quickly
   - Wait for the specified time and try again with fewer chats

3. **Session File Issues**:
   - If authentication keeps failing, try deleting the `.session` file and re-authenticating

4. **ModuleNotFoundError: No module named 'imghdr'**:
   - This occurs because of an incomplete Python installation or environment issue
   - **Solution 1**: Reinstall Python with the complete standard library
   - **Solution 2**: Use a Python distribution like Anaconda that includes all standard libraries
   - **Solution 3**: Create a simple mock imghdr.py file in your project folder:
     ```python
     # Simple mock for imghdr module
     def what(file, h=None):
         return None
     
     tests = []
     ```
   - **Solution 4**: Downgrade Telethon to an earlier version:
     ```bash
     pip uninstall telethon
     pip install telethon==1.24.0
     ```

## Advanced Usage

- You can modify the code to add custom filters for which chats to leave
- Consider adding features like:
  - Chat archiving instead of leaving
  - Muting notifications for selected chats
  - Exporting chat lists before leaving

## Security Considerations

- The `.session` file contains sensitive authentication information; keep it secure
- Never share your API credentials or session file with others
- Consider enabling Two-Factor Authentication on your Telegram account

## Disclaimer

This tool is for personal use and should be used responsibly. Excessive or abusive use of userbots can lead to account limitations or permanent bans by Telegram. The developer assumes no liability for any misuse of this tool or any resulting consequences.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
