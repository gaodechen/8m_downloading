import os
import csv
import time
import numpy as np
from joblib import Parallel, delayed
from tqdm import tqdm

from optical_flow_extractor.video2img import video2frames
from optical_flow_extractor.run import OpticalFlowAnalyzer
from utils import save_ckpt, load_ckpt, check_path

csv_paths = ['video_0']
csv_folder = './'
src_folder = './video_samples/'
img_folder = './output/video_images/'
dst_folder = './output/optical_feature/'
ckpt_path = 'video.ckpt'
n_proc = 4


def proc_func(infile, outfile, csv_path, csv_index):
    img_path = img_folder + infile.split('.')[0] + '/'
    video2frames(src_folder + infile, img_path)
    feature = OpticalFlowAnalyzer(img_path).analyze()
    np.savez(dst_folder + outfile, feature)

    [csv_old, index_old] = load_ckpt(ckpt_path).split('#')
    ckpt_index = str(max(csv_index, int(index_old))
                     if csv_path is csv_old else csv_index)
    ckpt_info = csv_path + '#' + ckpt_index
    save_ckpt(ckpt_info, ckpt_path)


if __name__ == "__main__":
    check_path(ckpt_path, binary=True)

    ckpt_info = load_ckpt(ckpt_path)
    if ckpt_info is None or '#' not in ckpt_info:
        ckpt_chunk = csv_paths[0]
        ckpt_index = -1
        save_ckpt(ckpt_chunk + '#' + str(ckpt_index), ckpt_path)
    else:
        ckpt_chunk = ckpt_info.split('#')[0]
        ckpt_index = int(ckpt_info.split('#')[1])

    print('continue from checkpoint ' + ckpt_chunk + ' ' + str(ckpt_index))

    for csv_path in csv_paths:
        print(csv_path + ' has began ...')
        csv_file = csv.reader(open(csv_folder + csv_path + '.csv'))
        _ = next(csv_file)
        rows = [row for row in csv_file]
        start_time = time.time()
        Parallel(n_jobs=n_proc, backend='multiprocessing')(delayed(proc_func)(
            rows[i][0], rows[i][1], csv_path, i) for i in tqdm(range(ckpt_index + 1, len(rows))))

        print(csv_path + ' has been done in ' + str(time.time() - start_time))
