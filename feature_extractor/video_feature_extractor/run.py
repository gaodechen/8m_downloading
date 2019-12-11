import torch as th
import math
import numpy as np
from video_loader import VideoLoader
from torch.utils.data import DataLoader
import argparse
from model import get_model
from preprocessing import Preprocessing
from random_sequence_shuffler import RandomSequenceSampler
import torch.nn.functional as F
import time


# csv_paths = ['video_' + str(i) + '.csv' for i in range(0, 6)]
csv_paths = ['list.csv']
csv_folder = './'
src_folder = './'
dst_folder = '../output/video_feature/'
num_thread = 16

model_path = './model/resnext101.pth'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Video Feature Extractor')

    parser.add_argument('--batch_size', type=int, default=64,
                        help='batch size')
    parser.add_argument('--type', type=str, default='3d',
                        help='CNN type')
    parser.add_argument('--half_precision', type=int, default=1,
                        help='output half precision float')
    parser.add_argument('--num_decoding_thread', type=int, default=num_thread,
                        help='Num parallel thread for video decoding')
    parser.add_argument('--l2_normalize', type=int, default=1,
                        help='l2 normalize feature')
    parser.add_argument('--resnext101_model_path', type=str, default='./model/resnext101.pth',
                        help='Resnext model path')
    args = parser.parse_args()

    for csv_path in csv_paths:

        print(csv_path + ' began ...')
        start_time = time.time();

        dataset = VideoLoader(
            csv=csv_path,
            src_folder=src_folder,
            dst_folder=dst_folder,
            framerate=1 if args.type == '2d' else 24,
            size=224 if args.type == '2d' else 112,
            centercrop=(args.type == '3d'),
        )
        n_dataset = len(dataset)
        sampler = RandomSequenceSampler(n_dataset, 10)
        loader = DataLoader(
            dataset,
            batch_size=1,
            shuffle=False,
            num_workers=args.num_decoding_thread,
            sampler=sampler if n_dataset > 10 else None,
            pin_memory=True
        )
        preprocess = Preprocessing(args.type)
        model = get_model(args)

        with th.no_grad():
            for k, data in enumerate(loader):
                input_file = data['input'][0]
                output_file = data['output'][0]
                if len(data['video'].shape) > 3:
                    print('Computing features of video {}/{}: {}'.format(
                        k + 1, n_dataset, input_file))
                    video = data['video'].squeeze()
                    if len(video.shape) == 4:
                        video = preprocess(video)
                        n_chunk = len(video)
                        features = th.cuda.FloatTensor(n_chunk, 2048).fill_(0)
                        n_iter = int(math.ceil(n_chunk / float(args.batch_size)))
                        for i in range(n_iter):
                            min_ind = i * args.batch_size
                            max_ind = (i + 1) * args.batch_size
                            video_batch = video[min_ind:max_ind].cuda()
                            batch_features = model(video_batch)
                            if args.l2_normalize:
                                batch_features = F.normalize(batch_features, dim=1)
                            features[min_ind:max_ind] = batch_features
                        features = features.cpu().numpy()
                        if args.half_precision:
                            features = features.astype('float16')
                        np.save(output_file, features)
                else:
                    print('Video {} already processed.'.format(input_file))
        print(csv_path + ' has been finished within ' + str(time.time()-start_time))
