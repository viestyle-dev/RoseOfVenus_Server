from scipy.signal import periodogram


def get_psd_from_time_series(data2nft, SAMPLE_FREQ_VIE=600, FreqStart=4, FreqEnd=40):
    freq_l, spct_l = periodogram(data2nft,
                                 fs=SAMPLE_FREQ_VIE,
                                 window="hamming",
                                 axis=0,
                                 scaling="density",
                                 return_onesided=False,
    )
    idxL = (FreqStart <= freq_l) & (freq_l <= FreqEnd)
    freqL = freq_l[idxL]
    spctL = spct_l[idxL]
    return spctL
