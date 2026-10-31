---
id: fortigate-74-ssl-inspection
title: FortiGate 7.4 SSL Deep Inspection Certificate Exemption
families: fortinet_fortios
triggers: ssl inspection, deep inspection, certificate warning, certificate expired, untrusted certificate, ssl exemption, ssl exempt, certificate-not-after, certificate-not-before, site certificate warning, web app blocked after ssl inspection, exemption site ssl, custom-deep-inspection, ssl-ssh-profile, certificate-inspection, ssl inspection not working, inspection blocked web
vendor: Fortinet
versions: FortiOS 7.4.0 — 7.4.14
sources: https://docs.fortinet.com/document/fortigate/7.4.2/administration-guide/929997/ssl-ssh-inspection
---
# FortiGate 7.4 SSL Deep Inspection Certificate Exemption

## SSL Inspection | ผู้ใช้ขึ้นเตือน certificate
คำค้น: ssl inspection, deep inspection, certificate warning, certificate expired, untrusted certificate, ssl blocked website, https blocked after ssl inspection, ssl inspection blocked, invalid certificate blocked, expired-server-cert, untrusted-server-cert, revoked-server-cert, cert-validation-failure, cert-validation-timeout, deep-inspection blocked, certificate-inspection blocked
อาการ: ผู้ใช้ขึ้นเตือน certificate expired, untrusted CA, revoked certificate หลังเปิด SSL deep inspection, HTTPS website เข้าไม่ได้, browser แสดง NET::ERR_CERT_*, SSL inspection block website ที่ certificate ไม่ถูกต้อง, ผู้ใช้เข้าถึงเว็บภายในที่ต้องใช้ self-signed certificate ไม่ได้
คำสั่งตรวจ:
```
get system firewall ssl-ssh-profile
```
อ่านผล:
- `get system firewall ssl-ssh-profile`: ดู ssl-ssh-profile ที่มีทั้งหมด — `certificate-inspection` (default, อ่าน header), `deep-inspection` (default, deep scan), `no-inspection` (default), `custom-deep-inspection` (แก้ไขได้)
- `config firewall ssl-ssh-profile "custom-deep-inspection"`: ดูการตั้งค่า — `inspect-all` (certificate-inspection / deep-inspection), `expired-server-cert` (default = block), `untrusted-server-cert` (default = allow), `revoked-server-cert` (default = block)
- `config firewall policy`: ดู ssl-ssh-profile ที่ผูกใน policy — ต้อง set profile ที่ต้องการ inspection
สาเหตุที่พบบ่อย:
1. `expired-server-cert = block` (default) — เว็บไซต์ certificate หมดอายุถูก block ทันที
2. `untrusted-server-cert = allow` (default) — certificate ที่ไม่ได้ลง CA ที่ trusted ถูก allow แต่บาง browser แสดง warning
3. `revoked-server-cert = block` (default) — certificate ที่ถูกเพิกถอนถูก block
4. Policy ไม่ผูก ssl-ssh-profile — traffic ไม่ผ่าน SSL inspection
วิธีแก้:
- เปิดดู ssl-ssh-profile: `config firewall ssl-ssh-profile` → `edit custom-deep-inspection`
- เปลี่ยน expired-server-cert = allow: `set expired-server-cert allow` (ถ้าต้องการเว็บ certificate หมดอายุให้ผ่านได้)
- เปลี่ยน revoked-server-cert = allow: `set revoked-server-cert allow` (ถ้าต้องการ certificate ที่ถูกเพิกถอนให้ผ่านได้)
- เปลี่ยน untrusted-server-cert = allow (default) — certificate ที่ไม่ trusted ให้ผ่านได้
- Set inspection level: `set inspect-all deep-inspection` (deep scan) หรือ `certificate-inspection` (ตรวจสอบ header เท่านั้น)
- ผูก profile ใน policy: `config firewall policy` → `edit <id>` → `set ssl-ssh-profile "custom-deep-inspection"`
ที่มา: SSL & SSH Inspection (FortiOS 7.4.2) https://docs.fortinet.com/document/fortigate/7.4.2/administration-guide/929997/ssl-ssh-inspection

## SSL Exemption | กำหนด site ที่ไม่ต้องผ่าน SSL inspection
คำค้น: ssl exemption, ssl exempt, bypass ssl inspection, ssl inspection bypass, certificate-not-after, certificate-not-before, exemption site, exempt ssl, ssl-exempt, wildcard-fqdn, fortiguard-category ssl exempt, ssl exemption log, exemption allowlist
อาการ: ต้องการให้เว็บไซต์บางแห่งไม่ต้องผ่าน SSL inspection, เว็บภายในที่ไม่มี certificate ผ่าน SSL inspection ไม่ได้, ต้องการ bypass SSL inspection สำหรับบาง FQDN, SSL inspection ช้าเพราะต้อง decrypt ทุกเว็บ
คำสั่งตรวจ:
```
get system firewall ssl-ssh-profile
```
อ่านผล:
- `config firewall ssl-ssl-profile "<name>"`: ดู `config ssl-exempt` — รายการ site ที่ exempt จาก SSL inspection
- แต่ละ exempt entry: ดู `type` (fortiguard-category / address / address6 / wildcard-fqdn / regex)
- `ssl-exemption-log`: ดูว่ามีการ log SSL exemption หรือไม่ (default = disable)
- `ssl-exemption-ip-rating`: IP-based URL rating สำหรับ exemption (default = enable)
- `ssl-handshake-log`: ดู handshake log สำหรับ troubleshooting
สาเหตุที่พบบ่อย:
1. เว็บภายในไม่มี certificate — ต้อง exempt ออกไปจาก SSL inspection
2. SSL inspection ช้า — ต้อง exempt เว็บที่ไม่จำเป็นต้อง decrypt
3. FortiGuard category ที่ไม่ต้องการ inspect — ต้อง exempt ตาม category ID
วิธีแก้:
- เปิด ssl-ssh-profile: `config firewall ssl-ssh-profile` → `edit custom-deep-inspection`
- เพิ่ม exempt โดย FQDN: `config ssl-exempt` → `edit 1` → `set type wildcard-fqdn` → `set wildcard-fqdn *.internal.local` → `end`
- เพิ่ม exempt โดย FortiGuard category: `config ssl-exempt` → `edit 2` → `set type fortiguard-category` → `set fortiguard-category 140` → `end` (ID 140 = Adult)
- เพิ่ม exempt โดย address: `config ssl-exempt` → `edit 3` → `set type address` → `set address "internal-servers"` → `end`
- Enable exemption log: `set ssl-exemption-log enable` (ดู log ที่ Security Fabric → Log Visualization → SSL Exemption)
- Enable allowlist: `set allowlist enable` (ใช้ FortiGuard allowlist สำหรับ exempt)
ที่มา: SSL & SSH Inspection (FortiOS 7.4.2) https://docs.fortinet.com/document/fortigate/7.4.2/administration-guide/929997/ssl-ssh-inspection
