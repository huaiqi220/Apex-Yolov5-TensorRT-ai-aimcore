# TensorRTx

TensorRTx aims to implement popular deep learning networks with TensorRT network definition API.

Why don't we use a parser (ONNX parser, UFF parser, caffe parser, etc), but use complex APIs to build a network from scratch? I have summarized the advantages in the following aspects.
- **Flexible**, easy to modify the network, add/delete a layer or input/output tensor, replace a layer, merge layers, integrate preprocessing and postprocessing into network, etc.
- **Debuggable**, construct the entire network in an incremental development manner, easy to get middle layer results.
- **Chance to learn**, learn about the network structure during this development, rather than treating everything as a black box.

The basic workflow of TensorRTx is:
1. Get the trained models from pytorch, mxnet or tensorflow, etc. Some pytorch models can be found in my repo [pytorchx](https://github.com/wang-xinyu/pytorchx), the remaining are from popular open-source repos.
2. Export the weights to a plain text file -- [.wts file](./tutorials/getting_started.md#the-wts-content-format).
3. Load weights in TensorRT, define the network, build a TensorRT engine.
4. Load the TensorRT engine and run inference.

## News

- `18 Dec 2022`. [YOLOv5](./yolov5) upgrade to support v7.0, including instance segmentation.
- `12 Dec 2022`. [East-Face](https://github.com/East-Face): [UNet](./unet) upgrade to support v3.0 of [Pytorch-UNet](https://github.com/milesial/Pytorch-UNet).
- `26 Oct 2022`. [ausk](https://github.com/ausk): YoloP(You Only Look Once for Panopitic Driving Perception).
- `19 Sep 2022`. [QIANXUNZDL123](https://github.com/QIANXUNZDL123) and [lindsayshuo](https://github.com/lindsayshuo): YOLOv7.
- `7 Sep 2022`. [xiang-wuu](https://github.com/xiang-wuu): YOLOv5 v6.2 classification models.
- `19 Aug 2022`. [Dominic](https://github.com/Dominic-DallOsto) and [sbmalik](https://github.com/sbmalik): Yolov3-tiny and Arcface support TRT8.
- `6 Jul 2022`. [xiang-wuu](https://github.com/xiang-wuu): SuperPoint - Self-Supervised Interest Point Detection and Description, vSLAM related.
- `26 May 2022`. [triple-Mu](https://github.com/triple-Mu): YOLOv5 python script with CUDA Python API.
- `23 May 2022`. [yhpark](https://github.com/yester31): Real-ESRGAN, Practical Algorithms for General Image/Video Restoration.
- `19 May 2022`. [vjsrinivas](https://github.com/vjsrinivas): YOLOv3 TRT8 support and Python script.
- `15 Mar 2022`. [sky_hole](https://github.com/wdhao): Swin Transformer - Semantic Segmentation.
- `19 Oct 2021`. [liuqi123123](https://github.com/liuqi123123) added cuda preprossing for yolov5, preprocessing + inference is 3x faster when batchsize=8.
- `18 Oct 2021`. [xupengao](https://github.com/xupengao): YOLOv5 updated to v6.0, supporting n/s/m/l/x/n6/s6/m6/l6/x6.
- `31 Aug 2021`. [FamousDirector](https://github.com/FamousDirector): update retinaface to support TensorRT 8.0.
- `27 Aug 2021`. [HaiyangPeng](https://github.com/HaiyangPeng): add a python wrapper for hrnet segmentation.

## Tutorials

- [Install the dependencies.](./tutorials/install.md)
- [A guide for quickly getting started, taking lenet5 as a demo.](./tutorials/getting_started.md)
- [The .wts file content format](./tutorials/getting_started.md#the-wts-content-format)
- [Frequently Asked Questions (FAQ)](./tutorials/faq.md)
- [Migrating from TensorRT 4 to 7](./tutorials/migrating_from_tensorrt_4_to_7.md)
- [How to implement multi-GPU processing, taking YOLOv4 as example](./tutorials/multi_GPU_processing.md)
- [Check if Your GPU support FP16/INT8](./tutorials/check_fp16_int8_support.md)
- [How to Compile and Run on Windows](./tutorials/run_on_windows.md)
- [Deploy YOLOv4 with Triton Inference Server](https://github.com/isarsoft/yolov4-triton-tensorrt)
- [From pytorch to trt step by step, hrnet as example(Chinese)](./tutorials/from_pytorch_to_trt_stepbystep_hrnet.md)

## Test Environment

1. TensorRT 7.x
2. TensorRT 8.x(Some of the models support 8.x)

## How to run

Each folder has a readme inside, which explains how to run the models inside.

## Models

Following models are implemented.

|Name | Description |
|-|-|
|[mlp](./mlp) | the very basic model for starters, properly documented |
|[lenet](./lenet) | the simplest, as a "hello world" of this project |
|[alexnet](./alexnet)| easy to implement, all layers are supported in tensorrt |
|[googlenet](./googlenet)| GoogLeNet (Inception v1) |
|[inception](./inception)| Inception v3, v4 |
|[mnasnet](./mnasnet)| MNASNet with depth multiplier of 0.5 from the paper |
|[mobilenet](./mobilenet)| MobileNet v2, v3-small, v3-large |
|[resnet](./resnet)| resnet-18, resnet-50 and resnext50-32x4d are implemented |
|[senet](./senet)| se-resnet50 |
|[shufflenet](./shufflenetv2)| ShuffleNet v2 with 0.5x output channels |
|[squeezenet](./squeezenet)| SqueezeNet 1.1 model |
|[vgg](./vgg)| VGG 11-layer model |
|[yolov3-tiny](./yolov3-tiny)| weights and pytorch implementation from [ultralytics/yolov3](https://github.com/ultralytics/yolov3) |
|[yolov3](./yolov3)| darknet-53, weights and pytorch implementation from [ultralytics/yolov3](https://github.com/ultralytics/yolov3) |
|[yolov3-spp](./yolov3-spp)| darknet-53, weights and pytorch implementation from [ultralytics/yolov3](https://github.com/ultralytics/yolov3) |
|[yolov4](./yolov4)| CSPDarknet53, weights from [AlexeyAB/darknet](https://github.com/AlexeyAB/darknet#pre-trained-models), pytorch implementation from [ultralytics/yolov3](https://github.com/ultralytics/yolov3) |
|[yolov5](./yolov5)| yolov5 v1.0-v7.0 of [ultralytics/yolov5](https://github.com/ultralytics/yolov5), detection, classification and instance segmentation |
|[yolov7](./yolov7)| yolov7 v0.1, pytorch implementation from [WongKinYiu/yolov7](https://github.com/WongKinYiu/yolov7) |
|[yolop](./yolop)| yolop, pytorch implementation from [hustvl/YOLOP](https://github.com/hustvl/YOLOP) |
|[retinaface](./retinaface)| resnet50 and mobilnet0.25, weights from [biubug6/Pytorch_Retinaface](https://github.com/biubug6/Pytorch_Retinaface) |
|[arcface](./arcface)| LResNet50E-IR, LResNet100E-IR and MobileFaceNet, weights from [deepinsight/insightface](https://github.com/deepinsight/insightface) |
|[retinafaceAntiCov](./retinafaceAntiCov)| mobilenet0.25, weights from [deepinsight/insightface](https://github.com/deepinsight/insightface), retinaface anti-COVID-19, detect face and mask attribute |
|[dbnet](./dbnet)| Scene Text Detection, weights from [BaofengZan/DBNet.pytorch](https://github.com/BaofengZan/DBNet.pytorch) |
|[crnn](./crnn)| pytorch implementation from [meijieru/crnn.pytorch](https://github.com/meijieru/crnn.pytorch) |
|[ufld](./ufld)| pytorch implementation from [Ultra-Fast-Lane-Detection](https://github.com/cfzd/Ultra-Fast-Lane-Detection), ECCV2020 |
|[hrnet](./hrnet)| hrnet-image-classification and hrnet-semantic-segmentation, pytorch implementation from [HRNet-Image-Classification](https://github.com/HRNet/HRNet-Image-Classification) and [HRNet-Semantic-Segmentation](https://github.com/HRNet/HRNet-Semantic-Segmentation) |
|[psenet](./psenet)| PSENet Text Detection, tensorflow implementation from [liuheng92/tensorflow_PSENet](https://github.com/liuheng92/tensorflow_PSENet) |
|[ibnnet](./ibnnet)| IBN-Net, pytorch implementation from [XingangPan/IBN-Net](https://github.com/XingangPan/IBN-Net), ECCV2018 |
|[unet](./unet)| U-Net, pytorch implementation from [milesial/Pytorch-UNet](https://github.com/milesial/Pytorch-UNet) |
|[repvgg](./repvgg)| RepVGG, pytorch implementation from [DingXiaoH/RepVGG](https://github.com/DingXiaoH/RepVGG) |
|[lprnet](./lprnet)| LPRNet, pytorch implementation from [xuexingyu24/License_Plate_Detection_Pytorch](https://github.com/xuexingyu24/License_Plate_Detection_Pytorch) |
|[refinedet](./refinedet)| RefineDet, pytorch implementation from [luuuyi/RefineDet.PyTorch](https://github.com/luuuyi/RefineDet.PyTorch) |
|[densenet](./densenet)| DenseNet-121, from torchvision.models |
|[rcnn](./rcnn)| FasterRCNN and MaskRCNN, model from [detectron2](https://github.com/facebookresearch/detectron2) |
|[tsm](./tsm)| TSM: Temporal Shift Module for Efficient Video Understanding, ICCV2019 |
|[scaled-yolov4](./scaled-yolov4)| yolov4-csp, pytorch from [WongKinYiu/ScaledYOLOv4](https://github.com/WongKinYiu/ScaledYOLOv4) |
|[centernet](./centernet)| CenterNet DLA-34, pytorch from [xingyizhou/CenterNet](https://github.com/xingyizhou/CenterNet) |
|[efficientnet](./efficientnet)| EfficientNet b0-b8 and l2, pytorch from [lukemelas/EfficientNet-PyTorch](https://github.com/lukemelas/EfficientNet-PyTorch) |
|[detr](./detr)| DE⫶TR, pytorch from [facebookresearch/detr](https://github.com/facebookresearch/detr) |
|[swin-transformer](./swin-transformer)| Swin Transformer - Semantic Segmentation, only support Swin-T. The Pytorch implementation is [microsoft/Swin-Transformer](https://github.com/microsoft/Swin-Transformer.git) |
|[real-esrgan](./real-esrgan)| Real-ESRGAN. The Pytorch implementation is [real-esrgan](https://github.com/xinntao/Real-ESRGAN) |
|[superpoint](./superpoint)| SuperPoint. The Pytorch model is from [magicleap/SuperPointPretrainedNetwork](https://github.com/magicleap/SuperPointPretrainedNetwork) |

## Model Zoo

The .wts files can be downloaded from model zoo for quick evaluation. But it is recommended to convert .wts from pytorch/mxnet/tensorflow model, so that you can retrain your own model.

[GoogleDrive](https://drive.google.com/drive/folders/1Ri0IDa5OChtcA3zjqRTW57uG6TnfN4Do?usp=sharing) | [BaiduPan](https://pan.baidu.com/s/19s6hO8esU7-TtZEXN7G3OA) pwd: uvv2

## Tricky Operations

Some tricky operations encountered in these models, already solved, but might have better solutions.

|Name | Description |
|-|-|
|BatchNorm| Implement by a scale layer, used in resnet, googlenet, mobilenet, etc. |
|MaxPool2d(ceil_mode=True)| use a padding layer before maxpool to solve ceil_mode=True, see googlenet. |
|average pool with padding| use setAverageCountExcludesPadding() when necessary, see inception. |
|relu6| use `Relu6(x) = Relu(x) - Relu(x-6)`, see mobilenet. |
|torch.chunk()| implement the 'chunk(2, dim=C)' by tensorrt plugin, see shufflenet. |
|channel shuffle| use two shuffle layers to implement `channel_shuffle`, see shufflenet. |
|adaptive pool| use fixed input dimension, and use regular average pooling, see shufflenet. |
|leaky relu| I wrote a leaky relu plugin, but PRelu in `NvInferPlugin.h` can be used, see yolov3 in branch `trt4`. |
|yolo layer v1| yolo layer is implemented as a plugin, see yolov3 in branch `trt4`. |
|yolo layer v2| three yolo layers implemented in one plugin, see yolov3-spp. |
|upsample| replaced by a deconvolution layer, see yolov3. |
|hsigmoid| hard sigmoid is implemented as a plugin, hsigmoid and hswish are used in mobilenetv3 |
|retinaface output decode| implement a plugin to decode bbox, confidence and landmarks, see retinaface. |
|mish| mish activation is implemented as a plugin, mish is used in yolov4 |
|prelu| mxnet's prelu activation with trainable gamma is implemented as a plugin, used in arcface |
|HardSwish| hard_swish = x * hard_sigmoid, used in yolov5 v3.0 |
|LSTM| Implemented pytorch nn.LSTM() with tensorrt api |

## Speed Benchmark

| Models | Device | BatchSize | Mode | Input Shape(HxW) | FPS |
|-|-|:-:|:-:|:-:|:-:|
| YOLOv3-tiny | Xeon E5-2620/GTX1080 | 1 | FP32 | 608x608 | 333 |
| YOLOv3(darknet53) | Xeon E5-2620/GTX1080 | 1 | FP32 | 608x608 | 39.2 |
| YOLOv3(darknet53) | Xeon E5-2620/GTX1080 | 1 | INT8 | 608x608 | 71.4 |
| YOLOv3-spp(darknet53) | Xeon E5-2620/GTX1080 | 1 | FP32 | 608x608 | 38.5 |
| YOLOv4(CSPDarknet53) | Xeon E5-2620/GTX1080 | 1 | FP32 | 608x608 | 35.7 |
| YOLOv4(CSPDarknet53) | Xeon E5-2620/GTX1080 | 4 | FP32 | 608x608 | 40.9 |
| YOLOv4(CSPDarknet53) | Xeon E5-2620/GTX1080 | 8 | FP32 | 608x608 | 41.3 | 
| YOLOv5-s v3.0 | Xeon E5-2620/GTX1080 | 1 | FP32 | 608x608 | 142 |
| YOLOv5-s v3.0 | Xeon E5-2620/GTX1080 | 4 | FP32 | 608x608 | 173 |
| YOLOv5-s v3.0 | Xeon E5-2620/GTX1080 | 8 | FP32 | 608x608 | 190 |
| YOLOv5-m v3.0 | Xeon E5-2620/GTX1080 | 1 | FP32 | 608x608 | 71 |
| YOLOv5-l v3.0 | Xeon E5-2620/GTX1080 | 1 | FP32 | 608x608 | 43 |
| YOLOv5-x v3.0 | Xeon E5-2620/GTX1080 | 1 | FP32 | 608x608 | 29 |
| YOLOv5-s v4.0 | Xeon E5-2620/GTX1080 | 1 | FP32 | 608x608 | 142 |
| YOLOv5-m v4.0 | Xeon E5-2620/GTX1080 | 1 | FP32 | 608x608 | 71 |
| YOLOv5-l v4.0 | Xeon E5-2620/GTX1080 | 1 | FP32 | 608x608 | 40 |
| YOLOv5-x v4.0 | Xeon E5-2620/GTX1080 | 1 | FP32 | 608x608 | 27 |
| RetinaFace(resnet50) | Xeon E5-2620/GTX1080 | 1 | FP32 | 480x640 | 90 |
| RetinaFace(resnet50) | Xeon E5-2620/GTX1080 | 1 | INT8 | 480x640 | 204 |
| RetinaFace(mobilenet0.25) | Xeon E5-2620/GTX1080 | 1 | FP32 | 480x640 | 417 |
| ArcFace(LResNet50E-IR) | Xeon E5-2620/GTX1080 | 1 | FP32 | 112x112 | 333 |
| CRNN | Xeon E5-2620/GTX1080 | 1 | FP32 | 32x100 | 1000 |

Help wanted, if you got speed results, please add an issue or PR.

## Acknowledgments & Contact

Any contributions, questions and discussions are welcomed, contact me by following info.

E-mail: wangxinyu_es@163.com

WeChat ID: wangxinyu0375 (可加我微信进tensorrtx交流群，**备注：tensorrtx**)
