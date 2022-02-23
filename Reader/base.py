class BaseReader:
    def __init__(self, file_name, annotation_file=None):
        import numpy as np
        self._file_name = file_name
        self._anno_file = annotation_file
        self._raw = None
        self._anno = None

    @property
    def raw(self):
        # self._raw = self._raw.resample(100).filter(l_freq=0.1, h_freq=40)
        return self._raw

    def get_event_raw(self, event_name):
        '''
        获取指定event阶段的raw
        Parameters
        ----------
        tag_name: Annotation中指定阶段的名称

        Returns
        -------
        event_raw: Raw
        '''
        import numpy as np

        tmp_raw = self.raw.copy()
        if event_name in ['rest', 'baseline']:
            return tmp_raw.copy().crop(tmin=0, tmax=60*5)
        event_idx = np.where(self._anno.description == event_name)
        start_time = self._anno.onset[event_idx][0]
        duration = self._anno.duration[event_idx][0]
        tmax = min(start_time+duration, tmp_raw.last_samp/tmp_raw.info['sfreq'])
        return tmp_raw.crop(tmin=start_time, tmax=tmax, include_tmax=True)
