from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Render the main dashboard page."""
    # Sample data for Plotly chart – a simple line
    plot_data = {
        "x": [1, 2, 3, 4, 5],
        "y": [10, 15, 13, 17, 22]
    }
    return render_template('index.html', plot_data=plot_data)

@main_bp.route('/graph')
def graph():
    """Render a Cytoscape graph visualization of the digital twin."""
    # Example graph data – nodes and edges
    nodes = [
        {"data": {"id": "vehicle", "label": "Vehicle"}},
        {"data": {"id": "charger", "label": "Charger"}},
        {"data": {"id": "supplier", "label": "Supplier"}}
    ]
    edges = [
        {"data": {"source": "vehicle", "target": "charger", "label": "charges"}},
        {"data": {"source": "charger", "target": "supplier", "label": "supplied_by"}}
    ]
    return render_template('graph.html', nodes=nodes, edges=edges)

@main_bp.route('/map')
def view_map():
    return render_template('map.html')

@main_bp.route('/predict')
def view_predict():
    return render_template('predict.html')

@main_bp.route('/upload')
def view_upload():
    return render_template('upload.html')

@main_bp.route('/digital-twin')
def view_digital_twin():
    return render_template('digital_twin.html')
