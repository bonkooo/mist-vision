package com.mammoot.hakatonfront;

import android.os.AsyncTask;
import android.util.Log;

import com.google.gson.Gson;

import java.io.IOException;
import java.util.Map;
import java.util.concurrent.TimeUnit;

import okhttp3.ConnectionPool;
import okhttp3.FormBody;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;



public class ApiClient {

    private static final String TAG = "ApiClient";
    private static final String BASE_URL = "http://10.0.2.2:5000"; // replace with your server

    public interface Callback {
        void onSuccess(Map<String, Object> json);
        void onError(String error);
    }

    public static void processImage(int imageId, Callback callback) {
        new AsyncTask<Integer, Void, Map<String, Object>>() {
            String error = null;

            @Override
            protected Map<String, Object> doInBackground(Integer... params) {
                OkHttpClient client = new OkHttpClient();
                RequestBody formBody = new FormBody.Builder()
                        .add("image", String.valueOf(params[0]))
                        .build();

                Request request = new Request.Builder()
                        .url(BASE_URL + "/process")
                        .post(formBody)
                        .build();

                try (Response response = client.newCall(request).execute()) {
                    if (!response.isSuccessful()) {
                        error = "Unexpected code: " + response;
                        return null;
                    }

                    String jsonString = response.body().string();
                    Gson gson = new Gson();
                    return gson.fromJson(jsonString, Map.class);

                } catch (IOException e) {
                    error = e.getMessage();
                    return null;
                }
            }

            @Override
            protected void onPostExecute(Map<String, Object> result) {
                if (error != null) {
                    callback.onError(error);
                } else {
                    callback.onSuccess(result);
                }
            }
        }.execute(imageId);
    }

    public static Map<String, Object> processImageSync(int imageId) throws IOException {
        OkHttpClient client = new OkHttpClient.Builder()
                .connectionPool(new ConnectionPool(0, 1, TimeUnit.SECONDS)) // no reuse
                .retryOnConnectionFailure(true)
                .build();
        RequestBody formBody = new FormBody.Builder()
                .add("image", String.valueOf(imageId))
                .build();

        Request request = new Request.Builder()
                .url(BASE_URL + "/process")
                .post(formBody)
                .build();

        try (Response response = client.newCall(request).execute()) {
            if (!response.isSuccessful()) throw new IOException("Unexpected code: " + response);
            String jsonString = response.body().string();
            Gson gson = new Gson();
            return gson.fromJson(jsonString, Map.class);
        }
    }
}
