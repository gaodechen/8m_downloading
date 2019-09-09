from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

import absl.flags
from magenta.models.gansynth.lib import flags as lib_flags
from magenta.models.gansynth.lib import generate_util as gu
from magenta.models.gansynth.lib import model as lib_model
from magenta.models.gansynth.lib import util
from csv2notes import read_trim_notes
import tensorflow as tf


absl.flags.DEFINE_string('ckpt_dir',
                         '/tmp/gansynth/acoustic_only',
                         'Path to the base directory of pretrained checkpoints.'
                         'The base directory should contain many '
                         '"stage_000*" subdirectories.')
absl.flags.DEFINE_string('output_dir',
                         '/tmp/gansynth/samples',
                         'Path to directory to save wave files.')
absl.flags.DEFINE_string('csv_file',
                         '',
                         'Path to a csv file to synthesize.')
absl.flags.DEFINE_integer('batch_size', 8, 'Batch size for generation.')
absl.flags.DEFINE_float('secs_per_instrument', 6.0,
                        'In random interpolations, the seconds it takes to '
                        'interpolate from one instrument to another.')

FLAGS = absl.flags.FLAGS
tf.logging.set_verbosity(tf.logging.INFO)


def main(unused_argv):
  absl.flags.FLAGS.alsologtostderr = True

  # Load the model
  flags = lib_flags.Flags({'batch_size_schedule': [FLAGS.batch_size]})
  model = lib_model.Model.load_from_path(FLAGS.ckpt_dir, flags)

  # Make an output directory if it doesn't exist
  output_dir = util.expand_path(FLAGS.output_dir)
  if not tf.gfile.Exists(output_dir):
    tf.gfile.MakeDirs(output_dir)

  if FLAGS.csv_file:
    # If a csv file is provided, synthesize interpolations across the clip
    notes = read_trim_notes(FLAGS.csv_file)
    print(notes['pitches'])

    # Distribute latent vectors linearly in time
    z_instruments, t_instruments = gu.get_random_instruments(
        model,
        notes['end_times'][-1],
        secs_per_instrument=FLAGS.secs_per_instrument)

    # Get latent vectors for each note
    z_notes = gu.get_z_notes(notes['start_times'], z_instruments, t_instruments)

    # Generate audio for each note
    print('Generating {} samples...'.format(len(z_notes)))
    audio_notes = model.generate_samples_from_z(z_notes, notes['pitches'])

    # Make a single audio clip
    audio_clip = gu.combine_notes(audio_notes,
                                  notes['start_times'],
                                  notes['end_times'],
                                  notes['velocities'])

    # Write the wave files
    fname = os.path.join(output_dir, 'generated_clip.wav')
    gu.save_wav(audio_clip, fname)
  else:
    # Otherwise, just generate a batch of random sounds
    waves = model.generate_samples(FLAGS.batch_size)
    # Write the wave files
    for i in range(len(waves)):
      fname = os.path.join(output_dir, 'generated_{}.wav'.format(i))
      gu.save_wav(waves[i], fname)


def console_entry_point():
  tf.app.run(main)


if __name__ == '__main__':
  console_entry_point()
