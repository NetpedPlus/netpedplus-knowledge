---
id: f5-awaf-credential-stuffing-behavioral-dos-threat-campaigns
title: F5 BIG-IP 17.x AWAF - Credential Stuffing, Behavioral L7 DoS, Threat Campaigns
families: f5_tmsh
triggers: f5 credential stuffing, f5 brute force, f5 behavioral dos, f5 l7 dos, f5 threat campaign, f5 awaf credential stuffing, f5 bados, f5 leaked credential check, login URL brute force, credential stuffing dictionary, distributed brute force, behavioral detection, server latency
versions: BIG-IP 17.1 / 17.5 (AWAF / ASM 17.x)
sources: https://techdocs.f5.com/en-us/bigip-17-5-0/big-ip-asm-implementations/mitigating-brute-force-attacks.html, https://techdocs.f5.com/en-us/bigip-17-5-0/big-ip-asm-implementations/preventing-dos-attacks-on-applications.html, https://techdocs.f5.com/en-us/bigip-17-1-0/big-ip-system-dos-protection-and-protocol-firewall-implementations/detecting-and-preventing-dos-attacks.html, https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/asm/asm_policy.html, https://clouddocs.f5.com/cli/tmsh-reference/v15/modules/security/security_dos_profile.html, https://techdocs.f5.com/en-us/bigip-16-1-0/big-ip-lcc-guide/registering-lcc-with-bigip-cloud-services.html
---

# F5 BIG-IP 17.x AWAF - Credential Stuffing, Behavioral L7 DoS, Threat Campaigns

คำค้น: f5 credential stuffing, f5 brute force, f5 behavioral dos, f5 l7 dos, f5 threat campaign, f5 awaf, f5 bados, f5 leaked credential check
อาการ: Login URL ถูก brute force / credential stuffing จากหลาย IP, server ตอบช้า (L7 DoS), ต้องการเปิด Threat Campaigns

หมายเหตุ: AWAF ตั้งค่าเกือบทั้งหมดใน GUI คำสั่ง tmsh ใช้ได้แค่ดู config ของ policy / profile / virtual server

---

## 1. ตรวจว่า virtual server ผูก WAF policy และ DoS profile แล้ว

คำค้น: ตรวจ asm policy, waf policy ผูก virtual server, dos profile ผูก virtual server, enforcement mode
อาการ: ต้องรู้ก่อนว่า virtual server ที่จะป้องกันมี WAF policy / DoS profile และ policy อยู่โหมด Blocking หรือ Transparent
คำสั่งตรวจ:
```
list asm policy <policy_name>
list ltm virtual <vs_name> profiles policies
```
อ่านผล:
- `list asm policy`: ดู `active` และ `enforcement-mode` (blocking / transparent)
- `list ltm virtual`: ในส่วน `policies` ต้องเห็น LTM policy ที่ผูก WAF policy (ชื่อมักขึ้นต้น `asm_auto_l7_policy__`) และในส่วน `profiles` ต้องเห็น DoS profile ถ้าใช้ L7 DoS
ที่มา: [tmsh reference: asm policy](https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/asm/asm_policy.html)
วิธีแก้:
- ผูก policy / DoS profile ใน GUI: Local Traffic > Virtual Servers > เลือก VS > แท็บ Security > Policies
- ระวัง: policy ที่ยังเป็น Transparent จะแค่ alarm / log ไม่ block ให้ดู log จนมั่นใจก่อนเปลี่ยนเป็น Blocking

---

## 2. ตั้ง Login Page และ Brute Force Protection

คำค้น: brute force protection, login page, login url, credential stuffing config, distributed brute force, maximum login attempts
อาการ: ต้องป้องกันการเดารหัส / credential stuffing ที่หน้า login ของเว็บ
ตรวจใน GUI: Security > Application Security > Sessions and Logins > Login Pages List (ต้องมี login URL) และหน้า Brute Force Attack Prevention ของ policy (ต้องมีรายการที่ผูกกับ login page นั้น)
อ่านผล:
- ไม่มี login page = brute force protection ทำงานไม่ได้ เพราะระบบไม่รู้ว่า login สำเร็จหรือล้มเหลว
- login page ต้องบอกเงื่อนไขว่า login ล้มเหลวได้ถูกต้อง (เช่น response code / ข้อความ / cookie) ไม่งั้นนับผิด
ที่มา: [Mitigating Brute Force Attacks (BIG-IP ASM 17.5)](https://techdocs.f5.com/en-us/bigip-17-5-0/big-ip-asm-implementations/mitigating-brute-force-attacks.html)
วิธีแก้:
- สร้าง Login Page: ระบุ URL, วิธีส่ง (POST), ชื่อช่อง username / password และเงื่อนไขที่บอกว่า login ไม่สำเร็จ
- สร้างรายการใน Brute Force Attack Prevention ผูกกับ login page แล้วตั้งการตรวจจับทั้งแบบต้นทางเดียว (ต่อ IP / device) และแบบกระจาย (distributed)
- เลือกการตอบโต้ทีละขั้น: Alarm ก่อน แล้วค่อย CAPTCHA / Client-side integrity / Drop
- ระวัง: ผู้ใช้หลัง NAT IP เดียวกันจำนวนมาก (เช่น สำนักงาน) อาจโดนนับรวม ให้เริ่มที่ Alarm และดู log ก่อน

---

## 3. Leaked Credential Check (credential stuffing จาก dictionary ที่รั่ว)

คำค้น: leaked credential check, credential stuffing dictionary, cloud services registration, LCC, blackfish
อาการ: ต้องตรวจจับการ login ด้วย username / password ที่หลุดจากเว็บอื่น
ตรวจใน GUI: Security > Cloud Services > Cloud Security Services Applications (ต้องเห็นบริการ Leaked Credential Check ลงทะเบียนแล้ว)
อ่านผล:
- ยังไม่ลงทะเบียน = ตัวเลือก Detect Leaked Credential Stuffing ใน Brute Force Attack Prevention จะไม่มีผล
ที่มา: [Registering LCC with BIG-IP Cloud Services](https://techdocs.f5.com/en-us/bigip-16-1-0/big-ip-lcc-guide/registering-lcc-with-bigip-cloud-services.html)
วิธีแก้:
- ต้องมี subscription Leaked Credential Check แล้วนำ API key ที่ได้จาก F5 มาใส่ในหน้า Cloud Security Services Applications (ห้ามจด API key ลงไฟล์หรือ log)
- เปิด Detect Leaked Credential Stuffing ในรายการ Brute Force Attack Prevention ของ login page
- BIG-IP ต้องออกอินเทอร์เน็ตไปบริการ cloud ของ F5 ได้ (DNS / route / proxy)

---

## 4. Behavioral L7 DoS (BaDoS)

คำค้น: behavioral dos, bados, behavioral detection, l7 dos, stress-based detection, server latency, application dos, dos profile
อาการ: server ตอบช้า / pool member overload จาก request จำนวนมากที่ดูเหมือนปกติ
คำสั่งตรวจ:
```
list security dos profile <dos_profile_name>
list ltm virtual <vs_name> profiles
```
อ่านผล:
- `list security dos profile`: ต้องมีส่วน `application` ในโปรไฟล์ (ไม่มี = ยังไม่ได้เปิด Application Security ใน DoS profile)
- `list ltm virtual`: DoS profile ต้องอยู่ใน `profiles` ของ virtual server ที่ต้องการป้องกัน
ที่มา: [Preventing DoS Attacks on Applications (BIG-IP ASM 17.5)](https://techdocs.f5.com/en-us/bigip-17-5-0/big-ip-asm-implementations/preventing-dos-attacks-on-applications.html)
วิธีแก้:
- GUI: Security > DoS Protection > Protection Profiles > เลือก profile > เปิด Application Security > Behavioral & Stress-based Detection
- เปิด Bad actors behavior detection และ Request signatures detection แล้วเลือก Protection Level (Conservative / Balanced / Aggressive) เริ่มที่ Conservative
- ผูก DoS profile กับ virtual server: Local Traffic > Virtual Servers > แท็บ Security > Policies > DoS Protection Profile
- ระวัง: BaDoS ต้องใช้เวลาเรียนรู้ traffic ปกติก่อน จึงจะตรวจจับได้แม่น
- ระวัง: ถ้า backend ช้าเพราะปัญหาภายใน (ฐานข้อมูล / server ล่ม) ระบบอาจมองว่าเป็น DoS ได้

---

## 5. เปิดใช้ Threat Campaigns และอัปเดตอัตโนมัติ

คำค้น: threat campaign, threat campaigns, live update, signature update, staging threat campaign
อาการ: ต้องการให้ WAF policy block การโจมตีจาก campaign ที่ F5 ติดตามอยู่ และอัปเดตเองสม่ำเสมอ
ตรวจใน GUI: Security > Live Update (แท็บ Threat Campaigns: ดูเวอร์ชันที่ติดตั้งและตั้งเวลาอัปเดตอัตโนมัติ) และในหน้า policy ดูว่า Threat Campaigns เปิดอยู่
อ่านผล:
- ถ้าเวอร์ชันเก่าหรือไม่มีการอัปเดตอัตโนมัติ = campaign ใหม่จะไม่ถูกจับ
- Threat Campaigns ต้องมี license ที่รองรับ
ที่มา: [Working with Violations (BIG-IP ASM 17.5)](https://techdocs.f5.com/en-us/bigip-17-5-0/big-ip-asm-implementations/working-with-violations.html)
วิธีแก้:
- ตั้งอัปเดตอัตโนมัติใน Security > Live Update
- ในหน้า policy เปิด Threat Campaigns และตรวจ action ของ violation ที่เกี่ยวข้องใน Learning and Blocking Settings
- ถ้าต้องการทดสอบก่อนบังคับใช้ ให้เปิด staging ของ Threat Campaigns แล้วดู log ระหว่าง staging
- ระวัง: ติดตั้งแพ็กเกจแล้วค้าง / timeout ให้ดู F5 K000156642 และเปิดเคสกับ F5 ห้ามแก้ไฟล์ระบบใน BIG-IP เอง

---

## 6. ดู log การโจมตี

คำค้น: brute force log, dos event log, threat campaign log, asm violations, event log
อาการ: ต้องการดูว่ามี brute force / L7 DoS / threat campaign เกิดขึ้นหรือไม่ และ block ไปแล้วเท่าไร
ตรวจใน GUI: Security > Event Logs > Application (Requests และ Brute Force Attacks) และ Security > Event Logs > DoS > Application Events
อ่านผล:
- Requests: กรองตาม violation เช่น Brute Force หรือ Threat Campaign เพื่อดู IP / URL / action ที่ระบบทำ
- Brute Force Attacks: เห็นช่วงเวลาที่ตรวจพบ ต้นทาง และการตอบโต้ (alarm / CAPTCHA / drop)
- DoS Application Events: เห็นช่วงเวลาที่ BaDoS ตรวจพบและการ mitigate
ที่มา: [Mitigating Brute Force Attacks (BIG-IP ASM 17.5)](https://techdocs.f5.com/en-us/bigip-17-5-0/big-ip-asm-implementations/mitigating-brute-force-attacks.html)
วิธีแก้:
- ถ้าผู้ใช้จริงโดน block: ดู request ใน Event Log ว่าโดน violation อะไร แล้วปรับเฉพาะจุดนั้น (ไม่ปิด policy ทั้งตัว)
- ส่ง log ไป SIEM ด้วย Logging Profile ที่ผูกกับ virtual server เพื่อเก็บย้อนหลัง
