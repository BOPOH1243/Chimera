from Cheat import Cheat
import pymem
import pymem.process
import tkinter as tk  # Python 3
from tkinter import *
from tkinter.ttk import Frame, Label
import win32api
import time
from threading import Thread


class ESPBox(Cheat):
    def _start(self):

        self.running = True
        m_dwBoneMatrix = int(hex(self.offsets['netvars']['m_dwBoneMatrix']),16)
        dwLocalPlayer = int(hex(self.offsets['signatures']['dwLocalPlayer']),16)
        dwRadarBase = int(hex(self.offsets['signatures']['dwRadarBase']),16)
        m_iTeamNum = int(hex(self.offsets['netvars']['m_iTeamNum']),16)
        dwEntityList = int(hex(self.offsets['signatures']['dwEntityList']),16)
        dwViewMatrix = int(hex(self.offsets['signatures']['dwViewMatrix']),16)
        m_vecOrigin = int(hex(self.offsets['netvars']['m_vecOrigin']),16)

        pm = pymem.Pymem("csgo.exe")
        Client = pymem.process.module_from_name(pm.process_handle, 'client.dll').lpBaseOfDll

        Width = win32api.GetSystemMetrics(0)
        Height = win32api.GetSystemMetrics(1)

        root = tk.Tk()
        root.overrideredirect(True)
        root.wm_attributes("-topmost", True)
        root.wm_attributes("-toolwindow", True)
        root.wm_attributes("-disabled", True)
        root.wm_attributes("-transparentcolor", "white")
        root.update()

        def W2S(posX, posY, posZ, view):
            clipCoordsX = posX * view[0] + posY * view[1] + posZ * view[2] + view[3]
            clipCoordsY = posX * view[4] + posY * view[5] + posZ * view[6] + view[7]
            clipCoordsZ = posX * view[8] + posY * view[9] + posZ * view[10] + view[11]
            clipCoordsW = posX * view[12] + posY * view[13] + posZ * view[14] + view[15]

            if clipCoordsW < 0.1:
                return False, 0, 0

            NDCx = clipCoordsX / clipCoordsW
            NDCy = clipCoordsY / clipCoordsW
            NDCz = clipCoordsZ / clipCoordsW

            screenX = (Width / 2 * NDCx) + (NDCx + Width / 2)
            screenY = -(Height / 2 * NDCy) + (NDCy + Height / 2)
            return True, screenX, screenY

        def get_distance(PlAddr, EnAddr):

            enemy_posRx = pm.read_float(EnAddr + m_vecOrigin)
            enemy_posRy = pm.read_float(EnAddr + m_vecOrigin + 4)
            enemy_posRz = pm.read_float(EnAddr + m_vecOrigin + 8)

            my_posRx = pm.read_float(PlAddr + m_vecOrigin)
            my_posRy = pm.read_float(PlAddr + m_vecOrigin + 4)
            my_posRz = pm.read_float(PlAddr + m_vecOrigin + 8)

            my_posx = my_posX - enemy_posX
            my_posy = my_posY - enemy_posY
            my_posz = my_posZ - enemy_posZ

            return ((my_posx * my_posx + my_posy * my_posy + my_posz + my_posz) ** 0.5) / 10

        def get_originpos(EnAddr):
            my_posRx = pm.read_float(EnAddr + m_vecOrigin)
            my_posRy = pm.read_float(EnAddr + m_vecOrigin + 4)
            my_posRz = pm.read_float(EnAddr + m_vecOrigin + 8)

            return my_posRx, my_posRy, my_posRz

        def get_bonepos(Entity, n):
            Bonebase = pm.read_int(Entity + m_dwBoneMatrix)

            EnemyBonesx = pm.read_float(Bonebase + 0x30 * n + 0x0C)
            EnemyBonesy = pm.read_float(Bonebase + 0x30 * n + 0x1C)
            EnemyBonesz = pm.read_float(Bonebase + 0x30 * n + 0x2C)
            return EnemyBonesx, EnemyBonesy, EnemyBonesz

        EntityList = {}
        dsfindent = True
        def FindEnt():
            nonlocal EntityList
            while dsfindent:
                LocalPlayer = pm.read_int(Client + dwLocalPlayer)
                LocalTeam = pm.read_int(m_iTeamNum + LocalPlayer)
                TempEntityList = {}
                size = 0x174
                Struck = pm.read_int(Client + dwRadarBase)
                Pointer = pm.read_int(Struck + 0x78)
                for i in range(33):

                    Entity = pm.read_int(Client + dwEntityList + (i * 0x10))
                    PlNameI = i - 2
                    name = pm.read_string((Pointer + 0x5E8) + (PlNameI * size))

                    if (Entity and Entity != LocalPlayer):
                        EntityDormsnt = pm.read_int(Entity + 0xED)
                        if not EntityDormsnt:
                            TempEntityList[Entity] = name

                EntityList = TempEntityList
                #time.sleep(1)

        findent = Thread(target=FindEnt)
        findent.start()
        canvas = tk.Canvas(root, width=Width, height=Height, bg='white')
        canvas.pack()
        while 1:
            if self.running == False:
                dsfindent = False
                break

            TempEntityList = EntityList

            view = []
            for i in range(17):
                view.append(pm.read_float(Client + dwViewMatrix + (i * 4)))

            for Entity in TempEntityList:

                Hp = pm.read_int(Entity + 0x100)
                if not Hp: continue

                my_posRx, my_posRy, my_posRz = get_originpos(Entity)
                state, LegX, LegY = W2S(my_posRx, my_posRy, my_posRz, view)

                my_hedRx, my_hedRy, my_hedRz = get_bonepos(Entity, 8)
                state2, HeadX, HeadY = W2S(my_hedRx, my_hedRy, my_hedRz, view)

                if state and state2:
                    Diff = HeadY - LegY
                    HeadY += Diff // 5
                    Diff = HeadY - LegY
                    # LEFT & RIGHT
                    canvas.create_line(LegX - Diff // 4, HeadY, LegX - Diff // 4, LegY, fill='red')
                    canvas.create_line(LegX + Diff // 4, HeadY, LegX + Diff // 4, LegY, fill='red')
                    # UP & DOWN
                    canvas.create_line(LegX - Diff // 4, HeadY, LegX + Diff // 4, HeadY, fill='red')
                    canvas.create_line(LegX - Diff // 4, LegY, LegX + Diff // 4, LegY, fill='red')
                    # NAME
                    canvas.create_text(HeadX, HeadY - 10,
                                       text=TempEntityList[Entity],
                                       justify=CENTER, font="Arial 14", fill='blue')
            root.update()
            canvas.create_rectangle(0, 0, Width, Height, fill='white')
    def start(self):
        if self.running==False:
            thread = Thread(target=self._start)
            thread.start()

    def get_name(self):
        return 'ESPBox Wallhack'
