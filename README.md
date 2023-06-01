# PhysRecorder
A tool for recording high availability rPPG datasets.  

## Setup  
First, you need to run Contec SpO2 Assistant and connect to the device via HID (currently not supporting devices with COM ports). When the SpO2 Assistant displays waveforms, PhysRecorder can Synchronously read waveform data.  

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
            ├── 00000000.png        # PNG lossless format.
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

## Use Seq-rPPG to extract BVP signals from Example  
![image](https://github.com/KegangWangCCNU/PICS/blob/main/ME.gif)  

![image](https://github.com/KegangWangCCNU/PICS/blob/main/BVP.gif)  
