def print_nested_profile(stats, threshold=0.1, max_indent=3):
    "Print nested profile showing call hierarchy: name, calls, cum, self, % of total. Shows all entries with cum >= threshold."
    from collections import defaultdict
    stats.calc_callees()
    items = list(stats.stats.items())  # (func, (cc, ncalls, tt, ct, callers?))
    def cum(v): return v[3] if len(v) > 3 else (v[2] if len(v) > 2 else 0.0)
    def tt(v):  return v[2] if len(v) > 2 else 0.0
    cum_map = {k: cum(v) for k, v in items}
    ncalls_map = {k: (v[1] if len(v) > 1 else 0) for k, v in items}
    self_map = {}
    # Build call graph: children[caller] = list of callees
    children = defaultdict(list)
    callers_map = defaultdict(set)  # callers_map[callee] = set of callers
    for fn, vals in items:
        callers = vals[4] if len(vals) > 4 else {}
        if isinstance(callers, dict):
            for caller in callers:
                children[caller].append(fn)
                callers_map[fn].add(caller)
    # Calculate self time
    for fn, vals in items:
        if len(vals) > 2 and vals[2] is not None:
            self_map[fn] = tt(vals)
        else:
            child_sum = sum(cum_map.get(ch,0.0) for ch in children.get(fn,[]))
            self_map[fn] = max(0.0, cum_map.get(fn,0.0) - child_sum)
    total = getattr(stats, "total_tt", None) or (sum(cum_map.values()) or 1.0)
    def name(k):
        if isinstance(k, tuple) and len(k) >= 3: return f"{k[2]}:{k[1]}"
        return str(k)
    # Find root functions (not called by others)
    all_funcs = set(cum_map.keys())
    root_funcs = [f for f in all_funcs if not callers_map.get(f)]
    if not root_funcs:
        # If no clear roots, use functions with highest cumulative time
        root_funcs = sorted(all_funcs, key=lambda f: cum_map.get(f,0.0), reverse=True)[:1]
    # Build tree structure
    def build_tree(func, visited=None):
        if visited is None:
            visited = set()
        if func in visited:
            return None  # Cycle detected
        visited.add(func)
        node = {
            'func': func,
            'cum': cum_map.get(func, 0.0),
            'self': self_map.get(func, 0.0),
            'ncalls': ncalls_map.get(func, 0),
            'children': []
        }
        # Sort children by cumulative time descending
        child_funcs = sorted(children.get(func, []), key=lambda f: cum_map.get(f,0.0), reverse=True)
        for child in child_funcs:
            child_node = build_tree(child, visited.copy())
            if child_node:
                node['children'].append(child_node)
        visited.remove(func)
        return node
    # Build trees for root functions
    trees = []
    for root in root_funcs:
        tree = build_tree(root)
        if tree:
            trees.append(tree)
    # Sort trees by cumulative time
    trees.sort(key=lambda t: t['cum'], reverse=True)
    # Filter tree: keep only nodes with percentage >= threshold
    def filter_tree(node):
        """Filter tree, keeping only nodes with percentage >= threshold."""
        node_pct = (node['cum']/total)*100 if total else 0.0
        filtered_children = []
        for child in node['children']:
            child_pct = (child['cum']/total)*100 if total else 0.0
            if child_pct >= threshold:
                filtered_child = filter_tree(child)
                if filtered_child:
                    filtered_children.append(filtered_child)
        
        # If node itself is below threshold, return None
        if node_pct < threshold:
            return None
        
        # Create filtered node
        filtered_node = {
            'func': node['func'],
            'cum': node['cum'],
            'self': node['self'],
            'ncalls': node['ncalls'],
            'children': filtered_children
        }
        return filtered_node
    
    # Filter trees
    filtered_trees = []
    for tree in trees:
        tree_pct = (tree['cum']/total)*100 if total else 0.0
        if tree_pct >= threshold:
            filtered_tree = filter_tree(tree)
            if filtered_tree:
                filtered_trees.append(filtered_tree)
    
    # Print header
    print(f"{'cum(s)':>9}  {'self(s)':>9}  {'calls':>6}  {'%':>7}  name")
    # Print nested structure
    def print_node(node, depth=0, visited=None):
        if visited is None:
            visited = set()
        if node['func'] in visited:
            return
        visited.add(node['func'])
        indent = "  " * depth
        ncalls = node['ncalls']
        c = node['cum']
        s = node['self']
        pct = (c/total)*100 if total else 0.0
        nm = name(node['func'])
        print(f"{c:7.1f} s  {s:7.1f} s  {ncalls:6d}  {pct:6.0f}%  {indent}{nm}")
        # Only print children if we haven't reached max_indent
        if depth < max_indent:
            # Sort children by cumulative time and print them
            for child in sorted(node['children'], key=lambda ch: ch['cum'], reverse=True):
                print_node(child, depth + 1, visited.copy())
        visited.remove(node['func'])
    # Print filtered trees
    for tree in filtered_trees:
        print_node(tree)

