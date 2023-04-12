import streamlit as st
import streamlit_toggle as tog
from streamlit_agraph import agraph, Node, Edge, Config


def unified_module_name(module_name):
    module_name = module_name.replace("_", " ").lower()
    module_name = module_name[0].upper() + module_name[1:]
    return module_name


def visualize_pipeline(pipeline):

    nodes = []
    edges = []
    logger_nodes = []
    modules = []
    params = []
    stages_ids = dict()

    stages = pipeline.get("stages")

    actions_enabled = pipeline.get("actions_enabled")
    enable_autolog = pipeline.get("enable_autolog")
    enabled = pipeline.get("enabled")
    sealed = pipeline.get("sealed")

    for stage in stages:
        modules.append(stage.get("module").get("name"))
        params.append(stage.get("module").get("parameters"))
        stages_ids[stage.get("id")] = stage.get("stage_before")

    for module, stage_id in zip(modules, list(stages_ids.keys())):
        # if "-0" in stage_id:
        if stages_ids.get(stage_id) is None:
            color = "#DC143C"
        elif "logger" in module.lower() or "logger" in stage_id.lower():
            color = "#000080"
        else:
            color = "#AFEEEE"
        nodes.append(
            Node(
                id=stage_id,
                label=unified_module_name(module),
                size=20,
                shape="hexagon",
                color=color,
            )
        )

    for stage_key, stage_value in zip(
        list(stages_ids.keys()), list(stages_ids.values())
    ):
        if stage_key != "null":
            edges.append(
                Edge(source=stage_value, target=stage_key, color="#000000", size=50)
            )

    config = Config(
        width=1500,
        height=600,
        staticGraph=True,
        staticGraphWithDragAndDrop=True,
        collapsible=True,
    )

    return_value = agraph(
        nodes=nodes,
        edges=edges,
        config=config,
    )

    return params, nodes, return_value
