# -*- coding: utf-8 -*-
"""
Author: Shustov Aleksei (SemperAnte), semperante@mail.ru
 
Домашнее задание к занятию 25
"""
import scipy.stats
import math

def step1_type1(data, typeA):
    ''' Тип задачи - 1
        Строим математическую модель, формулируем гипотезы,
        формулируем утверждение о статистике критерия'''
        
    data['n12'] = data['n1p'] - data['n11'] # неудачи опыта 1
    data['n22'] = data['n2p'] - data['n21'] # неудачи опыта 2
    data['np1'] = data['n11'] + data['n21'] # всего успехов
    data['np2'] = data['n12'] + data['n22'] # всего неуспехов
    data['n'] = data['n1p'] + data['n2p']   # всего опытов

    print('0. Математическая модель')
    print(f'{"":10s}|{"успехи":10s}|{"неудачи":10s}|{"всего":10s}|')
    print('-'*44)
    print('{:10s}|{:10d}|{:10d}|{:10d}|'.format('1 серия', data['n11'], data['n12'], data['n1p']))
    print('{:10s}|{:10d}|{:10d}|{:10d}|'.format('2 серия', data['n21'], data['n22'], data['n2p']))
    print('{:10s}|{:10d}|{:10d}|{:10d}|'.format('всего', data['np1'], data['np2'], data['n']))
    
    print('1. Гипотезы')
    print('Ho: p1 = p2')
    if typeA == 1:
        print('Ha: p1 != p2')
    elif typeA == 2:
        print('Ha: p1 > p2')
    elif typeA == 3:
        print('Ha: p1 < p2')
    else:
        raise TypeError('Wrong type for typeA.')
        
    print('2. Утверждение о статистике критерия')
    print('Если гипотеза Ho верна, то T ~ N(0; 1)')
    return data

def step2_type1(data):
    ''' Тип задачи - 1
        Вычисляем значение статистики критерия '''
    
    T = (data['n11']/data['n1p'] - data['n12']/data['n2p']) / \
        (math.sqrt(data['np1']/data['n'] * \
                   (1 - data['np1']/data['n'])*(1/data['n1p'] + 1/data['n2p'])))
    print(f'3. Статистика критерия - {T:.2f}')
    return T

def step1_type2(data1, data2, typeA):
    ''' Тип задачи - 2
        Cтроим математическую модель, формулируем гипотезы,
        формулируем утверждение о статистике критерия'''
        
    print(f'Данные 1: {data1}')
    print(f'Данные 2: {data2}')
    
    # объединенный отсортированный список
    com = data1 + data2
    com.sort()
    # простой способ нахождения ранга в объединенной выборке
    def find_rank(data):
        rank = []
        for elem in data:
            idx = com.index(elem)
            count = com.count(elem)
            rank.append(idx + 1 + count / 2 - 0.5)
        return rank
        
    rank1 = find_rank(data1)
    rank2 = find_rank(data2)
        
    print(f'Ранг 1: {rank1}')
    print(f'Ранг 2: {rank2}')
    
    print('1. Гипотезы')
    print('Ho: p1 = p2')
    if typeA == 1:
        print('Ha: p1 != p2')
    elif typeA == 2:
        print('Ha: p1 > p2')
    elif typeA == 3:
        print('Ha: p1 < p2')
    else:
        raise TypeError('Wrong type for typeA.')
        
    print('2. Утверждение о статистике критерия')
    print('Если гипотеза Ho верна, то W ~ N(0; 1)')
    return (rank1, rank2)

def step2_type2(rank1, rank2):
    ''' Тип задачи - 2
        Вычисляем значение статистики критерия '''
    
    print('3. Вычисляем значение статистики критерия')
    W = sum(rank2)
    print(f'W = {W}')
    m = len(rank1)
    n = len(rank2)
    M = n / 2 * (m + n + 1)
    print(f'M = {M:.2f}')
    D = m * n / 12 * (m + n + 1)
    print(f'D = {D:.2f}')    
    WS = (W - M)/math.sqrt(D)
    print(f'Статистика критерия, WS = {WS:.2f}')
    return WS

def step3(alpha, typeA, T):
    ''' Доверительная и критическая области,
        принятие решения '''

    if typeA == 1:
        ppf1 = scipy.stats.norm.ppf(alpha/2)
        ppf2 = scipy.stats.norm.ppf(1 - alpha/2) 
        print(f'4a. Доверительная область: [{ppf1:.2f}; {ppf2:.2f}]')
        print(f'Критическая область: T < {ppf1:.2f} или T > {ppf2:.2f}')
        print(f'Уровень значимости - {alpha:.2f}')        
        res =  ppf1 < T < ppf2
    elif typeA == 2:
        ppf = scipy.stats.norm.ppf(1 - alpha)
        print(f'4a. Доверительная область: T < {ppf:.2f}')
        print(f'Критическая область: T > {ppf:.2f}')
        print(f'Уровень значимости - {alpha:.2f}')
        res = T < ppf
    elif typeA == 3:
        ppf = scipy.stats.norm.ppf(alpha)
        print(f'4a. Доверительная область: T > {ppf:.2f}')
        print(f'Критическая область: T < {ppf:.2f}')
        print(f'Уровень значимости - {alpha:.2f}')
        res = T > ppf
    else:
        raise TypeError('Wrong type for typeA.')
            
    if res:
        print('5a. Статистика критерия попала в доверительную область')
        print('Принимается Ho')
    else:
        print('5a. Статистика критерия попала в критическую область')
        print('Принимается Ha')
            
def step4(T, typeA):
    ''' Высисление p-значения '''
    
    cdf = scipy.stats.norm.cdf(T)
    if typeA == 1:    
        p = min(2*cdf, 2 - 2*cdf)
    elif typeA == 2:
        p = 1 - cdf
    elif typeA == 3:
        p = cdf
    print(f'4b. P-значениие: {p:.2f}')
    return p

if __name__ == '__main__':
    # Задача 1
    # основная гитпотеза - p1 = p2
    # выбираем тип альтернативной гипотезы
    # 1 - p1 != p2
    # 2 - p1 > p2
    # 3 - p1 < p2
    typeA = 1
    # уровень значимости
    alpha = 0.05
    # исходные данные
    data = {}
    data['n11'] = 42        # успехи опыта 1
    data['n1p'] = 105       # всего опытов 1
    data['n21'] = 65        # успехи опыта 2
    data['n2p'] = 195       # всего опытов 2
    print('Решение задачи 1')
    data = step1_type1(data, typeA)
    T = step2_type1(data)
    step3(alpha, typeA, T)
    p = step4(T, typeA)   

    # Задача 2
    # основная гитпотеза - p1 = p2
    # выбираем тип альтернативной гипотезы
    # 1 - p1 != p2
    # 2 - p1 > p2
    # 3 - p1 < p2
    typeA = 2
    # уровень значимости
    alpha = 0.05
    # исходные данные
    data = {}
    data['n11'] = 172        # успехи опыта 1
    data['n1p'] = 172 + 3    # всего опытов 1
    data['n21'] = 168        # успехи опыта 2
    data['n2p'] = 168 + 32   # всего опытов 2
    print('\nРешение задачи 2')
    data = step1_type1(data, typeA)
    T = step2_type1(data)
    step3(alpha, typeA, T)
    p = step4(T, typeA)  
    
    # Задача 3
    # основная гитпотеза - p1 = p2
    # выбираем тип альтернативной гипотезы
    # 1 - p1 != p2
    # 2 - p1 > p2
    # 3 - p1 < p2
    typeA = 2
    # уровень значимости
    alpha = 0.05
    # исходные данные
    data1 = [130, 110, 120, 140, 200, 130, 140, 170, 160, 140]
    data2 = [120, 190, 130, 160, 150, 120, 110, 120, 200]
    print('\nРешение задачи 3')
    rank1, rank2 = step1_type2(data1, data2, typeA)
    T = step2_type2(rank1, rank2)
    step3(alpha, typeA, T)
    p = step4(T, typeA)  
    
    # Задача 4
    # основная гитпотеза - p1 = p2
    # выбираем тип альтернативной гипотезы
    # 1 - p1 != p2
    # 2 - p1 > p2
    # 3 - p1 < p2
    typeA = 1
    # уровень значимости
    alpha = 0.05
    # исходные данные
    data1 = [102.4, 100.0, 67.6, 65.9, 64.7, 39.6, 31.2]
    data2 = [48.1, 45.5, 41.7, 35.4, 29.1, 18.9, 58.3, 68.8, 71.3, 94.3]
    print('\nРешение задачи 4')
    rank1, rank2 = step1_type2(data1, data2, typeA)
    T = step2_type2(rank1, rank2)
    step3(alpha, typeA, T)
    p = step4(T, typeA)  
    
    # Задача из презентации
    # основная гитпотеза - p1 = p2
    # выбираем тип альтернативной гипотезы
    # 1 - p1 != p2
    # 2 - p1 > p2
    # 3 - p1 < p2
    typeA = 3
    # уровень значимости
    alpha = 0.05
    # исходные данные
    data1 = [30, 28, 46, 42, 35, 33, 44, 43, 31, 38]
    data2 = [26, 37, 39, 28, 31, 27, 32, 35]
    print('\nЗадача из презентации')
    rank1, rank2 = step1_type2(data1, data2, typeA)
    T = step2_type2(rank1, rank2)
    step3(alpha, typeA, T)
    p = step4(T, typeA)  