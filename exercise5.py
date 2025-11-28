import os
import time

class GameOfLife:
    # Конструктор класса
    def __init__(self, input_filename, output_filename,  generations=-1):
       self.dirfile = "/home/andybyokv/Python_PJCS/PythonExercises/" 
       self.intput_filename = self.dirfile + input_filename
       if output_filename == '':
           self.output_filename = ''
       else:
           self.output_filename = self.dirfile + output_filename          
       self.grid = self.load_from_file()       
       self.rows = len(self.grid) # вычисляем длину строки
       self.cols = len(self.grid[0]) # вычисляем количество столбцов по 0 строке
       self.generations = generations  # количество генераций            

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

        for row in range(self.rows):           # Y
            for col in range(self.cols):       # X
                neighbors = self.neighbors_counter(row, col)

                current_cell = self.grid[row][col]  # запоминаем текущее состояние ИСХОДНОГО поля
        
                if current_cell == 1:  # ЖИВАЯ клетка
                    if neighbors == 2 or neighbors == 3:
                        new_grid[row][col] = 1  # остается живой
                    else:
                        new_grid[row][col] = 0  # умирает

                if current_cell == 0:  # ПУСТАЯ клетка 
                    if neighbors == 3:
                        new_grid[row][col] = 1  # рождается
                    else:
                        new_grid[row][col] = 0  # остается пустой
        self.grid = new_grid
        return new_grid
     
    def write_to_file(self, generation):
        """Пишет в файл"""
        if self.output_filename != '':
            path = self.output_filename
            lines = []
            lines.append(f"Generation {generation}")
            for row in self.grid:
                # преобразуем строку чисел в строку символов
                lines.append(' '.join(map(str, row)))
            text = '\n'.join(lines) + '\n\n'

            with open(path, 'a', encoding='utf-8') as f:
                f.write(text)
        return          

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

    def run_simulation(self):
        """Запуск симуляции """
        gen_count = 1 # счетчик поколений
        
        if self.generations > 0: # указанное количество итераций                     
            for _ in range(self.generations):
                self.next_gen()
                self.display()
                self.write_to_file(gen_count)
                gen_count += 1
                time.sleep(0.3)  # Пауза 
            return        
        elif self.generations == -1: # бесконечно
            while True:
                self.next_gen()
                self.display()
                self.write_to_file(gen_count)
                gen_count += 1
                time.sleep(0.3)  # Пауза 

def main():

    game = GameOfLife("input.txt","") 
    
    try:
        #game.display()
       #print(game.cols)
       # print(game.rows)
        #print(game.grid)
        #rows = len(game.grid)
        #print(rows)

        #cols = len(game.grid[0])
        #print(cols)
        game.run_simulation()
    except KeyboardInterrupt:
        print("\nKeyboard Interrupt!")

if __name__ == "__main__":
    main()