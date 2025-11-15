package com.mammoot.hakatonfront;

import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.view.View;

import java.util.ArrayList;
import java.util.List;

public class OverlayView extends View {

    private List<Detection> detections = new ArrayList<>();
    private Paint paint;

    public OverlayView(Context context) {
        super(context);
        init();
    }

    private void init() {
        paint = new Paint();
        paint.setColor(Color.RED);
        paint.setStyle(Paint.Style.STROKE);
        paint.setStrokeWidth(5f);
    }

    public void setDetections(List<Detection> detections) {
        this.detections = detections;
        invalidate();
    }

    @Override
    protected void onDraw(Canvas canvas) {
        super.onDraw(canvas);

        if (detections == null) return;

        for (Detection d : detections) {
            float left = (float) d.x;
            float top = (float) d.y;
            float right = left + (float) d.width;
            float bottom = top + (float) d.height;
            canvas.drawRect(left, top, right, bottom, paint);
        }
    }
}
