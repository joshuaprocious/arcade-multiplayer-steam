import time
import steam_wrapper as steam

APP_ID = 480  # Spacewar AppID

def wait_for_connection(target_id=None):
    print("🔄 Waiting for connection...")
    while True:
        steam.run_callbacks()
        result = steam.read_p2p()
        if result:
            msg, sender = result
            print(f"📨 From {sender}: {msg.decode()}")
            if not target_id:
                steam.send_p2p(sender, b"Welcome to the game!")
            return sender
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

def find_friend_running_game(target_app_id=APP_ID):
    print("👥 Scanning friends for active players...")
    count = steam.get_friend_count()
    for i in range(count):
        fid = steam.get_friend_by_index(i)
        game_info = steam.get_friend_game_played(fid)
        if game_info and game_info["app_id"] == target_app_id:
            print(f"✅ Found friend in-game: {fid}")
            return fid
    print("❌ No friend found running the game.")
    return None

def send_hello_until_connected(target_id, timeout=10.0):
    print(f"🚀 Connecting to {target_id}...")
    start = time.time()
    while time.time() - start < timeout:
        steam.run_callbacks()
        steam.send_p2p(target_id, b"hello?")
        result = steam.read_p2p()
        if result:
            msg, sender = result
            print(f"✅ Connected to {sender}: {msg.decode()}")
            return sender
        time.sleep(0.5)
    raise TimeoutError("❌ Failed to connect.")

def host_mode():
    print("🛠 Starting as host...")
    if not steam.create_lobby(2, 2):
        print("❌ Failed to create lobby")
        return
    print("✅ Lobby created. Waiting for friend to join via Steam overlay...")
    sender = wait_for_connection()
    lobby_chat(sender)

def client_mode():
    print("🔗 Starting as client...")
    time.sleep(2)  # Give Steam time to finalize join

    host_id = find_friend_running_game()
    if not host_id:
        print("❌ No host detected. Exiting.")
        return

    try:
        partner = send_hello_until_connected(host_id)
        lobby_chat(partner)
    except TimeoutError as e:
        print(str(e))

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
