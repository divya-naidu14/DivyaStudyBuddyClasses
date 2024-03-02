from collections import deque
from datetime import date


def getTimeString(time):
    return "{}:{}".format(str(time[0]).zfill(2), str(time[1]).zfill(2))


def printSubjectTopics(Topics):
    if not len(Topics):
        print("There are no current topics added")
        return
    maxNameLength = 12
    for topic in Topics:
        maxNameLength = max(maxNameLength, len(topic.name))
    equalToString = "=" * (maxNameLength + 7)
    underscoreString = "-" * (maxNameLength + 7)
    print(equalToString)
    print("S.No | {:<{}}".format("Topic Name", maxNameLength))
    print(equalToString)
    for i in range(len(Topics) - 1):
        topic = Topics[i]
        print("{:<{}} | {:<{}}".format(i + 1, 4,
                                       topic.name, maxNameLength))
        print(underscoreString)
    topic = Topics[-1]
    print("{:<{}} | {:<{}}".format(len(Topics), 4,
                                   topic.name, maxNameLength))
    print(equalToString, end='\n\n')


def printSubjectTasks(Tasks):
    if not len(Tasks):
        print("You have no pending tasks!")
        return
    maxNameLength = 12
    maxSubjectLength = 12
    for task in Tasks:
        maxNameLength = max(maxNameLength, len(task.name))
        maxSubjectLength = max(maxSubjectLength, len(task.subject.name))
    equalToString = "=" * (maxNameLength + 23)
    underscoreString = "-" * (maxNameLength + 23)
    print(equalToString)
    print("S.No | {:<{}}  | {:<{}}".format("Task Name", maxNameLength,
                                           "Deadline", 12))
    print(equalToString)
    for i in range(len(Tasks) - 1):
        task = Tasks[i]
        print("{:<{}} | {:<{}}  | {:<{}}".format(i + 1, 4,
                                                 task.name, maxNameLength,
                                                 task.deadline, 12))
        print(underscoreString)
    task = Tasks[-1]
    print("{:<{}} | {:<{}}  | {:<{}}".format(len(Tasks), 4,
                                             task.name, maxNameLength,
                                             task.deadline, 12))
    print(equalToString, end='\n\n')


# Subject
class Subject:
    def __init__(self, name):
        self.name = name
        self.topics = set()
        self.pending_tasks = set()
        self.submissions = set()

    def add_topic(self, name):
        self.topics.add(Topic(name, self))

    def remove_topic(self, topic):
        self.topics.remove(topic)
        for session in topic.study_sessions:
            session.delete()

    def add_task(self, name, deadline):
        self.pending_tasks.add(Task(name, self, deadline))

    def move_task_to_submissions(self, task):
        self.pending_tasks.remove(task)
        today_date = str(date.today())
        self.submissions.add(Submission(task.name, self, task.deadline, today_date))

    def delete_task(self, task):
        for session in task.task_sessions:
            session.delete()
        self.pending_tasks.remove(task)

    def detach(self):
        for topic in self.topics:
            for session in topic.study_sessions:
                session.delete()
        for task in self.pending_tasks:
            for session in task.task_sessions:
                session.delete()

    def print(self):
        equalToString = "=" * (14 + len(self.name))
        print(equalToString)
        print("SUBJECT NAME: {}".format(self.name))
        print(equalToString)
        print("\nTOPICS")
        equalToString = '=' * 6
        print(equalToString)
        if not len(self.topics):
            print("There are no current topics added in {}".format(self.name))
        else:
            printSubjectTopics(list(self.topics))
        print("\nTASKS PENDING")
        equalToString = '=' * 13
        print(equalToString)
        if not len(self.pending_tasks):
            print("There are no pending tasks in {}!".format(self.name))
        else:
            printSubjectTasks(list(self.pending_tasks))
        print('\n')


class Topic:
    def __init__(self, name, subject):
        self.name = name
        self.subject = subject
        self.study_sessions = set()

    def add_session(self, start_time, end_time, template):
        session = StudySession(self, start_time, end_time, template)
        self.study_sessions.add(session)
        return session

    def remove_study_session(self, study_session):
        self.study_sessions.remove(study_session)

    def __str__(self):
        return self.name

    def delete(self):
        self.subject.remove_topic(self)
        for session in self.study_sessions:
            session.delete()


class StudySession:
    def __init__(self, topic, start_time, end_time, template):
        self.name = topic.name
        self.topic = topic
        self.start_time = start_time
        self.end_time = end_time
        self.template = template

    def update(self, start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time

    def delete(self):
        self.topic.remove_study_session(self)
        self.template.removeSession(self)

    def splitPush(self, newEnd, newStart, template):
        self.end_time = newEnd
        return self.topic.add_session(newStart, self.end_time, template)

    def __str__(self):
        return self.name

    def print(self):
        print("Session Name: {}\n"
              "Session Type: Study Session\n"
              "Session StartTime: {}\n"
              "Session End Time: {}\n".format(self.name, getTimeString(self.start_time), getTimeString(self.end_time)))


class Task:
    def __init__(self, name, subject, deadline):
        self.name = name
        self.subject = subject
        self.deadline = deadline
        self.task_sessions = set()

    def add_session(self, start_time, end_time, template):
        session = TaskSession(self, start_time, end_time, template)
        self.task_sessions.add(session)
        return session

    def submitTask(self):
        self.subject.move_task_to_submissions(self)
        for session in self.task_sessions:
            session.delete()

    def deleteTaskSession(self, taskSession):
        self.task_sessions.remove(taskSession)
        for session in self.task_sessions:
            session.delete()

    def moveToSubmissions(self):
        self.subject.move_task_to_submissions(self)
        for session in self.task_sessions:
            session.delete()

    def print(self):
        print("Name: {}\n"
              "Deadline: {}\n".format(self.name, self.deadline))

    def __str__(self):
        return self.name


class TaskSession:
    def __init__(self, task, start_time, end_time, template):
        self.task = task
        self.name = task.name
        self.start_time = start_time
        self.end_time = end_time
        self.template = template

    def update(self, start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time

    def splitPush(self, newEnd, newStart, template):
        self.end_time = newEnd
        return self.task.add_session(newStart, self.end_time, template)

    def delete(self):
        self.task.deleteTaskSession(self)
        self.template.removeSession(self)

    def print(self):
        print("Session Name: {}\n"
              "Session Type: Task Session\n"
              "Session StartTime: {}\n"
              "Session End Time: {}\n".format(self.name, getTimeString(self.start_time), getTimeString(self.end_time)))


class Submission:
    def __init__(self, name, subject, deadline, submitted_on):
        self.name = name
        self.subject = subject
        self.submitted_on = submitted_on


