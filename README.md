# PhysRecorder
A tool for recording high availability rPPG datasets, lossless and highly synchronized. This tool aims to guide researchers in collecting high-value rPPG datasets. In past dataset works, some studies lacked attention to signal synchronization and compression formats, making their collected datasets unsuitable for training and only suitable as test sets, which limited the use of the datasets. It is hoped that this program can help everyone quickly and cost-effectively solve this problem.

## Setup  
First, you need to run Contec SpO2 Assistant and connect to the device via HID (currently not supporting devices with COM ports). When the SpO2 Assistant displays waveforms, PhysRecorder can synchronously read waveform data.  

![image](https://github.com/KegangWangCCNU/PICS/blob/main/Contec%20CMS50E.jpg)  

## Setting  
The user interface has multiple options for selection, allowing users to determine the recording duration, video resolution, camera transmission format, and file storage format. At the top are three indicator icons for users to confirm the BVP signal reading status, camera signal reading status, and recording status.  

![image](https://github.com/KegangWangCCNU/PICS/blob/main/PhysRecorder.jpg)  

* `name` Participant name or number.  
* `video` Video title or number.
* `duration` Automatically stop recording after this many seconds; if set to 0, it can only be stopped manually.  
* `size` Resolution, the camera supports all resolutions @30fps in `MJPG` transmission mode. In `YUY2` lossless transmission mode, it supports 480p@30fps, 720p@10fps, and 1080p@5fps.  
* `camera codec` Camera transmission mode. `MJPG` compressed transmission, supporting higher resolution and frame rate; `YUY2` lossless transmission, with higher image quality. 
* `file codec` Video file storage format.  
  The following options can be selected simultaneously.
  * `H264` Using Cisco OpenH264 encoder for encoding, the compression ratio is high, and the degree of damage to physiological signals is high.
  * `I420` Store video in YUV420 format, although there is no compression, some chroma information is discarded, and the degree of damage to physiological signals is small.  
  * `RGBA` Without any compression, all information is preserved, resulting in a larger file size. 
  * `MJPG` Moderate compression ratio, moderate damage to physiological signals.
  * `PNGS` Lossless compression, like RGBA, does not lose information but has a much smaller size. 

## File structure  

To view examples, please download the `Example` folder.

```
Root
├── p001
    ├── v01                      
        ├── pictures_ZIP_RAW_RGB    # PNGS format.
            ├── 00000000.png        # PNG lossless pictures.
            ├── 00000001.png
            ├── ...
        ├── video_ZIP_H264.avi      # H264 format.
        ├── video_ZIP_MJPG.avi      # MJPG format.
        ├── video_RAW_I420.avi      # YUV420 lossless format.
        ├── video_RAW_RGBA.avi      # RGBA lossless format.
        ├── BVP.csv                 # BVP wavefrom with UNIX timestamps.
        ├── frames_timestamp.csv    # UNIX timestamps for each frame.
        ├── info.txt                # Information related to video recording.
        ├── missed_frames.csv       # If all frames are written correctly to the file, it is empty. 
    ├── ... 
├── ...
```

## Compatible with PhysBench  
If you have collected your own dataset, it is recommended to use PhysBench for training and testing. See https://github.com/KegangWangCCNU/PhysBench  
For the collected single video, you can use `inference.py` in PhysBench to extract BVP signals. 

## Use Seq-rPPG to extract BVP signals from the Example  
![image](https://github.com/KegangWangCCNU/PICS/blob/main/ME.gif)  
The above video was recorded using PhysRecorder and saved in the `Example` folder. To extract the BVP signal using PhysBench, use the following command:   
`python inference.py --video face.avi --out BVP.csv`  
Visualize them:  
![image](https://github.com/KegangWangCCNU/PICS/blob/main/BVP.jpg)  
The BVP waveforms extracted from different video formats are shown from top to bottom, and it can be seen that the H264 format causes significant damage to physiological signals.  

## Precautions:
To ensure high synchronization, higher device performance is required.
* For RGBA or I420 formats, make sure the hard drive has sufficient write performance. 
* For PNGS format, ensure that the CPU has enough core numbers to compress in parallel. 
* For H264 format, the CPU performance should be as high as possible. Cisco's encoder will automatically adapt to the CPU. If the performance is insufficient, compression rate will decrease.   


Recommended configuration: 8-core or higher CPU and SSD hard drive.   
**It is strongly discouraged to use USB portable hard drives!**  

## Citation  

If you use PhysRecorder, please cite the following <a href="https://github.com/KegangWangCCNU/PICS/raw/main/PhysBench.pdf" target="_blank">paper</a>
```
@misc{wang2023physbench,
      title={PhysBench: A Benchmark Framework for Remote Physiological Sensing with New Dataset and Baseline}, 
      author={Kegang Wang and Yantao Wei and Mingwen Tong and Jie Gao and Yi Tian and YuJian Ma and ZhongJin Zhao},
      year={2023},
      eprint={2305.04161},
      archivePrefix={arXiv},
      primaryClass={cs.CV}
}
```
