#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: nl8590687
用于训练语音识别系统语音模型的程序

"""
import os

import tensorflow as tf
from keras.backend.tensorflow_backend import set_session


from SpeechModel251 import ModelSpeech

os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "0,1"
# #进行配置，使用95%的GPU
# config = tf.ConfigProto()
# # config.gpu_options.per_process_gpu_memory_fraction = 0.95
# # config.gpu_options.allow_growth=True   #不全部占满显存, 按需分配
# set_session(tf.Session(config=config))


datapath = 'dataset'
modelpath = 'model_speech'

if(not os.path.exists(modelpath)): # 判断保存模型的目录是否存在
	os.makedirs(modelpath) # 如果不存在，就新建一个，避免之后保存模型的时候炸掉

ms = ModelSpeech(datapath)
ms.TrainModel(datapath, epoch = 50, batch_size = 16, save_step = 500)