// #include <WICTextureLoader.h>
//#include <ScreenGrab.h>
//#include <DirectXTex.h>

#include <directxmath.h>
#include <d3d11_2.h>
#include "PixelShader.h"
#include "VertexShader.h"

#pragma comment (lib, "d3d11.lib")

using namespace DirectX;

IDXGISwapChain *swapchain;             
ID3D11Device *device;                  
ID3D11DeviceContext *deviceContext;    
ID3D11RenderTargetView *backbuffer;    

IDXGIOutputDuplication* outputDuplication;
ID3D11Texture2D* acquiredDesktopImage;

ID3D11VertexShader* VertexShader;
ID3D11PixelShader* PixelShader;
ID3D11InputLayout* InputLayout;
ID3D11Buffer* VertexBuffer;

ID3D11RenderTargetView* renderTargetView;
ID3D11Texture2D* renderTargetTexture;
ID3D11ShaderResourceView* renderTargetResourceView;
ID3D11SamplerState* pointSamplerState;

typedef struct _VERTEX
{
	XMFLOAT3 Pos;
	XMFLOAT2 TexCoord;
} VERTEX;
const int ox = 1280;
const int oy = 720;

#define NUMVERTICES 6
UINT Stride = sizeof(VERTEX);
UINT Offset = 0;
VERTEX Vertices[NUMVERTICES] =
{
	{ XMFLOAT3(-1.0f, -1.0f, 0.0f), XMFLOAT2(0.0f, 1.0f) },
	{ XMFLOAT3(-1.0f, 1.0f, 0.0f), XMFLOAT2(0.0f, 0.0f) },
	{ XMFLOAT3(1.0f, -1.0f, 0.0f), XMFLOAT2(1.0f, 1.0f) },
	{ XMFLOAT3(1.0f, -1.0f, 0.0f), XMFLOAT2(1.0f, 1.0f) },
	{ XMFLOAT3(-1.0f, 1.0f, 0.0f), XMFLOAT2(0.0f, 0.0f) },
	{ XMFLOAT3(1.0f, 1.0f, 0.0f), XMFLOAT2(1.0f, 0.0f) },
};

D3D11_VIEWPORT renderTargetViewport;
D3D11_VIEWPORT windowViewport;


// this function initializes and prepares Direct3D for use
void InitD3D(HWND hWnd)
{
	int outputNum = 0;

	// create a struct to hold information about the swap chain
	DXGI_SWAP_CHAIN_DESC scd;

	// clear out the struct for use
	ZeroMemory(&scd, sizeof(DXGI_SWAP_CHAIN_DESC));

	// fill the swap chain description struct
	scd.BufferCount = 1;                                    // one back buffer
	scd.BufferDesc.Format = DXGI_FORMAT_R8G8B8A8_UNORM;     // use 32-bit color
	scd.BufferUsage = DXGI_USAGE_RENDER_TARGET_OUTPUT;      // how swap chain is to be used
	scd.OutputWindow = hWnd;                                // the window to be used
	scd.SampleDesc.Count = 4;                               // how many multisamples
	scd.Windowed = TRUE;                                    // windowed/full-screen mode
	//scd.SwapEffect = DXGI_SWAP_EFFECT_FLIP_SEQUENTIAL;
	//scd.BufferCount = 2;
	//scd.SampleDesc.Count = 1;
	//scd.SampleDesc.Quality = 0;

	HRESULT hr = D3D11CreateDeviceAndSwapChain(NULL,
		D3D_DRIVER_TYPE_HARDWARE,
		NULL,
		NULL,  
		NULL,
		NULL,
		D3D11_SDK_VERSION,
		&scd,
		&swapchain,
		&device,
		NULL,
		&deviceContext);

	if (FAILED(hr))
		return;

	IDXGIDevice* dxgiDevice = nullptr;
	hr = device->QueryInterface(__uuidof(IDXGIDevice), reinterpret_cast<void**>(&dxgiDevice));
	if (FAILED(hr))
		return;

	IDXGIAdapter* dxgiAdapter = nullptr;
	hr = dxgiDevice->GetParent(__uuidof(IDXGIAdapter), reinterpret_cast<void**>(&dxgiAdapter));
	if (FAILED(hr))
		return;
	dxgiDevice->Release();

	// Select correct output
	IDXGIOutput* dxgiOutput = nullptr;
	hr = dxgiAdapter->EnumOutputs(outputNum, &dxgiOutput);
	if (FAILED(hr))
		return;
	dxgiAdapter->Release();

	IDXGIOutput1* dxgiOutput1 = nullptr;
	hr = dxgiOutput->QueryInterface(__uuidof(IDXGIOutput1), reinterpret_cast<void**>(&dxgiOutput1));
	if (FAILED(hr))
		return;

	dxgiOutput->Release();

	// Set duplication
	hr = dxgiOutput1->DuplicateOutput(device, &outputDuplication);
	if (FAILED(hr))
		return;

	dxgiOutput1->Release();

	// Create rendertargetview for the backbuffer
	ID3D11Texture2D *pBackBuffer;
	hr = swapchain->GetBuffer(0, __uuidof(ID3D11Texture2D), (LPVOID*)&pBackBuffer);

	if (FAILED(hr))
		return;

	device->CreateRenderTargetView(pBackBuffer, NULL, &backbuffer);
	pBackBuffer->Release();

	// Create the sampler state
	D3D11_SAMPLER_DESC SampDesc;
	RtlZeroMemory(&SampDesc, sizeof(SampDesc));
	SampDesc.Filter = D3D11_FILTER_MIN_MAG_MIP_POINT;
	SampDesc.AddressU = D3D11_TEXTURE_ADDRESS_CLAMP;
	SampDesc.AddressV = D3D11_TEXTURE_ADDRESS_CLAMP;
	SampDesc.AddressW = D3D11_TEXTURE_ADDRESS_CLAMP;
	SampDesc.ComparisonFunc = D3D11_COMPARISON_NEVER;
	SampDesc.MinLOD = 0;
	SampDesc.MaxLOD = D3D11_FLOAT32_MAX;
	hr = device->CreateSamplerState(&SampDesc, &pointSamplerState);
	if (FAILED(hr))
		return;

	// Create vertex shader
	UINT Size = ARRAYSIZE(g_VS);
	hr = device->CreateVertexShader(g_VS, Size, nullptr, &VertexShader);
	if (FAILED(hr))
		return;

	// Create input layout
	D3D11_INPUT_ELEMENT_DESC Layout[] =
	{
		{ "POSITION", 0, DXGI_FORMAT_R32G32B32_FLOAT, 0, 0, D3D11_INPUT_PER_VERTEX_DATA, 0 },
		{ "TEXCOORD", 0, DXGI_FORMAT_R32G32_FLOAT, 0, 12, D3D11_INPUT_PER_VERTEX_DATA, 0 }
	};

	UINT NumElements = ARRAYSIZE(Layout);
	hr = device->CreateInputLayout(Layout, NumElements, g_VS, Size, &InputLayout);
	if (FAILED(hr))
		return;

	deviceContext->IASetInputLayout(InputLayout);

	// Create pixel shader
	Size = ARRAYSIZE(g_PS);
	hr = device->CreatePixelShader(g_PS, Size, nullptr, &PixelShader);
	if (FAILED(hr))
		return;

	// Create vertex buffer
	D3D11_BUFFER_DESC BufferDesc;
	RtlZeroMemory(&BufferDesc, sizeof(BufferDesc));
	BufferDesc.Usage = D3D11_USAGE_DEFAULT;
	BufferDesc.ByteWidth = sizeof(VERTEX) * NUMVERTICES;
	BufferDesc.BindFlags = D3D11_BIND_VERTEX_BUFFER;
	BufferDesc.CPUAccessFlags = 0;

	D3D11_SUBRESOURCE_DATA InitData;
	RtlZeroMemory(&InitData, sizeof(InitData));
	InitData.pSysMem = Vertices;

	hr = device->CreateBuffer(&BufferDesc, &InitData, &VertexBuffer);
	if (FAILED(hr))
		return;

	// Create viewports
	ZeroMemory(&renderTargetViewport, sizeof(D3D11_VIEWPORT));
	renderTargetViewport.TopLeftX = 0;
	renderTargetViewport.TopLeftY = 0;
	renderTargetViewport.Width = ox;
	renderTargetViewport.Height = oy;

	ZeroMemory(&windowViewport, sizeof(D3D11_VIEWPORT));
	windowViewport.TopLeftX = 0;
	windowViewport.TopLeftY = 0;
	windowViewport.Width = 1920;
	windowViewport.Height = 1080;
}

// this is the function used to render a single frame
void RenderFrame(void)
{
	// clear the back buffer
	float color[4] = { 0.0f, 0.2f, 0.4f, 1.0f };
	deviceContext->ClearRenderTargetView(backbuffer, color);

	// Request frame
	IDXGIResource* DesktopResource = nullptr;
	DXGI_OUTDUPL_FRAME_INFO FrameInfo;
	HRESULT hr = outputDuplication->AcquireNextFrame(16, &FrameInfo, &DesktopResource);

	if (hr == DXGI_ERROR_WAIT_TIMEOUT)
		return;

	if (FAILED(hr))
		return;

	// Acquire texture
	hr = DesktopResource->QueryInterface(__uuidof(ID3D11Texture2D), reinterpret_cast<void **>(&acquiredDesktopImage));


	if (FAILED(hr))
		return;

	DesktopResource->Release();
	DesktopResource = nullptr;

	// get acquired desc
	D3D11_TEXTURE2D_DESC acquiredTextureDescription;
	acquiredDesktopImage->GetDesc(&acquiredTextureDescription);

	if (renderTargetTexture == nullptr)
	{
		// Create render target texture
		D3D11_TEXTURE2D_DESC renderTargetTextureDesc;
		ZeroMemory(&renderTargetTextureDesc, sizeof(D3D11_TEXTURE2D_DESC));
		renderTargetTextureDesc.Width = ox;
		renderTargetTextureDesc.Height = oy;
		renderTargetTextureDesc.MipLevels = 1;
		renderTargetTextureDesc.ArraySize = 1;
		renderTargetTextureDesc.Format = DXGI_FORMAT_B8G8R8A8_UNORM;
		renderTargetTextureDesc.SampleDesc.Count = 1;
		renderTargetTextureDesc.SampleDesc.Quality = 0;
		renderTargetTextureDesc.Usage = D3D11_USAGE_DEFAULT;
		renderTargetTextureDesc.BindFlags = D3D11_BIND_RENDER_TARGET | D3D11_BIND_SHADER_RESOURCE;
		renderTargetTextureDesc.CPUAccessFlags = 0;
		renderTargetTextureDesc.MiscFlags = 0;

		hr = device->CreateTexture2D(&renderTargetTextureDesc, NULL, &renderTargetTexture);
		if (FAILED(hr))
			return;

		// Create render target view
		D3D11_RENDER_TARGET_VIEW_DESC renderTargetViewDesc;
		renderTargetViewDesc.Format = renderTargetTextureDesc.Format;
		renderTargetViewDesc.ViewDimension = D3D11_RTV_DIMENSION_TEXTURE2D;
		renderTargetViewDesc.Texture2D.MipSlice = 0;

		hr = device->CreateRenderTargetView(renderTargetTexture, &renderTargetViewDesc, &renderTargetView);
		if (FAILED(hr))
			return;

		// Create render target resource view
		D3D11_SHADER_RESOURCE_VIEW_DESC renderTargetResourceViewDesc;
		renderTargetResourceViewDesc.Format = acquiredTextureDescription.Format;
		renderTargetResourceViewDesc.Texture2D.MipLevels = acquiredTextureDescription.MipLevels;
		renderTargetResourceViewDesc.Texture2D.MostDetailedMip = acquiredTextureDescription.MipLevels - 1;
		renderTargetResourceViewDesc.ViewDimension = D3D11_SRV_DIMENSION_TEXTURE2D;

		hr = device->CreateShaderResourceView(renderTargetTexture, &renderTargetResourceViewDesc, &renderTargetResourceView);
		if (FAILED(hr))
			return;
	}

	// Create acquired image resource view 
	D3D11_SHADER_RESOURCE_VIEW_DESC shaderResourceViewDesc;
	shaderResourceViewDesc.Format = acquiredTextureDescription.Format;
	shaderResourceViewDesc.Texture2D.MipLevels = acquiredTextureDescription.MipLevels;
	shaderResourceViewDesc.Texture2D.MostDetailedMip = acquiredTextureDescription.MipLevels - 1;
	shaderResourceViewDesc.ViewDimension = D3D11_SRV_DIMENSION_TEXTURE2D;

	ID3D11ShaderResourceView* shaderResourceView = nullptr;
	hr = device->CreateShaderResourceView(acquiredDesktopImage, &shaderResourceViewDesc, &shaderResourceView);
	if (FAILED(hr))
		return;
	
	//FLOAT blendFactor[4] = { 0.f, 0.f, 0.f, 0.f };
	//deviceContext->OMSetBlendState(m_BlendState, blendFactor, 0xFFFFFFFF);
	//deviceContext->PSSetSamplers(0, 1, &m_SamplerLinear);

	// Set render target 
	deviceContext->RSSetViewports(1, &renderTargetViewport);
	deviceContext->OMSetRenderTargets(1, &renderTargetView, nullptr);
	deviceContext->ClearRenderTargetView(renderTargetView, color);

	// Set device resources
	deviceContext->VSSetShader(VertexShader, nullptr, 0);
	deviceContext->PSSetShader(PixelShader, nullptr, 0);
	deviceContext->PSSetShaderResources(0, 1, &shaderResourceView);
	deviceContext->PSSetSamplers(0, 1, &pointSamplerState);

	deviceContext->IASetPrimitiveTopology(D3D11_PRIMITIVE_TOPOLOGY_TRIANGLELIST);
	deviceContext->IASetVertexBuffers(0, 1, &VertexBuffer, &Stride, &Offset);

	// Draw render target
	deviceContext->Draw(NUMVERTICES, 0);

	//D3D11_TEXTURE2D_DESC copyTextureDescription;
	//ZeroMemory(&copyTextureDescription, sizeof(copyTextureDescription));
	//copyTextureDescription.Width = ox;
	//copyTextureDescription.Height = oy;
	//copyTextureDescription.MipLevels = 1;
	//copyTextureDescription.ArraySize = 1;
	//copyTextureDescription.Format = acquiredTextureDescription.Format;
	//copyTextureDescription.Usage = D3D11_USAGE_STAGING;
	//copyTextureDescription.BindFlags = 0;
	//copyTextureDescription.CPUAccessFlags = D3D11_CPU_ACCESS_READ;
	//copyTextureDescription.MiscFlags = 0;
	//copyTextureDescription.SampleDesc.Count = 1;
	//copyTextureDescription.SampleDesc.Quality = 0;

	//ID3D11Texture2D* copyTexture = nullptr;
	//hr = device->CreateTexture2D(&copyTextureDescription, NULL, &copyTexture);
	//if (FAILED(hr))
	//	return;

	//deviceContext->CopyResource(copyTexture, renderTargetTexture);

	//int subResource = 0;
	//D3D11_MAPPED_SUBRESOURCE resource;
	//ZeroMemory(&resource, sizeof(resource));
	//hr = deviceContext->Map(copyTexture, 0, D3D11_MAP_READ, 0x0, &resource);

	////byte* outputReader = (byte*)imageData;
	//byte bytes[ox * oy * 4];
	//byte* outputReader = bytes;
	//byte* textureReader = (byte*)resource.pData;

	//for (int y = 0; y < oy; ++y)
	//{
	//	memcpy(outputReader, textureReader, ox * 4);
	//	outputReader += ox * 4;
	//	textureReader += resource.RowPitch;
	//}

	//deviceContext->Unmap(copyTexture, subResource);

	// Set window
	deviceContext->RSSetViewports(1, &windowViewport);
	deviceContext->OMSetRenderTargets(1, &backbuffer, NULL);

	// Set shader resource to rendertarget
	deviceContext->PSSetShaderResources(0, 1, &renderTargetResourceView);

	// Draw window
	deviceContext->Draw(NUMVERTICES, 0);
	swapchain->Present(0, 0);

	outputDuplication->ReleaseFrame();

	//wchar_t fn[16];
	//wsprintf(fn, L"d:\\temp\\%d.bmp", 1);
	//hr = SaveWICTextureToFile(
	//	deviceContext, 
	//	renderTargetTexture,
	//	GUID_ContainerFormatBmp,
	//	fn);
}

void CleanD3D(void)
{
	swapchain->Release();
	backbuffer->Release();
	device->Release();
	deviceContext->Release();
}