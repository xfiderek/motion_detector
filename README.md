# **MOTION DETECTOR** 

*Package contains script that separates moving objects from background having video / webcam stream as an input and displays them as another image*  
*It works in real time and is adaptive to new background, thus if any new static object appears it won't be considered as moving one after some time*  

**Description**  

  *Algorithm calculates median of (periodically added and exchanged) frames, and then assumes that it represents the background.  
  Then absolute difference between every pixel in new frame and median is used to decide whether moving object appears in this pixel*

  *As calculating median is expensive operation it is performed on second thread, which helps to avoid periodic lack of performance*  
  *As mentioned before algorithm updates the median to react to new objects in background, which makes it powerful tool that can be used e.g. in the parking lot*
  
**Sample videos**  

>[Adaptive background presentation](https://www.youtube.com/watch?v=XmBV3SKfKBg)  
>[Indian traffic - SEE DESCRIPTION](https://www.youtube.com/watch?v=AjUrxjvNR2A)  

**Prerequisites**
  
  *OpenCV, numpy*  
  
**Running**
  
  *To run just hit* 
  >python3 main.py -h

  *to learn about possible options* 

**Tips and Trick**  
  *One can pause the video by pressing "p" button*

**Parameters description**
  
  *parameters are listed in config.json*

  > **background_difference_threshold**  
  >> *type* - int  
  >> *value* - (0, 255)    
  >> *description* - if absolute difference between value of particular pixel in median image and frame is higher than this then pixel is marked as object in motion  

  > **refresh_hz**  
  >> *type* - float  
  >> *value* - <0, inf)       
  >> *description* - frequency of refresh of background. if set to zero median is calculated only once (background is assumed to be static)   
    
  > **num_of_frames**   
  >> *type* - int  
  >> *value* - <0, inf)  
  >> *description* - number of frames used to calculate median. Algorithm have to accumulate this number of frames to proceed  

  > **accept_new_frame_time**
  >> *type* - float  
  >> *value* - (0, inf)  
  >> *description* - time after which oldest frame will be replaced by new one to calculate next median

