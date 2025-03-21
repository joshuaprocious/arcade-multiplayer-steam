import ctypes
import os
import sys

# We'll assume 'steamworks' package is installed or placed in the root folder
from steamworks import STEAMWORKS

def main():
    root_path = os.getcwd()
    
    # 1. Check for DLL in the root folder
    dll_path = os.path.join(root_path, "SteamworksPy64.dll")
    if not os.path.exists(dll_path):
        print(f"❌ ERROR: SteamworksPy64.dll not found in root folder:\n   {dll_path}")
        sys.exit(1)

    # 2. Load the DLL to ensure it’s actually accessible and has dependencies
    try:
        ctypes.CDLL(dll_path)
        print(f"✅ SteamworksPy64.dll successfully loaded from:\n   {dll_path}")
    except OSError as e:
        print(f"❌ ERROR: Failed to load SteamworksPy64.dll. Check dependencies.\n   {e}")
        sys.exit(1)

    # 3. Initialize Steamworks
    try:
        steam = STEAMWORKS()
        steam.initialize()
        steam.run_callbacks()         # Manually pump callbacks (sometimes needed per frame in older forks)

        # Check if Steam is running
        if steam.IsSteamRunning():
            # If running, attempt to read the user's name via the Friends interface
            persona = steam.GetPersonaName()
            print(f"✅ Steam is running. Logged in as: {persona}")
        else:
            print("❌ Steam client not running or user not logged on.")
            #sys.exit(1)
    except Exception as e:
        print(f"❌ ERROR: SteamworksPy initialization failed.\n   {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
