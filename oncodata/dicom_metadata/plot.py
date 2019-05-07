"""Helper functions for plotting aspects of DICOM metadata summary."""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

PLOT_REGISTRY = {}

NO_PLOT_ERR = 'Parser {} not in PLOT_REGISTRY! Available plot functions are {}.'

def RegisterPlot(plot_name):
    """Registers a plot function."""

    def decorator(func):
        PLOT_REGISTRY[plot_name] = func
        return func

    return decorator

def get_plot(plot_name):
    if not plot_name in PLOT_REGISTRY:
        raise Exception(
            NO_PLOT_ERR.format(
                plot_name, PLOT_REGISTRY.keys()))

    return PLOT_REGISTRY[plot_name]

@RegisterPlot('dicom_counts')
def plot_dicom_counts(summary, title, save_path):
    """Plots a bar graph of the number of accessions with a given number of DICOMs.

    Arguments:
        summary(dict): A dictionary containing summary statistics
            for DICOM metadata. Must include a 'num_dicoms_to_count'
            key which maps to a dictionary of (number_of_dicoms => count).
        title(str): The title which will be put on the bar graph.
        save_path(str): Path where the bar graph will be saved.
    """

    num_dicoms_to_count_dict = summary['num_dicoms_to_count']
    num_dicoms = sorted(num_dicoms_to_count_dict.keys(), key=lambda num_dicoms: int(num_dicoms))
    counts = [num_dicoms_to_count_dict[num] for num in num_dicoms]
    positions = np.arange(len(num_dicoms))

    plt.bar(positions, counts, tick_label=num_dicoms)
    plt.title(title)
    plt.ylabel('Frequency')
    plt.xlabel('Number of DICOMs')
    plt.xticks(fontsize=5, rotation=90)
    plt.savefig(save_path)

@RegisterPlot('pixel_intensity_relationships')
def plot_pixel_intensity_relationships(summary, title, save_path):
    """Plots a bar graph of the number of DICOMs for each PixelIntensityRelationship.

    Arguments:
        summary(dict): A dictionary containing summary statistics
            for DICOM metadata. Must include a 'pixel_intensity_relationships'
            key which maps to a dictionary of
            (PixelIntensityRelationship => count).
        title(str): The title which will be put on the bar graph.
        save_path(str): Path where the bar graph will be saved.
    """

    PIRs_dict = summary['pixel_intensity_relationships']
    PIRs = sorted(PIRs_dict.keys()) 
    counts = [PIRs_dict[PIR] for PIR in PIRs]
    positions = np.arange(len(PIRs))

    plt.bar(positions, counts, tick_label=PIRs)
    plt.title(title)
    plt.ylabel('Frequency')
    plt.xlabel('Pixel Intensity Relationship')
    plt.savefig(save_path)

@RegisterPlot('years')
def plot_years(summary, title, save_path):
    """Plots a bar graph of the number of DICOMs per year.

    Arguments:
        summary(dict): A dictionary containing summary statistics
            for DICOM metadata. Must include a 'years' key which
            maps to a dictionary of (year => count).
        title(str): The title which will be put on the bar graph.
        save_path(str): Path where the bar graph will be saved.
    """

    years_dict = summary['years']
    years = sorted(years_dict.keys(), key=lambda year: int(year) if year != 'None' else -float('inf'))
    counts = [years_dict[year] for year in years]
    positions = np.arange(len(years))

    plt.bar(positions, counts, tick_label=years)
    plt.title(title)
    plt.ylabel('Frequency')
    plt.xlabel('Year')
    plt.savefig(save_path)
