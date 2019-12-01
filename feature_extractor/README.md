# Categories

1. **optical_flow_extractor**: DIS optical flow algorithm ([arXiv Link](https://arxiv.org/abs/1603.03590)) implemented using OpenCV lib.

2. **[video_feature_extractor](https://github.com/antoine77340/video_feature_extractor)**: implemented with 3D ResNet pretrained models

3. **audio_feature_extractor**: employed the powerful [librosa](http://librosa.github.io/) lib and speeded up with [joblib](https://github.com/joblib/joblib)

# Usage

`joblib` are employed in all extractors to speed up tasks by paralleling computing. Also, you could pause your task anytime as checkpoints are recorded.

- `process_audio.py`
- `process_video.py`

To adapt in your tasks, modify those as you need.

``` Python
csv_paths = ['audio_0']                 # list of csv files
csv_folder = './'                       # folder of csv files
src_folder = './video_samples/'         # folder storing files listed in csv
dst_folder = './output/audio_feature/'  # folder to save output featuers
ckpt_path = 'audio.ckpt'                # file to save the checkpoints
n_proc = 4                              # number of multi-processes in parallel
```

CSV format are shown below:

audio_path | feature path
-|-|
demo1.m4a | demo1.npz
demo2.webm | demo2.npz

# References

- Kroeger T , Timofte R , Dai D , et al. [Fast Optical Flow using Dense Inverse Search[J]. 2016.](https://arxiv.org/abs/1603.03590)
- [Video Feature Extractor](https://github.com/antoine77340/video_feature_extractor)
- [librosa](http://librosa.github.io/) 
- [joblib](https://github.com/joblib/joblib)
