---
id: h3c-s6520x-irf-lag-vlan
title: H3C S6520X Comware 7 — IRF แตก, BAGG (LACP) ไม่ขึ้น, VLAN ไม่ผ่าน
families: hpe_comware
triggers: h3c, comware, s6520x, irf, bridge-aggregation, irf split, irf topology, display irf, display link-aggregation, port trunk permit vlan
vendor: H3C
versions: Comware 7 (S6520X-HI/EI/SI, S6520-SI)
sources: https://www.h3c.com/en/Support/Resource_Center/EN/Home/Public/00-Public/Technical_Documents/Configure___Deploy/Configuration_Guides/S6520X-EI_HI_SI_S6520-SI_CG-R65xx/02/202412/2328678_294551_0.htm
---
# H3C S6520X Comware 7 — IRF แตก, BAGG (LACP) ไม่ขึ้น, VLAN ไม่ผ่าน

## IRF แตก / split | ตรวจว่า IRF fabric ยังเชื่อมต่อกันหรือไม่
คำค้น: irf split, irf fabric, display irf, display irf topology, irf link, irf member, irf priority, irf split detection, irf bridge mac, mad, lacp mad, bfd mad, irf topology down, irf port down
อาการ: IRF แตก — ต้องการตรวจว่า member ไหน down, ต้องการดู irf topology, IRF link ไม่ขึ้น, ต้องการตรวจ irf fabric status, ต้องการดู member priority, bridge mac address
คำสั่งตรวจ:
```
display irf
display irf topology
```
อ่านผล:
- `display irf`: ดู IRF fabric ทั้งหมด — member ID, role (Master/Slave), priority, bridge MAC, description, active ID
- `display irf topology`: ดู IRF topology — IRF-Port1/2, member ID, link state (UP/DOWN), link neighbor, belogn to
- ตัวอย่าง output:
```
<Sysname> display irf
Topology Info
IRF-Port1 IRF-Port2
MemberID Link neighbor Link neighbor Belong To
1 DOWN --- UP 2 000f-cbb8-1a82
2 UP 1 DOWN --- 000f-cbb8-1a82
```
สาเหตุที่พบบ่อย:
1. IRF link ไม่ขึ้น — ตรวจสอบ physical connection, SFP, cable
2. Active ID ไม่ตรงกัน — IRF fabric ได้ split
3. IRF priority ผิด — device ที่ควรเป็น Master มี priority ต่ำกว่า
4. LACP MAD หรือ BFD MAD ไม่ทำงาน — IRF fabric ไม่ detect split
วิธีแก้:
- ตรวจ IRF link: `display irf topology` → ดู Link field — ถ้า DOWN ให้ตรวจ physical connection, SFP, cable (เอกสาร: IRF commands, H3C S6520X Comware 7)
- แก้ IRF priority: `system-view` → `irf port 1` → `priority <1-9>` → `quit` (เอกสาร: 01-IRF configuration, H3C S6520X Comware 7)
- แก้ IRF member ID: `system-view` → `irf member <id> priority <1-9>` → `quit` (เอกสาร: 01-IRF configuration, H3C S6520X Comware 7)
- บันทึก config: `save` → `y` (Comware มีผลทันที บันทึกด้วย save) (เอกสาร: 01-IRF configuration, H3C S6520X Comware 7)
ที่มา: IRF commands (H3C S6520X Comware 7) https://www.h3c.com/en/Support/Resource_Center/EN/Home/Public/00-Public/Technical_Documents/Configure___Deploy/Configuration_Guides/S6520X-EI_HI_SI_S6520-SI_CG-R65xx/02/202412/2328678_294551_0.htm

## BAGG (LACP) ไม่ขึ้น | ตรวจว่า LAG ขึ้นหรือไม่
คำค้น: lacp, bagg, bridge-aggregation, display link-aggregation, link aggregation not up, lacp not working, lacp active passive, lacp timeout, lacp system priority, lacp system mac, display link-aggregation verbose, display link-aggregation summary, lacp mismatch, lacp partner
อาการ: LAG ไม่ขึ้น — ต้องการตรวจว่า LACP config ถูกต้องหรือไม่, BAGG ไม่ขึ้น, ต้องการดู LACP state, ต้องการดู member port ของ LAG, ต้องการดู LACP system priority, ต้องการดู LACP partner information
คำสั่งตรวจ:
```
display link-aggregation summary
display link-aggregation verbose
display link-aggregation member-port <interface-type> <interface-number>
```
อ่านผล:
- `display link-aggregation summary`: ดู LAG ทั้งหมด — Aggregate Interface Type (BAGG=L2, RAGG=L3), group ID, status
- `display link-aggregation verbose`: ดู LAG detail — member ports, LACP state, index, selected/not selected
- `display link-aggregation member-port <interface>`: ดู member port detail — aggregate interface, port number, LACP state
- ตัวอย่าง output:
```
<Sysname> display link-aggregation summary
Aggregate Interface Type:
BAGG -- Bridge-Aggregation, RAGG -- Route-Aggregation
Bridge-Aggregation1:
    Type: Dynamic Selected-Ports: 2 Total-Ports: 2
    Port Status:
        Ten-GigabitEthernet1/0/1 Selected
        Ten-GigabitEthernet1/0/2 Selected
```
สาเหตุที่พบบ่อย:
1. LACP mode ไม่ตรง — side 1 เป็น active, side 2 เป็น passive → ต้องใช้ active-active หรือ active-passive
2. LACP timeout ผิด — side 1 เป็น short timeout, side 2 เป็น long timeout → ต้องตรงกัน
3. LACP system priority ไม่ตรง → ใช้ system MAC address ผิด
4. Member port config ผิด → ต้องใช้ command ที่ถูกต้อง
วิธีแก้:
- สร้าง LAG: `system-view` → `bridge-aggregation <id>` → `lacp priority <0-65535>` → `quit` (เอกสาร: Ethernet link aggregation commands, H3C S6520X Comware 7)
- เพิ่ม member port: `interface <type> <number>` → `link-aggregation mode dynamic` → `link-aggregation group <id>` → `quit` (เอกสาร: Ethernet link aggregation configuration, H3C S6520X Comware 7)
- ตรวจ LACP: `display link-aggregation verbose` → ดู LACP state, selected/not selected (เอกสาร: Ethernet link aggregation commands, H3C S6520X Comware 7)
- บันทึก config: `save` → `y` (Comware มีผลทันที บันทึกด้วย save) (เอกสาร: Ethernet link aggregation configuration, H3C S6520X Comware 7)
ที่มา: Ethernet link aggregation commands (H3C S6520X Comware 7) https://www.h3c.com/en/d_202407/2219027_294551_0.htm

## VLAN ไม่ผ่าน | ตรวจว่า VLAN config ถูกต้องหรือไม่
คำค้น: vlan, display vlan, port trunk, port access, port hybrid, vlan not working, vlan not passed, trunk port, access port, trunk permit vlan, access port vlan, hybrid port vlan
อาการ: VLAN ไม่ผ่าน — ต้องการตรวจว่า VLAN config ถูกต้องหรือไม่, ต้องการดู VLAN information, ต้องการดู trunk port config, ต้องการดู access port config, ต้องการดู hybrid port config
คำสั่งตรวจ:
```
display vlan
display vlan brief
display port { trunk | hybrid }
```
อ่านผล:
- `display vlan`: ดู VLAN ทั้งหมด — VLAN ID, name, status, member ports
- `display vlan brief`: ดู VLAN สั้น — VLAN ID, status, number of ports
- `display port { trunk | hybrid }`: ดู port config — port type (trunk/hybrid), permitted VLANs
- ตัวอย่าง output:
```
<Sysname> display vlan 2
VLAN ID: 2
VLAN Type: static
Description: VLAN 0002
Bridge-Aggregation1: 1
Ten-GigabitEthernet1/0/1: 1
```
สาเหตุที่พบบ่อย:
1. Trunk port ยังไม่ได้ permit VLAN — ต้องใช้ command `port trunk permit vlan`
2. Access port ยังไม่ได้ assign VLAN — ต้องใช้ command `port access vlan`
3. VLAN ยังไม่ได้สร้าง — ต้องใช้ command `vlan <id>`
วิธีแก้:
- สร้าง VLAN: `system-view` → `vlan <id>` → `description <name>` → `quit` (เอกสาร: VLAN commands, H3C S6520X Comware 7)
- เพิ่ม VLAN ไป trunk port: `interface <type> <number>` → `port link-type trunk` → `port trunk permit vlan <id-list>` → `quit` (เอกสาร: VLAN commands, H3C S6520X Comware 7)
- assign VLAN ไป access port: `interface <type> <number>` → `port link-type access` → `port access vlan <id>` → `quit` (เอกสาร: VLAN commands, H3C S6520X Comware 7)
- บันทึก config: `save` → `y` (Comware มีผลทันที บันทึกด้วย save) (เอกสาร: VLAN commands, H3C S6520X Comware 7)
ที่มา: VLAN commands (H3C S6520X Comware 7) https://www.h3c.com/en/d_202511/2692614_294551_0.htm
