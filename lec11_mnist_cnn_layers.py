import tensorflow as tf

from tensorflow.examples.tutorials.mnist import input_data

tf.set_random_seed(777)

mnist = input_data.read_data_sets("MNIST_data/", ont_hot=True)

#hyper parameters
learning_rate = 0.001
training_epochs = 15
batch_size = 100

class Model:
    def __init__(self, sess, name):
        self.sess = sess
        self.name = name
        self._build_net()

    def _build_net(self):
        with tf.variable_scope(self.name):

            self.training = tf.placeholder(tf.bool)

            #input X place holder
            self.X = tf.placeholder(tf.float32, [None, 784])

            #Image Input Layer/ 28*28*1 (RGB = 1 (black/white))
            X_img = tf.reshape(self.X, [-1,28,28,1])
            self.Y = tf.placeholder(tf.float32, [None, 10])

            #Conv Layer1 / Pooling Layer1
            conv1 = tf.layers.conv2d(inputs=X_img, filters=32, kernal_size=[3,3], padding="SAME", activation=tf.nn.relu)
            pool1 = tf.layers.max_pooling2d(inputs=conv1, pooling_size=[2,2], padding="SAME", strides=2)  #stride = 2 / 필터가 2씩 이동.
            dropout1 = tf.layers.dropout(inputs=pool1, rate=0.7, training=self.training)

            #Conv Layer2 / Pooling Layer2
            conv2 = tf.layers.conv2d(inputs=dropout1, filters=64, kernal_size=[3,3], padding="SAME", activation=tf.nn.relu)
            pool2 = tf.layers.max_pooling2d(inputs=conv2, pooling_size=[2,2], padding="SAME", strides=2)  #stride = 2 / 필터가 2씩 이동.
            dropout2 = tf.layers.dropout(inputs=pool2, rate=0.7, training=self.training)

            #Conv Layer3 / Pooling Layer2
            conv3 = tf.layers.con2d(inputs=dropout2, filters=128, kernal_size=[3,3], padding="SAME", activation=tf.nn.relu)
            pool3 = tf.layers.max_pooling2d(inputs=conv3, pooling_size=[2,2],padding="same", strides=2)
            dropout3 = tf.layers.dropout(inputs=pool3, rate=0.7, training=self.training)

            #Dense Layer with ReLU (fully connected Layer)
            flat = tf.reshape(dropout3, [-1,128*4*4])
            dense4 = tf.layers.dense(inputs=flat,
                                     units=625, activation=tf.nn.relu) # units => 몇개를 출력할 지 정해준다.
            dropout4 = tf.layers.dropout(inputs=dense4,
                                         rate=0.5, training=self.training)

            # Fully connected Layer(Logits Layer) : activation - X (ReLU 아님!) / inputs : 625 ==> outputs : 10
            self.logits = tf.layers.dense(inputs=dropout4, units=10)

        # define cost/loss & optimizer
        self.cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=self.logits, labels=self.Y))
        self.optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(self.cost)

        correct_prediction = tf.equal(
            tf.argmax(self.logits, 1), tf.argmax(self.Y, 1))
        self.accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

    def predict(self, x_test, training=False):
        return self.sess.run(self.logits,
                             feed_dict={self.X: x_test, self.training: training})

    def get_accuracy(self, x_test, y_test, training=False):
        return self.sess.run(self.accuracy,
                             feed_dict={self.X: x_test,
                                        self.Y: y_test, self.training: training})

    def train(self, x_data, y_data, training=True):
        return self.sess.run([self.cost, self.optimizer], feed_dict={
            self.X: x_data, self.Y: y_data, self.training: training})

# initialize
sess = tf.Session()
m1 = Model(sess, "m1")

sess.run(tf.global_variables_initializer())

print('Learning Started!')

# train my model
for epoch in range(training_epochs):
    avg_cost = 0
    total_batch = int(mnist.train.num_examples / batch_size)

    for i in range(total_batch):
        batch_xs, batch_ys = mnist.train.next_batch(batch_size)
        c, _ = m1.train(batch_xs, batch_ys)
        avg_cost += c / total_batch

    print('Epoch:', '%04d' % (epoch + 1), 'cost =', '{:.9f}'.format(avg_cost))

print('Learning Finished!')

# Test model and check accuracy
print('Accuracy:', m1.get_accuracy(mnist.test.images, mnist.test.labels))
