---
id: fortigate-74-harden-system
title: FortiGate 7.4 Hardening Checklist: System Crypto, Logging, PSIRT
families: fortinet_fortios
triggers: fortigate hardening system, strong crypto ssl-static-key-ciphers, dh-params, private data encryption, ssl-min-proto-version, logging config, PSIRT security rating, diagnose autoupdate versions, fortigate strong crypto, fortigate ssl-static-key-ciphers, fortigate dh-params, fortigate disable weak ciphers, fortigate ssl-min-proto-version, fortigate TLS version, fortigate disable TLSv1, fortigate disable SSLv3, fortigate private data encryption, fortigate private key encryption, fortigate AES 128-bit encryption, fortigate logging config, fortigate log setting, fortigate local-in logging, fortigate syslog override, fortigate syslog setting, fortigate log server config, fortigate syslogd setting, fortigate syslog udp, fortigate PSIRT, fortigate security rating, fortigate check version, fortigate autoupdate versions, fortigate get system status
versions: FortiOS 7.4.x
sources: https://docs.fortinet.com/document/fortigate/7.4.0/cli-reference/001620/config-system-global, https://docs.fortinet.com/document/fortigate/7.4.0/best-practices/555436, https://docs.fortinet.com/document/fortigate/7.4.4/cli-reference/196223761/config-log-setting, https://docs.fortinet.com/document/fortigate/7.4.4/cli-reference/141516630/config-log-syslogd-setting, https://docs.fortinet.com/document/fortigate/7.4.2/administration-guide/292634/security-rating
---

# FortiGate 7.4 Hardening Checklist: System Crypto, Logging, PSIRT

คำค้น: fortigate hardening system, strong crypto ssl-static-key-ciphers, dh-params, private data encryption, ssl-min-proto-version, logging config, PSIRT security rating, diagnose autoupdate versions
อาการ: ต้องตรวจและแก้ไขการตั้งค่า crypto, logging, firmware update ของ FortiGate 7.4 ให้ปลอดภัย

---

## 1. เปิด Strong Crypto: SSL Static Key Ciphers + DH Params

คำค้น: fortigate strong crypto, fortigate ssl-static-key-ciphers, fortigate dh-params, fortigate disable weak ciphers
อาการ: ต้องปิด weak ciphers และเพิ่ม DH params เป็น 8192 เพื่อความปลอดภัยสูงสุด

คำสั่งตรวจ:
```
get system global
```
อ่านผล:
- ดูค่า `set strong-crypto` (default enable)
- ดูค่า `set ssl-static-key-ciphers` (default enable — ต้อง disable เพื่อความปลอดภัย)
- ดูค่า `set dh-params` (default 2048 — ต้องเปลี่ยนเป็น 8192)
ที่มา: [config system global — FortiOS 7.4 CLI Reference](https://docs.fortinet.com/document/fortigate/7.4.0/cli-reference/001620/config-system-global)
วิธีแก้:
- ปิด static key ciphers และเพิ่ม DH params เป็น 8192: `config system global`, `set strong-crypto enable`, `set ssl-static-key-ciphers disable`, `set dh-params 8192`, `end`
- **ระวัง:** การเปลี่ยน dh-params เป็น 8192 อาจส่งผลต่อ performance ของ HTTPS/SSH admin connection ในกรณีที่ device มี CPU ต่ำ — ต้องทดสอบก่อน

---

## 2. ตั้งค่า SSL/TLS Minimum Protocol Version

คำค้น: fortigate ssl-min-proto-version, fortigate TLS version, fortigate disable TLSv1, fortigate disable SSLv3
อาการ: ต้องตั้งค่า TLS minimum เป็น TLSv1.2 เพื่อป้องกัน protocol downgrade

คำสั่งตรวจ:
```
get system global
```
อ่านผล:
- ดูค่า `set ssl-min-proto-version` (default TLSv1.2)
- หากเป็น SSLv3 หรือ TLSv1 = ต้องเปลี่ยน
ที่มา: [config system global — FortiOS 7.4 CLI Reference](https://docs.fortinet.com/document/fortigate/7.4.0/cli-reference/001620/config-system-global)
วิธีแก้:
- ตั้งค่า TLS minimum เป็น TLSv1.2: `config system global`, `set ssl-min-proto-version TLSv1-2`, `end`

---

## 3. เปิด Private Data Encryption

คำค้น: fortigate private data encryption, fortigate private key encryption, fortigate AES 128-bit encryption
อาการ: ต้องเปิด private data encryption เพื่อเข้ารหัส password/certificate ที่เก็บใน FortiGate

คำสั่งตรวจ:
```
get system global
```
อ่านผล:
- ดูค่า `set private-data-encryption` (default disable)
- หากยังอยู่ใน default = ยังไม่ได้เปิด
ที่มา: [Hardening — FortiOS 7.4 Best Practices](https://docs.fortinet.com/document/fortigate/7.4.0/best-practices/555436)
วิธีแก้:
- เปิด private data encryption: `config system global`, `set private-data-encryption enable`, `end`
- **ระวัง:** เมื่อเปิด private data encryption แล้ว config backup จะเข้ารหัสด้วย — ต้องเก็บ encryption key ไว้ในที่ปลอดภัย (vault) — หากสูญเสีย key จะไม่สามารถ restore config ได้

---

## 4. ตั้งค่า System Logging

คำค้น: fortigate logging config, fortigate log setting, fortigate local-in logging, fortigate syslog override
อาการ: ต้องเปิด logging สำหรับ local-in policy, traffic, และ event ต่างๆ

คำสั่งตรวจ:
```
get log setting
```
อ่านผล:
- ดูว่า logging settings ใดถูกเปิดอยู่ (เช่น local-in-allow, local-in-deny-unicast, local-out)
- หาก local-out = enable = ถูกเปิดไว้แล้ว
ที่มา: [config log setting — FortiOS 7.4 CLI Reference](https://docs.fortinet.com/document/fortigate/7.4.4/cli-reference/196223761/config-log-setting)
วิธีแก้:
- ระวัง: `local-in-allow` และ `local-in-deny-broadcast` สร้าง log จำนวนมาก (ทุก ping / broadcast) เปิดเฉพาะตอนตรวจปัญหา หรือเช็กพื้นที่ log / license SIEM ก่อน
- เปิด logging สำหรับ local-in policies: `config log setting`, `set local-in-allow enable`, `set local-in-deny-unicast enable`, `set local-in-deny-broadcast enable`, `end`
- เปิด extended log สำหรับ traffic logging: `config log setting`, `set extended-log enable`, `set log-policy-comment enable`, `end`

---

## 5. ตั้งค่า Syslog Server

คำค้น: fortigate syslog setting, fortigate log server config, fortigate syslogd setting, fortigate syslog udp
อาการ: ต้องเชื่อม FortiGate กับ syslog server (เช่น QRadar / Splunk) สำหรับ centralized logging

คำสั่งตรวจ:
```
get log syslogd setting
```
อ่านผล:
- ดูว่า syslog server ถูกตั้งค่าไว้หรือไม่
- ดูว่า `set status` เป็น enable หรือ disable
- ดูว่า `set mode` เป็น udp หรือ legacy-reliable
ที่มา: [config log syslogd setting — FortiOS 7.4 CLI Reference](https://docs.fortinet.com/document/fortigate/7.4.4/cli-reference/141516630)
วิธีแก้:
- ตั้งค่า syslog server: `config log syslogd setting`, `set status enable`, `set server "<syslog-server-IP>"`, `set port 514`, `set mode udp`, `set facility local0`, `end`
- ส่งแบบเข้ารหัส TLS (ปลายทางต้องรับ syslog-TLS ได้ ปกติ TCP 6514): `config log syslogd setting`, `set mode reliable`, `set enc-algorithm high`, `set port 6514`, `set ssl-min-proto-version TLSv1-2`, `end`
- ระวัง: `set mode` ต้องตรงกับฝั่ง SIEM (QRadar รับ UDP 514 เป็นค่าเริ่มต้น) เปลี่ยนแล้ว log จะหายถ้าปลายทางไม่รองรับ

---

## 6. ตรวจ PSIRT / Security Rating / Firmware Version

คำค้น: fortigate PSIRT, fortigate security rating, fortigate check version, fortigate autoupdate versions, fortigate get system status
อาการ: ต้องตรวจว่า firmware version ล่าสุดมี vulnerability ที่ยังไม่ patch หรือไม่

คำสั่งตรวจ:
```
get system status
diagnose autoupdate versions
```
อ่านผล:
- `get system status` แสดง firmware version, uptime, HA status
- `diagnose autoupdate versions` แสดง Security Rating Package version และ contract expiry
- หาก Security Rating Package มี status ที่แสดง license ไม่ valid = ต้องต่อ license
ที่มา: [Security rating — FortiOS 7.4 Administration Guide](https://docs.fortinet.com/document/fortigate/7.4.2/administration-guide/292634/security-rating)
วิธีแก้:
- ไปที่ GUI: **Security Fabric > Security Rating** เพื่อดูคะแนนและคำแนะนำ
- ตรวจสอบ PSIRT advisory ที่ [Fortinet Support](https://support.fortinet.com)
