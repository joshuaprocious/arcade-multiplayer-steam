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

    # Assume the client knows our ID and will initiate contact
    print("✅ Lobby created. Waiting for connection...")
    client_id = 76561199837045498  # <- your second account Steam ID
    sender = send_hello_until_connected(client_id)  # We respond to whoever pings us
    lobby_chat(sender)


def client_mode():
    print("🔗 Starting as client...")

    time.sleep(2)  # Let Steam complete the join

    # Replace with actual known host SteamID
    host_id = 76561198074054767
    print(f"📤 Attempting to connect to host {host_id}...")

    try:
        partner_id = send_hello_until_connected(host_id)
        lobby_chat(partner_id)

    except TimeoutError as e:
        print(str(e))


def send_hello_until_connected(target_id: int, timeout=10.0):
    print(f"🚀 Sending hello to {target_id} until connected...")
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
    raise TimeoutError("❌ Failed to establish connection.")


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
