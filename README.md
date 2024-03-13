## Introduction
ForestSim is a repostitory that utilizes open-mmlab's mmsegmentation toolbox to train and test a model for object recognition and detection in unstructured off-road environments. The data, which consists of segmentation and rgb images, used to train and test models were collected using AirSim and Unreal Engine. Here is a link to our website which contains the collected data [ForestSim Website](https://vailforestsim.github.io/)

## Platform and Hardware used for Data Collection
Data was collected on an Intel NUC NUC11PHKi7 11th Gen Core i7-1165G7 Quad-Core up to 4.70 GHz Processor, 32GB DDR4 RAM, 1TB PCIe NVMe SSD, GeForce RTX 2060 6GB GDDR6 Graphics running the Windows 11 OS. The Windows OS has strong support for both Unreal and AirSim which are essential to set up the environment for data collection. There is also strong support for the MacOS but the hardware needs to be capable enough to run the CPU and GPU intensive environments. 

## Technologies used for data collection
Epic Games Launcher was used to install Unreal Engine and download environments that met the criteria for unstructured environments. AirSim is a plugin which provides a simulation platform for AI research which exposes API’s to interact with a ground vehicle car or air vehicle multirotor programmatically in Unreal Engine to retrieve images, get state, control the vehicle along with many other functionalities. AirSim was utilized to collect rgb, segmentation images using Python 3.7 which was used to interact with AirSim API’s to automate data collection. AirSim also provides other image types along with camera information such as the camera intrinsic matrix from environments running on Unreal Engine. 

## Steps to set up environment
1) First Build AirSim on Windows. Documented steps to do this can be seen on AirSim's official page https://microsoft.github.io/AirSim/build_windows/

2. Once AirSim is built this will create a ready to use plugin bits in the Unreal\Plugins folder that can be dropped into any Unreal project. Drop the plugins folder into any project folder. 

3. Here are steps provided by AirSim to setup a custom environment. https://microsoft.github.io/AirSim/unreal_custenv/. This provides clear intructions on running AirSim on a environment and can be repeated for any custom environment from Unreal Engine.

4. Once you are able to set up an environment with AirSim, here are some steps on using the airsim api to interact with the vehicle and retrieve images. https://microsoft.github.io/AirSim/apis/

5. AirSim supports two motor types Multirotor and Car and directions on setting the configurations for each can be found here https://microsoft.github.io/AirSim/settings/#SimMode. This also provides directions on how to set up the settings.json file that is used for configuration of AirSim. 

6. In the airsim_settigs_json folder within this repo there are two folders, car and multirotor, which provide an example of the settings.json for each motor type. The settings.json in the car folder one was used for the ForestSim dataset.

7. Once the settings.json file is configured you are ready to  begin collecting images. Make sure the settings.json file is in the directory that is used by AirSim and Unreal Engine which can be located using steps provides here https://microsoft.github.io/AirSim/settings/.

# Process Data
### For all python code, the file locations and paths will need to be updated to be usable. The only data the needs to be processed are the segmentation data, the rgb images are not modified from the original collected from AirSim.

## Steps to collect data

1. First run a given environment in Unreal with the AirSim plugin setup and start in AirSimGameMode
2. Once the environment is running, the airsim api can interact with the vehicle and retrieve images
3. Execute the car_path.py using python which will move the car programmtically
4. In parallel execute the car_collect_images.py file which will collect images based on a time interval and save those images to a specified folder. The paths in the python files use a forward slash and should run as is but based on the OS used it may differ so it might need some simple changes to get it to work.

## Steps to process and consolidated segmentation images 
The images collected using AirSim can not be directly used but need to be processed to be usable. Some environments segment the same class of object with different rgbs which need to consolidated to be used. Other environments label different classes the same rgb value for their segmentation images and these type of environments are not usable.

1. Next once you have collected the images for the environments. You have to map each seg ids found in the environment, which can be seen in the class count csv for that environment, to a class of object. The seg ids should match with what you see in the [rgb_ids](rgb_ids.csv) file.
2. This is done by looking through each of the segmentation images collected from each environment and then creating a mapping of each rgb found in the images to its object. Almost all of the rgbs values you will see in the images can be seen in the [rgb_ids](rgb_ids.csv) and have a correspond id. 
3. Create a mapping of the label to the a pre-specified rgb you want to convert the segementation images to. In our case we used this [Class Mapping](tools/post_processing_code/LabelsWRGBS.csv).
4. The below example shows what Seg Ids from the AirSim collected segmentation images correspond to what label

    ![alt text](readme_img.png)

5. Once a mapping like this is created for all the usable environments they must be consolidated. Using the created mapping, like above, each image was iterated pixel by pixel, the Seg Ids corresponding rgb could be found using the [rgb_ids](rgb_ids.csv) and were converted to the rgb specified in the [Class Mapping](tools/post_processing_code/LabelsWRGBS.csv) based on the label.

[Process Segmentation](tools/post_processing_code/ProcessSegmentation.py) was used to process the images and was made for the [Class Mapping](tools/post_processing_code/LabelsWRGBS.csv) found here. 


## Steps to process data for training
1. Once the AirSim segmentation images have been converted based on the [Class Mapping](tools/post_processing_code/LabelsWRGBS.csv), the next step is to convert them into a trainable and testable format. 
2.  Mmsegmentation was used and the documentation for this exists here on their official website https://mmsegmentation.readthedocs.io/en/main/.
3. To train and test, the segmentation images need to be converted pixel by pixel to a format mmsegmentation understands. For example the rgbs per pixel would be just a 1*3 of their id, [id, id, id]. For example all grass pixels would become [1, 1, 1] but as we use zero indexing it will actually become [0, 0 , 0] as grass is the first class.
4. The [Relabel Python File](tools/dataset_converters/forestsim_relabel_one_dim.py) was used to relabel the images and the [Split Python File](tools/dataset_converters/forestsim_train_test_split.py) to get the splits for them.


# Train and Test
1. Here is a guide on how to install mmsegmentation https://github.com/open-mmlab/mmsegmentation/blob/main/docs/en/get_started.md
2. Here you can find the MMSeg Basic Tutorial https://github.com/open-mmlab/mmsegmentation?tab=readme-ov-file and read through them on how to use mmsegmentation. 
3. This repo is set up to be able to train and test. It needs to be installed using `pip install .` or if it works `pip install -v -e .` and then the data will need to be downloaded and added to the correct location. The location can be found in the value of data_root in the config datasets.
4. Reading the docs here https://mmsegmentation.readthedocs.io/en/main/ should help you understand the code in this repo. 
