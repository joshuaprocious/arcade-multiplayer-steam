import time
import steam_wrapper as steam

def wait_for_connection(target_id=None):
    print("🔄 Waiting for connection...")
    while True:
        steam.run_callbacks()

        result = steam.read_p2p()
        if result:
            msg, sender = result
            print(f"📨 From {sender}: {msg.decode()}")

            # If host, respond
            if not target_id:
                steam.send_p2p(sender, b"Welcome to the game!")
            return sender  # Return sender's ID for ongoing chat

        time.sleep(0.05)

def lobby_chat(partner_id):
    print("💬 Chatting with:", partner_id)
    while True:
        steam.run_callbacks()

        result = steam.read_p2p()
        if result:
            msg, sender = result
            print(f"📨 From {sender}: {msg.decode()}")

        time.sleep(0.05)

def host_mode():
    print("🛠 Starting as host...")
    if not steam.create_lobby(2, 2):  # Public, max 2
        print("❌ Failed to create lobby")
        return

    print("✅ Lobby created. Wait for player to join via Steam overlay...")
    client_id = wait_for_connection()
    lobby_chat(client_id)

def client_mode():
    print("🔗 Starting as client...")

    # Wait for Steam to complete overlay lobby join
    time.sleep(2)

    # Send message to lobby host (detected after join)
    my_id = steam.get_steam_id()
    print(f"✅ Client SteamID: {my_id}")

    # Attempt to talk to whoever responds
    # Send to the known host ID or broadcast message
    # This only works if you've joined a Steam lobby!
    try_ids = [76561198074054767]  # Add known hosts here or scan friends later
    for target in try_ids:
        print(f"📤 Sending message to host {target}")
        steam.send_p2p(target, b"Hello from client!")

    partner_id = wait_for_connection()
    lobby_chat(partner_id)

def main():
    steam.init_steam()
    my_id = steam.get_steam_id()
    print(f"🎮 Running as SteamID: {my_id}")

    try:
        choice = input("🟢 Host or Join? [h/j] ").strip().lower()
        if choice == "h":
            host_mode()
        elif choice == "j":
            client_mode()
        else:
            print("❌ Invalid choice.")
    except KeyboardInterrupt:
        print("🛑 Shutting down.")
    finally:
        steam.shutdown_steam()

if __name__ == "__main__":
    main()
