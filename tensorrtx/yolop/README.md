YoloP
=====

The original pytorch model is from [hustvl/YOLOP](https://github.com/hustvl/YOLOP)

## Authors

<a href="https://github.com/ausk"><img src="https://avatars.githubusercontent.com/u/4545060?v=4?s=48" width="40px;" alt=""/></a>
<a href="https://github.com/aliceint"><img src="https://avatars.githubusercontent.com/u/15520773?v=4?s=48" width="40px;" alt=""/></a>
<a href="https://github.com/mantuoluozk"><img src="https://avatars.githubusercontent.com/u/43333969?v=4?s=48" width="40px;" alt=""/></a>

## 1. Prepare building environments

Make sure you have install `c++`(support c++11)、 `cmake`、`opencv`(4.x)、`cuda`(10.x)、`nvinfer`(7.x).


## 2. build yolop

Go to `yolop`.

```
mkdir build
cd build

cmake ..
make
```

Now you can get `yolop` and `libmyplugins.so`.


## 3. Test in C++

Go to `yolop/build`.

### 3.1 generate yolop.wts
Download/Clone [YOLOP](https://github.com/hustvl/YOLOP)

Edit `gen_wts.py` , change `YOLOP_BASE_DIR` to realpath of `YOLOP`.

```
# [WARN] Please download/clone YOLOP, then set YOLOP_BASE_DIR to the root of YOLOP
python3 ../gen_wts.py
```

### 3.2 generate yolop.trt
```
./yolop -s yolop.wts  yolop.trt
```

Now you have such files:  `libmyplugins.so yolop yolop.wts  yolop.trt`


### 3.3 test yolop.trt
```
mkdir ../results

YOLOP_BASE_DIR=/home/user/jetson/tmp/YOLOP
./yolop -d yolop.trt  $YOLOP_BASE_DIR/inference/images/
```

It will output like as follow if successful! ( test on `Jetson Xavier NX - Jetpack 4.4`)
```
1601ms # the fist time is slow
26ms   # then it is faster
29ms
27ms
29ms
29ms
```

![](https://user-images.githubusercontent.com/4545060/197756635-38348dc5-d8e7-4ae3-be56-6b231dd2f5db.jpg)


## 4. Test in python3
Go to `yolop`.

Make sure you have install `pycuda` `tensorrt`; and modify `image_dir` to your image dir.

```
# usage: xxx <engine file> <plugin file> <image dir>

python3 yolop_trt.py  build/yolop.trt  build/libmyplugins.so /home/user/jetson/tmp/YOLOP/inference/images
```

It will output like as follow if successful! ( test on `Jetson Xavier NX - Jetpack 4.4`)
```
usage: xxx <engine file> <plugin file> <image dir>
[WARN] preaprea you image_dir, such as: samples, or /home/user/jetson/tmp/YOLOP/inference/images
bingding:  data (3, 384, 640)
bingding:  det (6001, 1, 1)
bingding:  seg (1, 360, 640)
bingding:  lane (1, 360, 640)
batch size is 1
warm_up->(384, 640, 3), time->1070.87ms
input->['/home/user/jetson/tmp/YOLOP/inference/images/3c0e7240-96e390d2.jpg'], time->25.94ms, saving into output/
input->['/home/user/jetson/tmp/YOLOP/inference/images/adb4871d-4d063244.jpg'], time->25.34ms, saving into output/
input->['/home/user/jetson/tmp/YOLOP/inference/images/8e1c1ab0-a8b92173.jpg'], time->25.03ms, saving into output/
input->['/home/user/jetson/tmp/YOLOP/inference/images/7dd9ef45-f197db95.jpg'], time->25.45ms, saving into output/
input->['/home/user/jetson/tmp/YOLOP/inference/images/9aa94005-ff1d4c9a.jpg'], time->24.93ms, saving into output/
input->['/home/user/jetson/tmp/YOLOP/inference/images/0ace96c3-48481887.jpg'], time->25.33ms, saving into output/
done!
```

![](https://user-images.githubusercontent.com/4545060/198003852-204f3bae-18ad-44fb-9ecd-4a2a07a726a3.jpg)


**Notice** : The results of c++ and python are not aligned for now!

----------------------------------------

```BibTeX
@misc{2108.11250,
Author = {Dong Wu and Manwen Liao and Weitian Zhang and Xinggang Wang},
Title = {YOLOP: You Only Look Once for Panoptic Driving Perception},
Year = {2021},
Eprint = {arXiv:2108.11250},
}
```

