---
id: f5-bigip-17-snmp
title: F5 BIG-IP 17.x — SNMP trap, snmpd และข้อความที่เกี่ยวข้อง
families: f5_tmsh
triggers: f5 snmp, snmp trap, snmpd, snmpd.log, daemon_heartbeat snmpd, sys-location, control character
versions: BIG-IP 17.5.x
sources: https://my.f5.com/manage/s/article/K11127, https://my.f5.com/manage/s/article/K12778420, https://my.f5.com/manage/s/article/K34432004, https://my.f5.com/manage/s/article/K000164072, https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/sys/sys_snmp.html
---

# F5 BIG-IP 17.x — SNMP trap, snmpd และข้อความที่เกี่ยวข้อง

---

## ข้อความใน log ที่เกี่ยวกับ snmpd

คำค้น: f5 snmpd disabled enabled, f5 daemon_heartbeat snmpd, f5 snmpd.log ใหญ่, f5 log disk 80%

ที่มา: K12778420 (https://my.f5.com/manage/s/article/K12778420) Applies to BIG-IP LTM มี 17.5.0, 17.5.X และ K34432004 (https://my.f5.com/manage/s/article/K34432004) Applies to BIG-IP LTM มี 17.5.1, 17.5.0, 17.5.X

"While updating SNMP trap destinations, you may see the following message in /var/log/ltm" — K12778420, Description
"HA daemon_heartbeat % snmpd disabled" — K12778420
"HA daemon_heartbeat % snmpd enabled" — K12778420

"When changes are made to SNMP configuration, the service is restarted." — K12778420, Cause

"alertd[PID]: 01100048:0: Log disk usage still higher than 80% after logrotate and 24 times log deletion" — K34432004, Description
"The /var/log/snmpd.log file is not being rotated" — K34432004, Cause

หมายเหตุ: วิธีแก้ใน K34432004 (modify sys log-rotate) เป็นการเปลี่ยนค่า ไม่ใส่ในบล็อกตรวจ เรื่องพื้นที่ดิสก์ดู playbook f5-bigip-17-disk-space

คำสั่งตรวจ:
```
show sys log ltm
```

---

## ทดสอบ SNMP trap และการอัปเกรดที่ SNMP config มี control character

คำค้น: f5 test snmp trap, f5 snmp control character, f5 configuration fails to load snmp

ที่มา: K11127 (https://my.f5.com/manage/s/article/K11127) Applies to BIG-IP LTM มี 17.5.1, 17.5.0, 17.5.X และ K000164072 (https://my.f5.com/manage/s/article/K000164072) Applies to BIG-IP LTM มีเฉพาะ 17.5.1

"You want to generate test messages to test SNMP traps on the BIG-IP system." — K11127, Topic

"The configuration load failed during the upgrade, which left the device INOPERATIVE." — K000164072, Cause

ตรวจใน GUI: ไม่พบที่มาของเมนู GUI สำหรับดูค่า SNMP ในต้นฉบับที่อ่าน

หมายเหตุความปลอดภัย: ไม่ใส่คำสั่งแสดงค่า SNMP (เช่น list sys snmp หรือ show running-config sys snmp) ในบล็อกตรวจ เพราะหน้า tmsh sys_snmp ไม่ระบุว่าผลลัพธ์จะแสดงชื่อ community หรือรหัสของ SNMPv3 หรือไม่ ห้ามเผยค่าเหล่านี้ และตัวอย่างใน K77406702 ที่มีค่าของ community ไม่ได้คัดมา

---

ไม่พบที่มา
- ตรวจ K11127 แล้ว วิธีทดสอบเป็นคำสั่ง bash (snmptrap, logger) ไม่ใส่ในบล็อกตรวจ
- ตรวจ K000164072 แล้ว วิธีตรวจเป็นคำสั่ง bash (grep, perl) ไม่ใส่ในบล็อกตรวจ
- ไม่พบที่มา: คำสั่ง show/list ที่ยืนยันว่าไม่แสดงชื่อ community หรือรหัสของ SNMPv3
- ไม่พบที่มา: วิธีตรวจสถานะ snmpd ด้วยคำสั่ง show
