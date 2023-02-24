import random
import sqlite3

def get_board_size(complexity):
    if complexity == "легка":
        return 5
    elif complexity == "середня":
        return 10
    else:
        raise ValueError("Невірна складність гри")

def start(complexity, name):
   print("Складність гри: "+ complexity)
   print("Ваше ім'я: "+ name)

def hide_treasure(board):
    animal = 0
    treasures=0
    while treasures <= 1 and animal<=1:
        random_row = random.randrange(0, len(board))
        random_col = random.randrange(0, len(board))
        if 0 <= random_row < len(board) and 0 <= random_col < len(board) and board[random_row][random_col] == " ":
         if treasures == 1 and random.random() < 0.5: # додаткова умова на з'явлення звіра
            board[random_row][random_col] = "Z"
         else:
            board[random_row][random_col] = "T"
            treasures += 1

def generate_map(board, show_treasure=False):
    size = len(board)
    print("  ", end="")
    for i in range(size):
         print("   %d" % i, end="")
    print("\n   " + "---+" * size)
    for row in range(size):
        print( "%d |" % row, end="")
        for col in range(size):
            cell = " " if board[row][col] in ["T", "Z"] and not show_treasure else board[row][col]
            print(" %s |" % cell, end="")
        print("\n   " + "---+" * size)

def make_user_move(board):
    valid_move=False
    while not valid_move:
        try:
            ask_row = int(input("В якому рядку ви б хотіли шукати (0-%d): " % (len(board) - 1)))
            ask_col = int(input("В якому стовпцю ви б хотіли шукати (0-%d): " % (len(board) - 1)))
            if board[ask_row][ask_col] == "T":
                board[ask_row][ask_col] = "$"
                print("Так! Ви знайшли скарб")
                return True
            elif board[ask_row][ask_col] == "Z":
                board[ask_row][ask_col] = "&"
                print("Ви натрапили на звіра")
                return True
            elif board[ask_row][ask_col] == "$" or board[ask_row][ask_col] == "X" or board[ask_row][ask_col] == "&":
                print("Ви вже тут шукали, виберіть інші координати: ")
            else:
                board[ask_row][ask_col]="X"
                print("Тут нічого немає")
                break
        except ValueError:
            print("Ви ввели невірні координати!")
            continue
        except IndexError:
            print("Це не дійсне місцезнаходження. Спробуйте щераз!")

def main():

   complexity = input("Виберіть складність гри (легка/середня): ")
   name = input("Вкажіть ваше ім'я: ")

   size = get_board_size(complexity)
   board = [[" " for _ in range(size)] for _ in range(size)]
   
   print("Ласкаво просимо до гри Пошук Скарбів!")
   guess=5
   treasures=0
   animal = 0
   while guess!=0 and treasures!=1 :
         print("У вас є",guess,"спроб, щоб знайти ",treasures,"/1  скарб.")
         hide_treasure(board)
         generate_map(board)
         start(complexity,name)
         guess-=1
         if make_user_move(board):
            treasures+=1

         if guess == 0:
            print("У вас закінчилися спроби!")
            print("*** Гра завершина ***")
            break
         if animal==1:
            generate_map(show_treasure=False)
            print("Ви натрапили на звіра!!!")
            print("*** Гра завершина ***") 
         elif treasures==1:
            generate_map(board)
            print("*** Гра завершина ***")

def database():
   connect = sqlite3.connect('game_server.db')
   cursor = connect.cursor()

   cursor.execute("""CREATE TABLE IF NOT EXISTS players (
        name TEXT,
        level TEXT
   )""")
    
   name = input('Нік: ')
   game = input('Складність: ')

   cursor.execute(f"SELECT name FROM players WHERE name LIKE '%{name}%'")
   data = cursor.fetchone()

   if data is None:
      cursor.execute("INSERT INTO players (name, level)values(?, ?);", [name, game])
      connect.commit()
   else:
        print('Такий нік вже є')


database()
main()
#В мене не вийшло  нормально підкючити базу даних, тому я зробив так.