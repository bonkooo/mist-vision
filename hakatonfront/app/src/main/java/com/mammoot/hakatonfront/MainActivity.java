package com.mammoot.hakatonfront;

import android.graphics.Color;
import android.net.Uri;
import android.os.Bundle;
import android.util.Log;
import android.widget.ImageView;
import android.widget.MediaController;
import android.widget.VideoView;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;
import androidx.activity.EdgeToEdge;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

public class MainActivity extends AppCompatActivity {

    VideoView videoView;
    Timer timer;
    OverlayView overlayView;
    private ImageView weatherIcon;
    private ImageView dangerIcon;

    private static final String TAG = "MainActivity";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_main);

        // Adjust padding for system bars
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.mainVideoView), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });

        // Initialize views
        videoView = findViewById(R.id.mainVideoView);
        overlayView = new OverlayView(this); // temporary; we will add to layout manually
        weatherIcon = findViewById(R.id.weatherIcon);
        dangerIcon = findViewById(R.id.dangerIcon);

        // Setup MediaController
        MediaController mediaController = new MediaController(this);
        mediaController.setAnchorView(videoView);
        videoView.setMediaController(mediaController);

        // Play video from raw resources
        timer = new Timer();
        String uriPath = "android.resource://" + getPackageName() + "/" + R.raw.testvideo;
        Uri uri = Uri.parse(uriPath);
        videoView.setVideoURI(uri);
        videoView.start();
        timer.start();
        videoView.setBackgroundColor(Color.TRANSPARENT);

        // Set initial weather icon
        setWeatherIcon("fog");

        // Show danger icon
        setDanger(true);

        // Add OverlayView on top of VideoView
        ((android.widget.FrameLayout) findViewById(R.id.mainVideoView).getParent()).addView(overlayView);

        // Simulate detections
        //simulateDetections();
        ProcessingThread processingThread = new ProcessingThread(this);
        processingThread.start();
        Log.d("MyTag", "Playing");
    }

    private void setWeatherIcon(String weather) {
        switch (weather) {
            case "rain/storm":
                weatherIcon.setImageResource(R.drawable.storm);
                break;
            case "snow/frosty":
                weatherIcon.setImageResource(R.drawable.snow);
                break;
            case "sun/clear":
                weatherIcon.setImageResource(R.drawable.sunny);
                break;
            case "cloudy/overcast":
                weatherIcon.setImageResource(R.drawable.cloudy);
                break;
            case "foggy/hazy":
            default:
                weatherIcon.setImageResource(R.drawable.fog);
                break;
        }
    }

    public void setDanger(boolean isDanger) {
        dangerIcon.setVisibility(isDanger ? ImageView.VISIBLE : ImageView.GONE);
    }

    // Simulated detection for demo purposes
    private void simulateDetections() {
        new Thread(() -> {
            try {
                for (int i = 0; i < 20; i++) {
                    List<Detection> detections = new ArrayList<>();
                    detections.add(new Detection("car", 0.9, 100 + i*5, 150, 120, 60));
                    detections.add(new Detection("person", 0.8, 300, 200 + i*3, 50, 100));

                    runOnUiThread(() -> overlayView.setDetections(detections));

                    Thread.sleep(500); // refresh every 0.5s
                }
            } catch (InterruptedException e) {
                Log.e(TAG, "Simulation interrupted", e);
            }
        }).start();
    }
}
