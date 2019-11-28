import os
import csv
import time
import numpy as np
from joblib import Parallel, delayed

from audio_feature_extractor.run import AudioAnalyzer
from optical_flow_extractor.run import OpticalFlowAnalyzer
from video2img import video2frames

src_folder = './video_samples/'
dst_folder = './output/'

file_list = os.listdir(src_folder)

audio_format = ['249', '250', '251', '140', '139']
video_format = ['133', '242', '160', '278', '134', '394']

start_time = time.time()

for item in file_list:
    file_name = item.split('.')[0][:-3]
    file_format = item.split('.')[0][-3:]
    if file_format in audio_format:
        audio_analyzer = AudioAnalyzer(src_folder + item)
        audio_analyzer.compute_features()
        feature = audio_analyzer.analyze()
        np.save(dst_folder + file_name + '.npy', feature)
    else:
        video2frames()
        optical_flow_analyzer = OpticalFlowAnalyzer(src_folder + item)

end_time = time.time()
print(end_time - start_time)