package com.mammoot.hakatonfront;

public class Timer extends Thread {
    private int currentTime;

    public Timer()
    {
        currentTime = 0;
    }

    public void run()
    {
        try{
            while(true)
            {
                Thread.sleep(10);
                synchronized(this)
                {
                    currentTime+=10;
                }
            }
        }
        catch(Exception e)
        {
        }

    }

    synchronized int getTime()
    {
        return currentTime;
    }


}
