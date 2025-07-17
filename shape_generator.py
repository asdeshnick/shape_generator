import plotly.graph_objects as go
import numpy as np
import random
import math

# Константы
WIDTH = 500
HEIGHT = 500
GRID_DENOMINATOR = 10
MIN_RADIUS = 3
MAX_RADIUS = 15
SQUARE_SIZE = 15

# Функция для проверки пересечения фигур
def shapes_intersect(shape1, shape2):
    # Проверка пересечения двух кругов
    if shape1['type'] == 'circle' and shape2['type'] == 'circle':
        distance = math.sqrt((shape1['x'] - shape2['x'])**2 + (shape1['y'] - shape2['y'])**2)
        return distance < (shape1['radius'] + shape2['radius'])
    
    # Проверка пересечения двух квадратов
    elif shape1['type'] == 'square' and shape2['type'] == 'square':
        return not (shape1['x'] + shape1['size'] < shape2['x'] or
                shape2['x'] + shape2['size'] < shape1['x'] or
                shape1['y'] + shape1['size'] < shape2['y'] or
                shape2['y'] + shape2['size'] < shape1['y'])
    
    # Проверка пересечения круга и квадрата
    else:
        circle = shape1 if shape1['type'] == 'circle' else shape2
        square = shape2 if shape2['type'] == 'square' else shape1
        
        closest_x = max(square['x'], min(circle['x'], square['x'] + square['size']))
        closest_y = max(square['y'], min(circle['y'], square['y'] + square['size']))
        
        distance = math.sqrt((circle['x'] - closest_x)**2 + (circle['y'] - closest_y)**2)
        return distance < circle['radius']


if __name__ == "__main__":
    fig = go.Figure()
    
    # Генерация сетки
    x_step = WIDTH / GRID_DENOMINATOR
    y_step = HEIGHT / GRID_DENOMINATOR - (GRID_DENOMINATOR // 2)
    
    for y in np.arange(0, HEIGHT, y_step):
        fig.add_trace(go.Scatter(
            x=[0, WIDTH],
            y=[y, y],
            mode='lines',
            line=dict(color='lightgray', width=0.5),
            showlegend=False,
            hoverinfo='none'
        ))
    
    for x in np.arange(0, WIDTH, x_step):
        fig.add_trace(go.Scatter(
            x=[x, x],
            y=[0, HEIGHT],
            mode='lines',
            line=dict(color='lightgray', width=0.5),
            showlegend=False,
            hoverinfo='none'
        ))

    # Генерация фигур
    placed_shapes = []
    num_shapes = random.randint(5, 15)
    
    for _ in range(num_shapes):
        attempts = 0
        max_attempts = 100
        valid_position = False
        
        while not valid_position and attempts < max_attempts:
            attempts += 1
            shape_type = random.choice(['flower', 'grass'])
            
            if shape_type == 'grass':
                radius = random.randint(MIN_RADIUS, MAX_RADIUS)
                circle_x = random.randint(radius, WIDTH - radius)
                circle_y = random.randint(radius, HEIGHT - radius)
                
                new_shape = {'type': 'circle', 'x': circle_x, 'y': circle_y, 'radius': radius}
                
                intersects = any(shapes_intersect(new_shape, s) for s in placed_shapes)
                
                if not intersects:
                    placed_shapes.append(new_shape)
                    fig.add_trace(go.Scatter(
                        x=[circle_x],
                        y=[circle_y],
                        mode='markers',
                        marker=dict(size=radius*2, color='rgba(255,0,0,0.5)', line=dict(width=2, color='red')),
                        name=f'цветок (R={radius})'
                    ))
                    valid_position = True
            
            else:
                square_x = random.randint(0, WIDTH - SQUARE_SIZE)
                square_y = random.randint(0, HEIGHT - SQUARE_SIZE)
                square_x_end = square_x + SQUARE_SIZE
                square_y_end = square_y + SQUARE_SIZE
                
                new_shape = {'type': 'square', 'x': square_x, 'y': square_y, 'size': SQUARE_SIZE}
                
                intersects = any(shapes_intersect(new_shape, s) for s in placed_shapes)
                
                if not intersects:
                    placed_shapes.append(new_shape)
                    fig.add_trace(go.Scatter(
                        x=[square_x, square_x, square_x_end, square_x_end, square_x],
                        y=[square_y, square_y_end, square_y_end, square_y, square_y],
                        mode='lines',
                        fill='toself',
                        fillcolor='rgba(0,0,255,0.3)',
                        line=dict(color='blue', width=2),
                        name=f'трава ({SQUARE_SIZE}x{SQUARE_SIZE})'
                    ))
                    valid_position = True

    # Настройка отображения
    fig.update_layout(
        plot_bgcolor='white',
        xaxis=dict(range=[0, WIDTH], dtick=50),
        yaxis=dict(range=[0, HEIGHT], dtick=50),
        width=700,
        height=700,
        title='Алхимик 500х500'
    )
    fig.show()
