FROM ubuntu:bionic

# Update apt with all package repositories
RUN apt-get update && yes | apt-get upgrade

# Create directory to hold tensorflow models
RUN mkdir -p /tensorflow/models

# Update Python to 3.7 and change default Python
RUN apt-get -y install python3.7
RUN ln -s /usr/bin/python3.7 /usr/bin/python
RUN apt-get -y install python3-pip 

RUN python -m pip install pip

# Install required dependencies
# RUN apt-get -y install protobuf-compiler python3-pil python3-lxml
RUN apt-get -y install git

# Clone tensorflow models repository into the folder created
RUN git clone --branch v1.13.0 https://github.com/tensorflow/models.git /tensorflow/models

# Set working directory
WORKDIR /tensorflow/models/research

# Install tensorflow
RUN python -m pip install tensorflow==1.14
RUN python -m pip install Cython==0.29.14
RUN python -m pip install contextlib2==0.6.0.post1
RUN python -m pip install pillow==7.0.0
RUN python -m pip install lxml==4.4.2
RUN python -m pip install jupyter==1.0.0
RUN python -m pip install matplotlib==3.1.2
RUN python -m pip install pandas

ENV DEBIAN_FRONTEND=noninteractive 
RUN apt-get -y install protobuf-compiler python3-tk

RUN protoc object_detection/protos/*.proto --python_out=.

# Add current directory + slim dir to PYTHONPATH
ENV PYTHONPATH=/tensorflow/models/research:/tensorflow/models/research/slim:/tensorflow/models/research/object_detection
RUN jupyter notebook --generate-config --allow-root
RUN echo "c.NotebookApp.password = u'sha1:6a3f528eec40:6e896b6e4828f525a6e20e5411cd1c8075d68619'" >> /root/.jupyter/jupyter_notebook_config.py

COPY ./object_detection_tutorial.ipynb /tensorflow/models/research/object_detection/object_detection_tutorial.ipynb
COPY ./scripts /tensorflow/scripts
