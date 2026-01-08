import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import io
import networkx as nx

INTERIOR_LOBBY = ["File DV6","Password DV6","Password DV8","Skunk","Wisp","Killer"]
INTERIOR_BASIC = ["Hellhound","Sabertooth","Raven x2" ,"Hellhound","Wisp","Raven","Password DV6" ,"File DV6" ,"Control Node DV6" ,"Password DV6" ,"Skunk","Asp","Scorpion","Killer, Skunk","Wisp x3" ,"Liche"]
INTERIOR_STANDARD = ["Hellhound x2","Hellhound, Killer","Skunk x2","Sabertooth","Scorpion","Hellhound","Password DV8","File DV8","Control Node DV8","Password DV8","Asp","Killer","Liche","Asp","Raven x3","Liche, Raven"]
INTERIOR_UNCOMMON = ["Kraken","Hellhound, Scorpion","Hellhound, Killer","Raven x2","Sabertooth","Hellhound","Password DV10","File DV10","Control Node DV10","Password DV10","Killer","Liche","Dragon","Asp, Raven","Dragon, Wisp","Giant"]
INTERIOR_ADVANCED = ["Hellhound x3","Asp x2","Hellhound, Liche","Wisp x3","Hellhound, Sabertooth","Kraken","Password DV12","File DV12","Control Node DV12","Password DV12","Giant","Dragon","Killer, Scorpion","Kraken","Raven, Wisp, Hellhound","Dragon x2"]

def get_occupancy_name(floor, difficulty):
    """Get the occupancy name for a floor based on difficulty"""
    if floor.level <= 2:
        return INTERIOR_LOBBY[floor.occupancy-1]
    
    if difficulty == 1:
        return INTERIOR_BASIC[floor.occupancy-3]
    elif difficulty == 2:
        return INTERIOR_STANDARD[floor.occupancy-3]
    elif difficulty == 3:
        return INTERIOR_UNCOMMON[floor.occupancy-3]
    elif difficulty == 4:
        return INTERIOR_ADVANCED[floor.occupancy-3]
    return "Unknown"

def get_node_color(floor, difficulty):
    """Determine node color based on content type"""
    occupancy = get_occupancy_name(floor, difficulty)
    
    # Entry nodes
    if floor.level <= 2 and not any(ice in occupancy for ice in ['Hellhound', 'Sabertooth', 'Raven', 'Wisp', 'Killer', 'Asp', 'Scorpion', 'Liche', 'Kraken', 'Dragon', 'Giant', 'Skunk']):
        return '#4A90E2'  # Blue for lobby
    
    # ICE types
    if any(ice in occupancy for ice in ['Hellhound', 'Sabertooth', 'Raven', 'Wisp', 'Killer', 'Asp', 'Scorpion', 'Liche', 'Kraken', 'Dragon', 'Giant', 'Skunk']):
        return '#E74C3C'  # Red for ICE
    
    # Files and passwords
    if 'File' in occupancy or 'Password' in occupancy:
        return '#F39C12'  # Orange for files/passwords
    
    # Control nodes
    if 'Control Node' in occupancy:
        return '#9B59B6'  # Purple for control nodes
    
    return '#95A5A6'  # Gray default

def hierarchy_pos(G, root, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5):
    """
    Create a hierarchical layout for a tree graph.
    Returns a dictionary of positions keyed by node.
    """
    pos = _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)
    return pos

def _hierarchy_pos(G, root, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5, pos=None, parent=None, parsed=[]):
    if pos is None:
        pos = {root: (xcenter, vert_loc)}
    else:
        pos[root] = (xcenter, vert_loc)
    
    children = list(G.neighbors(root))
    if not isinstance(G, nx.DiGraph) and parent is not None:
        children.remove(parent)
    
    if len(children) != 0:
        dx = width / len(children)
        nextx = xcenter - width/2 - dx/2
        for child in children:
            nextx += dx
            pos = _hierarchy_pos(G, child, width=dx, vert_gap=vert_gap,
                                vert_loc=vert_loc-vert_gap, xcenter=nextx,
                                pos=pos, parent=root, parsed=parsed)
    return pos

def create_network_graph(floors, difficulty):
    """Create a networkx graph from the floor structure"""
    G = nx.DiGraph()
    
    def add_to_graph(floor):
        occupancy = get_occupancy_name(floor, difficulty)
        color = get_node_color(floor, difficulty)
        
        # Truncate long occupancy names
        short_name = occupancy[:25] + "..." if len(occupancy) > 25 else occupancy
        
        G.add_node(floor.id, 
                   label=f"[{floor.id}]\n{short_name}",
                   color=color,
                   level=floor.level)
        
        for child in floor.childs:
            G.add_edge(floor.id, child.id)
            add_to_graph(child)
    
    add_to_graph(floors[0])
    return G

def create_network_diagram_matplotlib(floors, difficulty):
    """
    Create a visual network architecture diagram using matplotlib and networkx
    Returns: bytes of PNG image
    """
    G = create_network_graph(floors, difficulty)
    
    # Use custom hierarchical layout with better centering
    root = floors[0].id
    pos = hierarchy_pos(G, root, width=2., vert_gap=0.5, xcenter=0)
    
    # Create figure with dark background
    fig, ax = plt.subplots(figsize=(14, 10), facecolor='#0a0a0a')
    ax.set_facecolor('#0a0a0a')
    ax.axis('off')
    
    # Get colors and labels for each node
    node_colors = [G.nodes[node]['color'] for node in G.nodes()]
    node_labels = {node: G.nodes[node]['label'] for node in G.nodes()}
    
    # Draw edges first (so they appear behind nodes)
    nx.draw_networkx_edges(G, pos, ax=ax, 
                          edge_color='#00FF41', 
                          width=2.5, 
                          arrows=True,
                          arrowsize=20,
                          arrowstyle='->',
                          connectionstyle='arc3,rad=0.1')
    
    # Draw nodes (rounded rectangles for better look)
    nx.draw_networkx_nodes(G, pos, ax=ax,
                          node_color=node_colors,
                          node_size=4000,
                          node_shape='o',  # Changed to circle
                          edgecolors='#00FF41',
                          linewidths=2.5)
    
    # Draw labels with better formatting
    for node, (x, y) in pos.items():
        label = node_labels[node]
        # Split long labels into multiple lines
        if len(label) > 20:
            parts = label.split('\n')
            if len(parts[1]) > 20:
                # Wrap occupancy text
                words = parts[1].split()
                lines = [parts[0]]  # Keep [ID] on first line
                current_line = ""
                for word in words:
                    if len(current_line + " " + word) <= 15:
                        current_line += (" " if current_line else "") + word
                    else:
                        if current_line:
                            lines.append(current_line)
                        current_line = word
                if current_line:
                    lines.append(current_line)
                label = '\n'.join(lines)
        
        ax.text(x, y, label,
               horizontalalignment='center',
               verticalalignment='center',
               fontsize=8,
               color='white',
               fontweight='bold',
               fontfamily='monospace',
               bbox=dict(boxstyle='round,pad=0.4', facecolor='#1a1a1a', 
                        edgecolor='none', alpha=0.7))
    
    # Add title
    plt.title('Network Architecture', 
              color='#00FF41', 
              fontsize=18, 
              fontweight='bold',
              fontfamily='monospace',
              pad=20)
    
    # Create legend
    legend_elements = [
        mpatches.Patch(color='#4A90E2', label='Entry/Lobby'),
        mpatches.Patch(color='#E74C3C', label='ICE'),
        mpatches.Patch(color='#F39C12', label='Files/Passwords'),
        mpatches.Patch(color='#9B59B6', label='Control Nodes')
    ]
    ax.legend(handles=legend_elements, 
             loc='upper right',
             facecolor='#1a1a1a',
             edgecolor='#00FF41',
             labelcolor='white',
             fontsize=11,
             framealpha=0.9)
    
    # Set axis limits to center the content
    x_coords = [coord[0] for coord in pos.values()]
    y_coords = [coord[1] for coord in pos.values()]
    x_margin = (max(x_coords) - min(x_coords)) * 0.2 + 0.5
    y_margin = (max(y_coords) - min(y_coords)) * 0.1 + 0.5
    
    ax.set_xlim(min(x_coords) - x_margin, max(x_coords) + x_margin)
    ax.set_ylim(min(y_coords) - y_margin, max(y_coords) + y_margin)
    
    plt.tight_layout()
    
    # Save to bytes
    buf = io.BytesIO()
    plt.savefig(buf, format='png', facecolor='#0a0a0a', dpi=150, bbox_inches='tight')
    buf.seek(0)
    plt.close()
    
    return buf.getvalue()

def create_simple_network_diagram_matplotlib(floors, difficulty):
    """
    Create a simpler diagram with just node IDs
    Returns: bytes of PNG image
    """
    G = create_network_graph(floors, difficulty)
    
    # Use custom hierarchical layout with centering
    root = floors[0].id
    pos = hierarchy_pos(G, root, width=2., vert_gap=0.4, xcenter=0)
    
    fig, ax = plt.subplots(figsize=(12, 9), facecolor='#0a0a0a')
    ax.set_facecolor('#0a0a0a')
    ax.axis('off')
    
    node_colors = [G.nodes[node]['color'] for node in G.nodes()]
    
    # Draw edges
    nx.draw_networkx_edges(G, pos, ax=ax,
                          edge_color='#00FF41',
                          width=3,
                          arrows=True,
                          arrowsize=18,
                          arrowstyle='->',
                          connectionstyle='arc3,rad=0.1')
    
    # Draw nodes (circles for simple view)
    nx.draw_networkx_nodes(G, pos, ax=ax,
                          node_color=node_colors,
                          node_size=2000,
                          edgecolors='#00FF41',
                          linewidths=3)
    
    # Draw just the ID numbers
    id_labels = {node: str(node) for node in G.nodes()}
    nx.draw_networkx_labels(G, pos, id_labels, ax=ax,
                           font_size=14,
                           font_color='white',
                           font_weight='bold',
                           font_family='monospace')
    
    plt.title('Network Architecture Map',
              color='#00FF41',
              fontsize=16,
              fontweight='bold',
              fontfamily='monospace',
              pad=20)
    
    # Add legend
    legend_elements = [
        mpatches.Patch(color='#4A90E2', label='Entry/Lobby'),
        mpatches.Patch(color='#E74C3C', label='ICE'),
        mpatches.Patch(color='#F39C12', label='Files/Passwords'),
        mpatches.Patch(color='#9B59B6', label='Control Nodes')
    ]
    ax.legend(handles=legend_elements, 
             loc='upper right',
             facecolor='#1a1a1a',
             edgecolor='#00FF41',
             labelcolor='white',
             fontsize=10,
             framealpha=0.9)
    
    # Set axis limits to center the content
    x_coords = [coord[0] for coord in pos.values()]
    y_coords = [coord[1] for coord in pos.values()]
    x_margin = (max(x_coords) - min(x_coords)) * 0.2 + 0.5
    y_margin = (max(y_coords) - min(y_coords)) * 0.1 + 0.5
    
    ax.set_xlim(min(x_coords) - x_margin, max(x_coords) + x_margin)
    ax.set_ylim(min(y_coords) - y_margin, max(y_coords) + y_margin)
    
    plt.tight_layout()
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', facecolor='#0a0a0a', dpi=150, bbox_inches='tight')
    buf.seek(0)
    plt.close()
    
    return buf.getvalue()