Documentation – MistVision
Problem:
Driving in unfavorable weather conditions such as fog, when visibility is reduced and additional driver assistance is needed to maintain driving quality and safety.

Solution
Step 1

For the system to operate, it is necessary to detect the weather conditions in which the assistance should be activated. This is why the first stage involves classification. Using available vehicle cameras or additional sensor data, the system determines the current weather conditions.

This approach is chosen due to the lack of specialized sensors, or due to limited communication and data transmission capabilities in dense fog.
The classifier determines one of the following weather modes: fog, snow, rain, clear sky, or cloudy sky.
Based on the detected condition, the system receives a signal to activate and switches into object detection mode.

Step 2

The system’s specialization for foggy conditions is achieved by processing the image displayed to the user, providing improved road visibility. This functionality is implemented through real-time dashcam analysis using two stages: dehaze and detect.

During the first pass, a dehazing filter is applied. It processes the footage through several steps, removes noise, and prepares it for further analysis.
The result is improved contrast and clearer object boundaries, enhancing computer vision accuracy.

The filter is designed so that the resulting image remains natural and close to the original, but visually enhanced for optimal user experience.

Step 3

A key system component is the detection of low-visibility objects on the road.
The focus is on real-time detection. Besides marking object positions, the user also receives information about:

Object type

Approximate distance

Additionally, color-coded priority levels indicate the urgency of reaction, based on collected data.

Step 4

The entire architecture is integrated into an Android application with a user interface featuring distance-based color coding. Based on how close an object is (its size in the frame), the driver is visually warned about approaching vehicles.

Object markers are implemented as bounding boxes for improved visibility.
Object distance is estimated based on their relative size in the image.
There is also potential for future improvements, including motion prediction using additional vehicle metadata.

Technologies Used

OpenCV – used for visual data processing, efficient loading, manipulation, and real-time display. Also used in integration with YOLO models and the weather classifier.

Classifier (WIC) – a vision-language model trained for weather condition classification from images. It is based on deep neural networks that jointly process visual and textual data, enabling training on text-image pairs. The model is imported from Hugging Face and built on the SigLIP2 architecture.

Dehazing Filter – based on the numeric Dark Channel Prior method. It reconstructs the input image by removing artifacts and performs preprocessing aimed at improving detection accuracy.

YOLO11 Model – used for object detection and selected for clearly marking road participants in fog. Excellent for real-time tasks, and limitations caused by dense fog and low contrast are mitigated through preprocessing.

HuggingFace Transformers – enables the use of pretrained models for both visual and textual data tasks.

PyTorch – the main library used for training and running neural networks, enabling execution of pretrained models.

FFmpeg – used for multimedia manipulation. It allows format conversion, compression, and real-time file merging, making it ideal for handling vehicle camera footage.

Flask – backend service implemented as a REST API for receiving frames, processing them, and sending detected objects to the client app in real time.

Android Studio (Java) – used for creating the Android application and its UI. Java is used to implement the interface, visualize detected objects, and display warnings.
