#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#                                                       "model.ckpt-50")
#                                                       "model.ckpt-50")
#                                        "model.ckpt-50.data-00000-of-00001")
#                                    os.path.join(BIN_FOLDER, "infer.py"))
#                                    os.path.join(BIN_FOLDER, "infer.py"))
#                                    os.path.join(BIN_FOLDER, "train.py"))
#                           "num_units": 8
#                           "num_units": 8
#                       "cell_class": "GRUCell",
#                       "cell_class": "GRUCell",
#                       "cell_params": {
#                       "cell_params": {
#                       }
#                       }
#                   "rnn_cell": {
#                   "rnn_cell": {
#                   "source_files": [sources_dev.name],
#                   "source_files": [sources_train.name],
#                   "target_files": [targets_dev.name],
#                   "target_files": [targets_train.name],
#                   }
#                   }
#               "class": "ParallelTextInputPipeline",
#               "class": "ParallelTextInputPipeline",
#               "decoder.params": {
#               "embedding.dim": 10,
#               "encoder.params": {
#               "params": {
#               "params": {
#               }
#               }
#               }
#               },
#           "input_pipeline_dev": {
#           "input_pipeline_train": {
#           "model_params": {
#           "train_steps": 50,
#           - {}
#           - {}
#           - {}
#           - {}
#           rouge_type: rouge_1/f_score
#           }
#           },
#           },
#         file: {}
#         os.path.exists(os.path.join(attention_dir, "attention_scores.npz")))
#         os.path.join(os.path.dirname(__file__), "../../bin"))
#         output_dir: {}
#         params:
#         postproc_fn: seq2seq.data.postproc.decode_sentencepiece
#         source_files:
#         source_files:
#         sources=["a a a a", "b b b b", "c c c c", "笑 笑 笑 笑"],
#         sources=["a a", "b b", "c c c", "笑 笑 笑"],
#         target_files:
#         target_files:
#         targets=["b b b b", "a a a a", "c c c c", "泣 泣 泣 泣"])
#         targets=["b b", "a a", "c c c", "泣 泣 泣"])
#       - class: BleuMetricSpec
#       - class: LogPerplexityMetricSpec
#       - class: MetadataCaptureHook
#       - class: PrintModelAnalysisHook
#       - class: RougeMetricSpec
#       - class: TrainSampleHook
#       class: ParallelTextInputPipeline
#       class: ParallelTextInputPipeline
#       inference.beam_search.beam_width: 5
#       num_units: 10
#       params:
#       params:
#       params:
#       params:
#       params:
#       yaml.dump({
#       }, config_file)
#     """
#     """
#     """
#     """
#     """.format(attention_dir)
#     """.format(os.path.join(self.output_dir, "beams.npz"))
#     """.format(sources_dev.name, targets_dev.name)
#     """.format(sources_dev.name, targets_dev.name)
#     """.format(vocab_source.name, vocab_target.name)
#     """Tests training and inference scripts.
#     # Create dummy data
#     # Load attention scores and assert shape
#     # Make sure a checkpoint was written
#     # Make sure attention scores and visualizations exist
#     # Make sure inference runs successfully
#     # Reset flags and import inference script
#     # Run inference w/ beam search
#     # Run training
#     # Set inference flags
#     # Set inference flags
#     # Set training flags
#     # Test inference with beam search
#     # Use DecodeText Task
#     # We pass a few flags via a config file
#     - class: DecodeText
#     - class: DecodeText
#     - class: DumpAttention
#     - class: DumpBeams
#     _clear_flags()
#     _clear_flags()
#     _clear_flags()
#     attention.params:
#     attention_dir = os.path.join(self.output_dir, "att")
#     config_path = os.path.join(self.output_dir, "train_config.yml")
#     expected_checkpoint = os.path.join(self.output_dir,
#     infer_script = imp.load_source("seq2seq.test.infer_bin",
#     infer_script = imp.load_source("seq2seq.test.infer_bin",
#     infer_script.main([])
#     infer_script.main([])
#     os.path.join(os.path.dirname(__file__), "../../bin"))
#     scores = np.load(os.path.join(attention_dir, "attention_scores.npz"))
#     self.assertEqual(scores["arr_0"].shape[1], 3)
#     self.assertEqual(scores["arr_1"].shape[1], 3)
#     self.assertEqual(scores["arr_2"].shape[1], 4)
#     self.assertEqual(scores["arr_3"].shape[1], 4)
#     self.assertIn("arr_0", scores)
#     self.assertIn("arr_1", scores)
#     self.assertIn("arr_2", scores)
#     self.assertIn("arr_3", scores)
#     self.assertTrue(
#     self.assertTrue(os.path.exists(expected_checkpoint))
#     self.assertTrue(os.path.exists(os.path.join(attention_dir, "00002.png")))
#     self.assertTrue(os.path.exists(os.path.join(self.output_dir, "beams.npz")))
#     self.bin_folder = os.path.abspath(
#     self.output_dir = tempfile.mkdtemp()
#     shutil.rmtree(self.output_dir, ignore_errors=True)
#     sources_dev, targets_dev = test_utils.create_temp_parallel_data(
#     sources_train, targets_train = test_utils.create_temp_parallel_data(
#     super(PipelineTest, self).setUp()
#     super(PipelineTest, self).tearDown()
#     tf.app.flags.FLAGS.batch_size = 2
#     tf.app.flags.FLAGS.batch_size = 2
#     tf.app.flags.FLAGS.batch_size = 2
#     tf.app.flags.FLAGS.checkpoint_path = os.path.join(self.output_dir,
#     tf.app.flags.FLAGS.checkpoint_path = os.path.join(self.output_dir,
#     tf.app.flags.FLAGS.config_paths = config_path
#     tf.app.flags.FLAGS.hooks = """
#     tf.app.flags.FLAGS.input_pipeline = """
#     tf.app.flags.FLAGS.input_pipeline = """
#     tf.app.flags.FLAGS.metrics = """
#     tf.app.flags.FLAGS.model = "AttentionSeq2Seq"
#     tf.app.flags.FLAGS.model_dir = self.output_dir
#     tf.app.flags.FLAGS.model_dir = self.output_dir
#     tf.app.flags.FLAGS.model_params = """
#     tf.app.flags.FLAGS.model_params = """
#     tf.app.flags.FLAGS.output_dir = self.output_dir
#     tf.app.flags.FLAGS.tasks = """
#     tf.app.flags.FLAGS.tasks = """
#     tf.contrib.framework.get_or_create_global_step()
#     tf.logging.set_verbosity(tf.logging.INFO)
#     tf.reset_default_graph()
#     tf.reset_default_graph()
#     tf.reset_default_graph()
#     train_script = imp.load_source("seq2seq.test.train_bin",
#     train_script.main([])
#     vocab_source = test_utils.create_temporary_vocab_file(["a", "b", "c", "笑"])
#     vocab_source: {}
#     vocab_target = test_utils.create_temporary_vocab_file(["a", "b", "c", "泣"])
#     vocab_target: {}
#     with gfile.GFile(config_path, "w") as config_file:
#   """
#   """Resets Tensorflow's FLAG values"""
#   """Tests training and inference scripts.
#   #pylint: disable=W0212
#   def setUp(self):
#   def tearDown(self):
#   def test_train_infer(self):
#   tf.app.flags._global_parser = argparse.ArgumentParser()
#   tf.app.flags.FLAGS = tf.app.flags._FlagValues()
#   tf.test.main()
# """
# """
# #
# #
# #
# #      http://www.apache.org/licenses/LICENSE-2.0
# # -*- coding: utf-8 -*-
# # Copyright 2017 Google Inc.
# # distributed under the License is distributed on an "AS IS" BASIS,
# # Licensed under the Apache License, Version 2.0 (the "License");
# # limitations under the License.
# # See the License for the specific language governing permissions and
# # Unless required by applicable law or agreed to in writing, software
# # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# # you may not use this file except in compliance with the License.
# # You may obtain a copy of the License at
# BIN_FOLDER = os.path.abspath(
# class PipelineTest(tf.test.TestCase):
# def _clear_flags():
# from __future__ import absolute_import
# from __future__ import division
# from __future__ import print_function
# from __future__ import unicode_literals
# from seq2seq.test import utils as test_utils
# from tensorflow import gfile
# if __name__ == "__main__":
# import argparse
# import imp
# import numpy as np
# import os
# import shutil
# import tempfile
# import tensorflow as tf
# import yaml
# Test Cases for RNN encoders.