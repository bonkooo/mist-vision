package com.mammoot.hakatonfront;

import android.net.Uri;
import android.os.Bundle;
import android.widget.ImageView;
import android.widget.MediaController;
import android.widget.VideoView;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;
import androidx.activity.EdgeToEdge;

public class MainActivity extends AppCompatActivity {

    private VideoView videoView;
    private ImageView weatherIcon;

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

        // Weather icon
        weatherIcon = findViewById(R.id.weatherIcon);

        // ovo je hardcodovano za sad
        setWeatherIcon("fog");
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
}
