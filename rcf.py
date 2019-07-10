from keras.layers import Conv2D, Conv2DTranspose, Input
from keras.layers import Conv2D, BatchNormalization, Activation, add
from keras.layers import Concatenate, Activation, Add, Lambda, MaxPooling2D, BatchNormalization
from keras.models import Model
from Subpixel import SubpixelConv2D as subpixel


def side_branch(x, factor):
    x = Conv2D(1, (1, 1), activation=None, padding='same')(x)
    kernel_size = (2*factor, 2*factor)
    x = Conv2DTranspose(1, kernel_size, strides=factor, padding='same', use_bias=False, activation=None)(x)

    return x



def rcf(input_shape=None):
    # Input
    inputs = Input(shape=input_shape)
    x = Lambda(lambda x: x / 255, name='pre-process')(inputs)

    # Block 1
    x1_conv1 = Conv2D(64, (3, 3), activation='relu', padding='same', name='block1_conv1')(inputs)
    x1_conv1_out = Conv2D(21, (1, 1), activation='relu', padding='same', name='b1_conv1_out')(x1_conv1)
    x1_conv2 = Conv2D(64, (3, 3), activation='relu', padding='same', name='block1_conv2')(x1_conv1)
    x1_conv2_out = Conv2D(21, (1, 1), activation='relu', padding='same', name='b1_conv2_o2')(x1_conv2)

    x1_add = Add()([x1_conv1_out, x1_conv2_out])
    b1 = Conv2D(1, (1, 1), activation=None, padding='same')(x1_add)
    #b1 = side_branch(x1_add,1)

    x1 = MaxPooling2D((2, 2), strides=(2, 2), padding='same', name='block1_pool')(x1_conv2)


    # Block 2
    x2_conv1 = Conv2D(128, (3, 3), activation='relu', padding='same', name='block2_conv1')(x1)
    x2_conv1_out = Conv2D(21, (1, 1), activation='relu', padding='same', name='b2_conv1_out')(x2_conv1)
    x2_conv2 = Conv2D(128, (3, 3), activation='relu', padding='same', name='block2_conv2')(x2_conv1)
    x2_conv2_out = Conv2D(21, (1, 1), activation='relu', padding='same', name='b2_conv2_out')(x2_conv2)

    x2_add = Add()([x2_conv1_out, x2_conv2_out])
    b2 = Conv2D(4, (1, 1), activation=None, padding='same')(x2_add)
    #b2 = side_branch(x2_add,2)
    b2 = subpixel(upsampling_factor=2)(b2)

    x2 = MaxPooling2D((2, 2), strides=(2, 2), padding='same', name='block2_pool')(x2_conv2)


    # Block 3
    x3_conv1 = Conv2D(256, (3, 3), activation='relu', padding='same', name='block3_conv1')(x2)
    x3_conv1_out = Conv2D(21, (1, 1), activation='relu', padding='same', name='b3_conv1_out')(x3_conv1)
    x3_conv2 = Conv2D(256, (3, 3), activation='relu', padding='same', name='block3_conv2')(x3_conv1)
    x3_conv2_out = Conv2D(21, (1, 1), activation='relu', padding='same', name='b3_conv2_out')(x3_conv2)
    x3_conv3 = Conv2D(256, (3, 3), activation='relu', padding='same', name='block3_conv3')(x3_conv2)
    x3_conv3_out = Conv2D(21, (1, 1), activation='relu', padding='same', name='b3_conv3_out')(x3_conv3)

    x3_add = Add()([x3_conv1_out, x3_conv2_out, x3_conv3_out])
    b3 = Conv2D(16, (1, 1), activation=None, padding='same')(x3_add)
    #b3 = side_branch(x3_add,4)
    b3 = subpixel(upsampling_factor=4)(b3)

    x3 = MaxPooling2D((2, 2), strides=(2, 2), padding='same', name='block3_pool')(x3_conv3)


    # Block 4
    x4_conv1 = Conv2D(512, (3, 3), activation='relu', padding='same', name='block4_conv1')(x3)
    x4_conv1_out = Conv2D(21, (1, 1), activation='relu', padding='same', name='b4_conv1_out')(x4_conv1)
    x4_conv2 = Conv2D(512, (3, 3), activation='relu', padding='same', name='block4_conv2')(x4_conv1)
    x4_conv2_out = Conv2D(21, (1, 1), activation='relu', padding='same', name='b4_conv2_out')(x4_conv2)
    x4_conv3 = Conv2D(512, (3, 3), activation='relu', padding='same', name='block4_conv3')(x4_conv2)
    x4_conv3_out = Conv2D(21, (1, 1), activation='relu', padding='same', name='b4_conv3_out')(x4_conv3)

    x4_add = Add()([x4_conv1_out, x4_conv2_out, x4_conv3_out])
    b4 = Conv2D(64, (1, 1), activation=None, padding='same')(x4_add)
    #b4 = side_branch(x4_add,8)
    b4 = subpixel(upsampling_factor=8)(b4)

    x4 = MaxPooling2D((2, 2), strides=(1, 1), padding='same', name='block4_pool')(x4_conv3)


    # Block 5
    x5_conv1 = Conv2D(512, (3, 3), activation='relu', padding='same', name='block5_conv1')(x4)
    x5_conv1_out = Conv2D(21, (1, 1), activation='relu', padding='same', name='b5_conv1_out')(x5_conv1)
    x5_conv2 = Conv2D(512, (3, 3), activation='relu', padding='same', name='block5_conv2')(x5_conv1)
    x5_conv2_out = Conv2D(21, (1, 1), activation='relu', padding='same', name='b5_conv2_out')(x5_conv2)
    x5_conv3 = Conv2D(512, (3, 3), activation='relu', padding='same', name='block5_conv3')(x5_conv2)
    x5_conv3_out = Conv2D(21, (1, 1), activation='relu', padding='same', name='b5_conv3_out')(x5_conv3)

    x5_add = Add()([x5_conv1_out, x5_conv2_out, x5_conv3_out])
    b5 = Conv2D(64, (1, 1), activation=None, padding='same')(x5_add)
    #b5 = side_branch(x5_add,8)
    b5 = subpixel(upsampling_factor=8)(b5)

    # fuse
    fuse = Concatenate(axis= -1)([b1, b2, b3, b4, b5])
    fuse = Conv2D(1, (1,1), padding='same', use_bias=False, activation=None)(fuse)

    # outputs
    o1    = Activation('sigmoid', name='o1')(b1)
    o2    = Activation('sigmoid', name='o2')(b2)
    o3    = Activation('sigmoid', name='o3')(b3)
    o4    = Activation('sigmoid', name='o4')(b4)
    o5    = Activation('sigmoid', name='o5')(b5)
    ofuse = Activation('sigmoid', name='ofuse')(fuse)


    # model
    model = Model(inputs=[inputs], outputs=[o1, o2, o3, o4, o5, ofuse])

    return model