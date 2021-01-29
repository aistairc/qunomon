#!/usr/bin/env python
# coding: utf-8

# # AIT Development notebook
# 
# 
# ## notebook of structure
# 
# |#|area name|cell num|description|edit or not|
# |---|---|---|---|---|
# | 1|flags set|1|setting of launch jupyter or ait flag.|no edit|
# | 2|ait-sdk install|1|Use only jupyter launch.<br>find ait-sdk and install.|no edit|
# | 3|create requirements and pip install|3|Use only jupyter launch.<br>create requirements.txt.<br>And install by requirements.txt.|should edit(second cell, you set use modules.)|
# | 4|import|2|you should write use import modules.<br>but bottom lines do not edit.|should edit(first cell, you import your moduel.)|
# | 5|create manifest|1|Use only jupyter launch.<br>create ait.manifest.json.|should edit|
# | 6|create input|1|Use only jupyter launch.<br>create ait.input.json.|should edit|
# | 7|initialize|1|this cell is initialize for ait progress.|no edit|
# | 8|functions|N|you defined measures, resources, downloads in ait.manifesit.json. <br>Define any functions to add these.|should edit|
# | 9|main|1|Read the data set or model and calls the function defined in `functions-area`.|should edit|
# |10|entrypoint|1|Call the main function.|no edit|
# |11|license attribute set|1|Use only notebook launch.<br>Setting attribute for license.|should edit|
# |12|prepare deploy|1|Use only notebook launch.<br>Convert to python programs and create dag.py.|no edit|
# 
# ## notebook template revision history
# 
# ### 1.0.1 2020/10/21
# 
# * add revision history
# * separate `create requirements and pip install` editable and noeditable
# * separate `import` editable and noeditable
# 
# ### 1.0.0 2020/10/12
# 
# * new cerarion

# In[1]:


#########################################
# area:flags set
# do not edit
#########################################

# Determine whether to start AIT or jupyter by startup argument
import sys
is_ait_launch = (len(sys.argv) == 2)


# In[2]:


#########################################
# area:ait-sdk install
# do not edit
#########################################
if not is_ait_launch:
    # get ait-sdk file name
    from pathlib import Path
    from glob import glob
    import re

    def numericalSort(value):
        numbers = re.compile(r'(\d+)')
        parts = numbers.split(value)
        parts[1::2] = map(int, parts[1::2])
        return parts
    latest_sdk_file_path=sorted(glob('../lib/*.whl'), key=numericalSort)[-1]

    ait_sdk_name = Path(latest_sdk_file_path).name
    
    # copy to develop dir
    import shutil
    current_dir = get_ipython().run_line_magic('pwd', '')
    shutil.copyfile(f'../lib/{ait_sdk_name}', f'{current_dir}/{ait_sdk_name}')

    # install ait-sdk
    get_ipython().system('pip install --upgrade pip')
    get_ipython().system('pip install --force-reinstall ./$ait_sdk_name')


# In[3]:


#########################################
# area:create requirements and pip install
# do not edit
#########################################
if not is_ait_launch:
    from ait_sdk.common.files.ait_requirements_generator import AITRequirementsGenerator
    requirements_generator = AITRequirementsGenerator()


# In[4]:


#########################################
# area:create requirements and pip install
# should edit
#########################################
if not is_ait_launch:
    requirements_generator.add_package('Cython')
    requirements_generator.add_package('docopt')
    requirements_generator.add_package('clint')
    requirements_generator.add_package('crontab')
    requirements_generator.add_package('tablib')
    requirements_generator.add_package('matplotlib')
    requirements_generator.add_package('Pillow')
    requirements_generator.add_package('pycocotools')
    requirements_generator.add_package('tensorflow','2.4.0')
    requirements_generator.add_package('lxml')
    requirements_generator.add_package('tf_slim')
    requirements_generator.add_package('pandas')
    requirements_generator.add_package('numpy')
    requirements_generator.add_package('ipython')
    requirements_generator.add_package('zipp','3.1.0')


# In[5]:


#########################################
# area:create requirements and pip install
# do not edit
#########################################
if not is_ait_launch:
    requirements_generator.add_package(f'./{ait_sdk_name}')
    requirements_path = requirements_generator.create_requirements(current_dir)

    get_ipython().system('pip install -r $requirements_path ')


# In[6]:


#########################################
# area:import
# should edit
#########################################

# import if you need modules cell
import numpy as np
import os
import csv
import pathlib
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile
import json
import pandas as pd
import glob
import shutil
from pathlib import Path
from os import makedirs, path
from collections import Iterable
from io import StringIO
from matplotlib import pyplot as plt
from PIL import Image
from IPython.display import display


# In[7]:


#########################################
# area:import
# do not edit
#########################################

# must use modules
import shutil  # do not remove
from ait_sdk.common.files.ait_input import AITInput  # do not remove
from ait_sdk.common.files.ait_output import AITOutput  # do not remove
from ait_sdk.common.files.ait_manifest import AITManifest  # do not remove
from ait_sdk.develop.ait_path_helper import AITPathHelper  # do not remove
from ait_sdk.utils.logging import get_logger, log, get_log_path  # do not remove
from ait_sdk.develop.annotation import measures, resources, downloads, ait_main  # do not remove
# must use modules


# In[8]:


#########################################
# area:create manifest
# should edit
#########################################
if not is_ait_launch:
    from ait_sdk.common.files.ait_manifest_generator import AITManifestGenerator
    
    manifest_genenerator = AITManifestGenerator(current_dir)
    manifest_genenerator.set_ait_name('eval_bdd100k_aicc_tf2.3')
    manifest_genenerator.set_ait_description('''The image classification model infers the image data (.jpg).
Compare the inference result with the correct answer data (.json).
Output the coverage of the comparison result.
!!!Caution!!!
Please set the memory allocation of docker to 4GB or more.''')
    manifest_genenerator.set_ait_author('AIST')
    manifest_genenerator.set_ait_email('')
    manifest_genenerator.set_ait_version('0.1')
    manifest_genenerator.set_ait_quality('https://airc.aist.go.jp/aiqm/quality/internal/Accuracy_of_trained_model')
    manifest_genenerator.set_ait_reference('')
    manifest_genenerator.add_ait_inventories(name='trained_model_checkpoint', 
                                             type_='model', 
                                             description='trained_model_checkpoint', 
                                             format_=['zip'], 
                                             schema='https://www.tensorflow.org/guide/saved_model')
    manifest_genenerator.add_ait_inventories(name='trained_model_graph', 
                                             type_='model', 
                                             description='trained_model_graph', 
                                             format_=['zip'], 
                                             schema='https://www.tensorflow.org/guide/saved_model')
    manifest_genenerator.add_ait_inventories(name='trained_model_protobuf', 
                                             type_='model', 
                                             description='trained_model_protobuf', 
                                             format_=['zip'], 
                                             schema='https://www.tensorflow.org/guide/saved_model')
    manifest_genenerator.add_ait_inventories(name='test_set_images', 
                                             type_='dataset', 
                                             description='image_dataset（bdd100K）', 
                                             format_=['zip'], 
                                             schema='https://bdd-data.berkeley.edu/')
    manifest_genenerator.add_ait_inventories(name='test_set_labels', 
                                             type_='dataset', 
                                             description='image_label_dataset（bdd100K）', 
                                             format_=['json'], 
                                             schema='https://bdd-data.berkeley.edu/')
    manifest_genenerator.add_ait_inventories(name='labels_define', 
                                             type_='dataset', 
                                             description='labels_define', 
                                             format_=['txt'], 
                                             schema='https://github.com/tensorflow/models/tree/master/research/object_detection/data')
    manifest_genenerator.add_ait_measures(name='traffic_sign_accuracy', 
                                          type_='float', 
                                          description='accuracy predicted of traffic_sign', 
                                          structure='single')
    manifest_genenerator.add_ait_measures(name='traffic_light_accuracy', 
                                          type_='float', 
                                          description='accuracy predicted of traffic_light', 
                                          structure='single')
    manifest_genenerator.add_ait_measures(name='car_accuracy', 
                                          type_='float', 
                                          description='accuracy predicted of car', 
                                          structure='single')
    manifest_genenerator.add_ait_measures(name='rider_accuracy', 
                                          type_='float', 
                                          description='accuracy predicted of rider', 
                                          structure='single')
    manifest_genenerator.add_ait_measures(name='motor_accuracy', 
                                          type_='float', 
                                          description='accuracy predicted of motor', 
                                          structure='single')
    manifest_genenerator.add_ait_measures(name='person_accuracy', 
                                          type_='float', 
                                          description='accuracy predicted of person', 
                                          structure='single')
    manifest_genenerator.add_ait_measures(name='bus_accuracy', 
                                          type_='float', 
                                          description='accuracy predicted of bus', 
                                          structure='single')
    manifest_genenerator.add_ait_measures(name='truck_accuracy', 
                                          type_='float', 
                                          description='accuracy predicted of truck', 
                                          structure='single')
    manifest_genenerator.add_ait_measures(name='bike_accuracy', 
                                          type_='float', 
                                          description='accuracy predicted of bike', 
                                          structure='single')
    manifest_genenerator.add_ait_measures(name='train_accuracy', 
                                          type_='float', 
                                          description='accuracy predicted of train', 
                                          structure='single')
    manifest_genenerator.add_ait_resources(name='all_label_accuracy_csv',  
                                           type_='table', 
                                           description='accuracy of all label')
    manifest_genenerator.add_ait_resources(name='all_label_accuracy_png', 
                                           type_='picture', 
                                           description='accuracy of all label')
    manifest_genenerator.add_ait_downloads(name='Log', 
                                           description='AIT_log')
    manifest_genenerator.add_ait_downloads(name='each_label_accuracy', 
                                           description='accuracy of each label')
    manifest_genenerator.add_ait_downloads(name='each_picture', 
                                           description='predict of each picture')
    manifest_path = manifest_genenerator.write()


# In[9]:


#########################################
# area:create input
# should edit
#########################################
if not is_ait_launch:
    from ait_sdk.common.files.ait_input_generator import AITInputGenerator
    input_generator = AITInputGenerator(manifest_path)
    input_generator.add_ait_inventories(name='trained_model_checkpoint',
                                        value='trained_model_checkpoint/trained_model_checkpoint.zip')
    input_generator.add_ait_inventories(name='trained_model_graph',
                                        value='trained_model_graph/trained_model_graph.zip')
    input_generator.add_ait_inventories(name='trained_model_protobuf',
                                        value='trained_model_protobuf/trained_model_protobuf.zip')
    input_generator.add_ait_inventories(name='test_set_images',
                                        value='test_set_images/test_set_images.zip')
    input_generator.add_ait_inventories(name='test_set_labels',
                                        value='test_set_labels/bdd100k_labels_images_val.json')
    input_generator.add_ait_inventories(name='labels_define',
                                        value='labels_define/mscoco_complete_label_map.pbtxt')
    input_generator.write()


# In[10]:


#########################################
# area:initialize
# do not edit
#########################################

logger = get_logger()

ait_manifest = AITManifest()
ait_input = AITInput(ait_manifest)
ait_output = AITOutput(ait_manifest)

if is_ait_launch:
    # launch from AIT
    current_dir = path.dirname(path.abspath(__file__))
    path_helper = AITPathHelper(argv=sys.argv, ait_input=ait_input, ait_manifest=ait_manifest, entry_point_dir=current_dir)
else:
    # launch from jupyter notebook
    # ait.input.json make in input_dir
    input_dir = '/usr/local/qai/mnt/ip/job_args/1/1'
    current_dir = get_ipython().run_line_magic('pwd', '')
    path_helper = AITPathHelper(argv=['', input_dir], ait_input=ait_input, ait_manifest=ait_manifest, entry_point_dir=current_dir)

ait_input.read_json(path_helper.get_input_file_path())
ait_manifest.read_json(path_helper.get_manifest_file_path())

### do not edit cell


# In[11]:


if not is_ait_launch:
    
    get_ipython().system('apt-get update -yqq')
    get_ipython().system('apt-get install gcc g++ make libffi-dev libssl-dev -yqq')
    get_ipython().system('apt-get install python-lxml -y')
    get_ipython().system('apt-get install python-dev libxml2 libxml2-dev libxslt-dev curl -y')

    get_ipython().system('export PYTHONPATH=$PYTHONPATH:/tensorflow/models/research:/tensorflow/')

    get_ipython().run_line_magic('cd', '/tmp')
    get_ipython().system('apt-get install -y unzip')
    get_ipython().system('curl -OL https://github.com/google/protobuf/releases/download/v3.9.0/protoc-3.9.0-linux-x86_64.zip')
    get_ipython().system('unzip -d protoc3 protoc-3.9.0-linux-x86_64.zip')
    get_ipython().system('mv protoc3/bin/* /usr/local/bin/')
    get_ipython().system('mv protoc3/include/* /usr/local/include/')
    get_ipython().system('rm -rf protoc-3.9.0-linux-x86_64.zip protoc3')


# In[12]:


if not is_ait_launch:
    get_ipython().system('apt-get install git -y')
    get_ipython().system('git clone https://github.com/cocodataset/cocoapi.git')
    get_ipython().run_line_magic('cd', '/tmp/cocoapi/PythonAPI')
    get_ipython().system('python3 setup.py build_ext --inplace')
    get_ipython().system('rm -rf build')
    get_ipython().system('python3 setup.py build_ext install')
    get_ipython().system('rm -rf build')

    get_ipython().system('mkdir /tensorflow')
    get_ipython().run_line_magic('cd', '/tensorflow')
    get_ipython().system('git clone https://github.com/tensorflow/models.git')
    get_ipython().run_line_magic('cd', '/tensorflow/models/research')
    get_ipython().system('protoc object_detection/protos/*.proto --python_out=.')
    
    get_ipython().run_line_magic('cd', '/workdir/root/develop')


# In[13]:


sys.path.append(os.path.join(Path().resolve(), '/tensorflow/models/research'))

from object_detection.utils import ops as utils_ops
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util

utils_ops.tf = tf.compat.v1
tf.gfile = tf.io.gfile

g_total_accuracy = []

resultFile = []
# With a range of -1 you will get evrything
limit_box_range = 0
# Obtaining yolo results
g_image_name = ""
count_traffic_label = 0
gt_list_boxes = []

total_correct_predicted = [0,0,0,0,0,0,0,0,0,0]
total_GT_correct_predicted = [0,0,0,0,0,0,0,0,0,0]
total_predicted_per_label = [0,0,0,0,0,0,0,0,0,0]
correct_predicted = [0,0,0,0,0,0,0,0,0,0]

jsonFileName = ""

average_accuracy = []
avg_acc_per_traffic_sign = []
avg_acc_per_traffic_light = []
avg_acc_per_car = []
avg_acc_per_rider = []
avg_acc_per_motor = []
avg_acc_per_person = []
avg_acc_per_bus = []
avg_acc_per_truck = []
avg_acc_per_bike = []
avg_acc_per_train = []

f_each = []


# In[14]:


def _run_inference_for_single_image(model, image) -> np.ndarray:
    image = np.asarray(image)
    # The input needs to be a tensor, convert it using `tf.convert_to_tensor`.
    input_tensor = tf.convert_to_tensor(image)
    # The model expects a batch of images, so add an axis with `tf.newaxis`.
    input_tensor = input_tensor[tf.newaxis,...]

    # Run inference
    model_fn = model.signatures['serving_default']
    output_dict = model_fn(input_tensor)

    # All outputs are batches tensors.
    # Convert to numpy arrays, and take index [0] to remove the batch dimension.
    # We're only interested in the first num_detections.
    num_detections = int(output_dict.pop('num_detections'))
    output_dict = {key:value[0, :num_detections].numpy() 
                                for key,value in output_dict.items()}
    output_dict['num_detections'] = num_detections

    # detection_classes should be ints.
    output_dict['detection_classes'] = output_dict['detection_classes'].astype(np.int64)

    # Handle models with masks:
    if 'detection_masks' in output_dict:
        # Reframe the the bbox mask to the image size.
        detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(
                            output_dict['detection_masks'], output_dict['detection_boxes'],
                            image.shape[0], image.shape[1])			
        detection_masks_reframed = tf.cast(detection_masks_reframed > 0.5, tf.uint8)
        output_dict['detection_masks_reframed'] = detection_masks_reframed.numpy()

    return output_dict


# In[15]:


def _read_labels(label_path) -> np.ndarray:
    labels = json.load(open(label_path, 'r'))
    if not isinstance(labels, Iterable):
        labels = [labels]
    return labels


# In[16]:


def _get_boxes(objects) -> np.ndarray:
    return [o for o in objects if ('box2d' in o and o['box2d'] is not None)
            or ('box3d' in o and o['box3d'] is not None)]


# In[17]:


def _get_id_label(current_object_label) -> int:
    if current_object_label == "traffic sign":
        #traffic_sign = 0
        return 0
    elif current_object_label == "traffic light":
        #traffic light = 1
        return 1
    elif current_object_label == "car":
        #car = 2
        return 2
    elif current_object_label == "rider":
        #rider = 3
        return 3
    elif current_object_label == "motor":
        #motor = 4
        return 4
    elif current_object_label == "person":
        #person = 5
        return 5
    elif current_object_label == "bus":
        #bus = 6
        return 6
    elif current_object_label == "truck":
        #truck = 7
        return 7
    elif current_object_label == "bike":
        #bike = 8
        return 8
    elif current_object_label == "train":
        #train = 9
        return 9
    return -1


# In[18]:


def _get_label_from_id(id) -> str:
    if id == 0:
        return "traffic sign"
    elif id == 1:
        return "traffic light"
    elif id == 2:
        return "car"
    elif id == 3:
        return "rider"
    elif id == 4:
        return "motor"
    elif id == 5:
        return "person"
    elif id == 6:
        return "bus"
    elif id == 7:
        return "truck"
    elif id == 8:
        return "bike"
    elif id == 9:
        return "train"
    return ""


# In[19]:


def _adding_avg_label_from_id(id, value, avg_acc_per_traffic_sign, avg_acc_per_traffic_light, 
                                avg_acc_per_car, avg_acc_per_rider, avg_acc_per_motor, avg_acc_per_person, 
                                avg_acc_per_bus, avg_acc_per_truck, avg_acc_per_bike, avg_acc_per_train):
    if id == 0:
        avg_acc_per_traffic_sign.append(value)
    elif id == 1:
        avg_acc_per_traffic_light.append(value)
    elif id == 2:
        avg_acc_per_car.append(value)
    elif id == 3:
        avg_acc_per_rider.append(value)
    elif id == 4:
        avg_acc_per_motor.append(value)
    elif id == 5:
        avg_acc_per_person.append(value)
    elif id == 6:
        avg_acc_per_bus.append(value)
    elif id == 7:
        avg_acc_per_truck.append(value)
    elif id == 8:
        avg_acc_per_bike.append(value)
    elif id == 9:
        avg_acc_per_train.append(value)

    return avg_acc_per_traffic_sign, avg_acc_per_traffic_light, avg_acc_per_car, avg_acc_per_rider, avg_acc_per_motor, avg_acc_per_person, avg_acc_per_bus, avg_acc_per_truck, avg_acc_per_bike, avg_acc_per_train


# In[20]:


def _search_image_information(objects, image_name) -> np.ndarray:
    list_boxes = []
    for counter,o in enumerate(objects):
        if o['name'] != image_name:
            continue

        for b in _get_boxes(o["labels"]):

            current_object_label = b['category']

            x1 = b['box2d']['x1']
            y1 = b['box2d']['y1']
            x2 = b['box2d']['x2']
            y2 = b['box2d']['y2']

            if abs(x1 - x2) < limit_box_range and abs(y1 - y2) < limit_box_range:
                continue


            # Last value is to determine if this box has been found or not
            list_boxes.append([current_object_label,x1,y1,x2,y2, False])

        break

    return list_boxes


# In[21]:


def _load_labels_ground_truth(gt_list_boxes, total_GT_correct_predicted):
    list_ground_truth = [0,0,0,0,0,0,0,0,0,0]
    for counter, box in enumerate(gt_list_boxes):
        id = _get_id_label(box[0])
        list_ground_truth[id] = list_ground_truth[id] + 1
        total_GT_correct_predicted[id] = total_GT_correct_predicted[id] + 1
    return list_ground_truth,total_GT_correct_predicted


# In[22]:


def _averageOfList(num) -> float:
    sumOfNumbers = 0
    for t in num:
        sumOfNumbers = sumOfNumbers + t

    avg = sumOfNumbers / len(num)
    return avg


# In[23]:


# JSONファイルと推論結果を比較する
def _compare_json(gt_list_boxes, objects, total_GT_correct_predicted,avg_acc_per_traffic_sign, avg_acc_per_traffic_light, 
                                avg_acc_per_car, avg_acc_per_rider, avg_acc_per_motor, avg_acc_per_person, 
                                avg_acc_per_bus, avg_acc_per_truck, avg_acc_per_bike, avg_acc_per_train) -> None:

    for line in resultFile:

        listWords = line.split(" ")
        if (listWords[0] == "Enter"):
            # CHECK ACCURACY OF PREVIOUS IMAGE
            if len(gt_list_boxes) > 0:
                total_labels = len(gt_list_boxes)

                list_ground_truth,total_GT_correct_predicted = _load_labels_ground_truth(gt_list_boxes,total_GT_correct_predicted)

                labels_found = 0
                # WRITE RESULTS IN A FILE
                for box in gt_list_boxes:
                    if box[5]:
                        labels_found = labels_found + 1

                labels_found = 0
                for counter, items in enumerate(list_ground_truth):
                    labels_found = labels_found + correct_predicted[counter]

                f_each.append(str(g_image_name)+" ACCURACY of labels found: "+str(labels_found/total_labels)+"\n")

                avg_acc = 0

                for counter, items in enumerate(list_ground_truth):

                    if items == 0:
                        f_each.append(_get_label_from_id(counter)+ "- Correct Predicted/labels in image:"+ str(correct_predicted[counter]) + "/" + str(items) + " = 0\n")
                    else:
                        f_each.append(_get_label_from_id(counter)+ "- Correct Predicted/labels in image:"+ str(correct_predicted[counter]) + "/" + str(items) + " = " +  str(correct_predicted[counter]/items) + "\n")

                    if predicted_per_label[counter] == 0:
                        f_each.append(str(_get_label_from_id(counter))+ "- Good predicted(TP)/total predicted(FP):"+ str(correct_predicted[counter])+ "/"+str(predicted_per_label[counter])+" = 0\n")
                        f_each.append(str(_get_label_from_id(counter))+ "- False predicted(FP)/total predicted(FP):"+ str(predicted_per_label[counter] - correct_predicted[counter])+ "/"+str(predicted_per_label[counter])+" = 0\n")
                    else:
                        f_each.append(str(_get_label_from_id(counter))+ "- Good predicted(TP)/total predicted:"+ str(correct_predicted[counter]) + "/"+str(predicted_per_label[counter])+" = "+ str(correct_predicted[counter]/predicted_per_label[counter]) + "\n")
                        f_each.append(str(_get_label_from_id(counter))+ "- False predicted(FP)/total predicted:"+ str(predicted_per_label[counter] - correct_predicted[counter]) + "/"+str(predicted_per_label[counter])+" = "+ str((predicted_per_label[counter] - correct_predicted[counter])/predicted_per_label[counter]) + "\n")


                    if predicted_per_label[counter] > 0 and items == 0:
                        f_each.append(str(_get_label_from_id(counter))+ "- Accuracy: 0 \n")
                        label_avg_acc = 0
                        avg_acc_per_traffic_sign, avg_acc_per_traffic_light, avg_acc_per_car, avg_acc_per_rider, avg_acc_per_motor, avg_acc_per_person, avg_acc_per_bus, avg_acc_per_truck, avg_acc_per_bike, avg_acc_per_train = _adding_avg_label_from_id(counter, 0, avg_acc_per_traffic_sign, avg_acc_per_traffic_light, avg_acc_per_car, avg_acc_per_rider, avg_acc_per_motor, avg_acc_per_person, avg_acc_per_bus, avg_acc_per_truck, avg_acc_per_bike, avg_acc_per_train)
                    elif predicted_per_label[counter] == 0 and items > 0:
                        f_each.append(str(_get_label_from_id(counter))+ "- Accuracy: 0 \n")
                        label_avg_acc = 0
                        avg_acc_per_traffic_sign, avg_acc_per_traffic_light, avg_acc_per_car, avg_acc_per_rider, avg_acc_per_motor, avg_acc_per_person, avg_acc_per_bus, avg_acc_per_truck, avg_acc_per_bike, avg_acc_per_train = _adding_avg_label_from_id(counter, 0, avg_acc_per_traffic_sign, avg_acc_per_traffic_light, avg_acc_per_car, avg_acc_per_rider, avg_acc_per_motor, avg_acc_per_person, avg_acc_per_bus, avg_acc_per_truck, avg_acc_per_bike, avg_acc_per_train)
                    elif predicted_per_label[counter] == 0 and items == 0:
                        f_each.append(str(_get_label_from_id(counter))+ "- Accuracy: 0 \n")
                        avg_acc_per_traffic_sign, avg_acc_per_traffic_light, avg_acc_per_car, avg_acc_per_rider, avg_acc_per_motor, avg_acc_per_person, avg_acc_per_bus, avg_acc_per_truck, avg_acc_per_bike, avg_acc_per_train = _adding_avg_label_from_id(counter, 100, avg_acc_per_traffic_sign, avg_acc_per_traffic_light, avg_acc_per_car, avg_acc_per_rider, avg_acc_per_motor, avg_acc_per_person, avg_acc_per_bus, avg_acc_per_truck, avg_acc_per_bike, avg_acc_per_train)
                        label_avg_acc = 0
                    else: # It has predicted correctly that there are any label of the object searched
                        f_each.append(str(_get_label_from_id(counter))+ "- Accuracy: " + str((correct_predicted[counter]/items)*100) + " \n")
                        label_avg_acc = (correct_predicted[counter]/items)*100
                        avg_acc_per_traffic_sign, avg_acc_per_traffic_light, avg_acc_per_car, avg_acc_per_rider, avg_acc_per_motor, avg_acc_per_person, avg_acc_per_bus, avg_acc_per_truck, avg_acc_per_bike, avg_acc_per_train = _adding_avg_label_from_id(counter, ((correct_predicted[counter]/items)*100), avg_acc_per_traffic_sign, avg_acc_per_traffic_light, avg_acc_per_car, avg_acc_per_rider, avg_acc_per_motor, avg_acc_per_person, avg_acc_per_bus, avg_acc_per_truck, avg_acc_per_bike, avg_acc_per_train)

                    avg_acc = avg_acc + label_avg_acc
                    f_each.append("---\n")

                f_each.append(str(g_image_name)+" AVERAGE ACCURACY: "+str(avg_acc/10)+"\n")
                average_accuracy.append(avg_acc/10)

                f_each.append("--------------------------------------------------------------------\n")


            correct_predicted = [0,0,0,0,0,0,0,0,0,0]
            predicted_per_label = [0,0,0,0,0,0,0,0,0,0]
            g_image_name = listWords[3]

            # ADD HERE THE INFORMATION LABELS OF THAT images
            gt_list_boxes = _search_image_information(objects, g_image_name)
        else:
            # using remove() to
            # perform removal
            while("" in listWords) :
                listWords.remove("")
            current_object_label = listWords[0][:-1]

            if current_object_label == "traffi":
                current_object_label = "traffic" + " " + listWords[1][:-1]
                count_traffic_label = 1
            else:
                count_traffic_label = 0


            # 他の物体を認識したときはスルーする
            if _get_id_label(current_object_label) == -1:
                print(current_object_label)
                continue


            # Left_x
            left_x = listWords[2+count_traffic_label]

            # top_y
            top_y = listWords[4+count_traffic_label]

            # width
            width = listWords[6+count_traffic_label]

            # height
            height = listWords[8+count_traffic_label][:-2]

            # Get the X-Y info
            x1 = int(float(left_x))
            y1 = int(float(top_y))
            x2 = x1 + int(float(width))
            y2 = y1 + int(float(height))

            if abs(x1 - x2) < limit_box_range and abs(y1 - y2) < limit_box_range:
                continue
            total_predicted_per_label[_get_id_label(current_object_label)] = total_predicted_per_label[_get_id_label(current_object_label)] + 1
            predicted_per_label[_get_id_label(current_object_label)] = predicted_per_label[_get_id_label(current_object_label)] + 1

            position = -1
            range = 200

            for counter, box in enumerate(gt_list_boxes):
                box_label= box[0]
                box_x1 = box[1]
                if box_label == current_object_label:
                    if range >= abs(box_x1 - x1):
                        range = abs(box_x1 - x1)
                        position = counter

            if position >= 0:
                if gt_list_boxes[position][5] == False:

                    gt_list_boxes[position][5] = True

                    id = _get_id_label(current_object_label)
                    correct_predicted[id] = correct_predicted[id] + 1
                    total_correct_predicted[id] = total_correct_predicted[id] + 1


# In[24]:


def _accuracy_count(total_GT_correct_predicted, avg_acc_per_traffic_sign, avg_acc_per_traffic_light, 
                                avg_acc_per_car, avg_acc_per_rider, avg_acc_per_motor, avg_acc_per_person, 
                                avg_acc_per_bus, avg_acc_per_truck, avg_acc_per_bike, avg_acc_per_train) -> None:

    f_each.append("\n")
    f_each.append("TOTAL\n")
    f_each.append("--------------------------------------------------------------------\n")
    f_each.append("Average accuracy: " + str(_averageOfList(average_accuracy))+"\n")

    string_result_amount_labels = ""
    string_result_acc = ""

    for counter,amount_label in enumerate(total_GT_correct_predicted):

        f_each.append(str(_get_label_from_id(counter)) +"- Amount of labels: " + str(amount_label) + "\n")

        if counter == 0:
            f_each.append(str(_get_label_from_id(counter)) +"- Average accuracy: " + str(_averageOfList(avg_acc_per_traffic_sign))+"\n") 
            string_result_acc = string_result_acc +  str(_averageOfList(avg_acc_per_traffic_sign)) + ","
        elif counter == 1:
            f_each.append(str(_get_label_from_id(counter)) +"- Average accuracy: " + str(_averageOfList(avg_acc_per_traffic_light))+"\n")
            string_result_acc = string_result_acc +  str(_averageOfList(avg_acc_per_traffic_light)) + ","
        elif counter == 2:
            f_each.append(str(_get_label_from_id(counter)) +"- Average accuracy: " + str(_averageOfList(avg_acc_per_car))+"\n")
            string_result_acc = string_result_acc +  str(_averageOfList(avg_acc_per_car)) + ","
        elif counter == 3:
            f_each.append(str(_get_label_from_id(counter)) +"- Average accuracy: " + str(_averageOfList(avg_acc_per_rider))+"\n")
            string_result_acc = string_result_acc +  str(_averageOfList(avg_acc_per_rider)) + ","
        elif counter == 4:
            f_each.append(str(_get_label_from_id(counter)) +"- Average accuracy: " + str(_averageOfList(avg_acc_per_motor))+"\n") 
            string_result_acc = string_result_acc +  str(_averageOfList(avg_acc_per_motor)) + ","
        elif counter == 5:
            f_each.append(str(_get_label_from_id(counter)) +"- Average accuracy: " + str(_averageOfList(avg_acc_per_person))+"\n")
            string_result_acc = string_result_acc +  str(_averageOfList(avg_acc_per_person)) + ","
        elif counter == 6:
            f_each.append(str(_get_label_from_id(counter)) +"- Average accuracy: " + str(_averageOfList(avg_acc_per_bus))+"\n")
            string_result_acc = string_result_acc +  str(_averageOfList(avg_acc_per_bus)) + ","
        elif counter == 7:
            f_each.append(str(_get_label_from_id(counter)) +"- Average accuracy: " + str(_averageOfList(avg_acc_per_truck))+"\n")
            string_result_acc = string_result_acc +  str(_averageOfList(avg_acc_per_truck)) + ","
        elif counter == 8:
            f_each.append(str(_get_label_from_id(counter)) +"- Average accuracy: " + str(_averageOfList(avg_acc_per_bike))+"\n") 
            string_result_acc = string_result_acc +  str(_averageOfList(avg_acc_per_bike)) + ","
        elif counter == 9:
            f_each.append(str(_get_label_from_id(counter)) +"- Average accuracy: " + str(_averageOfList(avg_acc_per_train))+"\n")
            string_result_acc = string_result_acc +  str(_averageOfList(avg_acc_per_train)) + ","

        string_result_amount_labels = string_result_amount_labels + str(amount_label) + ","


        f_each.append("---\n")


# In[25]:


def _view_accuracy_label(total_GT_correct_predicted) -> None:

    false_result = []

    for index,amount_label in enumerate(total_predicted_per_label):
        correct_buffer = total_correct_predicted[index]
        false_buffer = 0

        if amount_label > total_GT_correct_predicted[index]: 
            false_buffer = amount_label - correct_buffer
        else:
            false_buffer = total_GT_correct_predicted[index] - correct_buffer
        false_result.append(false_buffer)

        if correct_buffer == 0:
            g_total_accuracy.append(0)
        else:
            g_total_accuracy.append( correct_buffer / (correct_buffer + false_buffer))

    df = pd.DataFrame({'Name': ["traffic sign","traffic light","car","rider","motor","person","bus","truck","bike","train"],
                    'Original_data': total_GT_correct_predicted, 
                    'Predicted_num': total_predicted_per_label,
                    'Predicted_correct_num': total_correct_predicted,
                    'Predicted_false_num': false_result,
                    'Accuracy': g_total_accuracy})
    print(df)
    # resourcesに追加
    save_all_label_accuracy_csv(df)
    save_all_label_accuracy_png(df)


# In[26]:


# ワイルドカードを使ってファイルの削除
def _remove_glob(pathname, recursive=True):
    for p in glob.glob(pathname, recursive=recursive):
        if os.path.isfile(p):
            os.remove(p)


# In[27]:


# 画像データの解凍
def _load_image(file_path: str) -> np.ndarray:
    with zipfile.ZipFile(file_path) as existing_zip:            

        existing_zip.extractall('/tmp')

        path_to_test_images_dir = pathlib.Path('/tmp')
        test_image_path = sorted(list(path_to_test_images_dir.glob("*.jpg")))
        data = test_image_path
    return data


# In[28]:


#########################################
# area:functions
# should edit
#########################################

@log(logger)
@downloads(ait_output, path_helper, 'each_picture', '{}predict.jpg')
def save_images(model, image_path_list, category_index, file_path: str=None) -> None:
    out_files = []
    
    for image_path in image_path_list:
        
        # the array based representation of the image will be used later in order to prepare the
        # result image with boxes and labels on it.
        image_np = np.array(Image.open(image_path))
        # Actual detection.
        output_dict = _run_inference_for_single_image(model, image_np)

        tmp_image_name = 'Enter Image Path: ' + image_path.name
        resultFile.append(tmp_image_name)

        for index, item in enumerate(output_dict['detection_boxes']):
            kind = output_dict['detection_classes'][index]
            accuracy = output_dict['detection_scores'][index]
            accuracy_int = int(accuracy * 100)

            # boxの位置情報はymin、xmin、ymax、xmaxで、０～１の範囲
            # imageは1280*720なので、x軸×1280、y軸×720
            if accuracy_int >= 50:
                left_x = int(output_dict['detection_boxes'][index][1] * 1280)
                top_y = int(output_dict['detection_boxes'][index][0] * 780)
                width = int(output_dict['detection_boxes'][index][3] * 1280)
                height = int(output_dict['detection_boxes'][index][2] * 780)

                kind_name = ""
                if category_index[kind]['name'] == "bicycle":
                            kind_name = "bike"
                elif category_index[kind]['name'] == "motorcycle":
                            kind_name = "motor"
                else:
                            kind_name = category_index[kind]['name']

                tmp_buffer = kind_name + ': ' + str(accuracy_int) + '%\t(left_x: ' + str(left_x) +                                         '	 top_y: ' + str(top_y) + '	 width: ' + str(width) + '	 height: ' + str(height) + ')'
                resultFile.append(tmp_buffer)


        # Visualization of the results of a detection.
        vis_util.visualize_boxes_and_labels_on_image_array(
                image_np,
                output_dict['detection_boxes'],
                output_dict['detection_classes'],
                output_dict['detection_scores'],
                category_index,
                instance_masks=output_dict.get('detection_masks_reframed', None),
                use_normalized_coordinates=True,
                min_score_thresh=.5,
                line_thickness=8)

        predict_image = file_path.format(image_path.name[0:-4])
        out_files.append(predict_image)
        Image.fromarray(image_np).save(predict_image)

    return out_files


# In[29]:


#########################################
# area:functions
# should edit
#########################################

@log(logger)
@resources(ait_output, path_helper, 'all_label_accuracy_csv', 'all_label_accuracy.csv')
def save_all_label_accuracy_csv(df, file_path: str=None) -> None:
    df.to_csv(file_path)


# In[30]:


#########################################
# area:functions
# should edit
#########################################

@log(logger)
@resources(ait_output, path_helper, 'all_label_accuracy_png', 'all_label_accuracy.png')
def save_all_label_accuracy_png(df, file_path: str=None) -> None:
    # 以前の画像ファイルがあれば削除
    _remove_glob(str(Path(file_path).parent)+ '/*.png')
    
    fig = plt.figure(figsize=(12, 8), dpi=100)
    ax = fig.subplots()
    ax.axis('off')
    ax.axis('tight')
    tmp_table = ax.table(cellText=df.values,
        colLabels=df.columns,
        rowLabels=df.index,
        bbox=[0,0,1,1])
    plt.savefig(file_path)
    plt.close('all')


# In[31]:


#########################################
# area:functions
# should edit
#########################################

@log(logger)
@downloads(ait_output, path_helper, 'each_label_accuracy', 'each_label_accuracy.csv')
def save_each_label_accuracy(file_path: str=None) -> None:
    with open(file_path, 'w') as f:
        writer = csv.writer(f)
        for buf in f_each:
            writer.writerow(buf)


# In[32]:


#########################################
# area:functions
# should edit
#########################################

@log(logger)
@measures(ait_output, 'traffic_sign_accuracy')
def measure_traffic_sign_accuracy(accuracy):
    return accuracy


# In[33]:


#########################################
# area:functions
# should edit
#########################################

@log(logger)
@measures(ait_output, 'traffic_light_accuracy')
def measure_traffic_light_accuracy(accuracy):
    return accuracy


# In[34]:


#########################################
# area:functions
# should edit
#########################################

@log(logger)
@measures(ait_output, 'car_accuracy')
def measure_car_accuracy(accuracy):
    return accuracy


# In[35]:


#########################################
# area:functions
# should edit
#########################################

@log(logger)
@measures(ait_output, 'rider_accuracy')
def measure_rider_accuracy(accuracy):
    return accuracy


# In[36]:


#########################################
# area:functions
# should edit
#########################################

@log(logger)
@measures(ait_output, 'motor_accuracy')
def measure_motor_accuracy(accuracy):
    return accuracy


# In[37]:


#########################################
# area:functions
# should edit
#########################################

@log(logger)
@measures(ait_output, 'person_accuracy')
def measure_person_accuracy(accuracy):
    return accuracy


# In[38]:


#########################################
# area:functions
# should edit
#########################################

@log(logger)
@measures(ait_output, 'bus_accuracy')
def measure_bus_accuracy(accuracy):
    return accuracy


# In[39]:


#########################################
# area:functions
# should edit
#########################################

@log(logger)
@measures(ait_output, 'truck_accuracy')
def measure_truck_accuracy(accuracy):
    return accuracy


# In[40]:


#########################################
# area:functions
# should edit
#########################################

@log(logger)
@measures(ait_output, 'bike_accuracy')
def measure_bike_accuracy(accuracy):
    return accuracy


# In[41]:


#########################################
# area:functions
# should edit
#########################################

@log(logger)
@measures(ait_output, 'train_accuracy')
def measure_train_accuracy(accuracy):
    return accuracy


# In[42]:


#########################################
# area:functions
# should edit
#########################################

@log(logger)
@downloads(ait_output, path_helper, 'Log', 'ait.log')
def move_log(file_path: str=None) -> None:
    shutil.move(get_log_path(), file_path)


# In[43]:


#########################################
# area:main
# should edit
#########################################

@log(logger)
@ait_main(ait_output, path_helper)
def main() -> None:

    # インベントリのMNISTラベル・画像を読み込み
    image_path = ait_input.get_inventory_path('test_set_images')
    
    model_checkpoint_path = ait_input.get_inventory_path('trained_model_checkpoint')
    model_graph_path = ait_input.get_inventory_path('trained_model_graph')
    model_protobuf_path = ait_input.get_inventory_path('trained_model_protobuf')

    # モデル読み込み
    zipfile.ZipFile(model_checkpoint_path).extractall('/tmp')
    zipfile.ZipFile(model_graph_path).extractall('/tmp/ssd_mobilenet_v2_coco')
    zipfile.ZipFile(model_protobuf_path).extractall('/tmp/ssd_mobilenet_v2_coco')
    model = tf.saved_model.load(str('/tmp/ssd_mobilenet_v2_coco/saved_model'))
    
    # jsonファイルのパス
    jsonFileName = ait_input.get_inventory_path('test_set_labels')
    objects = _read_labels(jsonFileName)

    # ラベルの定義読み込み
    label_map_name = ait_input.get_inventory_path('labels_define')
    category_index = label_map_util.create_category_index_from_labelmap(label_map_name, use_display_name=True)
    
    # 画像読み込み
    image_list = _load_image(image_path)
    

    # 推論 (resources)
    save_images(model, image_list, category_index)

    resultFile.append('Enter Image Path: END')

    # JSONファイルと推論結果を比較する
    _compare_json(gt_list_boxes, objects, total_GT_correct_predicted, avg_acc_per_traffic_sign, avg_acc_per_traffic_light, 
                                avg_acc_per_car, avg_acc_per_rider, avg_acc_per_motor, avg_acc_per_person, 
                                avg_acc_per_bus, avg_acc_per_truck, avg_acc_per_bike, avg_acc_per_train)
    # 推論結果の集計
    _accuracy_count(total_GT_correct_predicted, avg_acc_per_traffic_sign, avg_acc_per_traffic_light, 
                                avg_acc_per_car, avg_acc_per_rider, avg_acc_per_motor, avg_acc_per_person, 
                                avg_acc_per_bus, avg_acc_per_truck, avg_acc_per_bike, avg_acc_per_train)
    # label毎に確率を集計 (resources)
    _view_accuracy_label(total_GT_correct_predicted)
    
    # download
    save_each_label_accuracy()

    # measure
    measure_traffic_sign_accuracy(g_total_accuracy[0])
    measure_traffic_light_accuracy(g_total_accuracy[1])
    measure_car_accuracy(g_total_accuracy[2])
    measure_rider_accuracy(g_total_accuracy[3])
    measure_motor_accuracy(g_total_accuracy[4])
    measure_person_accuracy(g_total_accuracy[5])
    measure_bus_accuracy(g_total_accuracy[6])
    measure_truck_accuracy(g_total_accuracy[7])
    measure_bike_accuracy(g_total_accuracy[8])
    measure_train_accuracy(g_total_accuracy[9])

    
    move_log()


# In[ ]:


#########################################
# area:entory point
# do not edit
#########################################
if __name__ == '__main__':
    main()


# In[ ]:


#########################################
# area:license attribute set
# should edit
#########################################
ait_owner='AIST'
ait_creation_year='2020'


# In[ ]:


#########################################
# area:prepare deproy
# do not edit
#########################################

if not is_ait_launch:
    from ait_sdk.deploy import prepare_deploy
    from ait_sdk.license.license_generator import LicenseGenerator
    
    current_dir = get_ipython().run_line_magic('pwd', '')
    prepare_deploy(ait_manifest, ait_sdk_name, current_dir, requirements_path, is_remote_deploy=True)
    
    # output License.txt
    license_generator = LicenseGenerator()
    license_generator.write('../top_dir/LICENSE.txt', ait_creation_year, ait_owner)


# In[ ]:




