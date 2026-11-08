---
id: f5-bigip-icap-kaspersky
title: F5 BIG-IP 17.5.x — ICAP ไป Kaspersky Antivirus
families: f5_tmsh
triggers: f5 bigip icap kaspersky, f5 bigip icap virus detected, f5 bigicap icap uri reqmod, f5 bigicap virus header name, f5 bigicap inspect file uploads, f5 bigicap guarantee enforcement icap down
versions: BIG-IP 17.5.x (17.5.1.8–17.5.1.11)
sources: https://techdocs.f5.com/en-us/bigip-17-5-0/big-ip-asm-implementations/configuring-general-asm-system-options.html,https://techdocs.f5.com/en-us/bigip-17-5-0/big-ip-asm-implementations/securing-smtp-traffic.html,https://techdocs.f5.com/en-us/bigip-17-5-0/big-ip-asm-implementations/logging-application-security-events.html
---

# F5 BIG-IP 17.5.x — ICAP ไป Kaspersky Antivirus

คำค้น: f5 bigip icap kaspersky, f5 bigip icap virus detected, f5 bigicap icap uri reqmod, f5 bigicap virus header name, f5 bigicap inspect file uploads, f5 bigicap guarantee enforcement icap down
อาการ: ICAP เชื่อมต่อ Kaspersky ไม่ผ่าน, virus detection ไม่ทำงาน, หรือ ICAP server ล่มแล้ว traffic สะดุด

อ้างอิง playbook อื่น:
- `f5-bigip-17-security-upgrade-assessment-ha` -> อัปเกรด HA ทั่วไป
- `f5-bigip-17-5-advanced-waf-upgrade-precautions` -> Cookie, Provisioning, Device Group หลัง upgrade
- `f5-bigip-asm-false-positive-staging` -> ASM False Positive / Staging / Learning
- `f5-bigip-ucs-restore-master-key` -> UCS Restore และ Master Key

---

## 1 ตรวจสอบ ICAP เชื่อมต่อ Kaspersky ไม่ผ่าน

คำค้น: f5 bigip icap kaspersky connection timeout, f5 bigip icap server host name port
อาการ: ICAP connection timeout, file upload ไม่ผ่าน, Virus Detected violation — เกิดจาก Kaspersky ICAP server unreachable, port ผิด, DNS resolution ผิด, หรือ ICAP URI ผิด

ตรวจใน GUI:
- Security > Application Security > Integrated Services > Anti-Virus Protection — ดู Server Host Name / IP และ Port

ตรวจใน log:
- (bash) `cat /var/log/asm | grep -i "icap\|virus\|antivirus"` — ASM log (**ต้องเปิด logging ก่อน — ค่าเริ่มต้นปิด; ดูวิธีเปิดใน [Logging Application Security Events (17.5)](https://techdocs.f5.com/en-us/bigip-17-5-0/big-ip-asm-implementations/logging-application-security-events.html)**)

วิธีแก้:
- ตรวจสอบ network connectivity ไปยัง Kaspersky ICAP server
- ตรวจสอบ port (default 1344)
- ตรวจสอบ DNS ถ้าใช้ hostname
- ตรวจสอบ ICAP URI: ต้องตรงกับค่าบน Kaspersky ICAP server
- ตรวจสอบ virus_header_name: ต้องตรงกับค่าบน Kaspersky ICAP server

ที่มา: [Configuring General ASM System Options (17.5)](https://techdocs.f5.com/en-us/bigip-17-5-0/big-ip-asm-implementations/configuring-general-asm-system-options.html), [Securing SMTP Traffic (17.5)](https://techdocs.f5.com/en-us/bigip-17-5-0/big-ip-asm-implementations/securing-smtp-traffic.html)

อ้างอิง:
- "Before you can incorporate antivirus protection, you need to have an ICAP server setup in your network."
- "The default value is 1344."
- "ASM was tested with McAfee VirusScan, Trend Micro InterScan, Symantec Protection Engine, and Kaspersky Antivirus products, and may work with others."
- "The ICAP server examines the requests for viruses and, if the ICAP server detects a virus, it notifies ASM, which then issues the Virus Detected violation."

---

## 2 ตรวจสอบ ICAP URI และ virus_header_name

คำค้น: f5 bigip icap uri virus header name icap server settings, f5 bigicap system variables icap_uri
อาการ: ICAP ทำงานไม่ถูกต้อง, virus detection ไม่ผ่าน — เกิดจาก ICAP URI หรือ virus_header_name ไม่ตรงกับ Kaspersky config

ตรวจใน GUI:
- Security > Options > Protocol Security > Advanced Configuration — ดู System Variables area
- ตรวจสอบ icap_uri และ virus_header_name

วิธีแก้:
- ตรวจสอบค่า ICAP URI และ virus_header_name บน Kaspersky ICAP server
- ตั้งค่าบน BIG-IP ให้ตรงกับค่าบน Kaspersky ICAP server
- Apply หลังแก้ไข

ที่มา: [Securing SMTP Traffic (17.5)](https://techdocs.f5.com/en-us/bigip-17-5-0/big-ip-asm-implementations/securing-smtp-traffic.html)

อ้างอิง:
- "In the System Variables area, ensure that the values for the icap_uri (URI for the ICAP service), and virus_header_name (header name used) internal parameters correspond to your ICAP server's settings."

---

## 3 เปิด Inspect File Uploads สำหรับ SOAP

คำค้น: f5 bigip inspect file uploads http requests soap attachments xml profile, f5 bigicap antivirus protection enabled disabled list
อาการ: ไฟล์ที่ถูก upload ไม่ถูก scan โดย Kaspersky, Virus Detected ไม่ trigger — เกิดจาก "Inspect file uploads within HTTP requests" ไม่ enable หรือ XML profile ไม่ enable สำหรับ SOAP

ตรวจใน GUI:
- Security > Application Security > Integrated Services > Anti-Virus Protection — ตรวจสอบ checkbox "Inspect file uploads within HTTP requests"
- ตรวจสอบ XML Profiles ใน Antivirus Protection Enabled list

วิธีแก้:
- Enable "Inspect file uploads within HTTP requests" checkbox
- สำหรับ SOAP: move XML profiles จาก Disabled list ไป Enabled list
- Apply policy หลังแก้ไข

ที่มา: [Configuring General ASM System Options (17.5)](https://techdocs.f5.com/en-us/bigip-17-5-0/big-ip-asm-implementations/configuring-general-asm-system-options.html)

อ้างอิง:
- "To have the external ICAP server inspect file uploads for viruses before releasing the content to the web server, select the Inspect file uploads within HTTP requests check box."
- "To perform anti-virus scanning on SOAP attachments, if the security policy includes one or more XML profiles, in the XML Profiles setting, move the profiles from the Antivirus Protection Disabled list to the Antivirus Protection Enabled list."

---

## 4 ICAP Server Down Guarantee Enforcement

คำค้น: f5 bigip icap server down guarantee enforcement antivirus, f5 bigicap virus checking slow down
อาการ: Kaspersky server down, traffic สะดุดหรือไม่ — ICAP server unreachable, ASM block หรือ bypass traffic

ตรวจใน GUI:
- Security > Application Security > Integrated Services > Anti-Virus Protection — ดู "Guarantee Enforcement" setting

ตรวจใน log:
- (bash) `cat /var/log/asm | grep -i "icap\|virus\|antivirus"` — ASM log (**ต้องเปิด logging ก่อน — ค่าเริ่มต้นปิด; ดูวิธีเปิดใน [Logging Application Security Events (17.5)](https://techdocs.f5.com/en-us/bigip-17-5-0/big-ip-asm-implementations/logging-application-security-events.html)**)

วิธีแก้:
- ตรวจสอบ setting "Guarantee Enforcement" ใน Anti-Virus Protection screen
- **เอกสารไม่ระบุ** ว่า ICAP server down แล้ว ASM block หรือ bypass — ต้องตรวจสอบ setting "Guarantee Enforcement" ด้วยตนเอง
- ถ้า ICAP server down → troubleshooting Kaspersky side

ที่มา: [Configuring General ASM System Options (17.5)](https://techdocs.f5.com/en-us/bigip-17-5-0/big-ip-asm-implementations/configuring-general-asm-system-options.html)

อ้างอิง:
- "If you want to perform virus checking even if it may slow down the web application, select the Guarantee Enforcement check box."
