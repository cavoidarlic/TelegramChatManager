import os
import asyncio
import sys
from dotenv import load_dotenv
from pathlib import Path

# Check if .env file exists before attempting to load it
env_path = Path('.env')
if not env_path.is_file():
    print("Error: .env file not found!")
    print("Please create a .env file based on the provided .env.example:")
    print("1. Copy .env.example to .env")
    print("2. Fill in your API_ID, API_HASH, and PHONE_NUMBER")
    print("\nExample:")
    print("  API_ID=123456")
    print("  API_HASH=abcdef1234567890abcdef1234567890")
    print("  PHONE_NUMBER=+1234567890")
    sys.exit(1)

# Load environment variables from .env file
load_dotenv()

# Check if required environment variables are set
required_vars = ['API_ID', 'API_HASH', 'PHONE_NUMBER']
missing_vars = [var for var in required_vars if not os.getenv(var)]

if missing_vars:
    print(f"Error: Missing required environment variables: {', '.join(missing_vars)}")
    print("Please check your .env file and ensure all required variables are set.")
    sys.exit(1)

# Import Telethon after environment checks to prevent unnecessary errors
try:
    from telethon import TelegramClient
    from telethon.tl.types import Dialog, Channel, Chat, User
except ImportError as e:
    print(f"Error importing Telethon: {e}")
    print("Please ensure Telethon is properly installed: pip install telethon")
    if "imghdr" in str(e):
        print("\nDetected missing 'imghdr' module. This is a standard library issue.")
        print("Try one of these solutions:")
        print("1. Reinstall Python with the complete standard library")
        print("2. Create a mock imghdr.py in your project directory")
        print("3. Downgrade Telethon: pip install telethon==1.24.0")
    sys.exit(1)

# Authentication details
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
phone_number = os.getenv('PHONE_NUMBER')

class TelegramManager:
    def __init__(self):
        self.client = None
    
    async def connect(self):
        """Connect to Telegram and authenticate."""
        self.client = TelegramClient('telegram_manager_session', api_id, api_hash)
        await self.client.start(phone_number)
        print("Connected to Telegram!")
    
    async def list_dialogs(self):
        """List all dialogs (chats, channels, users) you're part of."""
        chats = []
        channels = []
        users = []
        
        print("Fetching dialogs...")
        async for dialog in self.client.iter_dialogs():
            entity = dialog.entity
            
            if isinstance(entity, Channel):
                channels.append(dialog)
            elif isinstance(entity, Chat):
                chats.append(dialog)
            elif isinstance(entity, User):
                users.append(dialog)
        
        return {
            'chats': chats,
            'channels': channels,
            'users': users
        }
    
    async def display_dialogs(self, dialogs_dict):
        """Display dialogs in a formatted way."""
        print("\n=== GROUPS ===")
        for i, dialog in enumerate(dialogs_dict['chats']):
            print(f"{i+1}. {dialog.name} (ID: {dialog.id})")
        
        print("\n=== CHANNELS ===")
        for i, dialog in enumerate(dialogs_dict['channels']):
            print(f"{i+1}. {dialog.name} (ID: {dialog.id})")
        
        print("\n=== PRIVATE CHATS ===")
        for i, dialog in enumerate(dialogs_dict['users']):
            print(f"{i+1}. {dialog.name} (ID: {dialog.id})")
    
    async def leave_chat(self, dialog):
        """Leave a specific chat/channel."""
        try:
            print(f"Leaving {dialog.name}...")
            await self.client.delete_dialog(dialog.entity)
            return True
        except Exception as e:
            print(f"Error leaving {dialog.name}: {e}")
            return False
    
    async def bulk_leave(self, dialogs_list):
        """Leave multiple chats/channels."""
        success_count = 0
        for dialog in dialogs_list:
            if await self.leave_chat(dialog):
                success_count += 1
            # Adding a small delay to prevent hitting rate limits
            await asyncio.sleep(0.5)
        
        print(f"Successfully left {success_count} out of {len(dialogs_list)} chats/channels.")
    
    async def disconnect(self):
        """Disconnect from Telegram."""
        await self.client.disconnect()
        print("Disconnected from Telegram.")

async def main():
    manager = TelegramManager()
    
    try:
        # Connect to Telegram
        await manager.connect()
        
        while True:
            print("\n=== TELEGRAM MANAGER ===")
            print("1. List all chats")
            print("2. Bulk leave chats")
            print("3. Exit")
            
            choice = input("Select an option: ")
            
            if choice == '1':
                dialogs = await manager.list_dialogs()
                await manager.display_dialogs(dialogs)
            
            elif choice == '2':
                dialogs = await manager.list_dialogs()
                await manager.display_dialogs(dialogs)
                
                print("\nSelect which type to leave:")
                print("1. Groups")
                print("2. Channels")
                print("3. Both groups and channels")
                
                leave_type = input("Enter your choice (1-3): ")
                
                to_leave = []
                if leave_type in ('1', '3'):
                    to_leave.extend(dialogs['chats'])
                if leave_type in ('2', '3'):
                    to_leave.extend(dialogs['channels'])
                
                if not to_leave:
                    print("No chats selected to leave.")
                    continue
                
                confirm = input(f"You are about to leave {len(to_leave)} chats/channels. Confirm? (y/n): ")
                if confirm.lower() == 'y':
                    await manager.bulk_leave(to_leave)
            
            elif choice == '3':
                break
            
            else:
                print("Invalid option. Please try again.")
    
    finally:
        await manager.disconnect()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
    except Exception as e:
        print(f"Error: {e}")
