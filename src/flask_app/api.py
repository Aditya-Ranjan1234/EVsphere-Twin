from flask import Blueprint, jsonify, request, send_file, current_app
import io
import json
import pandas as pd
from ..graph.db import driver
from ..graph.impact_engine import ImpactEngine

api_bp = Blueprint('api', __name__)

# ── Rich demo data (used when Neo4j has no data) ────────────────────────────
DEMO_NODES = [
    {"data": {"id": "SUP_001", "label": "Tata Supplier",       "type": "Supplier"}},
    {"data": {"id": "SUP_002", "label": "LG Chem Supplier",    "type": "Supplier"}},
    {"data": {"id": "SUP_003", "label": "CATL Supplier",       "type": "Supplier"}},
    {"data": {"id": "BAT_001", "label": "LFP Battery Pack A",  "type": "Battery"}},
    {"data": {"id": "BAT_002", "label": "NMC Battery Pack B",  "type": "Battery"}},
    {"data": {"id": "BAT_003", "label": "Solid‑State Cell C",  "type": "Battery"}},
    {"data": {"id": "VEH_001", "label": "Nexon EV Fleet",      "type": "Vehicle"}},
    {"data": {"id": "VEH_002", "label": "Tigor EV Fleet",      "type": "Vehicle"}},
    {"data": {"id": "VEH_003", "label": "Punch EV Fleet",      "type": "Vehicle"}},
    {"data": {"id": "CHG_001", "label": "Mumbai Fast Charger",  "type": "Charger"}},
    {"data": {"id": "CHG_002", "label": "Pune DC Charger",     "type": "Charger"}},
    {"data": {"id": "CHG_003", "label": "Delhi Hub Charger",   "type": "Charger"}},
    {"data": {"id": "CHG_004", "label": "Bengaluru AC Charger","type": "Charger"}},
    {"data": {"id": "SVC_001", "label": "Service Centre MH",   "type": "ServiceCenter"}},
    {"data": {"id": "SVC_002", "label": "Service Centre KA",   "type": "ServiceCenter"}},
    {"data": {"id": "SVC_003", "label": "Service Centre DL",   "type": "ServiceCenter"}},
]

DEMO_EDGES = [
    # Suppliers → Batteries
    {"data": {"source": "SUP_001", "target": "BAT_001", "label": "SUPPLIES"}},
    {"data": {"source": "SUP_002", "target": "BAT_002", "label": "SUPPLIES"}},
    {"data": {"source": "SUP_003", "target": "BAT_003", "label": "SUPPLIES"}},
    # Batteries → Vehicles
    {"data": {"source": "BAT_001", "target": "VEH_001", "label": "POWERS"}},
    {"data": {"source": "BAT_002", "target": "VEH_002", "label": "POWERS"}},
    {"data": {"source": "BAT_003", "target": "VEH_003", "label": "POWERS"}},
    {"data": {"source": "BAT_001", "target": "VEH_003", "label": "POWERS"}},
    # Vehicles → Chargers
    {"data": {"source": "VEH_001", "target": "CHG_001", "label": "CHARGES_AT"}},
    {"data": {"source": "VEH_001", "target": "CHG_002", "label": "CHARGES_AT"}},
    {"data": {"source": "VEH_002", "target": "CHG_003", "label": "CHARGES_AT"}},
    {"data": {"source": "VEH_003", "target": "CHG_004", "label": "CHARGES_AT"}},
    # Vehicles → Service Centres
    {"data": {"source": "VEH_001", "target": "SVC_001", "label": "MAINTAINED_BY"}},
    {"data": {"source": "VEH_002", "target": "SVC_002", "label": "MAINTAINED_BY"}},
    {"data": {"source": "VEH_003", "target": "SVC_003", "label": "MAINTAINED_BY"}},
    # Supplier cross
    {"data": {"source": "SUP_001", "target": "BAT_002", "label": "SUPPLIES"}},
]

DEMO_GEOJSON_FEATURES = [
    {"type":"Feature","properties":{"name":"Mumbai Fast Charger","type":"Charger","status":"Online"},
     "geometry":{"type":"Point","coordinates":[72.8777,19.0760]}},
    {"type":"Feature","properties":{"name":"Pune DC Charger","type":"Charger","status":"Online"},
     "geometry":{"type":"Point","coordinates":[73.8567,18.5204]}},
    {"type":"Feature","properties":{"name":"Delhi Hub Charger","type":"Charger","status":"Busy"},
     "geometry":{"type":"Point","coordinates":[77.2090,28.6139]}},
    {"type":"Feature","properties":{"name":"Bengaluru AC Charger","type":"Charger","status":"Online"},
     "geometry":{"type":"Point","coordinates":[77.5946,12.9716]}},
    {"type":"Feature","properties":{"name":"Hyderabad Charger","type":"Charger","status":"Maintenance"},
     "geometry":{"type":"Point","coordinates":[78.4867,17.3850]}},
    {"type":"Feature","properties":{"name":"Tata Motors Factory Pune","type":"Supplier","status":"Active"},
     "geometry":{"type":"Point","coordinates":[73.7898,18.6298]}},
    {"type":"Feature","properties":{"name":"LG Chem Battery Plant GJ","type":"Supplier","status":"Active"},
     "geometry":{"type":"Point","coordinates":[72.6369,23.0225]}},
    {"type":"Feature","properties":{"name":"CATL Cell Facility KA","type":"Supplier","status":"Active"},
     "geometry":{"type":"Point","coordinates":[77.1025,13.3379]}},
    {"type":"Feature","properties":{"name":"Service Centre Mumbai","type":"ServiceCenter","status":"Open"},
     "geometry":{"type":"Point","coordinates":[72.9500,19.1200]}},
    {"type":"Feature","properties":{"name":"Service Centre Bengaluru","type":"ServiceCenter","status":"Open"},
     "geometry":{"type":"Point","coordinates":[77.6200,12.9500]}},
    {"type":"Feature","properties":{"name":"Service Centre Delhi","type":"ServiceCenter","status":"Open"},
     "geometry":{"type":"Point","coordinates":[77.3500,28.5500]}},
    {"type":"Feature","properties":{"name":"Nexon EV Hub Mumbai","type":"Vehicle","status":"Active"},
     "geometry":{"type":"Point","coordinates":[72.8600,19.1000]}},
    {"type":"Feature","properties":{"name":"Tigor EV Hub Chennai","type":"Vehicle","status":"Active"},
     "geometry":{"type":"Point","coordinates":[80.2707,13.0827]}},
    {"type":"Feature","properties":{"name":"Battery Research Facility Pune","type":"Battery","status":"Active"},
     "geometry":{"type":"Point","coordinates":[73.8600,18.5600]}},
]


def _serialize_node(n):
    """Convert a Neo4j node to Cytoscape element format."""
    try:
        labels = list(n.labels)
        node_type = labels[0] if labels else 'Unknown'
        node_id   = str(n.get('id') or n.get('name') or n.element_id)
        node_label = str(n.get('name') or n.get('id') or node_id)
        return {"data": {"id": node_id, "label": node_label, "type": node_type}}
    except Exception:
        return None


def _serialize_edge(r):
    """Convert a Neo4j relationship to Cytoscape element format."""
    try:
        src_id = str(r.start_node.get('id') or r.start_node.get('name') or r.start_node.element_id)
        tgt_id = str(r.end_node.get('id')   or r.end_node.get('name')   or r.end_node.element_id)
        return {"data": {"source": src_id, "target": tgt_id, "label": r.type}}
    except Exception:
        return None


# ── /api/graph ───────────────────────────────────────────────────────────────
@api_bp.route('/api/graph')
def api_graph():
    nodes, edges = [], []
    seen_nodes, seen_edges = set(), set()

    try:
        with driver.session() as session:
            result = session.run("MATCH (n)-[r]->(m) RETURN n, r, m LIMIT 500")
            for rec in result:
                n = rec.get('n')
                r = rec.get('r')
                m = rec.get('m')
                if n:
                    nd = _serialize_node(n)
                    if nd and nd['data']['id'] not in seen_nodes:
                        nodes.append(nd)
                        seen_nodes.add(nd['data']['id'])
                if m:
                    md = _serialize_node(m)
                    if md and md['data']['id'] not in seen_nodes:
                        nodes.append(md)
                        seen_nodes.add(md['data']['id'])
                if r:
                    ed = _serialize_edge(r)
                    if ed:
                        ekey = (ed['data']['source'], ed['data']['target'], ed['data']['label'])
                        if ekey not in seen_edges:
                            edges.append(ed)
                            seen_edges.add(ekey)
    except Exception as exc:
        current_app.logger.warning(f"Neo4j graph query failed: {exc}")

    # Fallback to demo data when DB is empty or unreachable
    if not nodes:
        nodes = DEMO_NODES
        edges = DEMO_EDGES

    return jsonify({"nodes": nodes, "edges": edges})


# ── /api/map ─────────────────────────────────────────────────────────────────
@api_bp.route('/api/map')
def api_map():
    features = []
    try:
        with driver.session() as session:
            result = session.run(
                "MATCH (n) WHERE n.lat IS NOT NULL AND n.lng IS NOT NULL "
                "RETURN n LIMIT 200"
            )
            for rec in result:
                n = rec['n']
                labels = list(n.labels)
                node_type = labels[0] if labels else 'Unknown'
                features.append({
                    "type": "Feature",
                    "properties": {
                        "name": n.get('name') or n.get('id') or 'Node',
                        "type": node_type,
                        "status": n.get('status', '')
                    },
                    "geometry": {
                        "type": "Point",
                        "coordinates": [float(n['lng']), float(n['lat'])]
                    }
                })
    except Exception as exc:
        current_app.logger.warning(f"Neo4j map query failed: {exc}")

    if not features:
        features = DEMO_GEOJSON_FEATURES

    return jsonify({"type": "FeatureCollection", "features": features})


# ── /api/predict ─────────────────────────────────────────────────────────────
@api_bp.route('/api/predict', methods=['POST'])
def api_predict():
    payload = request.get_json() or {}
    engine  = ImpactEngine(driver)
    result  = engine.run_simulation(
        seed_node    = payload.get('seed_node', 'SUP_001'),
        node_type    = payload.get('node_type', 'Supplier'),
        failure_prob = float(payload.get('failure_prob', 0.5)),
        depth        = int(payload.get('depth', 3)),
        horizon      = payload.get('time_horizon'),
        mode         = payload.get('simulation_mode'),
        impact_dim   = payload.get('impact_dimension')
    )
    return jsonify({"plot_data": result['plot_data']})


# ── /api/upload ──────────────────────────────────────────────────────────────
@api_bp.route('/api/upload', methods=['POST'])
def api_upload():
    file = request.files.get('file')
    if not file:
        return jsonify({"error": "No file provided"}), 400
    import os
    dest = os.path.join(current_app.root_path, '..', '..', 'data', 'raw', file.filename)
    dest = os.path.normpath(dest)
    file.save(dest)
    return jsonify({"status": "uploaded", "filename": file.filename})


# ── /api/export/<fmt> ────────────────────────────────────────────────────────
@api_bp.route('/api/export/<fmt>')
def api_export(fmt):
    if fmt == 'json':
        data = api_graph().get_json()
        return jsonify(data)

    elif fmt == 'csv':
        data   = api_graph().get_json()
        nodes  = data.get('nodes', [])
        output = io.StringIO()
        output.write("id,label,type\n")
        for n in nodes:
            d = n['data']
            output.write(f"{d.get('id','')},{d.get('label','')},{d.get('type','')}\n")
        output.seek(0)
        return send_file(
            io.BytesIO(output.read().encode()),
            mimetype='text/csv',
            as_attachment=True,
            download_name='graph_nodes.csv'
        )

    elif fmt == 'graphml':
        try:
            import networkx as nx
            data  = api_graph().get_json()
            G     = nx.DiGraph()
            for n in data.get('nodes', []):
                d = n['data']
                G.add_node(d['id'], label=d.get('label',''), type=d.get('type',''))
            for e in data.get('edges', []):
                d = e['data']
                G.add_edge(d['source'], d['target'], label=d.get('label',''))
            out = io.BytesIO()
            nx.write_graphml(G, out)
            out.seek(0)
            return send_file(out, mimetype='application/xml', as_attachment=True, download_name='graph.graphml')
        except Exception as ex:
            return jsonify({"error": str(ex)}), 500

    elif fmt == 'cypher':
        data  = api_graph().get_json()
        stmts = []
        for n in data.get('nodes', []):
            d = n['data']
            stmts.append(f"MERGE (n:{d.get('type','Node')} {{id: '{d.get('id')}', name: '{d.get('label')}'}});")
        for e in data.get('edges', []):
            d = e['data']
            stmts.append(
                f"MATCH (a {{id: '{d['source']}'}}), (b {{id: '{d['target']}'}}) "
                f"MERGE (a)-[:{d.get('label','REL')}]->(b);"
            )
        cypher_txt = '\n'.join(stmts)
        return send_file(
            io.BytesIO(cypher_txt.encode()),
            mimetype='text/plain',
            as_attachment=True,
            download_name='graph.cypher'
        )

    else:
        return jsonify({"error": f"Unsupported format: {fmt}"}), 400
