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
    nodes.forEach(function(node) {
        node.style = $('#color_scheme').val().toLowerCase().replace(' ', '_');
        color_node(node);
    });
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
color_node = function(node) {
    colors = COLORS
    const toggle_completed = document.getElementById('toggle_completed').checked;
    const show_names = document.getElementById('show_names').checked;

    selected_color = colors[node.style][node[node.style]] || DEFAULT_NODE_COLOR;

    if (!node.show) {
        if (toggle_completed) {
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

    node.color = selected_color;
    node.font = show_names
        ? {color: node.show ? NORMAL_COLOR : FADED_COLOR}
        : HIDDEN_FONT;
    nodes.update(node);

    const edge_updates = [];
    network.getConnectedEdges(node.id).forEach(function(id) {
        edge = edges.get(id);
        // As long as there are no other connected nodes that are hidden
        if (network.getConnectedNodes(id).some(function(n) { return !nodes.get(n).show; })) {
            if (toggle_completed) {
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
        edge_updates.push(edge);
    });
    if (edge_updates.length) {
        edges.update(edge_updates);
    }
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
            width: min(320px, calc(100vw - 48px));
            min-height: 0;
        }
        #quest-search-panel.expanded #quest_search_body {
            display: flex;
            flex-direction: column;
            max-height: 100%;
            min-height: 0;
            overflow: hidden;
        }
        #quest_search {
            width: 100%;
            box-sizing: border-box;
            padding: 8px 36px 8px 12px;
            border: 1px solid #555;
            border-radius: 4px;
            background: rgba(43, 43, 43, 0.92);
            color: #fff;
            outline: none;
            flex: 0 0 auto;
        }
        #quest_search:focus { border-color: #ffc107; }
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
            margin-top: 4px;
            background: rgba(43, 43, 43, 0.96);
            border: 1px solid #555;
            border-radius: 4px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.35);
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
            <i class="bi bi-info-circle"></i>
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
        const ids = nodes.get().filter(function(node) {
            if (node.hidden) return false;
            return node_matches_legend_key(node, scheme, key);
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
    document.querySelectorAll('.vis-tooltip').forEach(function(el) {
        el.style.visibility = 'hidden';
        el.style.display = 'none';
        el.style.opacity = '0';
    });
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
network.on('hold', remove_selected);
network.on('doubleClick', function(params) {
    if (params.nodes.length) {
        lookup_nodes(params.nodes);
    }
});
network.on('oncontext', function(params) {
    params.event.preventDefault();
    params.event.stopPropagation();
    hide_quest_infobox();
    const nodeId = network.getNodeAt(params.pointer.DOM);
    if (!nodeId) {
        hide_context_menu();
        return;
    }
    network.selectNodes([nodeId]);
    hide_quest_infobox();
    show_context_menu(params.event.clientX, params.event.clientY);
});

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
