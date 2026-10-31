---
id: fortigate-74-ssl-inspection
title: FortiGate 7.4 SSL Deep Inspection Certificate Exemption
families: fortinet_fortios
triggers: fortigate, fortios, deep inspection, ssl inspection, ssl-ssh-profile, certificate-inspection, ssl exempt
vendor: Fortinet
versions: FortiOS 7.4.0 — 7.4.14
sources: https://docs.fortinet.com/document/fortigate/7.4.2/administration-guide/929997/ssl-ssh-inspection
---
# FortiGate 7.4 SSL Deep Inspection Certificate Exemption

## SSL Inspection | certificate expired หรือ revoked ถูก block
คำค้น: ssl inspection, deep inspection, certificate expired, certificate revoked, ssl blocked website, https blocked after ssl inspection, ssl inspection blocked, expired-server-cert, revoked-server-cert
อาการ: ผู้ใช้เข้าเว็บไม่ได้หลังเปิด SSL inspection, browser แสดง NET::ERR_CERT_DATE_EXPIRED หรือ NET::ERR_CERT_REVOKED, SSL inspection block website ที่ certificate หมดอายุหรือถูกเพิกถอน
วิธีแก้:
- แก้ certificate action: `config firewall ssl-ssh-profile` → `edit custom-deep-inspection` → `set expired-server-cert allow`
- แก้ certificate action: `set revoked-server-cert allow`
- Set inspection level: `set inspect-all deep-inspection` หรือ `set inspect-all certificate-inspection`
- ผูก profile ใน policy: `config firewall policy` → `edit <id>` → `set ssl-ssh-profile "custom-deep-inspection"` (เอกสาร: SSL & SSH Inspection, FortiOS 7.4.2)
ที่มา: SSL & SSH Inspection (FortiOS 7.4.2) https://docs.fortinet.com/document/fortigate/7.4.2/administration-guide/929997/ssl-ssh-inspection

## SSL Inspection | certificate warning (Fortinet_CA_SSL ไม่ trusted)
คำค้น: certificate warning, untrusted certificate, ssl inspection blocked, untrusted-server-cert, Fortinet_CA_SSL, browser untrusted warning, certificate pinning, deep-inspection blocked
อาการ: ผู้ใช้ขึ้นเตือน untrusted certificate หลังเปิด SSL deep inspection, browser แสดงว่า certificate ไม่ trusted, HTTPS website เข้าไม่ได้, Apps ที่ใช้ certificate pinning ไม่ทำงาน
สาเหตุ:
1. Fortinet_CA_SSL ไม่อยู่ใน browser trusted CA list — FortiGate re-sign certificate แล้ว browser แสดง untrusted warning (เอกสาร: Deep inspection — Browser messages when using deep inspection, FortiOS 7.4.2)
2. Apps ที่ใช้ certificate pinning — certificate ที่ FortiGate re-sign ไม่ตรงกับ pin (เอกสาร: Exempt web sites from deep inspection, FortiOS 7.4.2)
วิธีแก้ certificate warning:
- เข้า GUI → Security Profiles → SSL/SSH Inspection → edit deep-inspection profile → Click Download (Fortinet_CA_SSL) → install ใน Trusted Root CA ของ client PC (เอกสาร: Deep inspection — Browser messages when using deep inspection, FortiOS 7.4.2)
วิธีแก้ certificate pinning:
- Exempt apps ที่ pin certificate: `config firewall ssl-ssh-profile` → `edit custom-deep-inspection` → `config ssl-exempt` → `edit <id>` → `set type address` → `set address "<pin-app-server>"` → `end` (เอกสาร: Exempt web sites from deep inspection, FortiOS 7.4.2)
ที่มา: Deep inspection (FortiOS 7.4.2) https://docs.fortinet.com/document/fortigate/7.4.2/administration-guide/122078/deep-inspection

## SSL Exemption | กำหนด site ที่ไม่ต้องผ่าน SSL inspection
คำค้น: ssl exemption, ssl exempt, bypass ssl inspection, ssl inspection bypass, certificate-not-after, certificate-not-before, exemption site, exempt ssl, ssl-exempt, wildcard-fqdn, fortiguard-category ssl exempt, exemption allowlist
อาการ: ต้องการให้เว็บไซต์บางแห่งไม่ต้องผ่าน SSL inspection, เว็บภายในที่ไม่มี certificate ผ่าน SSL inspection ไม่ได้, SSL inspection ช้าเพราะต้อง decrypt ทุกเว็บ
สาเหตุ:
1. เว็บภายในไม่มี certificate — ต้อง exempt (เอกสาร: Exempt web sites from deep inspection, FortiOS 7.4.2)
2. SSL inspection ช้า — ต้อง exempt เว็บที่ไม่จำเป็นต้อง decrypt (เอกสาร: Exempt web sites from deep inspection, FortiOS 7.4.2)
3. FortiGuard category ที่ไม่ต้องการ inspect (เอกสาร: Exempt web sites from deep inspection, FortiOS 7.4.2)
วิธีแก้:
- เพิ่ม exempt โดย FQDN: `config firewall ssl-ssh-profile` → `edit custom-deep-inspection` → `config ssl-exempt` → `edit 1` → `set type wildcard-fqdn` → `set wildcard-fqdn *.internal.local` → `end` (เอกสาร: Exempt web sites from deep inspection, FortiOS 7.4.2)
- เพิ่ม exempt โดย FortiGuard category: `config ssl-exempt` → `edit 2` → `set type fortiguard-category` → `set fortiguard-category <category-id>` → `end` (เอกสาร: Exempt web sites from deep inspection, FortiOS 7.4.2)
- เพิ่ม exempt โดย address: `config ssl-exempt` → `edit 3` → `set type address` → `set address "internal-servers"` → `end` (เอกสาร: Exempt web sites from deep inspection, FortiOS 7.4.2)
- Enable allowlist: `set allowlist enable` (เอกสาร: Configuring an SSL/SSH inspection profile, FortiOS 7.4.2)
ที่มา: SSL & SSH Inspection (FortiOS 7.4.2) https://docs.fortinet.com/document/fortigate/7.4.2/administration-guide/929997/ssl-ssh-inspection
