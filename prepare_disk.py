#! /usr/bin/python

import os
import subprocess
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--disk", required=True)
args = parser.parse_args()

boot_mnt_path = "/mnt/boot_part"
root_mnt_path = "/mnt/root_part"

config_txt_path = f"{boot_mnt_path}/config.txt"
config_txt_content = """
program_usb_boot_mode=1
max_usb_current = 1
"""
cmdline_txt_path = f"{boot_mnt_path}/cmdline.txt"
cmdline_txt_content = " cgroup_memory=1 cgroup_enable=memory usb-storage.quirks=152d:0576:u"

def create_folder(path):
    if not os.path.exists(path):
        print("Creating", path)
        os.makedirs(path)

def mount_partition(part, target):
    if not os.path.exists(part) or not os.path.exists(target):
        raise Exception("The provided partition does not exist!")

    print(f"Mounting {part} to {target}")
    subprocess.call(["mount", part, target])

def unmount_partition(part):
    if not os.path.exists(part):        
        raise Exception("The provided partition does not exist!")

    print(f"Unmounting {part}")
    subprocess.call(["umount", part])

def update_file(path, content, mode="a"):
    with open(path, mode) as file:
        file.write(content)
        file.close()

def main():
    print("Checking required folder structure")
    for path in (boot_mnt_path, root_mnt_path):
        create_folder(path)

    print("Mount partitions")
    for mount in ((1, boot_mnt_path),(2, root_mnt_path)):
        mount_partition("{0}{1}".format(args.disk, mount[0]), mount[1])

    print("Adding content to /boot/config.txt")
    update_file(config_txt_path, content=config_txt_content, mode="a")

    print("Overwriting cmdline")
    update_file(cmdline_txt_path, content=cmdline_txt_content)

    print("Unmount partitions")
    for mount in (1,2):
        unmount_partition("{0}{1}".format(args.disk, mount))
        
main()