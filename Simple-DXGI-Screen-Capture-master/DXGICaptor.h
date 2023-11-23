#include <d3d11.h>
#include <dxgi1_2.h>

class VideoDXGICaptor
{
public:
    VideoDXGICaptor();
    ~VideoDXGICaptor();

public:
    BOOL Init();
    VOID Deinit();

public:
    virtual BOOL CaptureImage(RECT& rect, void* pData, INT& nLen);
    virtual BOOL CaptureImage(void* pData, INT& nLen);
    virtual BOOL ResetDevice();

private:
    BOOL  AttatchToThread(VOID);
    BOOL  QueryFrame(void* pImgData, INT& nImgSize);
    BOOL  QueryFrame(void* pImgData, INT& nImgSize, int z);

private:
    IDXGIResource* zhDesktopResource;
    DXGI_OUTDUPL_FRAME_INFO zFrameInfo;
    ID3D11Texture2D* zhAcquiredDesktopImage;
    IDXGISurface* zhStagingSurf;

private:
    BOOL                    m_bInit;
    int                     m_iWidth, m_iHeight;

    ID3D11Device* m_hDevice;
    ID3D11DeviceContext* m_hContext;

    IDXGIOutputDuplication* m_hDeskDupl;
    DXGI_OUTPUT_DESC        m_dxgiOutDesc;
};