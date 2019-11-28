import time
import numpy as np
import librosa
from joblib import Parallel, delayed


def get_mfcc_in_loop(audio, sr, sample_len):
        # We split long array into small ones of lenth sample_len
        y_windowed = np.array_split(audio, np.arange(
            sample_len, len(audio), sample_len))
        for sample in y_windowed:
            mfcc = librosa.feature.mfcc(y=sample, sr=sr)


if __name__ == "__main__":

    n_proc = 4

    y, sr = librosa.load(librosa.util.example_audio_file(),
                         duration=60)  # load audio sample
    # repeat signal so that we can get more reliable measurements
    y = np.repeat(y, 10)
    # We will compute MFCC for short pieces of audio
    sample_len = int(sr * 0.2)

    start = time.time()
    y_windowed = np.array_split(y, np.arange(sample_len, len(y), sample_len))
    Parallel(n_jobs=n_proc, backend='multiprocessing')(delayed(get_mfcc_in_loop)(
        audio=data, sr=sr, sample_len=sample_len) for data in y_windowed)
    print('Time multiprocessing with joblib (many small tasks):', time.time() - start)
