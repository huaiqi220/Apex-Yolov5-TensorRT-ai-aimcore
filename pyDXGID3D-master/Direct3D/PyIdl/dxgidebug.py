##
##    Copyright (C) Microsoft.  All rights reserved.
##    Windows Kits version 10.0.19041.0
##
##   Translate in Python by J. Vnh
##
import comtypes
import ctypes
import ctypes.wintypes as wintypes

DXGI_DEBUG_BINARY_VERSION = 1

DXGI_DEBUG_RLO_FLAGS = ctypes.c_uint
DXGI_DEBUG_RLO_SUMMARY         = DXGI_DEBUG_RLO_FLAGS(0x1)
DXGI_DEBUG_RLO_DETAIL          = DXGI_DEBUG_RLO_FLAGS(0x2)
DXGI_DEBUG_RLO_IGNORE_INTERNAL = DXGI_DEBUG_RLO_FLAGS(0x4)
DXGI_DEBUG_RLO_ALL             = DXGI_DEBUG_RLO_FLAGS(0x7)

##==================================================================================================================================
##
## DXGI Debug Producer GUIDs
##
##==================================================================================================================================

DXGI_DEBUG_ID   = comtypes.GUID
DXGI_DEBUG_ALL  = comtypes.GUID("{e48ae283-da80-490b-87e6-43e9a9cfda08}") # DXGI_DEBUG_ALL,  0xe48ae283, 0xda80, 0x490b, 0x87, 0xe6, 0x43, 0xe9, 0xa9, 0xcf, 0xda, 0x08
DXGI_DEBUG_DX   = comtypes.GUID("{35cdd7fc-13be-421d-a5d7-7e4451287d64}") # DXGI_DEBUG_DX,   0x35cdd7fc, 0x13b2, 0x421d, 0xa5, 0xd7, 0x7e, 0x44, 0x51, 0x28, 0x7d, 0x64
DXGI_DEBUG_DXGI = comtypes.GUID("{25cddaa4-b1c6-47e1-ac3e-98875b5a2e2a}") # DXGI_DEBUG_DXGI, 0x25cddaa4, 0xb1c6, 0x47e1, 0xac, 0x3e, 0x98, 0x87, 0x5b, 0x5a, 0x2e, 0x2a
DXGI_DEBUG_APP  = comtypes.GUID("{06cd6e01-4219-4ebd-8709-27ed23360c62}") # DXGI_DEBUG_APP,   0x6cd6e01, 0x4219, 0x4ebd, 0x87, 0x9, 0x27, 0xed, 0x23, 0x36, 0xc, 0x62


##==================================================================================================================================
##
## Info Queue
##
##==================================================================================================================================

DXGI_INFO_QUEUE_MESSAGE_CATEGORY = ctypes.c_uint
DXGI_INFO_QUEUE_MESSAGE_CATEGORY_UNKNOWN               = DXGI_INFO_QUEUE_MESSAGE_CATEGORY(0)
DXGI_INFO_QUEUE_MESSAGE_CATEGORY_MISCELLANEOUS         = DXGI_INFO_QUEUE_MESSAGE_CATEGORY(1)
DXGI_INFO_QUEUE_MESSAGE_CATEGORY_INITIALIZATION        = DXGI_INFO_QUEUE_MESSAGE_CATEGORY(2)
DXGI_INFO_QUEUE_MESSAGE_CATEGORY_CLEANUP               = DXGI_INFO_QUEUE_MESSAGE_CATEGORY(3)
DXGI_INFO_QUEUE_MESSAGE_CATEGORY_COMPILATION           = DXGI_INFO_QUEUE_MESSAGE_CATEGORY(4)
DXGI_INFO_QUEUE_MESSAGE_CATEGORY_STATE_CREATION        = DXGI_INFO_QUEUE_MESSAGE_CATEGORY(5)
DXGI_INFO_QUEUE_MESSAGE_CATEGORY_STATE_SETTING         = DXGI_INFO_QUEUE_MESSAGE_CATEGORY(6)
DXGI_INFO_QUEUE_MESSAGE_CATEGORY_STATE_GETTING         = DXGI_INFO_QUEUE_MESSAGE_CATEGORY(7)
DXGI_INFO_QUEUE_MESSAGE_CATEGORY_RESOURCE_MANIPULATION = DXGI_INFO_QUEUE_MESSAGE_CATEGORY(8)
DXGI_INFO_QUEUE_MESSAGE_CATEGORY_EXECUTION             = DXGI_INFO_QUEUE_MESSAGE_CATEGORY(9)
DXGI_INFO_QUEUE_MESSAGE_CATEGORY_SHADER                = DXGI_INFO_QUEUE_MESSAGE_CATEGORY(10)

DXGI_INFO_QUEUE_MESSAGE_SEVERITY = ctypes.c_uint
DXGI_INFO_QUEUE_MESSAGE_SEVERITY_CORRUPTION = DXGI_INFO_QUEUE_MESSAGE_SEVERITY(0)
DXGI_INFO_QUEUE_MESSAGE_SEVERITY_ERROR      = DXGI_INFO_QUEUE_MESSAGE_SEVERITY(1)
DXGI_INFO_QUEUE_MESSAGE_SEVERITY_WARNING    = DXGI_INFO_QUEUE_MESSAGE_SEVERITY(2)
DXGI_INFO_QUEUE_MESSAGE_SEVERITY_INFO       = DXGI_INFO_QUEUE_MESSAGE_SEVERITY(3)
DXGI_INFO_QUEUE_MESSAGE_SEVERITY_MESSAGE    = DXGI_INFO_QUEUE_MESSAGE_SEVERITY(4)

DXGI_INFO_QUEUE_MESSAGE_ID = ctypes.c_int
DXGI_INFO_QUEUE_MESSAGE_ID_STRING_FROM_APPLICATION = 0

class DXGI_INFO_QUEUE_MESSAGE(ctypes.Structure):
    _fields_ = [('Producer',              DXGI_DEBUG_ID),
                ('Category',              DXGI_INFO_QUEUE_MESSAGE_CATEGORY),
                ('Severity',              DXGI_INFO_QUEUE_MESSAGE_SEVERITY),
                ('ID',                    DXGI_INFO_QUEUE_MESSAGE_ID),
                ('pDescription',          ctypes.POINTER(ctypes.c_char_p)), # [annotation("_Field_size_(DescriptionByteLength)")]
                ('DescriptionByteLength', ctypes.c_size_t),

    ]

class DXGI_INFO_QUEUE_FILTER_DESC(ctypes.Structure):
    _fields_ = [('NumCategories', wintypes.UINT),
                ('pCategoryList', ctypes.POINTER(DXGI_INFO_QUEUE_MESSAGE_CATEGORY)), # [annotation("_Field_size_(NumCategories)")
                ('NumSeverities', wintypes.UINT),
                ('pSeverityList', ctypes.POINTER(DXGI_INFO_QUEUE_MESSAGE_SEVERITY)), # annotation("_Field_size_(NumSeverities)")]
                ('NumIDs',        wintypes.UINT),
                ('pIDList',       ctypes.POINTER(DXGI_INFO_QUEUE_MESSAGE_ID)), # [annotation("_Field_size_(NumIDs)")]

    ]

class DXGI_INFO_QUEUE_FILTER(ctypes.Structure):
    _fields_ = [('AllowList', DXGI_INFO_QUEUE_FILTER_DESC),
                ('DenyList',  DXGI_INFO_QUEUE_FILTER_DESC),
    ]

DXGI_INFO_QUEUE_DEFAULT_MESSAGE_COUNT_LIMIT = 1024
# HRESULT WINAPI DXGIGetDebugInterface(REFIID riid, void **ppDebug)


##=============================================================================
## IDXGIInfoQueue
##
## Logs DX Messages.
## This interface is a singleton per process.  Debug DX devices will log messages
## to this object which can be retrieved through its APIs.
##
##

class IDXGIInfoQueue(comtypes.IUnknown):
    _iid_ = comtypes.GUID("{D67441C7-672A-476f-9E82-CD55B44949CE}")
    _methods_ = [
        ##=========================================================================
        ## Methods for configuring how much data is stored in the queue.
        comtypes.STDMETHOD(comtypes.HRESULT,"SetMessageCountLimit", [
            DXGI_DEBUG_ID,          # _In_ Producer
            ctypes.c_ulonglong,     # _In_ MessageCountLimit
            ]),
        comtypes.STDMETHOD(None, "ClearStoredMessage", [
            DXGI_DEBUG_ID,          # _In_ Producer
            ]),
        
        ##=========================================================================
        ## Methods for retrieving data or statistics from the queue.
        comtypes.STDMETHOD(comtypes.HRESULT, "GetMessage", [
            DXGI_DEBUG_ID,          # _In_ Producer
            ctypes.c_ulonglong,     # _In_ MessageIndex
            ctypes.POINTER(DXGI_INFO_QUEUE_MESSAGE), # _Out_writes_bytes_opt_(*pMessageByteLength) pMessage
            ctypes.POINTER(ctypes.c_size_t), # _Inout_ pMessageByteLength
            ]),
        comtypes.STDMETHOD(ctypes.c_ulonglong,"GetNumStoredMessagesAllowedByRetrievalFilters", [
            DXGI_DEBUG_ID,          # _In_ Producer
            ]),
        comtypes.STDMETHOD(ctypes.c_ulonglong,"GetNumStoredMessages", [
            DXGI_DEBUG_ID,          # _In_ Producer
            ]),
        comtypes.STDMETHOD(ctypes.c_ulonglong,"GetNumMessagesDiscardedByMessageCountLimit", [
            DXGI_DEBUG_ID,          # _In_ Producer
            ]),
        comtypes.STDMETHOD(ctypes.c_ulonglong,"GetMessageCountLimit", [
            DXGI_DEBUG_ID,          # _In_ Producer
            ]),
        comtypes.STDMETHOD(ctypes.c_ulonglong,"GetNumMessagesAllowedByStorageFilter", [
            DXGI_DEBUG_ID,          # _In_ Producer
            ]),
        comtypes.STDMETHOD(ctypes.c_ulonglong,"GetNumMessagesDeniedByStorageFilter", [
            DXGI_DEBUG_ID,          # _In_ Producer
            ]),
        
        ##=========================================================================
        ## Methods for filtering what gets stored in the queue
        comtypes.STDMETHOD(comtypes.HRESULT, "AddStorageFilterEntries", [
            DXGI_DEBUG_ID,                              # _In_ Producer
            ctypes.POINTER(DXGI_INFO_QUEUE_FILTER),     # _In_ pFilter
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "GetStorageFilter", [
            DXGI_DEBUG_ID,                          # _In_ Producer
            ctypes.POINTER(DXGI_INFO_QUEUE_FILTER), # _Out_writes_bytes_opt_(*pFilterByteLength) pFilter
            ctypes.POINTER(ctypes.c_size_t),        # _Inout_ pFilterByteLength
            ]),
        comtypes.STDMETHOD(None, "ClearStorageFilter", [
            DXGI_DEBUG_ID,
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "PushEmptyStorageFilter", [
            DXGI_DEBUG_ID,
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "PushDenyAllStorageFilter", [
            DXGI_DEBUG_ID,
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "PushCopyOfStorageFilter", [
            DXGI_DEBUG_ID,
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "PushStorageFilter", [
            DXGI_DEBUG_ID,
            ctypes.POINTER(DXGI_INFO_QUEUE_FILTER),
            ]),
        comtypes.STDMETHOD(None, "PopStorageFilter", [
            DXGI_DEBUG_ID,
            ]),
        comtypes.STDMETHOD(wintypes.UINT, "GetStorageFilterStackSize", [
            DXGI_DEBUG_ID,
            ]),
        
        ##=========================================================================
        ## Methods for filtering what gets read out of the queue by GetMessage().
        comtypes.STDMETHOD(comtypes.HRESULT, "AddRetrievalFilterEntries", [
            DXGI_DEBUG_ID,
            ctypes.POINTER(DXGI_INFO_QUEUE_FILTER),
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "GetRetrievalFilter", [
            DXGI_DEBUG_ID,
            ctypes.POINTER(DXGI_INFO_QUEUE_FILTER),
            ctypes.POINTER(ctypes.c_size_t),
            ]),
        comtypes.STDMETHOD(None, "ClearRetrievalFilter", [
            DXGI_DEBUG_ID,
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "PushEmptyRetrievalFilter", [
            DXGI_DEBUG_ID,
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "PushDenyAllRetrievalFilter", [
            DXGI_DEBUG_ID,
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "PushCopyOfRetrievalFilter", [
            DXGI_DEBUG_ID,
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "PushRetrievalFilter", [
            DXGI_DEBUG_ID,
            comtypes.POINTER(DXGI_INFO_QUEUE_FILTER),
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "PopRetrievalFilter", [
            DXGI_DEBUG_ID,
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "GetRetrievalFilterStackSize", [
            DXGI_DEBUG_ID,
            ]),
        
        ##=========================================================================
        ## Methods for adding entries to the queue.
        comtypes.STDMETHOD(comtypes.HRESULT, "AddMessage", [
            DXGI_DEBUG_ID,
            DXGI_INFO_QUEUE_MESSAGE_CATEGORY,
            DXGI_INFO_QUEUE_MESSAGE_SEVERITY,
            DXGI_INFO_QUEUE_MESSAGE_ID,
            wintypes.LPCSTR,
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "AddApplicationMessage", [
            DXGI_INFO_QUEUE_MESSAGE_SEVERITY,
            wintypes.LPCSTR,
            ]),
        
        ##=========================================================================
        ##  Methods for breaking on errors that pass the storage filter
        comtypes.STDMETHOD(comtypes.HRESULT, "SetBreakOnCategory", [
            DXGI_DEBUG_ID,
            DXGI_INFO_QUEUE_MESSAGE_CATEGORY,
            wintypes.BOOL,
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "SetBreakOnSeverity", [
            DXGI_DEBUG_ID,
            DXGI_INFO_QUEUE_MESSAGE_SEVERITY,
            wintypes.BOOL,
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "SetBreakOnID", [
            DXGI_DEBUG_ID,
            DXGI_INFO_QUEUE_MESSAGE_ID,
            wintypes.BOOL,
            ]),
        comtypes.STDMETHOD(wintypes.BOOL, "GetBreakOnCategory", [
            DXGI_DEBUG_ID,
            DXGI_INFO_QUEUE_MESSAGE_CATEGORY,
            ]),
        comtypes.STDMETHOD(wintypes.BOOL, "GetBreakOnSeverity", [
            DXGI_DEBUG_ID,
            DXGI_INFO_QUEUE_MESSAGE_SEVERITY,
            ]),
        comtypes.STDMETHOD(wintypes.BOOL, "GetBreakOnID", [
            DXGI_DEBUG_ID,
            DXGI_INFO_QUEUE_MESSAGE_ID,
            ]),

        ##=========================================================================
        ## Methods for muting debug spew from the InfoQueue
        comtypes.STDMETHOD(comtypes.HRESULT, "SetMuteDebugOutput", [
            DXGI_DEBUG_ID,
            wintypes.BOOL,
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "GetMuteDebugOutput", [
            DXGI_DEBUG_ID,
            ]),
    ]

class IDXGIDebug(comtypes.IUnknown):
    _iid_ = comtypes.GUID("{119E7452-DE9E-40fe-8806-88F90C12B441}")
    _methods_ = [
        comtypes.STDMETHOD(comtypes.HRESULT, "ReportLiveObjects", [
            ctypes.POINTER(comtypes.GUID),          # apiid
            DXGI_DEBUG_RLO_FLAGS,   # flags
            ]),
    ]

class IDXGIDebug1(IDXGIDebug):
    _iid_ = comtypes.GUID("{c5a05f0c-16f2-4adf-9f4d-a8c4d58ac550}")
    _methods_ = [
        comtypes.STDMETHOD(None, "EnableLeakTrackingForThread", []),
        comtypes.STDMETHOD(None, "DisableLeakTrackingForThread", []),
        comtypes.STDMETHOD(wintypes.BOOL, "IsLeakTrackingEnabledForThread", []),
    ]

####### END OF FILE ####### 

