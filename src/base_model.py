import os
import sys
import functools
import tensorflow as tf

mod_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(mod_path)

import src.utils.base_utils as base_utils

'''
Base model class is inherited to re-use some common code
'''


class BaseModel(object):

    @base_utils.config_checker(['image_width',
                                'image_height',
                                'image_channels',
                                'grayscale'])
    def __init__(self, config=None):
        self.image = tf.placeholder(tf.float32, shape=(None,
                                                       config.image_height,
                                                       config.image_width,
                                                       1 if config.grayscale else config.image_channels),
                                    name='input_image')

    @base_utils.config_checker(['learning_rate', 'optimizer_type'])
    def optimizer(self, config=None):
        with tf.variable_scope('optimizer', reuse=tf.AUTO_REUSE):
            if config.optimizer_type == 'rmsprop':
                optimizer = tf.train.RMSPropOptimizer(config.learning_rate)
            elif config.optimizer_type == 'sgd':
                optimizer = tf.train.GradientDescentOptimizer(config.learning_rate)
            elif config.optimizer_type == 'adam':
                optimizer = tf.train.AdamOptimizer(config.learning_rate)
            else:
                raise Exception('Unkown optimizer type: %s' % config.optimizer_type)
        return optimizer.minimize(self.loss)