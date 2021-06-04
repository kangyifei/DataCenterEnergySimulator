from SixSigmaDCSDK.engine import Engine
from core.cooling_equipment import CoolingEquipment
import os
import time
import pyautogui
import win32gui


class Room(CoolingEquipment):
    def __init__(self, bashpath):
        if bashpath[-1] == "/":
            bashpath = bashpath[:-1]
        self.inPath = bashpath + "/in.csv"
        self.outPath = bashpath + "/out.csv"
        if os.path.exists(self.inPath):
            os.remove(self.inPath)
        if os.path.exists(self.outPath):
            os.remove(self.outPath)
        self.eng = Engine()
        self.inletTemp = 12
        self.state_paraslist = {}
        self.control_paramslist = {}
        self.state_paraslist["inlet_temp"] = 12
        self.control_paramslist["set_temp"] = 12
        self.power = (self.state_paraslist["inlet_temp"] - self.control_paramslist["set_temp"]) * 26 \
            if (self.state_paraslist["inlet_temp"] - self.control_paramslist["set_temp"]) * 26 > 1e-6 \
            else 0
        print("now start 6SigmaDC")
        while (not self.eng.readCFDOutFile(self.outPath)):
            pass

    def control(self, control_paramslist):
        fanspeed = control_paramslist["Fanspeed"]
        if fanspeed > 100:
            fanspeed = 100
        if fanspeed < 0:
            fanspeed = 0
        self.eng.setSolutionAttr("ACU", "ACU01", "FanSpeed", str(fanspeed), "%")
        i = 1
        for machine in self.cluster.machines:
            cpuUsage = int(machine.state["cpu_usage_percent"] * 100)
            # print("machine"+str(i),cpuUsage)
            self.eng.setSolutionAttr("ITEquipment", "Server" + str(i), "HeatPowerFactor", str(cpuUsage), "%")
            i += 1
        self.eng.setSolutionAttr("<<Control>>", "<<Solution>>", "Time", str(int(self.simulation.env.now)), "s")
        # print(self.simulation.env.now)
        # print("FanSpeed", str(fanspeed))
        self.eng.writeCFDInFile(self.inPath)

    def update_self(self):
        while (not self.eng.readCFDOutFile(self.outPath)):
            pass
        self.state_paraslist["inlet_temp"] = float(
            self.eng.getSolutionAttr("Sensor", "Average Return Air", "Value").value)
        self.control_paramslist["set_temp"] = float(
            self.eng.getSolutionAttr("Controller", "Air Temperature Controller", "SetPoint").value)
        self.power = (self.state_paraslist["inlet_temp"] - self.control_paramslist["set_temp"]) * 26 \
            if (self.state_paraslist["inlet_temp"] - self.control_paramslist["set_temp"]) * 26 > 1e-6 \
            else 0
    def update_cluster(self):
        i = 1
        for machine in self.cluster.machines:
            # print("front" + str(i))
            machine.inlet_temp = float(self.eng.getSolutionAttr("Sensor", "front" + str(i), "Value").value)
            cpuUsage = int(machine.state["cpu_usage_percent"] * 100)
            self.eng.setSolutionAttr("ITEquipment", "Server" + str(i), "HeatPowerFactor", str(cpuUsage), "%")
            i += 1

    def attach(self, simulation):
        self.simulation = simulation
        self.cluster = simulation.cluster
        self.machines = self.cluster.machines

    def stop(self):
        while (win32gui.FindWindow(None, "运行工具失败") == 0):
            pass
        print("need to restart 6SigmaDC Room")
        while True:
            try:
                if os.path.exists(self.inPath):
                    os.remove(self.inPath)
                if os.path.exists(self.outPath):
                    os.remove(self.outPath)
                    break
            except PermissionError:
                pass
        # 关闭运行工具失败床阔
        pyautogui.click(1132, 554, button="left")
        time.sleep(1)
        # 重新开始仿真
        pyautogui.click(1790, 1018, button="left")
        time.sleep(1)
        self.eng = Engine()
        while (not self.eng.readCFDOutFile(self.outPath)):
            pass
