"""Plots a bar graph of the number of DICOMs per year."""

import argparse
import json
from os.path import dirname, realpath
import sys
sys.path.append(dirname(dirname(dirname(realpath(__file__)))))

from oncodata.dicom_metadata.plot import PLOT_REGISTRY, get_plot

def main(summary_path, plot_type, title, save_path):
    """Plots a bar graph of the number of DICOMs per year.

    Arguments:
        summary_path(str): Path to a summary statistics JSON
            as produced by dicom_metadata_summary.py.
        title(str): The title which will be put on the bar graph.
        save_path(str): Path where the bar graph will be saved.
    """

    with open(summary_path, 'r') as summary_file:
        summary = json.load(summary_file)

    plot_func = get_plot(plot_type)
    plot_func(summary, title, save_path)

if __name__ == '__main__':
    plot_types = sorted(list(PLOT_REGISTRY.keys()))

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--summary_path',
        type=str,
        required=True,
        help='Path to a JSON file with summary statistics.')
    parser.add_argument(
        '--plot_type',
        type=str,
        required=True,
        help='The type of plot function to use. Available plot functions are: {}.'.format(plot_types))
    parser.add_argument(
        '--title',
        type=str,
        required=True,
        help='Title of the bar graph.')
    parser.add_argument(
        '--save_path',
        type=str,
        required=True,
        help='Path where the graph will be saved.')
    args = parser.parse_args()

    main(args.summary_path, args.plot_type, args.title, args.save_path)
