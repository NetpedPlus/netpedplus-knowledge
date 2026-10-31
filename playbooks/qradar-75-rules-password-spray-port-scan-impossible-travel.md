---
id: qradar-75-rules-password-spray-port-scan-impossible-travel
title: QRadar 7.5 Offense Rules: Password Spray, Port Scan, Impossible Travel
families:
triggers: qradar password spray, qradar port scan, qradar impossible travel, qradar offense rule, qradar building block, qradar reference table, qradar AQL, qradar custom rule, qradar threshold rule, qradar behavioral rule
versions: QRadar 7.5.x
sources: https://www.ibm.com/docs/en/SS42VS_7.5/pdf/b_qradar_users_guide.pdf, https://www.ibm.com/docs/en/SS42VS_7.5/pdf/b_qradar_tuning_guide.pdf, https://www.ibm.com/docs/en/SS42VS_7.5/pdf/b_siem_deployment.pdf, https://www.ibm.com/docs/hr/qradar-on-cloud?topic=language-aql-data-retrieval-functions, https://sra.io/blog/impossible-travel/
---

# QRadar 7.5 Offense Rules: Password Spray, Port Scan, Impossible Travel

คำค้น: qradar password spray, qradar port scan, qradar impossible travel, qradar offense rule, qradar building block, qradar reference table, qradar AQL
อาการ: ต้องสร้าง offense rule สำหรับตรวจจับ password spray, port scan, และ impossible travel บน QRadar 7.5.x

---

## 1. แนวทางการสร้าง Offense Rule ใน QRadar 7.5

คำค้น: qradar custom rule, qradar rule creation wizard, qradar building block, qradar CRE
อาการ: ต้องเข้าใจโครงสร้างการสร้าง rule ใน QRadar
คำสั่งตรวจ:
```
ตรวจใน GUI: Offenses tab > Rules > New Event Rule / New Flow Rule / New Common Rule / New Offense Rule
```
อ่านผล:
- QRadar มี rule 4 ประเภท: Event Rule (ตรวจสอบ event จาก log source), Flow Rule (ตรวจสอบ flow data), Common Rule (ตรวจสอบทั้ง event และ flow), Offense Rule (ตรวจสอบ parameter ของ offense)
- Building Block (BB) เป็น collection ของ test ที่ไม่มี action — ใช้รวมกลุ่ม IP addresses, privileged user names, หรือ event collections เพื่อ reuse ใน rule ต่างๆ
- CRE (Custom Rules Engine) เป็น component ที่ process events เทียบกับ rule ที่กำหนด แล้ว generate offense
- ก่อนสร้าง rule ต้องมี permission: **Offenses > Maintain Custom Rules**
ที่มา: [QRadar 7.5 User Guide (Rules)](https://www.ibm.com/docs/en/SS42VS_7.5/pdf/b_qradar_users_guide.pdf), [QRadar Tuning Guide — Rules and Building Blocks](https://www.ibm.com/docs/en/SS42VS_7.5/pdf/b_qradar_tuning_guide.pdf), [QRadar Architecture — Custom Rules Engine](https://www.ibm.com/docs/en/SS42VS_7.5/pdf/b_siem_deployment.pdf)
วิธีแก้:
- สร้าง rule: ไปที่ Offenses tab > Rules > จาก Actions list เลือก rule type (New Event Rule / New Flow Rule / New Common Rule / New Offense Rule) > คลิก Next
- ใน Rule Test Stack Editor: พิมพ์ชื่อ rule, เลือก Local หรือ Global, แล้วเพิ่ม test ด้วย AND/OR logic
- เพิ่ม building block: ที่ Rules > Display list เลือก Building Blocks > Double-click BB ที่ต้องการ edit > อัพเดทข้อมูล > คลิก Finish
- สร้าง building block ใหม่: จาก rule wizard คลิก "Export as Building Block" แล้วพิมพ์ unique name

---

## 2. Password Spray Detection

คำค้น: qradar password spray, qradar authentication failure, qradar threshold rule, qradar reference set building block
อาการ: ต้องตรวจจับ password spray — attacker ซ้อม login หลาย username จาก IP เดียวกัน
คำสั่งตรวจ:
```
ตรวจใน GUI: Offenses tab > Rules > Building Blocks > BB:CategoryDefinition: Authentication Failures
ตรวจใน GUI: Offenses tab > Rules > Building Blocks > BB:CategoryDefinition: Authentication Success
```
อ่านผล:
- BB:CategoryDefinition: Authentication Failures คือ building block ที่รวม event category ของ authentication failures ทั้งหมด
- BB:CategoryDefinition: Authentication Success คือ building block ที่รวม event category ของ authentication successes ทั้งหมด
ที่มา: [QRadar 7.5 User Guide (Rules)](https://www.ibm.com/docs/en/SS42VS_7.5/pdf/b_qradar_users_guide.pdf), แนวทาง rule มาจาก [Reddit r/QRadar (บุคคลที่สาม)](https://www.reddit.com/r/QRadar/comments/f1wduu/password_spray_detection/), [QRadar User Guide (Rules)](https://www.ibm.com/docs/en/SS42VS_7.5/pdf/b_qradar_users_guide.pdf)
วิธีแก้:
- สร้าง Building Block (Response action: adds to reference set and dispatches event): "and when an event matches any of the following BB:CategoryDefinition: Authentication Failures" และ "when at least <threshold> events are seen with the same Source IP and different Username in <time_window> minutes" — ค่าตั้งต้นจากแหล่งบุคคลที่สาม: 25 events ใน 1 นาที (ปรับตามจำนวนผู้ใช้จริง ดู log สักระยะก่อน)
- สร้าง Rule (Event Rule — Password Spray Attempt — dispatches offense): "and when an event matches any of the following BB:CategoryDefinition: Authentication Failures" และ "when at least <threshold> events are seen with the same Source IP and different Username in <time_window> minutes" และ "and when the source IP is NOT one of the following <excluded_subnets>"
- สร้าง Rule (Event Rule — Successful Password Spray): "and when any of Source IP are contained in any of [Reference Set ที่สร้างจาก Building Block ของ Attempt Rule]" และ "and when an event matches any of the following BB:CategoryDefinition: Authentication Success"
- สร้าง Rule (Event Rule — Brute Force Attempt — same pattern, ใช้ "same Username" แทน "different Username" เพื่อแยกจาก password spray)
- ตั้งค่า response: Dispatch new event + Ensure the detected event is part of an offense

---

## 3. Port Scan Detection

คำค้น: qradar port scan, qradar superflow, qradar recon, qradar flow rule type C, qradar recon building block
อาการ: ต้องตรวจจับ port scan — attacker scan หลาย port หรือหลาย host จาก IP เดียวกัน
คำสั่งตรวจ:
```
ตรวจใน GUI: Offenses tab > Rules > Building Blocks > BB:Recon Detected
ตรวจใน GUI: Offenses tab > Rules > Building Blocks > BB:HostDefinition
```
อ่านผล:
- QRadar มี rule / building block กลุ่ม Recon มาให้แล้ว (ค้นด้วยคำว่า Recon ในรายการ rule) ชื่อและค่าเกณฑ์ให้ดูจากเครื่องจริง เพราะต่างกันตามเวอร์ชันและ content pack
- Type C Superflows คือ port scan detection — aggregate ของ non-ICMP flows ที่มี source IP เดียวกัน, destination IP เดียวกัน แต่หลาย ports
ที่มา: [QRadar Admin Guide — Default Recon Rules](https://www.ibm.com/docs/en/SS42VS_7.5/pdf/b_qradar_admin_guide.pdf), [QRadar User Guide — Superflow Type C: Port Scan](https://www.ibm.com/docs/en/SS42VS_7.5/pdf/b_qradar_users_guide.pdf), [QRadar Tuning Guide](https://www.ibm.com/docs/en/SS42VS_7.5/pdf/b_qradar_tuning_guide.pdf)
วิธีแก้:
- ตรวจสอบ built-in recon rules: Offenses tab > Rules > จาก Display list เลือก "All Rules" แล้วค้นหา "Recon" — default rules ทำงานอยู่แล้ว
- สร้าง custom Port Scan Rule (Flow Rule): ใช้ test แบบ "when at least <threshold> flows are seen with the same Source IP and different Destination Port in <time_window> minutes"
- สร้าง custom Host Scan Rule (Flow Rule): ใช้ test แบบ "when at least <threshold> flows are seen with the same Source IP and different Destination IP in <time_window> minutes"
- ถ้าไม่มี flow (ไม่มี QFlow / NetFlow) ใช้ Event Rule กับ log deny ของ firewall แทนด้วย test รูปแบบเดียวกัน
- สร้าง Building Block สำหรับ authorized outbound ports: "and when the destination port is one of the following" (ports ที่อนุญาต outbound) เพื่อลด false positive
- สร้าง Building Block สำหรับ trusted IPs: เพิ่ม trusted management IPs เข้า exclusion list
- ตั้งค่า response: Dispatch new event + Ensure the detected event is part of an offense

---

## 4. Impossible Travel Detection

คำค้น: qradar impossible travel, qradar reference table, qradar AQL, qradar GEO function, qradar risk-based authentication
อาการ: ต้องตรวจจับ impossible travel — user login จาก IP ที่มี location ห่างกันเกินไปในเวลาสั้นๆ (ไม่เดินทางทัน)
คำสั่งตรวจ:
```
ตรวจใน GUI: Admin tab > Reference Data Management (ดูว่ามี reference table user-ip-date และมีข้อมูลเพิ่มขึ้นหลังมีคน login)
```
อ่านผล:
- QRadar ไม่มี built-in impossible travel rule — ต้องสร้าง custom rule โดยใช้ reference table + AQL query
- AQL มีฟังก์ชัน GEO::DISTANCE(sourceip, ip_address) สำหรับคำนวณระยะทางระหว่าง IP addresses
- AQL มี REFERENCETABLE(table_name, column_name, key) สำหรับดึงข้อมูลจาก reference table
- ต้องสร้าง reference table แบบ key: username (ALNIC), ip (IP), date (DATE)
ที่มา: [Impossible Travel Detection (SRA blog, บุคคลที่สาม)](https://sra.io/blog/impossible-travel/), [AQL Data Retrieval Functions — REFERENCETABLE](https://www.ibm.com/docs/hr/qradar-on-cloud?topic=language-aql-data-retrieval-functions)
วิธีแก้:
- สร้าง Reference Table: ใช้ QRadar API `POST /reference_data/tables` ด้วย key_name_types: `[{"element_type": "ALNIC","key_name": "usernameKey"}, {"element_type": "IP","key_name": "ipKey"}, {"element_type": "DATE","key_name": "dateKey"}]` — ตั้งชื่อ table เช่น "user-ip-date"
- สร้าง Rule 1 (Event Rule — Populate Reference Table): กรองเฉพาะ VPN/remote access login events ที่ successful — "and when the event QID is one of the following QIDs" (VPN login QID) และ "Add to Reference Data" → เลือก table "user-ip-date" → map usernameKey, ipKey, dateKey → rule นี้จะเก็บ IP address ของแต่ละ user ทุกครั้งที่ login
- สร้าง Rule 2 (Event Rule — Detect Impossible Travel): "and when the event matches this AQL Query" → `GEO::DISTANCE(sourceip, REFERENCETABLE('user-ip-date','ipKey',username))/DOUBLE(DOUBLE(starttime-REFERENCETABLE('user-ip-date','dateKey',username))/3600000) > 200.0 and GEO::DISTANCE(sourceip, REFERENCETABLE('user-ip-date','ipKey',username)) > 0` — ค่า speed threshold (km/h) ปรับตามนโยบายองค์กร (200 = รถยนต์/รถไฟ, 600 = เครื่องบิน)
- สร้าง Rule 3 (ไม่บังคับ, login พร้อมกันจากหลายที่): test "when at least 2 events are seen with the same Username and different Source IP in <time_window> minutes"
- ตั้งค่า response: Dispatch new event + Ensure the detected event is part of an offense + Index by Username

---

## 5. ตรวจสอบและ Tune Rules

คำค้น: qradar rule testing, qradar false positive tuning, qradar rule threshold, qradar building block edit
อาการ: ต้องตรวจว่า rule ทำงานถูกต้อง และ tune false positive
คำสั่งตรวจ:
```
ตรวจใน GUI: Log Activity tab > Actions > Historical Correlation (สร้าง profile เลือก rule ที่จะทดสอบกับ event ย้อนหลัง)
ตรวจใน GUI: Log Activity tab > เลือก event > ปุ่ม False Positive
```
อ่านผล:
- Historical correlation รัน rule กับข้อมูลย้อนหลังตามช่วงเวลาที่เลือก ได้ offense แยกจากของจริง ใช้ดูว่า rule จับเกินหรือขาด
- ปุ่ม False Positive ใน Log Activity / Network Activity สร้างการ tune ให้ event / flow แบบนั้นไม่ทำให้เกิด offense อีก
- Building blocks สามารถ edit ได้ตลอดเวลาเพื่อปรับ threshold และ exclusion lists
ที่มา: [QRadar Tuning Guide — Rule Testing](https://www.ibm.com/docs/en/SS42VS_7.5/pdf/b_qradar_tuning_guide.pdf), [QRadar User Guide — Tuning False Positives](https://www.ibm.com/docs/en/SS42VS_7.5/pdf/b_qradar_users_guide.pdf)
วิธีแก้:
- ทดสอบ rule กับข้อมูลย้อนหลัง: Historical Correlation (ด้านบน) ก่อนเปิดใช้จริง
- Tune false positive: Log Activity tab > เลือก event > ปุ่ม False Positive
- แก้ building block: Offenses tab > Rules > Display list เลือก Building Blocks > Double-click BB > อัพเดท threshold/exclusion lists > คลิก Finish
- ใช้ Threshold Rule / Behavioral Rule / Anomaly Rule สำหรับ advanced detection — ต้อง save search criteria ก่อนจึงจะ enable options เหล่านี้ได้
- ตั้งค่า Response Limiter ใน rule responses เพื่อจำกัด frequency ของ offense generation

---

## 6. ระวังเรื่องสำคัญ

คำค้น: qradar rule pitfalls, qradar reference data, qradar AQL functions, qradar geo distance
อาการ: ต้องระวังข้อผิดพลาดทั่วไปเมื่อสร้าง QRadar rules
คำสั่งตรวจ:
```
ตรวจใน GUI: Log Activity tab > Advanced Search (รัน AQL ที่จะใส่ใน rule ก่อน ดูว่าได้ผลตามคาด)
```
อ่านผล:
- AQL ที่ error หรือไม่คืนผลใน Advanced Search ก็จะใช้ใน rule ไม่ได้เช่นกัน
ที่มา: [AQL Data Retrieval Functions (IBM)](https://www.ibm.com/docs/hr/qradar-on-cloud?topic=language-aql-data-retrieval-functions), [QRadar Tuning Guide](https://www.ibm.com/docs/en/SS42VS_7.5/pdf/b_qradar_tuning_guide.pdf)
วิธีแก้:
- AQL ที่ใส่ใน rule ให้ทดสอบใน Log Activity > Advanced Search ก่อน
- GEO::DISTANCE ใช้ฐานข้อมูลตำแหน่ง IP ของ QRadar (อัปเดตผ่าน auto update) IP ภายใน / VPN / proxy / cloud ให้ตำแหน่งผิดได้ ต้องตัด IP เหล่านี้ออกก่อน ไม่งั้น false positive เยอะ
- Reference table ที่สร้างผ่าน API ต้องมี key type ที่ถูกต้อง (ALNIC สำหรับ username, IP สำหรับ IP address, DATE สำหรับ timestamp)
- ไม่แนะนำให้สร้าง rule ที่ match ทุก authentication failure (too broad) — ต้อง set threshold + time window + exclusion list
- Port scan detection ผ่าน flow อาจมี false positive จาก legitimate services (เช่น DNS queries ไปหลาย ports, load balancer health checks) — ต้อง tune building blocks
- Password spray rule ต้องแยกจาก brute force: password spray = different usernames จาก source IP เดียว, brute force = same username หลายครั้งจาก source IP เดียว
