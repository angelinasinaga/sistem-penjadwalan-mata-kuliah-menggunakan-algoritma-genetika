class Kelas:
    kelas = None

    def __init__(self, name, size):
        self.name = name
        self.size = size

    @staticmethod
    def find(name):
        for i in range(len(Kelas.kelas)):
            if Kelas.kelas[i].name == name:
                return i
        return -1

    def __repr__(self):
        return "Kelas: " + self.name


class Dosen:
    dosen = None

    def __init__(self, name):
        self.name = name

    @staticmethod
    def find(name):
        for i in range(len(Dosen.dosen)):
            if Dosen.dosen[i].name == name:
                return i
        return -1

    def __repr__(self):
        return "Dosen Pengampu: " + self.name


class CourseClass:
    classes = None

    def __init__(self, code, is_lab=False):
        self.code = code
        self.is_lab = is_lab

    @staticmethod
    def find(code):
        for i in range(len(CourseClass.classes)):
            if CourseClass.classes[i].code == code:
                return i
        return -1

    def __repr__(self):
        return "Kode Matakuliah: " + self.code


class Room:
    rooms = None

    def __init__(self, name, size, is_lab=False):
        self.name = name
        self.size = size
        self.is_lab = is_lab

    @staticmethod
    def find(name):
        for i in range(len(Room.rooms)):
            if Room.rooms[i].name == name:
                return i
        return -1

    def __repr__(self):
        return "Ruangan:  " + self.name


class Schedule:
    schedules = None

    def __init__(self, start, end, day, is_lab_slot=False):
        self.start = start
        self.end = end
        self.day = day
        self.is_lab_slot = is_lab_slot

    def __repr__(self):
        return "Pukul :" + self.start + "-" + self.end + " Day: " + self.day
