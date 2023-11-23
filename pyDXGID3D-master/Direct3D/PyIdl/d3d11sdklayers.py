## ////////////////////////////////////////////////////////////////////////////////////////////
##                                                                                           
##  D3D11SDKLayers.idl
##                                                                                           
##  Contains interface definitions for the D3D11 SDK Layers .                                
##                                                                                           
##  Copyright (c) Microsoft Corporation.                                                     
##                                                                                           
## ////////////////////////////////////////////////////////////////////////////////////////////
import ctypes
import ctypes.wintypes as wintypes

import comtypes

from Direct3D.PyIdl.dxgi  import *
from Direct3D.PyIdl.d3d11 import *

D3D11_SDK_LAYER_VERSION = 1

## ==================================================================================================================================
## 
##  Debugging Layer
## 
## ==================================================================================================================================
D3D11_DEBUG_FEATURE_FLUSH_PER_RENDER_OP = 0x1
D3D11_DEBUG_FEATURE_FINISH_PER_RENDER_OP = 0x2
D3D11_DEBUG_FEATURE_PRESENT_PER_RENDER_OP = 0x4
D3D11_DEBUG_FEATURE_ALWAYS_DISCARD_OFFERED_RESOURCE = 0x8
D3D11_DEBUG_FEATURE_NEVER_DISCARD_OFFERED_RESOURCE = 0x10
D3D11_DEBUG_FEATURE_AVOID_BEHAVIOR_CHANGING_DEBUG_AIDS = 0x40
D3D11_DEBUG_FEATURE_DISABLE_TILED_RESOURCE_MAPPING_TRACKING_AND_VALIDATION = 0x80

D3D11_RLDO_FLAGS           = ctypes.c_uint
D3D11_RLDO_SUMMARY         = D3D11_RLDO_FLAGS(0x1).value
D3D11_RLDO_DETAIL          = D3D11_RLDO_FLAGS(0x2).value
D3D11_RLDO_IGNORE_INTERNAL = D3D11_RLDO_FLAGS(0x4).value

class ID3D11Debug(comtypes.IUnknown):
    _iid_ = comtypes.GUID("{79cf2233-7536-4948-9d36-1e4692dc5760}")
    _mehtods_ = [
        comtypes.STDMETHOD(comtypes.HRESULT,"SetFeatureMask", [
            wintypes.UINT, # UNIT Mask
            ]),
        comtypes.STDMETHOD(ctypes.c_uint,"GetFeatureMask",[]),
        comtypes.STDMETHOD(comtypes.HRESULT,"SetPresentPerRenderOpDelay",[
            wintypes.UINT, # UINT Milliseconds
            ]),
        comtypes.STDMETHOD(ctypes.c_uint,"GetPresentPerRenderOpDelay",[]),
        comtypes.STDMETHOD(comtypes.HRESULT,"SetSwapChain",[
            ctypes.POINTER(IDXGISwapChain), # _In_opt_ IDXGISwapChain * pSwapchain
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT,"GetSwapChain",[
            ctypes.POINTER(comtypes.POINTER(IDXGISwapChain)) # _Out_ IDXGISwapChain ** ppSwapchain
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT,"ValidateContext",[
            ctypes.POINTER(ID3D11DeviceContext), # _In_ ID3D11DeviceContext * pContext
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT,"ReportLiveDeviceObjects", [
            D3D11_RLDO_FLAGS, # D3D11_RLDO_FLAGS Flags
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT,"ValidateContextForDispatch",[
            ctypes.POINTER(ID3D11DeviceContext), # _In_ ID3D11DeviceContext * pContext
            ]),
    ]

class ID3D11SwitchToRef(comtypes.IUnknown):
    _iid_ = comtypes.GUID("{1EF337E3-58E7-4F83-A692-DB221F5ED47E}")
    _mehtods_ = [
        comtypes.STDMETHOD(ctypes.wintypes.BOOL,"SetUseRef", [
            wintypes.BOOL,  # BOOL UseRef
            ]),
        comtypes.STDMETHOD(ctypes.wintypes.BOOL,"GetUseRef", []),
    ]

D3D11_SHADER_TRACKING_RESOURCE_TYPE = ctypes.c_uint
D3D11_SHADER_TRACKING_RESOURCE_TYPE_NONE                 = D3D11_SHADER_TRACKING_RESOURCE_TYPE(0).value # call has no effect
D3D11_SHADER_TRACKING_RESOURCE_TYPE_UAV_DEVICEMEMORY     = D3D11_SHADER_TRACKING_RESOURCE_TYPE(1).value # call affects device memory created with UAV bind flags
D3D11_SHADER_TRACKING_RESOURCE_TYPE_NON_UAV_DEVICEMEMORY = D3D11_SHADER_TRACKING_RESOURCE_TYPE(2).value # call affects device memory created without UAV bind flags
D3D11_SHADER_TRACKING_RESOURCE_TYPE_ALL_DEVICEMEMORY     = D3D11_SHADER_TRACKING_RESOURCE_TYPE(3).value # call affects all device memory
D3D11_SHADER_TRACKING_RESOURCE_TYPE_GROUPSHARED_MEMORY   = D3D11_SHADER_TRACKING_RESOURCE_TYPE(4).value # call affects all shaders that use group shared memory created
D3D11_SHADER_TRACKING_RESOURCE_TYPE_ALL_SHARED_MEMORY    = D3D11_SHADER_TRACKING_RESOURCE_TYPE(5).value # call affects everything except device memory created without UAV bind flags
D3D11_SHADER_TRACKING_RESOURCE_TYPE_GROUPSHARED_NON_UAV  = D3D11_SHADER_TRACKING_RESOURCE_TYPE(6).value # call affects everything except device memory created with UAV bind flags
D3D11_SHADER_TRACKING_RESOURCE_TYPE_ALL                  = D3D11_SHADER_TRACKING_RESOURCE_TYPE(7).value # call affects all memory on the device


D3D11_SHADER_TRACKING_OPTION = ctypes.c_uint
D3D11_SHADER_TRACKING_OPTION_IGNORE                                       = D3D11_SHADER_TRACKING_OPTION(0).value
D3D11_SHADER_TRACKING_OPTION_TRACK_UNINITIALIZED                          = D3D11_SHADER_TRACKING_OPTION(0x1).value    # track reading uninitialized data
D3D11_SHADER_TRACKING_OPTION_TRACK_RAW                                    = D3D11_SHADER_TRACKING_OPTION(0x2).value    # track read-after-write hazards
D3D11_SHADER_TRACKING_OPTION_TRACK_WAR                                    = D3D11_SHADER_TRACKING_OPTION(0x4).value    # track write-after-read hazards
D3D11_SHADER_TRACKING_OPTION_TRACK_WAW                                    = D3D11_SHADER_TRACKING_OPTION(0x8).value    # track write-after-write hazards
D3D11_SHADER_TRACKING_OPTION_ALLOW_SAME                                   = D3D11_SHADER_TRACKING_OPTION(0x10).value   # allow a hazard if the data
D3D11_SHADER_TRACKING_OPTION_TRACK_ATOMIC_CONSISTENCY                     = D3D11_SHADER_TRACKING_OPTION(0x20).value   # make sure only one type of atomic is used on an address written didn't change the value
D3D11_SHADER_TRACKING_OPTION_TRACK_RAW_ACROSS_THREADGROUPS                = D3D11_SHADER_TRACKING_OPTION(0x40).value   # track read-after-write hazards across thread groups
D3D11_SHADER_TRACKING_OPTION_TRACK_WAR_ACROSS_THREADGROUPS                = D3D11_SHADER_TRACKING_OPTION(0x80).value   # track write-after-read hazards across thread groups
D3D11_SHADER_TRACKING_OPTION_TRACK_WAW_ACROSS_THREADGROUPS                = D3D11_SHADER_TRACKING_OPTION(0x100).value  # track write-after-write hazards across thread groups
D3D11_SHADER_TRACKING_OPTION_TRACK_ATOMIC_CONSISTENCY_ACROSS_THREADGROUPS = D3D11_SHADER_TRACKING_OPTION(0x200).value  # make sure only one type of atomic is used on an address across thread groups
D3D11_SHADER_TRACKING_OPTION_UAV_SPECIFIC_FLAGS                           = D3D11_SHADER_TRACKING_OPTION_TRACK_RAW_ACROSS_THREADGROUPS | D3D11_SHADER_TRACKING_OPTION_TRACK_WAR_ACROSS_THREADGROUPS | D3D11_SHADER_TRACKING_OPTION_TRACK_WAW_ACROSS_THREADGROUPS | D3D11_SHADER_TRACKING_OPTION_TRACK_ATOMIC_CONSISTENCY_ACROSS_THREADGROUPS # flags ignored for GSM
D3D11_SHADER_TRACKING_OPTION_ALL_HAZARDS                                  = D3D11_SHADER_TRACKING_OPTION_TRACK_RAW | D3D11_SHADER_TRACKING_OPTION_TRACK_WAR | D3D11_SHADER_TRACKING_OPTION_TRACK_WAW | D3D11_SHADER_TRACKING_OPTION_TRACK_ATOMIC_CONSISTENCY | D3D11_SHADER_TRACKING_OPTION_TRACK_RAW_ACROSS_THREADGROUPS | D3D11_SHADER_TRACKING_OPTION_TRACK_WAR_ACROSS_THREADGROUPS | D3D11_SHADER_TRACKING_OPTION_TRACK_WAW_ACROSS_THREADGROUPS | D3D11_SHADER_TRACKING_OPTION_TRACK_ATOMIC_CONSISTENCY_ACROSS_THREADGROUPS
D3D11_SHADER_TRACKING_OPTION_ALL_HAZARDS_ALLOWING_SAME                    = D3D11_SHADER_TRACKING_OPTION_ALL_HAZARDS | D3D11_SHADER_TRACKING_OPTION_ALLOW_SAME
D3D11_SHADER_TRACKING_OPTION_ALL_OPTIONS                                  = D3D11_SHADER_TRACKING_OPTION_ALL_HAZARDS_ALLOWING_SAME | D3D11_SHADER_TRACKING_OPTION_TRACK_UNINITIALIZED

class ID3D11TracingDevice(comtypes.IUnknown):
    _iid_ = comtypes.GUID("{1911c771-1587-413e-a7e0-fb26c3de0268}")
    _methods_ = [
        comtypes.STDMETHOD(comtypes.HRESULT, "SetShaderTrackingOptionsByType", [
            wintypes.UINT,
            wintypes.UINT,
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "SetShaderTrackingOptions", []),
    ]


class ID3D11RefTrackingOptions(comtypes.IUnknown):
    _iid_ = comtypes.GUID("{193dacdf-0db2-4c05-a55c-ef06cac56fd9}")
    _methods_ = [
        comtypes.STDMETHOD(comtypes.HRESULT, "SetTrackingOptions", [
            wintypes.UINT,  # UINT uOptions
            ]),
    ]


class ID3D11RefDefaultTrackingOptions(comtypes.IUnknown):
    _iid_ = comtypes.GUID("{03916615-c644-418c-9bf4-75db5be63ca0}")
    _methods_ = [
        comtypes.STDMETHOD(comtypes.HRESULT, "SetTrackingOptions", [
            wintypes.UINT,  # UINT ResourceTypeFlags
            wintypes.UINT,  # UINT Options
            ]),
    ]


## ==================================================================================================================================
## 
##  Info Queue
## 
## ==================================================================================================================================
D3D11_MESSAGE_CATEGORY = ctypes.c_uint
D3D11_MESSAGE_CATEGORY_APPLICATION_DEFINED   = D3D11_MESSAGE_CATEGORY(0).value
D3D11_MESSAGE_CATEGORY_MISCELLANEOUS         = D3D11_MESSAGE_CATEGORY(1).value
D3D11_MESSAGE_CATEGORY_INITIALIZATION        = D3D11_MESSAGE_CATEGORY(2).value
D3D11_MESSAGE_CATEGORY_CLEANUP               = D3D11_MESSAGE_CATEGORY(3).value
D3D11_MESSAGE_CATEGORY_COMPILATION           = D3D11_MESSAGE_CATEGORY(4).value
D3D11_MESSAGE_CATEGORY_STATE_CREATION        = D3D11_MESSAGE_CATEGORY(5).value
D3D11_MESSAGE_CATEGORY_STATE_SETTING         = D3D11_MESSAGE_CATEGORY(6).value
D3D11_MESSAGE_CATEGORY_STATE_GETTING         = D3D11_MESSAGE_CATEGORY(7).value
D3D11_MESSAGE_CATEGORY_RESOURCE_MANIPULATION = D3D11_MESSAGE_CATEGORY(8).value
D3D11_MESSAGE_CATEGORY_EXECUTION             = D3D11_MESSAGE_CATEGORY(9).value
D3D11_MESSAGE_CATEGORY_SHADER                = D3D11_MESSAGE_CATEGORY(10).value

D3D11_MESSAGE_SEVERITY = ctypes.c_uint
D3D11_MESSAGE_SEVERITY_CORRUPTION = D3D11_MESSAGE_SEVERITY(0).value
D3D11_MESSAGE_SEVERITY_ERROR      = D3D11_MESSAGE_SEVERITY(1).value
D3D11_MESSAGE_SEVERITY_WARNING    = D3D11_MESSAGE_SEVERITY(2).value
D3D11_MESSAGE_SEVERITY_INFO       = D3D11_MESSAGE_SEVERITY(3).value
D3D11_MESSAGE_SEVERITY_MESSAGE    = D3D11_MESSAGE_SEVERITY(4).value

D3D11_MESSAGE_ID = ctypes.c_uint
## a very long list of parameters

class D3D11_MESSAGE(comtypes.Structure):
    _fields_ = [("Category",  D3D11_MESSAGE_CATEGORY), 
                ("Severity", D3D11_MESSAGE_SEVERITY),
                ("ID", D3D11_MESSAGE_ID),
                ("pDescription", ctypes.c_char_p),
                ("DescriptionByteLength", ctypes.c_size_t),
    ]

class D3D11_INFO_QUEUE_FILTER_DESC(comtypes.Structure):
    _fields_ = [("NumCategories", wintypes.UINT),
                ("pCategoryList", ctypes.POINTER(D3D11_MESSAGE_CATEGORY)),
                ("NumSeverities", wintypes.UINT),
                ("pSeverityList", ctypes.POINTER(D3D11_MESSAGE_SEVERITY)),
                ("NumIDs"       , wintypes.UINT),
                ("pIDList"      , ctypes.POINTER(D3D11_MESSAGE_ID)),
    ]

class D3D11_INFO_QUEUE_FILTER(comtypes.Structure):
    _fields_ = [("AllowList", D3D11_INFO_QUEUE_FILTER_DESC),
                ("DenyList", D3D11_INFO_QUEUE_FILTER_DESC),

    ]

class ID3D11InfoQueue(comtypes.IUnknown):
    _iid_ = comtypes.GUID("{6543dbb6-1b48-42f5-ab82-e97ec74326f6}")
    _methods_ = [
        ## =========================================================================
        ##   Methods for configuring how much data is stored in the queue.
        comtypes.STDMETHOD(comtypes.HRESULT, "SetMessageCountLimit", [
            ctypes.c_ulonglong, # UINT64 MessageCountLimit
            ]),
        comtypes.STDMETHOD(None, "ClearStoredMessages", []),
        
        ## =========================================================================
        ##   Methods for retrieving data or statistics from the queue.
        comtypes.STDMETHOD(comtypes.HRESULT, "GetMessage", [
            ctypes.c_ulonglong,                 # _In_                                        UINT64          MessageIndex
            ctypes.POINTER(D3D11_MESSAGE),      # _Out_writes_bytes_opt_(*pMessageByteLength) D3D11_MESSAGE * pMessage
            ctypes.POINTER(comtypes.c_size_t),  # _Inout_                                     SIZE_T        * pMessageByteLength
            ]),
        comtypes.STDMETHOD(ctypes.c_ulonglong, "GetNumMessagesAllowedByStorageFilter", []),
        comtypes.STDMETHOD(ctypes.c_ulonglong, "GetNumMessagesDeniedByStorageFilter", []),
        comtypes.STDMETHOD(ctypes.c_ulonglong, "GetNumStoredMessages", []),
        comtypes.STDMETHOD(ctypes.c_ulonglong, "GetNumStoredMessagesAllowedByRetrievalFilter", []),
        comtypes.STDMETHOD(ctypes.c_ulonglong, "GetNumMessagesDiscardedByMessageCountLimit", []),
        comtypes.STDMETHOD(ctypes.c_ulonglong, "GetMessageCountLimit", []),

        ## =========================================================================
        ##   Methods for filtering what gets stored in the queue
        comtypes.STDMETHOD(comtypes.HRESULT, "AddStorageFilterEntries", [
            ctypes.POINTER(D3D11_INFO_QUEUE_FILTER), # _In_ D3D11_INFO_QUEUE_FILTER * pFilter
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "GetStorageFilter", []),
        comtypes.STDMETHOD(None, "ClearStorageFilter", []),
        comtypes.STDMETHOD(comtypes.HRESULT, "PushEmptyStorageFilter", []),
        comtypes.STDMETHOD(comtypes.HRESULT, "PushCopyOfStorageFilter", []),
        comtypes.STDMETHOD(comtypes.HRESULT, "PushStorageFilter", []),
        comtypes.STDMETHOD(None, "PopStorageFilter", []),
        comtypes.STDMETHOD(ctypes.c_uint, "GetStorageFilterStackSize", []),

        ## =========================================================================
        ##   Methods for filtering what gets read out of the queue by GetMessage().
        comtypes.STDMETHOD(comtypes.HRESULT, "AddRetrievalFilterEntries", []),
        comtypes.STDMETHOD(comtypes.HRESULT, "GetRetrievalFilter", []),
        comtypes.STDMETHOD(None, "ClearRetrievalFilter", []),
        comtypes.STDMETHOD(comtypes.HRESULT, "PushEmptyRetrievalFilter", []),
        comtypes.STDMETHOD(comtypes.HRESULT, "PushCopyOfRetrievalFilter", []),
        comtypes.STDMETHOD(comtypes.HRESULT, "PushRetrievalFilter", []),
        comtypes.STDMETHOD(comtypes.HRESULT, "PopRetrievalFilter", []),
        comtypes.STDMETHOD(ctypes.c_uint, "GetRetrievalFilterStackSize", []),

        ## =========================================================================
        ##   Methods for adding entries to the queue.
        comtypes.STDMETHOD(comtypes.HRESULT, "AddMessage", []),
        comtypes.STDMETHOD(comtypes.HRESULT, "AddApplicationMessage", []),
        ## =========================================================================
        ##   Methods for breaking on errors that pass the storage filter.
        comtypes.STDMETHOD(comtypes.HRESULT, "SetBreakOnCategory", []),
        comtypes.STDMETHOD(comtypes.HRESULT, "SetBreakOnSeverity", [
            D3D11_MESSAGE_SEVERITY, # _In_ D3D11_MESSAGE_SEVERITY Severity
            wintypes.BOOL,          # _In_ BOOL bEnable
            ]),

    ]