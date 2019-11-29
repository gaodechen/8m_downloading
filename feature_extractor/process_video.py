import os
import csv
import time
import numpy as np
from joblib import Parallel, delayed

from optical_flow_extractor.run import OpticalFlowAnalyzer
from video2img import video2frames

def proc_func(item):
    file_name = item.split('.')[0][:-3]
    audio_analyzer = AudioAnalyzer(src_folder + item)
    audio_analyzer.compute_features()
    feature = audio_analyzer.analyze()
    np.save(dst_folder + file_name + '.npy', feature)

if __name__ == "__main__":

    src_folder = './video_samples/'
    dst_folder = './output/'
    n_proc = 4

    file_list = os.listdir(src_folder)

    start_time = time.time()

    Parallel(n_jobs=n_proc, backend='multiprocessing')(delayed(proc_func)(item) for item in file_list)

    for item in file_list:
        video2frames()
        optical_flow_analyzer = OpticalFlowAnalyzer(src_folder + item)

    end_time = time.time()
    print(end_time - start_time)