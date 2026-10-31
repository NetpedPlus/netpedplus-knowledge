---
id: tplink-omada-sx6632yf-mstp-lag-vlan
title: TP-Link Omada SX6632YF — MSTP topology change บ่อย, LAG ไม่ขึ้น, VLAN ไม่ผ่าน
families: tplink_jetstream
triggers: tp-link, tplink, omada, sx6632yf, jetstream
vendor: TP-Link
versions: SX6632YF (Omada Firmware UN 1.0 — 1.20)
sources: https://www.tp-link.com/en/configuration-guides/configuring_spanning_tree/, https://www.tp-link.com/en/configuration-guides/configuring_lag/, https://www.tp-link.com/en/configuration-guides/configuring_802_1q_vlan/, https://omada.tp-link.com/en/article/key-581
---
# TP-Link Omada SX6632YF — MSTP topology change บ่อย, LAG ไม่ขึ้น, VLAN ไม่ผ่าน

> **หมายเหตุ:** สวิตช์นี้จัดการผ่าน **Omada Controller** (GUI) เป็นหลัก เจ้าของล็อกอินตัวสวิตช์ไม่ได้
> ขั้นตอน GUI คือวิธีหลัก CLI ใส่ได้เฉพาะที่คัดลอกจาก CLI Reference Guide จริง ไม่เจอให้ลบ

## MSTP topology change บ่อย | ตรวจผ่าน Omada Controller ว่า TC มาจากพอร์ตไหน
คำค้น: topology change, tc protect, tc bpdu, show spanning-tree, show spanning-tree interface, show spanning-tree mst, show spanning-tree bridge, show lacp internal, omada controller, topology, port flap, sfp rx low, edge port, bpdu protect, bpdu filter
อาการ: MSTP topology change บ่อย, ต้องการดู topology change จากไหน, ต้องการดู edge port, ต้องการดู tc protect, ต้องการดู port ที่ flap, ต้องการดู sfp rx
คำสั่งตรวจ:
```
show spanning-tree bridge mode
show spanning-tree interface ten-gigabitEthernet 1/0/1
show lacp internal
```
อ่านผล:
- `show spanning-tree bridge mode`: ดู STP mode (STP/RSTP/MSTP), root bridge priority, bridge priority
- `show spanning-tree interface <port>`: ดู port STP status, role, state, edge, cost, priority
- `show lacp internal`: ดู LACP internal info — sys-priority, sys-mac, port-priority, port-state, admin-key
ตรวจใน GUI:
1. **Topology → Dashboard**: ดู topology map — จุดที่ขึ้นสีแดง/เหลือง = link down/flap
2. **Topology → Topology**: ดู topology tree — หา port ที่ขึ้น "Disconnected" หรือ "Topology Change"
3. **Devices → SX6632YF → Port Management**: ดู port status, SFP Rx power (mW/dBm) — Rx ต่ำกว่า -15 dBm = sfp เก่า/สกปรก
4. **Devices → SX6632YF → Spanning Tree**: ดู MSTP mode, root bridge, port role, port state
5. **Devices → SX6632YF → Logs**: ดู log "topology change", "port down", "link down" — หา source port
สาเหตุที่พบบ่อย:
1. Port ที่ไม่มี edge-port flag — เมื่อ port ขึ้น/ลง จะ generate TC
2. Port server/SFP flap (SFP Rx ต่ำ — มักเกิดจาก SFP เก่า/สกปรก/ไม่ตรง spec)
3. ไม่มี TC Protect — TC BPDU หลายตัวทำให้ MAC table ล้างบ่อย
4. Edge port ไม่ได้ enable BPDU filter — port ผู้ใช้ส่ง BPDU ทำให้ recalculate
วิธีแก้ (Omada Controller GUI):
1. Enable TC Protect: **Omada Controller → Devices → SX6632YF → Spanning Tree → TC Protect → Enable** → Save
2. Set edge port: **Devices → SX6632YF → Port Management → Port → Edit → Spanning Tree → Edge Port → Enable** → Save
3. Enable BPDU Filter: **Devices → SX6632YF → Port Management → Port → Edit → Spanning Tree → BPDU Filter → Enable** → Save
4. ตรวจ SFP: **Devices → SX6632YF → Port Management** → ดู SFP Rx Power — ถ้าต่ำกว่า -15 dBm ให้เปลี่ยน SFP
5. CLI: `configure` → `spanning-tree tc-protect` → `end` → `copy running-config startup-config` (เอกสาร: Configuring Spanning Tree, TP-Link)
ที่มา: TP-Link Omada Configuring Spanning Tree https://www.tp-link.com/en/configuration-guides/configuring_spanning_tree/ + Omada Controller GUI https://omada.tp-link.com/en/article/key-581

## LAG ไม่ขึ้น | ตรวจผ่าน Omada Controller ว่า LAG ขึ้นหรือไม่
คำค้น: lag table, lacp config, port-channel, static lag, lacp lag, show lacp internal, show lacp sys-id, omada controller, lag status, lacp neighbor, admin key
อาการ: LAG ไม่ขึ้น, ต้องการดู lag status, ต้องการดู lacp neighbor, ต้องการดู admin key, ต้องการดู port-channel status
คำสั่งตรวจ:
```
show lacp internal
show lacp sys-id
```
อ่านผล:
- `show lacp internal`: ดู LACP internal — sys-priority, sys-mac, port-priority, port-state, admin-key, selected/not selected
- `show lacp sys-id`: ดู LACP system priority globally — sys-priority, sys-mac
ตรวจใน GUI:
1. **Devices → SX6632YF → LAG → LAG Table**: ดู LAG status — Active/Inactive, member ports, admin key
2. **Devices → SX6632YF → LAG → LACP Config**: ดู LACP mode, port priority, status — port ที่ไม่ขึ้นเป็น "Inactive"
3. **Devices → SX6632YF → Port Management**: ดู member port status — port ที่ไม่ join LAG จะแสดง "Disconnected"
4. **Devices → SX6632YF → Logs**: ดู log "lag down", "member port down" — หาสาเหตุ
สาเหตุที่พบบ่อย:
1. Mode ไม่ตรง — side 1 เป็น active, side 2 เป็น passive → ต้องใช้ active-active หรือ active-passive
2. Admin Key ไม่ตรง — port ต้องมี Admin Key เดียวกันจึงจะ join group เดียวกัน
3. Port priority ผิด — port backup ไม่เลือก port ที่ต้องการ
4. Port member ไม่ได้ set LAG — port ต้องถูกเพิ่มใน LAG group
วิธีแก้ (Omada Controller GUI):
1. Set LAG mode: **Devices → SX6632YF → LAG → LACP Config** → เลือก port → Mode = Active/Passive → Admin Key = เดียวกัน → Apply
2. Set port priority: **Devices → SX6632YF → LAG → LACP Config** → Port Priority = 32768 (default) → Apply
3. ตรวจ LAG status: **Devices → SX6632YF → LAG → LAG Table** → ดู Active/Inactive
4. CLI: `configure` → `interface ten-gigabitEthernet 1/0/1` → `lag mode lacp` → `lag group 1` → `end` → `copy running-config startup-config` (เอกสาร: Configuring LAG, TP-Link)
ที่มา: TP-Link Omada Configuring LAG https://www.tp-link.com/en/configuration-guides/configuring_lag/ + Omada Controller GUI https://omada.tp-link.com/en/article/key-581

## VLAN ไม่ผ่าน | ตรวจผ่าน Omada Controller ว่า VLAN config ถูกต้องหรือไม่
คำค้น: vlan config, port config, show vlan, show interface switchport, switchport general allowed vlan, switchport pvid vlan-id, omada controller, vlan mapping, port profile, vlan id
อาการ: VLAN ไม่ผ่าน, ต้องการดู vlan config, ต้องการดู port config, ต้องการดู pvid, ต้องการดู vlan mapping
คำสั่งตรวจ:
```
show vlan id 10
show interface switchport
```
อ่านผล:
- `show vlan id <id>`: ดู VLAN detail — VLAN ID, Name, Type, Ports
- `show interface switchport`: ดู switchport detail — Port, LAG, Type (General/Access), PVID, Acceptable frame type, Ingress Checking
ตรวจใน GUI:
1. **Devices → SX6632YF → VLAN → 802.1Q VLAN → VLAN Config**: ดู VLAN ID, Name, member ports (tagged/untagged)
2. **Devices → SX6632YF → VLAN → 802.1Q VLAN → Port Config**: ดู port PVID, Acceptable frame type, Ingress Checking
3. **Devices → SX6632YF → Port Management**: ดู port status — ถ้า port ถูก assign ผิด VLAN จะเห็น "Untagged" หรือ "Tagged" ผิด
4. **Devices → SX6632YF → Logs**: ดู log "vlan mismatch", "port down" — หาสาเหตุ
สาเหตุที่พบบ่อย:
1. Port ยังไม่ได้ assign VLAN — ต้องใช้ command `switchport general allowed vlan`
2. PVID ยังไม่ได้ set — ต้องใช้ command `switchport pvid vlan-id`
3. Ingress Checking ยังไม่ได้ enable — ต้องใช้ command `switchport check ingress`
4. Tagged/Untagged ผิด — port ไป server ต้องเป็น tagged, port ไป PC ต้องเป็น untagged
วิธีแก้ (Omada Controller GUI):
1. สร้าง VLAN: **Devices → SX6632YF → VLAN → 802.1Q VLAN → VLAN Config** → Enter VLAN ID, Name → Add ports (tagged/untagged) → Save
2. Set PVID: **Devices → SX6632YF → VLAN → 802.1Q VLAN → Port Config** → Port PVID = VLAN ID → Apply
3. Set tagged/untagged: **Devices → SX6632YF → VLAN → 802.1Q VLAN → VLAN Config** → Add port as tagged/untagged → Save
4. CLI: `configure` → `interface ten-gigabitEthernet 1/0/1` → `switchport general allowed vlan 10 tagged` → `end` → `copy running-config startup-config` (เอกสาร: Configuring 802.1Q VLAN, TP-Link)
ที่มา: TP-Link Omada Configuring 802.1Q VLAN https://www.tp-link.com/en/configuration-guides/configuring_802_1q_vlan/ + Omada Controller GUI https://omada.tp-link.com/en/article/key-581
