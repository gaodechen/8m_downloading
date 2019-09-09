## Usage 

Here are some script interface for [GANSynth](https://github.com/tensorflow/magenta/tree/master/magenta/models/gansynth) using pitches estimation results as input, and some samples generated for test.

Estimation results are computed by [CREPE](https://github.com/marl/crepe) library, which is a file containing three labels `[time, frequency, confidence]` in csv format.

Here we process those labels first with `csv2notes.py`, in order to feed into generator later.

As a interface for GANSynth, you could simply apply:

```
$ python csv_tester.py --ckpt_dir=./all_instruments --output_dir=./output --csv_file=[csv_path] --secs_per_instrument=[x]
```

`--csv_file=[csv_path]` indicates csv output.

Don't forget to replace `--secs_per_instruments=[x]` with a suitable time stride or just go without this parameter.

## Categories

```
    input
        test.csv        ...     pitch estimation output
        test.wav        ...     wav used for estimation
        test.mid        ...     midi file for interpolation
        test_2.mid      ...     midi file for interpolation
    output
        pe_x.wav        ...     synthsized audio using pitch estimation with a confidence x
        test.wav        ...     midi interpolated results
    csv_tester.py       ...     GANSynth interface adapted for pitches seqeunce
    csv2notes.py        ...     preprocess for pitch estimation
```