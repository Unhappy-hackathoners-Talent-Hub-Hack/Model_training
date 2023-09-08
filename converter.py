#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import coremltools
import keras

model_path = 'popitkaAD3.h5'
keras_model =  keras.models.load_model(model_path)
model = coremltools.convert(keras_model, convert_to="mlprogram")
model.save('model_AD')