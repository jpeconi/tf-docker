# Understanding directory layout  

## Each project will have the following directory layout  

> An empty directory structure like the following has been included. Change the name of the ```project-name``` directory to a name of your choosing and follow the remaining instructions found [here](https://tensorflow-object-detection-api-tutorial.readthedocs.io/en/latest/training.html)  

1. ```annotations```: This folder will be used to store all *.csv files and the respective TensorFlow *.record files, which contain the list of annotations for our dataset images.

2. ```images```: This folder contains a copy of all the images in our dataset, as well as the respective *.xml files produced for each one, once labelImg is used to annotate objects.

    - ```images\train```: This folder contains a copy of all images, and the respective *.xml files, which will be used to train our model.
    - ```images\test```: This folder contains a copy of all images, and the respective *.xml files, which will be used to test our model.

3. ```pre-trained-model```: This folder will contain the pre-trained model of our choice, which shall be used as a starting checkpoint for our training job.

4. ```training```: This folder will contain the training pipeline configuration file *.config, as well as a *.pbtxt label map file and all files generated during the training of our model.