import sys
import os
import shutil
import torch
import time
import subprocess
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, utils
import numpy as np
from math import floor
import pandas as pd
import argparse
from PIL import Image

from video_processing import six_four_crop_video
from frame_loader import FrameLoader, return_start_and_end
from transition_network import TransitionCNN
from snippet import getSnippet
from utilities import normalize_frame, print_shape


def video2frames(file_path, img_folder):
    os.makedirs(img_folder, exist_ok=True)
    cmd = 'ffmpeg -i ' + file_path + ' -y -f image2 -r 2 ' + img_folder + '/img_%06d.jpg'
    FNULL = open(os.devnull, 'w')
    subprocess.Popen(cmd, stdout=FNULL, stderr=subprocess.STDOUT)


def img2log(img_folder, log_path):
    img_list = os.listdir(img_folder)
    img_list = [img_folder + i for i in img_list]
    open(log_path, 'w').write('\n'.join(img_list))


class ShotBoundaryExtractor:
    def __init__(self, src_folder, dst_folder, video_path, feature_path, filename, fps=15, auto_clean=True):
        self.model_path = './shot_boundary_extractor/model/shot_boundary_detector_model.pt'
        self.src_folder = src_folder
        self.dst_folder = dst_folder
        self.video_path = video_path
        self.feature_path = feature_path
        self.fps = fps
        self.auto_clean = auto_clean

        self.frame_buf_folder = './' + filename + '/'
        self.frame_list_path = './' + filename + '_log.txt'

    def clean(self):
        if os.path.exists(self.frame_list_path):
            os.remove(self.frame_list_path)
        if os.path.exists(self.frame_buf_folder):
            shutil.rmtree(self.frame_buf_folder)

    def get_shot_boundary(self):
        device = 'cuda'

        #load model
        model = TransitionCNN()
        model.load_state_dict(torch.load(self.model_path))
        model.to(device)

        output_path = self.dst_folder + self.feature_path
        pred_file = open(output_path, 'w+')

        frame_list = FrameLoader(self.frame_list_path,
                                 sample_size=100, overlap=9)
        frame_loader = DataLoader(frame_list, batch_size=1, num_workers=1)

        video_indexes = []
        vals = np.arange(frame_list.get_line_number())
        length = len(frame_list)

        for val in range(length):
            s, e = return_start_and_end(val)
            video_indexes.append(vals[s:e])

        for indx, batch in enumerate(frame_loader):
            batch.to(device)
            batch = batch.type('torch.cuda.FloatTensor')
            predictions = model(batch)
            predictions = predictions.argmax(dim=1).cpu().numpy()
            for idx, prediction_set in enumerate(predictions):
                for i, prediction in enumerate(prediction_set):
                    if prediction[0][0] == 0:
                        frame_index = video_indexes[indx][i+5]
                        pred_file.write(str(frame_index) + '\n')
        pred_file.close()

    def run(self):
        start_time = time.time()
        try:
            video2frames(self.src_folder + self.video_path, self.frame_buf_folder)
            img2log(self.frame_buf_folder, self.frame_list_path)
        except Exception as e:
            print(e)
            print(self.video_path + ' failed to extract frames')
            return
        try:
            self.get_shot_boundary()
        except Exception as e:
            print(e)
            print(self.video_path + ' failed to extract shot boundary')
            return
        if self.auto_clean:
            self.clean()
