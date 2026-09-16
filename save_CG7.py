import random
import time
from math import fmod, floor
import data as dt
import pygame
import pygame


class player:
    def __init__(self, rn, name, spawner, start_gx, start_gy):
        self.rn = rn
        self.name = name
        self.obj_spawn = spawner

        # Физика и координаты
        self.F = [0.0, 0.0]  # Игрок изначально стоит
        self.global_cord = [start_gx, start_gy]
        self.last_tick = 0

        # Игровые параметры
        self.color = (0, 255, 0)  # Зеленый цвет игрока
        self.collected_hydrogen = 0  # Счётчик собранных бонусов
        self.speed_power = 2.0  # Сила ускорения при нажатии клавиш

        # Заглушки для совместимости с твоей таблицей Менделеева
        self.is_easy = True
        self.mass = 0
        self.rt = 3500.0
        self.is_compile = False
        self.A = [0, 0, 0]
        self.B = [0, 0, [0], 0]
        self.zar = 0

    def get_info(self):
        # Метод для отрисовщика draww(), возвращает цвет
        return [self.rn, self.name, self.color, self.color]

    def handle_input(self):
        # Опрос клавиатуры (управление WASD и стрелочками)
        keys = pygame.key.get_pressed()

        # Движение по X
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.F[0] = -self.speed_power
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.F[0] = self.speed_power
        else:
            self.F[0] *= 0.7  # Плавное торможение (инерция)

        # Движение по Y
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.F[1] = -self.speed_power
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.F[1] = self.speed_power
        else:
            self.F[1] *= 0.7  # Плавное торможение (инерция)


class molekyla:
    def __init__(self,rn,name,spawner):
        self.rn = rn
        self.name = name
        self.F = [random.uniform(-1.5, 1.5), random.uniform(-1.5, 1.5)]

        print('=='*50)
        self.is_easy = True #/
        self.color = (0,0,0)
        self.obj_spawn = spawner
        self.mass = 0
        self.rt = 3500.0
        self.is_compile = False
        self.A = [0,0,0] #electr,val,kol
        self.B = [0,0,[0],0]
        self.data2 = []
        self.zar = 0
        self.last_tick = 0
        self.global_cord = [random.randint(0,750),250]


    def get_info(self):
        # Метод СТРОГО возвращает имя, скорость, легкость и НАСТОЯЩИЙ цвет молекулы
        return (self.name, self.F, self.is_easy, self.color, self.obj_spawn, self.mass)


    def compile_razl(self,k,t):
        E = 0
        """E = ((k*t)*(
                (self.A[1]*self.A[2])+(abs(self.B[1])*(self.B[3]/self.A[2]))/2
             )) - (self.A[0]+self.B[0])"""
        f1 = (self.A[1]*self.A[2])+(abs(self.B[1])*(self.B[3]/self.A[2]))/2
        f2 = (self.A[0]+self.B[0])
        t = (f1+f2)/k
        self.rt = t
        return t

    def compile_A_and_B(self):
        data = self.name.split('/')
        data2 = [el.split() for el in data]
        self.data2 = data2
        #a
        #print(data2)
        A = data2[0]
        inf = dt.periodic_table1.get(A[0])[0]
        self.A = [inf[1],inf[2][0],int(A[1])]
        #b
        B = data2[1:]
        infv = 0
        i = 0
        ele = 0
        kol = [0]
        for el in B:
            if len(el[0]) <= 2:
                inf = dt.periodic_table1.get(el[0])[0]
                ele += inf[1]
                if i == 0:
                    infv += inf[2][-1] * int(el[1])
                    kol = [int(el[1])]
                else:
                    infv -= inf[2][-1] * int(el[1])
                    kol.append(int(el[1]))
                i+=1
        val = infv
        #print(f'val - {val} ')
        self.B = [ele,val,kol,int(self.NOK(val,self.A[1])/self.A[1])]
        return (self.A,self.B)

    def NOD(self,a,b):
        while b:
            a, b = b, a%b

        return a

    def NOK(self,a,b):
        return (a*b)/self.NOD(a,b)

    def update(self):
        pass




class game_data:
    def __init__(self,size,chank_size):
        self.size = size
        self.chank_size = chank_size
        self.MofD = [[[[None,0,0]] for x in range(size[0])]for y in range(size[1])]

    def printt(self):
        for el in self.MofD:
            print(el)

    def get_chunk_dist(self, mo1, mo2):
        # Расстояние в чанках по Пифагору прямо из global_cord
        return int((((mo1.global_cord[0] - mo2.global_cord[0]) ** 2 +
                 (mo1.global_cord[1] - mo2.global_cord[1]) ** 2) ** 0.5) / self.chank_size)

    def get_info(self, ids, deep):
        ot = []
        # ids[0] — это y (строка), ids[1] — это x (столбец)
        cy, cx = ids[0], ids[1]


        min_y = max(0, cy - deep)
        max_y = min(self.size[1], cy + deep + 1)
        min_x = max(0, cx - deep)
        max_x = min(self.size[0], cx + deep + 1)


        for y in range(min_y, max_y):
            for x in range(min_x, max_x):
                for cell in self.MofD[y][x]:
                    if cell is not None and cell[0] is not None:
                        ot.append(cell)
        return ot

    def get_info11(self, ids, deep):
        ot = []
        # ids[0] — это y (строка), ids[1] — это x (столбец)
        cy, cx = ids[0], ids[1]


        min_y = max(0, cy - deep)
        max_y = min(self.size[1], cy + deep + 1)
        min_x = max(0, cx - deep)
        max_x = min(self.size[0], cx + deep + 1)

        # ПРАВИЛЬНЫЙ обход двумерного среза чанков
        for y in range(min_y, max_y):
            for x in range(min_x, max_x):
                for cell in self.MofD[y][x]:
                    if cell is None:
                        continue
                    else:
                        ot.append(cell)
        print(ot)
        return ot

    def add_obj(self, ids, obj):
        # ids[0] — y, ids[1] — x, ids[2] — c (индекс внутри чанка)
        self.MofD[ids[0]][ids[1]][ids[2]] = obj

    def comile_v(self, ids):
        # ids — это строго кортеж (y_chunk, x_chunk, c_idx)
        y_chunk = ids[0]
        x_chunk = ids[1]
        c_idx = ids[2]

        # Достаем ячейку [obj, lx, ly] и сам объект
        current_cell = self.MofD[y_chunk][x_chunk][c_idx]
        main_obj = current_cell[0]

        # --- ЗАЩИТА ОТ ОШИБКИ ИЗВЛЕЧЕНИЯ ИЗ ТАБЛИЦЫ МЕНДЕЛЕЕВА ---
        raw_symbol = main_obj.rn
        element_data = dt.periodic_table1.get(raw_symbol)

        if element_data is None:
            # Парсим первую букву имени (например, "H" из "H 2/...")
            clean_symbol = str(main_obj.name).split()[0].split('/')[0]
            element_data = dt.periodic_table1.get(clean_symbol)

        if element_data is None:
            element_data = dt.periodic_table1.get('Null')

        # Извлекаем радиус из структуры твоей таблицы Менделеева
        element_data = element_data[0]
        mn = element_data[4] + 50
        # --------------------------------------------------------

        # Ищем соседей через твою функцию get_info
        sosedi = self.get_info((y_chunk, x_chunk), mn)

        # --- ТЕРМОДИНАМИКА ЧАНКА С МАСШТАБИРОВАНИЕМ ---
        try:
            # Умножаем на 2 для масштаба drawing_mas (150x150)
            temp_y = y_chunk * 2
            temp_x = x_chunk * 2

            # Извлекаем число температуры из структуры списка
            chunk_temp = self.gamep.drawing_mas[temp_y][temp_x][0]
        except (AttributeError, IndexError, TypeError):
            chunk_temp = 20.0  # Дефолтная комнатная температура

        temp_factor = abs(chunk_temp - 100.0) / 100.0 + 0.5
        # ----------------------------------------------

        # Отладочный принт для игрока
        if hasattr(self, 'player_obj') and main_obj is self.player_obj:
            print(
                f"!!! ИГРОК В КУРСЕ ФИЗИКИ !!! Всего соседей в радиусе: {len(sosedi)} | Градусы в чанке: {chunk_temp}°C")

        # --- ПАРАБОЛИЧЕСКОЕ ОТТАЛКИВАНИЕ (ПЛОТНОСТЬ) ---
        density_count = 0
        for el in sosedi:
            if el[0] is not main_obj:
                d = self.get_chunk_dist(main_obj, el[0])
                if d <= 3.0:
                    density_count += 1
        repulsion_force = 0.02 * (density_count ** 2)

        all_neighbors = []
        for el in sosedi:
            neighbor_obj = el[0]  # Достаем сам объект из структуры [obj, lx, ly]
            if neighbor_obj is main_obj:
                continue
            dist = self.get_chunk_dist(main_obj, neighbor_obj)
            all_neighbors.append((dist, el))

        # Сортируем топ-3 соседей
        all_neighbors.sort(key=lambda x: x[0])
        best_three = all_neighbors[:3]

        for dist, best_cell in best_three:
            neighbor_obj = best_cell[0]

            # --- ЖЕСТКАЯ КОЛЛИЗИЯ С ИГРОКОМ ---
            is_main_player = (hasattr(self, 'player_obj') and main_obj is self.player_obj)
            is_neighbor_player = (hasattr(self, 'player_obj') and neighbor_obj is self.player_obj)

            if is_main_player or is_neighbor_player:
                dx_p = neighbor_obj.global_cord[0] - main_obj.global_cord[0]
                dy_p = neighbor_obj.global_cord[1] - main_obj.global_cord[1]
                pixel_dist = (dx_p ** 2 + dy_p ** 2) ** 0.5

                if pixel_dist < 15.0:
                    if pixel_dist == 0: pixel_dist = 0.1
                    main_obj.F[0] = -(dx_p / pixel_dist) * 2.0
                    main_obj.F[1] = -(dy_p / pixel_dist) * 2.0
                    neighbor_obj.F[0] = (dx_p / pixel_dist) * 2.0
                    neighbor_obj.F[1] = (dy_p / pixel_dist) * 2.0
                    continue  # Коллизия блокирует притяжение

            # --- ХИМИЧЕСКОЕ ВЗАИМОДЕЙСТВИЕ (РЕАКТОР ВСТРОЕН СЮДА) ---
            if dist < 1.0:  # Столкновение (Слипание)
                if dist == 0: dist = 0.01

                # ТЕРМИЧЕСКИЙ РАСПАД (ПРИ ОБЫЧНОМ НАГРЕВЕ 350-5000)
                if chunk_temp >= 350.0 and chunk_temp < 5000.0:
                    main_obj.F[0] = random.uniform(-6.0, 6.0)
                    main_obj.F[1] = random.uniform(-6.0, 6.0)
                    neighbor_obj.F[0] = random.uniform(-6.0, 6.0)
                    neighbor_obj.F[1] = random.uniform(-6.0, 6.0)

                # --- ЖЕСТКИЙ ХИМИЧЕСКИЙ ВЗРЫВ ПРИ ТЕМПЕРАТУРЕ 9000 ---
                elif chunk_temp >= 5000.0:
                    print("💥 ВСПЫШКА СВЕРХНОВОЙ! ТЕМПЕРАТУРА 9000+! ТОТАЛЬНОЕ ЗАМЕЩЕНИЕ!")

                    # Прямая мгновенная реакция замещения без фильтров
                    main_obj.name = "H2"
                    main_obj.color = (255, 255, 255)  # Белый летучий Водород
                    # Стремительно улетает вверх по оси Y со скоростью -8.0!
                    main_obj.F = [random.uniform(-4.0, 4.0), -8.0]

                    neighbor_obj.name = "FeSO4"
                    neighbor_obj.color = (0, 255, 100)  # Изумрудный сульфат железа
                    neighbor_obj.F = [random.uniform(-2.0, 2.0), random.uniform(-2.0, 2.0)]

                    print(f"🧬 КВАНТОВЫЙ ВЗРЫВ: Получились '{main_obj.name}' и '{neighbor_obj.name}'!")

                else:
                    # --- ОБЫЧНАЯ ТЕМПЕРАТУРА: ВЕРОЯТНОСТЬ ИЗ КЛОЗУРЫ 500/t*E ---
                    E = 10.0
                    # Формула вероятности: прямо пропорциональна температуре
                    reaction_chance = (chunk_temp / 500.0) * E

                    if random.uniform(0, 100) <= reaction_chance:
                        print('--- УСПЕШНОЕ СТОЛКНОВЕНИЕ: AB + CD = AD + CB ---')

                        # Перестраиваем продукты в чистый вид для графики draww()
                        main_obj.name = "H2"
                        main_obj.color = (255, 255, 255)
                        main_obj.F = [random.uniform(-2.0, 2.0), -5.0]  # Водород улетает вверх

                        neighbor_obj.name = "FeSO4"
                        neighbor_obj.color = (0, 255, 100)  # Изумрудный крест соли
                        neighbor_obj.F = [0.0, 0.0]
                    else:
                        # Если шанс не выпал, они просто усредняют скорости (стандартное слипание)
                        avg_fx = (main_obj.F[0] + neighbor_obj.F[0]) / 2
                        avg_fy = (main_obj.F[1] + neighbor_obj.F[1]) / 2

                        # ТЕПЛОВОЙ ХАОС (БРОУНОВСКОЕ ДВИЖЕНИЕ)
                        if chunk_temp > 100.0:
                            chaos_power = (chunk_temp - 100.0) * 0.02
                            avg_fx += random.uniform(-chaos_power, chaos_power)
                            avg_fy += random.uniform(-chaos_power, chaos_power)

                        main_obj.F[0] = avg_fx
                        main_obj.F[1] = avg_fy
                        neighbor_obj.F[0] = avg_fx
                        neighbor_obj.F[1] = avg_fy
            else:
                # Химическое притяжение (когда они далеко)
                raw_rn1 = main_obj.rn
                raw_rn2 = neighbor_obj.rn
                P1 = dt.periodic_table1.get(raw_rn1)[0][1] if dt.periodic_table1.get(raw_rn1) else 1.0
                P2 = dt.periodic_table1.get(raw_rn2)[0][1] if dt.periodic_table1.get(raw_rn2) else 1.0
                q = (P1 + P2) * (1.0 / (dist ** 2)) * temp_factor

                dx = neighbor_obj.global_cord[0] - main_obj.global_cord[0]
                dy = neighbor_obj.global_cord[1] - main_obj.global_cord[1]

                mag = (dx ** 2 + dy ** 2) ** 0.5
                if mag > 0:
                    dx /= mag
                    dy /= mag

                # Отключаем отталкивание плотности для реагентов железа и кислоты
                is_reagent = ("S" in str(main_obj.name) or "Fe" in str(main_obj.name))
                current_repulsion = 0.0 if is_reagent else repulsion_force

                main_obj.F[0] += (dx * q * 0.1) - (dx * current_repulsion)
                main_obj.F[1] += (dy * q * 0.1) - (dy * current_repulsion)
                neighbor_obj.F[0] -= (dx * q * 0.1) - (dx * current_repulsion)
                neighbor_obj.F[1] -= (dy * q * 0.1) - (dy * current_repulsion)

    def move(self, tick):
        pending_moves = []
        removals_by_chunk = {}

        # Границы игрового поля в пикселях
        max_width = 750.0
        max_height = 750.0

        y = -1
        for el in self.MofD:
            y += 1
            x = -1
            for el2 in el:
                x += 1
                c = 0
                for el3 in el2:
                    if el3 is not None and len(el3) >= 3:
                        obj = el3[0]



                        if obj is not None and obj.last_tick != tick:
                            self.comile_v((y, x, c))
                            # 1. ТРЕНИЕ: Вся сила F каждый тик немного уменьшается (инерция)
                            # 0.98 означает, что объект теряет 2% скорости за тик. Можно поставить 0.95 для более вязкой среды
                            if hasattr(self, 'gamep') and self.gamep is not None:
                                self.gamep.react((y, x, c))
                            obj.F[0] *= 0.99
                            obj.F[1] *= 0.99

                            F = obj.F
                            cord = obj.global_cord

                            # Считаем потенциальные новые координаты
                            new_gx = cord[0] + F[0]
                            new_gy = cord[1] + F[1]

                            # 2. ЖЕСТКИЕ ГРАНИЦЫ И ОТСКОК С ПОЛОВИНОЙ СИЛЫ
                            # Проверка левой и правой стенки (ось X)
                            if new_gx <= 0:
                                new_gx = 0.0
                                obj.F[0] = -obj.F[0] * 0.5  # Разворот скорости по X и потеря половины силы
                            elif new_gx >= max_width:
                                new_gx = max_width
                                obj.F[0] = -obj.F[0] * 0.5

                            # Проверка верхней и нижней стенки (ось Y)
                            if new_gy <= 0:
                                new_gy = 0.0
                                obj.F[1] = -obj.F[1] * 0.5  # Разворот скорости по Y и потеря половины силы
                            elif new_gy >= max_height:
                                new_gy = max_height
                                obj.F[1] = -obj.F[1] * 0.5

                            # 3. Находим индекс чанка АБСОЛЮТНО на основе финальных координат
                            fx = int(new_gx // self.chank_size)
                            fy = int(new_gy // self.chank_size)

                            # Дополнительная страховка индексов по границам сетки
                            if fx >= self.size[0]: fx = self.size[0] - 1
                            if fx < 0: fx = 0
                            if fy >= self.size[1]: fy = self.size[1] - 1
                            if fy < 0: fy = 0

                            # 4. Считаем чистую локальную координату внутри нового чанка
                            nlx = new_gx % self.chank_size
                            nly = new_gy % self.chank_size

                            # Запоминаем удаление из текущего чанка (y, x)
                            chunk_key = (y, x)
                            if chunk_key not in removals_by_chunk:
                                removals_by_chunk[chunk_key] = []
                            removals_by_chunk[chunk_key].append(c)

                            # Запоминаем новые данные для вставки
                            pending_moves.append([fy, fx, [obj, nlx, nly], new_gx, new_gy])
                    c += 1

        # Фаза 1 ПЕРЕНОСА: Безопасное удаление старых позиций
        for (old_y, old_x), indices in removals_by_chunk.items():
            indices.sort(reverse=True)
            for idx in indices:
                self.MofD[old_y][old_x].pop(idx)

        # Фаза 2 ПЕРЕНОСА: Запись объектов в новые чанки
        for item in pending_moves:
            fy = item[0]
            fx = item[1]
            new_data = item[2]
            new_gx = item[3]
            new_gy = item[4]

            obj = new_data[0]
            obj.global_cord = [new_gx, new_gy]
            obj.last_tick = tick

            self.MofD[fy][fx].append(new_data)


import math
import random


class gamepole:
    def __init__(self, size, father):
        self.size = size
        self.father = father
        self.k_r = 0.05
        self.k_t = 0.05
        # Инициализируем трехмерный массив температуры
        self.drawing_mas = [[[10] for i in range(size[0])] for j in range(size[1])]
        # E =  (A[0]+C[0]+D[0]+(v*self.k_t))-(B[0]*(B[1]**2/2))

    def react(self, id):
        # id — это кортеж (y_chunk, x_chunk, c_idx)
        y_ch = id
        x_ch = id
        c_idx = id

        # Вытаскиваем текущий игровой тик из класса-отца d (game_data)
        # В твоем цикле move переменная называется tick
        current_tick = self.father.tick if hasattr(self.father, 'tick') else 0

        try:
            current_cell = self.father.MofD[y_ch][x_ch][c_idx]
            mn = current_cell
        except (IndexError, TypeError, KeyError):
            return

        # === ЖЕСТКИЙ КУЛДАУН: За тик молекула может среагировать только ОДИН раз! ===
        if hasattr(mn, 'last_react_tick') and mn.last_react_tick == current_tick:
            return  # Если она уже среагировала в этом кадре — уходим!
        # =========================================================================

        A = mn.A
        B = mn.B

        # Жесткий радиус соударения лоб в лоб (всего 25 пикселей)
        search_radius = 25
        data = self.father.get_info((y_ch, x_ch), search_radius)

        try:
            chunk_temp = self.drawing_mas[y_ch * 2][x_ch * 2]
            if chunk_temp <= 0: chunk_temp = 1.0
        except Exception:
            chunk_temp = 20.0

        maxE = 0.0
        bl_d = None
        tp = None
        eth_d = None

        for el in data:
            if el is None or len(el) < 3 or el is None:
                continue

            neighbor_obj = el

            # Если сосед УЖЕ среагировал в этом тике — пропускаем его, чтобы не дублировать
            if hasattr(neighbor_obj, 'last_react_tick') and neighbor_obj.last_react_tick == current_tick:
                continue

            if mn != neighbor_obj:
                E = 10.0  # Базовая энергия связи

                # Твоя формула вероятности: прямо пропорциональна жаре и энергии связи E
                reaction_chance = (chunk_temp / 500.0) * E

                # Случайный барьер
                if random.uniform(0, 100) > reaction_chance:
                    continue

                if maxE < E:
                    is_mn_complex = ("S" in str(mn.name) or "Fe" in str(mn.name) or getattr(mn, 'color', None) == (
                    0, 255, 100))
                    is_neighbor_complex = (
                                "S" in str(neighbor_obj.name) or "Fe" in str(neighbor_obj.name) or getattr(neighbor_obj,
                                                                                                           'color',
                                                                                                           None) == (
                                0, 255, 100))

                    if is_mn_complex and is_neighbor_complex:
                        if not (("Fe" in str(mn.name) and "O" in str(mn.name)) and (
                                "Fe" in str(neighbor_obj.name) and "O" in str(neighbor_obj.name))):
                            maxE = E
                            bl_d = neighbor_obj
                            eth_d = el
                            tp = 1  # Замещение

        # Применяем результаты химического взаимодействия
        if maxE > 0 and eth_d is not None and bl_d is not None:
            if tp == 1:
                print('--- АВТОМАТИЧЕСКОЕ ЗАМЕЩЕНИЕ ПО ФОРМУЛЕ AB + CD = AD + CB ---')
                el = bl_d
                C = el.A
                D = el.B

                # Блокируем ОБЕ молекулы для конца этого тика
                mn.last_react_tick = current_tick
                el.last_react_tick = current_tick

                new_A1 = A
                new_B1 = D if D is not None else ""
                new_A2 = C
                new_B2 = B if B is not None else ""

                mn.A = new_A1
                mn.B = new_B1

                str_A1 = str(new_A1).replace("[", "").replace("]", "").replace(",", "")
                str_B1 = str(new_B1).replace("[", "").replace("]", "").replace(",", "")
                mn.name = f"{str_A1}{str_B1}".replace(" ", "").replace("/", "").replace("0", "")

                el.A = new_A2
                el.B = new_B2

                str_A2 = str(new_A2).replace("[", "").replace("]", "").replace(",", "")
                str_B2 = str(new_B2).replace("[", "").replace("]", "").replace(",", "")
                el.name = f"{str_A2}{str_B2}".replace(" ", "").replace("/", "").replace("0", "")

                # Подгонка имен для draww()
                if "2.2" in mn.name and "3.44" in mn.name and "1.83" not in mn.name:
                    mn.name = "H2O"
                elif "2.2" in mn.name and "1.83" not in mn.name:
                    mn.name = "H2"
                else:
                    mn.name = "FeSO4"

                if "2.2" in el.name and "3.44" in el.name and "1.83" not in el.name:
                    el.name = "H2O"
                elif "2.2" in el.name and "1.83" not in el.name:
                    el.name = "H2"
                else:
                    el.name = "FeSO4"

                # Цвета продуктов
                mn.color = (255, 255, 255) if mn.name == "H2" else (
                    (0, 200, 255) if mn.name == "H2O" else (0, 255, 100))
                el.color = (255, 255, 255) if el.name == "H2" else (
                    (0, 200, 255) if el.name == "H2O" else (0, 255, 100))

                # Водород улетает вверх
                if mn.name == "H2": mn.F = [random.uniform(-1.0, 1.0), -5.0]
                if el.name == "H2": el.F = [random.uniform(-1.0, 1.0), -5.0]

                print(f"🧬 РЕЗУЛЬТАТ СИНТЕЗА: Получились '{mn.name}' и '{el.name}'!")


class meni:

    # 1. Супер толчок (расталкивает ботов волной от игрока)
    def bonus_push(self, txt):
        if hasattr(self, 'gamep') and self.gamep.father.player_obj is not None:
            player = self.gamep.father.player_obj

            for row in self.gamep.father.MofD:
                for chunk in row:
                    for el in chunk:
                        # ИСПРАВЛЕНО: проверяем структуру [obj, lx, ly] и отсекаем [None, 0, 0]
                        if el is not None and len(el) >= 3 and el[0] is not None:
                            obj = el[0]  # Извлекаем чистый объект молекулы

                            if obj is not player:
                                dx = obj.global_cord[0] - player.global_cord[0]
                                dy = obj.global_cord[1] - player.global_cord[1]
                                dist = (dx ** 2 + dy ** 2) ** 0.5

                                # Радиус взрывной волны — 150 пикселей
                                if dist < 150.0 and dist > 0:
                                    # Даем мощный импульс отталкивания ботам от центра игрока
                                    obj.F[0] += (dx / dist) * 15.0
                                    obj.F[1] += (dy / dist) * 15.0
            print("Сработал супер-толчок (боты растолкнуты)!")
        return 0

    # 2. Поднять температуру во всем мире на 50 градусов
    def bonus_temp_up(self, txt):
        if hasattr(self, 'gamep'):
            for y in range(len(self.gamep.drawing_mas)):
                for x in range(len(self.gamep.drawing_mas[y])):
                    # ИСПРАВЛЕНО: Меняем число СТРОГО внутри вложенного списка [0]
                    self.gamep.drawing_mas[y][x][0] += 50.0
            print(f"Температура поднята! Текущая в чанке (0,0): {self.gamep.drawing_mas[0][0][0]}°C")
        return 0

    # 3. Опустить температуру во всем мире на 50 градусов
    def bonus_temp_down(self, txt):
        if hasattr(self, 'gamep'):
            for y in range(len(self.gamep.drawing_mas)):
                for x in range(len(self.gamep.drawing_mas[y])):
                    # ИСПРАВЛЕНО: Меняем число СТРОГО внутри списка [0] и не даем уйти ниже нуля
                    current_t = self.gamep.drawing_mas[y][x][0]
                    self.gamep.drawing_mas[y][x][0] = max(0.0, current_t - 50.0)
            print(f"Температура опущена! Текущая в чанке (0,0): {self.gamep.drawing_mas[0][0][0]}°C")
        return 0

    def __init__(self):
        def b1_pr(a):
            print("Done")
            self.w = 1
            self.is_anim = True
            return 0

        def b2_pr(a):
            print("hh")
            self.w = 0
            self.sc2.godbye()

        pygame.init()
        pygame.display.set_caption("The End?")

        # Расширяем экран до 950px, чтобы справа влезла панель бонусов
        self.screen = pygame.display.set_mode((950, 750))
        self.clock = pygame.time.Clock()
        self.screen.fill((15, 15, 15))
        self.base_color = (15, 15, 15)
        self.w = 3
        self.alld = []

        # Кнопки и окна из твоего старого конструктора
        self.b1 = button((100, 50), (200, 200), (200, 100, 150), b1_pr, self.screen)
        self.sc2 = window((750, 750), 10, (0, 0), (95, 60, 15), 0, self.screen)
        self.is_anim = False
        self.rn_but = button((100, 50), (400, 400), (255, 100, 100), b2_pr, self.screen, ("Start", 16))
        self.compile_flag = False
        self.menu = window((750, 750), 10, (0, 0), (15, 15, 15), 0, self.screen)

        self.elements_data = {
            "H": 1, "He": -1, "Li": 0, "Be": 1, "B": 0, "C": -1, "N": 0, "O": 1,
            "F": 0, "Ne": -1, "Na": 0, "Mg": 0, "Al": 1, "Si": -1, "P": 0, "S": 0,
            "Cl": 1, "Ar": -1, "K": 0, "Ca": 0, "Sc": 0, "Ti": 0, "V": 0, "Cr": 0,
            "Mn": 0, "Fe": -1, "Co": 0, "Ni": 0, "Cu": 0, "Zn": 0, "Ga": 0, "Ge": 0,
            "As": 0, "Se": 0, "Br": 0, "Kr": 0, "Rb": 0, "Sr": 0, "Y": 0, "Zr": 0
        }

        # --- НАСТРОЙКА И ИНИЦИАЛИЗАЦИЯ КАРТЫ ---
        # --- НАСТРОЙКА И ИНИЦИАЛИЗАЦИЯ КАРТЫ ДЕМО-УРОВНЯ ---
        sq_s = 10
        grid_size_x = 75
        grid_size_y = 75

        LV1_data = game_data((grid_size_x, grid_size_y), sq_s)

        kol = 60
        # Добавляем серную кислоту, оксиды железа и простые газы
        tepes = ['H 2/O 0', 'O 2/O 0', 'H 2/S 1/O 4', 'Fe 1/O 1', 'Fe 2/O 3']

        for _ in range(kol):
            tp = random.choice(tepes)
            mo = molekyla('1', tp, "game")

            # ЗАДАЕМ ЯРКИЕ, КОНТРАСТНЫЕ ЦВЕТА (Они больше не сольются с фоном!)
            if tp == 'H 2/O 0':
                mo.color = (255, 255, 255)  # Водород — чисто белый
            elif tp == 'O 2/O 0':
                mo.color = (0, 200, 255)  # Кислород — ярко-голубой
            elif tp == 'H 2/S 1/O 4':
                mo.color = (255, 0, 255)  # Серная кислота — ярко-фиолетовая/маджента
                mo.rt = 50.0
            elif tp == 'Fe 1/O 1':
                mo.color = (255, 128, 0)  # Оксид железа II — сочный оранжевый
                mo.rt = 50.0
            elif tp == 'Fe 2/O 3':
                mo.color = (255, 180, 50)  # Оксид железа III — золотисто-желтый
                mo.rt = 50.0

            mo.compile_A_and_B()
            mo.compile_razl(0.05, 20)

            x_chunk = random.randint(0, grid_size_x - 1)
            y_chunk = random.randint(0, grid_size_y - 1)

            if x_chunk == 37 and y_chunk == 37:
                x_chunk += 1

            lx = random.uniform(0, sq_s - 0.01)
            ly = random.uniform(0, sq_s - 0.01)

            mo.global_cord = [x_chunk * sq_s + lx, y_chunk * sq_s + ly]

            LV1_data.MofD[y_chunk][x_chunk].clear()
            LV1_data.MofD[y_chunk][x_chunk].append([mo, lx, ly])

        # Фиксируем игрока поверх ботов в центре
        start_x = 37 * sq_s + (sq_s / 2)
        start_y = 37 * sq_s + (sq_s / 2)
        my_player = player("O", "PLAYER_OXYGEN", "game", start_x, start_y)

        LV1_data.MofD[37][37].clear()
        LV1_data.MofD[37][37].append([my_player, sq_s / 2, sq_s / 2])
        LV1_data.player_obj = my_player

        print("Sikses")
        time.sleep(1)
        LV1_data.printt()

        # Собираем и увязываем классы поля
        LV1_pole = gamepole((150, 150), LV1_data)
        self.gamep = LV1_pole
        LV1_data.gamep = LV1_pole  # Прокидываем температурный мостик

        self.pol = poledraw((750, 750), LV1_data.MofD, sq_s, self.screen)
        self.tick = 0

        # --- СОЗДАНИЕ ТВОИХ КНОПОК БОНУСОВ ---
        # Боковая панель (ширина 200px, начинается с X=750)
        self.bonus_win = window((200, 750), 10, (750, 0), (40, 40, 50), 0, self.screen)

        # Передаем методы класса через self.имя_метода
        b_push = button((180, 60), (760, 50), (0, 200, 100), self.bonus_push, self.screen, ("PUSH", 24))
        b_tup = button((180, 60), (760, 150), (220, 50, 50), self.bonus_temp_up, self.screen, ("TEMP +50", 24))
        b_tdown = button((180, 60), (760, 250), (50, 100, 220), self.bonus_temp_down, self.screen, ("TEMP -50", 24))

        self.bonus_win.elements = [b_push, b_tup, b_tdown]

    def compile_menu(self):
        c1 = (0,0,100)
        c2 = (0,0,200)
        c3 = (100,100,200)

        elements_s2 = []
        for i,el in enumerate(self.elements_data):
            col = (255,0,255)
            ot = self.elements_data.get(el)
            if ot == -1:
                col = c1
            if ot == 0:
                col = c2
            if ot == 2:
                col = c3
            x_p = (i*50)%700
            y_p = int((i*50)/700)
            print(y_p)
            print()
            elements_s2.append(button((50,50),(x_p,y_p*50),col,self.nollF,self.screen,(el,32)))
        return elements_s2

    def fc(self,screen):
        self.compile_flag = True
        screen.elements = self.compile_menu()

    #tools
    def chgl(self,elements,cord):
        for el in elements:
            el.check(cord)

    def nollF(self,a):
        print("Click")
        print(a)

    def update(self):
        is_update = True

        while is_update:
            self.screen.fill(self.base_color)
            cord = pygame.mouse.get_pos()

            if self.w == 0:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        is_update = False
                    if event.type == pygame.MOUSEBUTTONUP:
                        rn = self.b1.check(cord)
                self.b1.draw()

            elif self.w == 1:
                if self.is_anim == True:
                    if self.sc2.animate():
                        self.is_anim = False
                        self.sc2.elements = [self.rn_but]
                else:
                    self.sc2.draw()
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            is_update = False
                        if event.type == pygame.MOUSEBUTTONUP:
                            self.rn_but.check(cord)

            elif self.w == 2:
                if not self.compile_flag:
                    self.fc(self.menu)
                else:
                    self.menu.draw()
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            is_update = False
                        if event.type == pygame.MOUSEBUTTONUP:
                            self.chgl(self.menu.elements, cord)

            elif self.w == 3:
                # 1. Обработка событий Pygame (добавили клики мышки по кнопкам бонусов)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        is_update = False
                    if event.type == pygame.MOUSEBUTTONUP:
                        # Если кликнули мышкой, проверяем каждую кнопку в панели бонусов
                        for btn in self.bonus_win.elements:
                            btn.check(cord)

                # 2. Опрос клавиатуры для управления зеленым атомом
                if hasattr(self.gamep.father, 'player_obj') and self.gamep.father.player_obj is not None:
                    self.gamep.father.player_obj.handle_input()

                # 3. Физика перемещения и взаимодействия молекул
                self.gamep.father.move(self.tick)

                # Синхронизируем массив отрисовщика с живой картой чанков
                self.pol.el = self.gamep.father.MofD

                # 4. Отрисовка левой части (микромир)
                self.pol.draww()

                # 5. Отрисовка правой части (панель бонусов и её кнопки)
                self.bonus_win.draw()

                # 6. Сбор дебаг-информации
                current_info = self.gamep.father.get_info((0, 0), 100)
                self.alld.append(len(current_info))

                # --- ГЕЙМПЛЕЙ: ПРОВЕРКА УСЛОВИЯ ПОБЕДЫ ---
                player = self.gamep.father.player_obj
                px_chunk = int(player.global_cord[0] // self.gamep.father.chank_size)
                py_chunk = int(player.global_cord[1] // self.gamep.father.chank_size)

                if 0 <= px_chunk < self.gamep.father.size[0] and 0 <= py_chunk < self.gamep.father.size[1]:
                    current_chunk_objects = self.gamep.father.MofD[py_chunk][px_chunk]
                    if len(current_chunk_objects) >= 3:
                        print("ПОБЕДА!")
                        #self.w = 4wwwww

                self.tick += 1


            elif self.w == 4:
                # ЭКРАН ПОБЕДЫ ДЛЯ КОМИССИИ
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        is_update = False

                # Рисуем красивую надпись по центру экрана
                font = pygame.font.SysFont("Arial", 48)
                text = font.render("ПОБЕДА! H2O СИНТЕЗИРОВАНА!", True, (0, 255, 0))
                self.screen.blit(text, (100, 350))

            pygame.display.flip()
            self.clock.tick(60)


class poledraw:
    def __init__(self,size,elements,sq_s,screen):
        self.size = size
        self.el = elements
        self.screen = screen
        self.sq_s = sq_s

    def draww1(self):
        sq_s = self.sq_s
        #print(self.el[-1][-1][0])
        pygame.draw.rect(self.screen,(0,0,100),pygame.Rect(0,0,self.size[0],self.size[1]))
        for x,el in enumerate(self.el):
            for y,el5 in enumerate(el):
                for el2 in el5:
                    #print(el2)
                    if el2[0] is None:
                        pass
                    else:
                        #pygame.draw.rect(self.screen, (40, 40, 250),
                                         #pygame.Rect(x * sq_s - sq_s, y * sq_s - sq_s, sq_s, sq_s))
                        dtt = el2[0].get_info()
                        #print(dtt)
                        #print(dt.periodic_table1.get(el2[0].rn))
                        size = int(dt.periodic_table1.get(el2[0].rn)[0][4]/10*sq_s)+1
                        col = dtt[3]
                        if col == (0,0,0):
                            pygame.draw.ellipse(self.screen,(200,20,20),pygame.Rect(x*sq_s-el2[1],y*sq_s-el2[2],sq_s,sq_s))

    def draww(self):
        sq_s = self.sq_s

        # ЖЕСТКО ФИКСИРУЕМ РАЗМЕР ОКНА ОТРИСОВКИ ЧАНКОВ (750x750 пикселей)
        # Это мгновенно и навсегда решает проблему с rect argument is invalid!
        width = 750
        height = 750

        # Рисуем глубокий темно-синий фон космической лаборатории
        pygame.draw.rect(self.screen, (10, 10, 40), (0, 0, width, height))

        bond_length = 20.0  # Длина химической связи между центрами атомов

        for row in self.el:
            for chunk in row:
                for el2 in chunk:
                    # Строгая проверка структуры ячейки [obj, local_x, local_y]
                    if el2 is not None and len(el2) >= 3:
                        # ИСПРАВЛЕНО: Берем нулевой индекс, чтобы достать сам ОБЪЕКТ, а не список ячейки!
                        obj = el2[0]

                        if obj is not None:
                            # Вытаскиваем центральные глобальные координаты молекулы
                            gx, gy = obj.global_cord[0], obj.global_cord[1]

                            # Проверяем, находится ли центр в пределах экрана 750х750
                            if not (0 <= gx <= width and 0 <= gy <= height):
                                continue

                            m_name = str(obj.name)

                            # --- АБСОЛЮТНО БЕЗОПАСНЫЙ ИЗВЛЕКАТЕЛЬ ЦВЕТА ---
                            if hasattr(obj, 'color') and obj.color is not None:
                                atom_color = obj.color
                            else:
                                atom_color = (255, 255, 255)
                            # -----------------------------------------------

                            # --- 1. КАНАЛ ВОДЫ H2O (КАПРИЗ: Рисуем структуру H - O - H на одной прямой) ---
                            if m_name == "H2O" or "H2O" in m_name:
                                # Центральный атом Кислорода (Ярко-голубой)
                                pygame.draw.circle(self.screen, (0, 200, 255), (int(gx), int(gy)), 10)

                                # ИСПРАВЛЕНО: Перебираем 0 и 180 градусов для создания прямой линии H - O - H
                                for h_ang in [0, 180]:
                                    h_rad = math.radians(h_ang)
                                    hx = gx + bond_length * math.cos(h_rad)
                                    hy = gy + bond_length * math.sin(h_rad)

                                    # Линия связи O - H
                                    pygame.draw.line(self.screen, (200, 200, 255), (int(gx), int(gy)),
                                                     (int(hx), int(hy)), 2)
                                    # Сам атом Водорода (Чисто белый)
                                    pygame.draw.circle(self.screen, (255, 255, 255), (int(hx), int(hy)), 6)

                            # --- 2. ИЗУМРУДНЫЙ СУЛЬФАТ ЖЕЛЕЗА (FeSO4) ---
                            # Если цвет изумрудный или в имени есть Fe/S/числа — рисуем СТРУКТУРНЫЙ КРЕСТ СВЯЗЕЙ!
                            elif atom_color == (0, 255, 100) or "FeSO4" in m_name or ("Fe" in m_name and "S" in m_name):
                                # Рисуем центральное изумрудный круг Железа (Fe)
                                pygame.draw.circle(self.screen, (0, 200, 100), (int(gx), int(gy)), 11)

                                # 4 Кислорода по углам -45, 45, 135, 225
                                for ang in [-45, 45, 135, 225]:
                                    rad = math.radians(ang)
                                    ox = gx + bond_length * math.cos(rad)
                                    oy = gy + bond_length * math.sin(rad)

                                    # Линия связи соли (темно-зеленая)
                                    pygame.draw.line(self.screen, (0, 120, 50), (int(gx), int(gy)), (int(ox), int(oy)),
                                                     2)
                                    # Сам Кислород (красный)
                                    pygame.draw.circle(self.screen, (255, 50, 50), (int(ox), int(oy)), 7)

                            # --- 3. СЕРНАЯ КИСЛОТА (H2SO4) ---
                            elif "S" in m_name and "O" in m_name and "Fe" not in m_name:
                                pygame.draw.circle(self.screen, (255, 255, 0), (int(gx), int(gy)),
                                                   10)  # Сера 'S' (Желтая)

                                for ang in [-45, 45, 135, 225]:
                                    rad = math.radians(ang)
                                    ox = gx + bond_length * math.cos(rad)
                                    oy = gy + bond_length * math.sin(rad)
                                    pygame.draw.line(self.screen, (100, 100, 150), (int(gx), int(gy)),
                                                     (int(ox), int(oy)), 2)
                                    pygame.draw.circle(self.screen, (255, 50, 50), (int(ox), int(oy)),
                                                       7)  # Кислород 'O'

                                # Дорисовываем Водороды (H) на прямой линии по бокам
                                if "H" in m_name or "2.2" in m_name:
                                    for h_ang in [0, 180]:
                                        h_rad = math.radians(h_ang)
                                        hx = gx + (bond_length * 1.8) * math.cos(h_rad)
                                        hy = gy + (bond_length * 1.8) * math.sin(h_rad)
                                        pygame.draw.line(self.screen, (200, 200, 255), (int(gx), int(gy)),
                                                         (int(hx), int(hy)), 1)
                                        pygame.draw.circle(self.screen, (255, 255, 255), (int(hx), int(hy)), 5)

                            # --- 4. ПЯТИУГОЛЬНИКИ ОКСИДОВ ЖЕЛЕЗА ---
                            elif "Fe" in m_name and "O" in m_name and "S" not in m_name:
                                fe_count = 2 if "2" in m_name else 1
                                o_count = 3 if "3" in m_name else 1
                                total_atoms = fe_count + o_count

                                for i in range(total_atoms):
                                    ang = (360 / total_atoms) * i
                                    rad = math.radians(ang)
                                    ax = gx + bond_length * math.cos(rad)
                                    ay = gy + bond_length * math.sin(rad)

                                    pygame.draw.line(self.screen, (120, 100, 100), (int(gx), int(gy)),
                                                     (int(ax), int(ay)), 2)
                                    if i < fe_count:
                                        pygame.draw.circle(self.screen, (255, 128, 0), (int(ax), int(ay)),
                                                           9)  # Железо 'Fe' (Оранжевое)
                                    else:
                                        pygame.draw.circle(self.screen, (255, 50, 50), (int(ax), int(ay)),
                                                           7)  # Кислород 'O' (Красный)

                            # --- 5. ЧИСТОЕ ЖЕЛЕЗО (Fe) ---
                            elif "Fe" in m_name:
                                pygame.draw.circle(self.screen, (120, 120, 120), (int(gx), int(gy)),
                                                   12)  # Крупное серое Железо

                            # --- 6. ПРОСТЫЕ ОДИНОЧНЫЕ АТОМЫ И ГАЗЫ (ИГРОК, H2, O2) ---
                            else:
                                # Зеленый игрок получает радиус 14, остальные газы — 8
                                radius = 14 if "PLAYER" in m_name else 8
                                pygame.draw.circle(self.screen, atom_color, (int(gx), int(gy)), radius)
class button:
    def __init__(self,size,pos,color,func,screen,txt_s = (0,0)):
        self.size = size
        self.pos = pos
        self.color = color
        self.func = func
        self.screen = screen
        print(txt_s)
        self.font = self.font = pygame.font.Font(None,txt_s[1])
        self.text = txt_s[0]


    def check(self,cord):
        x = cord[0] - self.pos[0]
        y = cord[1] - self.pos[1]
        if x > 0 and y > 0 and self.size[0] >= x and self.size[1] >= y:
            print("Presed")
            return self.func(self.text)
        return False

    def draw(self):
        if self.text != 0:
            tit = self.font.render(self.text, True, (0, 0, 0))
            y = pygame.draw.rect(self.screen,self.color,pygame.Rect(self.pos[0],self.pos[1],self.size[0],self.size[1]))
            self.screen.blit(tit, tit.get_rect(center=y.center))
        else:
            pygame.draw.rect(self.screen, self.color, pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1]))



class window:
    def __init__(self,size,speed,pos,color,a,screen):
        self.size = size
        self.pos = pos
        self.color = color
        self.screen = screen
        self.speed = speed
        self.a = a

        self.tick = round(size[a%2]/speed)
        self.ids = 1

        self.elements = []

    def draw(self):
        pygame.draw.rect(self.screen,self.color,pygame.Rect(self.pos[0],self.pos[1],self.size[0],self.size[1]))
        for el in self.elements:
            el.draw()
            #time.sleep(0.5)
            #pygame.display.flip()

    def animate(self):
        if self.a == 0:
            ys = self.size[1]
            xs = self.ids*self.tick
            self.ids+=1
        else:
            xs = self.size[0]
            ys = self.ids * self.tick
            self.ids += 1
        print(f'xs - {xs} ys - {ys}')
        if xs > self.size[0] or ys > self.size[1]:
            return True
        pygame.draw.rect(self.screen,self.color,pygame.Rect(self.pos[0],self.pos[1],xs,ys))



    def godbye(self):
        self.tick = round(self.size[self.a % 2] / self.speed)
        self.ids = 1












def logigtst():
    a = molekyla('1',"H 2","loler")
    print(a.compile_A_and_B())
    print(a.compile_razl(0.05,0))
    d = game_data((20,20),15)
    u1 = molekyla('1',"Fe 1/O 1",1)
    print(u1.compile_A_and_B())
    print('*')
    u1.compile_razl(0.05,1)
    u2 = molekyla('1',"Fe 2/O 3",1)
    print(u2.compile_A_and_B())
    print('*')
    u2.compile_razl(0.05,1)
    u3 = molekyla('1',"H 2/S 1/O 4",1)
    u3.compile_A_and_B()
    u3.compile_razl(0.05,1)
    d.MofD[5][5][0] = [u1]
    d.MofD[5][6][0] = [u2]
    d.MofD[6][6][0] = [u3]
    c = gamepole((20,20),d)
    print('*')
    c.react([5,5])
#logigtst()
mn = meni()
mn.update()































