import sys

import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, utils
import numpy as np
from snippet import getSnippet
from math import floor
from transition_network import TransitionCNN
from utilities import normalize_frame, print_shape
import pandas as pd
import os
import time
from TestVideo import TestVideo, return_start_and_end
from moviepy.editor import VideoFileClip
from video_processing import six_four_crop_video
from PIL import Image

# command line arguments --> file name, video_file_name, gpu or cpu

# first decompose the video to frames
# place the video to be detected into the directory


if __name__ == "__main__":
    start_time = time.time()

    video = sys.argv[1]
    pred_text_file_name = sys.argv[2]

    text_file = 'frames.txt'

    print('decomposing video to frames this may take a while  for large videos :) .....')
    frames_path = 'video_frames/'
    os.makedirs('video_frames/', exist_ok=True)
    os.makedirs('predictions/', exist_ok=True)

    vid = VideoFileClip(video)
    vid = six_four_crop_video(vid)

    frames = [frame for frame in vid.iter_frames()]

    f = open(text_file, 'w+')

    for j, frame in enumerate(frames):
            frame_path = frames_path + 'frame_' + str(j+1) + '.png'
            im = Image.fromarray(frame)
            im.save(frame_path)
            f.write(frame_path + '\n')

    print('frame decomposition complete !!! ')

    #load model
    model = TransitionCNN()
    model.load_state_dict(torch.load(
        './shot_boundary_detector_even_distrib.pt', map_location='cpu'))

    prediction_text_file = 'predictions/' + pred_text_file_name

    pred_file = open(prediction_text_file, 'w+')

    print('computing predictions for video', video, '...................')

    test_video = TestVideo('frames.txt', sample_size=100, overlap=9)
    test_loader = DataLoader(test_video, batch_size=1, num_workers=3)

    video_indexes = []
    vals = np.arange(test_video.get_line_number())
    length = len(test_video)

    for val in range(length):
        s, e = return_start_and_end(val)
        video_indexes.append(vals[s:e])

    for indx, batch in enumerate(test_loader):
            batch = batch.type('torch.FloatTensor')
            predictions = model(batch)
            predictions = predictions.argmax(dim=1).cpu().numpy()
            for idx, prediction_set in enumerate(predictions):
                for i, prediction in enumerate(prediction_set):
                    if prediction[0][0] == 0:
                        frame_index = video_indexes[indx][i+5]
                        pred_file.write(str(frame_index) + '\n')
    pred_file.close()

    print('Predictions complete ')
    print('Frames that are part of shot boundaries are listed in file the directory path predictions/' + pred_text_file_name)
    print(time.time() - start_time)
