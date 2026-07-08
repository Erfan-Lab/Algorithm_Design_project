import math
import os
import tempfile

import find_shortest_path as fsp

##TEST_FILE = "map1.txt"
##TEST_FILE = "map2.txt"
##TEST_FILE = "map3.txt"
##TEST_FILE = "map4.txt"
##TEST_FILE = "map5.txt"
TEST_FILE = "map6.txt"


# --------------------------------------------------------------------------- #
# Reading test.txt
# --------------------------------------------------------------------------- #
def read_test_file(path):
    """Split test.txt into map lines (V/E) and the request line.

    Returns:
        (map_lines, request_tokens). request_tokens is None if no REQUEST found.
    """
    map_lines = []
    request = None
    with open(path, "r") as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            tag = line.split()[0].upper()
            if tag in ("V", "E"):
                map_lines.append(line)
            elif tag == "REQUEST":
                request = line.split()[1:]
    return map_lines, request


def build_graph_from_lines(map_lines):
    """Write the map lines to a temp file and build the graph via build_graph."""
    fd, tmp = tempfile.mkstemp(suffix=".txt")
    with os.fdopen(fd, "w") as f:
        f.write("\n".join(map_lines) + "\n")
    graph = fsp.build_graph(tmp)
    os.remove(tmp)
    return graph


# --------------------------------------------------------------------------- #
# Output formatting
# --------------------------------------------------------------------------- #
def fmt_cost(cost):
    """Format a cost value nicely (drop trailing .0 for whole numbers)."""
    if cost == math.inf:
        return "inf"
    if float(cost).is_integer():
        return str(int(cost))
    return f"{cost:.3f}"


def print_header(map_lines):
    """Print the report header and echo the input map."""
    line = "=" * 66
    print(line)
    print(" SMART URBAN ROUTING - result")
    print(line)
    print("Input map:")
    for row in map_lines:
        print(f"    {row}")
    print()


def run_single(graph, algorithm, source, target):
    """Run and print a single source -> target request."""
    path, cost = fsp.find_optimal_shortest_path(graph, source, target)
    print(f"Algorithm : {algorithm}")
    print(f"Request   : single  ({source} -> {target})")
    if path is None:
        print("Result    : -")
        print("Status    : NEGATIVE CYCLE FOUND")
    elif not path:
        print("Result    : (no path)")
        print("Status    : UNREACHABLE")
    else:
        print(f"Result    : {' -> '.join(path)}")
        print(f"Cost      : {fmt_cost(cost)}")
        print("Status    : OK")


def run_multi(graph, algorithm, source, destinations):
    """Run and print a multi-destination request."""
    order, total, segments = fsp.multiple_destinations_shortest_path(
        graph, source, destinations
    )
    print(f"Algorithm    : {algorithm}")
    print(f"Request      : multi  (start {source}, visit {', '.join(destinations)})")
    if order is None and total == 0:
        print("Status       : NEGATIVE CYCLE FOUND")
    elif order is None:
        print("Status       : UNREACHABLE")
    else:
        print(f"Visit order  : {' -> '.join(order)}")
        print(f"Total cost   : {fmt_cost(total)}")
        print("Segments     :")
        for seg in segments:
            print(f"    {' -> '.join(seg)}")
        print("Status       : OK")





def main():
    map_lines, request = read_test_file(TEST_FILE)

    if request is None:
        print(f"No REQUEST line found in {TEST_FILE}.")
        return

    graph = build_graph_from_lines(map_lines)
    if graph is None:
        print(f"Could not build the graph from {TEST_FILE} (malformed map).")
        return

    print_header(map_lines)
    algorithm = "Bellman-Ford" if graph.has_negative_edge else "Dijkstra"
    mode = request[0].lower()

    if mode == "single":
        run_single(graph, algorithm, request[1], request[2])
    elif mode == "multi":
        run_multi(graph, algorithm, request[1], request[2:])
    else:
        print(f"Unknown request mode: {request[0]!r} (use 'single' or 'multi').")


if __name__ == "__main__":
    main()
