# Object Detection API Docker

This project is a Dockerfile which will build a Docker image containing the Tensorflow Object Detection API and all of it's required dependencies

## Getting Started  

### Building the Docker image  

```bash
    docker build -t tf-obj-cpu:1.14 .
```  

The previous command would build a Docker image with the name ```tf-obj-cpu``` and the version tag ```1.14```. This version tag is suitable for this image because the version of Tensorflow used is ```1.14```.  

> Note: Worth mentioning the image can be named whatever you like and given any version tag you would like  

This command will build a Docker image which can be used to build containers. This image contains Tensorflow v1.14, as well as the Tensorflow Models repository and all dependencies required to train an object detection model using their Object Detection API.  

### 📁 Preparing Workspace  

The workspace directory included in this repository contains a sample project with the correct directory structure to get started with using the Tensorflow Object Detection API.  

All projects or models you want to create in the future should contain this same directory structure in order to ensure everything runs correctly. This will be a convention based approach to rapidly develop models without having to worry about configuration.  

The directory is as follows:  

```
project-name
├─ annotations
├─ images
│   ├─ test
│   └─ train
├─ pre-trained-model
├─ training
└─ README.md 
```  

1. ```annotations```: This folder will be used to store all *.csv files and the respective TensorFlow *.record files, which contain the list of annotations for our dataset images.

2. ```images```: This folder contains a copy of all the images in our dataset, as well as the respective *.xml files produced for each one, once labelImg is used to annotate objects.

    - ```images\train```: This folder contains a copy of all images, and the respective *.xml files, which will be used to train our model.
    - ```images\test```: This folder contains a copy of all images, and the respective *.xml files, which will be used to test our model.  

3. ```pre-trained-model```: This folder will contain the pre-trained model of our choice, which shall be used as a starting checkpoint for our training job.

4. ```training```: This folder will contain the training pipeline configuration file *.config, as well as a *.pbtxt label map file and all files generated during the training of our model.

5. ```README.md```: This is an optional file which provides some general information regarding the training conditions of our model. It is not used by TensorFlow in any way, but it generally helps when you have a few training folders and/or you are revisiting a trained model after some time.  

6. ```customlabels.py```: This is a python file which contains a sample function which looks like the following.  

    ```python
    # TO-DO replace this with label map
    # These must match the label map file in the annotations directory
    def class_text_to_int(row_label):
        if row_label == 'dog':
            return 1
        elif row_label == 'cat':
            return 2
        else:
            None 
    ```
    This file must be modified to match the labels you will be trying to identify in your object detection model. There is also a sample label map file provided in the annotations directory which will also have go be modified to match the preceeding Python file.  

    ```python
    item {
    id: 1
    name: 'dog'
    }

    item {
    id: 2
    name: 'cat'
    }
    ```  

    You will notice it is important these two files match eachother's configurations or your model will not work correctly.  

### ❗ Important Note  ❗

> To keep the source repository clean and avoid any accidental committing to the original repo, you should copy the ```project-name``` directory from inside this repository to a location on your local machine. We will later mount this copied directory into the container which is running the object detection API. Rename your copied ```project-name``` directory to a project name of your choosing. For this example I will use ```pet``` since the labels denote ```cat and dog```

### 📷 Labelling / Annotating Images  

The first step in any machine learning pipeline is preparing your training data in a way which is compatible with the model being used. For our object detection model, the images must be labelled with a bouding box surrounding the objects we are looking to detect.  

This can be done on your local machine before use of any container functionality.  

To annotate images we will be using the [labelImg](https://github.com/tzutalin/labelImg) package. Follow installation instructions, if you haven't already done so.  

> Worth noting, your overall training images should be split into two separate piles. Something like a 70-30 or 80-20 split. ```train / test```. We need to hold some images aside for evaluating the performance of our model  

Put your images inside this newly created ```pet``` dir. Training will go to ```<path>/pet/images/train``` and ```<path>/pet/images/test``` accordingly

#### Run the labelImg application  

- Select Open Dir to select your source image directory ```test or train``` 
- Change save Dir to match the source image directory 
- Select the ```Create Rect Box``` icon from the menu and drag a box around each object and specify the desired label  

![Labelled](assets/labelled.PNG)  

- Click ```Save``` and this will generate an ```xml``` document with the correct labels and coordinates to the bounding box for each label. Repeat this process with both the ```testing``` and ```training``` directories until all photos are labelled  

### ✏ Editing Label Map  

This is the point where you would update the sample ```labelmap.pbtxt``` file which can be located in the ```annotations``` directory. For this example the label map is already correct. It was created for this README  

Example, if you were looking to detect basketballs and baseballs your labelmap would look like the following  

```python
    item {
        id: 1
        name: 'basketball'
    }

    item {
        id: 2
        name: 'baseball'
    }
``` 

### 💻 Running our container  

At this point we are ready to start leveraging the pre-built functionality which this container provides for us. We need to spin up a container from the image we created earlier and mount our newly created training data inside. 

To do this:  

```bash  
    docker run -it --name pet-detector \
    -v <path to pets dir>:/tensorflow/workspace/<name> \
    -p 8080:8080 \
    <image name> \
    /bin/bash
```  

For this example I would be swapping ```<path to pets>``` with where my pets directory is. This has to be a fully qualified path. ```NO RELATIVE PATHS```.   

- ```<name>``` - Will be the project name. For this example ```/tensorflow/workspace/pets``` would make sense  
- ```<image name>``` - Will be the tag we gave our container earlier. For this example this would be ```tf-obj-cpu:1.14```  
- ```-p 8080:8080``` - This parameter is optional, but this container has Jupyter notebooks pre-installed and also ccomes with the Tensorflow Object Detection notebook. You can go ahead and run Jupyter notebooks and run this notebook to ensure everything is working correctly. The ```-p 8080:8080``` forwards port ```8080``` from inside the container to ```8080``` on your host machine. The password for the ```root``` user is ```root```.  

If all went as planned, you should now see a bash prompt from inside the container. If you run ```pwd``` it should show something like ```/tensorflow/models/research```. If you ```cd``` back a few directories you should see your ```pets``` directory. This will be your local folder mounted into the container. Any changes made on your local machine to the files in this directory, will also be reflected inside the container


## ❗ The following steps will all be completed inside the container ❗

### 📝 Creating TensorFlow Records  

Now that we have generated our annotations and split our dataset into the desired training and testing subsets, it is time to convert our annotations into the so called ```TFRecord``` format.  

There are two steps in doing so:

- Converting the individual *.xml files to a unified *.csv file for each dataset.
- Converting the *.csv files of each dataset to *.record files (TFRecord format)  

Included in this repository is some scripts which will handle this functionality for you.  

> Again! Directory structure is important here, as these scripts are written assuming files are located in certain locations. Follow this guide and you should have no issues  




