'''
Module for managing the PyOpia processing pipeline

Refer to :class:`Pipeline` for examples of how to process datasets and images
'''


class Pipeline():
    '''The processing pipeline class
    ================================

    The classes called in the Pipeline steps can be modified, and the names of the steps changed.
    New steps can be added or deleted as required.

    The classes called in the Pipeline steps need to take a dictionary as input and return a dictionary as output.
    This common dictionary (`data`) is therefore passed between steps so that data
    or variables generated by each step can be passed along the pipeline.

    By default, the `steps` dict keys: 'initial' and 'classifier' are run when initialising `Pipeline`,
    the remaining steps will be run on Pipeline.run().
    You can change the initial steps by with the optional input `initial_steps`,
    which takes a list of the step keys that should only be run on initialisation of the pipeline.

    The step called 'classifier' must return a dict containing 'cl' in order to run successfully.

    `Pipeline.run()` takes a string as input.
    This string is put into the `data` dict available to the steps in the pipeline as `data['filename']`.
    This is intended for use in looping through several files during processing, so run can be
    called multiple times with different filenames.

    Examples:
    ^^^^^^^^^

    A holographic processing pipeline:
    """"""""""""""""""""""""""""""""""

    .. code-block:: python

        filename, background_file = exampledata.get_example_hologram_and_background()
        datafile_hdf = 'proc/holotest'
        model_path = exampledata.get_example_model()
        threshold = 0.9

        holo_initial_settings = {'pixel_size': 4.4, # pixel size in um
                                'wavelength': 658, # laser wavelength in nm
                                'minZ': 22, # minimum reconstruction distance in mm
                                'maxZ': 60, # maximum reconstruction distance in mm
                                'stepZ': 2} #step size in mm

        steps = {'initial': holo.Initial('imbg-001-2082.pgm', **holo_initial_settings),
                 'classifier': Classify(model_path=model_path),
                 'load': holo.Load(),
                 'reconstruct': holo.Reconstruct(stack_clean=0),
                 'segmentation': pyopia.process.Segment(threshold=threshold),
                 'statextract': pyopia.process.CalculateStats(),
                 'output': pyopia.io.StatsH5(datafile_hdf)}

        processing_pipeline = Pipeline(steps)

    A silcam processing pipeline:
    """""""""""""""""""""""""""""

    .. code-block:: python

        datafile_hdf = 'proc/test'
        model_path = exampledata.get_example_model()
        threshold = 0.85

        steps = {'classifier': Classify(model_path=model_path),
                 'load': SilCamLoad(),
                 'imageprep': ImagePrep(),
                 'segmentation': pyopia.process.Segment(threshold=threshold),
                 'statextract': pyopia.process.CalculateStats(),
                 'output': pyopia.io.StatsH5(datafile_hdf)}

        # initialise the pipeline with a only the 'classifier' initialisation step:
        processing_pipeline = Pipeline(steps, initial_steps=['classifier'])

    Running a pipeline:
    """""""""""""""""""

    .. code-block:: python

        stats = processing_pipeline.run(filename)


    You can check the workflow used by reading the steps from the metadata in output file, like this:

    .. code-block:: python

        pyopia.io.show_h5_meta(datafile_hdf + '-STATS.h5')



    '''

    def __init__(self, steps, initial_steps=['initial', 'classifier']):

        self.initial_steps = initial_steps
        print('Initialising pipeline')
        self.data = dict()
        self.steps = steps

        for s in self.steps:
            if not self.initial_steps.__contains__(s):
                continue
            if s == 'classifier':
                print('  Running', self.steps['classifier'])
                self.data['cl'] = self.steps['classifier']()
            else:
                print('  Running', self.steps[s])
                self.data = self.steps[s](self.data)

        print('Pipeline ready with these data: ', list(self.data.keys()))

    def run(self, filename):
        '''Method for executing the processing pipeline

        Returns:
            stats (DataFrame): stats DataFrame of particle statistics
        '''

        self.data['filename'] = filename

        self.data['steps_string'] = steps_to_string(self.steps)

        for s in self.steps:
            if self.initial_steps.__contains__(s):
                continue

            print('calling: ', str(type(self.steps[s])), ' with: ', list(self.data.keys()))
            self.data = self.steps[s](self.data)

        stats = self.data['stats']

        return stats

    def print_steps(self):
        '''Print the steps dictionary
        '''

        # an eventual metadata parser could replace this below printing
        # and format into an appropriate standard
        print('\n-- Pipeline configuration --\n')
        from pyopia import __version__ as pyopia_version
        print('PyOpia version: ' + pyopia_version + '\n')
        print(steps_to_string(self.steps))
        print('\n---------------------------------\n')


def steps_to_string(steps):
    '''Convert pipeline steps dictionary to a human-readable string

    Args:
        steps (dict): pipeline steps dictionary

    Returns:
        str: human-readable string of the types and variables
    '''

    steps_str = '\n'
    for i, key in enumerate(steps.keys()):
        steps_str += (str(i + 1) + ') Step: ' + key
                      + '\n   Type: ' + str(type(steps[key]))
                      + '\n   Vars: ' + str(vars(steps[key]))
                      + '\n')
    return steps_str
