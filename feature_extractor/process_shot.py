import os
import csv
import time
import sys
import numpy as np
from joblib import Parallel, delayed
from tqdm import tqdm

sys.path.append("./shot_boundary_extractor")

from shot_boundary_extractor.run import ShotBoundaryExtractor as SBE
from utils import save_ckpt, load_ckpt, check_path, read_ckpt

csv_paths = ['video_' + str(i) for i in range(0, 1)]
csv_folder = './'
src_folder = './video_samples/'
dst_folder = './output/shot_boundary/'
ckpt_folder = './ckpt/'
n_proc = 4


# process single file
def process(infile, outfile):
    filename = outfile.split('.')[0]
    sbe = SBE(src_folder, dst_folder, infile, filename + '.txt', filename)
    sbe.run()


def proc_func(csv_path):
    start_time = time.time()
    print(csv_path + ' has began ...')
    ckpt_path = ckpt_folder + csv_path + '.ckpt'
    check_path(ckpt_path, binary=True)
    ckpt_index = read_ckpt(ckpt_path)

    csv_file = csv.reader(open(csv_folder + csv_path + '.csv'))
    _ = next(csv_file)
    rows = [row for row in csv_file]
    print('start from checkpoint ' + str(ckpt_index + 1) + ' in ' + str(csv_path))

    for i in tqdm(range(ckpt_index + 1, len(rows))):
        process(rows[i][0], rows[i][1])
        save_ckpt(i, ckpt_path)
    print(csv_path + ' has been done in ' + str(time.time() - start_time))


if __name__ == "__main__":
    os.makedirs(dst_folder, exist_ok=True)
    os.makedirs(ckpt_folder, exist_ok=True)
    proc_func(csv_paths[0])

    # Parallel(n_jobs=n_proc, backend='multiprocessing')(
    #    delayed(proc_func)(csv_path) for csv_path in csv_paths)
