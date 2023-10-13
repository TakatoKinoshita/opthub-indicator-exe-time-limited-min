import json

import pytest

from opthub_scorer_exe_time_limited_best.exe_time_limited_best import limited_best


@pytest.fixture
def normal_solution_to_score_1():
    return json.dumps(
        {"id": 4, "objective": 1.5, "constraint": None, "info": {"exe_time": 1.5, "delays": [0, 0, 0, 0, 0, 0]}}
    )


@pytest.fixture
def normal_solutions_scored_1():
    return json.dumps(
        [
            {"id": 1, "objective": 2.0, "constraint": None, "info": {"exe_time": 2, "delays": [0, 0, 0, 0, 0, 0]}},
            {"id": 2, "objective": 3.0, "constraint": None, "info": {"exe_time": 2, "delays": [0, 0, 0, 0, 0, 0]}},
            {"id": 3, "objective": 1.0, "constraint": None, "info": {"exe_time": 3, "delays": [0, 0, 0, 0, 0, 0]}},
        ]
    )


@pytest.fixture
def normal_solutions_scored_2():
    return json.dumps(
        [
            {"id": 1, "objective": 2.0, "constraint": None, "info": {"exe_time": 2, "delays": [0, 0, 0, 0, 0, 0]}},
            {"id": 2, "objective": 3.0, "constraint": None, "info": {"exe_time": 2, "delays": [0, 0, 0, 0, 0, 0]}},
            {"id": 3, "objective": 4.0, "constraint": None, "info": {"exe_time": 3, "delays": [0, 0, 0, 0, 0, 0]}},
        ]
    )


def test_limited_best_normal_return_min_1(normal_solution_to_score_1, normal_solutions_scored_1):
    """
    最小値を返す
    """
    expected = 1.0

    limit = 100
    score = limited_best(normal_solution_to_score_1, normal_solutions_scored_1, limit)
    assert score == expected


def test_limited_best_normal_return_min_2(normal_solution_to_score_1, normal_solutions_scored_2):
    """
    最小値を返す
    """
    expected = 1.5

    limit = 100
    score = limited_best(normal_solution_to_score_1, normal_solutions_scored_2, limit)
    assert score == expected


def test_limited_best_normal_return_limited_min_1(normal_solution_to_score_1, normal_solutions_scored_2):
    """
    `exe_time`の合計が`limit`以下までの最小値を返す
    """
    expected = 2.0

    limit = 8
    score = limited_best(normal_solution_to_score_1, normal_solutions_scored_2, limit)
    assert score == expected


def test_limited_best_normal_return_limited_min_2(normal_solution_to_score_1, normal_solutions_scored_2):
    """
    `exe_time`の合計が`limit`以下までの最小値を返す
    """
    expected = 2.0

    limit = 6
    score = limited_best(normal_solution_to_score_1, normal_solutions_scored_2, limit)
    assert score == expected


def test_limited_best_error_limit_negative(normal_solution_to_score_1, normal_solutions_scored_1):
    """
    `limit`は正
    """
    with pytest.raises(ValueError):
        limit = -1
        limited_best(normal_solution_to_score_1, normal_solutions_scored_1, limit)
