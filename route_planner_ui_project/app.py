import tkinter as tk
from tkinter import messagebox
from graph import Graph
from algorithms import bfs, dijkstra
import random
import math

g = Graph()

# Store node positions and canvas items for visualization
node_positions = {}
node_items = {}  # Maps city to (oval_id, text_id)
edge_items = {}  # Maps (city1, city2) to line_id
NODE_RADIUS = 20
CANVAS_WIDTH = 600
CANVAS_HEIGHT = 400

# Dynamic input frame
input_frame = None

# Interaction state
dragging_node = None
selected_node = None
selected_edge = None

def clear_input_frame():
    global input_frame
    if input_frame:
        input_frame.destroy()
        input_frame = None

def add_city():
    clear_input_frame()
    global input_frame
    input_frame = tk.Frame(sidebar, bg="#f0f0f0")
    input_frame.pack(fill="x", padx=5, pady=5)
    
    tk.Label(input_frame, text="City name:", bg="#f0f0f0", font=("Arial", 10)).pack(anchor="w", padx=5)
    city_entry = tk.Entry(input_frame, font=("Arial", 10))
    city_entry.pack(fill="x", padx=5, pady=2)
    
    def submit():
        city = city_entry.get().strip()
        if not city:
            update_status("City name cannot be empty.")
            return
        if city in g.get_graph():
            update_status(f"Error: City '{city}' already exists.")
            return
        g.add_city(city)
        node_positions[city] = (random.randint(50, CANVAS_WIDTH-50), random.randint(50, CANVAS_HEIGHT-50))
        update_status(f"Added city: {city}")
        update_canvas()
        clear_input_frame()
    
    tk.Button(input_frame, text="Submit", command=submit, **submit_button_style).pack(side="left", padx=5, pady=2)
    tk.Button(input_frame, text="Cancel", command=clear_input_frame, **submit_button_style).pack(side="left", padx=5, pady=2)

def add_road():
    clear_input_frame()
    global input_frame
    input_frame = tk.Frame(sidebar, bg="#f0f0f0")
    input_frame.pack(fill="x", padx=5, pady=5)
    
    tk.Label(input_frame, text="From city:", bg="#f0f0f0", font=("Arial", 10)).pack(anchor="w", padx=5)
    road_from_entry = tk.Entry(input_frame, font=("Arial", 10))
    road_from_entry.pack(fill="x", padx=5, pady=2)
    tk.Label(input_frame, text="To city:", bg="#f0f0f0", font=("Arial", 10)).pack(anchor="w", padx=5)
    road_to_entry = tk.Entry(input_frame, font=("Arial", 10))
    road_to_entry.pack(fill="x", padx=5, pady=2)
    tk.Label(input_frame, text="Distance:", bg="#f0f0f0", font=("Arial", 10)).pack(anchor="w", padx=5)
    road_distance_entry = tk.Entry(input_frame, font=("Arial", 10))
    road_distance_entry.pack(fill="x", padx=5, pady=2)
    
    def submit():
        c1 = road_from_entry.get().strip()
        c2 = road_to_entry.get().strip()
        distance = road_distance_entry.get().strip()
        if not c1 or not c2:
            update_status("City names cannot be empty.")
            return
        if c1 not in g.get_graph():
            update_status(f"Error: City '{c1}' does not exist.")
            return
        if c2 not in g.get_graph():
            update_status(f"Error: City '{c2}' does not exist.")
            return
        if any(neighbor[0] == c2 for neighbor in g.get_graph().get(c1, [])):
            update_status(f"Error: Road from '{c1}' to '{c2}' already exists.")
            return
        try:
            distance = int(distance)
            if distance <= 0:
                update_status("Error: Distance must be a positive integer.")
                return
        except:
            update_status("Error: Invalid distance.")
            return
        g.add_road(c1, c2, distance)
        update_status(f"Road added from {c1} to {c2} with distance {distance}")
        update_canvas()
        clear_input_frame()
    
    tk.Button(input_frame, text="Submit", command=submit, **submit_button_style).pack(side="left", padx=5, pady=2)
    tk.Button(input_frame, text="Cancel", command=clear_input_frame, **submit_button_style).pack(side="left", padx=5, pady=2)

def find_bfs():
    clear_input_frame()
    global input_frame
    input_frame = tk.Frame(sidebar, bg="#f0f0f0")
    input_frame.pack(fill="x", padx=5, pady=5)
    
    tk.Label(input_frame, text="Start city:", bg="#f0f0f0", font=("Arial", 10)).pack(anchor="w", padx=5)
    start_entry = tk.Entry(input_frame, font=("Arial", 10))
    start_entry.pack(fill="x", padx=5, pady=2)
    tk.Label(input_frame, text="End city:", bg="#f0f0f0", font=("Arial", 10)).pack(anchor="w", padx=5)
    end_entry = tk.Entry(input_frame, font=("Arial", 10))
    end_entry.pack(fill="x", padx=5, pady=2)
    
    def submit():
        s = start_entry.get().strip()
        e = end_entry.get().strip()
        if not s or not e:
            update_status("Start or end city cannot be empty.")
            return
        if s not in g.get_graph():
            update_status(f"Error: Start city '{s}' does not exist.")
            return
        if e not in g.get_graph():
            update_status(f"Error: End city '{e}' does not exist.")
            return
        result = bfs(g.get_graph(), s, e)
        update_status(f"BFS Path: {result}" if result else "No path found.")
        highlight_path(result)
        clear_input_frame()
    
    tk.Button(input_frame, text="Submit", command=submit, **submit_button_style).pack(side="left", padx=5, pady=2)
    tk.Button(input_frame, text="Cancel", command=clear_input_frame, **submit_button_style).pack(side="left", padx=5, pady=2)

def find_dijkstra():
    clear_input_frame()
    global input_frame
    input_frame = tk.Frame(sidebar, bg="#f0f0f0")
    input_frame.pack(fill="x", padx=5, pady=5)
    
    tk.Label(input_frame, text="Start city:", bg="#f0f0f0", font=("Arial", 10)).pack(anchor="w", padx=5)
    start_entry = tk.Entry(input_frame, font=("Arial", 10))
    start_entry.pack(fill="x", padx=5, pady=2)
    tk.Label(input_frame, text="End city:", bg="#f0f0f0", font=("Arial", 10)).pack(anchor="w", padx=5)
    end_entry = tk.Entry(input_frame, font=("Arial", 10))
    end_entry.pack(fill="x", padx=5, pady=2)
    
    def submit():
        s = start_entry.get().strip()
        e = end_entry.get().strip()
        if not s or not e:
            update_status("Start or end city cannot be empty.")
            return
        if s not in g.get_graph():
            update_status(f"Error: Start city '{s}' does not exist.")
            return
        if e not in g.get_graph():
            update_status(f"Error: End city '{e}' does not exist.")
            return
        result, dist = dijkstra(g.get_graph(), s, e)
        update_status(f"Dijkstra Path: {result}, Distance: {dist}" if result else "No path found.")
        highlight_path(result)
        clear_input_frame()
    
    tk.Button(input_frame, text="Submit", command=submit, **submit_button_style).pack(side="left", padx=5, pady=2)
    tk.Button(input_frame, text="Cancel", command=clear_input_frame, **submit_button_style).pack(side="left", padx=5, pady=2)

def delete_selected():
    global selected_node, selected_edge
    if selected_node:
        g.remove_city(selected_node)
        node_positions.pop(selected_node, None)
        node_items.pop(selected_node, None)
        edge_items.clear()  # Clear edges as they will be redrawn
        update_status(f"Removed city: {selected_node}")
        selected_node = None
        selected_edge = None
        update_canvas()
    elif selected_edge:
        c1, c2 = selected_edge
        g.remove_road(c1, c2)
        edge_items.pop(selected_edge, None)
        update_status(f"Removed road between {c1} and {c2}")
        selected_edge = None
        update_canvas()
    else:
        update_status("Error: No city or road selected.")

def update_status(text):
    status_label.config(text=text)

def find_node_at(x, y):
    for city, (nx, ny) in node_positions.items():
        if math.sqrt((x - nx)**2 + (y - ny)**2) <= NODE_RADIUS:
            return city
    return None

def find_edge_at(x, y):
    for (c1, c2), line_id in edge_items.items():
        x1, y1 = node_positions[c1]
        x2, y2 = node_positions[c2]
        # Distance from point (x, y) to line segment
        length_squared = (x2 - x1)**2 + (y2 - y1)**2
        if length_squared == 0:
            dist = math.sqrt((x - x1)**2 + (y - y1)**2)
        else:
            t = max(0, min(1, ((x - x1)*(x2 - x1) + (y - y1)*(y2 - y1)) / length_squared))
            projection_x = x1 + t * (x2 - x1)
            projection_y = y1 + t * (y2 - y1)
            dist = math.sqrt((x - projection_x)**2 + (y - projection_y)**2)
        if dist < 5:  # Tolerance for clicking on line
            return (c1, c2)
    return None

def on_node_press(event):
    global dragging_node, selected_node, selected_edge
    # Clear previous selection
    if selected_node:
        oval_id, _ = node_items[selected_node]
        canvas.itemconfig(oval_id, fill="lightblue")
        selected_node = None
    if selected_edge:
        line_id = edge_items[selected_edge]
        canvas.itemconfig(line_id, fill="black", width=2)
        selected_edge = None
    # Check for node click
    city = find_node_at(event.x, event.y)
    if city:
        dragging_node = city
        selected_node = city
        oval_id, _ = node_items[city]
        canvas.itemconfig(oval_id, fill="yellow")  # Highlight selected/dragged node
    else:
        # Check for edge click
        edge = find_edge_at(event.x, event.y)
        if edge:
            selected_edge = edge
            line_id = edge_items[edge]
            canvas.itemconfig(line_id, fill="red", width=4)  # Highlight selected edge
        update_status("Status: Ready")

def on_node_drag(event):
    if dragging_node:
        x = max(NODE_RADIUS, min(CANVAS_WIDTH - NODE_RADIUS, event.x))
        y = max(NODE_RADIUS, min(CANVAS_HEIGHT - NODE_RADIUS, event.y))
        node_positions[dragging_node] = (x, y)
        update_canvas()
        if dragging_node in node_items:
            oval_id, _ = node_items[dragging_node]
            canvas.itemconfig(oval_id, fill="yellow")  # Keep highlighted

def on_node_release(event):
    global dragging_node
    dragging_node = None
    update_canvas()
    if selected_node in node_items:
        oval_id, _ = node_items[selected_node]
        canvas.itemconfig(oval_id, fill="yellow")  # Keep selected node highlighted
    if selected_edge in edge_items:
        canvas.itemconfig(edge_items[selected_edge], fill="red", width=4)  # Keep selected edge highlighted

def update_canvas():
    canvas.delete("all")
    edge_items.clear()
    # Draw edges
    for city, neighbors in g.get_graph().items():
        if city in node_positions:
            x1, y1 = node_positions[city]
            for neighbor, distance in neighbors:
                if neighbor in node_positions:
                    x2, y2 = node_positions[neighbor]
                    line_id = canvas.create_line(x1, y1, x2, y2, fill="black", width=2)
                    edge_items[(city, neighbor)] = line_id
                    mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
                    canvas.create_text(mid_x, mid_y - 10, text=str(distance), fill="blue", font=("Arial", 10, "bold"))
    
    # Draw nodes
    node_items.clear()
    for city, (x, y) in node_positions.items():
        oval_id = canvas.create_oval(x - NODE_RADIUS, y - NODE_RADIUS, x + NODE_RADIUS, y + NODE_RADIUS, fill="lightblue", outline="black")
        text_id = canvas.create_text(x, y, text=city, font=("Arial", 10, "bold"))
        node_items[city] = (oval_id, text_id)
        if city == selected_node:
            canvas.itemconfig(oval_id, fill="yellow")  # Highlight selected node
    
    # Highlight selected edge
    if selected_edge in edge_items:
        canvas.itemconfig(edge_items[selected_edge], fill="red", width=4)

def highlight_path(path):
    update_canvas()
    if path:
        for i in range(len(path) - 1):
            city1, city2 = path[i], path[i + 1]
            if city1 in node_positions and city2 in node_positions:
                x1, y1 = node_positions[city1]
                x2, y2 = node_positions[city2]
                canvas.create_line(x1, y1, x2, y2, fill="red", width=3)

app = tk.Tk()
app.title("Route Planner")
app.geometry("800x600")

# Create main frame with grid layout
main_frame = tk.Frame(app)
main_frame.pack(fill="both", expand=True)

# Sidebar for controls
sidebar = tk.Frame(main_frame, width=200, bg="#f0f0f0")
sidebar.grid(row=0, column=0, sticky="ns", padx=5, pady=5)

# Canvas for graph visualization
canvas = tk.Canvas(main_frame, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="white", relief="sunken", borderwidth=2)
canvas.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

# Bind mouse events for dragging and selection
canvas.bind("<Button-1>", on_node_press)  # Left-click to select/start drag
canvas.bind("<B1-Motion>", on_node_drag)  # Drag node
canvas.bind("<ButtonRelease-1>", on_node_release)  # Release drag

# Configure grid weights
main_frame.grid_columnconfigure(1, weight=1)
main_frame.grid_rowconfigure(0, weight=1)

# Button and submit button styling
button_style = {"padx": 10, "pady": 5, "bg": "#4CAF50", "fg": "white", "font": ("Arial", 10, "bold")}
submit_button_style = {"padx": 5, "pady": 3, "bg": "#2196F3", "fg": "white", "font": ("Arial", 8)}

# Add buttons to sidebar
tk.Button(sidebar, text="Add City", command=add_city, **button_style).pack(fill="x", padx=5, pady=5)
tk.Button(sidebar, text="Add Road", command=add_road, **button_style).pack(fill="x", padx=5, pady=5)
tk.Button(sidebar, text="Find Path (BFS)", command=find_bfs, **button_style).pack(fill="x", padx=5, pady=5)
tk.Button(sidebar, text="Find Shortest Path (Dijkstra)", command=find_dijkstra, **button_style).pack(fill="x", padx=5, pady=5)
tk.Button(sidebar, text="Delete", command=delete_selected, **button_style).pack(fill="x", padx=5, pady=5)

# Status bar
status_label = tk.Label(app, text="Status: Ready", relief=tk.SUNKEN, anchor="w", bg="#e0e0e0")
status_label.pack(fill="x", padx=5, pady=5)

app.mainloop()