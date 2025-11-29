import os
import time
from PIL import Image, ImageDraw

class GameOfLife:
    # Конструктор класса
    def __init__(self, input_filename, output_filename_txt, output_filename_png,  generations=-1):
       self.dirfile = "/home/andybyokv/Python_PJCS/PythonExercises/" 
       self.intput_filename = self.dirfile + input_filename

       if output_filename_txt == '':
           self.output_filename_txt = ''
       else:
           self.output_filename_txt = self.dirfile + output_filename_txt 

       if output_filename_png== '':
           self.output_filename_png= ''
       else:
           self.output_filename_png = self.dirfile + output_filename_png     

       self.grid = self.load_from_file()       
       self.rows = len(self.grid) # вычисляем длину строки
       self.cols = len(self.grid[0]) # вычисляем количество столбцов по 0 строке
       self.generations = generations  # количество генераций  
       self.iterations = 1 # количество итераций    
       self.gen_finish = False # флаг окончания 

        # Параметры визуализации
       self.base_color = (0, 0, 255)   # синий
       self.cell_size = 20
       self.border_width = 2
        
       # Для отслеживания возраста клеток
       self.age_grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

    def neighbors_counter(self, row, col):
        """ Счетчик соседей """
        counter = 0
        delta = [-1, 0, 1] # смещение относительно целевого элемента

    #  Перебираем строки
    #               -1 - вверх
    #                0 - та же строка
    #                1 - вниз
        for delta_row in delta:
    #  Перебираем столбцы
    #               -1 - влево
    #                0 - тот же стоблец
    #                1 - вправо
            for delta_col in delta:
                if delta_row == 0 and delta_col == 0: # целевую клетку пропускаем
                    continue
            # вычисляем координаты соседей
                n_row = row + delta_row
                n_col = col + delta_col

        # Проверка на выход за границы сетки
                if (0 <= n_row  < self.rows) and (0 <= n_col < self.cols):
                    counter += self.grid[n_row][n_col]  # инкрементируем   
        return counter
        
    def next_gen(self):
        """ Вычисляет следующее поколение """    
        new_grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

        new_age_grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

        for row in range(self.rows):           # Y
            for col in range(self.cols):       # X
                neighbors = self.neighbors_counter(row, col)
                current_cell = self.grid[row][col]  # запоминаем текущее состояние ИСХОДНОГО поля
                current_age = self.age_grid[row][col]
        
                if current_cell == 1:  # ЖИВАЯ клетка
                    if neighbors == 2 or neighbors == 3:
                        new_grid[row][col] = 1  # остается живой
                        new_age_grid[row][col] = current_age + 1  # Увеличиваем возраст
                    else:
                        new_grid[row][col] = 0  # умирает
                        new_age_grid[row][col] = 0  # Клетка умирает, возраст обнуляется

                if current_cell == 0:  # ПУСТАЯ клетка 
                    if neighbors == 3:
                        new_grid[row][col] = 1  # рождается
                        new_age_grid[row][col] = 1  # Новая клетка, возраст = 1
                    else:
                        new_grid[row][col] = 0  # остается пустой   
                        new_age_grid[row][col] = 0  

        if self.grid == new_grid:
            self.gen_finish = True
        
        self.grid = new_grid
        self.age_grid = new_age_grid  # обновляем возраст
        return new_grid
     
    def write_to_file(self, generation):
        """Пишет в файл"""
        if self.output_filename_txt != '':
            path = self.output_filename_txt
            lines = []
            lines.append(f"Generation {generation}")
            for row in self.grid:
                # преобразуем строку чисел в строку символов
                lines.append(' '.join(map(str, row)))
            text = '\n'.join(lines) + '\n\n'

            with open(path, 'a', encoding='utf-8') as f:
                f.write(text)
        return          

    def save_image(self, iteration):
        """PNG файл с изменением цвета в зависимости от возраста клеток"""
        if self.output_filename_png == '':
            return

        # Размеры изображения+ границы
        width = self.cols * (self.cell_size + self.border_width) + self.border_width
        height = self.rows * (self.cell_size + self.border_width) + self.border_width
        
        # изображение с фоном
        img = Image.new("RGB", (width, height), (30, 30, 30))
        draw = ImageDraw.Draw(img)
        
        # вертикальные линии
        for x in range(0, width, self.cell_size + self.border_width):
            draw.line(
                (x, 0, x, height),
                fill=(50, 50, 50),
                width=self.border_width
            )
        
        # горизонтальные линии
        for y in range(0, height, self.cell_size + self.border_width):
            draw.line(
                (0, y, width, y),
                fill=(50, 50, 50),
                width=self.border_width
            )
        
        # клетки 
        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row][col] == 1:
                    
                    age = self.age_grid[row][col] # получаем возраст
                    
                    max_age = 10  # Максимальный возраст для шкалы темноты
                    age_factor = min(age, max_age) / max_age # маппим 0.0 - 1.0

                     # затемнение 
                    """
                        1.0 - максимальная яркость                     
                        0.7 - коэффициент затемнения 
                    """
                    brightness = 1.0 - (age_factor * 0.7)  # От 1.0 до 0.2 

                    # компоненты RGB цвета                   
                    r = int(self.base_color[0] * brightness) # Умножаем каждый компонент базового цвета на яркость
                    g = int(self.base_color[1] * brightness)
                    b = int(self.base_color[2] * brightness)
                    
                    # Координаты левого верхнего угла клетки + границы
                    x0 = col * (self.cell_size + self.border_width) + self.border_width
                    y0 = row * (self.cell_size + self.border_width) + self.border_width

                    # Координаты правого нижнего угла клетки                    
                    x1 = x0 + self.cell_size - 1 # -1px 
                    y1 = y0 + self.cell_size - 1 # -1px 
                    
                    # Рисуем саму клетку                
                    draw.rectangle(
                        [x0, y0, x1, y1], # координаты прямоугольника
                        fill=(r, g, b) # цвет заливки 
                    )

        # Сохраняем изображение              
        img.save(f"{self.output_filename_png}/IMG{iteration}.png")
        print(f"Saved to: {self.output_filename_png}/IMG{iteration}.png")
       

    def load_from_file(self):
        """Загружеает данные из файла"""
        path = self.intput_filename
        with open(path, 'r') as f:
            try:                
                lines = f.readlines() # получаем список
                #print(lines)
                self.grid = [list(map(int, line.strip())) for line in lines]
                #print(self.grid)
                return self.grid
            except Exception as ex:
                print(ex)                

    def display(self):
        """Распечатка на консоль"""
        os.system('clear')  # Очищаем консоль
        for line in self.grid:
            for cell in line:
            #print(cell, end=' ')
                if cell == 1: 
                    print('■', end = ' ')
                else:
                    print('□', end = ' ')
                   #print('', end = ' ')
            print('')
         
        print(f"\nIteration:{self.iterations}") 
        if self.gen_finish: 
            print("Generation finished!")  
            

    def run_simulation(self):
        """Запуск симуляции """       
        def run():
            self.save_image(self.iterations)   # PIL 
            self.next_gen()            
            self.display()
            self.write_to_file(self.iterations)
            self.iterations +=1 
                               
            
        if self.generations > 0: # указанное количество итераций                     
            for _ in range(self.generations):
                run()
                if self.gen_finish == True:                    
                    break 
                time.sleep(0.3)  # Пауза 
            self.gen_finish = True    

            return      
        
        elif self.generations == -1: # бесконечно
            while True:
                run()
                if self.gen_finish == True:                    
                    break        
                       
                time.sleep(0.3)  # Пауза   

                          

def main():

    game = GameOfLife("input.txt","output.txt", "img", 30) 
    
    try:
        game.run_simulation()
    except KeyboardInterrupt:
        print("\nKeyboard Interrupt!")

if __name__ == "__main__":
    main()