# INSPECTIFY
## Criminal-Identification-Using-Face-Recognition


Problem Description: The worls's security is becoming ever more
 critical in this new era. There is an expectation of a banks 
 of organized crime activities that may attempt to cripple our 
 law enforcement and defence agencies. In such a scenario, 
 technology becomes of uppermost importance.  
 

INSPECTIFY is a desktop app that identifies the criminal based on the criminal history of that person upon receiving data via image or video(live or recorded). 


## Use-cases:
- Crowded places (railway or metro station, bus stand) where pickpocketers, kidnappers could be recognised as soon as they enter the field of camera.
- Criminal could be identified on the gate itself (of schools, colleges , banks and other social or private places).
- Upon identification it alerts us and shows up his/her criminal history.
- Runaway criminals and a missing person could be caught.



## Demo

![Screenshot 2022-05-27 at 2 01 29 PM](https://user-images.githubusercontent.com/60481406/170664478-18361f61-3b33-4d46-b680-111e5f9f1617.png)
![Screenshot 2022-05-28 at 7 36 27 PM](https://user-images.githubusercontent.com/60481406/170828931-6aa80562-179c-4f28-87aa-21600064024a.png)
![Screenshot 2022-05-27 at 2 08 28 PM](https://user-images.githubusercontent.com/60481406/170665089-10a70f14-1351-49c5-a047-46c37374d69e.png)
https://user-images.githubusercontent.com/60481406/170829799-e98b0572-8e56-499f-8767-d71f4af9ba9b.mp4


![Screenshot 2022-05-27 at 6 02 10 PM](https://user-images.githubusercontent.com/60481406/170699995-0fc437cb-96af-4265-bf72-690481aee232.png)
## Features
- Register a new Criminal
    - At least five images of a criminal are required to train the model.
    - details(name, DOB, father's name, gender, profile photo, crimes) are mandatory and automatically stored in an excel sheet(criminal.csv).
    - An error message is prompted if images are less than five or if any image is unclear or small.
    - it automatically creates a folder to store the images and prompts an error message if the system can't do it.
- Image Inspection
    - choose an image and click on identify.
    - If the person were a registered criminal, their name would be displayed in the box.
    - otherwise, the "no criminal found"    message would be prompted
    - can detect more than one criminal simultaneously.
- Video Inspection
    - Choose a video, and it will recognize the criminals throughout the recording.
    - A red frame will surround the recognized criminals, and their names will be displayed in the box.
- Back Button
    - can go back to the previous screen at any point in time.

## Installation

Install my-project following these steps:

```bash
- Clone my project
- Run pip3 install -r requirements.txt (Python 3)
- Open the inspectify directory
- Run python3 home.py

 
```
    
## Future Improvement

- Capture the faces of the people in the video, and then analyze another video to see how many of the persons in the first video are seen again in the second video and at what times, Now, if the above technology is used for thousands of videos gathered from hundreds of intelligence sources, with cross-checks across all videos, really significant information on patterns in any form of organized crime can be identified.
- Voice message as soon as criminal is identified.
- Combined with biometrics, it could be used for issuing IDs.
- Display the Images of Various prosthetic makeups that a criminal could do.
