# FaceRecon
A Production grade Face Recognization based Attendence System with Qt and OpenCV models.

## Architecture

```
.
├── assets/
└── src/
    ├── camera/
    │   ├── __init__.py
    │   └── livecam.py
    ├── db/
    │   └── initializer.py
    ├── gui/
    │   ├── adminpanel.py
    │   ├── home.py
    │   ├── regform.py
    │   ├── regpanel.py
    │   ├── sidebar.py
    │   ├── table.py
    │   ├── userpanel.py
    │   └── window.py
    ├── model/
    └── main.py
```
Here , entry point is ```main.py``` :

* ```main.py``` runs the Qt application loop.
* ```window.py``` called by ```main.py``` holds the main Qt Widget (and other widgets as child).

* ```sidebar.py``` and ```table.py``` these are ui components -> sidebar in all pages and tabelview in admin page inherit code from these files respectively.

#### GUI Pages :
 ```
       +-------------------------------------------------------+
       |                       window.py                       |
       +---------------------------+---------------------------+
                                   |
         +-------------------------+-------------------------+
         |                                                   |
 +-------v-------+                                   +-------v-------+
 |  sidebar.py   |                                   | QStackedWidget|
 +---------------+                                   +-------+-------+
                                                             |
                       +-------------------------------------+-------------------------------------+
                       |                                     |                                     |
             +---------v---------+                 +---------v---------+                 +---------v---------+
             |   userpanel.py    |                 |    regpanel.py    |                 |   adminpanel.py   |
             +---------+---------+                 +----+---------+----+                 +---------+---------+
                       |                                |         |                                  |
                 +-----v-----+                 +--------v--+   +--v--------+                   +-----v-----+
                 | livecam.py|                 | livecam.py|   | regform.py|                   |  table.py |
                 +-----------+                 +-----------+   +-----------+                   +-----------+
```
* These programs hold all the logic inside each page as in gui -> including db calls , face matching , rendering etc.

#### camera/livecam.py
* Handles all camera access and logics like start , stop , capture and get_face_image_embeddings -> called in ```userpanel.py``` and ```regpanel.py``` ; The video widget rendering camera input is a result of this file.

#### db/initializer.py
* Runs everytime the app runs to ensure DataBase tables are present , in absence the script will create two table ```Standard sqlite Table and a Vector Table with sqlite-vec extension``` -> they are mapped by common id.

### model :
This folder contains the models from OpenCV Zoo :

* ```face_detection_yunet_2026may.onnx``` : This model detects face in an image and by program we crop the face out of image with it's help, the cropped face is fed to ->

* ```face_recognition_sface_2021dec.onnx``` takes the cropped face as an input -> process to give data points of face : the vectors describe the face ; An array of 128 elements with 32-bit precision float stored as a flat vector.

### Function : 
* Takes image from camera -> detects face -> extract face features -> performs KNN (K-Nearest Neighbour) search on vector table -> returns the nearest vector whose score is <9 (threshold value is on basis of test) -> maps the returned id to data table -> marks attendence on the data table.

* On register -> similarly processes for face features -> store in vector table the features and data in data table.

## Acknowledgements

- **PySide6**: Official Python bindings for Qt 6, used for building cross-platform desktop GUIs with custom components, layout management, and responsive events.
  - [PySide6 Documentation](https://doc.qt.io/qtforpython-6/)

- **OpenCV (`opencv-python`)**: Open-source computer vision library used for real-time video stream capture, image processing, and camera input handling.
  - [OpenCV Documentation](https://docs.opencv.org/)

- **sqlite-vec**: A lightweight vector search extension for SQLite, enabling fast vector storage and similarity search directly inside SQLite databases.
  - [sqlite-vec GitHub / Docs](https://github.com/asgregorio/sqlite-vec)

- **SQLite (`sqlite3`)**: C-language library that provides a lightweight, disk-based database for local structured data storage.
  - [Python sqlite3 Module Documentation](https://docs.python.org/3/library/sqlite3.html)

- **uv**: An extremely fast Python package and project manager written in Rust, used for managing environments and dependencies seamlessly.
  - [uv Documentation](https://docs.astral.sh/uv/)

## Authors

<td align="center">
  <a href="https://github.com/Abhijit-71">
    <img src="https://github.com/Abhijit-71.png" width="100px;" alt="Author Profile Photo"/><br />
    <sub><b>@Abhijit-71</b></sub>
  </a>
</td>



[![GitHub Profile](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Abhijit-71)


<td align="center">
  <a href="https://github.com/Nwjwrbrh">
    <img src="https://github.com/Nwjwrbrh.png" width="100px;" alt="Author Profile Photo"/><br />
    <sub><b>@Nwjwrbrh</b></sub>
  </a>
</td>

[![GitHub Profile](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Nwjwrbrh)
