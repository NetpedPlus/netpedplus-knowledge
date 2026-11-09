---
id: f5-bigip-17-ha-failover
title: F5 BIG-IP 17.x — ตรวจและบังคับ failover บนคู่ HA
families: f5_tmsh
triggers: f5 bigip failover status, f5 show sys failover, f5 bigip force standby, f5 run failover
versions: BIG-IP 17.5.x
sources: https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/sys/sys_failover.html
---

# F5 BIG-IP 17.x — ตรวจและบังคับ failover บนคู่ HA

คำค้น: f5 bigip failover status, f5 show sys failover, f5 bigip force standby, f5 run failover

อาการ: ต้องตรวจ failover state ของ HA pair และบังคับให้ device ใด device หนึ่งเป็น standby

---

## 1. ตรวจ failover status

คำค้น: f5 show sys failover, f5 bigip failover status

อาการ: ตรวจ failover state ของ BIG-IP system

คำสั่งตรวจ:
```
show sys failover
```
อ่านผล: แสดง failover state ของระบบ (active, standby, offline, forced_offline) และระยะเวลาที่อยู่ใน state นั้น

ที่มา: [sys_failover.html (tmsh ref v17.0.0)](https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/sys/sys_failover.html)

อ้างอิง:
- "failover - Configures failover for a BIG-IP(r) unit in a redundant system configuration." — tmsh reference v17.0.0 (sys_failover.html, NAME section)
- "show failover — Displays the failover state of the BIG-IP system (active, standby, offline, forced_offline) and how long it has been in that state." — tmsh reference v17.0.0 (sys_failover.html, EXAMPLES section)

---

## 2. วิธีแก้: บังคับ failover

คำค้น: f5 run failover standby, f5 force standby bigip

อาการ: บังคับให้ active unit ไปเป็น standby และให้ standby unit กลายเป็น active

คำสั่งตรวจ:
```
show sys failover
```

วิธีแก้: `run sys failover standby`

หมายเหตุ: รูปที่เขียนในหน้าคือ `run failover standby` (ตัด module sys) คำสั่ง tmsh เต็มคือ `run sys failover standby`

อ่านผล: ทำให้ active unit หรือ cluster ไปอยู่ใน standby state และบังคับให้ unit หรือ cluster อีกตัวในระบบ redundant กลายเป็น active

ที่มา: [sys_failover.html (tmsh ref v17.0.0)](https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/sys/sys_failover.html)

อ้างอิง:
- "run failover standby — Causes the active unit or cluster to go into the standby state forcing the other unit or cluster in the redundant system configuration to become active." — tmsh reference v17.0.0 (sys_failover.html, EXAMPLES section)
- "standby - Specifies that the active unit or cluster fails over to a Standby state, causing the standby unit or cluster to become Active." — tmsh reference v17.0.0 (sys_failover.html, OPTIONS section)

---

หมายเหตุ:
- ไม่พบที่มาว่าควรสั่ง `run sys failover standby` เมื่อใดระหว่างอัปเกรด 17.5 (ตรวจแล้ว: sys_failover.html tmsh ref v17.0.0)
- ไม่พบที่มาของเมนู GUI "Force to Standby" ในหน้าที่ตรวจแล้ว (sys_failover.html) ยังไม่ได้ตรวจหน้าอื่น
