# This Python file uses the following encoding: utf-8
#make atlas and build asse

import sys
import os
import shutil
import re

g_absWorkPath = "";

def coyp_file(from_path, to_path):
    if os.path.isfile(from_path):
        if os.path.isfile(to_path):
            os.remove(to_path)
        else:
            print to_path + " is not exists"
        cmd = "cp -f " + from_path + " " + to_path
        print "\nCopy from:"
        print "    " + from_path
        print "to:"
        print "    " + to_path
        os.system(cmd)
    else:
        print from_path + "is not exists"

def coyp_dir(from_path, to_path):
    if os.path.exists(from_path):
        if os.path.exists(to_path):
            cmd = "cp -R " + from_path + " " + to_path
            print "\nCopyDir from:"
            print "    " + from_path
            print "to:"
            print "    " + to_path
            os.system(cmd)
        else:
            print to_path + "is not exists"
    else:
        print from_path + "is not exists"

def get_copy_data(node,parent_name,from_dir_path,to_dir_path):
    childNodes = node.childNodes
    for childNode in childNodes:
        if(childNode.nodeName != "#text" and childNode.nodeName != "#comment"):
            nodeName = childNode.nodeName
            from_path = ""
            to_path = ""
            if(parent_name == ""):
                f_dir_path = childNode.attributes["fromDirPath"].value
                if(f_dir_path == ""):
                    f_dir_path = g_absWorkPath
                    print "f_dir_path = " + f_dir_path

                t_dir_path = childNode.attributes["toDirPath"].value
                if(t_dir_path == ""):
                    t_dir_path = g_absWorkPath + "/" + g_projectName + "/" + g_projectName
                    print "t_dir_path = " + t_dir_path

                get_copy_data(childNode,nodeName,f_dir_path,t_dir_path)
            elif(parent_name == "copydir"):
                from_path = from_dir_path + childNode.attributes["fromDir"].value
                to_path = to_dir_path + childNode.attributes["toDir"].value
                print "copydir  from " + from_path + " to " + to_path
                coyp_dir(from_path,to_path)
            elif(parent_name == "copyfiles"):
                file_name = childNode.attributes["name"].value
                from_path = from_dir_path + childNode.attributes["fromDir"].value + "/" + file_name
                to_path = to_dir_path + childNode.attributes["toDir"].value
                print "copyfiles  from " + from_path + " to " + to_path
                coyp_file(from_path,to_path)

def delete_file(fileNameToDelete):
    _toDeleteFileAbsName = os.path.abspath(fileNameToDelete)
    if os.path.isfile(_toDeleteFileAbsName):
        os.remove(_toDeleteFileAbsName)
    elif os.path.isdir(_toDeleteFileAbsName):
        shutil.rmtree(_toDeleteFileAbsName)

def make_dir(dirNameToMake):
    _dirAbsNameToMake = os.path.abspath(dirNameToMake)
    if os.path.exists(_dirAbsNameToMake) == False:
        os.mkdir(_dirAbsNameToMake)

#------------------------unity operation------------------------------#

def get_work_path():
    global g_absWorkPath
    if(0 == len(g_absWorkPath)):
        g_absWorkPath = os.path.abspath(os.getcwd() + "/..")
    return g_absWorkPath


class UnityOperation():
    @classmethod
    def get_unity_path(cls, platform):
        unityPath = os.getenv("UNITY_PATH")
        if unityPath is None:
            if platform == g_platform_windows:
                unityPath = XmlParser.get_info_by_name("unityWinPath") #"\"C:/Program Files/Unity/Editor/Unity.exe\""
            else:
                unityPath = XmlParser.get_info_by_name("unityMacPath") #"/Applications/Unity/Unity.app/Contents/MacOS/Unity"
        return unityPath

    @classmethod
    def del_unity_log(cls):
        delete_file(get_work_path() + "/" + g_unityLogName);

    @classmethod
    def parse_unity_log(cls):
        _unityLogFileName = get_work_path() + "/" + g_unityLogName
        ret = True
        try:
                f = open(_unityLogFileName, 'r' )
                while True :
                        line = f.readline()
                        if len(line) == 0 :
                            break;
                        index1 = line.find("cmd error")
                        index2 = line.find("Scripts have compiler errors")
                        index3 = line.find("executeMethod method")
                        index4 = line.find("threw exception")
                        if ( index1 >= 0 or index2 >= 0 or (index3>=0 and index4>=0) ) :
                            ret = False
                            break
                f.close()
        except IOError:
                ret = False
        return ret;


    @classmethod
    def changeClassContent(cls, classPath, findStrs, replaceStrs):
        if not os.path.exists(classPath):
            print classPath + " is not exists."
            return
        print classPath + " is exists"
        #if len(findStrs) != len(replaceStrs):
        #    print g_logFormat % ("changeClassContent", "findStrs len is not equal replaceStrs")
        #    return
        l = []
        try:
            f = open(classPath, 'r')
            lines = f.readlines()
            for s in lines:
                for findStr in findStrs:
                    i = 0
                    if(-1 != s.find(findStr)):
                        s = replaceStrs[i]
                        print 'replace ' + findStr + ' to ' + replaceStrs[i]
                        break
                    i+=1
                l.append(s)
            f.close()
        except IOError:
            print g_logFormat % ("changeClassContent", "get replace data failed")
        try:
            f = open( classPath, 'w' )
            for line in l:
                f.write(line)
            f.close()
        except IOError:
            print g_logFormat % ("changeClassContent", "write new data failed")
        print classPath + " file is modified"

if __name__ == "__main__" :
    print "\nwarnning!"

