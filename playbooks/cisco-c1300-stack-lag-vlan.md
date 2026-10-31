---
id: cisco-c1300-stack-lag-vlan
title: Cisco Catalyst 1300 (C1300-24XS) — Stack ไม่ขึ้น, Port-channel ไม่ขึ้น, VLAN ไม่ผ่าน
families: cisco_sb
triggers: catalyst-1300, c1300, cisco-stack, catalyst-1200, cisco-sb
vendor: Cisco
versions: C1300 Firmware 4.10.x
sources: https://www.cisco.com/c/en/us/td/docs/switches/campus-lan-switches-access/Catalyst-1200-and-1300-Switches/cli/C1300-cli/stack-commands.html, https://www.cisco.com/c/en/us/td/docs/switches/campus-lan-switches-access/Catalyst-1200-and-1300-Switches/cli/C1300-cli/lacp-commands.html, https://www.cisco.com/c/en/us/td/docs/switches/campus-lan-switches-access/Catalyst-1200-and-1300-Switches/cli/C1300-cli/port-channel-commands.html, https://www.cisco.com/c/en/us/td/docs/switches/campus-lan-switches-access/Catalyst-1200-and-1300-Switches/cli/C1300-cli/vlan-commands.html
---
# Cisco Catalyst 1300 (C1300-24XS) — Stack ไม่ขึ้น, Port-channel ไม่ขึ้น, VLAN ไม่ผ่าน

## Stack ไม่ขึ้น | ตรวจ stack status, member, links
คำค้น: stack not up, stack member not joining, stack split, show stack, show stack links, show stack configuration, set stack unit-type, stack unit
อาการ: stack ไม่ขึ้น, สมาชิกไม่เข้า stack, ต้องการดู stack status, ต้องการดู stack links
คำสั่งตรวจ:
```
show stack
show stack links
show stack configuration
```
อ่านผล:
- `show stack`: ดู stack topology — member ID, status (Ready/Prep/Down), role (Active/Standby/Backup)
- `show stack links`: ดู stack member links — link status, speed (Gigabit/Ethernet), which ports are connected
- `show stack configuration`: ดู stack config — unit-id, unit-type, network-type, uplink-type
สาเหตุที่พบบ่อย:
1. Stack cable ไม่ต่อหรือต่อผิด port — ต้องต่อ stack cable ระหว่าง member
2. Stack members มี firmware version ไม่ตรงกัน — ต้อง upgrade firmware ให้ตรงกัน
3. Stack priority ไม่ set — ต้อง set unit-type และ priority
วิธีแก้:
1. ตรวจ stack cable: `show stack links` — ดู link status ว่าแต่ละ port connected หรือไม่
2. Set stack member: `stack unit <unit-id> <member-id>` — กำหนด member ID
3. Set stack priority: `set stack unit-type unit <unit-id> network <type> uplink <type>` — กำหนด network/uplink type
4. ตรวจ stack status: `show stack` — ดู member status เป็น Ready หรือยัง
ที่มา: Cisco C1300 CLI Guide — Stack Commands https://www.cisco.com/c/en/us/td/docs/switches/campus-lan-switches-access/Catalyst-1200-and-1300-Switches/cli/C1300-cli/stack-commands.html

## Port-channel ไม่ขึ้น | ตรวจ LACP, channel-group mode, lacp
คำค้น: port-channel not up, channel-group not joining, lacp not forming, show lacp, show lacp port-channel, show interfaces port-channel, channel-group mode
อาการ: port-channel ไม่ขึ้น, ต้องการดู lacp status, ต้องการดู channel-group mode, ต้องการดู lacp port-channel
คำสั่งตรวจ:
```
show lacp
show lacp port-channel
show interfaces port-channel
```
อ่านผล:
- `show lacp`: ดู LACP info — LACP system priority, port priority, port state (active/standby)
- `show lacp port-channel <number>`: ดู port-channel LACP info — port type, member ports, selected/not selected
- `show interfaces port-channel`: ดู port-channel status — line protocol, bandwidth, load balancing
สาเหตุที่พบบ่อย:
1. Mode ไม่ตรง — side 1 เป็น `on`, side 2 เป็น `auto` → ต้องใช้ on-on หรือ auto-auto
2. Port ยังไม่ได้ใส่ channel-group — ต้องใช้ `channel-group <number> mode on`
3. LACP timeout ไม่ตั้งค่า → port ไม่ตอบ LACP PDU
วิธีแก้:
1. Set channel-group: `interface <port>` → `channel-group <number> mode on` หรือ `auto` → `end`
2. Set LACP port-priority: `interface <port>` → `lacp port-priority <1-65535>` → `end`
3. Set LACP system-priority: `lacp system-priority <1-65535>` → `end`
4. ตรวจ port-channel: `show lacp port-channel <number>` — ดู selected port
5. ตรวจ port status: `show interfaces port-channel` — ดู line protocol ขึ้น/up หรือไม่
ที่มา: Cisco C1300 CLI Guide — Port Channel Commands https://www.cisco.com/c/en/us/td/docs/switches/campus-lan-switches-access/Catalyst-1200-and-1300-Switches/cli/C1300-cli/port-channel-commands.html + LACP Commands https://www.cisco.com/c/en/us/td/docs/switches/campus-lan-switches-access/Catalyst-1200-and-1300-Switches/cli/C1300-cli/lacp-commands.html

## VLAN ไม่ผ่าน | ตรวจ VLAN config, switchport mode, trunk
คำค้น: vlan not passing, switchport mode not set, trunk not working, show vlan, show interfaces switchport, switchport mode, switchport access vlan, switchport trunk
อาการ: VLAN ไม่ผ่าน, ต้องการดู vlan config, ต้องการดู switchport mode, ต้องการดู trunk config
คำสั่งตรวจ:
```
show vlan
show interfaces switchport
show interfaces protected-ports
```
อ่านผล:
- `show vlan`: ดู VLAN info — VLAN ID, name, member ports (tagged/untagged)
- `show interfaces switchport`: ดู switchport detail — mode (access/trunk), access VLAN, trunk native VLAN, trunk allowed VLAN
- `show interfaces protected-ports`: ดู protected port status — port ที่เป็น protected จะ isolate จากกัน
สาเหตุที่พบบ่อย:
1. Port ไม่ได้ set switchport mode → ต้อง set เป็น access หรือ trunk
2. Access VLAN ผิด → ต้อง set `switchport access vlan <id>`
3. Trunk ไม่ allow VLAN → ต้อง set `switchport trunk allowed vlan`
4. Trunk native VLAN ผิด → ต้อง set `switchport trunk native vlan`
วิธีแก้:
1. Set switchport mode: `interface <port>` → `switchport mode <access/trunk>` → `end`
2. Set access VLAN: `interface <port>` → `switchport access vlan <id>` → `end`
3. Set trunk allowed VLAN: `interface <port>` → `switchport trunk allowed vlan <id-list>` → `end`
4. Set trunk native VLAN: `interface <port>` → `switchport trunk native vlan <id>` → `end`
5. Set trunk acceptable-frame-type: `interface <port>` → `switchport general acceptable-frame-type <tagged/untagged/all>` → `end`
6. ตรวจ VLAN: `show vlan` — ดู member ports ของ VLAN ที่ต้องการ
7. ตรวจ switchport: `show interfaces switchport` — ดู mode/access VLAN/trunk config
ที่มา: Cisco C1300 CLI Guide — VLAN Commands https://www.cisco.com/c/en/us/td/docs/switches/campus-lan-switches-access/Catalyst-1200-and-1300-Switches/cli/C1300-cli/vlan-commands.html
