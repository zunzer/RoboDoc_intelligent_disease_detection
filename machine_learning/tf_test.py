import tensorflow as tf
import numpy as np
from tensorflow import keras

def test():
    """Test if your Tensor Flow Installation is working

    :return:
    """
    xs = np.array([-1.0, 0.0, 1.0, 2.0, 3.0, 4.0], dtype=float)
    ys = np.array([-3.0, -1.0, 1.0, 3.0, 5.0, 7.0], dtype=float)

    model = tf.keras.Sequential()
    model.add(keras.layers.Dense(units=1, input_shape=[1]))
    model.compile(optimizer='SGD', loss='mean_squared_error')
    model.fit(xs, ys, epochs=500)

    print(model.predict([22]))



if __name__ == "__main__":
    test()