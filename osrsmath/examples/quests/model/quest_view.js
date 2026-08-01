/* Constants */
NORMAL_COLOR = 'RGBA(0, 0, 0, 1)'
FADED_COLOR = 'RGBA(0, 0, 0, 0.1)'
DISABLED_EDGE_COLOR = '#A9A9A9'
DEFAULT_NODE_COLOR = '#000000'
HIDDEN_FONT = {color: 'RGBA(0, 0, 0, 0)', strokeWidth: 0}

function vis_node_color(cssColor) {
    const c = cssColor || DEFAULT_NODE_COLOR;
    return {
        background: c,
        border: c,
        highlight: { background: c, border: c },
        hover: { background: c, border: c },
    };
}

function current_color_scheme() {
    return (($('#color_scheme').val() || 'shell') + '').toLowerCase().replace(/ /g, '_');
}

/* Window Functions */
window.help = function() {
    Swal.fire({
        title: '<div style="display:flex;align-items:center;gap:0.75rem;text-align:left;">'
            + '<div class="swal2-icon swal2-info swal2-icon-show" style="display:flex;flex-shrink:0;margin:0;width:3.5em;height:3.5em;">'
            + '<div class="swal2-icon-content" style="font-size:2em;">i</div></div>'
            + '<span>Welcome to the Quest Explorer!</span></div>',
        html: HELP,
        width: 'min(90vw, 720px)',
        showCloseButton: true,
        didOpen: function(popup) {
            var actions = popup.querySelector('.swal2-actions');
            if (!actions || actions.querySelector('.quest-help-updated')) {
                return;
            }
            actions.style.width = '100%';
            actions.style.justifyContent = 'space-between';
            actions.style.alignItems = 'center';
            actions.style.paddingLeft = '1.25em';
            actions.style.paddingRight = '1.25em';
            actions.style.boxSizing = 'border-box';
            var stamp = document.createElement('span');
            stamp.className = 'quest-help-updated';
            stamp.style.cssText = 'color:#545454;font-size:0.875em;';
            stamp.textContent = 'Last updated: __LAST_UPDATED__';
            actions.prepend(stamp);
        }
    });
};
window.openWiki = function() {
    lookup_nodes(network.getSelectedNodes());
};
lookup_nodes = function(quest_names) {
    quest_names.forEach(function(quest_name) {
        const node = nodes.get(quest_name);
        if (node && node.url) {
            window.open(node.url);
        }
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
    const scheme = current_color_scheme();
    const mapOn = typeof WORLD_MAP !== 'undefined' && WORLD_MAP.enabled;
    const toggle_completed = document.getElementById('toggle_completed').checked;
    const show_names = document.getElementById('show_names').checked;

    const nodeUpdates = nodes.get().map(function(node) {
        let css = scheme_color_for(node, scheme);
        let physics = !mapOn;
        let hidden = false;
        if (!node.show) {
            if (toggle_completed) {
                css = BACKGROUND_COLOR;
            } else {
                physics = false;
                hidden = true;
            }
        }
        if (mapOn) physics = false;
        return {
            id: node.id,
            style: scheme,
            color: vis_node_color(css),
            font: show_names
                ? {
                    color: node.show ? NORMAL_COLOR : FADED_COLOR,
                    size: mapOn ? MAP_FONT_SIZE : 120,
                    strokeWidth: mapOn ? MAP_FONT_STROKE : 11,
                    strokeColor: BACKGROUND_COLOR,
                }
                : Object.assign({}, HIDDEN_FONT, {
                    size: mapOn ? MAP_FONT_SIZE : 120,
                }),
            physics: physics,
            hidden: hidden,
            fixed: mapOn ? { x: true, y: true } : { x: false, y: false },
            show: node.show,
        };
    });
    if (nodeUpdates.length) nodes.update(nodeUpdates);

    const edgeUpdates = edges.get().map(function(edge) {
        if (mapOn && should_hide_map_edge(edge)) {
            return { id: edge.id, physics: false, hidden: true, width: MAP_EDGE_WIDTH };
        }
        const endpointsHidden = network.getConnectedNodes(edge.id).some(function(n) {
            const cn = nodes.get(n);
            return !cn || !cn.show;
        });
        if (endpointsHidden && !toggle_completed) {
            return {
                id: edge.id,
                physics: false,
                hidden: true,
                width: mapOn ? MAP_EDGE_WIDTH : 24,
            };
        }
        const fromNode = nodes.get(edge.from);
        const fromCss = scheme_color_for(fromNode, scheme);
        return {
            id: edge.id,
            color: (endpointsHidden && toggle_completed) ? DISABLED_EDGE_COLOR : fromCss,
            physics: !mapOn,
            hidden: false,
            width: mapOn ? MAP_EDGE_WIDTH : 24,
        };
    });
    if (edgeUpdates.length) edges.update(edgeUpdates);

    if (typeof refresh_quest_legend === 'function') {
        refresh_quest_legend();
    }
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
function scheme_color_for(node, scheme) {
    if (!node) return DEFAULT_NODE_COLOR;
    const style = scheme || node.style || 'shell';
    const colors = COLORS;
    if (!colors[style]) return DEFAULT_NODE_COLOR;
    const bucket = colors[style];
    let key = node[style];
    if (style === 'combat' || style === 'members') {
        key = (key === true || key === 'true' || key === 'True') ? true : false;
        if (bucket[key] != null) return bucket[key];
        if (bucket[String(key)] != null) return bucket[String(key)];
        return DEFAULT_NODE_COLOR;
    }
    if (bucket[key] != null) return bucket[key];
    if (key != null && bucket[String(key)] != null) return bucket[String(key)];
    if (key != null && !isNaN(Number(key)) && bucket[Number(key)] != null) {
        return bucket[Number(key)];
    }
    return DEFAULT_NODE_COLOR;
}

color_node = function(node) {
    // Keep single-node updates working for animations; full refresh uses changeColor().
    node.style = current_color_scheme();
    const mapOn = typeof WORLD_MAP !== 'undefined' && WORLD_MAP.enabled;
    const toggle_completed = document.getElementById('toggle_completed').checked;
    const show_names = document.getElementById('show_names').checked;

    let css = scheme_color_for(node);
    let physics = !mapOn;
    let hidden = false;
    if (!node.show) {
        if (toggle_completed) css = BACKGROUND_COLOR;
        else { physics = false; hidden = true; }
    }
    if (mapOn) physics = false;

    nodes.update({
        id: node.id,
        style: node.style,
        color: vis_node_color(css),
        font: show_names
            ? {
                color: node.show ? NORMAL_COLOR : FADED_COLOR,
                size: mapOn ? MAP_FONT_SIZE : 120,
                strokeWidth: mapOn ? MAP_FONT_STROKE : 11,
                strokeColor: BACKGROUND_COLOR,
            }
            : Object.assign({}, HIDDEN_FONT, { size: mapOn ? MAP_FONT_SIZE : 120 }),
        physics: physics,
        hidden: hidden,
        fixed: mapOn ? { x: true, y: true } : { x: false, y: false },
        show: node.show,
    });

    const edge_updates = [];
    network.getConnectedEdges(node.id).forEach(function(id) {
        const edge = edges.get(id);
        if (mapOn && should_hide_map_edge(edge)) {
            edge_updates.push({ id: edge.id, physics: false, hidden: true, width: MAP_EDGE_WIDTH });
            return;
        }
        if (network.getConnectedNodes(id).some(function(n) {
            const cn = nodes.get(n);
            return !cn || !cn.show;
        })) {
            if (toggle_completed) {
                edge_updates.push({
                    id: edge.id,
                    color: DISABLED_EDGE_COLOR,
                    physics: !mapOn,
                    hidden: false,
                    width: mapOn ? MAP_EDGE_WIDTH : 24,
                });
            } else {
                edge_updates.push({
                    id: edge.id,
                    physics: false,
                    hidden: true,
                    width: mapOn ? MAP_EDGE_WIDTH : 24,
                });
            }
        } else {
            const fromNode = nodes.get(edge.from);
            edge_updates.push({
                id: edge.id,
                color: scheme_color_for(fromNode, node.style),
                physics: !mapOn,
                hidden: false,
                width: mapOn ? MAP_EDGE_WIDTH : 24,
            });
        }
    });
    if (edge_updates.length) edges.update(edge_updates);
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
/** Update visibility only for nodes whose show state changed. */
sync_quest_visibility = function(hidden_list) {
    const quests_to_hide = new Set(hidden_list);
    get_all_quests().forEach(function(name) {
        node = nodes.get(name);
        const should_show = !quests_to_hide.has(name);
        if (node.show !== should_show) {
            node.show = should_show;
            color_node(node);
        }
    });
};
/** Toggle / set show for a small set of quests and recolor only those. */
update_quest_nodes = function(quest_names, hidden_set) {
    quest_names.forEach(function(name) {
        node = nodes.get(name);
        if (!node) return;
        const should_show = !hidden_set.has(name);
        if (node.show === should_show) return;
        node.show = should_show;
        color_node(node);
    });
};
hideQuests = function() {
    sync_quest_visibility(get_quests_to_hide());
};
remove_selected = function(info) {
    const quests = info ? info.nodes : network.getSelectedNodes();
    const hidden = new Set(get_quests_to_hide());
    quests.forEach(function(name) {
        if (hidden.has(name)) {
            hidden.delete(name);
        } else {
            hidden.add(name);
        }
    });
    document.getElementById("quests_to_hide").value = Array.from(hidden).join(', ');
    update_quest_nodes(quests, hidden);
    network.unselectAll();
    network.releaseNode();
};
remove_selected_prereqs = function() {
    // We get the selected node. This is always a single quest, but we support future lists.
    const quests = network.getSelectedNodes();

    // Hidden quests are those in the text box.
    // The set of quests to hide is (already hidden (x), the selected quest (y), and the prereqs (z).
    const hidden_quests = get_quests_to_hide();
    const previously_hidden = new Set(hidden_quests);

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

    const x = hidden_quests.filter(n => !quests.includes(n));
    const y = quests.filter(n => !previously_hidden.has(n));
    const z = prereq_nodes.filter(n => !previously_hidden.has(n));
    const new_hidden = x.concat(y).concat(z);
    document.getElementById("quests_to_hide").value = new_hidden.join(', ');

    // Only recolor selected quests and their prereqs (the only nodes that can change).
    update_quest_nodes([...new Set(quests.concat(prereq_nodes))], new Set(new_hidden));

    // Hide the quests, and release all selections.
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

/* Quest title search (anchored top-right inside the canvas) */
const quest_search_state = { matches: [], index: -1 };

install_quest_search = function() {
    const host = document.getElementById('mynetwork');
    if (!host || document.getElementById('quest-search-panel')) return;
    host.style.position = 'relative';

    const style = document.createElement('style');
    style.textContent = `
        #quest-search-panel {
            position: absolute;
            top: 12px;
            right: 12px;
            z-index: 5;
            font-family: sans-serif;
            font-size: 14px;
            display: flex;
            flex-direction: column;
            align-items: flex-end;
        }
        #quest-search-panel.expanded {
            /* Clear left hamburger: 12 inset + 40 button + 12 gap; panel already has right: 12. */
            width: min(320px, calc(100% - 76px));
            max-height: calc(100% - 24px);
            overflow: hidden;
            align-items: stretch;
        }
        #quest_search_toggle {
            width: 40px;
            height: 40px;
            border: 1px solid #555;
            border-radius: 4px;
            background: rgba(43, 43, 43, 0.92);
            color: #fff;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
            padding: 0;
        }
        #quest_search_toggle:hover { background: rgba(68, 68, 68, 0.95); }
        #quest-search-panel.expanded #quest_search_toggle { display: none; }
        #quest_search_body {
            display: none;
            width: 100%;
            box-sizing: border-box;
            border: 1px solid #555;
            border-radius: 4px;
            background: rgba(43, 43, 43, 0.96);
            box-shadow: 0 4px 12px rgba(0,0,0,0.35);
            color: #fff;
            min-height: 0;
        }
        #quest-search-panel.expanded #quest_search_body {
            display: flex;
            flex-direction: column;
            max-height: 100%;
            min-height: 0;
            overflow: hidden;
        }
        #quest_search_header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 8px;
            padding: 8px 10px;
            border-bottom: 1px solid #555;
            font-weight: 600;
            flex: 0 0 auto;
        }
        #quest_search_close {
            background: transparent;
            border: none;
            color: #bbb;
            cursor: pointer;
            font-size: 18px;
            line-height: 1;
            padding: 0 4px;
        }
        #quest_search_close:hover { color: #fff; }
        #quest_search {
            width: 100%;
            box-sizing: border-box;
            padding: 8px 36px 8px 12px;
            border: none;
            border-bottom: 1px solid #555;
            border-radius: 0;
            background: transparent;
            color: #fff;
            outline: none;
            flex: 0 0 auto;
        }
        #quest_search:focus { border-bottom-color: #ffc107; }
        #quest_search_meta {
            position: absolute;
            right: 10px;
            top: 8px;
            color: #bbb;
            font-size: 12px;
            pointer-events: none;
        }
        #quest_search_wrap { position: relative; flex: 0 0 auto; }
        #quest_search_results {
            display: none;
            flex: 0 1 auto;
            min-height: 0;
            overflow-y: auto;
            background: transparent;
        }
        #quest_search_results.open { display: block; }
        .quest-search-item {
            padding: 6px 12px;
            cursor: pointer;
            color: #fff;
            user-select: none;
        }
        .quest-search-item:hover,
        .quest-search-item.active {
            background: #444;
        }
    `;
    document.head.appendChild(style);

    const panel = document.createElement('div');
    panel.id = 'quest-search-panel';
    panel.innerHTML = `
        <button type="button" id="quest_search_toggle" title="Search quests (Ctrl+F)" aria-label="Search quests">
            <i class="bi bi-search"></i>
        </button>
        <div id="quest_search_body">
            <div id="quest_search_header">
                <span>Search</span>
                <button type="button" id="quest_search_close" title="Close" aria-label="Close">&times;</button>
            </div>
            <div id="quest_search_wrap">
                <input id="quest_search" type="search" placeholder="Search quests..." autocomplete="off" spellcheck="false" />
                <span id="quest_search_meta"></span>
            </div>
            <div id="quest_search_results"></div>
        </div>
    `;
    host.appendChild(panel);
    panel.style.display = 'none';  // show after loading bar finishes
    panel.addEventListener('mousedown', function(e) { e.stopPropagation(); });
    panel.addEventListener('click', function(e) { e.stopPropagation(); });
    panel.addEventListener('wheel', function(e) { e.stopPropagation(); });

    const toggle = document.getElementById('quest_search_toggle');
    const closeBtn = document.getElementById('quest_search_close');
    const input = document.getElementById('quest_search');
    const results = document.getElementById('quest_search_results');
    const meta = document.getElementById('quest_search_meta');

    network.once('stabilizationIterationsDone', function() {
        // Match loadingBar fade timing from pyvis.
        setTimeout(function() { panel.style.display = ''; }, 500);
    });

    function expand_search() {
        panel.classList.add('expanded');
        input.focus();
        input.select();
        render_results(find_quests(input.value));
    }

    function collapse_search() {
        results.classList.remove('open');
        panel.classList.remove('expanded');
        input.blur();
    }

    toggle.addEventListener('click', function(e) {
        e.preventDefault();
        expand_search();
    });
    closeBtn.addEventListener('click', function(e) {
        e.preventDefault();
        e.stopPropagation();
        collapse_search();
    });

    function find_quests(query) {
        const q = query.trim().toLowerCase();
        const ids = nodes.get().map(n => n.id);
        if (!q) {
            return ids.slice().sort(function(a, b) {
                return a.toLowerCase().localeCompare(b.toLowerCase());
            });
        }
        return ids
            .filter(id => id.toLowerCase().includes(q))
            .sort((a, b) => {
                const al = a.toLowerCase(), bl = b.toLowerCase();
                const aStarts = al.startsWith(q), bStarts = bl.startsWith(q);
                if (aStarts !== bStarts) return aStarts ? -1 : 1;
                return al.localeCompare(bl);
            });
    }

    function go_to_quest(id) {
        if (!id || !nodes.get(id)) return;
        network.selectNodes([id]);
        network.focus(id, { animation: { duration: 400, easingFunction: 'easeInOutQuad' } });
        const i = quest_search_state.matches.indexOf(id);
        if (i >= 0) quest_search_state.index = i;
        update_search_meta();
        highlight_active_result();
    }

    function update_search_meta() {
        const n = quest_search_state.matches.length;
        if (!n) {
            meta.textContent = '0';
        } else if (quest_search_state.index < 0) {
            meta.textContent = String(n);
        } else {
            meta.textContent = `${quest_search_state.index + 1}/${n}`;
        }
    }

    function highlight_active_result() {
        results.querySelectorAll('.quest-search-item').forEach(function(el, i) {
            el.classList.toggle('active', i === quest_search_state.index);
        });
        const active = results.querySelector('.quest-search-item.active');
        if (active) active.scrollIntoView({ block: 'nearest' });
    }

    function render_results(matches) {
        quest_search_state.matches = matches;
        quest_search_state.index = -1;  // next Enter/Arrow lands on first match
        results.innerHTML = '';
        if (!matches.length) {
            results.classList.remove('open');
            update_search_meta();
            return;
        }
        matches.forEach(function(id) {
            const item = document.createElement('div');
            item.className = 'quest-search-item';
            item.textContent = id;
            item.addEventListener('mousedown', function(e) {
                e.preventDefault();  // keep focus in input
                quest_search_state.index = quest_search_state.matches.indexOf(id);
                go_to_quest(id);
                results.classList.add('open');
            });
            results.appendChild(item);
        });
        results.classList.add('open');
        update_search_meta();
    }

    function cycle_match(delta) {
        const matches = quest_search_state.matches;
        if (!matches.length) return;
        if (quest_search_state.index < 0) {
            quest_search_state.index = delta >= 0 ? 0 : matches.length - 1;
        } else {
            quest_search_state.index = (quest_search_state.index + delta + matches.length) % matches.length;
        }
        go_to_quest(matches[quest_search_state.index]);
    }

    input.addEventListener('input', function() {
        render_results(find_quests(input.value));
    });

    input.addEventListener('keydown', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            if (!quest_search_state.matches.length) {
                render_results(find_quests(input.value));
            }
            cycle_match(e.shiftKey ? -1 : 1);
        } else if (e.key === 'ArrowDown') {
            e.preventDefault();
            cycle_match(1);
        } else if (e.key === 'ArrowUp') {
            e.preventDefault();
            cycle_match(-1);
        } else if (e.key === 'Escape') {
            if (results.classList.contains('open')) {
                results.classList.remove('open');
            } else {
                collapse_search();
            }
        }
    });

    input.addEventListener('focus', function() {
        if (quest_search_state.matches.length) results.classList.add('open');
    });

    document.addEventListener('keydown', function(e) {
        if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'f') {
            e.preventDefault();
            expand_search();
        }
    });

    document.addEventListener('mousedown', function(e) {
        if (panel.classList.contains('expanded') && !panel.contains(e.target)) {
            collapse_search();
        }
    });
};

install_quest_search();

/* Color legend (anchored top-left inside the canvas) */
refresh_quest_legend = function() {};  // set by install_quest_legend

install_quest_legend = function() {
    const host = document.getElementById('mynetwork');
    if (!host || document.getElementById('quest-legend-panel')) return;
    host.style.position = 'relative';

    const style = document.createElement('style');
    style.textContent = `
        #quest-legend-panel {
            position: absolute;
            top: 12px;
            left: 12px;
            z-index: 5;
            font-family: sans-serif;
            font-size: 14px;
            display: flex;
            flex-direction: column;
            align-items: flex-start;
        }
        #quest-legend-panel.expanded {
            max-height: calc(100% - 24px);
            overflow: hidden;
            align-items: stretch;
        }
        #quest_legend_toggle {
            width: 40px;
            height: 40px;
            border: 1px solid #555;
            border-radius: 4px;
            background: rgba(43, 43, 43, 0.92);
            color: #fff;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
            padding: 0;
        }
        #quest_legend_toggle:hover { background: rgba(68, 68, 68, 0.95); }
        #quest-legend-panel.expanded #quest_legend_toggle { display: none; }
        #quest_legend_body {
            display: none;
            width: min(280px, calc(100vw - 48px));
            border: 1px solid #555;
            border-radius: 4px;
            background: rgba(43, 43, 43, 0.96);
            box-shadow: 0 4px 12px rgba(0,0,0,0.35);
            color: #fff;
            min-height: 0;
        }
        #quest-legend-panel.expanded #quest_legend_body {
            display: flex;
            flex-direction: column;
            max-height: 100%;
            min-height: 0;
            overflow: hidden;
        }
        #quest_legend_header {
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            gap: 8px;
            padding: 8px 10px;
            border-bottom: 1px solid #555;
            font-weight: 600;
            flex: 0 0 auto;
        }
        #quest_legend_heading {
            display: flex;
            flex-direction: column;
            gap: 2px;
            min-width: 0;
        }
        #quest_legend_subtitle {
            font-weight: 400;
            font-size: 12px;
            color: #bbb;
        }
        #quest_legend_close {
            background: transparent;
            border: none;
            color: #bbb;
            cursor: pointer;
            font-size: 18px;
            line-height: 1;
            padding: 0 4px;
        }
        #quest_legend_close:hover { color: #fff; }
        #quest_legend_list {
            display: none;
            flex: 0 1 auto;
            min-height: 0;
            overflow-y: auto;
            padding: 6px 0;
            background: rgba(43, 43, 43, 0.96);
        }
        #quest_legend_list.open { display: block; }
        .quest-legend-item {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 6px 12px;
            user-select: none;
            color: #fff;
            cursor: pointer;
        }
        .quest-legend-item:hover {
            background: #444;
        }
        .quest-legend-swatch {
            width: 14px;
            height: 14px;
            border-radius: 3px;
            border: 1px solid rgba(255,255,255,0.35);
            flex: 0 0 auto;
        }
        .quest-legend-label {
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }
    `;
    document.head.appendChild(style);

    const panel = document.createElement('div');
    panel.id = 'quest-legend-panel';
    panel.innerHTML = `
        <button type="button" id="quest_legend_toggle" title="Color legend" aria-label="Color legend">
            <i class="bi bi-list"></i>
        </button>
        <div id="quest_legend_body">
            <div id="quest_legend_header">
                <div id="quest_legend_heading">
                    <span id="quest_legend_title">Legend</span>
                    <span id="quest_legend_subtitle"></span>
                </div>
                <button type="button" id="quest_legend_close" title="Close" aria-label="Close">&times;</button>
            </div>
            <div id="quest_legend_list"></div>
        </div>
    `;
    host.appendChild(panel);
    panel.style.display = 'none';
    panel.addEventListener('mousedown', function(e) { e.stopPropagation(); });
    panel.addEventListener('click', function(e) { e.stopPropagation(); });
    panel.addEventListener('wheel', function(e) { e.stopPropagation(); });

    const toggle = document.getElementById('quest_legend_toggle');
    const list = document.getElementById('quest_legend_list');
    const title = document.getElementById('quest_legend_title');
    const subtitle = document.getElementById('quest_legend_subtitle');
    const closeBtn = document.getElementById('quest_legend_close');

    network.once('stabilizationIterationsDone', function() {
        setTimeout(function() { panel.style.display = ''; }, 500);
    });

    function current_scheme() {
        return $('#color_scheme').val().toLowerCase().replace(' ', '_');
    }

    function scheme_display_name(scheme) {
        if (scheme === 'shell') return 'Tier';
        return scheme.replace(/_/g, ' ').replace(/\b\w/g, function(c) { return c.toUpperCase(); });
    }

    function used_scheme_values(scheme) {
        const used = new Set();
        nodes.get().forEach(function(node) {
            const val = node[scheme];
            if (val === undefined || val === null) return;
            if (scheme === 'shell') {
                used.add(String(Number(val)));
            } else if (scheme === 'combat' || scheme === 'members') {
                used.add(Boolean(val) ? 'true' : 'false');
            } else {
                used.add(String(val));
            }
        });
        return used;
    }

    function scheme_entries(scheme) {
        const map = COLORS[scheme];
        if (!map) return [];
        const used = used_scheme_values(scheme);
        if (Array.isArray(map)) {
            return map.map(function(color, i) {
                return { label: 'Tier ' + i, color: color, key: i };
            }).filter(function(entry) {
                return used.has(String(entry.key));
            });
        }
        let entries = Object.keys(map).map(function(key) {
            let label = key;
            if (key === 'true' || key === 'True' || key === true) label = 'Yes';
            if (key === 'false' || key === 'False' || key === false) label = 'No';
            return { label: String(label), color: map[key], key: key };
        }).filter(function(entry, i, arr) {
            // Dedupe combat/members true variants.
            return arr.findIndex(function(e) { return e.label === entry.label; }) === i;
        }).filter(function(entry) {
            if (scheme === 'combat' || scheme === 'members') {
                const flag = (entry.key === true || entry.key === 'true' || entry.key === 'True') ? 'true' : 'false';
                return used.has(flag);
            }
            return used.has(String(entry.key));
        });
        if (scheme === 'series' || scheme === 'main_developer') {
            entries.sort(function(a, b) {
                return a.label.localeCompare(b.label, undefined, { sensitivity: 'base' });
            });
        }
        return entries;
    }

    function node_matches_legend_key(node, scheme, key) {
        const val = node[scheme];
        if (scheme === 'shell') {
            return Number(val) === Number(key);
        }
        if (scheme === 'combat' || scheme === 'members') {
            const want = (key === true || key === 'true' || key === 'True');
            return Boolean(val) === want;
        }
        return String(val) === String(key);
    }

    function frame_legend_group(scheme, key) {
        const restrictToMap = WORLD_MAP && WORLD_MAP.enabled
            && (WORLD_MAP.simple || WORLD_MAP.edgeless);
        const ids = nodes.get().filter(function(node) {
            if (node.hidden) return false;
            if (!node_matches_legend_key(node, scheme, key)) return false;
            if (restrictToMap && typeof node_on_map_image === 'function'
                    && !node_on_map_image(node)) {
                return false;
            }
            return true;
        }).map(function(node) { return node.id; });
        if (!ids.length) return;
        network.selectNodes(ids);
        network.fit({
            nodes: ids,
            animation: { duration: 500, easingFunction: 'easeInOutQuad' },
        });
    }

    function refresh_color_scheme_labels() {
        const select = document.getElementById('color_scheme');
        if (!select) return;
        Array.from(select.options).forEach(function(opt) {
            const scheme = opt.value.toLowerCase().replace(' ', '_');
            const pretty = scheme_display_name(scheme);
            const n = scheme_entries(scheme).length;
            opt.textContent = pretty + ' (' + n + ')';
        });
    }

    function refresh_quest_legend_impl() {
        const scheme = current_scheme();
        const pretty = scheme_display_name(scheme);
        const entries = scheme_entries(scheme);
        title.textContent = pretty;
        subtitle.textContent = entries.length + ' categor' + (entries.length === 1 ? 'y' : 'ies');
        list.innerHTML = '';
        entries.forEach(function(entry) {
            const row = document.createElement('div');
            row.className = 'quest-legend-item';
            const swatch = document.createElement('span');
            swatch.className = 'quest-legend-swatch';
            swatch.style.background = entry.color;
            const count = nodes.get().filter(function(node) {
                return node_matches_legend_key(node, scheme, entry.key);
            }).length;
            const label = document.createElement('span');
            label.className = 'quest-legend-label';
            label.textContent = entry.label + ' (' + count + ')';
            label.title = entry.label + ': ' + count + ' quest' + (count === 1 ? '' : 's');
            row.title = 'Frame ' + entry.label + ' (' + count + ')';
            row.appendChild(swatch);
            row.appendChild(label);
            row.addEventListener('click', function(e) {
                e.preventDefault();
                frame_legend_group(scheme, entry.key);
            });
            list.appendChild(row);
        });
        if (entries.length) {
            list.classList.add('open');
        } else {
            list.classList.remove('open');
        }
        refresh_color_scheme_labels();
    }
    refresh_quest_legend = refresh_quest_legend_impl;

    function expand_legend() {
        refresh_quest_legend_impl();
        panel.classList.add('expanded');
    }

    function collapse_legend() {
        panel.classList.remove('expanded');
    }

    toggle.addEventListener('click', function(e) {
        e.preventDefault();
        expand_legend();
    });
    closeBtn.addEventListener('click', function(e) {
        e.preventDefault();
        collapse_legend();
    });

    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && panel.classList.contains('expanded')) {
            collapse_legend();
        }
    });

    document.addEventListener('mousedown', function(e) {
        if (panel.classList.contains('expanded') && !panel.contains(e.target)) {
            collapse_legend();
        }
    });

    $('#color_scheme').on('change', function() {
        if (panel.classList.contains('expanded')) {
            refresh_quest_legend_impl();
        }
    });

    refresh_quest_legend_impl();
};

install_quest_legend();

/* Right-click context menu */
const QUEST_MENU_ACTIONS = [
    ['lookup', 'Lookup', 'Lookup the selected quest on the wiki.', '#6c757d', '#fff'],
    ['force', 'Force', 'Completed the selected quest.', '#ffc107', '#212529'],
    ['finish', 'Finish', 'Completed the selected quest and its prerequisites.', '#ffc107', '#212529'],
    ['complete', 'Complete', 'Completed the selected quest if its prerequisites are completed.', '#ffc107', '#212529'],
];
const quest_context_menu = document.createElement('div');
quest_context_menu.id = 'quest-context-menu';
Object.assign(quest_context_menu.style, {
    display: 'none',
    position: 'fixed',
    zIndex: '10000',
    background: '#2b2b2b',
    border: '1px solid #555',
    borderRadius: '4px',
    boxShadow: '0 4px 12px rgba(0,0,0,0.35)',
    minWidth: '140px',
    padding: '4px 0',
    fontFamily: 'sans-serif',
    fontSize: '14px',
});
const quest_menu_style = document.createElement('style');
quest_menu_style.textContent = 'body.quest-context-open .vis-tooltip { display: none !important; visibility: hidden !important; opacity: 0 !important; }';
document.head.appendChild(quest_menu_style);

QUEST_MENU_ACTIONS.forEach(function([action, label, tip, bg, fg]) {
    const item = document.createElement('div');
    item.dataset.action = action;
    item.textContent = label;
    item.title = tip;
    item.setAttribute('data-toggle', 'tooltip');
    item.setAttribute('data-placement', 'right');
    Object.assign(item.style, {
        padding: '6px 14px',
        cursor: 'pointer',
        userSelect: 'none',
        color: fg,
        background: bg,
        margin: '2px 6px',
        borderRadius: '3px',
    });
    item.addEventListener('mouseenter', function() { item.style.filter = 'brightness(1.1)'; });
    item.addEventListener('mouseleave', function() { item.style.filter = ''; });
    quest_context_menu.appendChild(item);
});
document.body.appendChild(quest_context_menu);
if (window.jQuery && $.fn.tooltip) {
    $(quest_context_menu).find('[data-toggle="tooltip"]').tooltip({container: 'body', trigger: 'hover'});
}

hide_quest_infobox = function() {
    // vis popup show() only sets visibility — never clear display/opacity or the
    // tooltip stays dead after a context-menu open.
    document.querySelectorAll('.vis-tooltip').forEach(function(el) {
        el.style.visibility = 'hidden';
        el.style.removeProperty('display');
        el.style.removeProperty('opacity');
    });
    try {
        if (network.interactionHandler) {
            if (network.interactionHandler.popup) {
                network.interactionHandler.popup.hide();
            }
            network.interactionHandler.popupObj = undefined;
        }
    } catch (e) {}
};
hide_context_menu = function() {
    quest_context_menu.style.display = 'none';
    document.body.classList.remove('quest-context-open');
    if (window.jQuery && $.fn.tooltip) {
        $(quest_context_menu).find('[data-toggle="tooltip"]').tooltip('hide');
    }
};
show_context_menu = function(x, y) {
    document.body.classList.add('quest-context-open');
    hide_quest_infobox();
    quest_context_menu.style.left = x + 'px';
    quest_context_menu.style.top = y + 'px';
    quest_context_menu.style.display = 'block';
};
quest_context_menu.addEventListener('click', function(e) {
    e.stopPropagation();
    const action = e.target.dataset.action;
    if (!action) return;
    hide_context_menu();
    switch (action) {
        case 'lookup': openWiki(); break;
        case 'force': remove_selected(); break;
        case 'finish': remove_selected_prereqs(); break;
        case 'complete': remove_selected_if_prereqs(); break;
    }
});
document.addEventListener('click', hide_context_menu);
document.addEventListener('scroll', hide_context_menu, true);

network.on('afterDrawing', add_output_div);
function open_quest_context_from_pointer(params) {
    if (params.event) {
        if (params.event.preventDefault) params.event.preventDefault();
        if (params.event.stopPropagation) params.event.stopPropagation();
    }
    hide_quest_infobox();
    const dom = params.pointer && params.pointer.DOM;
    const nodeId = (params.nodes && params.nodes.length && params.nodes[0])
        || (dom ? network.getNodeAt(dom) : null);
    if (!nodeId) {
        hide_context_menu();
        return;
    }
    network.selectNodes([nodeId]);
    hide_quest_infobox();
    const ev = params.event;
    let x, y;
    if (ev && ev.center && ev.center.x != null) {
        x = ev.center.x;
        y = ev.center.y;
    } else if (ev && ev.clientX != null) {
        x = ev.clientX;
        y = ev.clientY;
    } else if (ev && ev.srcEvent && ev.srcEvent.clientX != null) {
        x = ev.srcEvent.clientX;
        y = ev.srcEvent.clientY;
    } else if (dom && network.canvas && network.canvas.frame) {
        const rect = network.canvas.frame.getBoundingClientRect();
        x = rect.left + dom.x;
        y = rect.top + dom.y;
    } else {
        return;
    }
    show_context_menu(x, y);
}
network.on('hold', open_quest_context_from_pointer);
network.on('doubleClick', function(params) {
    if (params.nodes.length) {
        lookup_nodes(params.nodes);
    }
});
network.on('oncontext', open_quest_context_from_pointer);

/* Connect Click Event Listeners */
// window.toggle_tiered = function() {};
$('#toggle_completed').click(window.changeColor);
$('#show_names').click(window.changeColor);

/* OSRS map mode: pin nodes at start coords + map.png background.
 *
 * MAP_COORD_SCALE — game tiles → vis-network units (tune node/edge spacing).
 * MAP_ANCHORS — two (game x/y ↔ image pixel x/y) pairs calibrate the PNG.
 * Image pixels are top-left origin; game Y increases north.
 *
 * Display modes (dropdown):
 *   physics / no_physics  — physics layout (no_physics freezes it)
 *   map / map_simple / map_edgeless — map layout
 *     simple: hide off-image edges; edgeless: hide all edges
 * Physics sizes are snapshotted when entering map; leaving map resets all
 * nodes to the origin (physics re-spreads from there).
 */
const WORLD_MAP_AVAILABLE = __WORLD_MAP_AVAILABLE__;
const MAP_COORD_SCALE = 50;
const MAP_NODE_SIZE_FACTOR = 4.95;
const MAP_NODE_SIZE_MIN = 198;
const MAP_EDGE_WIDTH = 72;
const MAP_EDGE_EMPHASIS = MAP_EDGE_WIDTH * 3;
const PHYSICS_EDGE_EMPHASIS = 160;
const NODE_BORDER_EMPHASIS = 50;
const NODE_HOVER_SIZE_FACTOR = 2;

function match_hover_select_node(values, id, selected, hovering) {
    if (!(selected || hovering)) return;
    const node = nodes.get(id);
    let fill = DEFAULT_NODE_COLOR;
    if (node && node.color != null) {
        fill = (typeof node.color === 'object')
            ? (node.color.background || node.color.border || fill)
            : node.color;
    } else if (values.color) {
        fill = values.color;
    }
    // vis applies borderWidth/scale (screen px); node size is in world units.
    const scale = (network.body && network.body.view && network.body.view.scale) || 1;
    const size = values.size || (node && node.size) || 25;
    values.size = size * NODE_HOVER_SIZE_FACTOR;
    values.color = fill;
    values.borderColor = '#ffffff';
    values.borderWidth = Math.max(2, values.size * scale * 0.2);
}

// Hover and select use the same emphasis sizes (nodes + edges).
network.setOptions({
    nodes: {
        borderWidthSelected: NODE_BORDER_EMPHASIS,
        chosen: { node: match_hover_select_node },
    },
    edges: {
        hoverWidth: PHYSICS_EDGE_EMPHASIS,
        selectionWidth: PHYSICS_EDGE_EMPHASIS,
    },
});

/**
 * vis hit-tests edges with a fixed 10px world threshold and nodes with their
 * un-hovered shape. Hover visuals are much larger, so the cursor falls off the
 * hit box, hover drops, the visual shrinks, and it stutters. Match hit areas to
 * the enlarged hover geometry.
 */
function edge_hover_hit_radius(edge) {
    const w = (edge.options && edge.options.width != null) ? edge.options.width : 1;
    let hoverAdd = edge.options && edge.options.hoverWidth;
    if (hoverAdd == null) {
        hoverAdd = (typeof WORLD_MAP !== 'undefined' && WORLD_MAP.enabled)
            ? MAP_EDGE_EMPHASIS
            : PHYSICS_EDGE_EMPHASIS;
    }
    const hoveredWidth = (typeof hoverAdd === 'function')
        ? hoverAdd(w)
        : (w + hoverAdd);
    return Math.max(10, hoveredWidth / 2);
}

function install_stable_hover_hits() {
    const sh = network.selectionHandler;
    if (!sh || sh._osrsStableHover) return;
    sh._osrsStableHover = true;

    // Tooltip show/hide uses node.isOverlappingWith (base shape), while hover
    // visuals use 2× size — patch overlap to the same circle as getNodeAt.
    const firstId = network.body && network.body.nodeIndices && network.body.nodeIndices[0];
    if (firstId != null) {
        const proto = Object.getPrototypeOf(network.body.nodes[firstId]);
        if (proto && !proto._osrsOverlapPatched) {
            proto._osrsOverlapPatched = true;
            proto.isOverlappingWith = function(obj) {
                if (!this.shape) return false;
                const baseR = (this.shape.width > 0)
                    ? (this.shape.width / 2)
                    : ((this.options && this.options.size) || 25);
                const hitR = baseR * NODE_HOVER_SIZE_FACTOR;
                const px = (obj.left + obj.right) / 2;
                const py = (obj.top + obj.bottom) / 2;
                if (Math.abs(obj.right - obj.left) <= 2 && Math.abs(obj.bottom - obj.top) <= 2) {
                    const dx = px - this.x;
                    const dy = py - this.y;
                    return dx * dx + dy * dy <= hitR * hitR;
                }
                return (this.x - hitR) < obj.right && (this.x + hitR) > obj.left
                    && (this.y - hitR) < obj.bottom && (this.y + hitR) > obj.top;
            };
        }
    }

    sh.getEdgeAt = function(pointer) {
        const returnObj = !(arguments.length > 1 && arguments[1] !== undefined) || arguments[1];
        const canvasPos = this.canvas.DOMtoCanvas(pointer);
        let bestId = null;
        let bestDist = Infinity;
        const edgeObjs = this.body.edges;
        for (let i = 0; i < this.body.edgeIndices.length; i++) {
            const id = this.body.edgeIndices[i];
            const edge = edgeObjs[id];
            if (!edge || !edge.connected) continue;
            if (edge.options && edge.options.hidden) continue;
            if (!edge.edgeType || typeof edge.edgeType.getDistanceToEdge !== 'function') continue;
            const dist = edge.edgeType.getDistanceToEdge(
                edge.from.x, edge.from.y, edge.to.x, edge.to.y,
                canvasPos.x, canvasPos.y
            );
            const hitR = edge_hover_hit_radius(edge);
            if (dist < hitR && dist < bestDist) {
                bestDist = dist;
                bestId = id;
            }
        }
        if (bestId == null) return undefined;
        return returnObj ? this.body.edges[bestId] : bestId;
    };

    sh.getNodeAt = function(pointer) {
        const returnObj = !(arguments.length > 1 && arguments[1] !== undefined) || arguments[1];
        const canvasPos = this.canvas.DOMtoCanvas(pointer);
        const overlapping = [];
        const nodeObjs = this.body.nodes;
        for (let i = 0; i < this.body.nodeIndices.length; i++) {
            const id = this.body.nodeIndices[i];
            const node = nodeObjs[id];
            if (!node || !node.shape) continue;
            if (node.options && node.options.hidden) continue;
            const baseR = (node.shape.width > 0) ? (node.shape.width / 2) : (node.options.size || 25);
            const hitR = baseR * NODE_HOVER_SIZE_FACTOR;
            const dx = canvasPos.x - node.x;
            const dy = canvasPos.y - node.y;
            if (dx * dx + dy * dy <= hitR * hitR) {
                overlapping.push(id);
            }
        }
        if (!overlapping.length) return undefined;
        const id = overlapping[overlapping.length - 1];
        return returnObj ? this.body.nodes[id] : id;
    };
}

install_stable_hover_hits();

const MAP_FONT_SIZE = Math.round(120 * MAP_NODE_SIZE_FACTOR);
const MAP_FONT_STROKE = Math.round(11 * MAP_NODE_SIZE_FACTOR);
const MAP_IMAGE_URL = '__MAP_IMAGE_URL__';
const MAP_ANCHORS = [
    // The Great Brain Robbery
    { game: { x: 3682, y: 2963 }, img: { x: 8166, y: 3781 } },
    // The Forsaken Tower
    { game: { x: 1483, y: 3748 }, img: { x: 1569, y: 1425 } },
];

let DISPLAY_MODE = 'physics';
// Two layouts: physics | map.  no_physics / map_simple / map_edgeless are variants.
let LAYOUT = 'physics';
// Snapshot of physics-layout positions/sizes, taken when entering map.
let PHYSICS_LAYOUT_SAVE = null;

const WORLD_MAP = {
    enabled: false,
    simple: false,    // Map (simple): hide edges with endpoints off the image
    edgeless: false,  // Map (edgeless): hide all edges
    available: WORLD_MAP_AVAILABLE,
    image: null,
    calib: null,  // { sx, sy, ox, oy, imgW, imgH }
    saved: null,  // edge width/hidden while map is active
};

function node_start_xy(node) {
    // Wiki start is [data-lat, data-lon] == [y, x].
    if (Array.isArray(node.start) && node.start.length >= 2) {
        const gx = Number(node.start[1]);
        const gy = Number(node.start[0]);
        if (Number.isFinite(gx) && Number.isFinite(gy)) return { x: gx, y: gy };
    }
    const gx = Number(node.start_x);
    const gy = Number(node.start_y);
    if (!Number.isFinite(gx) || !Number.isFinite(gy)) return null;
    return { x: gx, y: gy };
}

function world_map_bounds() {
    let xMin = Infinity, xMax = -Infinity, yMin = Infinity, yMax = -Infinity;
    nodes.get().forEach(function(node) {
        const s = node_start_xy(node);
        if (!s) return;
        if (s.x < xMin) xMin = s.x;
        if (s.x > xMax) xMax = s.x;
        if (s.y < yMin) yMin = s.y;
        if (s.y > yMax) yMax = s.y;
    });
    if (!Number.isFinite(xMin)) {
        return { xMin: 0, xMax: 0, yMin: 0, yMax: 0 };
    }
    return { xMin: xMin, xMax: xMax, yMin: yMin, yMax: yMax };
}

function game_to_vis_xy(gx, gy) {
    // vis-network y grows downward; flip so higher game Y is toward the top.
    return { x: gx * MAP_COORD_SCALE, y: -gy * MAP_COORD_SCALE };
}

function game_on_map_image(gx, gy) {
    const c = WORLD_MAP.calib;
    if (!c) return true;
    const ix = c.sx * gx + c.ox;
    const iy = c.sy * gy + c.oy;
    return ix >= 0 && iy >= 0 && ix <= c.imgW && iy <= c.imgH;
}

function node_on_map_image(node) {
    if (!node) return false;
    const s = node_start_xy(node);
    // Missing start coords are pinned to the quest bbox center (usually on-map).
    if (!s) return true;
    return game_on_map_image(s.x, s.y);
}

function should_hide_map_edge(edge) {
    if (WORLD_MAP.edgeless) return true;
    if (WORLD_MAP.simple && !edge_on_map_image(edge)) return true;
    return false;
}

function apply_map_mode_flags(mode) {
    WORLD_MAP.simple = mode === 'map_simple';
    WORLD_MAP.edgeless = mode === 'map_edgeless';
}

function edge_on_map_image(edge) {
    return node_on_map_image(nodes.get(edge.from)) && node_on_map_image(nodes.get(edge.to));
}

function set_network_physics(on) {
    network.setOptions({ physics: { enabled: !!on } });
}

function calibrate_world_map(imgW, imgH) {
    const a = MAP_ANCHORS[0];
    const b = MAP_ANCHORS[1];
    const sx = (a.img.x - b.img.x) / (a.game.x - b.game.x);
    const sy = (a.img.y - b.img.y) / (a.game.y - b.game.y);
    const ox = a.img.x - sx * a.game.x;
    const oy = a.img.y - sy * a.game.y;
    WORLD_MAP.calib = { sx: sx, sy: sy, ox: ox, oy: oy, imgW: imgW, imgH: imgH };
}

function prepare_world_map_image(img) {
    calibrate_world_map(img.naturalWidth, img.naturalHeight);
    // Keep the full-res Image; downscaling here made the map blurry when stretched.
    WORLD_MAP.image = img;
    if (WORLD_MAP.enabled) fit_to_world_map();
}

function world_map_draw(ctx) {
    if (!WORLD_MAP.enabled || !WORLD_MAP.image || !WORLD_MAP.calib) return;
    const S = MAP_COORD_SCALE;
    const c = WORLD_MAP.calib;
    // Image pixel (0,0) → game (-ox/sx, -oy/sy) → vis.
    const left = (-c.ox / c.sx) * S;
    const top = (c.oy / c.sy) * S;           // = -(-oy/sy)*S
    const w = (c.imgW / c.sx) * S;
    const h = (-c.imgH / c.sy) * S;          // sy is negative (image y down)
    ctx.save();
    ctx.globalAlpha = 1;
    ctx.imageSmoothingEnabled = true;
    ctx.imageSmoothingQuality = 'high';
    ctx.drawImage(WORLD_MAP.image, left, top, w, h);
    ctx.restore();
}

function world_map_vis_rect() {
    if (!WORLD_MAP.calib) return null;
    const S = MAP_COORD_SCALE;
    const c = WORLD_MAP.calib;
    const left = (-c.ox / c.sx) * S;
    const top = (c.oy / c.sy) * S;
    const w = (c.imgW / c.sx) * S;
    const h = (-c.imgH / c.sy) * S;
    return { left: left, top: top, width: w, height: h };
}

function fit_to_world_map() {
    const rect = world_map_vis_rect();
    if (!rect || !(rect.width > 0) || !(rect.height > 0)) {
        network.fit({ animation: { duration: 600, easingFunction: 'easeInOutQuad' } });
        return;
    }
    const frame = (network.canvas && network.canvas.frame)
        || (network.body && network.body.container)
        || document.getElementById('mynetwork');
    const viewW = Math.max(1, frame.clientWidth || frame.offsetWidth || 800);
    const viewH = Math.max(1, frame.clientHeight || frame.offsetHeight || 600);
    const pad = 0.92;
    const scale = Math.min(viewW / Math.abs(rect.width), viewH / Math.abs(rect.height)) * pad;
    network.moveTo({
        position: {
            x: rect.left + rect.width / 2,
            y: rect.top + rect.height / 2,
        },
        scale: scale,
        animation: { duration: 600, easingFunction: 'easeInOutQuad' },
    });
}

// Captured after initial stabilization (vis zooms out via physics.stabilization.fit).
// Fallback is a typical zoomed-out scale for this large repulsion graph.
let PHYSICS_VIEW_SCALE = 0.05;

function fit_to_physics_origin() {
    zero_all_body_nodes();
    network.moveTo({
        position: { x: 0, y: 0 },
        scale: PHYSICS_VIEW_SCALE,
        animation: { duration: 600, easingFunction: 'easeInOutQuad' },
    });
}

function save_physics_layout() {
    // Keep sizes for map node scaling; positions are not restored (reset to origin).
    const sizes = {};
    nodes.get().forEach(function(node) {
        sizes[node.id] = node.size;
    });
    PHYSICS_LAYOUT_SAVE = { sizes: sizes };
}

function zero_all_body_nodes() {
    // Includes invisible dynamic-smooth support nodes that are NOT in the DataSet.
    const bodyNodes = network.body && network.body.nodes;
    if (!bodyNodes) return;
    Object.keys(bodyNodes).forEach(function(id) {
        const bn = bodyNodes[id];
        if (!bn) return;
        bn.x = 0;
        bn.y = 0;
        if (bn.vx != null) bn.vx = 0;
        if (bn.vy != null) bn.vy = 0;
    });
}

function snap_quest_nodes_to_origin() {
    const sizes = (PHYSICS_LAYOUT_SAVE && PHYSICS_LAYOUT_SAVE.sizes) || {};
    const ids = nodes.getIds();
    const updates = ids.map(function(id) {
        const u = {
            id: id,
            x: 0,
            y: 0,
            fixed: { x: false, y: false },
        };
        if (sizes[id] != null) u.size = sizes[id];
        return u;
    });
    if (updates.length) nodes.update(updates);
    ids.forEach(function(id) {
        try { network.moveNode(id, 0, 0); } catch (e) {}
    });
    zero_all_body_nodes();
}

function restore_graph_edge_options() {
    network.setOptions({
        nodes: {
            font: {
                size: 120,
                strokeWidth: 11,
                strokeColor: BACKGROUND_COLOR,
            },
            borderWidthSelected: NODE_BORDER_EMPHASIS,
            chosen: { node: match_hover_select_node },
        },
        edges: {
            smooth: { enabled: true, type: 'dynamic' },
            hoverWidth: PHYSICS_EDGE_EMPHASIS,
            selectionWidth: PHYSICS_EDGE_EMPHASIS,
        },
    });
}

function disable_world_map(opts) {
    opts = opts || {};
    const restorePhysics = opts.restorePhysics !== false;
    const edgeWidths = (WORLD_MAP.saved && WORLD_MAP.saved.edgeWidths) || {};
    const edgeHidden = (WORLD_MAP.saved && WORLD_MAP.saved.edgeHidden) || {};
    WORLD_MAP.enabled = false;
    WORLD_MAP.simple = false;
    WORLD_MAP.edgeless = false;
    WORLD_MAP.saved = null;
    LAYOUT = 'physics';

    set_network_physics(false);
    // Straight edges first so we do not spawn dynamic supports at map coords.
    network.setOptions({
        nodes: {
            font: { size: 120, strokeWidth: 11, strokeColor: BACKGROUND_COLOR },
            borderWidthSelected: NODE_BORDER_EMPHASIS,
            chosen: { node: match_hover_select_node },
        },
        edges: { smooth: false, hoverWidth: PHYSICS_EDGE_EMPHASIS, selectionWidth: PHYSICS_EDGE_EMPHASIS },
    });

    // Restore pre-map edge widths/visibility (colors come from changeColor next).
    const edgeRestores = edges.get().map(function(edge) {
        const w = edgeWidths[edge.id];
        return {
            id: edge.id,
            width: w == null ? 24 : w,
            hidden: edgeHidden[edge.id] == null ? false : edgeHidden[edge.id],
        };
    });
    if (edgeRestores.length) edges.update(edgeRestores);

    snap_quest_nodes_to_origin();
    restore_graph_edge_options();
    snap_quest_nodes_to_origin();

    set_network_physics(!!restorePhysics);
    // Colors MUST be last among data updates — later nodes.update wiped them before.
    window.changeColor();
    fit_to_physics_origin();
}

function sync_map_edges() {
    if (!WORLD_MAP.enabled) return;
    const updates = edges.get().map(function(edge) {
        if (should_hide_map_edge(edge)) {
            return {
                id: edge.id,
                hidden: true,
                physics: false,
                width: MAP_EDGE_WIDTH,
            };
        }
        const endpointsHidden = network.getConnectedNodes(edge.id).some(function(n) {
            const cn = nodes.get(n);
            return !cn || !cn.show;
        });
        const toggle_completed = document.getElementById('toggle_completed')
            && document.getElementById('toggle_completed').checked;
        if (endpointsHidden && !toggle_completed) {
            return { id: edge.id, hidden: true, physics: false, width: MAP_EDGE_WIDTH };
        }
        const fromNode = nodes.get(edge.from);
        const scheme = (($('#color_scheme').val() || 'shell') + '').toLowerCase().replace(/ /g, '_');
        return {
            id: edge.id,
            hidden: false,
            physics: false,
            width: MAP_EDGE_WIDTH,
            color: endpointsHidden ? DISABLED_EDGE_COLOR : scheme_color_for(fromNode, scheme),
        };
    });
    if (updates.length) edges.update(updates);
}

function enable_world_map(opts) {
    opts = opts || {};
    if (!WORLD_MAP.available) return;
    apply_map_mode_flags(opts.mode || (opts.simple ? 'map_simple' : 'map'));
    // Capture physics-layout sizes once when entering map (kept across map variants).
    if (LAYOUT === 'physics' || !PHYSICS_LAYOUT_SAVE) {
        save_physics_layout();
    }
    const bounds = world_map_bounds();
    const center = game_to_vis_xy(
        (bounds.xMin + bounds.xMax) / 2,
        (bounds.yMin + bounds.yMax) / 2
    );
    const scheme = (($('#color_scheme').val() || 'shell') + '').toLowerCase().replace(/ /g, '_');
    const updates = [];
    const savedEdgeWidths = {};
    const savedEdgeHidden = {};
    nodes.get().forEach(function(node) {
        const start = node_start_xy(node);
        const xy = start ? game_to_vis_xy(start.x, start.y) : center;
        const baseSize = (PHYSICS_LAYOUT_SAVE && PHYSICS_LAYOUT_SAVE.sizes[node.id] != null)
            ? PHYSICS_LAYOUT_SAVE.sizes[node.id]
            : (node.size || 25);
        updates.push({
            id: node.id,
            x: xy.x,
            y: xy.y,
            size: Math.max(MAP_NODE_SIZE_MIN, baseSize * MAP_NODE_SIZE_FACTOR),
            color: scheme_color_for(node, scheme),
            style: scheme,
            fixed: { x: true, y: true },
            physics: false,
        });
    });
    edges.get().forEach(function(edge) {
        savedEdgeWidths[edge.id] = edge.width;
        savedEdgeHidden[edge.id] = !!edge.hidden;
    });
    WORLD_MAP.saved = {
        edgeWidths: savedEdgeWidths,
        edgeHidden: savedEdgeHidden,
    };
    WORLD_MAP.enabled = true;
    LAYOUT = 'map';
    set_network_physics(false);
    network.setOptions({
        nodes: {
            font: { size: MAP_FONT_SIZE, strokeWidth: MAP_FONT_STROKE },
            borderWidthSelected: NODE_BORDER_EMPHASIS,
            chosen: { node: match_hover_select_node },
        },
        edges: {
            smooth: false,
            hoverWidth: MAP_EDGE_EMPHASIS,
            selectionWidth: MAP_EDGE_EMPHASIS,
        },
    });
    nodes.update(updates);
    updates.forEach(function(u) {
        try { network.moveNode(u.id, u.x, u.y); } catch (e) {}
    });
    if (!WORLD_MAP._drawBound) {
        network.on('beforeDrawing', world_map_draw);
        WORLD_MAP._drawBound = true;
    }
    if (typeof window.changeColor === 'function') window.changeColor();
    network.redraw();
    fit_to_world_map();
}

function is_map_display_mode(mode) {
    return mode === 'map' || mode === 'map_simple' || mode === 'map_edgeless';
}

window.setDisplayMode = function(mode) {
    const next = mode || 'physics';
    const prev = DISPLAY_MODE;
    if (next === prev) return;

    if (!WORLD_MAP.available && is_map_display_mode(next)) {
        const sel = document.getElementById('display_mode');
        if (sel) sel.value = prev;
        return;
    }

    const wasMap = is_map_display_mode(prev);
    const willMap = is_map_display_mode(next);

    if (wasMap && willMap) {
        // Map variants: same layout/view; only toggle edge visibility.
        apply_map_mode_flags(next);
        window.changeColor();
        network.redraw();
    } else if (!wasMap && willMap) {
        enable_world_map({ mode: next });
    } else if (wasMap && !willMap) {
        disable_world_map({ restorePhysics: next === 'physics' });
    } else {
        // Physics <-> No physics: same layout, freeze/resume without moving nodes.
        set_network_physics(next === 'physics');
    }

    DISPLAY_MODE = next;
    const sel = document.getElementById('display_mode');
    if (sel && sel.value !== next) sel.value = next;
};

function install_display_mode() {
    if (WORLD_MAP.available) {
        const img = new Image();
        img.onload = function() { prepare_world_map_image(img); };
        img.onerror = function() {
            console.error('Failed to load world map image:', MAP_IMAGE_URL);
        };
        img.src = MAP_IMAGE_URL;
        if (img.complete && img.naturalWidth) {
            prepare_world_map_image(img);
        }
    }
    const sel = document.getElementById('display_mode');
    if (sel) DISPLAY_MODE = sel.value || 'physics';
}
install_display_mode();

/* Execute */
nodes.forEach(function(node) {
    nodes.update({id: node.id, show: true});
});
window.changeColor();

// Record the post-stabilization camera scale (same zoom the app starts with).
network.once('stabilizationIterationsDone', function() {
    setTimeout(function() {
        const s = network.getScale();
        if (s && s > 0) PHYSICS_VIEW_SCALE = s;
    }, 550);
});
