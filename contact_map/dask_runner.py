"""
Implementation of ContactFrequency parallelization using dask.distributed
"""

from . import frequency_task


def dask_run(trajectory, client, run_info):
    """
    Runs dask version of ContactFrequency. Note that this API on this will
    definitely change before the release.

    Parameters
    ----------
    trajectory : mdtraj.trajectory
    client : dask.distributed.Client
        path to dask scheduler file
    run_info : dict
        keys are 'trajectory_file' (trajectory filename), 'load_kwargs'
        (additional kwargs passed to md.load), and 'parameters' (dict of
        kwargs for the ContactFrequency object)

    Returns
    -------
    :class:`.ContactFrequency` :
        total contact frequency for the trajectory
    """
    slices = frequency_task.default_slices(n_total=len(trajectory),
                                           n_workers=len(client.ncores()))

    subtrajs = client.map(frequency_task.load_trajectory_task, slices,
                          file_name=run_info['trajectory_file'],
                          **run_info['load_kwargs'])
    maps = client.map(frequency_task.map_task, subtrajs,
                      parameters=run_info['parameters'])
    freq = client.submit(frequency_task.reduce_all_results, maps)

    return freq.result()
