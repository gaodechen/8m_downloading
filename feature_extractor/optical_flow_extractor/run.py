import numpy as np
import cv2 as cv
import time
import os


class OpticalFlowAnalyzer:
    def __init__(self, file_name):
        self.file_name = file_name


    def warp_flow(self, img, flow):
        h, w = flow.shape[:2]
        flow = -flow
        flow[:,:,0] += np.arange(w)
        flow[:,:,1] += np.arange(h)[:,np.newaxis]
        res = cv.remap(img, flow, None, cv.INTER_LINEAR)
        return res


    def analyze(self):
        use_spatial_propagation = False
        use_temporal_propagation = True
        inst = cv.DISOpticalFlow.create(cv.DISOPTICAL_FLOW_PRESET_MEDIUM)
        inst.setUseSpatialPropagation(use_spatial_propagation)

        img_list = os.listdir('./img')
        img_list.sort()
        num = len(img_list)
        img_list = ['./img/' + img_list[i] for i in range(0, num)]

        flow = None
        img = cv.imread(img_list[0])
        prevgray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        for i in range(1, num):
            img = cv.imread(img_list[i])
            gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
            if flow is not None and use_temporal_propagation:
                #warp previous flow to get an initial approximation for the current flow:
                flow = inst.calc(prevgray, gray, self.warp_flow(flow,flow))
            else:
                flow = inst.calc(prevgray, gray, None)
            prevgray = gray
            print(flow.shape)
