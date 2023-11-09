""" Test Suite for SPMF Base Class """

from spmf.episode import TKE

def test_read_file() -> None:
    """ Test Read Input File """
    tke = TKE(k=6, max_window=2, timestamp_present=True)
    result = tke.run_file('contextEMMA.txt')
    print(result)
    assert len(result) > 0
