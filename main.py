

print("\n\n\tStart of main------------")


isClient = True
isServer = False

if isClient:
    import client

elif isServer:
    import server

else:
    print("Confused; not a server, not a client")




print("\n\n\tEnd of main------------")