#!/usr/bin/env python3
# networkFileRW.py
# Junio
# April 20, 2026
# Read network equipment from files, update IP addresses, write results to files

try:
    import json
except ImportError:
    print("Could not find json module")

# Constants
ROUTER_FILE = 'equip_r.txt'
SWITCH_FILE = 'equip_s.txt'
UPDATED_FILE = 'updated.txt'
INVALID_FILE = 'invalid.txt'

def getInventory():
    routers = {}
    switches = {}
    
    with open(ROUTER_FILE, 'r') as rfile:
        routers = json.load(rfile)
    
    with open(SWITCH_FILE, 'r') as sfile:
        switches = json.load(sfile)
    
    inventory = {**routers, **switches}
    return inventory

def displayInventory(inventory):
    print("\nNetwork Equipment Inventory\n")
    print("    {:<18} {}".format("equipment name", "IP address"))
    for device, ip in inventory.items():
        print("    {:<18} {}".format(device, ip))

def validateIP(ip):
    parts = ip.split('.')
    if len(parts) != 4:
        return False
    for part in parts:
        try:
            num = int(part)
            if num < 0 or num > 255:
                return False
        except ValueError:
            return False
    return True

def updateInventory(inventory):
    updated = {}
    invalidIPs = []
    
    while True:
        device = input("\nWhich device would you like to update (enter x to quit)? ")
        if device == 'x':
            break
        if device not in inventory:
            print("That device is not in the network inventory.")
            continue
        
        while True:
            newIP = input("What is the new IP address (111.111.111.111) ")
            if validateIP(newIP):
                inventory[device] = newIP
                updated[device] = newIP
                print("{} was updated; the new IP address is {}".format(device, newIP))
                break
            else:
                print("Sorry, that is not a valid IP address")
                invalidIPs.append(newIP)
    
    return updated, invalidIPs

def writeSummary(updated, invalidIPs):
    print("\nSummary:\n")
    print("Number of devices updated:", len(updated))
    print("Number of invalid addresses attempted:", len(invalidIPs))
    
    with open(UPDATED_FILE, 'w') as ufile:
        json.dump(updated, ufile)
    
    with open(INVALID_FILE, 'w') as ifile:
        json.dump(invalidIPs, ifile)

def main():
    inventory = getInventory()
    displayInventory(inventory)
    updated, invalidIPs = updateInventory(inventory)
    writeSummary(updated, invalidIPs)

main()