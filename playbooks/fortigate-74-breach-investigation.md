---
id: fortigate-74-breach-investigation
title: FortiGate 7.4 — ตรวจว่าอุปกรณ์ขอบเครือข่ายโดนเจาะแล้วหรือยัง
families: fortinet_fortios
triggers: FortiGate 7.4 forensic investigation threat detection security event
versions: FortiOS 7.4.x
sources: https://docs.fortinet.com/document/fortigate/7.4.0/administration-guide/876272/security-events-log-page
---

# FortiGate 7.4 — ตรวจว่าอุปกรณ์ขอบเครือข่ายโดนเจาะแล้วหรือยัง

คำค้น: FortiGate 7.4 breach investigation forensic threat detection security event
อาการ: ได้รับแจ้งว่าอุปกรณ์ขอบเครือข่ายอาจโดนโจมตีหรือเจาะระบบ — ต้องตรวจสอบ log, security event, FortiView, local-in, IPS, AV, web filter ว่ามีเหตุการณ์ผิดปกติหรือไม่

---

## 1. ตรวจว่า log ถูกบันทึกหรือไม่

คำค้น: FortiGate 7.4 log settings local storage fortianalyzer configuration
อาการ: ต้องตรวจว่า log ถูกบันทึก local และ/หรือส่ง FortiAnalyzer แล้วหรือไม่

คำสั่งตรวจ:
```
show log settings
show log fortianalyzer
execute log local show
```

อ่านผล:
- `show log settings` → ดูว่า `local-storage` เป็น enable หรือ disable
- `show log fortianalyzer` → ดูว่า server IP ที่กำหนดเป็น FortiAnalyzer จริงหรือไม่
- `execute log local show` → ดู disk status และ quota ที่ใช้

ที่มา: [Log settings and targets — FortiOS 7.4](https://docs.fortinet.com/document/fortigate/7.4.2/administration-guide/250999/log-settings-and-targets)

---

## 2. ตรวจ Security Events / Malware, IPS, Web Filter

คำค้น: FortiGate 7.4 "diagnose fortiview result security-log" top threats
อาการ: ต้องดูว่ามี Malware, IPS, Web Filter, Email ที่ถูกบล็อกหรือตรวจจับได้หรือไม่

คำสั่งตรวจ:
```
diagnose fortiview result security-log
diagnose fortiview result security-log action=blocked
diagnose fortiview result security-log action=passthrough
```

อ่านผล:
- action=blocked = ถูกบล็อก (good)
- action=passthrough = ผ่านได้ (bad — อาจเป็นการหลุด)
- ดูว่า signature ใดถูก trigger บ่อยที่สุด

ที่มา: [Security Events log page — FortiOS 7.4](https://docs.fortinet.com/document/fortigate/7.4.0/administration-guide/876272/security-events-log-page)

---

## 3. ตรวจ Log แต่ละหมวด / Virus, IPS, Web Filter, Email

คำค้น: FortiGate 7.4 execute log filter category log ids
อาการ: ต้องตรวจ log แต่ละหมวด (virus=2, webfilter=3, ips=4, emailfilter=5) แยกกัน

คำสั่งตรวจ:
```
execute log filter device 0
execute log filter category 2
execute log display
```

อ่านผล:
- category 2 = virus/malware — ดูว่ามีการ passthrough หรือไม่
- ดูว่า malware name ใดที่ตรวจเจอ และมาจาก IP ใด

ที่มา: [FortiOS log message reference — FortiOS 7.4](https://docs.fortinet.com/document/fortigate/7.4.0/fortios-log-message-reference/656858)

---

## 4. ตรวจ Forward Traffic Logs / Traffic ผิดปกติ

คำค้น: FortiGate 7.4 execute log filter forward traffic investigation
อาการ: ต้องดูว่ามี traffic ผิดปกติ — port scan, data exfiltration, connections ไป IP ที่ไม่น่าเชื่อถือ

คำสั่งตรวจ:
```
execute log filter device 0
execute log filter category 0
execute log display
```

อ่านผล:
- category 0 = forward traffic logs
- ดู source IP ภายในที่ไป connect ไป external IP ที่ไม่น่าเชื่อถือ
- ดู destination port ที่สูง (>1024) ซึ่งอาจเป็น reverse shell

ที่มา: [Log settings and targets — FortiOS 7.4](https://docs.fortinet.com/document/fortigate/7.4.2/administration-guide/250999/log-settings-and-targets)

---

## 5. ตรวจ Sessions ทั้งหมด / Connections ที่น่าสงสัย

คำค้น: FortiGate 7.4 "diagnose sys session list" active sessions
อาการ: ต้องดูว่ามี sessions ที่น่าสงสัย — connections จากภายนอกที่ไม่ได้รับอนุญาต หรือ reverse shell

คำสั่งตรวจ:
```
diagnose sys session list
diagnose sys session ip <external-IP>
```

อ่านผล:
- ดู session ที่มาจาก IP ภายนอก และไป destination port ที่ไม่ปกติ
- ดู session ที่มี source port สูง ซึ่งอาจเป็น reverse shell
- ดู session ที่มี duration ยาว (>1 ชั่วโมง) จาก IP ภายนอก

ที่มา: [Log-related diagnose commands — FortiOS 7.4](https://docs.fortinet.com/document/fortigate/7.4.0/administration-guide/668197/log-related-diagnose-commands)

---

## 6. ตรวจ Local-In Policy / Admin Access ที่น่าสงสัย

คำค้น: FortiGate 7.4 firewall local-in-policy admin access investigation
อาการ: ต้องดูว่ามีผู้ใดเข้าถึง admin interface ของ FortiGate จาก IP ที่ไม่ได้รับอนุญาตหรือไม่

คำสั่งตรวจ:
```
get firewall local-in-policy all
```

อ่านผล:
- ดู local-in policies ทั้งหมด
- ดูว่า allowaccess อนุญาตให้เข้าถึงได้จาก IP ใดบ้าง
- ดูว่ามี policy ที่ permit ทุก IP หรือไม่ (อันตราย)

ที่มา: [Local-in policy — FortiOS 7.4](https://docs.fortinet.com/document/fortigate/7.4.0/administration-guide/363127/local-in-policy)

---

## 7. ตรวจ Admin Access Logs / ใครเข้า Admin Interface

คำค้น: FortiGate 7.4 log filter admin login event log HTTPS SSH
อาการ: ต้องดูว่ามีผู้ใดเข้าถึง admin interface ของ FortiGate จาก IP ที่ไม่ได้รับอนุญาตหรือไม่

คำสั่งตรวจ:
```
execute log filter device 0
execute log filter category 1
execute log filter service HTTPS
execute log display
```

อ่านผล:
- category 1 = event logs — รวม admin login
- service HTTPS = เข้าผ่าน web GUI
- service SSH = เข้าผ่าน command line
- ดูว่า IP ที่เข้าเป็น IP ภายในหรือภายนอก

ที่มา: [FortiOS log message reference — FortiOS 7.4](https://docs.fortinet.com/document/fortigate/7.4.0/fortios-log-message-reference/656858)

---

## 8. ตรวจ Administrator Accounts / Backdoor

คำค้น: FortiGate 7.4 config admin user list accounts
อาการ: ต้องดูว่ามี admin account ที่สร้างขึ้นมาใหม่ — อาจเป็น backdoor

คำสั่งตรวจ:
```
get admin user
```

อ่านผล:
- ดูว่า admin account ใดบ้างที่มีอยู่
- ดูว่า account ใดที่สร้างขึ้นไม่ถูกต้อง (มีชื่อแปลกๆ, ไม่มี description)
- ดูว่า admin account ใดมี unencrypted password ที่ไม่ควรมี

ที่มา: [config system admin — FortiOS 7.4 CLI Reference](https://docs.fortinet.com/document/fortigate/7.4.0/cli-reference/13620/config-system-admin)

---

## 9. ตรวจ IPS Events / Exploit Attempts

คำค้น: FortiGate 7.4 log filter ips events category 4 exploit
อาการ: ต้องดูว่ามี exploit attempts, command injection, SQL injection, buffer overflow ที่ถูกบล็อกหรือไม่

คำสั่งตรวจ:
```
execute log filter device 0
execute log filter category 4
execute log display
```

อ่านผล:
- category 4 = IPS events
- ดูว่า attack name ใดที่ trigger บ่อยที่สุด
- ดูว่า attack ใดที่ passthrough (ไม่ถูกบล็อก) — อาจเป็นการหลุด

ที่มา: [IPS security profile — FortiOS 7.4](https://docs.fortinet.com/document/fortigate/7.4.4/ngfw-atp-deployment-guide/900128/ips-security-profile)

---

## 10. ตรวจ IPS Signature Status / Signature ที่ถูก Disable

คำค้น: FortiGate 7.4 "show ips sensor" ips sensor signature list
อาการ: ต้องดูว่า IPS signature สำคัญถูก disable หรือไม่

คำสั่งตรวจ:
```
show ips sensor
```

อ่านผล:
- ดู sensor profile ที่ใช้งาน
- ดูว่า signature ใดถูก disable
- signature ที่ disable อาจทำให้ exploit ที่ควรบล็อกไม่ถูกบล็อก

ที่มา: [IPS security profile — FortiOS 7.4](https://docs.fortinet.com/document/fortigate/7.4.4/ngfw-atp-deployment-guide/900128/ips-security-profile)

---

## 11. ตรวจ AV / Malware ที่หลุด Passthrough

คำค้น: FortiGate 7.4 antivirus passthrough malware quarantine
อาการ: ต้องดูว่ามีไฟล์ที่ติด malware ซึ่งอาจถูก passthrough (ไม่ถูกบล็อก) หรือไม่

คำสั่งตรวจ:
```
execute log filter device 0
execute log filter category 2
execute log filter action=passthrough
execute log display
```

อ่านผล:
- ดูว่า malware ใดที่ passthrough
- ดูว่าไฟล์มาจาก URL หรือ attachment
- ดูว่า device ใดที่ได้รับไฟล์

ที่มา: [IPS security profile — FortiOS 7.4](https://docs.fortinet.com/document/fortigate/7.4.4/ngfw-atp-deployment-guide/900128/ips-security-profile)

---

## 12. ตรวจ Web Filter / เข้าเว็บไซต์อันตราย

คำค้น: FortiGate 7.4 webfilter log malicious website phishing blocked
อาการ: ต้องดูว่ามีผู้ใช้หรือเครื่องภายในเข้าไปยัง phishing site, malware hosting, หรือ C2 server หรือไม่

คำสั่งตรวจ:
```
execute log filter device 0
execute log filter category 3
execute log display
```

อ่านผล:
- category 3 = web filter
- ดูว่า URL ใดที่ถูก block — phishing, malware, C2
- ดูว่า session ใดที่ passthrough เข้าเว็บอันตราย (อาจหลุด)

ที่มา: [Log settings and targets — FortiOS 7.4](https://docs.fortinet.com/document/fortigate/7.4.2/administration-guide/250999/log-settings-and-targets)

---

## 13. ตรวจ Anomaly และ DoS / SYN Flood, Port Scan, Brute-Force

คำค้น: FortiGate 7.4 anomaly detection syn flood port scan brute-force
อาการ: ต้องดูว่ามี anomaly detection events — SYN flood, port scan, brute-force ซึ่งอาจเป็นการโจมตี

คำสั่งตรวจ:
```
execute log filter device 0
execute log filter category 7
execute log display
```

อ่านผล:
- category 7 = anomaly events
- ดูว่า attack name ใดที่ trigger — syn-flood, port-scan, brute-force
- ดูว่า IP ใดเป็น attacker และ target คืออะไร

ที่มา: [Log-related diagnose commands — FortiOS 7.4](https://docs.fortinet.com/document/fortigate/7.4.0/administration-guide/668197/log-related-diagnose-commands)

---

## 14. ตรวจ FortiView Top Threats / สรุป Attack ทั้งหมด

คำค้น: FortiGate 7.4 "diagnose fortiview result top-threats" top threats
อาการ: ต้องดูสรุป attack ทั้งหมดจาก FortiView — ใช้เป็นจุดเริ่มต้นที่ดีสุด

คำสั่งตรวจ:
```
diagnose fortiview result top-threats
```

อ่านผล:
- ดู top 10 threats ทั้งหมด
- ดูว่า attack type ใดเป็นอันดับ 1
- ดู source IP ที่เป็น top attacker
- ดู destination IP ที่ถูกโจมตีมากที่สุด

ที่มา: [Security Events log page — FortiOS 7.4](https://docs.fortinet.com/document/fortigate/7.4.0/administration-guide/876272/security-events-log-page)

---

## 15. ตรวจ SSL/SSH / Encrypted Threat

คำค้น: FortiGate 7.4 ssl inspection log category 17 ssh inspection
อาการ: ต้องดูว่ามี SSL inspection logs ที่พบ SSL certificate ที่น่าสงสัย หรือ SSH command ที่ผิดปกติ

คำสั่งตรวจ:
```
execute log filter device 0
execute log filter category 17
execute log display
```

อ่านผล:
- category 17 = SSL inspection
- ดูว่า SSL certificate ใดที่ suspicious
- ดูว่า connection ใดถูก block เพราะ SSL inspection

ที่มา: [Log settings and targets — FortiOS 7.4](https://docs.fortinet.com/document/fortigate/7.4.2/administration-guide/250999/log-settings-and-targets)

---

## 16. สรุป / การตอบสนองเบื้องต้น

คำค้น: FortiGate 7.4 incident response breach block IP quarantine
อาการ: เมื่อพบเหตุการณ์ที่น่าสงสัย ต้องดำเนินการตอบสนองทันที

คำสั่งตรวจ:
```
execute log local export all
```

อ่านผล:
- ดูว่า log ถูก export ไปยัง path ใด

ที่มา: [Log settings and targets — FortiOS 7.4](https://docs.fortinet.com/document/fortigate/7.4.2/administration-guide/250999/log-settings-and-targets)

วิธีแก้:
1. **หยุดการแพร่กระจาย** — Block IP ที่น่าสงสัย: `config firewall address / set socket-address / set action deny`
2. **เก็บหลักฐาน** — บันทึก log ทั้งหมด: `execute log local export all`
3. **ตรวจสอบการเข้าถึงเพิ่มเติม** — เปลี่ยน password admin, ตรวจสอบ admin accounts, ตรวจสอบ local-in policies
4. **ตรวจสอบความเสียหาย** — ตรวจสอบว่าข้อมูลสำคัญถูกลักลอบออกไปหรือไม่, ตรวจสอบว่ามีการติดตั้ง backdoor หรือไม่

ตรวจใน GUI: *Log & Report > Security Events* — Dashboard > FortiView

---

## บทเรียน

คำค้น: FortiGate 7.4 breach investigation forensics playbook lessons
อาการ: บทเรียนจากการตรวจว่าอุปกรณ์โดนเจาะหรือไม่

คำสั่งตรวจ:
```
diagnose fortiview result security-log
```

อ่านผล:
- ดู summary ของ security events ทั้งหมด
- ใช้สรุปภาพรวมการโจมตี

ที่มา: [Security Events log page — FortiOS 7.4](https://docs.fortinet.com/document/fortigate/7.4.0/administration-guide/876272/security-events-log-page)

- การตรวจว่าอุปกรณ์โดนเจาะหรือไม่ ต้องดู log หลายแหล่ง — Security Events, Forward Traffic, Local-In, IPS, AV, Web Filter
- ใช้ `diagnose fortiview result security-log` เป็นจุดเริ่มต้นที่ดีที่สุด
- ตรวจสอบทั้ง `action=blocked` และ `action=passthrough` — passthrough อาจเป็นการหลุด
- ตรวจสอบ local-in policies เสมอ — admin access ที่ไม่ได้รับอนุญาตเป็น indicator สำคัญ
- บันทึกหลักฐาน (log export) ก่อนดำเนินการใดๆ
- ต้องเปิด log ทุกหมวด (traffic, virus, webfilter, ips, email, anomaly, ssl, ssh) และ log ไป FortiAnalyzer หรือ local storage
