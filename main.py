from collections import deque
from Driver import *


# Global Storage Items: Subjects, Tasks, Study Sessions, Templates, Report
PAGES_LIST = ("Pages:\n"
          "1. Schedule Today\n"
          "2. Subjects\n"
          "3. Time Templates\n"
          "4. Tasks\n"
          "5. View Submissions\n"
          "6. View Report\n"
          "7. Exit")


def getPageChoice():
    print(PAGES_LIST)
    pageChoice = int(input("Please enter your choice of page (1-7): "))
    while not (type(pageChoice) == int and 1 <= pageChoice <= 7):
        pageChoice = int(input("Please enter a valid page choice (1-7): "))
    return pageChoice


def main():
    print("Welcome to the Study Buddy App")
    while True:
        print()
        equalToString = '=' * 9
        print(equalToString)
        print("HOME PAGE")
        print(equalToString)
        pageChoice = getPageChoice()
        if pageChoice == 1:
            print("\n\n")
            time_tracker_function()
        elif pageChoice == 2:
            print("\n\n")
            subject_function()
        elif pageChoice == 3:
            print("\n\n")
            templates_function()
        elif pageChoice == 4:  # tasks
            print("\n\n")
            tasks_function()
        elif pageChoice == 5:  # submissions
            print("\n\n")
            submissions_function()
        elif pageChoice == 6:  # reports
            print("\n\n")
            reports_function()
        else:
            break
    print("Have a good day!")


if __name__ == "__main__":
    main()



