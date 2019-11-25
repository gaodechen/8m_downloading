import tensorflow as tf
import numpy as np
import sys
import os


def int64_feature(values):
    if not isinstance(values, (tuple, list)):
        values = [values]
    return tf.train.Feature(int64_list=tf.train.Int64List(value=values))


def bytes_feature(values):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[values]))


def float_feature(value):
    return tf.train.Feature(float_list=tf.train.FloatList(value=value))


def audio_to_tfexample(data, label):
    return tf.train.Example(features=tf.train.Features(feature={
        'data': bytes_feature(data),
        'label': int64_feature(label),
    }))


def write_tfrecord(npy_list, tfrecord_dir='./'):
    """ Convert data to TFRecord format. """
    output_filename = os.path.join(tfrecord_dir, "train.tfrecord")
    tfrecord_writer = tf.python_io.TFRecordWriter(output_filename)
    length = len(npy_list)
    for i in range(length):
        data = bytes(np.load(npy_list[i]))
        label = 1
        example = audio_to_tfexample(data, label)
        tfrecord_writer.write(example.SerializeToString())


def read_tfrecord(tfrecord_filename='train.tfrecord', shape=[416, 90]):
    def parser(record):
        features = tf.parse_single_example(record, features={
            'label': tf.FixedLenFeature([], tf.int64),
            'data': tf.FixedLenFeature([], tf.string), })
        data = tf.decode_raw(features["data"], tf.uint8)
        data = tf.reshape(data, shape)
        label = tf.cast(features["label"], tf.int64)
        return data, label

    dataset = tf.data.TFRecordDataset(tfrecord_filename)
    dataset = dataset.map(parser)
    dataset = dataset.repeat()
    dataset = dataset.batch(1)
    dataset = dataset.shuffle(buffer_size=1)
    iterator = dataset.make_one_shot_iterator()
    label_output = iterator.get_next()
    return label_output


if __name__ == '__main__':
    write_tfrecord(['test.npy'])
    dataset = read_tfrecord()
    sess = tf.Session()
    for i in range(10):
        data, label = sess.run(dataset)
        print(data)
        print(data.shape)
    sess.close()