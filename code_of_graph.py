import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch, Patch
from matplotlib.path import Path
import numpy as np

# Data
data = {
    "rows": [
        {"DEPT": "LOAN", "DESIGN": "MANAGER", "EMP_ID": 101, "FNAME": "RAJU", "LNAME": "RASTOGI", "PRICE": "0.80000", "SALARY": 37000},
        {"DEPT": "CASH", "DESIGN": "CASHIER", "EMP_ID": 102, "FNAME": "SHAM", "LNAME": "MOHAN", "PRICE": '0.9120', "SALARY": 32000},
        {"DEPT": "LOAN", "DESIGN": "ASOCIATE", "EMP_ID": 103, "FNAME": "BABURAO", "LNAME": "APTE", "PRICE": '1.342', "SALARY": 25000},
        {"DEPT": "ACCOUNT", "DESIGN": "ACCOUNTANT", "EMP_ID": 104, "FNAME": "PAUL", "LNAME": "PHILIP", "PRICE": '0.2334', "SALARY": 45000},
        {"DEPT": "ACCOUNT", "DESIGN": "ACCOUNTANT", "EMP_ID": 105, "FNAME": "PAUL", "LNAME": "PHILIP", "PRICE": '1.4543', "SALARY": 45000},
        {"DEPT": "DEPOSITE", "DESIGN": "ASSOCIATE", "EMP_ID": 106, "FNAME": "ALEX", "LNAME": "WATT", "PRICE": '4.5643', "SALARY": 35000},
        {"DEPT": "CASH", "DESIGN": "LEAD", "EMP_ID": 107, "FNAME": "LEENA", "LNAME": "JHONSON", "PRICE":'6.563', "SALARY": 25000},
        {"DEPT": "IT", "DESIGN": "MANAGER", "EMP_ID": 108, "FNAME": "JHON", "LNAME": "PAUL", "PRICE": '0.2331', "SALARY": 75000},
        {"DEPT": "LOAN", "DESIGN": "PROBATION", "EMP_ID": 109, "FNAME": "ALEX", "LNAME": "WATT", "PRICE": '4.232', "SALARY": 40000}
    ]
}

# Extract names, prices, and salaries
names = [f"{row['FNAME']} {row['LNAME']}" for row in data['rows']]
prices = [float(row['PRICE']) * 10000 if row['PRICE'] is not None else 0 for row in data['rows']]
salaries = [row['SALARY'] for row in data['rows']]

# Create figure and axis with dark background
fig, ax = plt.subplots(figsize=(16, 8), facecolor='#1e2836')
ax.set_facecolor('#1e2836')

# Bar properties
bar_width = 0.35
x_positions = np.arange(len(names))
max_value = max(max(salaries), max(prices))

# Function to create a gradient bar with curved top
def create_gradient_curved_bar(ax, x, width, height, gradient_colors, radius=1200):
    """Create a bar with gradient fill and curved top"""
    
    if height <= 0:
        return
    
    # Calculate where the curve starts
    rect_height = max(0, height - radius)
    
    # Create the curved top using arc
    theta = np.linspace(0, np.pi, 100)
    x_curve = (width/2) * np.cos(theta) + x
    y_curve = radius * np.sin(theta) + rect_height
    
    # Create vertices for the entire bar
    vertices = []
    vertices.append([x - width/2, 0])
    vertices.append([x - width/2, rect_height])
    for xc, yc in zip(x_curve, y_curve):
        vertices.append([xc, yc])
    vertices.append([x + width/2, rect_height])
    vertices.append([x + width/2, 0])
    vertices.append([x - width/2, 0])
    
    codes = [Path.MOVETO] + [Path.LINETO] * (len(vertices) - 2) + [Path.CLOSEPOLY]
    path = Path(vertices, codes)
    
    # Create gradient by drawing horizontal segments
    num_segments = 50
    for i in range(num_segments):
        segment_height = height / num_segments
        y_bottom = i * segment_height
        y_top = (i + 1) * segment_height
        
        # Color gradient
        ratio = i / num_segments
        color_bottom = gradient_colors[0]
        color_top = gradient_colors[1]
        
        r = int(color_bottom[0] + (color_top[0] - color_bottom[0]) * ratio)
        g = int(color_bottom[1] + (color_top[1] - color_bottom[1]) * ratio)
        b = int(color_bottom[2] + (color_top[2] - color_bottom[2]) * ratio)
        color = f'#{r:02x}{g:02x}{b:02x}'
        
        # Create segment vertices
        if y_top <= rect_height:
            # Rectangular segment
            segment_vertices = [
                [x - width/2, y_bottom], 
                [x - width/2, y_top],
                [x + width/2, y_top], 
                [x + width/2, y_bottom],
                [x - width/2, y_bottom]
            ]
        elif y_bottom >= rect_height:
            # Curved segment
            theta_range = np.linspace(0, np.pi, 100)
            y_curve_vals = radius * np.sin(theta_range) + rect_height
            mask = (y_curve_vals >= y_bottom) & (y_curve_vals <= y_top)
            
            if not mask.any():
                continue
                
            x_curve_segment = (width/2) * np.cos(theta_range[mask]) + x
            y_curve_segment = y_curve_vals[mask]
            
            segment_vertices = [[x - width/2, y_bottom]]
            if y_bottom == rect_height:
                segment_vertices.append([x - width/2, rect_height])
            
            for xc, yc in zip(x_curve_segment, y_curve_segment):
                segment_vertices.append([xc, yc])
            
            segment_vertices.append([x + width/2, y_bottom])
            segment_vertices.append([x - width/2, y_bottom])
        else:
            # Crosses the boundary
            segment_vertices = [
                [x - width/2, y_bottom], 
                [x - width/2, rect_height]
            ]
            
            theta_range = np.linspace(0, np.pi, 100)
            y_curve_vals = radius * np.sin(theta_range) + rect_height
            mask = (y_curve_vals >= rect_height) & (y_curve_vals <= y_top)
            
            if mask.any():
                x_curve_segment = (width/2) * np.cos(theta_range[mask]) + x
                y_curve_segment = y_curve_vals[mask]
                for xc, yc in zip(x_curve_segment, y_curve_segment):
                    segment_vertices.append([xc, yc])
            
            segment_vertices.append([x + width/2, rect_height])
            segment_vertices.append([x + width/2, y_bottom])
            segment_vertices.append([x - width/2, y_bottom])
        
        # Create and add segment patch
        segment_codes = [Path.MOVETO] + [Path.LINETO] * (len(segment_vertices) - 2) + [Path.CLOSEPOLY]
        segment_path = Path(segment_vertices, segment_codes)
        segment_patch = PathPatch(segment_path, facecolor=color, edgecolor='none', alpha=0.9)
        ax.add_patch(segment_patch)
    
    # Add border
    border_color = gradient_colors[1]
    patch = PathPatch(path, facecolor='none', 
                     edgecolor=f'#{border_color[0]:02x}{border_color[1]:02x}{border_color[2]:02x}', 
                     linewidth=1.5, alpha=0.6)
    ax.add_patch(patch)

# Define gradient colors
# Blue gradient for Price
price_gradient = [(0x3d, 0x5a, 0x80), (0x00, 0xb4, 0xd8)]  # Dark blue to bright blue
# Green gradient for Salary  
salary_gradient = [(0x2d, 0x6a, 0x4f), (0x06, 0xff, 0xa5)]  # Dark green to bright cyan/green

# Create bars for each employee
for i, (x_pos, price, salary) in enumerate(zip(x_positions, prices, salaries)):
    # Price bar (left)
    price_x = x_pos - bar_width/2
    create_gradient_curved_bar(ax, price_x, bar_width, price, price_gradient, radius=1200)
    
    if price > 0:
        ax.text(price_x, price + max_value*0.02, f'{price:,.0f}', 
                ha='center', va='bottom', fontsize=9, fontweight='bold', color='#00b4d8')
    
    # Salary bar (right)
    salary_x = x_pos + bar_width/2
    create_gradient_curved_bar(ax, salary_x, bar_width, salary, salary_gradient, radius=1200)
    ax.text(salary_x, salary + max_value*0.02, f'{salary:,}', 
            ha='center', va='bottom', fontsize=9, fontweight='bold', color='#06ffa5')

# Set axis properties
ax.set_xlim(-0.5, len(names) - 0.5)
ax.set_ylim(0, max_value * 1.15)
ax.set_xticks(x_positions)
ax.set_xticklabels(names, rotation=45, ha='right', fontsize=11, color='white')
ax.set_ylabel('Amount ', fontsize=13, fontweight='bold', color='white')
ax.set_xlabel('Employee Name', fontsize=13, fontweight='bold', color='white')
ax.set_title('Employee Price vs Salary Comparison', 
             fontsize=16, fontweight='bold', pad=20, color='white')

# Add grid
ax.grid(axis='y', alpha=0.2, linestyle='--', linewidth=0.7, color='white')
ax.set_axisbelow(True)

# Style the plot
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('white')
ax.spines['bottom'].set_color('white')
ax.spines['left'].set_linewidth(1.5)
ax.spines['bottom'].set_linewidth(1.5)
ax.tick_params(colors='white')

# Add legend
legend_elements = [
    Patch(facecolor='#00b4d8', label='Price', alpha=0.8),
    Patch(facecolor='#06ffa5', label='Salary', alpha=0.8)
]
ax.legend(handles=legend_elements, loc='upper left', fontsize=12, 
          frameon=True, facecolor='#2a3f54', edgecolor='white', 
          labelcolor='white', framealpha=0.8)

plt.tight_layout()
plt.show()