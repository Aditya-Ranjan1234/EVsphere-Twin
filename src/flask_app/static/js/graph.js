// src/flask_app/static/js/graph.js
// Fetch graph data from the API and initialise Cytoscape

document.addEventListener('DOMContentLoaded', function() {
  fetch('/api/graph')
    .then(r => r.json())
    .then(data => {
      const cy = cytoscape({
        container: document.getElementById('cy'),
        elements: {
          nodes: data.nodes,
          edges: data.edges
        },
        style: [
          {
            selector: 'node',
            style: {
              'label': 'data(label)',
              'background-color': '#1f77b4',
              'color': '#fff',
              'text-valign': 'center',
              'text-halign': 'center',
              'font-size': '12px',
              'width': '60px',
              'height': '60px',
              'class': 'cy-node'
            }
          },
          {
            selector: 'edge',
            style: {
              'label': 'data(label)',
              'width': 2,
              'line-color': '#888',
              'target-arrow-color': '#888',
              'target-arrow-shape': 'triangle',
              'curve-style': 'bezier',
              'font-size': '10px',
              'text-rotation': 'autorotate',
              'text-margin-x': 0,
              'text-margin-y': -10,
              'color': '#555'
            }
          }
        ],
        layout: { name: 'cose', animate: true }
      });
    })
    .catch(err => console.error('Graph fetch error', err));
});
