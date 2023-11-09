""" Test Suite for SPMF Base Class """

from spmf.episode import TKE

def test_run_file() -> None:
    """ Test Read Input File """
    tke = TKE(k=6, max_window=2, timestamp_present=True)
    result = tke.run_file('tests\\test_files\\contextEMMA.txt')
    print(result)
    assert len(result) > 0
