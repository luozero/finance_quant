from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import os.path
import sys

import numpy as np



import numpy as np
from six.moves import xrange  # pylint: disable=redefined-builtin
import tensorflow as tf
import tushare as ts
sys.path.append("../stock_deeplearning")
import input_data
import models
from tensorflow.python.platform import gfile

FLAGS = None

def ts_stock_codes():
  basic_data = ts.get_stock_basics()
  stockcode = list(basic_data.index)
  stockcode.remove('603657')
  stockcode.remove('300724')
  stockcode.remove('603192')
  stockcode.remove('601068')
  stockcode.remove('601069')
  stockcode.remove('601606')
  stockcode.sort()
  return stockcode

def main(_):
  # We want to see all the logging messages for this tutorial.
  tf.logging.set_verbosity(tf.logging.INFO)

  # Start a new TensorFlow session.
  sess = tf.InteractiveSession()
  
  FLAGS.stock_codes = ts_stock_codes()
  FLAGS.stock_number = len(FLAGS.stock_codes)

  #Load trade price data.
  stock_codes = list(FLAGS.stock_codes)
  
  model_settings = models.prepare_model_settings(FLAGS.stock_number,FLAGS.data_out_number,\
                                                 FLAGS.proc_days,\
                           FLAGS.hidden1,FLAGS.hidden2)
  stock_data = input_data.StockTradeData(stock_codes, FLAGS.data_input_dir, 
               FLAGS.data_output_dir, FLAGS.start_date,
                FLAGS.end_date, FLAGS.proc_days,FLAGS.verify_days,FLAGS.test_days)
                           
  training_steps_list = list(map(int, FLAGS.how_many_training_steps.split(',')))
  learning_rates_list = list(map(float, FLAGS.learning_rate.split(',')))
  if len(training_steps_list) != len(learning_rates_list):
    raise Exception(
        '--how_many_training_steps and --learning_rate must be equal length '
        'lists, but are %d and %d long instead' % (len(training_steps_list),
                                                   len(learning_rates_list)))
  model_settings['data_in_number']=model_settings['data_in_number']*\
  stock_data.stocks_test_data.shape[2]
  data_input_number = model_settings['data_in_number']

  stock_data_input = tf.placeholder(
      tf.float32, [None, data_input_number], name='data_input_number')

  logits, dropout_prob = models.create_model(
      stock_data_input,
      model_settings,
      FLAGS.model_architecture,
      is_training=True)

  # Define loss and optimizer
  stock_data_output = tf.placeholder(
      tf.float32, [None,1], name='stock_data_output')

  # Optionally we can add runtime checks to spot when NaNs or other symptoms of
  # numerical errors start occurring during training.
  control_dependencies = []
  if FLAGS.check_nans:
    checks = tf.add_check_numerics_ops()
    control_dependencies = [checks]

  # Create the back propagation and training evaluation machinery in the graph.
  with tf.name_scope('mean_squared'):
    mean_squared_error = tf.losses.mean_squared_error(
        labels=stock_data_output, predictions=logits)
  tf.summary.scalar('mean_squared', mean_squared_error)
  with tf.name_scope('train'), tf.control_dependencies(control_dependencies):
    learning_rate_input = tf.placeholder(
        tf.float32, [], name='learning_rate_input')
    train_step = tf.train.GradientDescentOptimizer(
        learning_rate_input).minimize(mean_squared_error)
        
  stock_predicted_sign = tf.sign(logits)
  stock_truth_sign = tf.sign(stock_data_output)
  correct_prediction = tf.equal(stock_predicted_sign, stock_truth_sign)
  evaluation_step = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
  tf.summary.scalar('accuracy', evaluation_step)

  global_step = tf.train.get_or_create_global_step()
  increment_global_step = tf.assign(global_step, global_step + 1)

  saver = tf.train.Saver(tf.global_variables())

  # Merge all the summaries and write them out to /tmp/retrain_logs (by default)
  merged_summaries = tf.summary.merge_all()
  train_writer = tf.summary.FileWriter(FLAGS.summaries_dir + '/train',
                                       sess.graph)
  validation_writer = tf.summary.FileWriter(FLAGS.summaries_dir + '/validation')

  tf.global_variables_initializer().run()

  start_step = 1
  if FLAGS.start_checkpoint:
    models.load_variables_from_checkpoint(sess, FLAGS.start_checkpoint)
    start_step = global_step.eval(session=sess)

  tf.logging.info('Training from step: %d ', start_step)

  # Save graph.pbtxt.
  tf.train.write_graph(sess.graph_def, FLAGS.train_dir,
                       FLAGS.model_architecture + '.pbtxt')

  # Save list of words.
  with gfile.GFile(
      os.path.join(FLAGS.train_dir, FLAGS.model_architecture + '_labels.txt'),
      'w') as f:
    stock_close_price = stock_data.stocks_test_data.loc[:,:,'close']
    f.write('\n'.join(str(np.sign(stock_close_price.loc[:,FLAGS.train_stock].values ))))

  # Training loop.
  training_steps_max = np.sum(training_steps_list)
  for training_step in xrange(start_step, training_steps_max + 1):
    # Figure out what the current learning rate is.
    training_steps_sum = 0
    for i in range(len(training_steps_list)):
      training_steps_sum += training_steps_list[i]
      if training_step <= training_steps_sum:
        learning_rate_value = learning_rates_list[i]
        break
    # Pull the audio samples we'll use for training.
    train_stock_truth, train_stock_input = stock_data.input_func(\
        FLAGS.train_stock, FLAGS.batch_size, FLAGS.future_day,\
        input_data.ProcessDataType.train)

    # Run the graph with this batch of training data.
    train_summary, train_accuracy, mean_squared_value, _, _ = sess.run(
        [
            merged_summaries, evaluation_step, mean_squared_error, train_step,
            increment_global_step
        ],
        feed_dict={
            stock_data_input: train_stock_input,
            stock_data_output: train_stock_truth,
            learning_rate_input: learning_rate_value,
            dropout_prob: 0.5
        })
    train_writer.add_summary(train_summary, training_step)
    tf.logging.info('Step #%d: rate %f, accuracy %.1f%%, mean squared value %f' %
                    (training_step, learning_rate_value, train_accuracy*100, mean_squared_value))
    is_last_step = (training_step == training_steps_max)
    if (training_step % FLAGS.eval_step_interval) == 0 or is_last_step:
      set_size = FLAGS.verify_days
      total_accuracy = 0
      #total_conf_matrix = None
      for i in xrange(0, set_size, FLAGS.batch_size):
        train_stock_truth, train_stock_input = stock_data.input_func(\
          FLAGS.train_stock, FLAGS.batch_size, FLAGS.future_day,\
          input_data.ProcessDataType.verify)
        # Run a validation step and capture training summaries for TensorBoard
        # with the `merged` op.
        validation_summary, validation_accuracy, validation_mean_squared_value = sess.run(
            [merged_summaries, evaluation_step, mean_squared_error],
            feed_dict={
                stock_data_input: train_stock_input,
                stock_data_output: train_stock_truth,
                dropout_prob: 1.0
            })
        validation_writer.add_summary(validation_summary, training_step)
        batch_size = min(FLAGS.batch_size, set_size - i)
        total_accuracy += (validation_accuracy * batch_size) / set_size
        #if total_conf_matrix is None:
        #  total_conf_matrix = conf_matrix
        #else:
        #  total_conf_matrix += conf_matrix
      #tf.logging.info('Confusion Matrix:\n %s' % (total_conf_matrix))
      tf.logging.info('Step %d: Validation accuracy = %.1f%% (N=%d)' %
                      (training_step, total_accuracy * 100, set_size))

    # Save the model checkpoint periodically.
    if (training_step % FLAGS.save_step_interval == 0 or
        training_step == training_steps_max):
      checkpoint_path = os.path.join(FLAGS.train_dir,
                                     FLAGS.model_architecture + '.ckpt')
      tf.logging.info('Saving to "%s-%d"', checkpoint_path, training_step)
      saver.save(sess, checkpoint_path, global_step=training_step)

  set_size = FLAGS.test_days
  tf.logging.info('set_size=%d', set_size)
  total_accuracy = 0
  #total_conf_matrix = None
  for i in xrange(0, set_size, FLAGS.batch_size):
    train_stock_truth,train_stock_input = stock_data.input_func(\
          FLAGS.train_stock, FLAGS.batch_size, FLAGS.future_day,\
          input_data.ProcessDataType.test)
        # Run a validation step and capture training summaries for TensorBoard
        # with the `merged` op.
    test_accuracy, test_mean_squared_value = sess.run(
        [evaluation_step, mean_squared_error],
        feed_dict={
            stock_data_input: train_stock_input,
            stock_data_output: train_stock_truth,
            dropout_prob: 1.0
        })
    batch_size = min(FLAGS.batch_size, set_size - i)
    total_accuracy += (test_accuracy * batch_size) / set_size
    #if total_conf_matrix is None:
    #  total_conf_matrix = conf_matrix
    #else:
     # total_conf_matrix += conf_matrix
  #tf.logging.info('Confusion Matrix:\n %s' % (total_conf_matrix))
  tf.logging.info('Final test accuracy = %.1f%% (N=%d)' % (total_accuracy * 100,
                                                           set_size))

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument(
      '--stock_codes',
      type=list,
      # pylint: disable=line-too-long
      default=['000001','000002','000018', '600000','600005','600007'],
      # pylint: enable=line-too-long
      help='stock codes.')
  parser.add_argument(
      '--stock_number',
      type=int,
      # pylint: disable=line-too-long
      default='6',
      # pylint: enable=line-too-long
      help='number of input stocks.')
  parser.add_argument(
      '--train_stock',
      type=str,
      # pylint: disable=line-too-long
      default='600007',
      # pylint: enable=line-too-long
      help='train stock codes.')
  parser.add_argument(
      '--start_date',
      type=str,
      default='2014-01-01',
      help='start training date.')
  parser.add_argument(
      '--end_date',
      type=str,
      default='2018-07-29',
      help='end training date.')
  parser.add_argument(
      '--proc_days',
      type=int,
      # pylint: disable=line-too-long
      default='15',
      # pylint: enable=line-too-long
      help='proc days.')
  parser.add_argument(
      '--verify_days',
      type=int,
      # pylint: disable=line-too-long
      default='20',
      # pylint: enable=line-too-long
      help='verified days.')
  parser.add_argument(
      '--test_days',
      type=int,
      # pylint: disable=line-too-long
      default='20',
      # pylint: enable=line-too-long
      help='test days.')
  parser.add_argument(
      '--future_day',
      type=int,
      # pylint: disable=line-too-long
      default='1',
      # pylint: enable=line-too-long
      help='future days.')  
  parser.add_argument(
      '--data_out_number',
      type=int,
      # pylint: disable=line-too-long
      default='1',
      # pylint: enable=line-too-long
      help='number of output stocks.')
  parser.add_argument(
      '--hidden1',
      type=int,
      # pylint: disable=line-too-long
      default='20',
      # pylint: enable=line-too-long
      help='number of output stocks.')
  parser.add_argument(
      '--hidden2',
      type=int,
      # pylint: disable=line-too-long
      default='20',
      # pylint: enable=line-too-long
      help='number of output stocks.')
  parser.add_argument(
      '--data_input_dir',
      type=str,
      default='../stock_data/stockdata/stocktradedata',
      help="""\
      Where to download the stock training data to.
      """)
  parser.add_argument(
      '--data_output_dir',
      type=str,
      default='../stock_data/stockdata/pctdata',
      help="""\
      Where to store the stock training data.
      """)
  parser.add_argument(
      '--how_many_training_steps',
      type=str,
      default='15,30',
      help='How many training loops to run')
  parser.add_argument(
      '--learning_rate',
      type=str,
      default='0.001,0.0001',
      help='How large a learning rate to use when training.')
  parser.add_argument(
      '--start_checkpoint',
      type=str,
      default='',
      help='If specified, restore this pretrained model before any training.')
  parser.add_argument(
      '--summaries_dir',
      type=str,
      default='/tmp/retrain_logs',
      help='Where to save summary logs for TensorBoard.')
  parser.add_argument(
      '--train_dir',
      type=str,
      default='/tmp/stock_price_train',
      help='Directory to write event logs and checkpoint.')
  parser.add_argument(
      '--eval_step_interval',
      type=int,
      default=400,
      help='How often to evaluate the training results.')
  parser.add_argument(
      '--save_step_interval',
      type=int,
      default=100,
      help='Save model checkpoint every save_steps.')
  parser.add_argument(
      '--model_architecture',
      type=str,
      default='relu',#line relu
      help='What model architecture to use')
  parser.add_argument(
      '--check_nans',
      type=bool,
      default=False,
      help='Whether to check for invalid numbers during processing')
  parser.add_argument(
      '--batch_size',
      type=int,
      default=5,
      help='How many items to train with at once',)
  
  FLAGS, unparsed = parser.parse_known_args()
  tf.app.run(main=main, argv=[sys.argv[0]] + unparsed)