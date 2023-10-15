import json

import pytest

from opthub_scorer_exe_time_limited_best.exe_time_limited_best import limited_min


@pytest.fixture
def now():
    return json.dumps(
        {"id": 4, "objective": 1.5, "constraint": None, "info": {"exe_time": 1.5, "delays": [0, 0, 0, 0, 0, 0]}}
    )


def test_limited_min_normal_return_min_1(now):
    """
    最小値を返す
    """
    expected = 1.0

    limit = 100
    until = json.dumps(
        [
            {
                "id": 1,
                "objective": 2.0,
                "constraint": None,
                "info": {"exe_time": 2, "delays": [0, 0, 0, 0, 0, 0]},
                "score": 2.0,
            },
            {
                "id": 2,
                "objective": 3.0,
                "constraint": None,
                "info": {"exe_time": 2, "delays": [0, 0, 0, 0, 0, 0]},
                "score": 2.0,
            },
            {
                "id": 3,
                "objective": 1.0,
                "constraint": None,
                "info": {"exe_time": 3, "delays": [0, 0, 0, 0, 0, 0]},
                "score": 1.0,
            },
        ]
    )

    score = limited_min(now, until, limit)
    assert score == expected


def test_limited_min_normal_return_min_2(now):
    """
    最小値を返す
    """
    expected = 1.5

    limit = 100
    until = json.dumps(
        [
            {
                "id": 1,
                "objective": 2.0,
                "constraint": None,
                "info": {"exe_time": 2, "delays": [0, 0, 0, 0, 0, 0]},
                "score": 2.0,
            },
            {
                "id": 2,
                "objective": 3.0,
                "constraint": None,
                "info": {"exe_time": 2, "delays": [0, 0, 0, 0, 0, 0]},
                "score": 2.0,
            },
            {
                "id": 3,
                "objective": 4.0,
                "constraint": None,
                "info": {"exe_time": 3, "delays": [0, 0, 0, 0, 0, 0]},
                "score": 2.0,
            },
        ]
    )

    score = limited_min(now, until, limit)
    assert score == expected


def test_limited_min_normal_return_limited_min_1(now):
    """
    `exe_time`の合計が`limit`以下までの最小値を返す
    """
    expected = 2.0

    limit = 6
    until = json.dumps(
        [
            {
                "id": 1,
                "objective": 2.0,
                "constraint": None,
                "info": {"exe_time": 2, "delays": [0, 0, 0, 0, 0, 0]},
                "score": 2.0,
            },
            {
                "id": 2,
                "objective": 3.0,
                "constraint": None,
                "info": {"exe_time": 2, "delays": [0, 0, 0, 0, 0, 0]},
                "score": 2.0,
            },
            {
                "id": 3,
                "objective": 1.0,
                "constraint": None,
                "info": {"exe_time": 3, "delays": [0, 0, 0, 0, 0, 0]},
                "score": 2.0,
            },
        ]
    )

    score = limited_min(now, until, limit)
    assert score == expected


def test_limited_min_normal_return_limited_min_2(now):
    """
    `exe_time`の合計が`limit`以下までの最小値を返す
    """
    expected = 2.0

    limit = 8
    until = json.dumps(
        [
            {
                "id": 1,
                "objective": 2.0,
                "constraint": None,
                "info": {"exe_time": 2, "delays": [0, 0, 0, 0, 0, 0]},
                "score": 2.0,
            },
            {
                "id": 2,
                "objective": 3.0,
                "constraint": None,
                "info": {"exe_time": 2, "delays": [0, 0, 0, 0, 0, 0]},
                "score": 2.0,
            },
            {
                "id": 3,
                "objective": 4.0,
                "constraint": None,
                "info": {"exe_time": 3, "delays": [0, 0, 0, 0, 0, 0]},
                "score": 2.0,
            },
        ]
    )

    score = limited_min(now, until, limit)
    assert score == expected


def test_limited_min_error_limit_negative(now):
    """
    `limit`は正
    """
    until = json.dumps(
        [
            {
                "id": 1,
                "objective": 2.0,
                "constraint": None,
                "info": {"exe_time": 2, "delays": [0, 0, 0, 0, 0, 0]},
                "score": 2.0,
            },
            {
                "id": 2,
                "objective": 3.0,
                "constraint": None,
                "info": {"exe_time": 2, "delays": [0, 0, 0, 0, 0, 0]},
                "score": 2.0,
            },
            {
                "id": 3,
                "objective": 1.0,
                "constraint": None,
                "info": {"exe_time": 3, "delays": [0, 0, 0, 0, 0, 0]},
                "score": 1.0,
            },
        ]
    )
    with pytest.raises(ValueError):
        limit = -1
        limited_min(now, until, limit)
