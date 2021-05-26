# Судоку
### Номинация: "Оконные приложения на PyQT"

***

##### Реализованный функционал:  

- Выбор уровня сложности судоку  
- Пауза / продолжение игры с остановкой игрового времени  
- Сохранение / восстановление / удаление записи игрового прогресса  
- Таблица рекордов общая / по каждому судоку отдельно  
- Фильтрация в таблице рекордов по уровню сложности  
- Возможность взятия реванша

Для того, чтобы не изобретать велосипед, в проекте для генерации валидных  
судоку матриц (с единственным решением) используется  
[интерпретация](https://www.cs.mcgill.ca/~aassaf9/python/algorithm_x.html) "[Алгоритма X](https://en.wikipedia.org/wiki/Knuth%27s_Algorithm_X)" 
за авторством Ali Assaf <ali.assaf.mail@gmail.com>

***

##### Запуск приложения:

1. Установить все необходимые зависимости командой  
    `pip install requirements.txt`
   
2. Запустить проект:
   - Напрямую, запустив файл main.py  
     `python main.py` (Windows)  
     или  
     `python3 main.py` (Linux)
     
   - Запустив бинарный файл по пути `/executable/dist/main.exe`  
     
   - Если бинарника нет, то скомпилировав проект с помощью pyinstaller:
     
     * установить pyinstaller командой `pip install pyinstaller`  
       (если вдруг он не установился сам на первом шаге)  
       
     * запустить .bat файл по пути`/executable/compilation.bat`  
       через командную строку
       
     * запустить .exe файл по пути `/executable/dist/main.exe`
    
3. Наслаждаться кофе / чаем с плюшками за разгадыванием судоку :)

***

Для проверки того, что судоку действительно разрешимо можно воспользоваться  
[сторонними ресурсами](https://sudokus.ru/reshateli/),
или же включить в приложении режим дебага,  
задав в файле settings.py
`DEBUG_MODE = True` и запустив исходник напрямую,  
подсмотреть решение в консоли.

***

#### Приятного тестирования, мой друг!)






