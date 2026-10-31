---
id: cisco-c9300x-stackwise-portchannel-vlan
title: Cisco Catalyst 9300X IOS-XE — StackWise ไม่ขึ้น, Port-channel ไม่ขึ้น, trunk / VLAN
families: cisco_ios
triggers: cisco, ios-xe, 9300x, stackwise, stackwise-1t, show switch, show etherchannel, show port-channel, switch trunk, switchport mode trunk, switchport access vlan
vendor: Cisco
versions: IOS-XE 17.5.x – 17.15.x (Catalyst 9300/9300X)
sources: https://www.cisco.com/c/en/us/support/docs/switches/catalyst-9300-series-switches/217684-verify-and-troubleshoot-stackwise-on-cat.html
---
# Cisco Catalyst 9300X IOS-XE — StackWise ไม่ขึ้น, Port-channel ไม่ขึ้น, trunk / VLAN

## StackWise ไม่ขึ้น | ตรวจว่า Stack ring ยังเชื่อมต่อกันหรือไม่
คำค้น: show switch, stackwise, show switch stack-ports, show switch detail, show inventory stack, show switch summary, switch not coming up, stack ring not up, stackwise-1t, switch reload, active switch, standby switch, switch priority, stack member
อาการ: StackWise ไม่ขึ้น — ต้องการตรวจว่า switch ring ยังเชื่อมต่อกันหรือไม่, ต้องการดู stack summary, ต้องการดู stack member status, ต้องการดู active/standby switch, ต้องการดู stack ring speed
คำสั่งตรวจ:
```
show switch
show switch stack-ports
```
อ่านผล:
- `show switch`: ดู switch stack ทั้งหมด — Stack ID, Model, Serial Number, Priority, Status (Ready/In RM/In ASM/Non-Ready/Invalid)
- `show switch stack-ports`: ดู stack port status — StackPort1/1, StackPort1/2, link status (UP/DOWN)
- ตัวอย่าง output:
```
Switch/Stack Mac Address : <mac-address>
H/W Current
RJ-Mac Address     Priority Version  State
-------------------------------------------------
*1 C9300X-XXXXXXXX  15     Running    Ready
 2 C9300X-XXXXXXXX  15     Running    Ready
```
สาเหตุที่พบบ่อย:
1. StackWise cable ไม่เชื่อมต่อ — ตรวจ physical connection
2. Stack adapter ผิด — ต้องใช้ C9300-STACK หรือ STACK-T4-50CM
3. Active switch ไม่ elected — ตรวจ switch priority
4. Firmware ไม่ตรงกัน — switch จะไม่ join stack
วิธีแก้:
- ตรวจ StackWise cable: `show switch stack-ports` → ดู link status (เอกสาร: 217684, Cisco)
- แก้ switch priority: `configure terminal` → `switch <id> priority <1-15>` → `end` (เอกสาร: Managing Switch Stacks, IOS-XE 17.15)
- บันทึก config: `copy running-config startup-config` (เอกสาร: Managing Switch Stacks, IOS-XE 17.15)
ที่มา: Cisco Catalyst 9300 StackWise troubleshooting (217684) https://www.cisco.com/c/en/us/support/docs/switches/catalyst-9300-series-switches/217684-verify-and-troubleshoot-stackwise-on-cat.html

## Port-channel ไม่ขึ้น | ตรวจว่า EtherChannel ขึ้นหรือไม่
คำค้น: show etherchannel summary, show port-channel, show lacp neighbor, etherchannel not up, port-channel not up, port-channel mode, lacp active, lacp passive, pagp desirable, pagp auto, channel-group
อาการ: Port-channel ไม่ขึ้น — ต้องการตรวจว่า EtherChannel ขึ้นหรือไม่, ต้องการดู port-channel status, ต้องการดู LACP neighbor, ต้องการดู channel-group mode
คำสั่งตรวจ:
```
show etherchannel summary
show port-channel <id>
```
อ่านผล:
- `show etherchannel summary`: ดู EtherChannel ทั้งหมด — Group, Port-Channel, Protocol (P=PAgP, L=LACP), Ports (G=good, P=bundled)
- `show port-channel <id>`: ดู port-channel detail — member ports, load balancing, mode
- ตัวอย่าง output:
```
Group  Port-channel  Protocol    Ports
------+-------------+-----------+-----------------------------------------------
1      Po1(SU)        LACP       Fa1/0/1(P)   Fa1/0/2(P)
```
สาเหตุที่พบบ่อย:
1. LACP mode ไม่ตรง — side 1 เป็น active, side 2 เป็น passive → ต้องใช้ active-active หรือ active-passive
2. Speed/duplex ไม่ตรง — ต้องตรงกันทุก port
3. VLAN ไม่ตรง — ต้องเป็น VLAN เดียวกันหรือ trunk
วิธีแก้:
- สร้าง EtherChannel: `configure terminal` → `interface range gigabitethernet 1/0/1 - 2` → `channel-group 1 mode active` → `end` (เอกสาร: Configuring EtherChannels, IOS-XE 17.15)
- ตรวจ LACP: `show etherchannel summary` → ดู Po status (SU=up, S=down, D=down, m=missing) (เอกสาร: Configuring EtherChannels, IOS-XE 17.15)
- บันทึก config: `copy running-config startup-config` (เอกสาร: Configuring EtherChannels, IOS-XE 17.15)
ที่มา: Cisco IOS-XE 17.15 Configuring EtherChannels https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-15/configuration_guide/lyr2/b_1715_lyr2_9300_cg/configuring_etherchannels.html

## trunk / VLAN | ตรวจว่า VLAN config ถูกต้องหรือไม่
คำค้น: show vlan, show vlan brief, show interface switchport, show interfaces trunk, switchport mode trunk, switchport access vlan, switchport trunk allowed vlan, vlan not working, trunk not working
อาการ: VLAN ไม่ผ่าน — ต้องการตรวจว่า VLAN config ถูกต้องหรือไม่, ต้องการดู VLAN information, ต้องการดู trunk port config, ต้องการดู switchport config
คำสั่งตรวจ:
```
show vlan brief
show interfaces trunk
show interface <interface-id> switchport
```
อ่านผล:
- `show vlan brief`: ดู VLAN ทั้งหมด — VLAN ID, Name, Ports
- `show interfaces trunk`: ดู trunk port — Port, Name, Status, Native VLAN, Allowed VLANs
- `show interface <interface-id> switchport`: ดู switchport detail — Mode, Access VLAN, Trunking VLANs, Admin/Operational
- ตัวอย่าง output:
```
VLAN Name                             Status    Ports
---- -------------------------------- --------- -------------------------------
1    default                          active
10    VLAN10                           active
100   VLAN100                          active
```
สาเหตุที่พบบ่อย:
1. Trunk port ยังไม่ได้ permit VLAN — ต้องใช้ command `switchport trunk allowed vlan add`
2. Access port ยังไม่ได้ assign VLAN — ต้องใช้ command `switchport access vlan`
3. VLAN ยังไม่ได้สร้าง — ต้องใช้ command `vlan <id>`
วิธีแก้:
- สร้าง VLAN: `configure terminal` → `vlan <id>` → `name <name>` → `end` (เอกสาร: Configuring VLANs, IOS-XE 17.15)
- เพิ่ม VLAN ไป trunk port: `configure terminal` → `interface <interface-id>` → `switchport mode trunk` → `switchport trunk allowed vlan add <id>` → `end` (เอกสาร: Configuring VLAN Trunks, IOS-XE 17.15)
- assign VLAN ไป access port: `configure terminal` → `interface <interface-id>` → `switchport mode access` → `switchport access vlan <id>` → `end` (เอกสาร: Configuring VLANs, IOS-XE 17.15)
- บันทึก config: `copy running-config startup-config` (เอกสาร: Configuring VLANs, IOS-XE 17.15)
ที่มา: Cisco IOS-XE 17.15 Configuring VLANs https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-15/configuration_guide/vlan/b_1715_vlan_9300_cg/configuring_vlans.html
