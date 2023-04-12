from streamlit_agraph import agraph, Node, Edge, Config
import streamlit as st
import streamlit_nested_layout
import streamlit_toggle as tog
import pandas as pd
import yaml
import uuid
from utils.modules_manager import (
    TRIGGERS,
    TARGET_GENERATORS,
    TARGET_FILTERS,
    CONVERTERS,
    DATA_GENERATORS,
    ACTIONERS,
)


def get_parameters_from_input(modules_to_target, node_label, param_list):
    for trigger in modules_to_target:
        if list(trigger.keys())[0] == node_label:
            for param in list(trigger.values())[0]:
                if param.get("type") == "str" or param.get("type") == "int":
                    p = st.text_input(param.get("name")) or None
                elif param.get("type") == "bool":
                    p = tog.st_toggle_switch(
                        label=param.get("name"),
                        default_value=False,
                        label_after=True,
                        inactive_color="#D3D3D3",
                        active_color="#11567f",
                        track_color="#29B5E8",
                    )
                param_dict = {"name": param.get("name"), "value": p}
                param_list.append(param_dict)

    return param_list


@st.experimental_memo
def convert_df(df):
    return df.to_csv().encode("utf-8")


def generate_stage_id(list_pos, pipeline_id):
    pipeline_id_splitted = pipeline_id.split("--")
    stage_id = (
        pipeline_id_splitted[0] + f"--stage-{list_pos}--" + pipeline_id_splitted[1]
    )
    return stage_id


def get_pipeline_id_from_name(pipeline_name):
    rand_id = str(uuid.uuid4())[:4]
    # return str(pipeline_name.split(" ")[1:]).replace(" ", "_").lower() + f"--{rand_id}"
    return pipeline_name.lower().replace(" ", "_") + f"--{rand_id}"


def main():
    param_list = []
    nodes_list = []

    if "stages" not in st.session_state:
        st.session_state["stages"] = []

    if "nodes" not in st.session_state:
        st.session_state["nodes"] = []

    if "edges" not in st.session_state:
        st.session_state["edges"] = []

    st.title("📊 Pipeline builder")

    c1, c2 = st.columns([4, 2])
    node_size = c2.slider("Node size", 20, 50, 30)

    with c2.expander("Node label"):
        if st.checkbox("Trigger"):
            node_label = st.selectbox(
                "Trigger",
                options=[list(trigger.keys())[0] for trigger in TRIGGERS],
            )

            param_list = get_parameters_from_input(TRIGGERS, node_label, param_list)

        elif st.checkbox("Target generator"):
            node_label = st.selectbox(
                "Target generator",
                options=[
                    list(target_generators.keys())[0]
                    for target_generators in TARGET_GENERATORS
                ],
            )
            param_list = get_parameters_from_input(
                TARGET_GENERATORS, node_label, param_list
            )

        elif st.checkbox("Converter"):
            node_label = st.selectbox(
                "Converter",
                options=[list(converter.keys())[0] for converter in CONVERTERS],
            )
            param_list = get_parameters_from_input(CONVERTERS, node_label, param_list)

        elif st.checkbox("Target filter"):
            node_label = st.selectbox(
                "Target filter",
                options=[
                    list(target_filter.keys())[0] for target_filter in TARGET_FILTERS
                ],
            )
            param_list = get_parameters_from_input(
                TARGET_FILTERS, node_label, param_list
            )

        elif st.checkbox("Data generator"):
            node_label = st.selectbox(
                "Data generator",
                options=[
                    list(data_generator.keys())[0] for data_generator in DATA_GENERATORS
                ],
            )
            param_list = get_parameters_from_input(
                DATA_GENERATORS, node_label, param_list
            )
        elif st.checkbox("Actioner"):
            node_label = st.selectbox(
                "Actioner",
                options=[list(actioner.keys())[0] for actioner in ACTIONERS],
            )
            param_list = get_parameters_from_input(ACTIONERS, node_label, param_list)
    config = Config(
        width=1000,
        height=600,
    )

    col1, col2 = c2.columns([2, 2])

    if col1.button("Add node"):
        if len(st.session_state.nodes) == 0:
            color = "#DC143C"
        else:
            color = "#AFEEEE"
        try:
            st.session_state.nodes.append(
                {
                    Node(
                        id=node_label,
                        label=node_label,
                        size=node_size,
                        shape="hexagon",
                        color=color,
                    ): param_list
                }
            )
            with c1:
                return_value = agraph(
                    nodes=[node for n in st.session_state.nodes for node in n.keys()],
                    edges=st.session_state.edges,
                    config=config,
                )
        except:
            st.write("💔 Something went wrong, please select a node to add...")

    if len(st.session_state.nodes) >= 2:

        edge_source = (
            c2.selectbox(
                "Source",
                options=[
                    node.label for n in st.session_state.nodes for node in n.keys()
                ],
                index=1,
            ),
        )
        edge_target = (
            c2.selectbox(
                "Target",
                options=[
                    node.label for n in st.session_state.nodes for node in n.keys()
                ],
                index=1,
            ),
        )

        if c2.button("Add edge"):
            st.session_state.edges.append(
                Edge(
                    source=edge_source[0],
                    # label="friend_of",
                    target=edge_target[0],
                    color="#000000",
                )
            )
            with c1:
                return_value = agraph(
                    nodes=[node for n in st.session_state.nodes for node in n.keys()],
                    edges=st.session_state.edges,
                    config=config,
                )

    with c2.expander("Remove", expanded=False):
        if st.button("Remove last node"):
            if len(st.session_state.nodes) >= 1:
                del st.session_state.nodes[-1]
                st.write("❌ Last node has been removed")
            else:
                st.write("❌ Can not remove element from empty list")
        if st.button("Remove last edge"):
            if len(st.session_state.edges) >= 1:
                del st.session_state.edges[-1]
                st.write("❌ Last edge has been removed")
            else:
                st.write("❌ Can not remove element from empty list")

        if st.button("Remove all"):
            # if len(st.session_state.nodes) >= 1:
            st.session_state.nodes = []
            st.session_state.edges = []
            st.session_state.stages = []

            st.write("❌ Graph has been removed")

    with st.expander("✨ Export to yaml"):
        pipeline_template = dict()

        if len(st.session_state.nodes) > 0 or len(st.session_state.edges) > 0:
            name = st.text_input("Pipeline name") or "pipeline"

            if st.button("Generate pipeline"):
                actions_enabled = tog.st_toggle_switch(
                    label="Actions enabled",
                    default_value=False,
                    label_after=True,
                    inactive_color="#D3D3D3",
                    active_color="#11567f",
                    track_color="#29B5E8",
                )
                enabled = tog.st_toggle_switch(
                    label="Enabled",
                    default_value=False,
                    label_after=True,
                    inactive_color="#D3D3D3",
                    active_color="#11567f",
                    track_color="#29B5E8",
                )
                sealed = tog.st_toggle_switch(
                    label="Sealed",
                    default_value=False,
                    label_after=True,
                    inactive_color="#D3D3D3",
                    active_color="#11567f",
                    track_color="#29B5E8",
                )

                pipeline_template["actions_enabled"] = actions_enabled
                pipeline_template["enable_autolog"] = True
                pipeline_template["enabled"] = enabled
                pipeline_template["migration_version"] = None
                pipeline_template["name"] = name
                pipeline_template["sealed"] = sealed

                pipeline_id = get_pipeline_id_from_name(name)
                pipeline_template["id"] = pipeline_id

                for node in st.session_state.nodes:
                    for key in node.keys():
                        nodes_list.append(key)

                for n in nodes_list:

                    module_dict = dict()
                    stages_dict = dict()

                    module_dict["name"] = n.label
                    for session_node in st.session_state.nodes:
                        for key in session_node.keys():
                            if key.label == n.label:
                                for value_list in session_node.values():
                                    module_dict["parameters"] = value_list

                    stage_id = generate_stage_id(
                        len(st.session_state.stages), pipeline_template["id"]
                    )

                    stages_dict["id"] = stage_id
                    stages_dict["module"] = module_dict
                    stages_dict["stage_before"] = None

                    st.session_state.stages.append(stages_dict)

                pipeline_template["stages"] = st.session_state.stages

                for e in st.session_state.edges:
                    for s in pipeline_template["stages"]:
                        if s.get("module").get("name") == e.source:
                            stage_before_id = s["id"]
                        if s.get("module").get("name") == e.to:
                            s["stage_before"] = stage_before_id

                            print(s)
                print("final pipe: ", pipeline_template)
                clicked = True
                clicked = st.download_button(
                    "Save pipeline to yaml",
                    data=yaml.dump(pipeline_template),
                    file_name=f"{name}.yaml",
                )
                if not clicked:
                    st.session_state.stages = []
                    del pipeline_template

    if c2.button("Reload graph"):
        with c1:
            return_value = agraph(
                nodes=[node for n in st.session_state.nodes for node in n.keys()],
                edges=st.session_state.edges,
                config=config,
            )


if __name__ == "__main__":
    main()
