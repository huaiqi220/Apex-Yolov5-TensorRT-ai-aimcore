#ThreadManager

class ThreadManager:
	#public
	def __init__(self): # THREADMANAGER();
		print("ThreadManager init()")
		self.__mPtrInfo        = None # PTR_INFO m_PtrInfo
		self.__m_ThreadHandles = None # _Field_size_(m_ThreadCount) HANDLE* m_ThreadHandles;
		self.__m_ThreadData    = None # _Field_size_(m_ThreadCount) THREAD_DATA* m_ThreadData;

	def __del__(self): # ~THREADMANAGER();
		print("ThreadManager del")

	def Clean(self):
		return 0 # return void

	def Initialize(self):
		return 0 # return DUPL_RETURN

	def GetPointerInfo(self):
		return 0 # return PTR_INFO*

	def WaitForThreadTermination(self):
		return 0 # return void

	#private
	def __InitializeDx(self):
		return 0 # return DUPL_RETURN

	def __CleanDx(self):
		return 0 # return void
