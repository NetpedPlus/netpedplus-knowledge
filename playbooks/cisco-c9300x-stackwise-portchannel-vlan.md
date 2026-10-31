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
- `show switch`: ดู switch stack ทั้งหมด — Stack ID, Model, Serial Number, Priority, State — ทุกตัวต้องเป็น Ready (ถ้าเป็น V-Mismatch = IOS-XE ไม่ตรงกัน, Provisioned = ยังไม่ join จริง)
- `show switch stack-ports`: ดู stack port status — StackPort1/1, StackPort1/2, link status (UP/DOWN)
สาเหตุที่พบบ่อย:
1. StackWise cable ไม่เชื่อมต่อ — ตรวจ physical connection
2. สาย stack / stack adapter หลวมหรือเสีย (ดู stack port ที่ DOWN)
3. Active switch ไม่ elected — ตรวจ switch priority
4. Firmware ไม่ตรงกัน — switch จะไม่ join stack
วิธีแก้:
- ตรวจ StackWise cable: `show switch stack-ports` → ดู link status (เอกสาร: 217684, Cisco)
- แก้ switch priority (privileged EXEC ไม่ต้องเข้า configure): `switch <stack-member-number> priority <new-value>` (ตัวที่ priority สูงกว่าเป็น active เมื่อ reload ทั้ง stack) (เอกสาร: Managing Switch Stacks, IOS-XE 17.15)
- บันทึก config: `copy running-config startup-config` (เอกสาร: Managing Switch Stacks, IOS-XE 17.15)
ที่มา: Cisco Catalyst 9300 StackWise troubleshooting (217684) https://www.cisco.com/c/en/us/support/docs/switches/catalyst-9300-series-switches/217684-verify-and-troubleshoot-stackwise-on-cat.html

## Port-channel ไม่ขึ้น | ตรวจว่า EtherChannel ขึ้นหรือไม่
คำค้น: show etherchannel summary, show port-channel, show lacp neighbor, etherchannel not up, port-channel not up, port-channel mode, lacp active, lacp passive, pagp desirable, pagp auto, channel-group
อาการ: Port-channel ไม่ขึ้น — ต้องการตรวจว่า EtherChannel ขึ้นหรือไม่, ต้องการดู port-channel status, ต้องการดู LACP neighbor, ต้องการดู channel-group mode
คำสั่งตรวจ:
```
show etherchannel summary
show etherchannel <id> detail
show lacp neighbor
```
อ่านผล:
- `show etherchannel summary`: ดู EtherChannel ทั้งหมด — Group, Port-Channel, Protocol (P=PAgP, L=LACP), Ports — flag P = bundled, I = stand-alone (ไม่ได้ LACP จากอีกฝั่ง), s = suspended, D = down; Po ต้องเป็น SU (L2) หรือ RU (L3)
- `show etherchannel <id> detail`: สถานะ member แต่ละพอร์ต + เหตุที่ไม่ bundle
- `show lacp neighbor`: อีกฝั่งส่ง LACP มาไหม (ไม่มี neighbor = อีกฝั่งไม่ใช่ LACP / สายผิดพอร์ต)
สาเหตุที่พบบ่อย:
1. ฝั่งหนึ่ง LACP (active / passive) อีกฝั่ง static (mode on) หรือ passive ทั้งสองฝั่ง → ต้องมี active อย่างน้อยหนึ่งฝั่ง และเป็น LACP ทั้งคู่
2. Speed/duplex ไม่ตรง — ต้องตรงกันทุก port
3. VLAN ไม่ตรง — ต้องเป็น VLAN เดียวกันหรือ trunk
วิธีแก้:
- สร้าง EtherChannel: `configure terminal` → `interface range gigabitethernet 1/0/1 - 2` → `channel-group 1 mode active` → `end` (เอกสาร: Configuring EtherChannels, IOS-XE 17.15)
- ตรวจ LACP: `show etherchannel summary` → Po ต้องเป็น SU / RU และ member เป็น P (เอกสาร: Configuring EtherChannels, IOS-XE 17.15)
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
