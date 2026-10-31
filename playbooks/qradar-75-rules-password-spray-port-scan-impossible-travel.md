---
id: qradar-75-rules-password-spray-port-scan-impossible-travel
title: QRadar 7.5 Offense Rules — Password Spray, Port Scan, Impossible Travel
families:
triggers: qradar password spray, qradar port scan, qradar impossible travel, qradar offense rule, qradar building block, qradar reference table, qradar AQL, qradar custom rule, qradar threshold rule, qradar behavioral rule
versions: QRadar 7.5.x
sources: https://www.ibm.com/docs/en/SS42VS_7.5/pdf/b_qradar_users_guide.pdf, https://www.ibm.com/docs/en/SS42VS_7.5/pdf/b_qradar_tuning_guide.pdf, https://www.ibm.com/docs/en/SS42VS_7.5/pdf/b_siem_deployment.pdf, https://www.ibm.com/docs/hr/qradar-on-cloud?topic=language-aql-data-retrieval-functions, https://sra.io/blog/impossible-travel/
---

# QRadar 7.5 Offense Rules — Password Spray, Port Scan, Impossible Travel

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
ที่มา: [QRadar User Guide — Rules — FortiOS 7.4.7](https://www.ibm.com/docs/en/SS42VS_7.5/pdf/b_qradar_users_guide.pdf), [QRadar Tuning Guide — Rules and Building Blocks](https://www.ibm.com/docs/en/SS42VS_7.5/pdf/b_qradar_tuning_guide.pdf), [QRadar Architecture — Custom Rules Engine](https://www.ibm.com/docs/en/SS42VS_7.5/pdf/b_siem_deployment.pdf)
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
ที่มา: [Password Spray Detection — Reddit QRadar Community](https://www.reddit.com/r/QRadar/comments/f1wduu/password_spray_detection/), [QRadar User Guide — Rules](https://www.ibm.com/docs/en/SS42VS_7.5/pdf/b_qradar_users_guide.pdf)
วิธีแก้:
- สร้าง Building Block (Response action: adds to reference set and dispatches event): "and when an event matches any of the following BB:CategoryDefinition: Authentication Failures" และ "when at least <threshold> events are seen with the same Source IP and different Username in <time_window> minutes" — ค่าแนะนำ: threshold=25 events, time_window=1 minute
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
- QRadar มี built-in recon building blocks: BB:Recon Detected: Host Port Scan (400+ ports scanned from single source IP in under 2 minutes), BB:Recon Detected: Local L2L Scanner (60+ hosts scanned in 20 minutes), BB:Recon Detected: Port Scan Detected Across Multiple Hosts
- Type C Superflows คือ port scan detection — aggregate ของ non-ICMP flows ที่มี source IP เดียวกัน, destination IP เดียวกัน แต่หลาย ports
- Default QRadar recon rules มีอยู่แล้ว: "Recon: Local L2L Scanner Detected", "Recon: Host Port Scan Detected", "Recon: Potential Local Port Scan Detected"
ที่มา: [QRadar Admin Guide — Default Recon Rules](https://www.ibm.com/docs/en/SS42VS_7.5/pdf/b_qradar_admin_guide.pdf), [QRadar User Guide — Superflow Type C: Port Scan](https://www.ibm.com/docs/en/SS42VS_7.5/pdf/b_qradar_users_guide.pdf), [QRadar Tuning Guide](https://www.ibm.com/docs/en/SS42VS_7.5/pdf/b_qradar_tuning_guide.pdf)
วิธีแก้:
- ตรวจสอบ built-in recon rules: Offenses tab > Rules > จาก Display list เลือก "All Rules" แล้วค้นหา "Recon" — default rules ทำงานอยู่แล้ว
- สร้าง custom Port Scan Rule (Flow Rule): "and when a flow matches any of the following" และ "when the destination port is one of the following" (ระบุ ports ที่สนใจ) และ "when at least <threshold> flows are seen from the same Source IP to the same Destination IP" และ "when at least <unique_ports> unique destination ports are seen in <time_window> minutes"
- สร้าง custom Host Scan Rule (Flow Rule): "when at least <threshold> flows are seen from the same Source IP to different Destination IPs" และ "when at least <unique_destinations> unique destination IPs are seen in <time_window> minutes"
- สร้าง Building Block สำหรับ authorized outbound ports: "and when the destination port is one of the following" (ports ที่อนุญาต outbound) เพื่อลด false positive
- สร้าง Building Block สำหรับ trusted IPs: เพิ่ม trusted management IPs เข้า exclusion list
- สำหรับ port scan ที่ใช้ NMAP: ถ้า NMAP ติดตั้งบน QRadar system สามารถใช้ "Performs a Network Mapper (NMAP) scan" feature ได้ (right-click > Port Scan)
- ตั้งค่า response: Dispatch new event + Ensure the detected event is part of an offense

---

## 4. Impossible Travel Detection

คำค้น: qradar impossible travel, qradar reference table, qradar AQL, qradar GEO function, qradar risk-based authentication
อาการ: ต้องตรวจจับ impossible travel — user login จาก IP ที่มี location ห่างกันเกินไปในเวลาสั้นๆ (ไม่เดินทางทัน)
คำสั่งตรวจ:
```
ตรวจใน GUI: Offenses tab > Rules > Building Blocks > BB:HostDefinition
```
อ่านผล:
- QRadar ไม่มี built-in impossible travel rule — ต้องสร้าง custom rule โดยใช้ reference table + AQL query
- AQL มีฟังก์ชัน GEO::DISTANCE(sourceip, ip_address) สำหรับคำนวณระยะทางระหว่าง IP addresses
- AQL มี REFERENCETABLE(table_name, column_name, key) สำหรับดึงข้อมูลจาก reference table
- ต้องสร้าง reference table แบบ key: username (ALNIC), ip (IP), date (DATE)
ที่มา: [Impossible Travel Detection — SRA Blog](https://sra.io/blog/impossible-travel/), [AQL Data Retrieval Functions — REFERENCETABLE](https://www.ibm.com/docs/hr/qradar-on-cloud?topic=language-aql-data-retrieval-functions)
วิธีแก้:
- สร้าง Reference Table: ใช้ QRadar API `POST /reference_data/tables` ด้วย key_name_types: `[{"element_type": "ALNIC","key_name": "usernameKey"}, {"element_type": "IP","key_name": "ipKey"}, {"element_type": "DATE","key_name": "dateKey"}]` — ตั้งชื่อ table เช่น "user-ip-date"
- สร้าง Rule 1 (Event Rule — Populate Reference Table): กรองเฉพาะ VPN/remote access login events ที่ successful — "and when the event QID is one of the following QIDs" (VPN login QID) และ "Add to Reference Data" → เลือก table "user-ip-date" → map usernameKey, ipKey, dateKey → rule นี้จะเก็บ IP address ของแต่ละ user ทุกครั้งที่ login
- สร้าง Rule 2 (Event Rule — Detect Impossible Travel): "and when the event matches this AQL Query" → `GEO::DISTANCE(sourceip, REFERENCETABLE('user-ip-date','ipKey',username))/DOUBLE(DOUBLE(starttime-REFERENCETABLE('user-ip-date','dateKey',username))/3600000) > 200.0 and GEO::DISTANCE(sourceip, REFERENCETABLE('user-ip-date','ipKey',username)) > 0` — ค่า speed threshold (km/h) ปรับตามนโยบายองค์กร (200 = รถยนต์/รถไฟ, 600 = เครื่องบิน)
- สร้าง Rule 3 (Optional — Concurrent Login Detection): "and when at least 2 events are seen with the same Username in <time_window> minutes" และ "and when the Source IPs are different" — สำหรับ concurrent login จากต่าง location
- ตั้งค่า response: Dispatch new event + Ensure the detected event is part of an offense + Index by Username

---

## 5. ตรวจสอบและ Tune Rules

คำค้น: qradar rule testing, qradar false positive tuning, qradar rule threshold, qradar building block edit
อาการ: ต้องตรวจว่า rule ทำงานถูกต้อง และ tune false positive
คำสั่งตรวจ:
```
ตรวจใน GUI: Offenses tab > Rules > แสดง rule ที่สร้าง > คลิก Test เพื่อ test rule
ตรวจใน GUI: Log Activity tab > Tuning false positives
```
อ่านผล:
- Rule testing ใช้ saved search criteria เพื่อเทสต์ว่า rule match กับ historical data หรือไม่
- False positive tuning สามารถ tune ได้จาก Log Activity tab หรือ Network Activity tab โดย select event/flow แล้ว choose "tune as false positive"
- Building blocks สามารถ edit ได้ตลอดเวลาเพื่อปรับ threshold และ exclusion lists
ที่มา: [QRadar Tuning Guide — Rule Testing](https://www.ibm.com/docs/en/SS42VS_7.5/pdf/b_qradar_tuning_guide.pdf), [QRadar User Guide — Tuning False Positives](https://www.ibm.com/docs/en/SS42VS_7.5/pdf/b_qradar_users_guide.pdf)
วิธีแก้:
- Test rule: Offenses tab > Rules > คลิก rule ที่สร้าง > คลิก Test เพื่อดูว่า historical events match rule หรือไม่
- Tune false positive: Log Activity tab > select event > right-click > Tune as False Positive หรือเลือก event > "Tuning false positives" ใน toolbar
- แก้ building block: Offenses tab > Rules > Display list เลือก Building Blocks > Double-click BB > อัพเดท threshold/exclusion lists > คลิก Finish
- ใช้ Threshold Rule / Behavioral Rule / Anomaly Rule สำหรับ advanced detection — ต้อง save search criteria ก่อนจึงจะ enable options เหล่านี้ได้
- ตั้งค่า Response Limiter ใน rule responses เพื่อจำกัด frequency ของ offense generation

---

## 6. ระวังเรื่องสำคัญ

คำค้น: qradar rule pitfalls, qradar reference data, qradar AQL functions, qradar domain
อาการ: ต้องระวังข้อผิดพลาดทั่วไปเมื่อสร้าง QRadar rules
คำสั่งตรวจ:
```
ตรวจใน GUI: Offenses tab > Rules > เลือก rule > Test
ตรวจใน GUI: Log Activity tab > Tuning false positives
```
อ่านผล:
- Rule testing ใช้ saved search criteria เพื่อเทสต์ว่า rule match กับ historical data หรือไม่
- False positive tuning สามารถ tune ได้จาก Log Activity tab โดย select event แล้ว choose "tune as false positive"
ที่มา: [QRadar Tuning Guide — Rule Testing](https://www.ibm.com/docs/en/SS42VS_7.5/pdf/b_qradar_tuning_guide.pdf), [QRadar User Guide — Tuning False Positives](https://www.ibm.com/docs/en/SS42VS_7.5/pdf/b_qradar_users_guide.pdf)
วิธีแก้:
- Rule testing ต้องใช้ saved search criteria ที่ group ตาม parameter เดียวกัน (เช่น username หรือ source IP) — ถ้าไม่ group ถูกต้อง rule จะไม่ทำงาน
- Building blocks ที่แก้ไขแล้วต้องมี "Deploy" QRadar configuration ใหม่ก่อน rule จะทำงาน
- AQL query ใน rule ต้องทดสอบใน Log Activity tab ก่อน (Search > Convert to AQL) เพื่อยืนยันว่า query return ผลถูกต้อง
- GEO::DISTANCE ใน AQL ใช้ IP geolocation database ของ QRadar — accuracy ขึ้นอยู่กับ log source ที่ให้ IP location data
- Reference table ที่สร้างผ่าน API ต้องมี key type ที่ถูกต้อง (ALNIC สำหรับ username, IP สำหรับ IP address, DATE สำหรับ timestamp)
- ใน domain-enabled environment REFERENCETABLE ต้องระบุ domainID หรือใช้ shared reference data เท่านั้น
- ไม่แนะนำให้สร้าง rule ที่ match ทุก authentication failure (too broad) — ต้อง set threshold + time window + exclusion list
- Port scan detection ผ่าน flow อาจมี false positive จาก legitimate services (เช่น DNS queries ไปหลาย ports, load balancer health checks) — ต้อง tune building blocks
- Password spray rule ต้องแยกจาก brute force: password spray = different usernames จาก source IP เดียว, brute force = same username หลายครั้งจาก source IP เดียว
