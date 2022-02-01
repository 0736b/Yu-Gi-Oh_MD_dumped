# **** REQUIREMENT ****

from pymem import *
from pymem.process import *
from os import system, name
from time import sleep
from pyinjector import inject

  
def clear():
    if name == 'nt':
        _ = system('cls')
        print("Yu-Gi-Oh Master Duel | Instant Win")
    else:
        _ = system('clear')
        print("Yu-Gi-Oh Master Duel | Instant Win")


clear()


while True:
    try:
        mem = Pymem("masterduel.exe")
        print("Process ID: ", mem.process_id, " Game found!")
        sleep(1)
        break
    except:
        print("Please run Yu-Gi-Oh Master duel, waiting for game...")
        sleep(1)
        clear()


def getPtrAddr(address, offsets):
    addr = mem.read_longlong(address)
    for offset in offsets:
        if offset != offsets[-1]:
            addr = mem.read_longlong(addr + offset)
    addr = addr + offsets[-1]
    return addr


isSpdHackLoaded = False


def loadSpdHack():
    global isSpdHackLoaded
    key = input("Want to use Speedhack? type Y for YES, N for NO: ")
    while key != 'Y' or key != 'N':
        if key == 'N':
            print("Not loading Speedhack")
            sleep(1)
            clear()
            print("Wait for duel start...")
            loadInstantWin()

        if not isSpdHackLoaded:
            if key == 'Y':
                clear()
                # Thanks to https://github.com/Aragon12UC/IL2CPPUniversalSpeed
                inject(mem.process_id, "Speedhack.dll")
                print("Speedhack injected.")
                isSpdHackLoaded = True
                sleep(1)
                clear()
                print("Wait for duel start...")
                loadInstantWin()


def loadInstantWin():
    while True:
        try:
            # BASE_ADDR = (0x7FFF41B60000)            # duel.dll base addr
            BASE_ADDR = pymem.process.module_from_name(mem.process_handle, "duel.dll").lpBaseOfDll
            BASE_PTR = BASE_ADDR + (0x00A11CD0)
            OFFSETS = [0xDAC] 
            enemyCard = mem.read_longlong(getPtrAddr(BASE_PTR, OFFSETS))
            if enemyCard > 0:
                print("Enemy's card count: ", enemyCard)
                sleep(0.5)
                mem.write_longlong(getPtrAddr(BASE_PTR, OFFSETS), 0)
                enemyCard = mem.read_longlong(getPtrAddr(BASE_PTR, OFFSETS))
                print("Enemy's card count: ", enemyCard)
                sleep(1)
        except:
            if isSpdHackLoaded:
                print("Press F1 for Toggle Speedhack")
            print("Wait for duel start...")
            sleep(1)
            clear()


loadSpdHack()


