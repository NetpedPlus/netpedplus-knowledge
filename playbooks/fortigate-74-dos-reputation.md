---
id: fortigate-74-dos-reputation
title: FortiGate 7.4 DoS Policy, IP Reputation, Geo-block
families: fortinet_fortios
triggers: fortigate dos policy, anomaly detection, tcp_syn_flood, udp_flood, icmp_flood, ip reputation, isdb, fortiguard, geo-block, country block, quarantine, dos-protect, ip reputation filter, geography address
versions: FortiOS 7.4.x
sources: https://docs.fortinet.com/document/fortigate/7.4.1/cli-reference/305620/config-firewall-dos-policy, https://docs.fortinet.com/document/fortigate/7.4.4/cli-reference/333889629/config-firewall-policy, https://docs.fortinet.com/document/fortigate/7.4.2/cli-reference/227620/config-firewall-address, https://docs.fortinet.com/document/fortigate/7.4.3/administration-guide/771644/dos-policy, https://docs.fortinet.com/document/fortigate/7.4.4/administration-guide/68937/ip-reputation-filtering, https://docs.fortinet.com/document/fortigate/7.4.0/cli-reference/95620/config-system-fortiguard
---

# FortiGate 7.4 DoS Policy, IP Reputation, Geo-block

คำค้น: fortigate dos policy, anomaly detection, tcp_syn_flood, udp_flood, icmp_flood, ip reputation, isdb, fortiguard, geo-block, country block, quarantine attacker, fortigate dos-protect
อาการ: ตรวจพบ SYN flood / UDP flood / ICMP flood เข้ามา, traffic ถูกบล็อกโดยไม่ทราบสาเหตุจาก IP reputation, ต้องการบล็อกประเทศที่ไม่จำเป็น, traffic จาก IP reputation ต่ำถูก drop

---

## 1. ตรวจ DoS policy ที่มีอยู่

คำค้น: fortigate dos policy, fortigate dos-protect, show firewall dos-policy
อาการ: ต้องตรวจว่ามี DoS policy อะไรอยู่บ้างก่อนแก้ไข

คำสั่งตรวจ:
```
get firewall dos-policy
```
อ่านผล:
- ดู policy ID, name, interface, srcaddr, dstaddr, service และสถานะ anomaly ทั้งหมดที่ active อยู่
- หากไม่มี policy เลย หรือ policy ที่อยู่ใช้ threshold สูงเกินไป = ต้องสร้าง DoS policy ใหม่

ที่มา: [config firewall DoS-policy — FortiOS 7.4 CLI Reference](https://docs.fortinet.com/document/fortigate/7.4.1/cli-reference/305620/config-firewall-dos-policy)

---

## 2. สร้าง DoS policy ตรวจสอบ SYN flood

คำค้น: tcp_syn_flood, syn flood protection, do-not-set flood policy
อาการ: ต้องการสร้าง DoS policy เพื่อตรวจจับและบล็อก SYN flood ที่โจมตี server ภายใน

คำสั่งตรวจ:
```
get firewall policy
```
อ่านผล:
- ดูว่ามี firewall policy ใดบ้างที่รองรับ traffic เข้า server ภายใน (dstintf = internal interface)
- ใช้ srcaddr / dstaddr ของ policy ที่มีอยู่มาสร้าง DoS policy ให้สอดคล้องกัน

ที่มา: [config firewall policy — FortiOS 7.4 CLI Reference](https://docs.fortinet.com/document/fortigate/7.4.4/cli-reference/333889629/config-firewall-policy)

วิธีแก้:
- สร้าง DoS policy ใหม่ด้วย `config firewall DoS-policy`, `edit <policyid>`, `set name "DoS-Flood"`, `set interface "port1"`, `set srcaddr "all"`, `set dstaddr "<internal-server-address>"`, `set service "ALL"`, `config anomaly`, `edit "tcp_syn_flood"`, `set status enable`, `set log enable`, `set action block`, `set quarantine attacker`, `set threshold 2000`, `next`, `end`, `next`, `end`
- แต่ละ anomaly ต้องกำหนด `set status enable`, `set action` (block หรือ pass), `set log` (enable หรือ disable), และ `set threshold` (packets per second สำหรับ flood, sessions per second สำหรับ scan/session)
- สำหรับ tcp_syn_flood ค่า threshold ที่แนะนำคือ 2000 packets per second หาก SYN packet rate ถึงจุดนี้ FortiGate จะ block และ quarantine IP ที่โจมตี
- ระวัง: การตั้งค่า threshold ต่ำเกินไปอาจบล็อก traffic ปกติได้ ควรเริ่มที่ค่าแนะนำและปรับตามสถิติจริง

---

## 3. เพิ่ม UDP / ICMP flood และ scan detection

คำค้น: udp_flood, icmp_flood, udp_scan, icmp_sweep, flood detection, scan detection
อาการ: ต้องการเพิ่ม anomaly อื่นๆ นอกเหนือจาก SYN flood เพื่อครอบคลุมการโจมตีหลายรูปแบบ

คำสั่งตรวจ:
```
get firewall policy
```
อ่านผล:
- ดู service ที่ใช้ร่วมใน firewall policy (ALL, UDP, ICMP, หรือ service เฉพาะ) เพื่อกำหนด threshold ให้เหมาะสมกับประเภท traffic

ที่มา: [config firewall DoS-policy — FortiOS 7.4 CLI Reference](https://docs.fortinet.com/document/fortigate/7.4.1/cli-reference/305620/config-firewall-dos-policy)

วิธีแก้:
- เพิ่ม anomaly เข้า policy เดียวกัน: `config firewall DoS-policy`, `edit <policyid>`, `config anomaly`, `edit "udp_flood"`, `set status enable`, `set action block`, `set log enable`, `set threshold 2000`, `next`, `edit "icmp_flood"`, `set status enable`, `set action block`, `set log enable`, `set threshold 250`, `next`, `edit "udp_scan"`, `set status enable`, `set action block`, `set log enable`, `set threshold 2000`, `next`, `edit "icmp_sweep"`, `set status enable`, `set action block`, `set log enable`, `set threshold 100`, `next`, `end`, `next`, `end`
- สำหรับ UDP/ICMP flood ค่า threshold ที่แนะนำคือ 2000 packets per second สำหรับ UDP และ 250 packets per second สำหรับ ICMP
- สำหรับ UDP/ICMP scan ค่า threshold ที่แนะนำคือ 2000 sessions per second สำหรับ UDP scan และ 100 sessions per second สำหรับ ICMP sweep

---

## 4. ตรวจสอบ IP reputation filtering

คำค้น: ip reputation, IP reputation filter, reputation-minimum, reputation-direction, ISDB
อาการ: ต้องตรวจว่า firewall policy ที่มี reputation filtering ถูกต้องหรือไม่

คำสั่งตรวจ:
```
get firewall policy
```
อ่านผล:
- ดู policy ที่มี `set reputation-minimum` และ `set reputation-direction`
- หาก policy สำคัญไม่มี reputation filtering เลย = ต้องเพิ่ม
- reputation level 1 = known malicious (phishing, botnet), level 5 = verified safe (Gmail, Amazon)
- IP ที่ไม่มีใน ISDB ถือว่า reputation level = 3 โดย default

ที่มา: [IP reputation filtering — FortiOS 7.4 Administration Guide](https://docs.fortinet.com/document/fortigate/7.4.4/administration-guide/68937/ip-reputation-filtering)

วิธีแก้:
- เพิ่ม reputation filtering ใน policy: `config firewall policy`, `edit <policyid>`, `set reputation-minimum 4`, `set reputation-direction destination`, `next`, `end`
- reputation-minimum = 4 หมายความว่าบล็อก IP reputation ระดับ 1-3 (malicious, unknown, medium) อนุญาตเฉพาะระดับ 4-5 (good, safe)
- reputation-direction = destination หมายถึงตรวจสอบ reputation ของ IP ปลายทาง
- หากต้องการตรวจสอบฝั่งผู้ส่ง ให้ใช้ `set reputation-direction source`
- reputation-minimum = 3 สำหรับ policy ที่ต้องการอนุญาตแต่เตือน (IP ที่ไม่มีข้อมูลจะถูกบล็อก)
- ระวัง: reputation filtering จะเพิ่ม overhead เพราะต้อง lookup FortiGuard cache

---

## 5. ตรวจสอบและเปิด ISDB / FortiGuard data

คำค้น: isdb, ISDB, fortiguard, reputation data, update-extdb, fortiguard cache
อาการ: ต้องตรวจสอบว่า FortiGuard reputation data ทำงานอย่างถูกต้อง

คำสั่งตรวจ:
```
get system fortiguard
```
อ่านผล:
- ดูว่า `update-extdb` (external database สำหรับ IP reputation) ตั้งเป็น `enable` หรือไม่
- ดูว่า `persistent-connection` ตั้งเป็น `enable` หรือไม่

ที่มา: [config system fortiguard — FortiOS 7.4 CLI Reference](https://docs.fortinet.com/document/fortigate/7.4.0/cli-reference/95620/config-system-fortiguard)

วิธีแก้:
- เปิด ISDB update: `config system fortiguard`, `set update-extdb enable`, `next`, `end`
- หากมี proxy สำหรับ FortiGuard: `config system fortiguard`, `set proxy-server-ip <IP>`, `set proxy-server-port <port>`, `set proxy-username <username>`, `set proxy-password <password>`, `next`, `end`
- ตรวจสอบ ISDB status: `diagnose ip reputation list` (ต้องมี cli-diagnose privilege)
- หากต้องการให้ FortiGuard ใช้ anycast server: `set fortiguard-anycast enable`
- ระวัง: หากไม่มี license FortiGuard หรือเชื่อม FortiGuard ไม่ได้ ISDB จะไม่ update และ reputation filtering จะใช้ cache เก่า

---

## 6. สร้าง address type geography สำหรับ geo-block

คำค้น: geography address, country block, china block, russia block, geo address
อาการ: ต้องสร้าง address object แบบ geography เพื่อระบุ IP จากประเทศที่ต้องการบล็อกหรืออนุญาต

คำสั่งตรวจ:
```
get firewall address
```
อ่านผล:
- ดูว่ามี address type geography อยู่แล้วหรือไม่ (`set type geography`)
- ดูว่ามี address group ที่รวม countries หลายแห่งหรือไม่

ที่มา: [config firewall address — FortiOS 7.4 CLI Reference](https://docs.fortinet.com/document/fortigate/7.4.2/cli-reference/227620/config-firewall-address)

วิธีแก้:
- สร้าง address type geography สำหรับประเทศเดียว: `config firewall address`, `edit "CN-Blocked"`, `set type geography`, `set country CN`, `next`, `end`
- สร้าง address group สำหรับหลายประเทศ: `config firewall addrgrp`, `edit "Blocked-Countries"`, `set member "CN-Blocked" "RU-Blocked" "KP-Blocked" "IR-Blocked"`, `next`, `end`
- แต่ละประเทศใช้รหัส ISO 2 ตัว: CN = จีน, RU = รัสเซีย, KP = เกาหลีเหนือ, IR = อิหร่าน, SY = ซีเรีย
- สำหรับประเทศอื่นให้สร้าง address type geography แยกตาม ISO code: `config firewall address`, `edit "<CC>-Blocked"`, `set type geography`, `set country <CC>`, `next`, `end`
- ระวัง: traffic ที่มาจาก IP ในประเทศที่ถูกบล็อกอาจรวมถึง cloud provider / CDN ที่ใช้ IP ของประเทศนั้น

---

## 7. ใช้ address geography ใน firewall policy

คำค้น: geo-block policy, country filter, geo tag policy, blocked country policy
อาการ: ต้องนำ address geography ที่สร้างไปใช้กับ firewall policy เพื่อบล็อกหรืออนุญาต traffic จากประเทศเฉพาะ

คำสั่งตรวจ:
```
get firewall policy
```
อ่านผล:
- ดูว่า firewall policy ใดบ้างที่มี srcaddr / dstaddr ที่ชี้ไปที่ address group ประเทศที่ถูกบล็อก
- ตรวจสอบลำดับ policy ว่า geo-block policy อยู่เหนือ policy อนุญาต traffic ทั่วไปหรือไม่

ที่มา: [config firewall policy — FortiOS 7.4 CLI Reference](https://docs.fortinet.com/document/fortigate/7.4.4/cli-reference/333889629/config-firewall-policy)

วิธีแก้:
- สร้าง geo-block policy: `config firewall policy`, `edit <policyid>`, `set action deny`, `set srcintf "wan"`, `set dstintf "internal"`, `set srcaddr "Blocked-Countries"`, `set dstaddr "all"`, `set service "ALL"`, `set schedule "always"`, `set status enable`, `next`, `end`
- geo-block policy ต้องอยู่เหนือ policy ที่อนุญาต traffic ทั่วไปเพื่อให้บล็อกก่อน
- หากต้องการ geo-block เฉพาะทิศทางเดียว (เช่น dstaddr เป็นประเทศ) ให้สลับ srcaddr/dstaddr
- ระวัง: ต้องตรวจสอบให้แน่ใจว่า policy ที่บล็อกอยู่ลำดับถูกต้อง — FortiGate match policy ตามลำดับ ID จากน้อยไปมาก
