from Subject import *
import random


def clean_sessions(sessions):
    return fillSessions(sort_sessions(list(sessions)))


def getTimeValue(time):
    return time[0]*60 + time[1]


def sort_sessions(sessions):
    sessionList = list(sessions)
    sessionList.sort(key=lambda x: getTimeValue(x.start_time))
    return sessionList


def fillSessions(sessions):
    currentTime = [0, 0]
    filledSessions = []
    for session in sessions:
        if getTimeValue(currentTime) < getTimeValue(session.start_time):
            filledSessions.append(FreeBlock(currentTime, session.start_time))
        filledSessions.append(session)
        currentTime = session.end_time
    if getTimeValue(currentTime) < getTimeValue([23, 59]):
        filledSessions.append(FreeBlock(currentTime, [23, 59]))
    return filledSessions


def printSessionBlocks(sessions):
    maxNameLength = 12
    maxSubjectName = 15
    for session in sessions:
        if type(session).__name__ == 'StudySession':
            subjectName = session.topic.subject.name
        elif type(session).__name__ == 'TaskSession':
            subjectName = session.task.subject.name
        else:
            subjectName = "*" * 12
        maxNameLength = max(maxNameLength, len(session.name))
        maxSubjectName = max(maxSubjectName, len(subjectName))
    equalToString = "=" * (maxNameLength + maxSubjectName + 49)
    underscoreString = "-" * (maxNameLength + maxSubjectName + 49)
    print(equalToString)
    print("{:<{}}  | {:<{}} | {:<{}} | {:<{}} | {:<{}}".format("Session Name", maxNameLength,
                                                               "Session Subject", maxSubjectName,
                                                               "Session Type", 12,
                                                               "Start Time", 12,
                                                               "End Time", 12))
    print(equalToString)
    for i in range(len(sessions)-1):
        session = sessions[i]
        if type(session).__name__ == 'StudySession':
            subjectName = session.topic.subject.name
            sessionType = "Study"
        elif type(session).__name__ == 'TaskSession':
            subjectName = session.task.subject.name
            sessionType = "Task"
        else:
            subjectName = "------------"
            sessionType = "------------"
        print("{:<{}}  | {:<{}} | {:<{}} | {:<{}} | {:<{}}".format(session.name, maxNameLength,
                                                                   subjectName, maxSubjectName,
                                                                   sessionType, 12,
                                                                   getTimeString(session.start_time), 12,
                                                                   getTimeString(session.end_time), 12))
        print(underscoreString)
    session = sessions[-1]
    if type(session).__name__ == 'StudySession':
        subjectName = session.topic.subject.name
        sessionType = "Study"
    elif type(session).__name__ == 'TaskSession':
        subjectName = session.task.subject.name
        sessionType = "Task"
    else:
        subjectName = "------------"
        sessionType = "------------"
    print("{:<{}}  | {:<{}} | {:<{}} | {:<{}} | {:<{}}".format(session.name, maxNameLength,
                                                               subjectName, maxSubjectName,
                                                               sessionType, 12,
                                                               getTimeString(session.start_time), 12,
                                                               getTimeString(session.end_time), 12))
    print(equalToString, end='\n\n')


def getTimeList(timeValue):
    return [timeValue // 60, timeValue % 60]


class FreeBlock:
    def __init__(self, start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time
        self.name = "------------"

    def update(self, start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time


class Template:
    def __init__(self, day):
        self.day = day
        self.sessions = set()

    def addSession(self, newSession):
        newSessionStartTime = getTimeValue(newSession.start_time)
        newSessionEndTime = getTimeValue(newSession.end_time)
        for session in self.sessions:
            sessionStartTime = getTimeValue(session.start_time)
            sessionEndTime = getTimeValue(session.end_time)
            if sessionStartTime >= newSessionEndTime or sessionEndTime <= newSessionStartTime:
                continue
            elif sessionStartTime >= newSessionStartTime and sessionEndTime <= newSessionEndTime:
                session.delete()
            elif sessionStartTime >= newSessionStartTime and sessionEndTime > newSessionEndTime:
                session.update(getTimeList(newSessionEndTime), getTimeList(sessionEndTime))
            elif sessionStartTime < newSessionStartTime and sessionEndTime <= newSessionEndTime:
                session.update(getTimeList(sessionStartTime), getTimeList(newSessionStartTime))
            else:
                splitSession = session.splitPush(getTimeList(newSessionStartTime), getTimeList(newSessionEndTime), self)
                self.sessions.add(splitSession)
        self.sessions.add(newSession)

    def removeSession(self, session):
        self.sessions.remove(session)

    def printSchedule(self):
        printSessionBlocks(clean_sessions(self.sessions))


def getTimeString(time):
    return "{}:{}".format(str(time[0]).zfill(2), str(time[1]).zfill(2))

