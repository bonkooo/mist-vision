import PIL.Image as Image
import skimage.io as io
import numpy as np
import time
from gf import guided_filter, guided_filter_new
import matplotlib.pyplot as plt
from scipy.ndimage import minimum_filter, uniform_filter
import cv2

class HazeRemoval(object):
    def __init__(self, omega=0.95, t0=0.1, radius=7, r=20, eps=0.001):
        self.eps = eps
        pass

    def open_image(self, img_path):
        img = Image.open(img_path).convert("RGB")
        self.src = np.array(img).astype(np.double)/255.
        # self.gray = np.array(img.convert('L'))
        self.rows, self.cols, _ = self.src.shape
        self.dark = np.zeros((self.rows, self.cols), dtype=np.double)
        self.Alight = np.zeros((3), dtype=np.double)
        self.tran = np.zeros((self.rows, self.cols), dtype=np.double)
        self.dst = np.zeros_like(self.src, dtype=np.double)
    def set_image(self, img):
        self.src = np.array(img).astype(np.double)/255.
        # self.gray = np.array(img.convert('L'))
        self.rows, self.cols, _ = self.src.shape
        self.dark = np.zeros((self.rows, self.cols), dtype=np.double)
        self.Alight = np.zeros((3), dtype=np.double)
        self.tran = np.zeros((self.rows, self.cols), dtype=np.double)
        self.dst = np.zeros_like(self.src, dtype=np.double)     

    def get_dark_channel(self, radius=7):
        print("Starting to compute dark channel prior...")
        start = time.time()
        tmp = self.src.min(axis=2)
        for i in range(self.rows):
            for j in range(self.cols):
                rmin = max(0,i-radius)
                rmax = min(i+radius,self.rows-1)
                cmin = max(0,j-radius)
                cmax = min(j+radius,self.cols-1)
                self.dark[i,j] = tmp[rmin:rmax+1,cmin:cmax+1].min()
        print("time:",time.time()-start)

    def get_dark_channel_fast(self, radius=7):
        """
        Compute dark channel prior in a fully vectorized way using a minimum filter.
        """
        print("Starting to compute dark channel prior...")
        start = time.time()

        # Per-pixel minimum over color channels -> 2D
        tmp = self.src.min(axis=2)

        # Apply local minimum filter with window size (2*radius+1)
        self.dark = minimum_filter(tmp, size=2*radius+1, mode='nearest')

        print("time:", time.time() - start)

    def get_air_light(self):
        print("Starting to compute air light prior...")
        start = time.time()
        flat = self.dark.flatten()
        flat.sort()
        num = int(self.rows*self.cols*0.001)
        threshold = flat[-num]
        tmp = self.src[self.dark>=threshold]
        tmp.sort(axis=0)
        self.Alight = tmp[-num:,:].mean(axis=0)
        # print(self.Alight)
        print("time:",time.time()-start)

    def get_transmission(self, radius=7, omega=0.95):
        print("Starting to compute transmission...")
        start = time.time()
        for i in range(self.rows):
            for j in range(self.cols):
                rmin = max(0,i-radius)
                rmax = min(i+radius,self.rows-1)
                cmin = max(0,j-radius)
                cmax = min(j+radius,self.cols-1)
                pixel = (self.src[rmin:rmax+1,cmin:cmax+1]/self.Alight).min()
                self.tran[i,j] = 1. - omega * pixel
        print("time:",time.time()-start)

    def compute_tran(self, radius=7, omega=0.95):
    # local minimum in a (2*radius+1) window
        print("Starting to compute transmission...")
        start = time.time()
        # Compute per-pixel minimum across channels (2D)
        dark_channel = self.src.min(axis=2)

        # Apply local minimum filter
        local_min = minimum_filter(dark_channel, size=2*radius+1, mode='nearest')

        # Transmission map
        self.tran = 1.0 - omega * local_min
        print("time:",time.time()-start)

    def guided_filter(self, r=60):
        print("Starting to compute guided filter trainsmission...")
        start = time.time()
        self.gtran = guided_filter_new(self.src, self.tran, r, self.eps)
        print("time:",time.time()-start)


    def recover(self, t0=0.1):
        print("Starting recovering...")
        start = time.time()
        self.gtran[self.gtran<t0] = t0
        t = self.gtran.reshape(*self.gtran.shape,1).repeat(3,axis=2)
        # import ipdb; ipdb.set_trace()
        self.dst = (self.src.astype(np.double) - self.Alight)/t + self.Alight
        self.dst *= 255
        self.dst[self.dst>255] = 255
        self.dst[self.dst<0] = 0
        self.dst = self.dst.astype(np.uint8)
        print("time:",time.time()-start)

    def new_recover(self, t0=0.1):
        """
        Recover haze-free image from source, transmission map, and airlight
        """
        print("Starting recovering...")
        start = time.time()

        # Ensure t has a minimum value
        gtran = np.maximum(self.gtran, t0)  # shape: (H, W) or (H, W, 1) or (H, W, 3)

        # Broadcast gtran to match src shape
        if gtran.ndim == 2:  # grayscale transmission
            t = np.repeat(gtran[:, :, np.newaxis], 3, axis=2)
        elif gtran.shape[2] == 1:  # single-channel transmission
            t = np.repeat(gtran, 3, axis=2)
        else:  # multi-channel transmission matches src already
            t = gtran

        # Recover the haze-free image
        self.dst = (self.src.astype(np.float64) - self.Alight) / t + self.Alight

        # Clip and scale to 0-255
        self.dst = np.clip(self.dst * 255, 0, 255).astype(np.uint8)

        print("time:", time.time() - start)
    def show(self):
        cv2.imwrite("img/src.jpg", (self.src*255).astype(np.uint8)[:,:,(2,1,0)])
        cv2.imwrite("img/dark.jpg", (self.dark*255).astype(np.uint8))
        cv2.imwrite("img/tran.jpg", (self.tran*255).astype(np.uint8))
        cv2.imwrite("img/gtran.jpg", (self.gtran*255).astype(np.uint8))
        cv2.imwrite("img/dst.jpg", self.dst[:,:,(2,1,0)])
        
        io.imsave("test.jpg", self.dst)


def remove_fog(image):
    hr = HazeRemoval()
    hr.set_image(image)
    hr.get_dark_channel_fast()
    hr.get_air_light()
    #hr.get_transmission()
    hr.compute_tran()
    hr.guided_filter()
    hr.new_recover()
    hr.show()
    return hr.dst

if __name__ == '__main__':
    import sys
    hr = HazeRemoval()
    hr.open_image(sys.argv[1])
    hr.get_dark_channel_fast()
    hr.get_air_light()
    #hr.get_transmission()
    hr.compute_tran()
    hr.guided_filter()
    hr.new_recover()
    hr.show()


    