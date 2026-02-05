"""Test suite for algorithm validation and expansion analysis."""

import logging
from random import randint
from typing import Callable

from . import general as testing


def run_paper_tests(algorithm: Callable[..., str]) -> None:
    """Run tests from the paper examples."""
    for test_case in testing.generatePaperTests():
        output = algorithm(test_case[0])[0][-1]
        solution = test_case[1]
        assert output == solution


def run_edge_cases(algorithm: Callable[..., str]) -> None:
    """Run edge case tests."""
    for test_case in testing.edgeCases():
        output = algorithm(test_case[0])[0][-1]
        solution = test_case[1]
        assert output == solution


def run_repeated_boxes_tests(
    algorithm: Callable[..., str],
    tuples: list[tuple[int, int, int, int]]
) -> None:
    """Run repeated boxes tests."""
    for n, k, m, l in tuples:
        test = testing.repeated_boxes(n, k)
        sol = testing.repeated_boxes_solution(n, k)
        alg_sol = algorithm(test)[0][-1]
        assert alg_sol == sol


def generate_tuples(
    start: int = 2,
    end: int = 15,
    number_of_tuples: int = 6
) -> list[tuple[int, int, int, int]]:
    """Generate random tuples for testing.
    
    Args:
        start: Minimum value for random integers
        end: Maximum value for random integers
        number_of_tuples: Number of tuples to generate
        
    Returns:
        List of tuples containing four random integers
    """
    return [
        (randint(start, end), randint(start, end),
         randint(start, end), randint(start, end))
        for _ in range(number_of_tuples)
    ]


def run_repeated_boxes_single_diamond_tests(
    algorithm: Callable[..., str],
    tuples: list[tuple[int, int, int, int]]
) -> None:
    """Run repeated boxes with single diamond tests."""
    for n, k, m, l in tuples:
        test = testing.single_diamond_repeated_boxes(n, k)
        sol = testing.single_diamond_repeated_boxes_solution(n, k)
        alg_sol = algorithm(test)[0][-1]
        assert sol == alg_sol


def run_repeated_boxes_repeated_diamond_tests(
    algorithm: Callable[..., str],
    tuples: list[tuple[int, int, int, int]]
) -> None:
    """Run repeated boxes with repeated diamond tests."""
    for n, k, m, l in tuples:
        test = testing.repeated_diamonds_and_boxes(n, k, m, l)
        sol = testing.repeated_diamonds_and_boxes_solution(n, k, m, l)
        alg_sol = algorithm(test)[0][-1]

        # In this case, gamma might be in different order, but it is the same.
        # So we just sort before checking
        gamma_algorithm = sorted(alg_sol.split("=>")[0].split(","))
        delta_algorithm = alg_sol.split("=>")[1]
        alg_string_recon = f"{','.join(gamma_algorithm)}=>{delta_algorithm}"

        gamma_sol = sorted(sol.split("=>")[0].split(","))
        delta_sol = sol.split("=>")[1]
        sol_string_recon = f"{','.join(gamma_sol)}=>{delta_sol}"

        assert alg_string_recon == sol_string_recon


def run_tests(algorithm: Callable[..., str]) -> bool:
    """Run all test suites.
    
    Args:
        algorithm: The algorithm to test
        
    Returns:
        True if all tests pass
    """
    run_paper_tests(algorithm)
    run_edge_cases(algorithm)
    tuples = generate_tuples()
    run_repeated_boxes_tests(algorithm, tuples)
    run_repeated_boxes_single_diamond_tests(algorithm, tuples)
    run_repeated_boxes_repeated_diamond_tests(algorithm, tuples)
    print("Passed all tests")
    return True


def test_algorithm_expansion(
    algorithm: Callable[..., str],
    verbose: bool = False
) -> None:
    """Test algorithm node expansion efficiency.
    
    Args:
        algorithm: The algorithm to test
        verbose: If True, print log contents; otherwise print summary
    """
    log_file = "expansion.log"

    logging.basicConfig(
        filename=log_file,
        filemode="w",
        level=logging.INFO,
        format="%(message)s"
    )

    test_configurations = [
        {
            "name": "REPEATED BOXES",
            "test_factory": lambda n, k, m, l: testing.repeated_boxes(n, k),
            "minimum_factory": (
                lambda n, k, m, l: testing.minimum_rules_repeated_boxes(n, k)
            ),
            "params": lambda n, k, m, l: f"n={n}, k={k}"
        },
        {
            "name": "REPEATED BOXES AND SINGLE DIAMOND",
            "test_factory": (
                lambda n, k, m, l: testing.single_diamond_repeated_boxes(n, k)
            ),
            "minimum_factory": (
                lambda n, k, m, l:
                testing.minimum_rules_single_diamond_repeated_boxes(n, k)
            ),
            "params": lambda n, k, m, l: f"n={n}, k={k}"
        },
        {
            "name": "REPEATED BOXES AND REPEATED DIAMOND",
            "test_factory": (
                lambda n, k, m, l:
                testing.repeated_diamonds_and_boxes(n, k, m, l)
            ),
            "minimum_factory": (
                lambda n, k, m, l:
                testing.minimum_rules_repeated_diamond_repeated_boxes(
                    n, k, m, l
                )
            ),
            "params": lambda n, k, m, l: f"n={n}, k={k}, m={m}, l={l}"
        }
    ]

    tuples = generate_tuples(start=2, end=30, number_of_tuples=10)

    for n, k, m, l in tuples:
        for config in test_configurations:
            test = config["test_factory"](n, k, m, l)
            minimum_nodes = config["minimum_factory"](n, k, m, l)
            alg_sol = algorithm(test)

            logging.info(
                f"{config['name']} [{config['params'](n, k, m, l)}]\n"
                f"Nodes expanded: {len(alg_sol[0])}\n"
                f"Nodes added: {alg_sol[3]}\n"
                f"Minimum required: {minimum_nodes}\n"
            )

    if verbose:
        with open(log_file, "r", encoding="utf-8") as f:
            print(f.read(), end="")
    else:
        print("Finished testing")

