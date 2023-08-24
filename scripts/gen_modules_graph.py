# !python
"""
PURPOSE: generate a Python modules graph in JSON to be viewed by
https://github.com/fzaninotto/DependencyWheel

REQUIRES: pip install modulegraph

USAGE: gen_modules_graph.py httpie.core > modules-graph.json

TO RUN:
poetry run python scripts/gen_modules_graph.py flake8_custom_import_rules.flake8_plugin >
modules-graph.json

Taken From:
https://github.com/Lucas-C/dotfiles_and_notes/blob/master/languages/python/gen_modules_graph.py
"""
import json
import sys

from modulegraph.modulegraph import BaseModule
from modulegraph.modulegraph import ModuleGraph


def build_modules_graph(
    path: list[str], entrypoint_modules: list[str]) -> dict:
    """
    Build a module graph based on the provided path and entrypoint modules.

    Parameters
    ----------
    path : list[str]
        The path to the directory containing the modules.
    entrypoint_modules : List[str]
        A list of module names that serve as entry points.

    Raises
    ------
    ValueError
        If the provided module entry points do not share the same root package
        name.

    Returns
    -------
    dict
        A dictionary containing the modules graph matrix and package names.
        - 'matrix' : List[List[int]]
            The adjacency matrix representing the dependencies between modules.
        - 'packageNames' : List[str]
            The names of the packages/modules in the graph, sorted in
            lexicographic order.

    Notes
    -----
    This function builds a graph of module dependencies based on the given path
    and entrypoint modules.
    It uses an adjacency matrix to represent the dependencies between modules.
    The graph is constructed by analyzing the imports in the modules and
    identifying the dependencies.
    Only internal modules (those within the same root package) are considered.
    """

    if len({m.split(".")[0] for m in entrypoint_modules}) != 1:
        raise ValueError("All provided module entry points do not share the same root package name")
    root_pkg = entrypoint_modules[0].split(".")[0]
    mf = ModuleGraph(path, debug=1)
    for mod in entrypoint_modules:
        mf.import_hook(mod)

    packages = {}  # map: name => unique id
    for m in sorted(mf.flatten(), key=lambda n: n.identifier):
        if not isinstance(
            m, BaseModule
        ):  # not a module import, probably a constant or function or C module
            continue
        if not m.identifier.startswith(f"{root_pkg}."):  # keeping only internal modules
            continue
        # module_name = m.identifier.split(".")[-1]
        if m.identifier not in packages:
            packages[m.identifier] = len(packages)

    matrix = _generate_matrix(mf, packages)

    matrix, packages = _update_matrix(matrix, packages)

    return {
        "matrix": matrix,
        "packageNames": [
            p[len(root_pkg) + 1 :] for p in sorted(packages.keys(), key=lambda name: packages[name])
        ],
    }


def _update_matrix(matrix, packages):
    # we remove all packages that have zero deps to & from other ones
    lone_modules_may_exist = True
    while lone_modules_may_exist:
        lone_modules_may_exist = False
        i = 0
        while i < len(matrix):
            n = len(matrix)  # this value will change as the matrix shrinks
            if all(matrix[i][j] == 0 for j in range(n)) and all(
                    matrix[j][i] == 0 for j in range(n)
            ):
                lone_modules_may_exist = True
                packages = {
                    pkg: index if index < i else index - 1
                    for pkg, index in packages.items()
                    if index != i
                }
                matrix = matrix[:i] + matrix[i + 1:]
                for j, row in enumerate(matrix):
                    matrix[j] = row[:i] + row[i + 1:]
            i += 1
    return matrix, packages


def _generate_matrix(mf, packages):
    """
    Generate a matrix based on the given matrix factorization and package
    dictionary

    Notes
    -----
    This function generates a matrix that represents the dependencies between
    packages.
    It iterates over the packages and their IDs, and for each package, it looks
    for outgoing edges in the graph.
    If an outgoing edge points to a different package (not the parent package)
    and that package is in the dictionary,
    it increments the corresponding matrix element.
    The resulting matrix represents the number of dependencies between packages.
    """
    n = len(packages)
    matrix = [[0] * n for _ in range(n)]
    for pkg_name, pkg_id in packages.items():
        parent_pkg = ".".join(pkg_name.split(".")[:-1])
        for outgoing_edge_id in mf.graph.nodes[pkg_name][1]:
            edge_dest_pkg_name = mf.graph.edges[outgoing_edge_id][1]
            if edge_dest_pkg_name != parent_pkg and edge_dest_pkg_name in packages:
                print(
                    f"Module {pkg_name} depends on module {edge_dest_pkg_name}",
                    file=sys.stderr,
                )
                matrix[pkg_id][packages[edge_dest_pkg_name]] += 1
    return matrix


if __name__ == "__main__":
    print(json.dumps(build_modules_graph(["."] + sys.path, sys.argv[1:])))
