---
id: f5-bigip-17-ha-config-sync
title: F5 BIG-IP 17.x — ตรวจ ConfigSync บนคู่ HA
families: f5_tmsh
triggers: f5 bigip configsync troubleshooting, f5 show cm sync-status, f5 list cm device-group
versions: BIG-IP 17.5.x
sources: https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/cm/cm_sync-status.html, https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/cm/cm_device-group.html, https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/cm/cm_device.html
---

# F5 BIG-IP 17.x — ตรวจ ConfigSync บนคู่ HA

คำค้น: f5 bigip configsync troubleshooting, f5 show cm sync-status, f5 list cm device-group

อาการ: ConfigSync ไม่ผ่าน, config ไม่ sync ระหว่าง HA pair

---

## 1. ตรวจ ConfigSync status

คำค้น: f5 show cm sync-status

อาการ: ตรวจ configuration synchronization status

คำสั่งตรวจ:
```
show cm sync-status
```
อ่านผล: แสดงสถานะ configuration synchronization ของเครื่องที่รันคำสั่ง

ที่มา: [cm_sync-status.html (tmsh ref v17.0.0)](https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/cm/cm_sync-status.html)

อ้างอิง:
- "sync-status - Displays the configuration synchronization status of the local device." — tmsh reference v17.0.0 (cm_sync-status.html, NAME section)

---

## 2. ตรวจ device-group

คำค้น: f5 list cm device-group, f5 bigip device group list

อาการ: ตรวจ properties ของ device-group

คำสั่งตรวจ:
```
list cm device-group
```
อ่านผล: แสดง properties ของ device group

ที่มา: [cm_device-group.html (tmsh ref v17.0.0)](https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/cm/cm_device-group.html)

อ้างอิง:
- "device-group - Configures device groups. The device groups that are created and maintained by the system cannot be modified by the user." — tmsh reference v17.0.0 (cm_device-group.html, NAME section)
- "list device-group my_device_group — Displays properties of the device group named my_device_group." — tmsh reference v17.0.0 (cm_device-group.html, EXAMPLES section)

---

## 3. ตรวจ device

คำค้น: f5 list cm device, f5 bigip device list

อาการ: ตรวจ device ที่ระบุ

คำสั่งตรวจ:
```
list cm device
```
อ่านผล: แสดงรายการ device ตาม filter (name/glob/regex)

ที่มา: [cm_device.html (tmsh ref v17.0.0)](https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/cm/cm_device.html)

อ้างอิง:
- "device - Manages a device." — tmsh reference v17.0.0 (cm_device.html, NAME section)
- "list device [ [ [name] | [glob] | [regex] ] ... ]" — tmsh reference v17.0.0 (cm_device.html, DISPLAY section)

---

หมายเหตุ:
- KME 3.2 Failover เอง: ไม่พบที่มาที่อธิบายขั้นตอนแก้ปัญหา (ตรวจแล้ว: cm_failover-status.html tmsh ref v17.0.0 — ยังไม่ได้เปิดตรวจหน้าอื่น)
- KME 3.3 Device Trust เสีย: ไม่พบที่มาที่อธิบายขั้นตอนแก้ปัญหา (ยังไม่ได้เปิดตรวจหน้า troubleshooting device trust)
- KME 3.4 Primary ล้ม / Traffic Groups: ไม่พบที่มาที่อธิบายขั้นตอนแก้ปัญหา (ตรวจแล้ว: cm_traffic-group.html tmsh ref v17.0.0 — DESCRIPTION: "You can use the traffic-group component to specify the failover behavior for devices in a failover device group." มีเนื้อหาเกี่ยวกับ failover แต่เป็นคำสั่งตั้งค่า ไม่ใช่ขั้นตอนแก้ปัญหา)
