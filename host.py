import time
import steam_wrapper as steam

# Replace this with your actual host Steam ID for testing
KNOWN_HOST_ID = 76561198074054767

def host_mode():
    print("🛠 Starting as host...")
    if not steam.create_lobby(2, 2):  # 2 = k_ELobbyTypePublic
        print("❌ Failed to create lobby")
        return

    print("✅ Lobby created. Waiting for player to join...")
    while True:
        steam.run_callbacks()

        result = steam.read_p2p()
        if result:
            msg, sender = result
            print(f"📨 From {sender}: {msg.decode()}")
            steam.send_p2p(sender, b"Welcome to the game!")
        time.sleep(0.05)

def client_mode():
    print("🔗 Starting as client...")

    # Wait briefly for Steam overlay join
    time.sleep(2)

    steam.send_p2p(KNOWN_HOST_ID, b"Hello from client!")
    print(f"📤 Sent message to host {KNOWN_HOST_ID}")

    while True:
        steam.run_callbacks()

        result = steam.read_p2p()
        if result:
            msg, sender = result
            print(f"📨 From {sender}: {msg.decode()}")
        time.sleep(0.05)

def main():
    steam.init_steam()
    my_id = steam.get_steam_id()
    print(f"🎮 Running as SteamID: {my_id}")

    choice = input("🟢 Host or Join? [h/j] ").strip().lower()
    try:
        if choice == "h":
            host_mode()
        elif choice == "j":
            client_mode()
        else:
            print("❌ Invalid choice. Exiting.")
    except KeyboardInterrupt:
        print("🛑 Shutting down.")
        steam.shutdown_steam()

if __name__ == "__main__":
    main()
