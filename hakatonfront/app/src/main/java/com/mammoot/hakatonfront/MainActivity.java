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

import java.util.Map;

public class MainActivity extends AppCompatActivity {

    private VideoView videoView;
    private ImageView weatherIcon;
    private ImageView dangerIcon;

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

        videoView = findViewById(R.id.mainVideoView);

        // Setup media controller
        MediaController mediaController = new MediaController(this);
        mediaController.setAnchorView(videoView);
        videoView.setMediaController(mediaController);

        // Set video from raw resources
        String uriPath = "android.resource://" + getPackageName() + "/" + R.raw.testvideo;

        Uri uri = Uri.parse(uriPath);
        videoView.setVideoURI(uri);
        videoView.start();
        videoView.setBackgroundColor(Color.TRANSPARENT);

        // Weather icon
        weatherIcon = findViewById(R.id.weatherIcon);
        dangerIcon = findViewById(R.id.dangerIcon);

        // ovo je hardcodovano za sad
        setWeatherIcon("fog");
        Log.d("MainActivity", "Ja sam Djole 2");
        for(int i = 0; i < 10; i++) {
            ApiClient.processImage(i, new ApiClient.Callback() {
                @Override
                public void onSuccess(Map<String, Object> json) {
                    Log.d("MainActivity", "Response: " + json.toString());
                }

                @Override
                public void onError(String error) {
                    Log.e("MainActivity", "Error: " + error);
                }
            });
        }
        setDanger(true);
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
            case "foggy/hazy": // default magla
            default:
                weatherIcon.setImageResource(R.drawable.fog);
                break;
        }
    }

    public void setDanger(boolean isDanger) {
        if (isDanger) {
            dangerIcon.setVisibility(ImageView.VISIBLE);
        } else {
            dangerIcon.setVisibility(ImageView.GONE);
        }
    }
}



