import os
import sys
import time
import pygame

# PyInstaller + Steam AppID setup
if hasattr(sys, '_MEIPASS'):
    os.chdir(sys._MEIPASS)
os.environ["SteamAppId"] = "480"
os.environ["SteamGameId"] = "480"

import steam_wrapper as steam

# --- Pygame Setup ---
pygame.init()
screen = pygame.display.set_mode((800, 600), pygame.SCALED | pygame.RESIZABLE)
pygame.display.set_caption("Echoes of Eternity")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 24)

log_lines = []
input_text = ""
in_chat = False
partner_id = None

def log(msg):
    log_lines.append(msg)
    if len(log_lines) > 100:
        log_lines.pop(0)
    print(msg)

def draw_console():
    screen.fill((10, 10, 10))
    for i, line in enumerate(log_lines[-28:]):
        surf = font.render(line, True, (200, 255, 200))
        screen.blit(surf, (20, 20 + i * 20))
    prompt = f"> {input_text}_"
    prompt_surf = font.render(prompt, True, (255, 255, 100))
    screen.blit(prompt_surf, (20, 580))
    pygame.display.flip()

def handle_command(cmd):
    global partner_id, in_chat
    if cmd == "h":
        log("🛠 Hosting lobby...")
        if not steam.create_lobby(2, 2):
            log("❌ Failed to create lobby")
            return
        log("✅ Lobby created. Waiting for player to join via overlay...")
        log("✅ Waiting for lobby propagation...")

        # Attempt to confirm by checking friend list or running callbacks
        for _ in range(30):
            steam.run_callbacks()
            time.sleep(0.1)

    elif cmd == "j":
        log("🔗 Join mode selected. Please join game via Steam overlay.")
        log("⌛ Waiting for host to message you...")
    elif cmd == "exit":
        pygame.quit()
        steam.shutdown_steam()
        sys.exit()
    elif in_chat and partner_id:
        steam.send_p2p(partner_id, cmd.encode())
        log(f"💬 You: {cmd}")
    else:
        log(f"❌ Unknown command or not connected: {cmd}")


def check_messages():
    global partner_id, in_chat
    result = steam.read_p2p()
    if result:
        msg, sender = result
        log(f"📨 From {sender}: {msg.decode()}")
        if not in_chat:
            partner_id = sender
            in_chat = True
            log(f"✅ Connected to {sender}. You may now chat.")


def main():
    global input_text
    steam.init_steam()
    log(f"🎮 SteamID: {steam.get_steam_id()}")
    log("🟢 Type 'h' to host or 'j' to join. Use overlay to join games. Type 'exit' to quit.")

    while True:
        steam.run_callbacks()
        check_messages()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                steam.shutdown_steam()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.key == pygame.K_RETURN:
                    cmd = input_text.strip()
                    log(f"> {cmd}")
                    handle_command(cmd.lower())
                    input_text = ""

                else:
                    input_text += event.unicode

        draw_console()
        clock.tick(30)

if __name__ == "__main__":
    main()
