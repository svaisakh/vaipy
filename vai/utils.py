import numpy as np


def remove_outlier(data, threshold=3.5, window_fraction=0.05, return_mask=False):
    """Based on http://www.itl.nist.gov/div898/handbook/eda/section3/eda35h.htm"""

    def __handle_args():
        if threshold < 0:
            raise ValueError('threshold should be non negative but got {}'.format(threshold))
        elif np.isinf(threshold) or np.isnan(threshold):
            raise ValueError('threshold should be a finite number but got {}'.format(threshold))

        if window_fraction < 0 or window_fraction > 1:
            raise ValueError('window_fraction should be a fraction (duh!). But got {}'.format(window_fraction))
        elif np.isinf(window_fraction) or np.isnan(window_fraction):
            raise ValueError('threshold should be a finite number but got {}'.format(threshold))

        if len(data.shape) == 1:
            return remove_outlier(np.expand_dims(data, -1), threshold, window_fraction)

    __handle_args()

    # Subdivide data into small windows
    window_length = int(len(data) * window_fraction)
    divide_ids = np.arange(window_length, len(data), window_length)

    split_data = np.split(data, divide_ids)

    def _remove_outlier(x):
        outlier_factor = 0.6745

        median = np.median(x, axis=0)
        distances = np.linalg.norm(x - median, axis=-1)
        median_deviation = np.median(distances)

        modified_z_scores = outlier_factor * distances / median_deviation

        outlier_mask = modified_z_scores > threshold

        if not return_mask:
            return x[~outlier_mask]

        return x[~outlier_mask], outlier_mask

    if not return_mask:
        return np.vstack([_remove_outlier(d) for d in split_data])

    filtered_data, outliers_mask = [], []

    for d in split_data:
        filtered_d, mask = _remove_outlier(d)
        filtered_data.append(filtered_d)
        outliers_mask.append(mask)

    return np.vstack(filtered_data), np.concatenate(outliers_mask)
