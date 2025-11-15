package com.mammoot.hakatonfront;

import android.util.Log;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

public class ProcessingThread extends Thread{
    MainActivity mainActivity;
    public ProcessingThread(MainActivity mainActivity){
        this.mainActivity = mainActivity;
    }
    public void run()
    {
        int NUM_FRAMES = 818;
        int DURATION =34; //mainActivity.videoView.getDuration();
        try {
            Log.d("MyTag", "Playing");
            while (mainActivity.timer.getTime() <= DURATION*1000) {

                Log.d("My Tag", Integer.toString(mainActivity.timer.getTime()));
                float passedVideoPercent = (float) mainActivity.timer.getTime() / 1000 / DURATION;
                int currFrame = NUM_FRAMES * (int) Math.ceil(passedVideoPercent);
                Map<String, Object> json = ApiClient.processImageSync(1);

                Log.d("MainActivity", "API Response: " + json.toString());

                // Parse detections
                if (json.containsKey("detections")) {
                    List<Map<String, Object>> detectionsList = (List<Map<String, Object>>) json.get("detections");
                    List<Detection> detectionObjects = new ArrayList<>();

                    for (Map<String, Object> d : detectionsList) {
                        Detection detection = new Detection();
                        detection.clazz = (String) d.get("class");
                        detection.confidence = ((Number) d.get("confidence")).doubleValue();
                        detection.height = ((Number) d.get("height")).doubleValue();
                        detection.width = ((Number) d.get("width")).doubleValue();
                        detection.x = ((Number) d.get("x")).doubleValue();
                        detection.y = ((Number) d.get("y")).doubleValue();
                        detectionObjects.add(detection);
                    }

                    // Update UI on main thread
                    mainActivity.runOnUiThread(() -> {
                        if (mainActivity.overlayView != null) {
                            mainActivity.overlayView.setDetections(detectionObjects);
                        }
                    });
                }

            }
        }
        catch (Exception e)
        {
            Log.d("MyTag", e.getMessage());
        }

    }
}
