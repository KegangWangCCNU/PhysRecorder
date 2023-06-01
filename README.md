# PhysRecorder
A tool for recording high availability rPPG datasets.  

## Setup  
First, you need to run Contec SpO2 Assistant and connect to the device via HID (currently not supporting devices with COM ports). When the SpO2 Assistant displays waveforms, PhysRecorder can synchronize and read waveform data. 

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
