# -*- coding:utf-8 -*-
# ========================
# -- IMPORTED MODULES --
# ========================
# Python Import
import comtypes
import ctypes
import ctypes.wintypes as wintypes
import enum
import multiprocessing
import numpy
import os
import sys

# pyDXGID3D Import
import Direct3D.PyIdl.dxgi
import Direct3D.PyIdl.dxgiformat
import Direct3D.PyIdl.dxgitype

from OutputManager import *
from ThreadManager import *

# ========================
# -- GLOBAL VARIABLES --
# ========================

OutMgr = OutputManager()

WNDPROC = ctypes.WINFUNCTYPE(ctypes.c_int, wintypes.HWND, ctypes.c_uint, wintypes.WPARAM, wintypes.LPARAM)

CS_HREDRAW = 0x0002
CS_VREDRAW = 0x0001

E_UNEXPECTED = 0x8000FFFF#L # _HRESULT_TYPEDEF_(0x8000FFFFL)

IDC_ARROW = 32512


STATUS_WAIT_0 = 0x00000000#L
SW_SHOW = 5

WAIT_OBJECT_0 = STATUS_WAIT_0 + 0
WM_DESTROY = 2
WM_QUIT    = 0x0012
WM_SIZE    = 0x0005
WM_USER    = 0x0400

WS_OVERLAPPED       = 0x00000000#L
WS_CAPTION          = 0x00C00000#L
WS_SYSMENU          = 0x00080000#L
WS_THICKFRAME       = 0x00040000#L
WS_MINIMIZEBOX      = 0x00020000#L
WS_MAXIMIZEBOX      = 0x00010000#L   
WS_OVERLAPPEDWINDOW = (WS_OVERLAPPED | WS_CAPTION | WS_SYSMENU | WS_THICKFRAME | WS_MINIMIZEBOX | WS_MAXIMIZEBOX)

DUPL_RETURN = ctypes.c_uint
DUPL_RETURN_SUCCESS          = 0
DUPL_RETURN_ERROR_EXCPECTED  = 1
DUPL_RETURN_ERROR_UNEXPECTED = 2

OCCLUSION_STATUS_MSG = WM_USER

# PeekMessageA
PM_NOREMOVE = 0x0000
PM_REMOVE   = 0x0001
PM_NOYIELD  = 0x0002

# ===================
# -- LOCAL CLASS --
# ===================
class WNDCLASSEXW(ctypes.Structure): # https://docs.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-wndclassexw
	_fields_ = [('cbSize'       , ctypes.c_uint),
				('style'        , ctypes.c_uint),
				('lpfnWndProc'  , WNDPROC),
				('cbClsExtra'   , ctypes.c_int),
				('cbWndExtra'   , ctypes.c_int),
				('hInstance'    , wintypes.HANDLE), #typedef void *PVOID HANDLE HINSTANCE; ctypes.c_void_p
				('hIcon'        , wintypes.HICON),
				('hCursor'      , wintypes.HICON), #typedef void *PVOID HANDLE HICON HCURSOR;
				('hbrBackground', wintypes.HBRUSH), #typedef void *PVOID HANDLE HBRUSH;  
				('lpszMenuName' , wintypes.LPCWSTR),   
				('lpszClassName', wintypes.LPCWSTR),
				('hIconSm'      , wintypes.HICON),
				]

class RECT(ctypes.Structure): # https://docs.microsoft.com/en-us/windows/desktop/api/windef/ns-windef-rect
	_fields_ = [('left', ctypes.c_long),
				('top', ctypes.c_long),
				('right', ctypes.c_long),
				('bottom', ctypes.c_long)
				]
class POINT(ctypes.Structure): #https://docs.microsoft.com/en-us/previous-versions/dd162805(v=vs.85)
	_fields_ = [('x', ctypes.c_long),
				('y', ctypes.c_long),
				]

class MSG(ctypes.Structure): #https://docs.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-msg
	_fields_ = [('hwnd',wintypes.HWND),
				('message',ctypes.c_uint),
				('wParam',wintypes.WPARAM),
				('lParam',wintypes.LPARAM),
				('time',wintypes.DWORD),
				('pt', POINT),
				('lPrivate',wintypes.DWORD),
				]

# =======================
# -- LOCAL FUNCTIONS --
# =======================
def ProcessFailure(Device, Str, Title, hr, ExpectedErrors):
	TranslatedHr = None # wintypes.HRESULT
	if Device:
		print('Device Exist') # Due to POO of the c++, we need to get value from


def WndProc(hwnd, uMsg, wParam, lParam):
	if uMsg == WM_DESTROY:
		ctypes.windll.user32.PostQuitMessage(0)
	elif uMsg == WM_SIZE:
		OutMgr.WindowResize();
	else:
		return ctypes.windll.user32.DefWindowProcW(hwnd, uMsg, ctypes.c_ulonglong(wParam), ctypes.c_longlong(lParam))
	return 0

def WinMain():

	# Synchronization (wintypes.HANDLE)
	UnexpectedErrorEvent  = None
	ExpectedErrorEvent    = None 
	TerminateThreadsEvent = None
	# Window
	WindowHandle = None # wintypes.HWND


	# Window # SingleOutput is normally configure by ProcessCmdline(&SingleOutput)
	# By C++ Program, we can see that the SingleOutput is set @ -1
	SingleOutput = -1

	# Event used by the threads to signal an unexcpected error and we want to quit the app
	UnexpectedErrorEvent = ctypes.windll.kernel32.CreateEventW(None, True, False, None) # The ExW provide an access violation 0x00..01
	if not UnexpectedErrorEvent:
		ProcessFailure(None, u"UnexpectedErrorEvent creation failed", u"Error", E_UNEXPECTED)
		return 0
	# Event for when a thread encounters an expected error
	ExpectedErrorEvent = ctypes.windll.kernel32.CreateEventW(None, True, False, None)
	if not ExpectedErrorEvent:
		ProcessFailure(None, u"ExpectedErrorEvent creation failed", u"Error", E_UNEXPECTED)
		return 0
	# Event to tell spawned threads to quit
	TerminateThreadsEvent = ctypes.windll.kernel32.CreateEventW(None, True, False, None)
	if not TerminateThreadsEvent:
		ProcessFailure(None, u"TerminateThreadsEvent creation failed", u"Error", E_UNEXPECTED)
		return 0

	# Register Class
	Wc = WNDCLASSEXW()
	Wc.cbSize        = ctypes.sizeof(WNDCLASSEXW)
	Wc.style         = CS_HREDRAW | CS_VREDRAW
	Wc.lpfnWndProc   = WNDPROC(WndProc)
	Wc.cbClsExtra    = 0
	Wc.cbWndExtra    = 0
	Wc.hInstance     = ctypes.windll.kernel32.GetModuleHandleW(None)
	Wc.hIcon         = None
	Wc.hCursor       = ctypes.windll.user32.LoadCursorW(None, ctypes.c_wchar_p(IDC_ARROW))
	Wc.hbrBackground = None
	Wc.lpszMenuName  = None
	Wc.lpszClassName = u"WinMain"
	Wc.hIconSm       = None
	if not ctypes.windll.user32.RegisterClassExW(ctypes.byref(Wc)):
		raise ctypes.WinError()

	WindowRect = RECT()
	WindowRect.left   = 0
	WindowRect.top    = 0
	WindowRect.right  = 2560
	WindowRect.bottom = 1600
	ctypes.windll.user32.AdjustWindowRectEx(ctypes.byref(WindowRect), WS_OVERLAPPEDWINDOW , False, 0)

	WindowHandle = ctypes.windll.user32.CreateWindowExW(0, Wc.lpszClassName, u"DXGI desktop duplication sample",
		ctypes.c_int(WS_OVERLAPPEDWINDOW),
		0,0,
		WindowRect.right - WindowRect.left, WindowRect.bottom - WindowRect.top,
		None, None, ctypes.c_ulonglong(Wc.hInstance), None)

	if not WindowHandle:
		raise ctypes.WinError()

	ctypes.windll.user32.ShowWindow(WindowHandle, SW_SHOW)
	ctypes.windll.user32.UpdateWindow(WindowHandle)

	
	# Quick test to check if everything is OK
	# msg = MSG()
	# while ctypes.windll.user32.GetMessageW(ctypes.byref(msg), None, 0, 0) != 0:
	# 	ctypes.windll.user32.TranslateMessage(ctypes.byref(msg))
	# 	ctypes.windll.user32.DispatchMessageW(ctypes.byref(msg))

	ThreadMgr = ThreadManager()
	DeskBounds = RECT()
	OutputCount = ctypes.c_uint(0) # UINT
	msg = MSG()
	FirstTime = True
	Occluded  = True
	numModes  = 1024
	modes = (Direct3D.PyIdl.dxgitype.DXGI_MODE_DESC * 1024)()
	while (WM_QUIT != msg.message):
		Ret = DUPL_RETURN_SUCCESS
		if ctypes.windll.user32.PeekMessageW(ctypes.byref(msg), None, 0,0, PM_REMOVE):
			if (msg.message == OCCLUSION_STATUS_MSG):
				Occluded = False
			else:
				ctypes.windll.user32.TranslateMessage(ctypes.byref(msg))
				ctypes.windll.user32.DispatchMessageW(ctypes.byref(msg))
		elif ctypes.windll.kernel32.WaitForSingleObjectEx(UnexpectedErrorEvent, 0, False) == WAIT_OBJECT_0:
			# Unexcpected error occured so exit the application
			break
		elif (FirstTime or ctypes.windll.kernel32.WaitForSingleObjectEx(ExpectedErrorEvent, 0, False) == WAIT_OBJECT_0):
			if not FirstTime:
				# Terminate other Threads
				print("Terminate other threads")
				ctypes.windll.kernel32.SetEvent(TerminateThreadsEvent)
				ThreadMgr.WaitForThreadTermination()
				ctypes.windll.kernel32.ResetEvent(TerminateThreadsEvent)
				ctypes.windll.kernel32.ResetEvent(ExpectedErrorEvent)

				# Clean up
				ThreadMgr.Clean()
				OutMgr.CleanRefs()

				# As we have encounter an error due to a system transition we wait before trying again, using this dynamic wait
				# the wait period will get progessively long to avoid wasting too much system resource if this state lasts a long time
				DynamicWait.Wait()
			else:
				# First time through the loop so nothing to clean up
				FirstTime = False

			# Re-initialize
			Ret = OutMgr.InitOutput(WindowHandle, SingleOutput, ctypes.byref(OutputCount), DeskBounds)
			if (Ret == 0):
				print("OutMgr.InitOuput success!")
				sharedHandle = OutMgr.GetSharedHandle()
				if sharedHandle:
					Ret = 0
					#Ret = ThreadMgr.Initialize(SingleOutput, OutputCount, UnexpectedErrorEvent, ExpectedErrorEvent, TerminateThreadsEvent, sharedHandle, ctypes.byref(DeskBounds))
				else:
					print("Failed to get handle of shared surface")
					Ret = 2 # DUPL_RETURN_ERROR_UNEXPECTED
			Occluded = True
		else:
			if not Occluded:
				Ret = OutMgr.UpdateApplicationWindow(ThreadMgr.GetPointerInfo(), ctypes.byref(Occluded))

		# check if for errors
# ============
# -- MAIN --
# ============
# ****************************************************************************
# main() :
# Parameters : None
# Returns    : None
# ****************************************************************************
if __name__ == '__main__':
	
	print(OutMgr)
	#del OutMgr # destroy the object
	sys.exit(WinMain())


# =============================
# -- REFERENCE -- WEB LINK --
# =============================
# ===================
# -- End Of File --
# ===================

