import lasagne
import numpy as np

#validate_every = 40
start_saving_at = 0
#write_every_batch = 10

epochs = 200
batch_size = 128
N_HIDDEN = 200
n_inputs = 42
num_classes = 8
seq_len = 700


learning_rate_schedule = {
    0: 0.001,
    150: 0.0005,
    400: 0.00025,
}

def build_model():
    l_in = lasagne.layers.InputLayer(shape=(None, seq_len, n_inputs))
    l_forward = lasagne.layers.LSTMLayer(l_in, N_HIDDEN)
    l_vertical = lasagne.layers.ConcatLayer([l_in,l_forward], axis=2)
    l_backward = lasagne.layers.LSTMLayer(l_vertical, N_HIDDEN, backwards=True)
    
    l_reshape = lasagne.layers.ReshapeLayer(
        l_backward, (batch_size*seq_len, N_HIDDEN))
    # Our output layer is a simple dense connection, with 1 output unit
    l_recurrent_out = lasagne.layers.DenseLayer(
        lasagne.layers.dropout(l_reshape, p=0.5), num_units=num_classes, nonlinearity=lasagne.nonlinearities.softmax)

    # Now, reshape the output back to the RNN format
    l_out = lasagne.layers.ReshapeLayer(
        l_recurrent_out, (batch_size, seq_len, num_classes))

    return l_in, l_out

def set_weights():
    metadata_path = "metadata/weight_save/dump_lstm_bi_200_vertical_nosum_dropout-20150709-112634-50.pkl"
    print "setting weights to: %s" %metadata_path
    metadata = np.load(metadata_path)
    return metadata['param_values']