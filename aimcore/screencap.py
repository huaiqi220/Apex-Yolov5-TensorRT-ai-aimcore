

import dxcam
import time

# camera = dxcam.create(device_idx=0, output_idx=0,region=(960, 480, 960 + 640, 480 + 640))
# print(dxcam.device_info())
# print(dxcam.output_info())
# while True:
#     start_time = time.time()

#     frame = camera.grab()
#     final_time = time.time()
#     print(frame.shape)
#     print(start_time)
#     print(final_time)
#     fps_txt = 1/(int(final_time * 100000) - int(start_time * 100000))
#     print(fps_txt)
import DXGI
g = DXGI.capture(960, 480, 960 + 640, 480 + 640) 


title = "fps"
start_time, fps = time.perf_counter(), 0
# cam = dxcam.create()
start = time.perf_counter()
while fps < 1000:
    # frame = cam.grab()
    frame = g.cap()
    # fps += 1
    if frame is not None:  # New frame
        fps += 1
end_time = time.perf_counter() - start_time
print(f"{title}: {fps/end_time}")

# camera = dxcam.create(output_idx=0,region=(960, 480, 960 + 640, 480 + 640))
# camera.start(target_fps=150)
# for i in range(1000):
#     image = camera.get_latest_frame()
# camera.stop()