# with c2.expander("Download", expanded=False):
#     if len(st.session_state.nodes) >= 1:
#         df_nodes = pd.DataFrame(columns=["node_id", "label", "size", "shape"])
#         for node in st.session_state.nodes:
#             df_nodes = df_nodes.append(
#                 {
#                     "node_id": node.id,
#                     "label": node.label,
#                     "size": node.size,
#                     "shape": node.shape,
#                 },
#                 ignore_index=True,
#             )

#         df_nodes.to_csv(
#             "/home/alixmachard/workspace/dirty/streamlit_app/dataframes/nodes.csv"
#         )

#         with open(
#             "/home/alixmachard/workspace/dirty/streamlit_app/dataframes/nodes.csv"
#         ) as f:
#             st.download_button(
#                 "Download nodes csv", data=f.read(), file_name="nodes.csv"
#             )

#     if len(st.session_state.edges) >= 1:
#         df_edges = pd.DataFrame(columns=["source", "target"])
#         for edge in st.session_state.edges:
#             df_edges = df_edges.append(
#                 {
#                     # "label": edge.label,
#                     "source": edge.source,
#                     "target": edge.to,
#                 },
#                 ignore_index=True,
#             )

#         df_edges.to_csv(
#             "/home/alixmachard/workspace/dirty/streamlit_app/dataframes/edges.csv"
#         )
#         with open(
#             "/home/alixmachard/workspace/dirty/streamlit_app/dataframes/edges.csv"
#         ) as f:
#             st.download_button(
#                 "Download edges csv", data=f.read(), file_name="edges.csv"
#             )
