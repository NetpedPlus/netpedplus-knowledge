---
id: f5-bigip-asm-false-positive-staging
title: F5 BIG-IP 17.5.x — ASM False Positive / Staging / Learning
families: f5_tmsh
triggers: f5 asm false positive, f5 asm block user, f5 asm staging blocking, f5 asm learning mode, f5 asm event logs, f5 asm violation learn
versions: BIG-IP 17.5.x
sources: https://techdocs.f5.com/en-us/bigip-17-5-0/big-ip-asm-implementations/working-with-violations.html,https://techdocs.f5.com/en-us/bigip-17-5-0/big-ip-asm-implementations/changing-security-policy-settings.html,https://techdocs.f5.com/en-us/bigip-17-5-0/big-ip-asm-implementations/logging-application-security-events.html
---

# F5 BIG-IP 17.5.x — ASM False Positive / Staging / Learning

คำค้น: f5 asm false positive, f5 asm block user, f5 asm staging blocking, f5 asm learning mode, f5 asm event logs, f5 asm violation learn
อาการ: ผู้ใช้ถูก ASM บล็อก (false positive), policy อยู่ใน staging mode ยังไม่ enforce, หรือต้องการเปิด learning mode สำหรับ traffic ใหม่

อ้างอิง playbook อื่น:
- `f5-bigip-17-security-upgrade-assessment-ha` -> อัปเกรด HA ทั่วไป
- `f5-bigip-17-5-advanced-waf-upgrade-precautions` -> Cookie, Provisioning, Device Group หลัง upgrade

---

## 1 ตรวจสอบ False Positive ASM บล็อกผู้ใช้จริง

คำค้น: f5 asm false positive violation rating, f5 asm event logs requests
อาการ: ผู้ใช้ถูก block, ได้รับ error 403, violation log เต็ม — เกิดจาก signature matching ผิด หรือ policy configuration ไม่ครอบคลุม legitimate traffic

ตรวจใน GUI:
- Security > Event Logs > Application > Requests — ดู request list

ตรวจสอบ logging:
- /var/log/asm ปิดเป็นค่าเริ่มต้น (เอกสารระบุ: "Logging to this file is off by default") — ต้องเปิด logging profile ก่อนจึงจะเห็น log ไฟล์

อ่านผล:
- ดู violation rating 1–5 ใน request list
- Rating 1 = most likely false positive
- Rating 3 = request needs further examination
- Rating 4 = looks like a threat but requires examination

วิธีแก้:
- คลิก Learn สำหรับ violations ที่ต้องการ allow
- เพิ่ม learning suggestions เข้า security policy
- ปรับ policy settings ถ้าจำเป็น
- Apply policy หลังแก้ไข

ที่มา: [Working with Violations (17.5)](https://techdocs.f5.com/en-us/bigip-17-5-0/big-ip-asm-implementations/working-with-violations.html)

อ้างอิง:
- "You or the security manager can examine requests that cause violations to determine whether the requests are real attacks or false positives."
- "The violation rating ranks the transaction from 1 to 5, where 5 indicates the highest probability of a real attack with high severity."
- "Rating 1: Request is most likely a false positive. If it is, then consider accepting learning suggestions to add this to the security policy."

---

## 2 จัดการ Violations และปรับ Policy

คำค้น: f5 asm manage violations learn button, f5 asm false positive click learn
อาการ: Users ถูก block, traffic ไม่ผ่าน, ต้อง approve traffic ผ่าน violation list

ตรวจใน GUI:
- Security > Event Logs > Application > Requests — ดู Request list และ violation rating

อ่านผล:
- Requests with high violation ratings = likely real attacks
- Requests with low violation ratings = อาจเป็น false positive

วิธีแก้:
- ดู request list แล้วจัดการ violation
- สำหรับ false positives → คลิก Learn → Accept suggestions
- ปรับ violation action จาก Block เป็น Alarm ถ้าต้องการแค่ monitor
- Apply policy หลังแก้ไข

ที่มา: [Working with Violations (17.5)](https://techdocs.f5.com/en-us/bigip-17-5-0/big-ip-asm-implementations/working-with-violations.html)

อ้างอิง:
- "Requests with high violation ratings are likely to be real attacks, and you can review them to analyze threats to your web applications."
- "You can review requests with low violation ratings and if they are false positives you can accept the request to adopt the learning suggestions for the security policy."
- "4. For violations that you want to allow (false positives), click the Learn button."

---

## 3 เปลี่ยน Staging เป็น Blocking

คำค้น: f5 asm staging blocking enforcement readiness period, f5 asm enforce mode transparent blocking
อาการ: Entity / signature ยังไม่ enforce, อยู่ใน staging mode — traffic ไม่ถูก block แม้มี violation

ตรวจใน GUI:
- Security > Application Security > Policy Building > Learning and Blocking Settings — ดู Enforcement Mode และ Enforcement Readiness Period

อ่านผล:
- Enforcement Mode = transparent → traffic ไม่ถูก block (แค่ log)
- Enforcement Mode = blocking → traffic ถูก block ถ้ามี violation และ enforcement readiness period เกินแล้ว
- Default Enforcement Readiness Period = 7 days (staging)

วิธีแก้:
- เปลี่ยน Enforcement Mode จาก Transparent เป็น Blocking เมื่อพร้อม
- **ผลกระทบ**: อาจบล็อกผู้ใช้จริง — ทำหลัง staging ครบ
- Adjust Enforcement Readiness Period ตามต้องการ (default 7 days)
- Apply policy หลังแก้ไข

ที่มา: [Changing Security Policy Settings (17.5)](https://techdocs.f5.com/en-us/bigip-17-5-0/big-ip-asm-implementations/changing-security-policy-settings.html)

อ้างอิง:
- "Security policies can be in one of two enforcement modes: transparent or blocking. The enforcement mode specifies whether the system simply logs or blocks a request that triggers a security policy violation."
- "When the enforcement mode is set to transparent, traffic is not blocked even if a violation is triggered. The system typically logs the violation event."
- "When the enforcement mode is set to blocking, traffic is blocked if it causes a violation (that is configured for blocking), and the enforcement readiness period is over."
- "For each security policy, you can configure the number of days used as the enforcement readiness period, also called staging. The default value of 7 days works well for most situations."

