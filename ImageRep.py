
# coding: utf-8

# In[1]:

import sys
import cv2 as cv
import numpy as np
sys.path.append('./Rect.py')
from Rect import Rect

kNumBins = 16;
class ImageRep:
    def __init__(self, image, computeIntegral, computeIntegralHist, colour):
        self.m_channels = 3 if colour else 1
        self.m_rect = Rect(0, 0, image.shape[1], image.shape[0])
        self.m_images, self.m_integralImages, self.m_integralHistImages = [],[],[]
        
        for i in range(self.m_channels):
            # self.m_images.append(cv.createMat(image.shape[0], image.shape[1], cv.CV_8UC1))
            self.m_images.append(np.zeros((image.shape[0], image.shape[1]), np.uint8))
            if computeIntegral:
                # self.m_integralImages.append(cv.createMat(image.shape[0]+1, image.shape[1]+1, cv.CV_32SC1))
                self.m_integralImages.append(np.zeros((image.shape[0]+1, image.shape[1]+1), np.float32))
            if computeIntegralHist:
                for j in range(kNumBins):
                    # self.m_integralHistImages.append(cv.createMat(image.shape[0]+1, image.shape[1]+1, cv.CV_32SC1))
                    self.m_integralHistImages.append(np.zeros((image.shape[0]+1, image.shape[1]+1), np.float32))
                            
        channels = image.shape[2]
        if colour:
            # assert(image.channels() == 3)
            assert(channels == 3)
            b, g, r = cv.split(image)
            self.m_images = [b, g, r]
        else:
            #assert(image.channels() == 3 or image.channels() == 1)
            assert(channels == 3 or channels == 1)
            if channels == 3:
                self.m_images[0] = cv.cvtColor(image, cv.COLOR_RGB2GRAY)
            elif channels() == 1:
                np.copyto(self.m_images[0], image)
        
        if computeIntegral:
            for i in range(self.m_channels):
                self.m_images[i] = cv.equalizeHist(self.m_images[i])
                self.m_integralImages[i] = cv.integral(self.m_images[i])
        
        if computeIntegralHist:
            # tmp = cv.createMat(image.shape[0], image.shape[1], cv.CV_8UC1)
            # tmp[:] = 0
            tmp = np.zeros((image.shape[0], image.shape[1]), np.uint8)
            for j in range(kNumBins):
                for y in range(image.shape[0]):
                    for x in range(image.shape[1]):
                        sbin = int(float(self.m_images[0][y][x])/256.0*kNumBins)
                        tmp[y][x] = 1 if sbin == j else 0
                self.m_integralImages[j] = cv.integral(tmp)
   
    
    def Sum(self, rRect, channel=0):
        assert(rRect.XMin()>=0 and rRect.YMin()>=0 and                rRect.XMax()<=self.m_images[0].shape[1] and rRect.YMax()<=self.m_images[0].shape[0])
        return self.m_integralImages[channel][rRect.YMin()][rRect.XMin()] +                 self.m_integralImages[channel][rRect.YMax()][rRect.XMax()] -                 self.m_integralImages[channel][rRect.YMax()][rRect.XMin()] -                 self.m_integralImages[channel][rRect.YMin()][rRect.XMax()]
    
    def Hist(self, rRect, h):
        assert(rRect.XMin()>=0 and rRect.YMin()>=0 and                 rRect.XMax()<=self.m_images[0].shape[1] and rRect.YMax()<=slef.m_images[0].shape[0])
        norm = rRect.Area();
        for i in range(kNumBins):
            total = self.m_integralHistImages[i][rRect.YMin()][rRect.XMin()] +                     self.m_integralHistImages[i][rRect.YMax()][rRect.XMax()] -                     self.m_integralHistImages[i][rRect.YMax()][rRect.XMin()] -                     self.m_integralHistImages[i][rRect.YMin()][rRect.XMax()]
            h[i] = float(total)/norm;
    
    def GetImage(self, channel=0):
        return self.m_images[channel]
    def GetRect(self):
        return self.m_rect;

