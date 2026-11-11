---
id: f5-bigip-17-virtual-server-not-responding
title: F5 BIG-IP 17.x — Virtual Server ไม่ตอบ
families: f5_tmsh
triggers: f5 virtual server not responding, f5 virtual server ไม่ตอบ, f5 virtual server offline, f5 virtual server unavailable
versions: BIG-IP 17.5.x
sources: https://my.f5.com/manage/s/article/K93017176, https://my.f5.com/manage/s/article/K55185917, https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/ltm/ltm_virtual.html
---

# F5 BIG-IP 17.x — Virtual Server ไม่ตอบ

## ตรวจสถานะและการตั้งค่า virtual server

คำค้น: f5 virtual server status, f5 show ltm virtual, f5 list ltm virtual, f5 State, f5 VLAN Disabled on, f5 Source Address, f5 Connection Rate Limit, virtual server ไม่ตอบ, vs ไม่ตอบ, ไม่ตอบ, เข้าเว็บไม่ได้, เข้า vip ไม่ได้, vs ไม่ทำงาน

ที่มา: https://my.f5.com/manage/s/article/K93017176 (General Properties, Configuration), https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/ltm/ltm_virtual.html

"Specifies whether the virtual server and its resources are available for load balancing." — K93017176, General Properties > State

"Disabled on: Specifies that the virtual server is disabled on the VLANs and tunnels specified in the Selected list." — K93017176, Configuration > VLAN and Tunnel Traffic

"The virtual server accepts clients only from one of these IP addresses." — K93017176, General Properties > Source Address

"When the number of connections-per-second reaches the limit for a given virtual server, the system drops (UDP) or resets (TCP) additional connection requests." — K93017176, Configuration > Connection Rate Limit

tmsh reference `ltm_virtual.html` DISPLAY section เขียนชื่อคำสั่งแบบละ module: `list virtual` และ `show virtual` (คำสั่งเต็ม: `list ltm virtual`, `show ltm virtual`)

"Displays statistics and status for the virtual named myV4." — ltm_virtual.html, EXAMPLES section

คำสั่งตรวจ:
```
list ltm virtual
show ltm virtual
```

---

## การตอบสนองเมื่อ virtual server offline และชนิด Reject

คำค้น: f5 virtual server offline, f5 virtual server unavailable, f5 service down immediate action, f5 reject virtual server, f5 show ltm virtual all-properties, vs offline, vs ล่ม, pool ล่มหมด, ตอบ reset, ถูก reset

ที่มา: https://my.f5.com/manage/s/article/K93017176 (Configuration), https://my.f5.com/manage/s/article/K55185917, https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/ltm/ltm_virtual.html

"Specifies the immediate action the BIG-IP system should respond with upon the receipt of the initial client's SYN packet, if the availability status of the virtual server is Offline or Unavailable." — K93017176, Configuration > Immediate Action On Service Down

"This is supported for the virtual server of Standard type and TCP protocol." — K93017176, Configuration > Immediate Action On Service Down

"A Reject virtual server rejects any traffic destined for the virtual server IP address." — K55185917, virtual server type table > Reject

"Displays statistics and status for the virtual named myV4." — ltm_virtual.html, EXAMPLES section

tmsh reference `ltm_virtual.html` EXAMPLES section แสดงตัวอย่าง: `show virtual myV4 all-properties` (คำสั่งเต็ม: `show ltm virtual myV4 all-properties`)

คำสั่งตรวจ:
```
show ltm virtual all-properties
```

ไม่พบที่มา — ตรวจ K93017176, K55185917, ltm_virtual.html แล้ว:
ความหมายของสถานะ availability (Offline กับ Unavailable) — ตรวจแล้วไม่พบคำจำกัดความ
วิธีแก้เมื่อ virtual server ไม่ตอบ — ตรวจแล้วไม่พบขั้นตอนการแก้ไข
การตรวจ pool member และ monitor — อ้างถึง playbook f5-bigip-17-ltm-monitor-troubleshooting
ขั้นตอนใน GUI — ตรวจแล้วไม่พบแหล่งที่มา
