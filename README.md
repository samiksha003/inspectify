# INSPECTIFY
## Criminal-Identification-Using-Face-Recognition


Problem Description: The security of India is becoming ever more
 critical in this new world. There is an expectation of a slew 
 of organized crime activities that may attempt to cripple our 
 law enforcement and defense agencies. In such a scenario, 
 technology becomes of paramount importance.  
 

INSPECTIFY is a desktop app which upon receiving data via image
 or video(live or recorded) identifies the criminal based on the
 criminal history of that person.

## Usecases:
- Crowded places (railway or metro station, bus stand) where pickpocketers, kidnappers could be recognised as soon as they enter the field of camera.
- Criminal could be identified on the entrance itself (of schools, colleges , banks and other social or private places).
- Upon identification it alerts us and shows up his/her criminal history.
- Runaway criminals and a missing person could be caught.



## Demo

![Screenshot 2022-05-27 at 2 01 29 PM](https://user-images.githubusercontent.com/60481406/170664478-18361f61-3b33-4d46-b680-111e5f9f1617.png)
![Screenshot 2022-05-27 at 2 05 19 PM](https://user-images.githubusercontent.com/60481406/170664861-fe65c415-d8b2-45b9-8833-c8817c2f8bbd.png)
![Screenshot 2022-05-27 at 2 08 28 PM](https://user-images.githubusercontent.com/60481406/170665089-10a70f14-1351-49c5-a047-46c37374d69e.png)
![Screenshot 2022-05-27 at 2 09 25 PM](https://user-images.githubusercontent.com/60481406/170665421-208d0cdb-f62d-45cb-98f8-702ab90aecce.png)
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
- Make sure to change the address of folders in the code according your system
- Open the inspectify directory
- Run python3 home.py

 
```
    
## Future Improvement

- Capture the faces of the people in the video, and then analyze another video to see how many of the persons in the first video are seen again in the second video and at what times, Now, if the above technology is used for thousands of videos gathered from hundreds of intelligence sources, with cross-checks across all videos, really significant information on patterns in any form of organized crime can be identified.
- Voice message as soon as criminal is identified.
- Combined with biometrics, it could be used for issuing IDs.
- Display the Images of Various prosthetic makeups that a criminal could do.
