import random
import time

from astar import astar
from farm import generate_farm

YIELD_COST = {"high": 0.5, "medium": 1.0, "low": 2.0}
YIELD_SCORE = {"high": 3, "medium": 2, "low": 1}


def unweighted_astar(grid, goal, start):
    """Same as astar.astar but with uniform per-step cost, i.e. classic A*
    with no perception input, used as the baseline a drone would fall back
    to without the ML yield-zone map."""
    return astar(grid, goal, start, yield_zones={})


def path_yield_score(path, yield_zones):
    if not path:
        return 0
    return sum(YIELD_SCORE[yield_zones[cell]] for cell in path)


def run_trial(rows, cols, rng):
    yield_zones = generate_farm(rows, cols)
    grid = [[0] * cols for _ in range(rows)]

    start = (rng.randrange(rows), rng.randrange(cols))
    goal = (rng.randrange(rows), rng.randrange(cols))
    while goal == start:
        goal = (rng.randrange(rows), rng.randrange(cols))

    t0 = time.perf_counter()
    weighted_path = astar(grid, goal, start, yield_zones)
    t1 = time.perf_counter()
    baseline_path = unweighted_astar(grid, goal, start)
    t2 = time.perf_counter()

    return {
        "weighted_ms": (t1 - t0) * 1000,
        "baseline_ms": (t2 - t1) * 1000,
        "weighted_score": path_yield_score(weighted_path, yield_zones),
        "baseline_score": path_yield_score(baseline_path, yield_zones),
        "path_len": len(weighted_path) if weighted_path else 0,
    }


def main():
    rng = random.Random(42)
    grid_sizes = [(20, 20), (40, 40), (80, 80)]
    trials_per_size = 200

    for rows, cols in grid_sizes:
        results = [run_trial(rows, cols, rng) for _ in range(trials_per_size)]
        n = len(results)

        avg_planning_ms = sum(r["weighted_ms"] for r in results) / n
        max_planning_ms = max(r["weighted_ms"] for r in results)

        # % improvement in average yield captured per path cell, weighted vs baseline
        gains = []
        for r in results:
            if r["path_len"] == 0:
                continue
            w = r["weighted_score"] / r["path_len"]
            b = r["baseline_score"] / r["path_len"]
            if b > 0:
                gains.append((w - b) / b * 100)
        avg_gain = sum(gains) / len(gains) if gains else 0.0

        print(f"Grid {rows}x{cols} ({rows*cols} cells), {n} random start/goal trials:")
        print(f"  Planning time: avg {avg_planning_ms:.3f} ms, max {max_planning_ms:.3f} ms")
        print(f"  Avg yield-per-cell gain vs unweighted A*: {avg_gain:+.1f}%")
        print()


if __name__ == "__main__":
    main()
