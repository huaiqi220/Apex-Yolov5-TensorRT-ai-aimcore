// DXGICaptureSample.cpp : Defines the entry point for the console application.
//


#include "stdafx.h"
#include "DXGIManager.h"
#include "string"
#include <chrono>
#include <iostream>

using namespace std;


DXGIManager g_DXGIManager;



int getBmpFrame()
{
	printf("DXGICaptureSample. Fast windows screen capture\n");
	printf("Capturing desktop to: capture.bmp\n");
	printf("Log: logfile.log\n");

	CoInitialize(NULL);


	g_DXGIManager.SetCaptureSource(CSDesktop);

	RECT rcDim;
	g_DXGIManager.GetOutputRect(rcDim);

	DWORD dwWidth = rcDim.right - rcDim.left;
	DWORD dwHeight = rcDim.bottom - rcDim.top;



	printf("dwWidth=%d dwHeight=%d\n", dwWidth, dwHeight);

	DWORD dwBufSize = dwWidth*dwHeight*4;
	for (int j = 0; j < 10; j++)
	{
		
		std::chrono::milliseconds ms = std::chrono::duration_cast<std::chrono::milliseconds>(
			std::chrono::system_clock::now().time_since_epoch()
		);

		std::cout << ms.count() << std::endl;
		
		BYTE* pBuf = new BYTE[dwBufSize];

		CComPtr<IWICImagingFactory> spWICFactory = NULL;
		HRESULT hr = spWICFactory.CoCreateInstance(CLSID_WICImagingFactory);
		if (FAILED(hr))
			return hr;

		int i = 0;
		do
		{
			hr = g_DXGIManager.GetOutputBits(pBuf, rcDim);
			i++;
		} while (hr == DXGI_ERROR_WAIT_TIMEOUT || i < 2);

		if (FAILED(hr))
		{
			printf("GetOutputBits failed with hr=0x%08x\n", hr);
			return hr;
		}

		printf("Saving capture to file\n");

		CComPtr<IWICBitmap> spBitmap = NULL;
		hr = spWICFactory->CreateBitmapFromMemory(dwWidth, dwHeight, GUID_WICPixelFormat32bppBGRA, dwWidth * 4, dwBufSize, (BYTE*)pBuf, &spBitmap);
		if (FAILED(hr))
			return hr;

		CComPtr<IWICStream> spStream = NULL;

		hr = spWICFactory->CreateStream(&spStream);
		if (SUCCEEDED(hr)) {

			hr = spStream->InitializeFromFilename(L"capture.bmp", GENERIC_WRITE);
		}

		CComPtr<IWICBitmapEncoder> spEncoder = NULL;
		if (SUCCEEDED(hr)) {
			hr = spWICFactory->CreateEncoder(GUID_ContainerFormatBmp, NULL, &spEncoder);
		}

		if (SUCCEEDED(hr)) {
			hr = spEncoder->Initialize(spStream, WICBitmapEncoderNoCache);
		}

		CComPtr<IWICBitmapFrameEncode> spFrame = NULL;
		if (SUCCEEDED(hr)) {
			hr = spEncoder->CreateNewFrame(&spFrame, NULL);
		}

		if (SUCCEEDED(hr)) {
			hr = spFrame->Initialize(NULL);
		}

		if (SUCCEEDED(hr)) {
			hr = spFrame->SetSize(dwWidth, dwHeight);
		}

		WICPixelFormatGUID format;
		spBitmap->GetPixelFormat(&format);

		if (SUCCEEDED(hr)) {
			hr = spFrame->SetPixelFormat(&format);
		}

		if (SUCCEEDED(hr)) {
			hr = spFrame->WriteSource(spBitmap, NULL);
		}

		if (SUCCEEDED(hr)) {
			hr = spFrame->Commit();
		}

		if (SUCCEEDED(hr)) {
			hr = spEncoder->Commit();
		}

		delete[] pBuf;
	}
	

	return 0;
}

int main() {
	getBmpFrame();


}

