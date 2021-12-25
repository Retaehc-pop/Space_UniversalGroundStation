import json
import os
import Port
import sys
import string
import time
from Clock import RTC
from Port import Port
import threading


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
        self.project = project
        self.ckp1()
        print("connection established!")
        self.display()

    def ckp1(self):
        self.comport = None
        while self.comport is None:
            self.comport = self.choose_port()

        self.PORT = Port(com=self.comport, end=self.project.end,
                         file_name=self.project.file, key=self.project.PKG)
        temp = input("Ready to connect? y/n : ")
        if temp.lower() == "y":
            self.PORT.connect()
        else:
            self.ckp()

    def format_data(self, PKG: dict):
        prompt = 0
        data = ""
        for key, data in PKG:
            pkg_tmp = f"{key}: {data}"
            prompt += 1
            pkg_tmp += "\n" if prompt % 4 == 0 else "\t\t"
            data += pkg_tmp
        data += "-------------------------------------------------\n"
        return data

    def display(self):
        self.clock = RTC()
        while True:
            clear()
            print(f"""
    Project:\t\t{self.porject['NAME']}\t\tDate:\t\t{self.clock.RTC.date()}
    Time:\t\t{self.clock.RTC.time_pc()}\t\tElapsed:\t\t{self.clock.time_elapsed()}
############################################################################""")

            PKG = self.PORT.reading()
            toprint = self.format_data(PKG)
            print(toprint)
            time.sleep(0.01)

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
