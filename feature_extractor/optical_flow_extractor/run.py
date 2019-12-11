import numpy as np
import cv2 as cv
import time
import os
from video2img import video2frames


class OpticalFlowAnalyzer:
    def __init__(self, src_folder, dst_folder, video_path, feature_path, buf_name, fps=5):
        self.src_folder = src_folder
        self.dst_folder = dst_folder
        self.video_path = video_path
        self.feature_path = feature_path
        self.frame_buf_folder = './' + buf_name + '/'
        self.fps = fps

    def warp_flow(self, img, flow):
        h, w = flow.shape[:2]
        flow = -flow
        flow[:, :, 0] += np.arange(w)
        flow[:, :, 1] += np.arange(h)[:, np.newaxis]
        res = cv.remap(img, flow, None, cv.INTER_LINEAR)
        return res

    def analyze(self):
        use_spatial_propagation = False
        use_temporal_propagation = True
        inst = cv.DISOpticalFlow.create(cv.DISOPTICAL_FLOW_PRESET_MEDIUM)
        inst.setUseSpatialPropagation(use_spatial_propagation)

        try:
            video2frames(self.src_folder + self.video_path, self.frame_buf_folder, self.fps)
        except Exception as e:
            print(e)
            print(self.video_path + ' failed to extract frames')
            return;

        img_list = os.listdir(self.frame_buf_folder)
        img_list = [self.frame_buf_folder + i for i in img_list]
        num = len(img_list)

        flow = []
        current_flow = None
        try:
            img = cv.imread(img_list[0])
        except Exception as e:
            print(e)
            print(self.video_path + ' failed to read frames')
            return
        prevgray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        for i in range(1, num):
            img = cv.imread(img_list[i])
            gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
            if current_flow is not None and use_temporal_propagation:
                #warp previous flow to get an initial approximation for the current flow:
                current_flow = inst.calc(prevgray, gray, self.warp_flow(current_flow, current_flow))
            else:
                current_flow = inst.calc(prevgray, gray, None)
            prevgray = gray
            flow.append(current_flow)
        
        np.save(self.dst_folder + self.feature_path, np.array(flow))