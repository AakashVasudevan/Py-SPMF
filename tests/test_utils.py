""" Test utility methods """

import pandas as pd

from spmf.episode import Episode, EpisodeRules


def test_map_episode_pattern() -> None:
    """ Test map pattern method for Episode Mining algorithms """
    episode = Episode()

    mapping1 = {'123': 'a345', '345': 'b456', '456': 'c123', '789': 'd965'}
    pattern1 = '123 345 -> 456 345'

    assert episode.map_pattern(pattern1, mapping1) == 'a345 b456 -> c123 b456'

    mapping2 = {'234': 'FIC104--LO_LO_ALM--15-CRITICAL--COMMON', '145': 'PIC234--LO_ALM--11-HIGH--UTIL'}
    pattern2 = '234 234 -> 234 234 234 -> 145 -> 145'

    assert episode.map_pattern(pattern2, mapping2) == ('FIC104--LO_LO_ALM--15-CRITICAL--COMMON FIC104--LO_LO_ALM--15-CRITICAL--COMMON -> '
                                                       'FIC104--LO_LO_ALM--15-CRITICAL--COMMON FIC104--LO_LO_ALM--15-CRITICAL--COMMON FIC104--LO_LO_ALM--15-CRITICAL--COMMON -> '
                                                       'PIC234--LO_ALM--11-HIGH--UTIL -> PIC234--LO_ALM--11-HIGH--UTIL')


def test_map_episode_rules_pattern() -> None:
    """ Test map pattern method for Episode Rules Mining algorithms """
    episode = EpisodeRules()

    mapping1 = {'123': 'a345', '345': 'b456', '456': 'c123', '789': 'd965'}
    pattern1 = '{123}{345} ==> {456}{345}'

    assert episode.map_pattern(pattern1, mapping1) == '{a345}{b456} ==> {c123}{b456}'

    mapping2 = {'234': 'FIC104--LO_LO_ALM--15-CRITICAL--COMMON', '145': 'PIC234--LO_ALM--11-HIGH--UTIL'}
    pattern2 = '{234 234} ==> {234 234 234} ==> {145} ==> {145}'

    assert episode.map_pattern(pattern2, mapping2) == ('{FIC104--LO_LO_ALM--15-CRITICAL--COMMON FIC104--LO_LO_ALM--15-CRITICAL--COMMON} ==> '
                                                       '{FIC104--LO_LO_ALM--15-CRITICAL--COMMON FIC104--LO_LO_ALM--15-CRITICAL--COMMON FIC104--LO_LO_ALM--15-CRITICAL--COMMON} ==> '
                                                       '{PIC234--LO_ALM--11-HIGH--UTIL} ==> {PIC234--LO_ALM--11-HIGH--UTIL}')
