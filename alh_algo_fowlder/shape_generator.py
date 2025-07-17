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
width = 500  # ширина холста
height = 500  # высота холста
grid_denominator = 10  # параметр для расчета плотности сетки

# Рассчитываем шаг сетки по осям
x_step = width / grid_denominator  # шаг между вертикальными линиями сетки
y_step = height / grid_denominator - (grid_denominator // 2)  # шаг между горизонтальными линиями сетки


# Цикл для рисования горизонтальных линий сетки
# Проходит по всем Y-координатам с шагом y_step
for y in np.arange(0, width, y_step):
    fig.add_trace(go.Scatter(
        x=[0, width],
        y=[y, y],
        mode='lines',
        line=dict(color='lightgray', width=0.5),  # светло-серые тонкие линии
        showlegend=False,  # не показывать в легенде
        hoverinfo='none'   # отключить всплывающие подсказки
    ))

# Цикл для рисования вертикальных линий сетки
# Проходит по всем X-координатам с шагом x_step
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
num_shapes = random.randint(5, 15)  # случайное количество фигур (от 5 до 15)
min_radius = 3   # минимальный радиус для кругов
max_radius = 15  # максимальный радиус для кругов
square_size = 15  # размер стороны квадрата

# Список для хранения информации о размещенных фигурах
placed_shapes = []

# Основной цикл генерации фигур
# Создает случайное количество фигур (num_shapes)
for _ in range(num_shapes):
    # Счетчик попыток для предотвращения бесконечного цикла
    attempts = 0
    max_attempts = 100
    valid_position = False
            
    # Цикл поиска валидной позиции для новой фигуры
    # Пытается найти непересекающуюся позицию до max_attempts раз
    while not valid_position and attempts < max_attempts:
        attempts += 1
        
        # Случайно выбираем тип фигуры для отрисовки
        shape_type = random.choice(['flower', 'grass'])
        
        if shape_type == 'grass':  # Круг (трава)
            radius = random.randint(min_radius, max_radius)
            circle_x = random.randint(radius, width - radius) + 20
            circle_y = random.randint(radius, height - radius) - 20
            
            # Создаем объект для проверки пересечений
            new_shape = {
                'type': 'circle',
                'x': circle_x,
                'y': circle_y,
                'radius': radius
            }
            
            # Проверяем пересечение с существующими фигурами
            intersects = False
            for existing_shape in placed_shapes:
                if shapes_intersect(new_shape, existing_shape):
                    intersects = True
                    break
            
            # Если нет пересечений, сохраняем и рисуем
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
                    name=f'цветок (R={radius})'    # подпись в легенде
                ))
                valid_position = True
        
        else:   # Обработка квадратов (цветы)
                # Генерация параметров квадрата
            square_x = random.randint(0, width - square_size) + 20
            square_y = random.randint(0, height - square_size) - 20
            square_x_end = square_x + square_size
            square_y_end = square_y + square_size
            
            # Создаем объект для проверки пересечений
            new_shape = {
                'type': 'square',
                'x': square_x,
                'y': square_y,
                'size': square_size
            }
            
            # Проверяем пересечение с существующими фигурами
            intersects = False
            for existing_shape in placed_shapes:
                if shapes_intersect(new_shape, existing_shape):
                    intersects = True
                    break
            
            # Если нет пересечений, сохраняем и рисуем
            if not intersects:
                placed_shapes.append(new_shape)
                fig.add_trace(go.Scatter(
                    x=[square_x, square_x, square_x_end, square_x_end, square_x],
                    y=[square_y, square_y_end, square_y_end, square_y, square_y],
                    mode='lines',
                    fill='toself',                              # заполнение внутренней области
                    fillcolor='rgba(0, 0, 255, 0.3)',           # полупрозрачная синяя заливка
                    line=dict(color='blue', width=2),           # синяя граница
                    name=f'трава ({square_size}x{square_size})' # подпись в легенде
                ))
                valid_position = True

# Настраиваем внешний вид графика
fig.update_layout(
    plot_bgcolor='white',  # белый фон области графика
    xaxis=dict(
        range=[0, width],  # диапазон оси X
        dtick=50           # шаг сетки 50 единиц
    ),
    yaxis=dict(
        range=[0, height],  # диапазон оси Y
        dtick=50            # шаг сетки 50 единиц
    ),
    width=700,                  # ширина фигуры в пикселях
    height=700,                 # высота фигуры в пикселях
    title='Алхимик 500х500'     # заголовок графика
)

# Отображаем фигуру
fig.show()
