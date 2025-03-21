from libc.stdint cimport uint32_t, uint64_t
from libc.stdint cimport uint16_t

from libc.stdlib cimport malloc, free
ctypedef bint bool

cdef extern from "steam/steam_api.h":
    bint SteamAPI_Init()
    void SteamAPI_RunCallbacks()
    void SteamAPI_Shutdown()

    cdef cppclass CSteamID:
        CSteamID()
        uint64_t ConvertToUint64()

    cdef cppclass ISteamUser:
        CSteamID GetSteamID()

    cdef cppclass ISteamMatchmaking:
        bool CreateLobby(int eLobbyType, int maxMembers)
        bool JoinLobby(CSteamID steamIDLobby)
        void LeaveLobby(CSteamID steamIDLobby)
        int GetNumLobbyMembers(CSteamID steamIDLobby)
        CSteamID GetLobbyMemberByIndex(CSteamID steamIDLobby, int iMember)

    cdef cppclass ISteamNetworking:
        bool SendP2PPacket(CSteamID steamIDRemote, const void* pubData, uint32_t cubData, int eP2PSendType, int nChannel)
        bool IsP2PPacketAvailable(uint32_t* pcubMsgSize, int nChannel)
        bool ReadP2PPacket(void* pubDest, uint32_t cubDest, uint32_t* pcubMsgSize, CSteamID* pSteamIDRemote, int nChannel)

    ISteamUser* SteamUser()
    ISteamMatchmaking* SteamMatchmaking()
    ISteamNetworking* SteamNetworking()

cdef extern from "steam/steam_api.h":
    cdef enum ELobbyType:
        k_ELobbyTypePrivate
        k_ELobbyTypeFriendsOnly
        k_ELobbyTypePublic
        k_ELobbyTypeInvisible

    cdef enum EP2PSend:
        k_EP2PSendUnreliable
        k_EP2PSendUnreliableNoDelay
        k_EP2PSendReliable
        k_EP2PSendReliableWithBuffering


cdef extern from "steam/steam_api.h":
    cdef cppclass CGameID:
        uint32_t AppID()

    
    cdef struct FriendGameInfo_t:
        CGameID m_gameID
        uint32_t m_unGameIP
        uint16_t m_usGamePort
        uint16_t m_usQueryPort
        CSteamID m_steamIDLobby

    cdef cppclass ISteamFriends:
        int GetFriendCount(int flags)
        CSteamID GetFriendByIndex(int index, int flags)
        bint GetFriendGamePlayed(CSteamID steamIDFriend, FriendGameInfo_t* pFriendGameInfo)

    ISteamFriends* SteamFriends()
