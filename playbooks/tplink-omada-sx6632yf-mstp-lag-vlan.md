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
> ขั้นตอนในหัวข้อนี้เป็นแบบ GUI ทั้งหมด (ยังไม่มี CLI ที่ยืนยันกับ CLI Reference ของรุ่นนี้)

## MSTP topology change บ่อย | ตรวจผ่าน Omada Controller ว่า TC มาจากพอร์ตไหน
คำค้น: topology change, tc protect, tc bpdu, omada controller, topology, port flap, sfp rx low, edge port, bpdu protect, bpdu filter
อาการ: MSTP topology change บ่อย, ต้องการดู topology change จากไหน, ต้องการดู edge port, ต้องการดู tc protect, ต้องการดู port ที่ flap, ต้องการดู sfp rx
ตรวจใน GUI:
1. **Topology → Dashboard**: ดู topology map — จุดที่ขึ้นสีแดง/เหลือง = link down/flap
2. **Topology → Topology**: ดู topology tree — หา port ที่ขึ้น "Disconnected" หรือ "Topology Change"
3. **Devices → SX6632YF → Port Management**: ดู port status, SFP Rx power (mW/dBm) — เทียบกับค่า Rx ที่ระบุใน datasheet ของ SFP รุ่นนั้น
4. **Devices → SX6632YF → Spanning Tree**: ดู MSTP mode, root bridge, port role, port state
5. **Devices → SX6632YF → Logs**: ดู log "topology change", "port down", "link down" — หา source port
สาเหตุที่พบบ่อย:
1. Port ที่ไม่มี edge-port flag — เมื่อ port ขึ้น/ลง จะ generate TC
2. Port server/SFP flap (SFP Rx ต่ำ — มักเกิดจาก SFP เก่า/สกปรก/ไม่ตรง spec)
3. ไม่มี TC Protect — TC BPDU หลายตัวทำให้ MAC table ล้างบ่อย
วิธีแก้ (Omada Controller GUI):
1. Enable TC Protect: **Omada Controller → Devices → SX6632YF → Spanning Tree → TC Protect → Enable** → Save
2. Set edge port: **Devices → SX6632YF → Port Management → Port → Edit → Spanning Tree → Edge Port → Enable** → Save
3. ตรวจ SFP: **Devices → SX6632YF → Port Management** → ดู SFP Rx Power — ต่ำกว่าช่วงใน datasheet ของ SFP = ทำความสะอาดหัว / เปลี่ยน SFP หรือสาย
ระวัง: edge port ใส่เฉพาะพอร์ตที่ต่อ server / เครื่องปลายทาง ห้ามใส่พอร์ตที่ต่อ switch อื่น (เกิด loop ได้) / เมนูใน Controller อาจต่างตามเวอร์ชัน
ที่มา: TP-Link Omada Configuring Spanning Tree https://www.tp-link.com/en/configuration-guides/configuring_spanning_tree/ + Omada Controller GUI https://omada.tp-link.com/en/article/key-581

## LAG ไม่ขึ้น | ตรวจผ่าน Omada Controller ว่า LAG ขึ้นหรือไม่
คำค้น: lag table, lacp config, port-channel, static lag, lacp lag, show lacp sys-id, omada controller, lag status, lacp neighbor, admin key
อาการ: LAG ไม่ขึ้น, ต้องการดู lag status, ต้องการดู lacp neighbor, ต้องการดู admin key, ต้องการดู port-channel status
ตรวจใน GUI:
1. **Devices → SX6632YF → LAG → LAG Table**: ดู LAG status — Active/Inactive, member ports, admin key
2. **Devices → SX6632YF → LAG → LACP Config**: ดู LACP mode, port priority, status — port ที่ไม่ขึ้นเป็น "Inactive"
3. **Devices → SX6632YF → Port Management**: ดู member port status — port ที่ไม่ join LAG จะแสดง "Disconnected"
4. **Devices → SX6632YF → Logs**: ดู log "lag down", "member port down" — หาสาเหตุ
สาเหตุที่พบบ่อย:
1. อีกฝั่งเป็น static LAG แต่ฝั่งนี้เป็น LACP (หรือ Passive ทั้งสองฝั่ง) → ต้องเป็น LACP ทั้งคู่ และมี Active อย่างน้อยหนึ่งฝั่ง
2. Admin Key ไม่ตรง — port ต้องมี Admin Key เดียวกันจึงจะ join group เดียวกัน
3. Port priority ผิด — port backup ไม่เลือก port ที่ต้องการ
4. Port member ไม่ได้ set LAG — port ต้องถูกเพิ่มใน LAG group
วิธีแก้ (Omada Controller GUI):
1. Set LAG mode: **Devices → SX6632YF → LAG → LACP Config** → เลือก port → Mode = Active/Passive → Admin Key = เดียวกัน → Apply
2. Set port priority: **Devices → SX6632YF → LAG → LACP Config** → Port Priority → Apply (ค่าน้อยกว่าถูกเลือกก่อน)
3. ตรวจ LAG status: **Devices → SX6632YF → LAG → LAG Table** → ดู Active/Inactive
ที่มา: TP-Link Omada Configuring LAG https://www.tp-link.com/en/configuration-guides/configuring_lag/ + Omada Controller GUI https://omada.tp-link.com/en/article/key-581

## VLAN ไม่ผ่าน | ตรวจผ่าน Omada Controller ว่า VLAN config ถูกต้องหรือไม่
คำค้น: vlan config, port config, show vlan, show interface switchport, switchport general allowed vlan, switchport pvid vlan-id, omada controller, vlan mapping, port profile, vlan id
อาการ: VLAN ไม่ผ่าน, ต้องการดู vlan config, ต้องการดู port config, ต้องการดู pvid, ต้องการดู vlan mapping
ตรวจใน GUI:
1. **Devices → SX6632YF → VLAN → 802.1Q VLAN → VLAN Config**: ดู VLAN ID, Name, member ports (tagged/untagged)
2. **Devices → SX6632YF → VLAN → 802.1Q VLAN → Port Config**: ดู port PVID, Acceptable frame type, Ingress Checking
3. **Devices → SX6632YF → Port Management**: ดู port status — ถ้า port ถูก assign ผิด VLAN จะเห็น "Untagged" หรือ "Tagged" ผิด
4. **Devices → SX6632YF → Logs**: ดู log "vlan mismatch", "port down" — หาสาเหตุ
สาเหตุที่พบบ่อย:
1. Port ยังไม่ได้ใส่ VLAN (tagged / untagged) ใน Port Profile
2. Native / PVID ของพอร์ตไม่ตรงกับอีกฝั่ง
3. Tagged / untagged ไม่ตรงกับอีกฝั่ง (trunk ไป server / switch = tagged, เครื่องที่ไม่รู้จัก VLAN = untagged)
วิธีแก้ (Omada Controller GUI):
1. สร้าง VLAN: **Devices → SX6632YF → VLAN → 802.1Q VLAN → VLAN Config** → Enter VLAN ID, Name → Add ports (tagged/untagged) → Save
2. Set PVID: **Devices → SX6632YF → VLAN → 802.1Q VLAN → Port Config** → Port PVID = VLAN ID → Apply
3. Set tagged/untagged: **Devices → SX6632YF → VLAN → 802.1Q VLAN → VLAN Config** → Add port as tagged/untagged → Save
ที่มา: TP-Link Omada Configuring 802.1Q VLAN https://www.tp-link.com/en/configuration-guides/configuring_802_1q_vlan/ + Omada Controller GUI https://omada.tp-link.com/en/article/key-581
