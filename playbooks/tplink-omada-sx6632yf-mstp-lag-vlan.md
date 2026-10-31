---
id: tplink-omada-sx6632yf-mstp-lag-vlan
title: TP-Link Omada SX6632YF — MSTP topology change บ่อย, LAG ไม่ขึ้น, VLAN ไม่ผ่าน
families: tplink_jetstream
triggers: tp-link, tplink, omada, sx6632yf, jetstream, show spanning-tree, show lacp, show vlan, switchport general allowed vlan, spanning-tree tc protect, spanning-tree bpduguard
vendor: TP-Link
versions: SX6632YF (Omada Firmware UN 1.0 — 1.20)
sources: https://www.tp-link.com/en/configuration-guides/configuring_spanning_tree/, https://www.tp-link.com/en/configuration-guides/configuring_lag/, https://www.tp-link.com/en/configuration-guides/configuring_802_1q_vlan/
---
# TP-Link Omada SX6632YF — MSTP topology change บ่อย, LAG ไม่ขึ้น, VLAN ไม่ผ่าน

## MSTP topology change บ่อย | ตรวจว่า TC เหตุผลจากอะไร
คำค้น: show spanning-tree, show spanning-tree interface, show spanning-tree mst, spanning-tree tc protect, tc protect, tc bpdu, topology change bpdu, show lacp internal, show lacp, show lacp sys-id, root bridge, bpdu protect, bpdu filter, edge port
อาการ: MSTP topology change บ่อย — ต้องการตรวจว่า TC เกิดจากอะไร, ต้องการดู spanning-tree status, ต้องการดู root bridge, ต้องการดู edge port, ต้องการดู TC protect config
คำสั่งตรวจ:
```
show spanning-tree bridge mode
show spanning-tree interface gigabitEthernet 1/0/1
show lacp internal
```
อ่านผล:
- `show spanning-tree bridge mode`: ดู STP mode (STP/RSTP/MSTP), root bridge priority, bridge priority
- `show spanning-tree interface <port>`: ดู port STP status, role, state, edge, cost, priority
- `show lacp internal`: ดู LACP internal info — sys-priority, sys-mac, port-priority, port-state, admin-key
- ตัวอย่าง output (จากเอกสาร TP-Link):
```
Switch# show spanning-tree bridge mode
Mode: RSTP
Root Bridge Priority: 32768
Bridge Priority: 32768
```
สาเหตุที่พบบ่อย:
1. Port ที่ไม่มี edge-port flag — เมื่อ port ขึ้น/ลง จะ generate TC
2. ไม่มี TC Protect — TC BPDU หลายตัวทำให้ MAC table ล้างบ่อย
3. Edge port ไม่ได้ enable BPDU filter — port ผู้ใช้ส่ง BPDU ทำให้ recalculate
วิธีแก้:
- Enable TC Protect: `configure` → `spanning-tree tc-protect` → `end` (เอกสาร: Configuring Spanning Tree, TP-Link)
- Set edge port: `configure` → `interface ten-gigabitEthernet 1/0/1` → `spanning-tree edge-port` → `end` (เอกสาร: Configuring Spanning Tree, TP-Link)
- Enable BPDU Filter: `configure` → `interface ten-gigabitEthernet 1/0/1` → `spanning-tree bpdu-filter` → `end` (เอกสาร: Configuring Spanning Tree, TP-Link)
- บันทึก config: `copy running-config startup-config` (เอกสาร: CLI Examples, TP-Link)
ที่มา: TP-Link Omada Configuring Spanning Tree https://www.tp-link.com/en/configuration-guides/configuring_spanning_tree/

## LAG ไม่ขึ้น | ตรวจว่า LAG (static/LACP) ขึ้นหรือไม่
คำค้น: show lacp internal, show lacp neighbor, show lacp sys-id, show lacp, show interface switchport, show interface port-channel, static lag, lacp lag, admin key, port priority, show lacp 1 internal
อาการ: LAG ไม่ขึ้น — ต้องการตรวจว่า LAG ขึ้นหรือไม่, ต้องการดู LACP internal, ต้องการดู sys-id, ต้องการดู admin key, ต้องการดู port priority
คำสั่งตรวจ:
```
show lacp internal
show lacp sys-id
```
อ่านผล:
- `show lacp internal`: ดู LACP internal — sys-priority, sys-mac, port-priority, port-state, admin-key, selected/not selected
- `show lacp sys-id`: ดู LACP system priority globally — sys-priority, sys-mac
- ตัวอย่าง output (จากเอกสาร TP-Link):
```
Switch# show lacp sys-id
0, 000a.eb13.2397
Switch# show lacp 1 internal
Flags: S - Device is requesting Slow LACPDUs
       D - Device is requesting Fast LACPDUs
       A - Device has arrived
       S - Device sending LACPDUs has gone
       F - Device requested timeout expiry
       R - Device requested LACP termination
       E - Device is requesting EDP
       * - Port is aggregating

Port   Flags  Sys-pri  Sys-Mac       Admin Key  Port Key  Port Prio  State
------ ------ -------- ------------- ---------- --------- ---------- -------
1      SAREFR 32768    000a.eb13.2397  0          1         32768      0x2D
```
สาเหตุที่พบบ่อย:
1. Mode ไม่ตรง — side 1 เป็น active, side 2 เป็น passive → ต้องใช้ active-active หรือ active-passive
2. Admin Key ไม่ตรง — port ต้องมี Admin Key เดียวกันจึงจะ join group เดียวกัน
3. Port priority ผิด — port backup ไม่เลือก port ที่ต้องการ
วิธีแก้:
- สร้าง LAG: GUI L2 FEATURES > Switching > LAG > LACP Config หรือ CLI `configure` → `interface ten-gigabitEthernet 1/0/1` → `lag mode lacp` → `lag group 1` → `end` (เอกสาร: Configuring LAG, TP-Link)
- ตรวจ LACP: `show lacp internal` → ดู port-state (0x2D = aggregating, selected) (เอกสาร: Configuring LAG, TP-Link)
- GUI: Omada Controller > Switching > LAG > LACP Config
- บันทึก config: `copy running-config startup-config` (เอกสาร: CLI Examples, TP-Link)
ที่มา: TP-Link Omada Configuring LAG https://www.tp-link.com/en/configuration-guides/configuring_lag/

## VLAN ไม่ผ่าน | ตรวจว่า VLAN config ถูกต้องหรือไม่
คำค้น: show vlan, show interface switchport, switchport general allowed vlan, switchport pvid vlan-id, switchport acceptable frame, switchport check ingress, port config vlan, show vlan id
อาการ: VLAN ไม่ผ่าน — ต้องการตรวจว่า VLAN config ถูกต้องหรือไม่, ต้องการดู VLAN information, ต้องการดู switchport config, ต้องการดู PVID config
คำสั่งตรวจ:
```
show vlan id 10
show interface switchport
```
อ่านผล:
- `show vlan id <id>`: ดู VLAN detail — VLAN ID, Name, Type, Ports
- `show interface switchport`: ดู switchport detail — Port, LAG, Type (General/Access), PVID, Acceptable frame type, Ingress Checking
- ตัวอย่าง output (จากเอกสาร TP-Link):
```
Switch# show interface switchport
Port    LAG   Type     PVID  Acceptable frame type  Ingress Checking
------  ---   -------- ----  ---------------------  ----------------
Gi1/0/1 N/A   General  1     All                    Enable
Gi1/0/2 N/A   General  10    All                    Enable
Gi1/0/4 N/A   General  1     All                    Enable
```
สาเหตุที่พบบ่อย:
1. Port ยังไม่ได้ assign VLAN — ต้องใช้ command `switchport general allowed vlan`
2. PVID ยังไม่ได้ set — ต้องใช้ command `switchport pvid vlan-id`
3. Ingress Checking ยังไม่ได้ enable — ต้องใช้ command `switchport check ingress`
วิธีแก้:
- สร้าง VLAN: GUI L2 FEATURES > VLAN > 802.1Q VLAN > VLAN Config หรือ CLI `configure` → `vlan 10` → `name Department_A` → `end` (เอกสาร: Configuring 802.1Q VLAN, TP-Link)
- เพิ่ม VLAN ไป port: `configure` → `interface ten-gigabitEthernet 1/0/1` → `switchport general allowed vlan 10 tagged` → `end` (เอกสาร: Configuring 802.1Q VLAN, TP-Link)
- Set PVID: `configure` → `interface ten-gigabitEthernet 1/0/1` → `switchport pvid vlan 10` → `end` (เอกสาร: Configuring 802.1Q VLAN, TP-Link)
- GUI: Omada Controller > Switching > VLAN > 802.1Q VLAN
- บันทึก config: `copy running-config startup-config` (เอกสาร: CLI Examples, TP-Link)
ที่มา: TP-Link Omada Configuring 802.1Q VLAN https://www.tp-link.com/en/configuration-guides/configuring_802_1q_vlan/
