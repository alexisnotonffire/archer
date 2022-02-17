from platform import architecture
from pydoc import doc
from yaml import load, Loader
from diagrams import Diagram, Cluster, Edge
from importlib import import_module

with open("example.yaml", "rb") as f:
    document = load(f, Loader)

nodes = {}

def _itergroups(groups):
    for group in groups:
        with Cluster(group["name"]):
            components = group.get("components", [])
            for component in components:
                path = f"diagrams.{component['resource']}".split(".")
                resource = (".".join(path[:-1]), path[-1])
                component_type = getattr(import_module(resource[0]), resource[1])
                nodes[component["name"]] = component_type(component["name"])


with Diagram(document["title"], show=False):
    architecture = document["architecture"]
    for network in architecture:
        with Cluster(network["name"]):
            _itergroups(network.get("logical-groups", []))
            _itergroups(network.get("physical-groups", []))

    connections = document["connections"]
    for connection in connections:
        src = connection.pop("from")
        tgt = connection.pop("to")
        nodes[src] >> Edge(**connection) >> nodes[tgt]

            

        