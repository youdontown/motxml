import xml.etree.ElementTree as ET
import xml.dom.minidom as MD

class MOT:
    def __init__(self):
        self.PlaySpeed = 0.0
        self.EndTime = 0.0
        self.Joints = []
        self.Keys = []

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
        self.Unknown = 0
        self.Keys = []

class JointKey:
    def __init__(self):
        self.Time = 0.0
        self.X = 0.0
        self.Y = 0.0
        self.Z = 0.0
        self.W = 0.0
        self.Joint = None

class Key:
    def __init__(self):
        self.Time = 0.0
        self.Joints = []

class KeyJoint:
    def __init__(self):
        self.Index = 0
        self.X = 0.0
        self.Y = 0.0
        self.Z = 0.0
        self.W = 0.0
        self.Key = None

def loadMotXML(path):
    tree = ET.parse(path)
    root = tree.getroot()

    mot = MOT()
    mot.PlaySpeed = float(root.attrib['PlaySpeed'])
    mot.EndTime = float(root.attrib['EndTime'])

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
        j.Unknown = int(joint.attrib['Unknown'])
        mot.Joints.append(j)

    for key in root.findall('./Key'):
        k = Key()
        k.Time = float(key.attrib['Time'])

        for joint in key.findall('./Joint'):
            jk = JointKey()
            jk.Time = float(key.attrib['Time'])
            jk.X = float(joint.attrib['X'])
            jk.Y = float(joint.attrib['Y'])
            jk.Z = float(joint.attrib['Z'])
            jk.W = float(joint.attrib['W'])
            jointIdx = int(joint.attrib['Index'])

            jk.Joint = mot.Joints[jointIdx]
            mot.Joints[jointIdx].Keys.append(jk)

            kj = KeyJoint()
            kj.Index = jointIdx
            kj.X = jk.X
            kj.Y = jk.Y
            kj.Z = jk.Z
            kj.W = jk.W

            k.Joints.append(kj)

        mot.Keys.append(k)

    return mot

def saveMotXML(mot, path):
    xml = ET.Element('MOT')
    xml.set('PlaySpeed', str(mot.PlaySpeed))
    xml.set('EndTime', str(mot.EndTime))

    for joint in mot.Joints:
        j = ET.SubElement(xml, 'Joint')
        j.set('Flag1', str(joint.Flag1))
        j.set('Flag2', str(joint.Flag2))

        flagArr = []
        if joint.TrackFlag & MOT_FLAGS.DISABLED:
            flagArr.append('DISABLED')
        if joint.TrackFlag & MOT_FLAGS.ROTATE:
            flagArr.append('ROTATE')
        if joint.TrackFlag & MOT_FLAGS.SCALE:
            flagArr.append('SCALE')
        if joint.TrackFlag & MOT_FLAGS.TRANSLATE:
            flagArr.append('TRANSLATE')
        if joint.TrackFlag & MOT_FLAGS.ENABLED:
            flagArr.append('ENABLED')

        j.set('TrackFlag', ', '.join(flagArr))
        j.set('BoneID', str(joint.BoneID))
        j.set('MaxTime', str(joint.MaxTime))
        j.set('Unknown', str(joint.Unknown))

    for key in mot.Keys:
        k = ET.SubElement(xml, 'Key')
        k.set('Time', str(key.Time))

        for joint in key.Joints:
            j = ET.SubElement(k, 'Joint')
            j.set('Index', str(joint.Index))
            j.set('X', str(joint.X))
            j.set('Y', str(joint.Y))
            j.set('Z', str(joint.Z))
            j.set('W', str(joint.W))

    xmlStr = ET.tostring(xml, encoding='unicode')
    reparsed = MD.parseString(xmlStr)
    f = open(path, 'wb')
    f.write(reparsed.toprettyxml(indent="\t", encoding='utf-8'))
    f.close()