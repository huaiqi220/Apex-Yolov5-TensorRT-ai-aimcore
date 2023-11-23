import tensorrt as trt
import os

import pycuda.driver as cuda
import pycuda.autoinit
from PIL import Image
import numpy as np

# For reading size information from batches
import struct

IMG_H, IMG_W, IMG_CH = 300, 300, 3

class SSDEntropyCalibrator(trt.IInt8EntropyCalibrator2):
    def __init__(self, data_dir, cache_file):
        # Whenever you specify a custom constructor for a TensorRT class,
        # you MUST call the constructor of the parent explicitly.
        trt.IInt8EntropyCalibrator2.__init__(self)

        self.num_calib_imgs = 100 # the number of images from the dataset to use for calibration
        self.batch_size = 10
        self.batch_shape = (self.batch_size, IMG_CH, IMG_H, IMG_W)
        self.cache_file = cache_file

        calib_imgs = [os.path.join(data_dir, f) for f in os.listdir(data_dir)]
        self.calib_imgs = np.random.choice(calib_imgs, self.num_calib_imgs)
        self.counter = 0 # for keeping track of how many files we have read

        self.device_input = cuda.mem_alloc(trt.volume(self.batch_shape) * trt.float32.itemsize)

    def get_batch_size(self):
        return self.batch_size

    # TensorRT passes along the names of the engine bindings to the get_batch function.
    # You don't necessarily have to use them, but they can be useful to understand the order of
    # the inputs. The bindings list is expected to have the same ordering as 'names'.
    def get_batch(self, names):

        # if there are not enough calibration images to form a batch,
        # we have reached the end of our data set
        if self.counter == self.num_calib_imgs:
            return None

        # debugging
        if self.counter % 10 == 0:
            print('Running Batch:', self.counter)

        batch_imgs = np.zeros((self.batch_size, IMG_H*IMG_W*IMG_CH))
        for i in range(self.batch_size):

            image = Image.open(self.calib_imgs[self.counter + i])

            # Note: Bilinear interpolation used by Pillow is a little bit
            # different than the one used by Tensorflow, so if network receives
            # an image that is not 300x300, the network output may differ
            # from the one output by Tensorflow
            image_resized = image.resize(
                size=(IMG_H, IMG_W),
                resample=Image.BILINEAR
            )
            img_np = self._load_image_into_numpy_array(image_resized)
            # HWC -> CHW
            img_np = img_np.transpose((2, 0, 1))
            # Normalize to [-1.0, 1.0] interval (expected by model)
            img_np = (2.0 / 255.0) * img_np - 1.0
            img_np = img_np.ravel()
            img_np = np.ascontiguousarray(img_np)

            # add this image to the batch array
            batch_imgs[i,:] = img_np

        # increase the counter for this batch
        self.counter += self.batch_size

        # Copy to device, then return a list containing pointers to input device buffers.
        cuda.memcpy_htod(self.device_input, batch_imgs.astype(np.float32))
        return [int(self.device_input)]

    def read_calibration_cache(self):
        # If there is a cache, use it instead of calibrating again. Otherwise, implicitly return None.
        if os.path.exists(self.cache_file):
            with open(self.cache_file, "rb") as f:
                return f.read()

    def write_calibration_cache(self, cache):
        print('writing calibration file')
        with open(self.cache_file, "wb") as f:
            f.write(cache)

    def _load_image_into_numpy_array(self, image):
        (im_width, im_height) = image.size
        return np.array(image).reshape(
            (im_height, im_width, 3)
        ).astype(np.uint8)
