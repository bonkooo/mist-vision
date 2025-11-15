package com.mammoot.hakatonfront;

public class Detection {
    public String clazz;      // use clazz because "class" is a reserved word
    public double confidence;
    public double height;
    public double width;
    public double x;
    public double y;

    public Detection(String car, double v, int i, int i1, int i2, int i3) {
        clazz = car;
        confidence = v;
        height = i;
        width = i1;
        x = i2;
        y = i3;
    }
    public Detection()
    {

    }
}