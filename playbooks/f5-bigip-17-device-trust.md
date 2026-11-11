---
id: f5-bigip-17-device-trust
title: F5 BIG-IP 17.x — ตรวจ Device Trust
families: f5_tmsh
triggers: device trust, trust domain, cm trust-domain, device trust ไม่ทำงาน, HA trust
versions: BIG-IP 17.5.x
sources: https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/cm/cm_trust-domain.html
---

# F5 BIG-IP 17.x — ตรวจ Device Trust

---

## ตรวจ trust domain ของ Device Trust

คำค้น: f5 device trust, f5 trust domain, f5 show running-config cm trust-domain, f5 device trust status, device trust มีปัญหา, trust พัง, trust หลุด, device trust ไม่ขึ้น, ตรวจ trust, คู่ ha ไม่เห็นกัน

ที่มา: tmsh reference v17.0.0 (https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/cm/cm_trust-domain.html)

"You can use the trust-domain component to manage the behavior of objects during fail over." — cm_trust-domain.html, DESCRIPTION section

"show running-config trust-domain" — cm_trust-domain.html, DISPLAY section
"show running-config trust-domain [ [ [name] | [glob] | [regex] ] ... ]" — cm_trust-domain.html, DISPLAY section

"Displays the status of the trust domain." — cm_trust-domain.html, OPTIONS section, status

"Displays the device group associated with the trust domain." — cm_trust-domain.html, OPTIONS section, trust-group

หมายเหตุละ module: tmsh reference เขียนรูป "show running-config trust-domain" โดยละ module คำสั่งเต็มที่ใช้ตรวจคือ show running-config cm trust-domain status และ show running-config cm trust-domain trust-group

หมายเหตุความระวัง: หน้า tmsh มี option ca-key ซึ่งคัดประโยคได้ว่า "Displays the certificate authority device trust key. This key only displays for certificate authorities." จึงไม่ใส่คำสั่งแสดงทั้ง object (เช่น list cm trust-domain) ในบล็อกคำสั่งตรวจ ใช้เฉพาะรูปที่ระบุ option

คำสั่งตรวจ:
```
show running-config cm trust-domain status
show running-config cm trust-domain trust-group
```

คำสั่ง list cm device และ show cm sync-status ตรวจความสัมพันธ์ของอุปกรณ์ใน HA ดูที่ playbook f5-bigip-17-ha-config-sync

---

ไม่พบที่มา
- ตรวจ cm_trust-domain.html แล้วไม่พบ: ค่าที่เป็นไปได้ของ status และความหมาย
- ตรวจ cm_trust-domain.html แล้วไม่พบ: อาการเมื่อ Device Trust เสียและวิธีแก้
- ตรวจ cm_trust-domain.html แล้วไม่พบ: วันหมดอายุของใบรับรอง Device Trust (K-article K000151455 ไม่ได้ตรวจ)
