document.addEventListener("DOMContentLoaded", function() {
    const feed = document.getElementById("risk-feed");
    const triggerBtn = document.getElementById("btn-trigger");
    const cyContainer = document.getElementById("cy-viewport");
    let cy;

    // Load initial topology from /api/graph
    if (cyContainer) {
        fetch('/api/graph')
            .then(res => res.json())
            .then(data => {
                // Dynamically populate drop-down selector
                const seedSelector = document.getElementById("control-seed");
                if (seedSelector && data.nodes) {
                    seedSelector.innerHTML = "";
                    data.nodes.forEach(n => {
                        const opt = document.createElement("option");
                        opt.value = n.data.id;
                        opt.innerText = n.data.label;
                        seedSelector.appendChild(opt);
                    });
                }

                cy = cytoscape({
                    container: cyContainer,
                    elements: {
                        nodes: data.nodes || [],
                        edges: data.edges || []
                    },
                    style: [
                        {
                            selector: 'node',
                            style: {
                                'label': 'data(label)',
                                'background-color': '#00d2ff',
                                'color': '#ffffff',
                                'text-valign': 'center',
                                'text-halign': 'center',
                                'font-size': '10px',
                                'width': '50px',
                                'height': '50px'
                            }
                        },
                        {
                            selector: 'edge',
                            style: {
                                'width': 1.5,
                                'line-color': '#4f5d73',
                                'target-arrow-color': '#4f5d73',
                                'target-arrow-shape': 'triangle',
                                'curve-style': 'bezier'
                            }
                        }
                    ],
                    layout: {
                        name: 'circle',
                        padding: 20
                    }
                });
            });
    }
    
    if(triggerBtn) {
        triggerBtn.addEventListener("click", () => {
            const seed = document.getElementById("control-seed").value;
            const logLine = document.createElement("p");
            logLine.innerText = `[TRACE] Initiated downstream tracking from ${seed}...`;
            feed.appendChild(logLine);
            
            fetch('/api/predict', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({seed_node: seed, node_type: 'Supplier', failure_prob: 0.5})
            })
            .then(res => res.json())
            .then(data => {
                const metricLine = document.createElement("p");
                metricLine.className = "text-danger";
                metricLine.innerText = `[ALERT] Estimated Impact: INR ${data.plot_data.metrics.estimated_revenue_loss_inr} | Nodes Affected: ${data.plot_data.metrics.nodes_affected}`;
                feed.appendChild(metricLine);

                // Highlight affected nodes in red
                if (cy) {
                    cy.nodes().style('background-color', '#00d2ff'); // Reset
                    const seedNode = cy.nodes().filter(n => n.data('label') === seed);
                    if (seedNode.length > 0) {
                        seedNode.style('background-color', '#ff3366');
                        seedNode.neighborhood().style('background-color', '#ff9900');
                    }
                }
            });
        });
    }
});

