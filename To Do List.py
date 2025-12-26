#To Do List 

import os
print("Current working directory is:", os.getcwd()) 

tasklist = [

]

try:
    with open("tasks.txt", "r", encoding="utf-8") as f:
        tasklist = [line.strip() for line in f.readlines()]
except FileNotFoundError:
    tasklist = []

def save_tasks():
    with open("tasks.txt", "w", encoding="utf-8") as f:
        for task in tasklist:
            f.write(task + "\n")

def todolist():
    for x, tasks in enumerate(tasklist):
            print(f"{x + 1}: {tasks}")


def main():
    print("Here are your options:") 
    print("""
1) View Tasks
2) Add Tasks 
3) Mark Tasks As Done 
4) Delete Task 
5) Quit
          """)
    Options = input("Now please choose an option (1/2/3/4/5) ").lower().strip()

    if Options == "1":
        todolist()
        if tasklist == [

        ]:
            print("No tasks added")
            print()
        main()

    elif Options == "2": 
        asktask = input("Please add your task here: ")
        if asktask: 
            print("Task Added!")
        
        tasklist.append(asktask)
        save_tasks()
        print()
        main()

    elif Options == "3":
        todolist()

        if not tasklist:
            print("No tasks to mark done.")
            main()
            return

        print("This is your current to do list above.")
        print("Which task do you want to mark done?")

        Running = True
        while Running:
            try:
                ask_mark_done = int(input("Please enter the number of the task you want to mark done here: ").strip())
            except ValueError:
                print("Please enter a valid number.")
                continue

            ask_mark_done2 = ask_mark_done - 1
            if 0 <= ask_mark_done2 < len(tasklist):
                if not tasklist[ask_mark_done2].endswith("✔️"):
                    tasklist[ask_mark_done2] += " ✔️"
                    save_tasks()
                    print(f"Task {ask_mark_done} marked done!")
                else:
                    print("That task is already marked done.")
                Running = False
                break
            else:
                print("Invalid task number. Please choose between 1 and", len(tasklist))

        main()
    
    elif Options == "4": 
         todolist()

         print("This is your current to do list above.")
         print("Which task do you want to delete?")
         
         playing = True 

         while playing: 
              ask_delete = int(input("Please enter the number of the task you want to delete here: ").strip())
              ask_delete2 = ask_delete - 1 

              if 0 <= ask_delete2 < len(tasklist): 
                   tasklist.pop(ask_delete2)
                   save_tasks()
                   print(f'Task {ask_delete} deleted!')
                   playing = False
                   break 
              else:
                   print("Invalid Input")
                   continue
              
         main()

    elif Options == "5":
         print("Thank You!")
         return
                   


main()


