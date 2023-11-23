# Apex-Yolov5-TensorRT-ai-aimcore
基于TensorRT和Yolov5的全套数据采集代码、数据标注、模型转换、推理代码
先前闲的时候，利用Yolo TensorRT python OpenCV DXGI以及罗技鼠标驱动做了一款APEX的ai辅助瞄准
控制上使用了PID以及FOV。
在训练场实测无配件R99中距离伤害可以达到120+。
实现了>60fps的高帧率辅助瞄准。
### 工作流上：
1. 首先使用数据采集代码，如main/screen.py采集屏幕中心640 * 640像素图片。
2. 从640 *640 图片中筛选存在队友和敌人的图片
3. 使用labelme进行数据标注。
4. 编写脚本将标签数据整理object detection成数据集格式。
5. 训练模型，分别训练s模型n模型x模型，精度与推理速度是个需要取舍的问题。
6. 根据TensortX框架将pt模型经过wts模型转换为engine模型
7. 编写鼠标控制代码
8. 调用模型，实现鼠标控制及辅助瞄准功能。

### 复盘：
1. 可用数据最终到手才7000张，也没有做数据增强，所以模型准确率，尤其是s模型PR一般
2. 截图，控制操作，最后使用更熟悉的python完成，如果使用C++推理速度还能更快
3. 鼠标控制上可以添加一些高级逻辑，如随机噪声，远近目标决策，最后都没时间做
4. 数据关系模型精度，训练一个数据筛选模型，可以从直播，游戏里极大增加训练数据量
5. 或许可以除队友，敌人外增加head body目标，但这对数据标注要求太高。
6. 数据增强手段上，也有很多手段可以使用。

### 为什么不继续做
没时间，没精力，实验室别的任务多起来了

### 有什么价值
没什么价值，做着玩的

### 游戏里开过吗，给不给模型文件
一次没开过，只训练场简单测试，开挂sm嗷，全套代码都在仓库，模型文件因大小原因暂时不提交到仓库，找我要也不给，别要了


