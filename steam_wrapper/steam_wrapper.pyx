# steam_wrapper.pyx

from libc.stdint cimport uint32_t, uint64_t
from libc.stdlib cimport malloc, free

from cpython.bytes cimport PyBytes_FromStringAndSize

cdef ISteamUser* user = NULL
cdef ISteamMatchmaking* matchmaking = NULL
cdef ISteamNetworking* networking = NULL




def init_steam():
    if not SteamAPI_Init():
        raise RuntimeError("SteamAPI_Init failed.")
    global user, matchmaking, networking
    user = SteamUser()
    matchmaking = SteamMatchmaking()
    networking = SteamNetworking()

def run_callbacks():
    SteamAPI_RunCallbacks()

def shutdown_steam():
    SteamAPI_Shutdown()

def get_steam_id():
    cdef CSteamID sid = user.GetSteamID()
    return sid.ConvertToUint64()

def create_lobby(int lobby_type, int max_members):
    return matchmaking.CreateLobby(<ELobbyType>lobby_type, max_members)




def get_num_lobby_members(uint64_t lobby_id):
    cdef CSteamID lid = CSteamID()
    (<unsigned long long*>(&lid))[0] = lobby_id
    return matchmaking.GetNumLobbyMembers(lid)

def get_lobby_member_by_index(uint64_t lobby_id, int index):
    cdef CSteamID lid = CSteamID()
    (<unsigned long long*>(&lid))[0] = lobby_id
    return matchmaking.GetLobbyMemberByIndex(lid, index).ConvertToUint64()

def send_p2p(uint64_t target_id, bytes data, int send_type=1, int channel=0):
    cdef CSteamID sid = CSteamID()
    (<uint64_t*>(&sid))[0] = target_id

    cdef const char* buf = data
    return networking.SendP2PPacket(sid, <const void*>buf, len(data), <EP2PSend>send_type, channel)


def read_p2p(int channel=0):
    cdef uint32_t size

    cdef CSteamID remote_id
    if not networking.IsP2PPacketAvailable(&size, channel):
        return None

    cdef char* buffer = <char*>malloc(size)
    if not networking.ReadP2PPacket(buffer, size, &size, &remote_id, channel):
        return None

    py_data = PyBytes_FromStringAndSize(buffer, size)
    free(buffer)
    return py_data, remote_id.ConvertToUint64()
