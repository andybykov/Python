import math

# Функция ввода данных
def Get_user_input():
    
    d1_yard = int(input("Введите кратчайшее расстояние между спасателем и кромкой воды, d1 (ярды): "))
    d2_feet = int(input("Введите кратчайшее расстояние от утопающего до берега, d2 (футы): "))
    h_yard = int(input("Введите боковое смещение между спасателем и утопающим, h (ярды): "))
    v_sand_miles_per_h = int(input("Введите скорость движения спасателя по песку, v_sand (мили в час): "))
    n = int(input("Введите коэффициент замедления спасателя при движении в воде, n: "))
    theta1_degree = float(input("Введите направление движения спасателя по песку, theta1 (градусы): "))
    
    return d1_yard, d2_feet, h_yard, v_sand_miles_per_h, n, theta1_degree



# Ярды в футы
def Convert_yards_to_feet(yard):

    feet = yard * 3

    return feet

# Мили/час в футы/секунду
def Convert_speed(miles_per_h):

    feets_per_s = miles_per_h * 5280 / 3600

    return feets_per_s 

# Градусы в радианы
def Convert_geegrees_to_rad(theta1_degree):

    theta1_rad  = theta1_degree * (math.pi / 180)

    return theta1_rad 

# конвертация значений для рассчета
def Convert_all_valuse(d1_yard, h_yard, v_sand_miles_per_s, theta1_deegre):

    d1_feet = Convert_yards_to_feet(d1_yard)
    h_feet = Convert_yards_to_feet(h_yard)
    v_sand_feets_per_s = Convert_speed(v_sand_miles_per_s)
    theta1_rad = Convert_geegrees_to_rad(theta1_deegre)

    return d1_feet, h_feet, v_sand_feets_per_s, theta1_rad


 # Функция для вычисления кратчайшего пути
def Calculate_path(d1_feet, d2_feet, h_feet, theta1_rad):
    
    x = d1_feet * math.tan(theta1_rad)
    L1 = math.sqrt(x**2 + d1_feet**2)
    L2 = math.sqrt((h_feet - x)**2 + d2_feet**2)
    
    return L1, L2

# Функция для вычисления времени 
def Сalculate_time(L1, L2, v_sand_feets_per_s, n):

    total_time = (L1 + n * L2) / v_sand_feets_per_s

    return total_time

# Основная для расчета времени спасения
def Rescue_time_calculator(d1_yard, d2_feet, h, v_sand_mph, n, theta1_deg):   

    # Конвертация единиц
    d1_feet, h_feet, v_sand_fps, theta1_rad = Convert_all_valuse(d1_yard, h, v_sand_mph, theta1_deg)    
    
    # Вычисление кратчайшего пути
    L1, L2 = Calculate_path(d1_feet, d2_feet, h_feet, theta1_rad)
    
    # Расчет времени
    time = Сalculate_time(L1, L2, v_sand_fps, n)
    
    return time

# Функция рассчета оптимального угла
def Calculate_optimal_angle(d1, d2, h, v_sand, n):
    

    best_time = 9999.0 # большое число
    best_angle = 0.0

    theta1_deg = 0.0  

    while theta1_deg <= 90.0:
        current_time = Rescue_time_calculator(d1, d2, h, v_sand, n, theta1_deg)
        
        if (current_time < best_time):
            best_time = current_time  
            best_angle = theta1_deg    
        
        theta1_deg += 0.1
    
    return best_angle, best_time
        


# Получение данных от пользователя
#d1, d2, h, v_sand, n, theta1 = Get_user_input()
d1, d2, h, v_sand, n, theta1 = 8, 10, 50, 5, 2, 39.413

    
# Расчет времени спасения
result = Rescue_time_calculator(d1, d2, h, v_sand, n, theta1)    

# Вывод результата
print(f"Rescue time: {result.__round__(1)} sec")

best_angle, best_time = Calculate_optimal_angle(d1, d2, h, v_sand, n)

# Вывод лучшего резульатат
print(f"Best rescue time: {best_time.__round__(1)} sec, Best angle: {best_angle.__round__(3)} degrees")



