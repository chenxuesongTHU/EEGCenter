"""
====================================
EEG artifact correction using FASTER
====================================
In this example, a variety of metrics are used to detect channels and epochs
that contain artifacts. Rejection and interpolation are used to clean the EEG
data.
References
----------
[1] Nolan H., Whelan R. and Reilly RB. FASTER: fully automated
    statistical thresholding for EEG artifact rejection. Journal of
    Neuroscience Methods, vol. 192, issue 1, pp. 152-162, 2010.
"""
import mne
from mne import io
from mne.datasets import sample
from src import *

from Reader import BrainVisionReader
from src  import (find_bad_channels, find_bad_epochs, find_bad_channels_in_epochs)

# Load raw data
# data_path = sample.data_path()
# raw_fname = data_path + '/MEG/sample/sample_audvis_filt-0-40_raw.fif'
# event_fname = data_path + '/MEG/sample/sample_audvis_filt-0-40_raw-eve.fif'

user_id = 'p01'
# raw = io.read_raw_fif(raw_fname, preload=True)
reader = BrainVisionReader(f'{RAW_EEG_PATH}/{user_id}.vhdr', f'{LOG_PATH}/{user_id}.csv')
raw = reader.raw.load_data()
raw.info['bads'] = []  # bads are going to be detected automatically
# events = mne.annotations(event_fname)
events, event_ids = mne.events_from_annotations(
    raw,
    # event_id=annotation_desc_2_event_id,
    # chunk_duration=30.
)

# In this example, we restrict analysis to EEG channels only to save memory and
# time. However, these methods also work for MEG data.
raw = raw.pick_types(meg=False, eeg=True, eog=True)

# Keep whatever EEG reference the amplifier used for now. After the data is
# cleaned, we will re-reference to an average reference.
raw, _ = io.set_eeg_reference(raw, ['TP9', 'TP10'])

# Highpass filter the EEG and EOG data to eliminate drifts
# NOTE: we do not lowpass filter here, because power line noise is useful for
#       detecting bad channels.
picks = mne.pick_types(raw.info, eeg=True, eog=True)
raw.filter(0.3, None, method='iir', picks=picks)

# Construct epochs. Note that we also include EOG channels.
# event_ids = {'AudL': 1, 'AudR': 2, 'VisL': 3, 'VisR': 4}
tmin = -0.2
tmax = 0.5
epochs = mne.Epochs(raw, events, event_ids, tmin, tmax, baseline=(None, 0),
                    preload=True, picks=picks)

# Compute evoked before cleaning, using an average EEG reference
epochs_before = epochs.copy()
epochs_before.info['custom_ref_applied'] = True
epochs_before, _ = io.set_eeg_reference(epochs_before)
epochs_before.apply_proj()
evoked_before = epochs_before.average()

###############################################################################
# Clean the data using FASTER

# Step 1: mark bad channels
epochs.info['bads'] = find_bad_channels(epochs, eeg_ref_corr=False)
if len(epochs.info['bads']) > 0:
    epochs.interpolate_bads()

# Step 2: mark bad epochs
bad_epochs = find_bad_epochs(epochs)
if len(bad_epochs) > 0:
    epochs.drop(bad_epochs)

# Step 3: mark bad channels for each epoch and interpolate them.
bad_channels_per_epoch = find_bad_channels_in_epochs(epochs, eeg_ref_corr=True)
for i, b in enumerate(bad_channels_per_epoch):
    if len(b) > 0:
        ep = epochs[i]
        ep.info['bads'] = b
        ep.interpolate_bads()
        epochs._data[i, :, :] = ep._data[0, :, :]

# Compute evoked after cleaning, using an average EEG reference
epochs.info['custom_ref_applied'] = False
epochs, _ = io.set_eeg_reference(epochs)
epochs.apply_proj()
evoked_after = epochs.average()

###############################################################################
# Plot the evokeds of the data, before and after cleaning
evoked_before.plot()
evoked_after.plot()
