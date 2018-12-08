from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from pydoc import locate

import logging
import sys
import subprocess
import time

from six import string_types
import tensorflow as tf
from tensorflow import gfile

from seq2seq import tasks, models
from seq2seq.configurable import _maybe_load_yaml, _deep_merge_dict
from seq2seq.data import input_pipeline
from seq2seq.inference import create_inference_graph
from seq2seq.training import utils as training_utils

flags_batch_size = 32
flags_checkpoint_path = None

saver = None
sess = None


def infer(flags_tasks, model_dir, flags_model_params):

    flags_tasks = _maybe_load_yaml(flags_tasks)

    # Load saved training options
    train_options = training_utils.TrainOptions.load(model_dir)

    # Create the model
    model_cls = locate(train_options.model_class) or \
                getattr(models, train_options.model_class)
    model_params = train_options.model_params

    model_params = _deep_merge_dict(
        model_params, _maybe_load_yaml(flags_model_params))
    model = model_cls(
        params=model_params,
        mode=tf.contrib.learn.ModeKeys.INFER)

    # Load inference tasks
    hooks = []
    for tdict in flags_tasks:
        if not "params" in tdict:
            tdict["params"] = {}
        task_cls = locate(tdict["class"]) or getattr(tasks, tdict["class"])
        task = task_cls(tdict["params"])
        hooks.append(task)

    return model, hooks


def everySenPre(flags_input_pipeline, model, hooks, model_dir, sess):
    flags_input_pipeline = _maybe_load_yaml(flags_input_pipeline)

    input_pipeline_infer = input_pipeline.make_input_pipeline_from_def(
        flags_input_pipeline, mode=tf.contrib.learn.ModeKeys.INFER,
        shuffle=False, num_epochs=1)
    tf.reset_default_graph()
    # Create the graph used for inference
    predictions, _, _ = create_inference_graph(
        model=model,
        input_pipeline=input_pipeline_infer,
        batch_size=flags_batch_size)

    saver = tf.train.Saver()
    checkpoint_path = flags_checkpoint_path
    if not checkpoint_path:
        checkpoint_path = tf.train.latest_checkpoint(model_dir)

    def session_init_op(_scaffold, sess):
        saver.restore(sess, checkpoint_path)
        tf.logging.info("Restored model from %s", checkpoint_path)

    scaffold = tf.train.Scaffold(init_fn=session_init_op)
    session_creator = tf.train.ChiefSessionCreator(scaffold=scaffold)

    # logging.basicConfig(filename='new.log',level=logging.DEBUG)

    sess = tf.train.MonitoredSession(session_creator=session_creator, hooks=hooks)
    output,result = sess.run([])

    # with tf.train.MonitoredSession(
    #         session_creator=session_creator,
    #         hooks=hooks) as sess:
    #     # sess.run(tf.global_variables_initializer())
    #     # Run until the inputs are exhausted
    #     while True:
    #         outputs, result = sess.run([])

    return result, sess