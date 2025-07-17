import plotly.graph_objects as go
import numpy as np
import random
import math


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
        # Определяем круг и квадрат
        circle = shape1 if shape1['type'] == 'circle' else shape2
        square = shape2 if shape2['type'] == 'square' else shape1
        
        # Находим ближайшую точку на квадрате к центру круга
        closest_x = max(square['x'], min(circle['x'], square['x'] + square['size']))
        closest_y = max(square['y'], min(circle['y'], square['y'] + square['size']))
        
        # Рассчитываем расстояние между центром круга и ближайшей точкой
        distance = math.sqrt((circle['x'] - closest_x)**2 + (circle['y'] - closest_y)**2)
        
        return distance < circle['radius']

# Создаем основную фигуру для визуализации
fig = go.Figure()

# Устанавливаем размеры холста
width = 500  
height = 500  
grid_denominator = 10  # размер клетки 


x_step = width / grid_denominator  
y_step = height / grid_denominator - (grid_denominator // 2)  


for y in np.arange(0, width, y_step):
    fig.add_trace(go.Scatter(
        x=[0, width],
        y=[y, y],
        mode='lines',
        line=dict(color='lightgray', width=0.5), 
        showlegend=False,  
        hoverinfo='none'   
    ))


for x in np.arange(0, height, x_step):
    fig.add_trace(go.Scatter(
        x=[x, x],
        y=[0, height],
        mode='lines',
        line=dict(color='lightgray', width=0.5),
        showlegend=False,  
        hoverinfo='none'  
    ))

# Параметры для генерации случайных фигур
num_shapes = random.randint(5, 15)  
min_radius = 3   
max_radius = 15  
square_size = 15  


placed_shapes = []

# Основной цикл генерации фигур
for _ in range(num_shapes):
    attempts = 0
    max_attempts = 100
    valid_position = False
            
    while not valid_position and attempts < max_attempts:
        attempts += 1
    
        shape_type = random.choice(['flower', 'grass'])
        
        if shape_type == 'grass':  # Круг (трава)
            radius = random.randint(min_radius, max_radius)
            circle_x = random.randint(radius, width - radius) + 20
            circle_y = random.randint(radius, height - radius) - 20
            
            new_shape = {
                'type': 'circle',
                'x': circle_x,
                'y': circle_y,
                'radius': radius
            }
            
            intersects = False
            for existing_shape in placed_shapes:
                if shapes_intersect(new_shape, existing_shape):
                    intersects = True
                    break
            
            if not intersects:
                placed_shapes.append(new_shape)
                fig.add_trace(go.Scatter(
                    x=[circle_x],
                    y=[circle_y],
                    mode='markers',
                    marker=dict(
                        size=radius * 2,                # диаметр круга
                        color='rgba(255, 0, 0, 0.5)',   # полупрозрачный красный
                        line=dict(width=2, color='red') # красная граница
                    ),
                    name=f'цветок (R={radius})'   
                ))
                valid_position = True
        
        else:   # Обработка квадратов (цветы)
            square_x = random.randint(0, width - square_size) + 20
            square_y = random.randint(0, height - square_size) - 20
            square_x_end = square_x + square_size
            square_y_end = square_y + square_size
            
            new_shape = {
                'type': 'square',
                'x': square_x,
                'y': square_y,
                'size': square_size
            }
            
            intersects = False
            for existing_shape in placed_shapes:
                if shapes_intersect(new_shape, existing_shape):
                    intersects = True
                    break
            
            if not intersects:
                placed_shapes.append(new_shape)
                fig.add_trace(go.Scatter(
                    x=[square_x, square_x, square_x_end, square_x_end, square_x],
                    y=[square_y, square_y_end, square_y_end, square_y, square_y],
                    mode='lines',
                    fill='toself',                             
                    fillcolor='rgba(0, 0, 255, 0.3)',          
                    line=dict(color='blue', width=2),        
                    name=f'трава ({square_size}x{square_size})' 
                ))
                valid_position = True

# Настраиваем внешний вид графика
fig.update_layout(
    plot_bgcolor='white',  
    xaxis=dict(
        range=[0, width],  
        dtick=50           
    ),
    yaxis=dict(
        range=[0, height],
        dtick=50            
    ),
    width=700,                 
    height=700,                 
    title='Алхимик 500х500'    
)


fig.show()
