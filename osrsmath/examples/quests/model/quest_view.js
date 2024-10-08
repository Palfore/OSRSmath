/* Constants */
NORMAL_COLOR = 'RGBA(0, 0, 0, 1)'
FADED_COLOR = 'RGBA(0, 0, 0, 0.1)'
DISABLED_EDGE_COLOR = '#A9A9A9'
DEFAULT_NODE_COLOR = "BLACK"
HIDDEN_FONT = {color: 'RGBA(0, 0, 0, 0)', strokeWidth: 0}

/* Window Functions */
window.help = function() {
    Swal.fire({
        title: 'Welcome to the Quest Explorer!',
        icon: 'info',
        html: HELP
    });
};
window.openWiki = function() {
    network.getSelectedNodes().forEach(function(quest_name) {
    	window.open(nodes.get(quest_name).url);
    });
};
window.swapDirections = function() {
	edges.forEach(function(edge) {
		from = JSON.parse(JSON.stringify(edge.from));
		edge.from = edge.to 
		edge.to = from;
		edges.update(edge);
	});
	window.changeColor();
};
window.changeColor = function() {
    nodes.forEach(function(node) {
        node.style = $('#color_scheme').val().toLowerCase().replace(' ', '_');
        color_node(node);
    });
};
window.animate_release = function() {
	document.getElementById("quests_to_hide").value = QUESTS_IN_ORDER
	animate_quests(true);
	document.getElementById("quests_to_hide").value = "";
}
window.animate_quests = function(show) {
    /* Reset quests */
    quests = get_quests_to_hide()
    quests.forEach(function(name) {
        node = nodes.get(name);
        node.show = !show;
        color_node(node);
    });

    /* Perform animation */
    var started = Date.now();
    var index = 0;
    function update() {
    	animation_length = $('#animation_speed').val();
        elapsedTime = Date.now() - started;
        if (elapsedTime > animation_length) {
            if (add(animation_length)) {
                return;  // stop
            }
            started = Date.now();
        }
        requestAnimationFrame(update);
    }
    function add(duration) {
        if (quests[index] === undefined) {
            return true;
        }
        name = quests[index];
        quest = nodes.get(name);
        quest.show = show;
        color_node(quest);
        network.fit({"animation": {"duration": duration, "easingFunction": "easeInOutCubic"}});
        $('#output').html(`Animating: ${quest.id} | Series: ${quest.series} | Year: ${quest.year}<hr>`);
        index += 1
    }
    add($('#animation_speed').val());
    requestAnimationFrame(update);
};

/* Helper Functions */
color_node = function(node) {
    colors = COLORS

    selected_color = colors[node.style][node[node.style]] || DEFAULT_NODE_COLOR;

    if (!node.show) {
        if (document.getElementById('toggle_completed').checked) {
            selected_color = BACKGROUND_COLOR;
            node.physics = true;
            node.hidden = false;
        } else {
            node.physics = false;
            node.hidden = true;
        }
    } else {
        node.physics = true;
        node.hidden = false;
    }
    nodes.update(node);

    if (document.getElementById('show_names').checked) {
	    if (node.show) {
	        nodes.update({id: node.id, color: selected_color, font: {color: NORMAL_COLOR}});
	    } else {
	        nodes.update({id: node.id, color: selected_color,  font: {color: FADED_COLOR}});
	    }
	} else {
    	nodes.update({id: node.id, color: selected_color, font: HIDDEN_FONT});
    }
    network.getConnectedEdges(node.id).forEach(function(id) {
        edge = edges.get(id);
        // As long as there are no other connected nodes that are hidden
        if (network.getConnectedNodes(id).filter(function(node) {return !nodes.get(node).show;}).length != 0) {
            if (document.getElementById('toggle_completed').checked) {
                edge.color = DISABLED_EDGE_COLOR;
                edge.physics = true;
                edge.hidden = false;
            } else {
                edge.physics = false;
                edge.hidden = true;
            }
        } else {
           	edge.color = nodes.get(edge.from).color; // Always "from" since swapDirections() swaps the from node when called.
            edge.physics = true;
            edge.hidden = false;
        }
        edges.update(edge);
    });
}
get_all_quests = function() {
	return nodes.get().map(obj => obj.id);
}
get_quests_to_hide = function() {
    return document.getElementById("quests_to_hide").value.split(',').filter(n => n).map(name => name.trim());
}
hide_all = function() {
    document.getElementById("quests_to_hide").value = get_all_quests().sort().join(', ')
}
show_quests = function(quests, state=true) {
	quests.forEach(function(quest) {
        node = nodes.get(quest);
        node.show = state;
        nodes.update(node);
    });
};
hideQuests = function() {
    quests_to_hide = get_quests_to_hide()
    get_all_quests().forEach(function(name) {
        node = nodes.get(name);
        node.show = !quests_to_hide.includes(name);
        color_node(node);
    });
};
remove_selected = function(info) {
    if (info) {
        quests = info.nodes;
        hidden_quests = get_quests_to_hide()  // Toggle via symmetric difference.
        const x = hidden_quests.filter(x => !quests.includes(x));
        const y = quests.filter(x => !hidden_quests.includes(x));
        document.getElementById("quests_to_hide").value = x.concat(y).join(', ');
        hideQuests();
        network.unselectAll();
        network.releaseNode();
    } else {
        // TODO: Optimize
        quests = network.getSelectedNodes()
        hidden_quests = get_quests_to_hide()  // Toggle via symmetric difference.
        const x = hidden_quests.filter(x => !quests.includes(x));
        const y = quests.filter(x => !hidden_quests.includes(x));
        document.getElementById("quests_to_hide").value = x.concat(y).join(', ');
        hideQuests();
        network.unselectAll();
        network.releaseNode();
    }
};
remove_selected_prereqs = function() {
    // We get the selected node. This is always a single quest, but we support future lists.
    quests = network.getSelectedNodes()

    // Hidden quests are those in the text box.
    // The set of quests to hide is (already hidden (x), the selected quest (y), and the prereqs (z).
    hidden_quests = get_quests_to_hide()  // Toggle via symmetric difference.


    // Determine the nodes that are prerequisites.
    var prereq_nodes = [];
    quests.forEach(function(questId) {
        var node = nodes.get(questId);
        if (node && node.prereqs && Array.isArray(node.prereqs)) {  // Check if the node has a "prereqs" attribute
            node.prereqs.forEach(function(prereqNodeId) {  // Iterate over the list of prerequisites
                prereq_nodes.push(prereqNodeId);  // Add the prerequisite node ID to the list of prerequisite nodes
            });
        }
    });


    const x = hidden_quests.filter(x => !quests.includes(x));
    const y = quests.filter(x => !hidden_quests.includes(x));
    const z = prereq_nodes.filter(x => !hidden_quests.includes(x));
    document.getElementById("quests_to_hide").value = x.concat(y).concat(z).join(', ');

    // Hide the quests, and release all selections.
    hideQuests();
    network.unselectAll();
    network.releaseNode();
};

remove_selected_if_prereqs = function() {
    // Get the selected node. This is always a single quest, but support future lists.
    var selectedQuest = network.getSelectedNodes()[0];

    remaining_quests = new Set()
    network.getConnectedNodes(selectedQuest).forEach(function(possible_prereq) {
        if (nodes.get(selectedQuest).prereqs.includes(possible_prereq)) {
            prereq = possible_prereq  // Yes, this is a prereq.
            if (nodes.get(prereq).show) { // If it is showing, 
                remaining_quests.add(prereq) // we need to tell the user to complete it.
            }
        } else {
            unlock = possible_prereq // No, not a prereq; an unlock. Do nothing.
        }
    });

    if (remaining_quests.size == 0) {
        remove_selected({nodes: [selectedQuest]})
    } else {
        alert("You still need to complete: " + Array.from(remaining_quests).join(", "))
    }
};



/* Event Bindings */
add_output_div = function() { // https://stackoverflow.com/questions/43135777/vis-js-callback-when-the-network-finishes-loading
    $('<div id="output"><hr></div>').insertAfter('.vis-network');  // Add an output div after loading
    network.off('afterDrawing', add_output_div)  // Disable this function after first execution
};
network.on('afterDrawing', add_output_div);
network.on("hold", remove_selected);
network.on("doubleClick", remove_selected);

/* Connect Click Event Listeners */
// window.toggle_tiered = function() {};
$('#toggle_physics').click(function() {network.setOptions({physics: this.checked});});
$('#toggle_completed').click(window.changeColor);
$('#show_names').click(window.changeColor);

/* Execute */
nodes.forEach(function(node) {
    nodes.update({id: node.id, show: true});
});
window.changeColor();