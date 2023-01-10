'''
Module containing SilCam specific tools to enable compatability with the :mod:`pyopia.pipeline`
'''

import os

import numpy as np
import pandas as pd
import pyopia


def silcam_steps(model_path, threshold, datafile_hdf):
    '''generate a default / suggested steps dictionary for standard silcam analsysis

    Parameters
    ----------
    model_path : str
        path to classification model
    threshold : float
        threshold for segmentation
    datafile_hdf : str
        output data path

    Returns
    -------
    steps : dict
        dictionary of steps
    initial_steps : list[str]
        list of strings for initial steps

    Example
    """""""

    .. code-block:: python

        from pyopia.instrument.silcam import silcam_steps
        default_steps, default_initial_steps = silcam_steps(model_path, threshold, datafile_hdf)

        # initialise the pipeline
        processing_pipeline = Pipeline(default_steps, initial_steps=default_initial_steps)

    '''
    steps = {'classifier': pyopia.classify.Classify(model_path=model_path),
             'load': SilCamLoad(),
             'imageprep': ImagePrep(),
             'segmentation': pyopia.process.Segment(threshold=threshold),
             'statextract': pyopia.process.CalculateStats(),
             'output': pyopia.io.StatsH5(datafile_hdf)}
    initial_steps = ['classifier']
    return steps, initial_steps


def timestamp_from_filename(filename):
    '''get a pandas timestamp from a silcam filename

    Args:
        filename (string): silcam filename (.silc)

    Returns:
        timestamp: timestamp from pandas.to_datetime()
    '''

    # get the timestamp of the image (in this case from the filename)
    timestamp = pd.to_datetime(os.path.splitext(os.path.basename(filename))[0][1:])
    return timestamp


class SilCamLoad():
    '''PyOpia pipline-compatible class for loading a single silcam image

    Parameters
    ----------
    filename : string
        silcam filename (.silc)

    Returns
    -------
    timestamp : timestamp
        timestamp from timestamp_from_filename()
    img : np.array
        raw silcam image
    '''

    def __init__(self):
        pass

    def __call__(self, data):
        timestamp = timestamp_from_filename(data['filename'])
        img = np.load(data['filename'], allow_pickle=False)
        data['timestamp'] = timestamp
        data['img'] = img
        return data


class ImagePrep():

    def __init__(self):
        pass

    def __call__(self, data):
        # @todo
        # #imbg = data['imbg']
        # background correction
        print('WARNING: Background correction not implemented!')
        imraw = data['img']
        imc = np.float64(imraw)

        # simplify processing by squeezing the image dimensions into a 2D array
        # min is used for squeezing to represent the highest attenuation of all wavelengths
        imc = np.min(imc, axis=2)
        imc -= np.min(imc)
        imc /= np.max(imc)

        data['imc'] = imc
        return data
