---
id: f5-bigip-icap-kaspersky
title: F5 BIG-IP 17.5.x — ICAP ไป Kaspersky Antivirus
families: f5_tmsh
triggers: f5 bigip icap kaspersky, f5 bigip icap virus detected, f5 bigicap inspect file uploads, f5 bigicap guarantee enforcement, f5 bigicap smtp virus
versions: BIG-IP 17.5.x
sources: https://techdocs.f5.com/en-us/bigip-17-5-0/big-ip-asm-implementations/configuring-general-asm-system-options.html,https://techdocs.f5.com/en-us/bigip-17-5-0/big-ip-asm-implementations/securing-smtp-traffic.html
---

# F5 BIG-IP 17.5.x — ICAP ไป Kaspersky Antivirus

คำค้น: f5 bigip icap kaspersky, f5 bigip icap virus detected, f5 bigicap inspect file uploads, f5 bigicap guarantee enforcement, f5 bigicap smtp virus
อาการ: ICAP เชื่อมต่อ Kaspersky ไม่ผ่าน, virus detection ไม่ทำงาน

อ้างอิง playbook อื่น:
- `f5-bigip-17-security-upgrade-assessment-ha` -> อัปเกรด HA ทั่วไป
- `f5-bigip-17-5-advanced-waf-upgrade-precautions` -> Cookie, Provisioning, Device Group หลัง upgrade
- `f5-bigip-asm-false-positive-staging` -> ASM False Positive / Staging / Learning
- `f5-bigip-ucs-restore-master-key` -> UCS Restore และ Master Key

---

## 1 ตรวจสอบ ICAP เชื่อมต่อ Kaspersky ไม่ผ่าน

คำค้น: f5 bigip icap server host name port, f5 bigicap dns server configure
อาการ: file upload ไม่ผ่าน, Virus Detected violation

ตรวจใน GUI:
- Security > Application Security > Integrated Services > Anti-Virus Protection — ดู Server Host Name / IP และ Port

วิธีแก้:
- ตรวจสอบ port (default 1344)
- **ถ้าใช้ host name**: คุณต้อง configure DNS server ก่อน (System > Configuration > Device > DNS)

ที่มา: [Configuring General ASM System Options (17.5)](https://techdocs.f5.com/en-us/bigip-17-5-0/big-ip-asm-implementations/configuring-general-asm-system-options.html), [Securing SMTP Traffic (17.5)](https://techdocs.f5.com/en-us/bigip-17-5-0/big-ip-asm-implementations/securing-smtp-traffic.html)

อ้างอิง:
- "Before you can incorporate antivirus protection, you need to have an ICAP server setup in your network."
- "The default value is 1344."
- "ASM was tested with McAfee VirusScan, Trend Micro InterScan, Symantec Protection Engine, and Kaspersky Antivirus products, and may work with others."
- "The ICAP server examines the requests for viruses and, if the ICAP server detects a virus, it notifies ASM, which then issues the Virus Detected violation."
- "If you specify the host name, you must first configure a DNS server by selecting System > Configuration > Device > DNS."

---

## 2 ตรวจสอบ ICAP URI และ virus_header_name

คำค้น: f5 bigip icap uri virus header name icap server settings, f5 bigicap smtp virus
อาการ: ICAP ทำงานไม่ถูกต้อง, virus detection ไม่ผ่าน — เกิดจาก ICAP URI หรือ virus_header_name ไม่ตรงกับ Kaspersky config

ตรวจใน GUI:
- Security > Options > Protocol Security > Advanced Configuration — ดู System Variables area
- ตรวจสอบ icap_uri และ virus_header_name

ตารางค่า Kaspersky (จากตารางในหน้า):
- icap_uri = /av/reqmod
- virus_header_name = X-Virus-ID

ตรวจในบริบท SMTP:
- เอกสารเขียนเกี่ยวกับ SMTP: "You can warn or block against email attachments containing a suspected virus."
- เมนู Protocol Security > Advanced Configuration อยู่ในบริบทนี้

วิธีแก้:
- ตรวจสอบค่า ICAP URI และ virus_header_name บน Kaspersky ICAP server
- ตั้งค่าบน BIG-IP ให้ตรงกับค่าบน Kaspersky ICAP server
- Save your changes

ที่มา: [Securing SMTP Traffic (17.5)](https://techdocs.f5.com/en-us/bigip-17-5-0/big-ip-asm-implementations/securing-smtp-traffic.html)

อ้างอิง:
- "In the System Variables area, ensure that the values for the icap_uri (URI for the ICAP service), and virus_header_name (header name used) internal parameters correspond to your ICAP server's settings."
- "By default, the system supports an ICAP server with McAfee anti-virus protection. If your organization uses a different ICAP server, update the parameters and save your changes."
- "You can warn or block against email attachments containing a suspected virus."
- "| **Kaspersky** | /av/reqmod |"
- "| **Kaspersky** | X-Virus-ID |"
