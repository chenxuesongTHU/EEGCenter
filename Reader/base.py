class BaseReader:
    def __init__(self, file_name, annotation_file=None):
        import numpy as np
        self._file_name = file_name
        self._anno_file = annotation_file
        self._raw = None
        self._anno = None

    @property
    def raw(self):
        self._raw = self._raw.resample(100).filter(l_freq=0.1, h_freq=40)
        return self._raw

    # @property
    # def anno(self):
    #     return self._anno

