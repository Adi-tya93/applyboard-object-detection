# Applyboard Object Detection

## Introduction

A Keras implementation of YOLOv3 (Tensorflow backend) inspired by [qqwweee](https://github.com/qqwweee/keras-yolo3) and [allanzelener/YAD2K](https://github.com/allanzelener/YAD2K).

---

## Quick Start

1. Download YOLOv3 weights from [YOLO website](http://pjreddie.com/darknet/yolo/).
2. Convert the Darknet YOLO model to a Keras model.
3. Run YOLO detection.

```
wget https://pjreddie.com/media/files/yolov3.weights
python convert.py configs/yolov3.cfg yolov3.weights model_data/yolo_weights.h5
python detect_image.py
```

### Usage
```
python detect_image.py
```

Configure the `config.json` file to make changes to anything.
```
{
    "model": {
        "model_path": "model_data/yolo_weights.h5",
        "anchors_path": "model_data/yolo_anchors.txt",
        "classes_path": "model_data/yolo_classes.txt",
        "score" : 0.3,
        "iou" : 0.5,
        "image_height" : 416,
        "image_width" : 416,
        "gpu_num" : 1
    },
    "train": {
        "training_file": "training_file.txt",
        "log_dir": "logs/000/",
        "classes_path": "model_data/yolo_classes.txt",
        "anchors_path": "model_data/yolo_anchors.txt"
    }
}
```
#### Model
| Name | Description |
| -- | -- |
| model_path | The path to the model to be used |
| anchors_path | The path to the anchors to be used |
| classes_path | A file that contains the classes trained to be detected |
| score | The minimum score used (from 0-1) for a positive match to be found |
| iou | Intersection Over Union threshold,  |
| image_height | Yolo downscales the image to this size |
| image_width | Yolo downscales the image to this size |
| gpu_num | The number of GPUs to use |

#### Training
| Name | Description |
| -- | -- |
| training_file | The training file created by voc_parser.py, this is used for training |
| log_dir | This is where the model will be exported to |
| classes_path | The classes you want the model to detect, these must match with your dataset |
| anchors_path | Initial anchors for training |

---

## Training

1. Generate your own annotation file and class names file. This file is used to train the mode, and is extracted from a VOC dataset. One row for one image;
    Row format: `image_file_path box1 box2 ... boxN`;  
    Box format: `x_min,y_min,x_max,y_max,class_id` (no space).    
    Here is an example:

    ```
    path/to/img1.jpg 50,100,150,200,0 30,50,200,120,3
    path/to/img2.jpg 120,300,250,600,2
    ...
    ```

    To create this file, run the `voc_annotation.py` file and it will parse through the `data/images` and `data/annotations` to create the annotation_file for training. 
    ```
    python voc_annotation.py
    ```

2. The file model_data/yolo_weights.h5 is used to load pretrained weights. Make sure you have run  
    ```
    python convert.py -w configs/yolov3.cfg yolov3.weights model_data/yolo_weights.h5
    ```

3. Modify train.py and start training.  
    ```
    python train.py
    ```


If you want to use original pretrained weights for YOLOv3:  
    1. `wget https://pjreddie.com/media/files/darknet53.conv.74`  
    2. rename it as darknet53.weights  
    3. `python convert.py -w configs/darknet53.cfg darknet53.weights model_data/darknet53_weights.h5`  
    4. use model_data/darknet53_weights.h5 in train.py

---

## Some issues to know

1. The test environment is
    - Python 3.5.2
    - Keras 2.1.5
    - tensorflow 1.6.0

2. Default anchors are used. If you use your own anchors, probably some changes are needed.

3. The inference result is not totally the same as Darknet but the difference is small.

4. The speed is slower than Darknet. Replacing PIL with opencv may help a little.

5. Always load pretrained weights and freeze layers in the first stage of training. Or try Darknet training. It's OK if there is a mismatch warning.

6. The training strategy is for reference only. Adjust it according to your dataset and your goal. And add further strategy if needed.

7. For speeding up the training process with frozen layers train_bottleneck.py can be used. It will compute the bottleneck features of the frozen model first and then only trains the last layers. This makes training on CPU possible in a reasonable time. See [this](https://blog.keras.io/building-powerful-image-classification-models-using-very-little-data.html) for more information on bottleneck features.
