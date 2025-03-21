import time
import steam_wrapper as steam  # <- your compiled Cython module

# Replace with the host's actual SteamID64
HOST_STEAM_ID = 76561198074054767  # ← Change this to your host's Steam ID

def main():
    steam.init_steam()
    my_id = steam.get_steam_id()
    print(f"✅ Client running as SteamID: {my_id}")

    print("⏳ Waiting to connect to host via overlay (Steam Friends → Join Game)...")
    time.sleep(3)  # Give time for Steam to complete lobby join

    # Send an initial message to the host
    steam.send_p2p(HOST_STEAM_ID, b"Hello from client!")
    print(f"📤 Sent greeting to host: {HOST_STEAM_ID}")

    try:
        while True:
            steam.run_callbacks()

            result = steam.read_p2p()
            if result:
                msg, sender_id = result
                print(f"📨 From {sender_id}: {msg.decode()}")

            time.sleep(0.05)

    except KeyboardInterrupt:
        print("🛑 Client shutting down.")
        steam.shutdown_steam()

if __name__ == "__main__":
    main()
