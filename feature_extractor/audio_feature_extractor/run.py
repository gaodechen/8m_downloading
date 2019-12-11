import librosa
import time
import numpy as np
import os
import matplotlib.pyplot as plt
from joblib import Parallel, delayed


class AudioAnalyzer:
    def __init__(self, filepath, sr=22050, offset=0.0, hop_length=512):
        self.hop_length = hop_length
        self.filepath = filepath
        self.filename = os.path.basename(
            os.path.normpath(filepath)).split(".")[0]

        self.y, self.sr = librosa.load(path=filepath, sr=sr, offset=offset)
        self.frames = self.duration_to_frame()

        self.timbre_features = []
        self.melody_features = []
        self.energy_features = []
        self.rhythm_features = []
        self.features = None

    ''' Timbre Space
    1. MFCC & MFCC delta
    2. spectral flux
    3. zero crossing rate
    4. rolloff
    5. spectral contrast
    6. spectral centroid
    '''

    def extract_timbre_features(self):
        mfcc = librosa.feature.mfcc(
            y=self.y, sr=self.sr, hop_length=self.hop_length, n_mfcc=13)
        # spectral flux computation
        mfcc_delta = librosa.feature.delta(mfcc)
        _spectral_flux = librosa.onset.onset_strength(y=self.y, sr=self.sr)
        spectral_flux = _spectral_flux / _spectral_flux.max()
        zero_crossing_rate = librosa.feature.zero_crossing_rate(y=self.y)
        rolloff = librosa.feature.spectral_rolloff(
            y=self.y, sr=self.sr, roll_percent=0.85)
        spectral_contrast = librosa.feature.spectral_contrast(
            y=self.y, sr=self.sr)
        spectral_centroid = librosa.feature.spectral_centroid(
            y=self.y, sr=self.sr)

        self.timbre_features = np.vstack(
            [mfcc, mfcc_delta, spectral_flux, zero_crossing_rate, rolloff, spectral_contrast, spectral_centroid])
        return self.timbre_features

    ''' Melody Space
    1. chromagram
    2. tonnets
    '''

    def extract_melody_features(self):
        chromagram = librosa.feature.chroma_cqt(
            y=self.y, sr=self.sr, hop_length=self.hop_length, bins_per_octave=12 * 3)
        tonnets = librosa.feature.tonnetz(y=self.y, sr=self.sr)
        self.melody_features = np.vstack([chromagram, tonnets])
        return self.melody_features

    ''' Energy Space
    1. rms
    2. loudness
    '''

    def extract_energy_features(self):
        y_stft = librosa.stft(y=self.y, hop_length=self.hop_length)
        S, _phase = librosa.magphase(y_stft)
        rms = librosa.feature.rms(S=S).flatten()
        # loudness computation
        power = np.abs(S)**2
        p_mean = np.sum(power, axis=0, keepdims=True)
        p_ref = np.max(power)
        loudness = librosa.power_to_db(p_mean, ref=p_ref)
        self.energy_features = np.vstack([rms, loudness])
        return self.energy_features

    ''' Rhythm Space
    1. onset
    2. dynamic_tempo
    3. tempogram
    '''

    def extract_rhythm_features(self):
        onset = librosa.onset.onset_strength(
            y=self.y, sr=self.sr, hop_length=self.hop_length)
        tempogram = librosa.feature.tempogram(
            onset_envelope=onset, sr=self.sr, hop_length=self.hop_length, win_length=5)
        dynamic_tempo = librosa.beat.tempo(
            onset_envelope=onset, sr=self.sr, aggregate=None)
        self.rhythm_features = np.vstack([dynamic_tempo, tempogram])
        return self.rhythm_features

    ''' get the frame for every sec_inc seconds
    '''

    def duration_to_frame(self, sec_inc=0.5):
        # duration in seconds
        duration = librosa.get_duration(
            y=self.y, sr=self.sr, hop_length=self.hop_length)
        time_stamp = sec_inc
        time = []
        while time_stamp <= duration:
            time.append(time_stamp)
            time_stamp += sec_inc
        return librosa.time_to_frames(time, hop_length=self.hop_length, sr=self.sr)

    ''' sync all the frames based on duration_to_frame
    '''

    def sync_frames(self, features, aggregate=np.mean):
        sync_feature = librosa.util.sync(
            features, self.frames, aggregate=aggregate)
        return sync_feature

    def proc_func(self, type):
        if type == 0:
            self.extract_energy_features()
        elif type == 1:
            self.extract_melody_features()
        elif type == 2:
            self.extract_rhythm_features()
        elif type == 3:
            self.extract_timbre_features()

    def compute_features(self):
        Parallel(n_jobs=4, backend='threading')(
            delayed(self.proc_func)(i) for i in range(0, 4))

    def analyze(self):
        if(self.features is None):
            self.compute_features()
        sync_features = np.vstack(
            [self.timbre_features, self.melody_features, self.energy_features])
        self.features = np.vstack([self.sync_frames(
            sync_features), self.sync_frames(sync_features, aggregate=np.std)])
        return {'general': self.features, 'rhythm': self.rhythm_features}
