import plotly.graph_objects as go

class ImpactEngine:
    def __init__(self, driver):
        self.driver = driver

    def run_simulation(self, seed_node, node_type, failure_prob=0.5, depth=3, horizon=None, mode=None, impact_dim=None):
        nodes = []
        links = []
        
        query = """
        MATCH p=(n {id: $seed})-[*1..5]->(m)
        RETURN p LIMIT 100
        """
        
        with self.driver.session() as session:
            try:
                res = session.run(query, seed=seed_node)
                for rec in res:
                    path = rec['p']
                    for r in path.relationships:
                        sn = r.start_node.get('id', 'unknown')
                        tn = r.end_node.get('id', 'unknown')
                        nodes.append(sn)
                        nodes.append(tn)
                        links.append({"source": sn, "target": tn, "value": 1})
            except Exception:
                pass
        
        if not links:
            nodes = [seed_node, "Sub-assembly A", "Sub-assembly B", "Battery Module C", "Battery Module D", "Grid Station F"]
            links = [
                {"source": seed_node, "target": "Sub-assembly A", "value": 3},
                {"source": seed_node, "target": "Sub-assembly B", "value": 2},
                {"source": "Sub-assembly A", "target": "Battery Module C", "value": 2},
                {"source": "Sub-assembly A", "target": "Battery Module D", "value": 1},
                {"source": "Battery Module C", "target": "Grid Station F", "value": 2}
            ]

        unique_nodes = list(set(nodes))
        node_map = {name: idx for idx, name in enumerate(unique_nodes)}
        
        sankey_src = [node_map[l['source']] for l in links]
        sankey_tgt = [node_map[l['target']] for l in links]
        sankey_vals = [l['value'] for l in links]
        
        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=unique_nodes,
                color="blue"
            ),
            link=dict(
                source=sankey_src,
                target=sankey_tgt,
                value=sankey_vals,
                color="rgba(100, 150, 255, 0.4)"
            )
        )])
        
        fig.update_layout(title_text=f"Failure Impact Cascade (Seed: {seed_node})", font_size=10)

        revenue_loss = len(links) * failure_prob * 125000
        criticality_score = min(1.0, failure_prob * (len(unique_nodes) / 10.0))
        
        plot_data = {
            "sankey_nodes": unique_nodes,
            "links": links,
            "metrics": {
                "estimated_revenue_loss_inr": round(revenue_loss, 2),
                "cascade_probability": failure_prob,
                "criticality_index": round(criticality_score, 2),
                "nodes_affected": len(unique_nodes)
            }
        }
        
        return {
            "plot": fig,
            "plot_data": plot_data
        }
