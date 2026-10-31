---
id: f5-awaf-credential-stuffing-behavioral-dos-threat-campaigns
title: F5 BIG-IP 17.x AWAF - Credential Stuffing, Behavioral L7 DoS, Threat Campaigns
families: f5_tmsh
triggers: f5 credential stuffing, f5 brute force, f5 behavioral dos, f5 l7 dos, f5 threat campaign, f5 awaf credential stuffing, f5 bados, f5 leaked credential check, login URL brute force, fortigate security profile, credential stuffing dictionary, distributed brute force, behavioral detection, server latency
versions: BIG-IP 17.1 / 17.5 (AWAF / ASM 17.x)
sources: https://techdocs.f5.com/en-us/bigip-17-5-0/big-ip-asm-implementations.html, https://techdocs.f5.com/en-us/bigip-17-5-0/big-ip-asm-implementations/mitigating-brute-force-attacks.html, https://techdocs.f5.com/en-us/bigip-17-5-0/big-ip-asm-implementations/preventing-dos-attacks-on-applications.html, https://techdocs.f5.com/en-us/bigip-17-1-0/big-ip-system-dos-protection-and-protocol-firewall-implementations/detecting-and-preventing-dos-attacks.html, https://clouddocs.f5.com/cli/tmsh-reference/v15/modules/security/security_dos_profile.html, https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/asm/asm_policy.html, https://techdocs.f5.com/en-us/bigip-17-5-0/big-ip-asm-implementations/working-with-violations.html, https://techdocs.f5.com/en-us/bigip-16-1-0/big-ip-lcc-guide/registering-lcc-with-bigip-cloud-services.html, https://techdocs.f5.com/en-us/bigip-16-1-0/big-ip-lcc-guide/lcc-credential-stuffing-with-cloud-services/lcc-distributed-brute-force-protection-functionali.html
---

# F5 BIG-IP 17.x AWAF - Credential Stuffing, Behavioral L7 DoS, Threat Campaigns

คำค้น: f5 credential stuffing, f5 brute force, f5 behavioral dos, f5 l7 dos, f5 threat campaign, f5 awaf, f5 bados, f5 leaked credential check
อาการ: Login URL ถูก brute force / credential stuffing จากหลาย IP, Server response latency สูง (L7 DoS), ต้องการเปิดใช้ Threat Campaign signatures

---

## 1. ตรวจระบบ Brute Force / Credential Stuffing

คำค้น: ตรวจ brute force, credential stuffing status, login URL, login pages
อาการ: ต้องตรวจว่ามี login URL ใดบ้างใน policy, brute force protection เปิดอยู่ไหม
คำสั่งตรวจ:
```
tmsh list asm policy /Common/<policy_name>
tmsh show /asm statistics login-url
tmsh list /ltm virtual | grep -i security
```

อ่านผล:
- `list asm policy` — ดูว่า policy มี `brute-force-protection` และ `login-url` กำหนดไว้หรือไม่
- `show /asm statistics login-url` — แสดงรายการ login URLs ทั้งหมดใน ASM policy พร้อม failed login counts
- `list /ltm virtual` — ดูว่า virtual server ตัวใดผูก security policy ไว้

ที่มา: [F5 TechDocs — BIG-IP ASM: Mitigating Brute Force Attacks (17.5.0)](https://techdocs.f5.com/en-us/bigip-17-5-0/big-ip-asm-implementations/mitigating-brute-force-attacks.html)

วิธีแก้:
- ต้องมี login URL อย่างน้อย 1 URL ใน security policy เพื่อ brute force protection จะทำงานได้
- ดู login URLs และ stats ด้วย `tmsh show /asm statistics login-url`
- ถ้าไม่มี login URL ให้สร้างผ่าน GUI: Security → Application Security → Policy Building → Sessions and Logins

ระวัง: brute force protection จะทำงานเฉพาะเมื่อ policy enforcement mode เป็น **Blocking** เท่านั้น

---

## 2. ตั้งค่า Brute Force Protection / Credential Stuffing

คำค้น: brute force protection, credential stuffing config, login URL, leaked credential check, distributed brute force

อาการ: ต้องการป้องกัน credential stuffing / brute force login attacks ผ่าน ASM policy

คำสั่งตรวจ:
```
tmsh show /asm statistics login-url
tmsh list asm policy /Common/<policy_name>
```

อ่านผล:
- `show /asm statistics login-url` — ตรวจสอบ login URLs และ failed login counts
- `list asm policy` — ตรวจสอบว่า policy มี brute-force-protection entity หรือไม่

ที่มา: [F5 TechDocs — BIG-IP ASM: Mitigating Brute Force Attacks (17.5.0)](https://techdocs.f5.com/en-us/bigip-17-5-0/big-ip-asm-implementations/mitigating-brute-force-attacks.html)

วิธีแก้:
- GUI: Security → Application Security → Sessions and Logins → Login Pages → สร้าง login URL (ระบุ URL, access validation)
- GUI: Security → Application Security → Brute Force Attack Prevention → Create
- ตั้งค่า Login Page → เลือก login URL ที่สร้างไว้
- Distributed Brute Force Protection: ตั้ง **Maximum login attempts** (default 100)
- Detect Leaked Credential Stuffing: เลือก **After X login attempts that match known leaked credentials dictionary** (ต้องเปิด Leaked Credential Check Cloud Service)
- Distributed Brute Force Mitigation: เลือก Alarm, CAPTCHA, หรือ Block
- ต้องเปิด `Brute Force: Maximum login attempts are exceeded` ใน Violation Rating (Security → Application Security → Policy Building → Learning and Blocking Settings) ให้เป็น **Block + Alarm**

ระวัง: ต้อง policy enforcement mode เป็น **Blocking** เท่านั้น brute force mitigation จะทำงาน

---

## 3. ตั้งค่า Leaked Credential Check Cloud Service (Credential Stuffing)

คำค้น: leaked credential check, blackfish API, credential stuffing dictionary, cloud services registration, LCC

อาการ: ต้องการเปิดใช้ leaked credential checking เพื่อตรวจจับ credential stuffing attacks จาก dictionary ที่รั่วไหล

คำสั่งตรวจ:
```
tmsh list /sys cloud-service
tmsh list /sys service lcc
```

อ่านผล:
- `list /sys cloud-service` — ตรวจสอบว่า Leaked Credential Check (blackfish) cloud service ถูก register ไว้หรือไม่
- `list /sys service lcc` — ตรวจสอบว่า LCC service เปิดอยู่หรือไม่

ที่มา: [F5 TechDocs — Leaked Credential Check with Cloud Services (LCC)](https://techdocs.f5.com/en-us/bigip-16-1-0/big-ip-lcc-guide/registering-lcc-with-bigip-cloud-services.html)

วิธีแก้:
- GUI: Security → Cloud Services → Cloud Security Services Applications
- เลือก **f5-credential-stuffing-blackfish**
- ระบุ API Key ID และ API Key Secret (ได้จาก F5 SPM Portal หลังซื้อ Leaked Credential Check)
- คลิก Save
- GUI: Security → Application Security → Brute Force Attack Prevention → แก้ login URL → Distributed Brute Force Protection → Detect Leaked Credential Stuffing → เลือก threshold (เช่น "After 100 login attempts that match known leaked credentials dictionary")

ระวัง: ถ้ายังไม่ register Leaked Credential Check กับ Cloud Service การตั้งค่า Detect Leaked Credential Stuffing จะไม่ทำงาน

---

## 4. ตรวจและเปิด Behavioral L7 DoS (BADoS)

คำค้น: behavioral dos, bados, behavioral detection, l7 dos, stress-based detection, server latency, application dos

อาการ: Server response latency สูง, pool members overload, ต้องการเปิด behavioral L7 DoS protection

คำสั่งตรวจ:
```
tmsh list security dos profile /Common/<dos_profile_name>
tmsh list ltm virtual /Common/<virtual_name>
tmsh show /ltm dos
```

อ่านผล:
- `list security dos profile` — ดูว่า DoS profile มี application section กับ stress-based detection เปิดอยู่หรือไม่
- `list ltm virtual` — ดูว่า virtual server ผูก DoS profile ไว้หรือไม่
- `show /ltm dos` — แสดงสถิติ attacks และ current status

ที่มา: [BIG-IP ASM: Preventing DoS Attacks on Applications](https://techdocs.f5.com/en-us/bigip-17-5-0/big-ip-asm-implementations/preventing-dos-attacks-on-applications.html), [Detecting and Mitigating DoS/DDoS Attacks](https://techdocs.f5.com/en-us/bigip-17-1-0/big-ip-system-dos-protection-and-protocol-firewall-implementations/detecting-and-preventing-dos-attacks.html), [Mitigating Brute Force Attacks](https://techdocs.f5.com/en-us/bigip-17-5-0/big-ip-asm-implementations/mitigating-brute-force-attacks.html), [TMSH Reference — security dos profile](https://clouddocs.f5.com/cli/tmsh-reference/v15/modules/security/security_dos_profile.html)

วิธีแก้:
- tmsh: `create security dos profile <name> application add { <app_profile> { options { bot-signatures { check enabled } } } }`
- tmsh: `modify security dos profile <name> application modify { <app_profile> { options { stress-based { thresholds-mode fully-automatic bad-actors-detection enabled request-signatures-detection enabled } } } }`
- tmsh: `modify security dos profile <name> application modify { <app_profile> { options { stress-based { protection-level conservative | balanced | aggressive } } } }`
- GUI: Security → DoS Protection → Protection Profiles → เปิด **Application Security** → Behavioral & Stress-based Detection → Bad actors behavior detection: **Enabled**
- GUI: Behavioral & Stress-based Detection → Request signatures detection: **Enabled**
- GUI: Set **Protection Level** → Conservative, Balanced, หรือ Aggressive
- GUI: Associate DoS profile กับ virtual server (Local Traffic → Virtual Servers → Security → DOS Profile)

ระวัง: ถ้าใช้ stress-based หรือ behavioral DoS protection และ backend server หยุดทำงาน ระบบอาจตรวจจับว่าเป็น DoS attack ได้ (false positive)

---

## 5. เปิดใช้ Threat Campaigns ใน ASM Policy

คำค้น: threat campaign, threat campaigns, security policy, signature update, exploit protection, staging threat campaign

อาการ: ต้องการเปิดใช้ threat campaign signatures เพื่อป้องกัน exploit ล่าสุดที่พบในธรรมชาติ (in-the-wild)

คำสั่งตรวจ:
```
tmsh list asm policy /Common/<policy_name>
tmsh show asm threat-campaigns
```

อ่านผล:
- `list asm policy` — ดูว่า policy เปิดอยู่ (`active`), มี threat campaigns binding หรือไม่
- `show asm threat-campaigns` — แสดงรายการ threat campaigns ที่มีอยู่และสถานะ

ที่มา: [Managing Threat Campaigns (BIG-IQ)](https://techdocs.f5.com/en-us/bigiq-7-0-0/managing-threat-campaigns-using-big-iq/managing-threat-campaigns.html), [Working with Violations](https://techdocs.f5.com/en-us/bigip-17-5-0/big-ip-asm-implementations/working-with-violations.html)

วิธีแก้:
- GUI: Configuration → SECURITY → Threat Intelligence → Web Application Security → Threat Campaigns Files List → ตรวจสอบว่า **Remote Updates** เปิดอยู่ (Download/Update automatically)
- GUI: Configuration → SECURITY → Web Application Security → Policies → เลือก policy → THREAT CAMPAIGNS
- เลือก threat campaigns ที่ต้องการใช้ → ตั้ง action เป็น **Block** หรือ **Alarm**
- GUI: Settings → Policy Building → Settings → Threat Campaigns → **Enable Threat Campaigns Staging** (optional: มี staging period ก่อน enforcement จริง)
- tmsh: `modify asm policy /Common/<policy_name> active` — เปิด policy หลัง config
- GUI: Security → Application Security → Policy Building → Learning and Blocking Settings → ตรวจสอบว่า **Threat Campaigns** violation มี action เป็น **Block** (หรือ Alarm)
- **Threat campaigns จัดการผ่าน GUI เป็นหลัก** — ไม่มี tmsh command สำหรับ config threat campaign โดยตรง (ใช้ BIG-IQ สำหรับ centralized management)

ระวัง: Threat campaigns ให้ action ระดับ 5 (immediate block) — false positive น้อยมาก แต่ staging period แนะนำใน production เพื่อทดสอบก่อน enforce จริง

---

## 6. ดูสถิติและ Log Brute Force / DoS / Threat Campaigns

คำค้น: brute force stats, dos statistics, threat campaign logs, asm violations, analytics report, event log

อาการ: ต้องการดูว่ามีการโจมตี brute force / DoS / threat campaign ไหม, ดูสถิติล่าสุด

คำสั่งตรวจ:
```
tmsh show /asm statistics login-url
tmsh show /ltm dos
tmsh show asm policy-violations
tmsh show asm log
tmsh show security dos device-config
tmsh show /asm analytics report view-by brute-force
```

อ่านผล:
- `show /asm statistics login-url` — แสดง login URLs, failed login counts, detected attacks
- `show /ltm dos` — แสดง DoS attack statistics, current mitigations
- `show asm policy-violations` — แสดง violations ล่าสุด (brute force, threat campaign, etc.)
- `show security dos device-config` — แสดง global DoS device stats
- `show /asm analytics report view-by brute-force` — แสดง brute force analytics report

ที่มา: [Working with Violations](https://techdocs.f5.com/en-us/bigip-17-5-0/big-ip-asm-implementations/working-with-violations.html), [Mitigating Brute Force Attacks](https://techdocs.f5.com/en-us/bigip-17-5-0/big-ip-asm-implementations/mitigating-brute-force-attacks.html), [Preventing DoS Attacks on Applications](https://techdocs.f5.com/en-us/bigip-17-5-0/big-ip-asm-implementations/preventing-dos-attacks-on-applications.html)

วิธีแก้:
- ตรวจสอบ violation ratings: **Threat Campaigns** = ระดับ 5 (always block)
- ตรวจสอบ brute force violation: **Brute Force: Maximum login attempts are exceeded**
- ดู log ด้วย `tmsh show asm log` หรือผ่าน GUI: Security → Application Security → Monitoring → Event Log
- ดู analytics ด้วย `tmsh show /asm analytics report`

---

## 7. ตรวจระบบ Threat Campaign Update และ Staging

คำค้น: threat campaign update, remote update, signature update, threat campaign staging period, BIG-IQ threat campaign

อาการ: ต้องการตรวจสอบว่า threat campaign signatures ได้รับการอัปเดตอัตโนมัติหรือไม่, ตั้งค่า staging period

คำสั่งตรวจ:
```
tmsh list sys db asm.threatcampaigns.update-status
tmsh list asm threat-campaigns
```

อ่านผล:
- `list sys db asm.threatcampaigns.update-status` — ตรวจสอบสถานะการอัปเดต threat campaign signatures
- `list asm threat-campaigns` — แสดงรายการ threat campaigns, version, last update time

ที่มา: [Managing Threat Campaigns (BIG-IQ)](https://techdocs.f5.com/en-us/bigiq-7-0-0/managing-threat-campaigns-using-big-iq/managing-threat-campaigns.html), [BIG-IP 17.5.1 Fixes](https://techdocs.f5.com/kb/en-us/products/big-ip_ltm/releasenotes/related/relnote-supplement-bigip-17-5-1-2.html)

วิธีแก้:
- GUI: Configuration → SECURITY → Threat Intelligence → Web Application Security → Threat Campaigns Files List → เปิด **Remote Updates** (auto-download)
- GUI: Schedule automatic updates (ตั้งค่า interval สำหรับ signature update)
- GUI: เลือก threat campaigns → **Enable Threat Campaigns Staging** → ตั้ง enforcement readiness period (เช่น 30 วัน)
- **BIG-IQ**: Configuration → SECURITY → Web Application Security → Threat Campaigns → จัดการ threat campaigns ทั่วทั้ง managed devices
- **GUI-only**: ไม่มี tmsh command สำหรับ config threat campaign updates — ใช้ GUI หรือ BIG-IQ เท่านั้น

ระวัง: การ install threat campaign ขนาดใหญ่อาจ timeout หลัง 1 ชั่วโมง — หากเกิด timeout ให้เพิ่ม recvTimeout ใน `/usr/local/share/perl5/F5/ASMConfig/EasyClient.pm` (ดู F5 K000156642)
