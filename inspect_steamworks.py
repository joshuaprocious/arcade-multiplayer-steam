from steamworks import STEAMWORKS
steam = STEAMWORKS()
steam.initialize()

# Print all attributes/methods in the STEAMWORKS object
print(dir(steam))  

# Also see what's in the steam.User or steam.Friends, if those exist:
print("steam.User:", dir(steam.Users))
print("steam.Friends:", dir(steam.Friends))
