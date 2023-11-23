##
##   Copyright (C) Microsoft.  All rights reserved.
##   Windows Kits version 10.0.19041.0
##
##   Translate in Python by J. Vnh
##
import ctypes
import ctypes.wintypes as wintypes

import comtypes

from Direct3D.PyIdl.dxgi import *
from Direct3D.PyIdl.dxgicommon import *
from Direct3D.PyIdl.dxgiformat import *
from Direct3D.PyIdl.dxgitype import *
from Direct3D.PyIdl.d3d11 import *

class IDXGIDisplayControl(comtypes.IUnknown):
    _iid_ = comtypes.GUID("{ea9dbf1a-c88e-4486-854a-98aa0138f30c}")
    _methods_ = [
        comtypes.STDMETHOD(ctypes.c_bool, "IsStereoEnabled",  [ ]),
        comtypes.STDMETHOD(None,          "SetStereoEnabled", [
            wintypes.BOOL,
            ]), 
    ]


## --------------------------------------------------------------------------------------------------------
##  IDXGIOutputDuplication structures
## --------------------------------------------------------------------------------------------------------

class DXGI_OUTDUPL_MOVE_RECT(ctypes.Structure):
    _fields_ = [('SourcePoint',     wintypes.POINT),
                ('DestinationRect', wintypes.RECT),
    ]

class DXGI_OUTDUPL_DESC(ctypes.Structure):
    _fields_ = [('ModeDesc',                   DXGI_MODE_DESC),
                ('Rotation',                   DXGI_MODE_ROTATION),
                ('DesktopImageInSystemMemory', wintypes.BOOL),
    ]

class DXGI_OUTDUPL_POINTER_POSITION(ctypes.Structure):
    _fields_ = [('Position', wintypes.POINT),
                ('Visible',  wintypes.UINT),
    ]

DXGI_OUTDUPL_POINTER_SHAPE_TYPE = ctypes.c_uint
DXGI_OUTDUPL_POINTER_SHAPE_TYPE_MONOCHROME     = DXGI_OUTDUPL_POINTER_SHAPE_TYPE(0x00000001)
DXGI_OUTDUPL_POINTER_SHAPE_TYPE_COLOR          = DXGI_OUTDUPL_POINTER_SHAPE_TYPE(0x00000002)
DXGI_OUTDUPL_POINTER_SHAPE_TYPE_MASKED_COLOR   = DXGI_OUTDUPL_POINTER_SHAPE_TYPE(0x00000004)

class DXGI_OUTDUPL_POINTER_SHAPE_INFO(ctypes.Structure):
    _fields_ = [('Type',    wintypes.UINT),
                ('Width',   wintypes.UINT),
                ('Height',  wintypes.UINT),
                ('Pitch',   wintypes.UINT),
                ('HotSpot', wintypes.POINT),
    ]

class DXGI_OUTDUPL_FRAME_INFO(ctypes.Structure):
    _fields_ = [('LastPresentTime',           wintypes.LARGE_INTEGER),
                ('LastMouseUpdateTime',       wintypes.LARGE_INTEGER),
                ('AccumulatedFrames',         wintypes.UINT),
                ('RectsCoalesced',            wintypes.BOOL),
                ('ProtectedContentMaskedOut', wintypes.BOOL),
                ('PointerPosition',           DXGI_OUTDUPL_POINTER_POSITION),
                ('TotalMetadataBufferSize',   wintypes.UINT),
                ('PointerShapeBufferSize',    wintypes.UINT),
    ]

## --------------------------------------------------------------------------------------------------------
##  IDXGIOutputDuplication interface
## --------------------------------------------------------------------------------------------------------
class IDXGIOutputDuplication(IDXGIObject):
    _iid_ = comtypes.GUID("{191cfac3-a341-470d-b26e-a864f428319c}")
    _methods_ = [
        comtypes.STDMETHOD(None,"GetDesc", [
            ctypes.POINTER(DXGI_OUTDUPL_DESC),
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT,"AcquireNextFrame", [
            wintypes.UINT,
            ctypes.POINTER(DXGI_OUTDUPL_FRAME_INFO),
            ctypes.POINTER(ctypes.POINTER(IDXGIResource)),
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT,"GetFrameDirtyRects", [
            wintypes.UINT,
            ctypes.POINTER(wintypes.RECT),
            ctypes.POINTER(wintypes.UINT),
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT,"GetFrameMoveRects", [
            wintypes.UINT,
            ctypes.POINTER(DXGI_OUTDUPL_MOVE_RECT),
            ctypes.POINTER(wintypes.UINT),
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT,"GetFramePointerShape", [
            wintypes.UINT,
            ctypes.c_void_p,
            ctypes.POINTER(wintypes.UINT),
            ctypes.POINTER(DXGI_OUTDUPL_POINTER_SHAPE_INFO),
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT,"MapDesktopSurface", [
            ctypes.POINTER(DXGI_MAPPED_RECT),
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT,"UnMapDesktopSurface", []),
        comtypes.STDMETHOD(comtypes.HRESULT,"ReleaseFrame", []),
    ]

DXGI_ALPHA_MODE = ctypes.c_uint
DXGI_ALPHA_MODE_UNSPECIFIED   = DXGI_ALPHA_MODE(0)
DXGI_ALPHA_MODE_PREMULTIPLIED = DXGI_ALPHA_MODE(1)
DXGI_ALPHA_MODE_STRAIGHT      = DXGI_ALPHA_MODE(2)
DXGI_ALPHA_MODE_IGNORE        = DXGI_ALPHA_MODE(3)
DXGI_ALPHA_MODE_FORCE_DWORD   = DXGI_ALPHA_MODE(0xffffffff)

class IDXGISurface2(IDXGISurface1):
    _iid_ = comtypes.GUID("{aba496dd-b617-4cb8-a866-bc44d7eb1fa2}")
    _methods_ = [
        comtypes.STDMETHOD(comtypes.HRESULT, "GetResource", [
            ctypes.POINTER(comtypes.GUID),
            ctypes.POINTER(ctypes.c_void_p),
            ctypes.POINTER(wintypes.UINT),
            ]),
    ]

class SECURITY_ATTRIBUTES(ctypes.Structure):
    _fields_ = [('nLength',              wintypes.DWORD),
                ('lpSecurityDescriptor', wintypes.LPVOID),
                ('bInheritHandle',       wintypes.BOOL),
    ]

class IDXGIResource1(IDXGIResource):
    _iid_ = comtypes.GUID("{30961379-4609-4a41-998e-54fe567ee0c1}")
    _methods_ = [
        comtypes.STDMETHOD(comtypes.HRESULT, "CreateSubresourceSurface", [
            wintypes.UINT,
            ctypes.POINTER(ctypes.POINTER(IDXGISurface2)),
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "CreateSharedHandle", [
            ctypes.POINTER(SECURITY_ATTRIBUTES),
            wintypes.DWORD,
            wintypes.LPCWSTR,
            ctypes.POINTER(wintypes.HANDLE),
            ])
    ]

DXGI_OFFER_RESOURCE_PRIORITY        = ctypes.c_uint
DXGI_OFFER_RESOURCE_PRIORITY_LOW    = DXGI_OFFER_RESOURCE_PRIORITY(1)
DXGI_OFFER_RESOURCE_PRIORITY_NORMAL = DXGI_OFFER_RESOURCE_PRIORITY(2)
DXGI_OFFER_RESOURCE_PRIORITY_HIGH   = DXGI_OFFER_RESOURCE_PRIORITY(3)

class IDXGIDevice2(IDXGIDevice1):
    _iid_ = comtypes.GUID("{05008617-fbfd-4051-a790-144884b4f6a9}")
    _methods_ = [
        comtypes.STDMETHOD(comtypes.HRESULT, "OfferResources", [
            wintypes.UINT,
            ctypes.POINTER(ctypes.POINTER(IDXGIResource)),
            DXGI_OFFER_RESOURCE_PRIORITY,
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "ReclaimResources", [
            wintypes.UINT,
            ctypes.POINTER(ctypes.POINTER(IDXGIResource)),
            ctypes.POINTER(wintypes.BOOL),
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "EnqueueSetEvent", [
            wintypes.HANDLE,
            ]),
    ]

DXGI_ENUM_MODES_STEREO          = 4 ## 4UL
DXGI_ENUM_MODES_DISABLED_STEREO = 8 ## 8UL
DXGI_SHARED_RESOURCE_READ       = 0x80000000
DXGI_SHARED_RESOURCE_WRITE      = 1

class DXGI_MODE_DESC1(ctypes.Structure):
    _fields_ = [('Width',            wintypes.UINT),
                ('Height',           wintypes.UINT),
                ('RefreshRate',      DXGI_RATIONAL),
                ('Format',           DXGI_FORMAT),
                ('ScanlineOrdering', DXGI_MODE_SCANLINE_ORDER),
                ('Scaling',          DXGI_MODE_SCALING),
                ('Stereo',           wintypes.BOOL),
    ]


## --------------------------------------------------------------------------------------------------------
##  IDXGISwapchain1 structures
## --------------------------------------------------------------------------------------------------------
DXGI_SCALING = ctypes.c_uint
DXGI_SCALING_STRETCH              = DXGI_SCALING(0)
DXGI_SCALING_NONE                 = DXGI_SCALING(1)
DXGI_SCALING_ASPECT_RATIO_STRETCH = DXGI_SCALING(2)

class DXGI_SWAP_CHAIN_DESC1(ctypes.Structure):
    _fields_ = [('Width',       wintypes.UINT),
                ('Height',      wintypes.UINT),
                ('Format',      DXGI_FORMAT),
                ('Stereo',      wintypes.BOOL),
                ('SampleDesc',  DXGI_SAMPLE_DESC),
                ('BufferUsage', DXGI_USAGE),
                ('BufferCount', wintypes.UINT),
                ('Scaling',     DXGI_SCALING),
                ('SwapEffect',  DXGI_SWAP_EFFECT),
                ('AlphaMode',   DXGI_ALPHA_MODE),
                ('Flags',       wintypes.UINT), ## DXGI_SWAP_CHAIN_FLAG
    ]

class DXGI_SWAP_CHAIN_FULLSCREEN_DESC(ctypes.Structure):
    _fields_ = [('RefreshRate',      DXGI_RATIONAL),
                ('ScanlineOrdering', DXGI_MODE_SCANLINE_ORDER),
                ('Scaling',          DXGI_MODE_SCALING),
                ('Windowed',         wintypes.BOOL),
    ]

class DXGI_PRESENT_PARAMETERS(ctypes.Structure):
    _fields_ = [('DirtyRectsCount', ctypes.c_uint),
                ('pDirtyRects', ctypes.POINTER(wintypes.RECT)),
                ('pScrollRect', ctypes.POINTER(wintypes.RECT)),
                ('pScrollOffset', ctypes.POINTER(wintypes.POINT)),
    ]

##--------------------------------------------------------------------------------------------------------
## IDXGISwapChain1 interface
##--------------------------------------------------------------------------------------------------------
class IDXGISwapChain1(IDXGISwapChain):
    _iid_ = comtypes.GUID("{790a45f7-0d42-4876-983a-0a55cfe6f4aa}")
    _methods_ = [
        comtypes.STDMETHOD(comtypes.HRESULT, "GetDesc1", [
            ctypes.POINTER(DXGI_SWAP_CHAIN_DESC1),
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "GetFullscreenDesc", [
            ctypes.POINTER(DXGI_SWAP_CHAIN_FULLSCREEN_DESC),
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "GetHwnd", [
            ctypes.POINTER(wintypes.HWND),
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "GetCoreWindow", [
            ctypes.POINTER(comtypes.GUID),
            ctypes.POINTER(ctypes.c_void_p),
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "Present1", [
            wintypes.BOOL,
            wintypes.BOOL,
            ctypes.POINTER(DXGI_PRESENT_PARAMETERS),
            ]),
        comtypes.STDMETHOD(wintypes.BOOL, "IsTemporaryMonoSupported", []),
        comtypes.STDMETHOD(comtypes.HRESULT, "GetRestrictToOutput", [
            ctypes.POINTER(ctypes.POINTER(IDXGIOutput)),
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "SetBackgroundColor", [
            ctypes.POINTER(DXGI_RGBA),
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "GetBackgroundColor", [
            ctypes.POINTER(DXGI_RGBA),
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "SetRotation", [
            DXGI_MODE_ROTATION,
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "GetRotation", [
            ctypes.POINTER(DXGI_MODE_ROTATION),
            ]),
    ]


## --------------------------------------------------------------------------------------------------------
##  IDXGIFactory2 interface
## --------------------------------------------------------------------------------------------------------
class IDXGIFactory2(IDXGIFactory1):
    _iid_ = comtypes.GUID("{50c83a1c-e072-4c48-87b0-3630fa36a6d0}")
    _methods_ = [
        comtypes.STDMETHOD(wintypes.BOOL , "IsWindowedStereoEnabled", []),
        comtypes.STDMETHOD(comtypes.HRESULT, "CreateSwapChainForHwnd", [
            ctypes.POINTER(comtypes.IUnknown),
            wintypes.HWND,
            ctypes.POINTER(DXGI_SWAP_CHAIN_DESC1),
            ctypes.POINTER(DXGI_SWAP_CHAIN_FULLSCREEN_DESC),
            ctypes.POINTER(IDXGIOutput),
            ctypes.POINTER(ctypes.POINTER(IDXGISwapChain1)),
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "CreateSwapChainForCoreWindow", [
            ctypes.POINTER(comtypes.IUnknown),
            ctypes.POINTER(comtypes.IUnknown),
            ctypes.POINTER(DXGI_SWAP_CHAIN_DESC1),
            ctypes.POINTER(IDXGIOutput),
            ctypes.POINTER(ctypes.POINTER(IDXGISwapChain1)),
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "GetSharedResourceAdapterLuid", [
            wintypes.HANDLE,
            LUID,
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "RegisterStereoStatusWindow", [
            wintypes.HWND,
            wintypes.UINT,
            ctypes.POINTER(wintypes.DWORD),
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "RegisterStereoStatusEvent", [
            wintypes.HANDLE,
            ctypes.POINTER(wintypes.DWORD),
            ]),
        comtypes.STDMETHOD(ctypes.c_void_p , "UnregisterStereoStatus", [
            wintypes.DWORD,
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "RegisterOcclusionStatusWindow", [
            wintypes.HWND,
            wintypes.UINT,
            ctypes.POINTER(wintypes.DWORD),
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "RegisterOcclusionStatusEvent", [
            wintypes.HANDLE,
            ctypes.POINTER(wintypes.DWORD),
            ]),
        comtypes.STDMETHOD(ctypes.c_void_p , "UnregisterOcclusionStatus", [
            wintypes.DWORD,
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "CreateSwapChainForComposition", [
            ctypes.POINTER(comtypes.IUnknown),
            ctypes.POINTER(DXGI_SWAP_CHAIN_DESC1),
            ctypes.POINTER(IDXGIOutput),
            ctypes.POINTER(ctypes.POINTER(IDXGISwapChain1)),
            ]),
    ]


## --------------------------------------------------------------------------------------------------------
##  IDXGIAdapter2 structures
## --------------------------------------------------------------------------------------------------------
DXGI_GRAPHICS_PREEMPTION_GRANULARITY = ctypes.c_uint
DXGI_GRAPHICS_PREEMPTION_DMA_BUFFER_BOUNDARY    = DXGI_GRAPHICS_PREEMPTION_GRANULARITY(0)
DXGI_GRAPHICS_PREEMPTION_PRIMITIVE_BOUNDARY     = DXGI_GRAPHICS_PREEMPTION_GRANULARITY(1)
DXGI_GRAPHICS_PREEMPTION_TRIANGLE_BOUNDARY      = DXGI_GRAPHICS_PREEMPTION_GRANULARITY(2)
DXGI_GRAPHICS_PREEMPTION_PIXEL_BOUNDARY         = DXGI_GRAPHICS_PREEMPTION_GRANULARITY(3)
DXGI_GRAPHICS_PREEMPTION_INSTRUCTION_BOUNDARY   = DXGI_GRAPHICS_PREEMPTION_GRANULARITY(4)

DXGI_COMPUTE_PREEMPTION_GRANULARITY = ctypes.c_uint
DXGI_COMPUTE_PREEMPTION_DMA_BUFFER_BOUNDARY      = DXGI_COMPUTE_PREEMPTION_GRANULARITY(0)
DXGI_COMPUTE_PREEMPTION_DISPATCH_BOUNDARY        = DXGI_COMPUTE_PREEMPTION_GRANULARITY(1)
DXGI_COMPUTE_PREEMPTION_THREAD_GROUP_BOUNDARY    = DXGI_COMPUTE_PREEMPTION_GRANULARITY(2)
DXGI_COMPUTE_PREEMPTION_THREAD_BOUNDARY          = DXGI_COMPUTE_PREEMPTION_GRANULARITY(3)
DXGI_COMPUTE_PREEMPTION_INSTRUCTION_BOUNDARY     = DXGI_COMPUTE_PREEMPTION_GRANULARITY(4)

class DXGI_ADAPTER_DESC2(ctypes.Structure):
    _fields_ = [('Description',           wintypes.WCHAR * 128),
                ('VendorId',              wintypes.UINT),
                ('DeviceId',              wintypes.UINT),
                ('SubSysId',              wintypes.UINT),
                ('Revision',              wintypes.UINT),
                ('DedicatedVideoMemory',  ctypes.c_size_t),
                ('DedicatedSystemMemory', ctypes.c_size_t),
                ('SharedSystemMemory',    ctypes.c_size_t),
                ('AdapterLuid',           LUID),
                ('Flags',                 wintypes.UINT),
                ('GraphicsPreemptionGranularity', DXGI_GRAPHICS_PREEMPTION_GRANULARITY),
                ('ComputePreemptionGranularity',  DXGI_GRAPHICS_PREEMPTION_GRANULARITY),
    ]


## --------------------------------------------------------------------------------------------------------
##  IDXGIAdapter2 interface
## --------------------------------------------------------------------------------------------------------
class IDXGIAdapter2(IDXGIAdapter1):
    _iid_ = comtypes.GUID("{0AA1AE0A-FA0E-4B84-8644-E05FF8E5ACB5}")
    _methods_ = [
        comtypes.STDMETHOD(comtypes.HRESULT, "GetDesc2", [
            ctypes.POINTER(DXGI_ADAPTER_DESC2),
            ]),
    ]


## --------------------------------------------------------------------------------------------------------
##  IDXGIOutput1
## --------------------------------------------------------------------------------------------------------
class IDXGIOutput1(IDXGIOutput):
    _iid_ = comtypes.GUID("{00cddea8-939b-4b83-a340-a685226666cc}")
    _methods_ = [
        comtypes.STDMETHOD(comtypes.HRESULT, "GetDisplayModeList1", [
            DXGI_FORMAT,
            wintypes.UINT,
            ctypes.POINTER(wintypes.UINT),
            ctypes.POINTER(DXGI_MODE_DESC1),
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "FindClosestMatchingMode1", [
            ctypes.POINTER(DXGI_MODE_DESC1),
            ctypes.POINTER(DXGI_MODE_DESC1),
            ctypes.POINTER(comtypes.IUnknown),
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "GetDisplaySurfaceData1", [
            ctypes.POINTER(IDXGIResource),
            ]),
        comtypes.STDMETHOD(comtypes.HRESULT, "DuplicateOutput", [
            ctypes.POINTER(ID3D11Device),
            ctypes.POINTER(ctypes.POINTER(IDXGIOutputDuplication)),
            ]),
    ]


## --------------------------------------------------------------------------------------------------------
##  End of file
## --------------------------------------------------------------------------------------------------------