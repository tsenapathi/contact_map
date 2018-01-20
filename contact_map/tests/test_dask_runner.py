from .utils import *

from contact_map.dask_runner import *

class TestDaskContactFrequency(object):
    def test_dask_integration(self):
        # this is an integration test to check that dask works
        dask = pytest.importorskip('dask')
        distributed = pytest.importorskip('dask.distributed')

        client = distributed.Client()
        filename = find_testfile("trajectory.pdb")

        dask_freq = DaskContactFrequency(client, filename, cutoff=0.075,
                                         n_neighbors_ignored=0)
        client.close()
        assert dask_freq.n_frames == 5
