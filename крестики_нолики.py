symbol=""

def main():
    print("******************ИГРА КРЕСТИКИ НОЛИКИ*************************")
    print("")
    print("*********************ВИД ПОЛЯ**********************************")
    print("")
    print("Для хода нужно ввести координаты клетки X Y (где X - столбец, Y - строка)")
    


def pole_draw():
    print("      0     1     2 ")
    print("    ----------------")
    for i,j in enumerate(filds):
        print(f"{i}   | {'  |  '.join(j)}  |" )
        print("    ----------------")
        print("")
    return


def vvod():
   while True:
    koordinat = input("Введите координаты клетки ")
    l=[]
    l=koordinat.split()
    if len(koordinat) > 3:
        print("Неверный формат, введите два числа через пробел")
        continue
    if  (not koordinat[0].isdigit()) or (not koordinat[2].isdigit()):
            print("Вы ввели не числа")
            continue
    x = int(l[0])
    y = int(l[1])
    if (x>2 or y>2):
        print("Неверный формат, числа вне диапазона")
        continue
    if (filds[x][y] =="X" or filds[x][y] =="O"):
        print("Клетка занята!")
        continue
    return x,y

def check_win(filds):
    win=0
    for j in range(0,3):
       if filds[0][j] == filds[1][j] == filds[2][j] == symbol:
           print(symbol + " выиграл!")
           win=1
       if filds[j][0] == filds[j][1] == filds[j][2] == symbol:
           print(symbol + " выиграл!")
           win=1
       if filds[0][0] == filds[1][1] == filds[2][2] == symbol:
           print(symbol + " выиграл!")
           win=1
       if filds[2][0] == filds[1][1] == filds[0][2] == symbol:
           print(symbol + " выиграли!")
           win=1
    return win

main()

filds = [["-", "-", "-"],["-", "-", "-"],["-", "-", "-"]]

pole_draw()

for i in range(1,10):
    
    if i%2 == 1:
        print("Ходят крестики")
        x, y = vvod()
        filds[x][y] =symbol= "X"
        pole_draw()
    else:
        print("Ходят нолики")
        x, y = vvod()
        filds[x][y] =symbol= "O"
        pole_draw()
                    
    if check_win(filds)==1:
        break
    if i==9:
        print("Ничья!")
        break
   
pole_draw()