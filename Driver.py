from datetime import datetime
from Subject import *
from Template import *
from collections import defaultdict


# Global Storage Items: Subjects, Tasks, Study Sessions, Templates, Report
SUBJECT_FUNCTION_PRINT_STRING = "1. Add Subject\n" \
                                "2. Choose Subject\n" \
                                "3. Return To Home Page"

SUBJECT_CHOSEN_PRINT_STRING = "1. Add Topic\n" \
                              "2. Remove Topic\n" \
                              "3. Add Task\n" \
                              "4. Move Task to Submissions\n" \
                              "5. Delete Task\n" \
                              "6. Delete Subject\n" \
                              "7. Back to Previous Menu"

TIME_TRACKER_FUNCTION_PRINT_STRING = "1. Add Session\n" \
                              "2. Remove Session\n" \
                              "3. Return To Home Page" \

SESSION_CHOICE_PRINT_STRING = "1. Study Session\n" \
                              "2. Task Session"

TEMPLATE_CHOICE_PRINT_STRING = "1. Add Session\n" \
                               "2. Remove Session\n" \
                               "3. Return To Home Page"

TASK_FUNCTION_PRINT_STRING = "1. Add Task\n" \
                             "2. Move Task to Submission\n" \
                             "3. Delete Task\n" \
                             "4. Return to Home Page"

TEMPLATE_DAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
Templates = dict()
for day in TEMPLATE_DAYS:
    Templates[day] = Template(day)
Subjects = set()


def getSubjectChoice():
    print(SUBJECT_FUNCTION_PRINT_STRING)
    subjectChoice = int(input("Please enter your choice of operation (1-3): "))
    while not (type(subjectChoice) == int and 1 <= subjectChoice <= 3):
        subjectChoice = int(input("Please enter a valid choice of operation (1-3): "))
    return subjectChoice


def printSubjects(subjectList):
    if not len(subjectList):
        print("There are no subjects yet. Add your subjects to get started!\n")
        return
    maxNameLength = 12
    for subject in subjectList:
        maxNameLength = max(maxNameLength, len(subject.name))
    equalToString = "=" * (maxNameLength + 40)
    underscoreString = "-" * (maxNameLength + 40)
    print(equalToString)
    print("S.No | {:<{}}  | {:<{}} | {:<{}} | {:<{}}".format("Subject Name", maxNameLength,
                                                             "Topics", 6,
                                                             "Tasks", 6,
                                                             "Submissions", 6))
    print(equalToString)
    for i in range(len(subjectList) - 1):
        subject = subjectList[i]
        print("{:<{}} | {:<{}}  | {:<{}} | {:<{}} | {:<{}}".format(i + 1, 4,
                                                                   subject.name, maxNameLength,
                                                                   len(subject.topics), 6,
                                                                   len(subject.pending_tasks), 6,
                                                                   len(subject.submissions), 11))
        print(underscoreString)
    subject = subjectList[-1]
    print("{:<{}} | {:<{}}  | {:<{}} | {:<{}} | {:<{}}".format(len(subjectList), 4,
                                                               subject.name, maxNameLength,
                                                               len(subject.topics), 6,
                                                               len(subject.pending_tasks), 6,
                                                               len(subject.submissions), 6))
    print(equalToString, end='\n\n')


def addSubjectFunction():
    subjectName = input("Enter Subject Name:")
    Subjects.add(Subject(subjectName))
    print("Subject Added Successfully!\n\n\n")


def addTopicFunction(subject):
    topicName = input("Enter Topic Name:")
    subject.add_topic(topicName)
    print("Topic Added Successfully\n\n\n")


def removeTopicFunction(subject):
    topics = list(subject.topics)
    for i in range(len(topics)):
        print("{}. {}".format(i+1, topics[i]))
    topicChoice = int(input("Please Enter a Topic Choice to remove ({} - {}): ".format(1, len(topics))))
    while not (type(topicChoice) == int and 1 <= topicChoice <= len(topics)):
        topicChoice = int(input("Please Enter a Valid Topic Choice ({} - {}): ".format(1, len(topics))))
    topic = topics[topicChoice-1]
    subject.remove_topic(topic)
    print("Topic Removed Successfully\n\n\n")


def addTaskFunction(subject):
    taskName = input("Enter Task Name:")
    deadline = input("Enter the task Deadline date (yyyy-mm-dd): ")
    subject.add_task(taskName, deadline)
    print("Task Added Successfully\n\n\n")


def moveTaskToSubmissionFunction(subject):
    Tasks = list(subject.pending_tasks)
    printSubjectTasks(Tasks)
    if not len(Tasks):
        return
    taskChoice = int(input("Please Enter Task Choice to move to submissions ({} - {}): ".format(1, len(Tasks))))
    while not (type(taskChoice) == int and 1 <= taskChoice <= len(Tasks)):
        taskChoice = int(input("Please Enter a Valid Task Choice ({} - {}): ".format(1, len(Tasks))))
    task = Tasks[taskChoice-1]
    task.moveToSubmissions()
    print("Task moved to Submissions Successfully\n\n\n")


def deleteTaskFunction(subject):
    Tasks = list(subject.pending_tasks)
    printSubjectTasks(Tasks)
    taskChoice = int(input("Please Enter Task Choice to delete ({} - {}): ".format(1, len(Tasks))))
    while not (type(taskChoice) == int and 1 <= taskChoice <= len(Tasks)):
        taskChoice = int(input("Please Enter a Valid Task Choice ({} - {}): ".format(1, len(Tasks))))
    task = Tasks[taskChoice - 1]
    subject.delete_task(task)
    print("Print Task deleted Successfully\n\n\n")


def chooseSubjectFunction():
    if not len(Subjects):
        print("Please add at least one subject before accessing the Choose Subject function\n\n\n")
        return
    subjectsList = list(Subjects)
    subjectChoice = int(input("Please Enter a Subject Choice ({} - {}): ".format(1, len(subjectsList))))
    while not (type(subjectChoice) == int and 1 <= subjectChoice <= len(subjectsList)):
        subjectChoice = int(input("Please Enter a Valid Subject Choice ({} - {}): ".format(1, len(subjectsList))))
    print("\n\n")
    subject = subjectsList[subjectChoice-1]
    while True:
        subject.print()
        print(SUBJECT_CHOSEN_PRINT_STRING)
        operationChoice = int(input("Please enter your choice of operation (1-7): "))
        while not (type(operationChoice) == int and 1 <= operationChoice <= 7):
            operationChoice = int(input("Please enter a valid choice of operation (1-7): "))
        if operationChoice == 1:  # add topic
            addTopicFunction(subject)
        elif operationChoice == 2:  # remove topic
            removeTopicFunction(subject)
        elif operationChoice == 3:  # add task
            addTaskFunction(subject)
        elif operationChoice == 4:  # move task to submission
            moveTaskToSubmissionFunction(subject)
        elif operationChoice == 5:  # delete task
            deleteTaskFunction(subject)
        elif operationChoice == 6:  # delete subject
            subject.detach()
            Subjects.remove(subject)
            print("\n\n")
            break
        elif operationChoice == 7:  # back to previous menu
            print("\n\n")
            break


def subject_function():
    equalsToString = '=' * 11
    while True:
        print(equalsToString)
        print("SUBJECTS TAB")
        print(equalsToString)
        subjectList = list(Subjects)
        printSubjects(subjectList)
        subjectChoice = getSubjectChoice()
        if subjectChoice == 1:  # add subject
            addSubjectFunction()
        elif subjectChoice == 2:  # choose subject
            chooseSubjectFunction()
        elif subjectChoice == 3:  # return to Home page
            print("\n")
            break


def addStudySessionFunction(subject, template):
    topics = list(subject.topics)
    if not len(subject.topics):
        print("Please add at least one topic to {} before proceeding to add a Study Session\n\n\n".format(subject.name))
        return
    printSubjectTopics(topics)
    topicChoice = int(input("Please Enter a Topic Choice ({} - {}): ".format(1, len(topics))))
    while not (type(topicChoice) == int and 1 <= topicChoice <= len(topics)):
        topicChoice = int(input("Please Enter a Valid Topic Choice ({} - {}): ".format(1, len(topics))))
    topic = topics[topicChoice-1]
    start_time = list(map(int, input("Enter session start time (hh:mm (24hr format)): ").split(':')))
    end_time = list(map(int, input("Enter session end time (hh:mm (24hr format)): ").split(':')))
    session = topic.add_session(start_time, end_time, template)
    template.addSession(session)
    print("Study Session added successfully!\n\n\n")


def addTaskSessionFunction(subject, template):
    taskList = list(subject.pending_tasks)
    if not len(taskList):
        print("Please add at least one task to {} before proceeding to add a Task Session\n\n\n".format(subject.name))
        return
    printSubjectTasks(taskList)
    taskChoice = int(input("Please Enter Task Choice ({} - {}): ".format(1, len(taskList))))
    while not (type(taskChoice) == int and 1 <= taskChoice <= len(taskList)):
        taskChoice = int(input("Please Enter a Valid Task Choice ({} - {}): ".format(1, len(taskList))))
    task = taskList[taskChoice-1]
    start_time = list(map(int, input("Enter session start time (hh:mm (24hr format)): ").split(':')))
    end_time = list(map(int, input("Enter session end time (hh:mm (24hr format)): ").split(':')))
    session = task.add_session(start_time, end_time, template)
    template.addSession(session)
    print("Task Session added successfully!\n\n\n")


def addSessionFunction(template):
    subjectsList = list(Subjects)
    if not len(subjectsList):
        print("You don't have any current subjects. "
              "Please add at least one subject before accessing the Add Session operation\n\n\n")
        return
    printSubjects(subjectsList)
    subjectChoice = int(input("Please Enter a Choice of Subject to add a session to ({} - {}): ".format(1, len(subjectsList))))
    while not (type(subjectChoice) == int and 1 <= subjectChoice <= len(subjectsList)):
        subjectChoice = int(input("Please Enter a Subject Choice ({} - {}): ".format(1, len(subjectsList))))
    subject = subjectsList[subjectChoice - 1]
    print(SESSION_CHOICE_PRINT_STRING)
    sessionChoice = int(
        input("Please Enter a Session Choice to add Session to (1 - 2): "))
    while not (type(sessionChoice) == int and 1 <= sessionChoice <= 2):
        sessionChoice = int(input("Please Enter a Valid Session Choice ({} - {}): ".format(1, len(subjectsList))))
    if sessionChoice == 1:  # add Study Session
        addStudySessionFunction(subject, template)
    else:  # add Task Session
        addTaskSessionFunction(subject, template)


def removeSessionFunction(template):
    sessionList = list(template.sessions)
    for i in range(len(sessionList)):
        session = sessionList[i]
        print(i+1)
        session.print()
    sessionChoice = int(
        input("Please Enter a Session Number to remove ({} - {}): ".format(1, len(sessionList))))
    while not (type(sessionChoice) == int and 1 <= sessionChoice <= len(sessionList)):
        sessionChoice = int(input("Please Enter a Valid Subject Choice ({} - {}): ".format(1, len(sessionList))))
    session = sessionList[sessionChoice - 1]
    session.delete()
    print("Session Removed Successfully!")


def getTimeTrackerChoice():
    print(TIME_TRACKER_FUNCTION_PRINT_STRING)
    timeTrackerChoice = int(input("Please enter your choice of operation (1-3): "))
    while not (type(timeTrackerChoice) == int and 1 <= timeTrackerChoice <= 3):
        timeTrackerChoice = int(input("Please enter a valid choice of operation (1-3): "))
    return timeTrackerChoice


def getTemplateChoice():
    print(TEMPLATE_CHOICE_PRINT_STRING)
    timeTrackerChoice = int(input("Please enter your choice of operation (1-3): "))
    while not (type(timeTrackerChoice) == int and 1 <= timeTrackerChoice <= 3):
        timeTrackerChoice = int(input("Please enter a valid choice of operation (1-3): "))
    return timeTrackerChoice


def time_tracker_function():
    equalToString = "=" * 16
    while True:
        day = datetime.today().strftime("%A")
        print(equalToString)
        print("TIME TRACKER TAB")
        print(equalToString)
        print(day.upper())
        template = Templates[day]
        template.printSchedule()
        timeTrackerChoice = getTimeTrackerChoice()
        if timeTrackerChoice == 1:  # Add Session
            if not len(Subjects):
                print("You don't have any current subjects. "
                      "Please add at least one subject before accessing the Add Session operation\n\n")
                continue
            addSessionFunction(template)
        elif timeTrackerChoice == 2:  # Remove Session
            if not len(Subjects):
                print("You don't have any current subjects. "
                      "Please add at least one subject before accessing the Remove Session operation\n\n")
                continue
            removeSessionFunction(template)
        else:
            print("\n\n")
            break


def printTemplateList():
    print("Templates are available for the following days: ")
    for i in range(len(TEMPLATE_DAYS)):
        print("{}. {}".format(i+1, TEMPLATE_DAYS[i]))


def getTemplateDay():
    printTemplateList()
    dayChoice = int(input("Please enter a day choice (1-7): "))
    while not (type(dayChoice) == int and 1 <= dayChoice <= 7):
        dayChoice = int(input("Please enter a valid day choice (1-7): "))
    return TEMPLATE_DAYS[dayChoice-1]


def templates_function():
    equalsToString = '=' * 13
    while True:
        print(equalsToString)
        print("TEMPLATES TAB")
        print(equalsToString)
        templateDay = getTemplateDay()
        template = Templates[templateDay]
        print()
        print(templateDay.upper())
        template.printSchedule()
        timeTrackerChoice = getTemplateChoice()
        if timeTrackerChoice == 1:  # Add Session
            addSessionFunction(template)
            template.printSchedule()
        elif timeTrackerChoice == 2:  # Remove Session
            removeSessionFunction(template)
            template.printSchedule()
        else:
            print("\n")
            break


def printTaskBlocks(Tasks):
    if not len(Tasks):
        print("You have no pending tasks!\n\n\n")
        return
    maxNameLength = 12
    maxSubjectLength = 12
    for task in Tasks:
        maxNameLength = max(maxNameLength, len(task.name))
        maxSubjectLength = max(maxSubjectLength, len(task.subject.name))
    equalToString = "=" * (maxNameLength + maxSubjectLength + 27)
    underscoreString = "-" * (maxNameLength + maxSubjectLength + 27)
    print(equalToString)
    print("S.No | {:<{}}  | {:<{}}  | {:<{}}".format("Task Name", maxNameLength,
                                                     "Subject Name", maxSubjectLength,
                                                     "Deadline", 12))
    print(equalToString)
    for i in range(len(Tasks) - 1):
        task = Tasks[i]
        print("{:<{}} | {:<{}}  | {:<{}}  | {:<{}}".format(i+1, 4,
                                                           task.name, maxNameLength,
                                                           task.subject.name, maxSubjectLength,
                                                           task.deadline, 12))
        print(underscoreString)
    task = Tasks[-1]
    print("{:<{}} | {:<{}}  | {:<{}}  | {:<{}}".format(len(Tasks), 4,
                                                       task.name, maxNameLength,
                                                       task.subject.name, maxSubjectLength,
                                                       task.deadline, 12))
    print(equalToString, end='\n\n\n')


def gather_tasks():
    Tasks = []
    for subject in Subjects:
        for task in subject.pending_tasks:
            Tasks.append(task)
    return Tasks


def getSubject():
    if not len(Subjects):
        print("Please add at least one subject before accessing the Add Task function\n\n")
        return None
    subjectsList = list(Subjects)
    subjectChoice = int(
        input("Please Enter a Subject Choice to add Task to ({} - {}): ".format(1, len(subjectsList))))
    while not (type(subjectChoice) == int and 1 <= subjectChoice <= len(subjectsList)):
        subjectChoice = int(input("Please Enter a Valid Subject Choice ({} - {}): ".format(1, len(subjectsList))))
    subject = subjectsList[subjectChoice - 1]
    return subject


def getTasksFunctionChoice():
    print(TASK_FUNCTION_PRINT_STRING)
    taskFunctionChoice = int(input("Please enter your choice of operation (1-4): "))
    while not (type(taskFunctionChoice) == int and 1 <= taskFunctionChoice <= 4):
        taskFunctionChoice = int(input("Please enter a valid choice of operation (1-4): "))
    return taskFunctionChoice


def getTaskFunction(Tasks):
    if not len(Tasks):
        print("You have no pending Tasks!")
        return None
    taskChoice = int(
        input("Please Enter your choice of Task ({} - {}): ".format(1, len(Tasks))))
    while not (type(taskChoice) == int and 1 <= taskChoice <= len(Tasks)):
        taskChoice = int(input("Please Enter a Valid Task Choice ({} - {}): ".format(1, len(Tasks))))
    task = Tasks[taskChoice - 1]
    return task


def moveTaskToSubmissionFromTaskbarFunction(Tasks):
    task = getTaskFunction(Tasks)
    if task is None:
        return
    task.moveToSubmissions()


def deleteTaskFromTaskbarFunction(Tasks):
    task = getTaskFunction(Tasks)
    if task is None:
        return
    task.delete()


def addTaskFromTaskbarFunction():
    subject = getSubject()
    if subject is None:
        return
    addTaskFunction(subject)


def tasks_function():
    equalToString = "=" * 9
    while True:
        print(equalToString)
        print("TASKS TAB")
        print(equalToString)
        Tasks = gather_tasks()
        printTaskBlocks(Tasks)
        operationChoice = getTasksFunctionChoice()
        if operationChoice == 1:  # add task
            addTaskFromTaskbarFunction()
        elif operationChoice == 2:  # move task to submission
            moveTaskToSubmissionFromTaskbarFunction(Tasks)
        elif operationChoice == 3:  # delete task
            deleteTaskFromTaskbarFunction(Tasks)
        else:
            print('\n')
            break


def printSubmissionBlocks(Submissions):
    if not len(Submissions):
        print("You have made not submissions yet")
        return None
    maxNameLength = 12
    maxSubjectLength = 12
    for submission in Submissions:
        maxNameLength = max(maxNameLength, len(submission.name))
        maxSubjectLength = max(maxSubjectLength, len(submission.subject.name))
    equalToString = "=" * (maxNameLength + maxSubjectLength + 27)
    underscoreString = "-" * (maxNameLength + maxSubjectLength + 27)
    print(equalToString)
    print("S.No | {:<{}}  | {:<{}}  | {:<{}}".format("Task Name", maxNameLength,
                                                     "Subject Name", maxSubjectLength,
                                                     "Submitted On", 12))
    print(equalToString)
    for i in range(len(Submissions) - 1):
        submission = Submissions[i]
        print("{:<{}} | {:<{}}  | {:<{}}  | {:<{}}".format(i+1, 4,
                                                           submission.name, maxNameLength,
                                                           submission.subject.name, maxSubjectLength,
                                                           submission.submitted_on, 12))
        print(underscoreString)
    submission = Submissions[-1]
    print("{:<{}} | {:<{}}  | {:<{}}  | {:<{}}".format(len(Submissions), 4,
                                                       submission.name, maxNameLength,
                                                       submission.subject.name, maxSubjectLength,
                                                       submission.submitted_on, 12))
    print(equalToString, end='\n\n')


def gather_submissions():
    Submissions = []
    for subject in Subjects:
        for submission in subject.submissions:
            Submissions.append(submission)
    return Submissions


def submissions_function():
    equalToString = "=" * 15
    print(equalToString)
    print("SUBMISSIONS TAB")
    print(equalToString)
    Submissions = gather_submissions()
    printSubmissionBlocks(Submissions)
    print("\n\n")


def defaultTimeValue():
    return [0, 0]


def getDuration(time1, time2):
    value = (time2[0] - time1[0]) * 60 + time2[1] - time1[1]
    return [value // 60, value % 60]


def addTime(time1, time2):
    time1[0] += time2[0]
    time1[1] += time2[1]
    if time1[1] > 60:
        time1[1] %= 60
        time1[0] += 1
    return time1


def getReport(report, subjectReport):
    for day in TEMPLATE_DAYS:
        template = Templates[day]
        for session in template.sessions:
            if type(session).__name__ == "StudySession":
                topic = session.topic
                subject = topic.subject
                subjectWiseReport = report[subject]
                topicWiseReport = subjectWiseReport[topic]
                duration = getDuration(session.start_time, session.end_time)
                topicWiseReport[0] += duration[0]
                topicWiseReport[1] += duration[1]
                if topicWiseReport[1] > 60:
                    topicWiseReport[1] %= 60
                    topicWiseReport[0] += 1
                subjectReport[subject][0] += duration[0]
                subjectReport[subject][1] += duration[1]
                if subjectReport[subject][1] > 60:
                    subjectReport[subject][1] %= 60
                    subjectReport[subject][0] += 1
            else:
                subject = session.subject
                subjectWiseReport = report[subject]['Tasks']
                duration = getDuration(session.start_time, session.end_time)
                subjectWiseReport[0] += duration[0]
                subjectWiseReport[1] += duration[1]
                if subjectWiseReport[1] > 60:
                    subjectWiseReport[1] %= 60
                    subjectWiseReport[0] += 1
                subjectReport[subject][0] += duration[0]
                subjectReport[subject][1] += duration[1]
                if subjectReport[subject][1] > 60:
                    subjectReport[subject][1] %= 60
                    subjectReport[subject][0] += 1


def getTimePrint(time):
    return "{} Hrs {} Mins".format(time[0], time[1])


def printReportTopics(sessionReport):
    Topics = list(sessionReport.keys())
    if not len(Topics):
        print("Time Spent on Study Sessions = 0 Hrs 0 Minutes\n\n")
        return
    maxNameLength = 12
    for topic in Topics:
        if topic == "Tasks":
            continue
        maxNameLength = max(maxNameLength, len(topic.name))
    equalToString = "=" * (maxNameLength + 25)
    underscoreString = "-" * (maxNameLength + 25)
    print(equalToString)
    print("S.No | {:<{}} | {:<{}}".format("Topic Name", maxNameLength,
                                          "Time Spent", 15))
    print(equalToString)
    for i in range(len(Topics) - 1):
        topic = Topics[i]
        if topic == "Tasks":
            continue
        duration = sessionReport[topic]
        print("{:<{}} | {:<{}} | {:<{}}".format(i + 1, 4,
                                                topic.name, maxNameLength,
                                                getTimePrint(duration), 15))
        print(underscoreString)
    topic = Topics[-1]
    if topic != "Tasks":
        duration = sessionReport[topic]
        print("{:<{}} | {:<{}} | {:<{}}".format(len(Topics), 4,
                                                topic.name, maxNameLength,
                                                getTimePrint(duration), 15))
    print(equalToString, end='\n\n')


def printReport(report, subjectReport):
    for subject in report:
        print("Total Time spent on subject {} = {}".format(subject.name, getTimePrint(subjectReport[subject])))
        sessionReport = report[subject]
        print("Total Time spent on doing Task = {}".format(getTimePrint(sessionReport["Tasks"])))
        printReportTopics(sessionReport)


def reports_function():
    equalToString = '=' * 11
    print(equalToString)
    print("REPORTS TAB")
    print(equalToString)
    report = defaultdict(lambda: defaultdict(defaultTimeValue))
    subjectReport = defaultdict(defaultTimeValue)
    getReport(report, subjectReport)
    printReport(report, subjectReport)
    print("\n\n")
