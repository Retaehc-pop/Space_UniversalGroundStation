import json
import os
import Port
import sys
import string
import time
from Port import Port


def clear():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')


class controller:
    def __init__(self, project: dict) -> None:
        clear()
        print(f"Starting {project['NAME']} ..................")
        time.sleep(1)
        self.comport = None
        while self.comport is None:
            self.comport = self.choose_port()

        self.PORT = Port(com=self.comport, end=project.end,
                         file_name=project.file, key=project.PKG)
        temp = input("Ready to connect? y/n : ")
        if temp.lower() == "y":
            self.PORT.connect()

    def choose_port(self):
        if len(Port.list_port()) == 0:
            input("No Com Port Founded. Please try again! [Enter].....")
            return None
        for index, port in enumerate(Port.list_port()):
            print(f"{index+1} : {port}")
        choose = input("Choose port: ")
        if choose in string.digits:
            if 0 <= int(choose)-1 <= len(Port.list_port()):
                return Port.list_port()[int(choose)]

        else:
            input("No Com Port Founded. Please try again! [Enter].....")
            return None


def menu():
    print("Choose project")
    projects = json.load(open("projects.json"))
    for index, project in enumerate(projects):
        print(f'{index+1} : {project}')
    choice = input("Project = ")
    if choice in projects.keys():
        project = projects[choice]
        controller(project)
    elif choice in string.digits:
        if 0 <= int(choice)-1 <= len(projects.keys()):
            project = projects[list(projects.keys())[int(choice)-1]]
            controller(project)
        else:
            print("try again!")
            splashscreen()
            menu()
    else:
        print("try again!")
        splashscreen()
        menu()


def splashscreen():
    clear()
    print("""
#######################################################################

      ■■■■■ ■■■■■    ■■■   ■■■■■■ ■■■■■■         ■■■   ■■■■■■
     ■      ■    ■  ■   ■  ■    ■ ■             ■   ■  ■    ■
      ■■■■  ■■■■■  ■■■■■■■ ■      ■■■■■■       ■■■■■■■ ■     
          ■ ■      ■     ■ ■    ■ ■            ■     ■ ■    ■
     ■■■■■  ■      ■     ■ ■■■■■■ ■■■■■■       ■     ■ ■■■■■■

#######################################################################
version 0.0.1 Ground Control Station by Retaehc_pop
    """)


if __name__ == "__main__":
    splashscreen()
    menu()
