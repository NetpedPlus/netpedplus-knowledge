---
id: huawei-port-mirroring
title: Huawei S12700E / S5731 Port Mirroring (observe-port)
families: huawei_vrp_s
triggers: huawei, observe-port, display port-mirroring, display observe-port, local port mirroring, 1:n mirroring, s12700e, s5731
vendor: Huawei
versions: VRP V200R019C00 ขึ้นไป (S12700, S12700E, S5731, S5735)
sources: https://support.huawei.com/enterprise/en/doc/EDOC1000091883/configuring-mirroring
---
# Huawei S12700E / S5731 Port Mirroring (observe-port)

## Port Mirroring | ตั้ง observe-port และ mirrored port สำหรับ capture traffic
คำค้น: port mirroring, observe-port, traffic mirroring, capture traffic, mirroring config, mirroring setup, local mirroring, 1:n mirroring, mirroring inbound, mirroring outbound, mirroring both, mirroring not working
อาการ: ต้องการ capture traffic เพื่อไล่ปัญหาเครือข่าย, traffic ไม่ผ่านต้องการดู packet, ต้องการ mirror traffic ไปยัง monitoring device (Wireshark, tcpdump, IDS), Mirroring ไม่ผ่าน — observe-port ไม่ได้รับ packet, mirrored port ส่ง packet ไป observe-port ไม่ได้
คำสั่งตรวจ:
```
display observe-port
display port-mirroring
```
อ่านผล:
- `display observe-port`: ดู observing port ที่ config ไว้ — Index, Interface, Untag-packet, Forwarding (Yes/No)
- `display port-mirroring`: ดู mirroring config ทั้งหมด — Port-mirror (Mirror-port, Direction, Observe-port), Stream-mirror, VLAN-mirror, MAC-mirror
สาเหตุที่พบบ่อย:
1. observe-port ไม่ได้ connect กับ monitoring device (Wireshark, IDS)
2. observe-port ยังเป็น unused — ต้อง config ก่อน mirrored port
3. Mirror port config ไม่ถูก direction — inbound/outbound/both
วิธีแก้:
- Config observe-port: `system-view` → `observe-port 1 interface gigabitethernet 1/0/1` (เอกสาร: Configuring Mirroring, Huawei S Series Troubleshooting Guide V200)
- Config mirrored port: `interface gigabitethernet 1/0/2` → `port-mirroring to observe-port 1 inbound` (เอกสาร: Configuring Mirroring, Huawei S Series Troubleshooting Guide V200)
- Config mirrored port ทั้ง inbound และ outbound: `port-mirroring to observe-port 1 both` (เอกสาร: Configuring Mirroring, Huawei S Series Troubleshooting Guide V200)
- Verify: `display observe-port` และ `display port-mirroring` — ต้องเห็น observe-port และ mirror-port ตรงกัน
ระวัง: S series (VRP V200) คำสั่งมีผลทันที ไม่ต้อง `commit` (commit เป็นของ CloudEngine) / พอร์ต observe ที่ส่ง traffic ไปเครื่อง capture อาจมีปริมาณเท่าพอร์ตต้นทาง — ถอด mirroring ออกเมื่อเสร็จ
ที่มา: Configuring Mirroring (Huawei S Series Troubleshooting Guide V200) https://support.huawei.com/enterprise/en/doc/EDOC1000091883/configuring-mirroring

## Port Mirroring | ตรวจ config mirroring ว่าถูกต้อง
คำค้น: display port-mirroring, display observe-port, mirroring check, mirroring verify, mirroring status, mirroring show, mirror configuration, mirror port not working, mirror traffic not received
อาการ: ต้องการตรวจว่า mirroring config ถูกต้องหรือไม่, observe-port ไม่ได้รับ mirrored traffic, mirrored port ไม่ copy traffic ไป observe-port, ต้องการดูว่า port ไหนเป็น mirror port, ต้องการดู direction ของ mirroring
คำสั่งตรวจ:
```
display observe-port
display port-mirroring
```
อ่านผล:
- `display observe-port`: ดู observing port ที่ config ไว้ — `Index` (1-8), `Interface` (พอร์ตที่ใช้งานเป็น observing port), `Untag-packet` (No/Yes), `Forwarding` (Yes/No)
- `display port-mirroring`: ดู Port-mirror section — `Mirror-port` (พอร์ตที่ mirror), `Direction` (Inbound/Outbound/Both), `Observe-port` (index ของ observing port)
- ตัวอย่าง output:
```
display port-mirroring
----------------------------------------------------------------------
Observe-port 1 : GigabitEthernet1/0/1
----------------------------------------------------------------------
Port-mirror:
----------------------------------------------------------------------
Mirror-port         Direction    Observe-port
----------------------------------------------------------------------
GigabitEthernet1/0/2  Inbound     Observe-port 1
----------------------------------------------------------------------
```
สาเหตุที่พบบ่อย:
1. observe-port index ไม่ตรงกับ port-mirroring config
2. Direction ไม่ถูก — ต้องใช้ `both` ถ้าต้องการทั้ง inbound และ outbound
3. observe-port ยังไม่ได้ commit — config ไม่生效
วิธีแก้:
- แก้ observe-port config: `system-view` → `observe-port 1 interface gigabitethernet 1/0/1`
- แก้ mirrored port direction: `interface gigabitethernet 1/0/2` → `port-mirroring to observe-port 1 both` (เอกสาร: Configuring Mirroring, Huawei S Series Troubleshooting Guide V200)
- ลบ mirroring: `undo port-mirroring to observe-port 1 inbound` (เอกสาร: Configuring Mirroring, Huawei S Series Troubleshooting Guide V200)
- ลบ observe-port: `undo observe-port 1` (เอกสาร: Configuring Mirroring, Huawei S Series Troubleshooting Guide V200)
ที่มา: Configuring Mirroring (Huawei S Series Troubleshooting Guide V200) https://support.huawei.com/enterprise/en/doc/EDOC1000091883/configuring-mirroring
