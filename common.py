import xml.etree.ElementTree as ET
from enum import Enum

class MOT:
    def __init__(self):
        self.PlaySpeed = 0.0
        self.EndTime = 0.0
        self.Joints = []

class MOT_FLAGS:
    TRANSLATE = 0x01
    SCALE = 0x02
    ROTATE = 0x08
    ENABLED = 0x20
    DISABLED = 0x40

class Joint:
    def __init__(self):
        self.Flag1 = 0
        self.Flag2 = 0
        self.TrackFlag = 0x0
        self.BoneID = 0
        self.MaxTime = 0.0
        self.Keys = []

class Key:
    def __init__(self):
        self.Time = 0.0
        self.X = 0.0
        self.Y = 0.0
        self.Z = 0.0
        self.W = 0.0
        self.Joint = None

def loadMotXML(path):
    tree = ET.parse(path)
    root = tree.getroot()

    mot = MOT()
    mot.PlaySpeed = root.attrib['PlaySpeed']
    mot.EndTime = root.attrib['EndTime']

    for joint in root.findall('./Joint'):
        j = Joint()
        j.Flag1 = int(joint.attrib['Flag1'])
        j.Flag2 = int(joint.attrib['Flag2'])
        
        if "TRANSLATE" in joint.attrib['TrackFlag']:
            j.TrackFlag = j.TrackFlag | MOT_FLAGS.TRANSLATE
        if "SCALE" in joint.attrib['TrackFlag']:
            j.TrackFlag = j.TrackFlag | MOT_FLAGS.SCALE
        if "ROTATE" in joint.attrib['TrackFlag']:
            j.TrackFlag = j.TrackFlag | MOT_FLAGS.ROTATE
        if "ENABLED" in joint.attrib['TrackFlag']:
            j.TrackFlag = j.TrackFlag | MOT_FLAGS.ENABLED
        if "DISABLED" in joint.attrib['TrackFlag']:
            j.TrackFlag = j.TrackFlag | MOT_FLAGS.DISABLED

        j.BoneID = int(joint.attrib['BoneID'])
        j.MaxTime = float(joint.attrib['MaxTime'])
        mot.Joints.append(j)

    for key in root.findall('./Key'):
        for joint in key.findall('./Joint'):
            k = Key()
            k.Time = float(key.attrib['Time'])
            k.X = float(joint.attrib['X'])
            k.Y = float(joint.attrib['Y'])
            k.Z = float(joint.attrib['Z'])
            k.W = float(joint.attrib['W'])
            jointIdx = int(joint.attrib['Index'])

            k.Joint = mot.Joints[jointIdx]
            mot.Joints[jointIdx].Keys.append(k)

    return mot