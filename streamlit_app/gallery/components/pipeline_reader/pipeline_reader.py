from streamlit_agraph import agraph, Node, Edge, Config
import streamlit_toggle as tog
import streamlit as st
import streamlit_nested_layout
import yaml


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

    with st.expander("Pipeline information"):
        actions_toggle = tog.st_toggle_switch(
            label="Actions enabled",
            default_value=actions_enabled,
            label_after=True,
            inactive_color="#D3D3D3",
            active_color="#11567f",
            track_color="#29B5E8",
        )
        autolog_toggle = tog.st_toggle_switch(
            label="Autolog enabled",
            default_value=enable_autolog,
            label_after=True,
            inactive_color="#D3D3D3",
            active_color="#11567f",
            track_color="#29B5E8",
        )
        enabled_toggle = tog.st_toggle_switch(
            label="Enabled",
            default_value=enabled,
            label_after=True,
            inactive_color="#D3D3D3",
            active_color="#11567f",
            track_color="#29B5E8",
        )
        sealed_toggle = tog.st_toggle_switch(
            label="Sealed",
            default_value=sealed,
            label_after=True,
            inactive_color="#D3D3D3",
            active_color="#11567f",
            track_color="#29B5E8",
        )
        # To be done....
        # if st.button("Update pipeline"):
        #     pipeline["actions_enabled"] = actions_enabled
        #     pipeline.get["enable_autolog"] = autolog_toggle
        #     pipeline.get["enabled"] = enabled_toggle
        #     pipeline.get["sealed"] = sealed_toggle

    with st.expander("Module parameters"):
        for param, node in zip(params, nodes):
            if node.id == return_value:
                if param != []:
                    st.markdown(f"**{node.label}**")
                    st.write([{p.get("name"): p.get("value")} for p in param])
                else:
                    st.markdown(f"💔 **{node.label}** has no parameter")


def main():

    st.title("📊 Pipeline Reader")

    uploaded_file = st.file_uploader(" ")

    if uploaded_file is not None:
        try:
            pipeline = yaml.safe_load(uploaded_file)

            visualize_pipeline(pipeline)
        except yaml.YAMLError as exc:
            print(exc)
    else:
        text = st.text_area("Enter yaml pipeline to visualize")
        try:
            # if text is not None:
            pipeline = yaml.safe_load(text)
            visualize_pipeline(pipeline)
        # st.write(pipeline)
        except:
            st.write("💔 No pipeline to display")


if __name__ == "__main__":
    main()
