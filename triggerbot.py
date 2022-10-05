import keyboard
import pymem
import pymem.process
import time
from Cheat import Cheat
#from win32gui import GetWindowText, GetForegroundWindow
from threading import Thread
from pywinauto import mouse
import win32api
import mouse

class TriggerBot(Cheat):

    def main(self):
        Width = win32api.GetSystemMetrics(0)
        Height = win32api.GetSystemMetrics(1)

        dwEntityList = (int(hex(self.offsets['signatures']['dwEntityList']),16))
        dwForceAttack = (int(hex(self.offsets['signatures']['dwForceAttack']),16))
        dwLocalPlayer = (int(hex(self.offsets['signatures']['dwLocalPlayer']),16))
        m_fFlags = (int(hex(self.offsets['netvars']['m_fFlags']),16))
        m_iCrosshairId = (int(hex(self.offsets['netvars']['m_iCrosshairId']),16))
        m_iTeamNum = (int(hex(self.offsets['netvars']['m_iTeamNum']),16))

        trigger_key = "shift"

        print("Sapphire has launched.")
        pm = pymem.Pymem("csgo.exe")
        client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
        self.running=True
        while True:
            if self.running==False:
                break

            if not keyboard.is_pressed(trigger_key):
                time.sleep(0.1)
            #if not GetWindowText(GetForegroundWindow()) == "Counter-Strike: Global Offensive - ":
                #print('нет окна КС')
                #time.sleep(1)
                #continue


            if keyboard.is_pressed(trigger_key):
                player = pm.read_int(client + dwLocalPlayer)
                entity_id = pm.read_int(player + m_iCrosshairId)
                entity = pm.read_int(client + dwEntityList + (entity_id - 1) * 0x10)

                try:
                    entity_team = pm.read_int(entity + m_iTeamNum)
                    player_team = pm.read_int(player + m_iTeamNum)
                except:
                    print("ошибка")
                    entity_team = 3
                    player_team = 3

                if entity_id > 0 and entity_id <= 64 and player_team != entity_team:
                    mouse.click(button='left')
                time.sleep(0.010)

    def start(self):
        if self.running==False:
            thread = Thread(target=self.main)
            thread.start()
            print(f"{self.get_name()} запущен")

    def get_name(self):
        return "triggerbot"