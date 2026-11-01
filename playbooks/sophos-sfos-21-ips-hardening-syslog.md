---
title: Sophos XGS / IPS / Hardening / Syslog
id: sophos-sfos-21-ips-hardening-syslog
topics: 5
families: sophos_sfos
equipment: Sophos XGS 5500
versions: SFOS 21.5
sources: https://docs.sophos.com/nsg/sophos-firewall/21.0/api/protect/intrusion%20prevention/ipspolicy/operations/AddIPSpolicy&UpdateIPSPolicy.html, https://docs.sophos.com/nsg/sophos-firewall/21.0/api/configure/system%20services/syslogservers/operations/AddSyslogServers&UpdateSyslogServers.html, https://www.avanet.com/en/kb/sophos-firewall-secure-access-device-access/, https://www.avanet.com/en/kb/sophos-firewall-mfa-webadmin-vpn/, https://docs.sophos.com/nsg/sophos-firewall/21.5/Help/en-us/webhelp/onlinehelp/AdministratorHelp/IntrusionPrevention/IPSPolicies/IPSAddRulesToPolicy/index.html
triggers: IPS policy, false positive IPS, device access hardening, admin 2FA, send log to SIEM, syslog Sophos
---

# Sophos XGS / IPS / Hardening / Syslog

อุปกรณ์: Sophos XGS 5500
SFOS: 21.5

## IPS policy / เลือก/ผูกกับ firewall rule

IPS policy เป็นแพทเทิร์นการตรวจจับ attack signatures ที่ผูกเข้ากับ firewall rule
IPS policy ไม่ทำงานถ้าไม่ได้ผูกกับ firewall rule (policies set to None ใน firewall rule)

คำค้น:
- สร้าง IPS policy ใหม่
- ผูก IPS policy กับ firewall rule
- IPS policy ไม่ทำงาน
- IPS false positive
- IPS log ไม่ขึ้น

ที่มา: https://docs.sophos.com/nsg/sophos-firewall/21.0/api/protect/intrusion%20prevention/ipspolicy/operations/AddIPSpolicy&UpdateIPSPolicy.html
      https://docs.sophos.com/nsg/sophos-firewall/21.5/Help/en-us/webhelp/onlinehelp/AdministratorHelp/IntrusionPrevention/IPSPolicies/IPSAddRulesToPolicy/index.html

คำสั่งตรวจ:
ตรวจใน GUI: ไปที่ Intrusion prevention > IPS policies — ต้องเห็น policy ที่มี signature rules
ตรวจใน GUI: ไปที่ Firewall > Firewall rules — rule ที่ต้องการให้ IPS ทำงานต้องมี IPS policy ที่เลือกไว้ (ไม่ใช่ None)
ตรวจใน GUI: ไปที่ Log viewer > IPS — ต้องเห็น signature ที่ถูก trigger

วิธีแก้:
1. ไปที่ Intrusion prevention > IPS policies > New — ตั้งชื่อ policy
2. เพิ่ม signature rules ลง policy — เลือก individual signature หรือ select all แล้วใช้ smart filter
   - filter ตาม category / severity / platform / target
   - เลือก action สำหรับแต่ละ rule ตามชื่อจริงของ Sophos:
     - Recommended: ใช้ action ตามที่ signature แนะนำ
     - Allow packet: ปล่อย packet ที่ผ่าน
     - Drop packet: ตัด packet ที่ตรวจพบ
     - Disable: ปิด signature นั้น (ไม่ตรวจ traffic ด้วย signature นี้)
     - Drop session: ตัด session ทั้งหมด
     - Reset: ตัด session และส่ง TCP reset ไปที่ originator
     - Bypass session: อนุญาต traffic และไม่ตรวจ signature ต่อใน session นั้น
   - ถ้าเจอ false positive: ถ้าต้องการไม่ตรวจ signature นี้เลยให้ใช้ Disable (ไม่ block แต่หยุดตรวจ) / ถ้าต้องการ block ให้ใช้ Drop packet
   - ตรวจผลใน log: ไปที่ Log viewer > IPS ดูว่า action ทำงานตามที่ต้องการ
3. ผูก policy กับ firewall rule — ไปที่ Firewall > Firewall rules > เลือก rule > Policies > IPS policy เลือก policy ที่สร้างไว้ (ไม่ใช่ None)
4. ระวัง: signature-based IPS ไม่ตรวจจับ encryption (HTTPS) ได้โดยตรง — traffic HTTPS ต้องใช้ SSL/TLS inspection ก่อน
5. ตรวจว่า IPS ทำงานจริง — ไปที่ Log viewer > IPS — ดูว่า signature ที่ตั้งใจ monitor ถูก log

## Hardening การเข้าถึงตัวเครื่อง / Device access ต่อ zone

Device access เป็นหน้าควบคุมว่า service ใด (Web Admin HTTPS, SSH CLI, User Portal ฯลฯ) อนุญาตให้เข้าถึงจาก zone ใดได้บ้าง
Device access ไม่ใช่ firewall rule — ไม่สามารถควบคุมผ่าน firewall rule ได้
การ hardening device access เป็นขั้นตอนพื้นฐานที่จำเป็นสำหรับทุก firewall

จดพอร์ตที่ใช้ก่อนปิด WAN access — Administration > Admin and user settings:
 WebAdmin TCP 4444, User Portal TCP 4443, VPN Portal TCP 443, SSL VPN TCP 8443 (ค่าเริ่มต้นตาม Avanet)

คำค้น:
- Device access hardening
- ปิด WAN access Web Admin
- Local service ACL exception
- admin profile

ที่มา: https://www.avanet.com/en/kb/sophos-firewall-secure-access-device-access/
      https://docs.sophos.com/nsg/sophos-firewall/21.5/Help/en-us/webhelp/onlinehelp/AdministratorHelp/Administration/DeviceAccess/index.html

คำสั่งตรวจ:
ตรวจใน GUI: ไปที่ Administration > Device access — ต้องเห็นว่า HTTPS/SSH เปิดเฉพาะ zone ที่ต้องการ (เช่น LAN) ไม่ใช่ WAN
ตรวจใน GUI: ไปที่ Administration > Device access > Local service ACL exception rule — ต้องเห็น rule เฉพาะ IP admin ที่อนุญาตเข้าถึงจาก WAN
ตรวจใน GUI: ไปที่ Profiles > Device access — ต้องเห็น admin profile ที่แยกบทบาท

วิธีแก้:
1. ปิด WAN access สำหรับ HTTPS และ SSH — ไปที่ Administration > Device access แล้วยกเลิกเลือก WAN สำหรับ HTTPS และ SSH (เปิดเฉพาะ LAN / DMZ ที่จำเป็น)
2. เปิด Local service ACL exception rule สำหรับ admin ที่ต้องเข้าถึงจากภายนอก — ไปที่ Administration > Device access > Local service ACL exception rule > Add
   - เลือก rule position: Top
   - Source zone: WAN
   - Source network/host: ใช้ IP admin โดยตรง (ห้ามใช้ Any / 0.0.0.0 — Sophos ไม่อนุญาต)
   - Destination host: IP ของ firewall ที่ใช้เข้าจัดการ (ห้ามเป็น Any)
   - Services: เลือก HTTPS
   - Action: Accept
   - สำหรับ mobile users ที่ source address เปลี่ยนแนะนำให้ใช้ VPN แทนการเปิด WAN access
3. สร้าง admin profile เฉพาะหน้าที่ — ไปที่ Profiles > Device access > New
   - เลือกสิทธิ์ตามหน้าที่ (read-only, full administrator, network administrator ฯลฯ)

## Admin 2FA / public key authentication

เปิด 2FA (MFA) สำหรับ admin และเปิด public key authentication สำหรับ SSH CLI

คำค้น:
- admin 2FA MFA
- public key SSH admin
- token MFA software hardware

ที่มา: https://www.avanet.com/en/kb/sophos-firewall-mfa-webadmin-vpn/
      https://docs.sophos.com/nsg/sophos-firewall/21.5/Help/en-us/webhelp/onlinehelp/AdministratorHelp/Authentication/OneTimePassword/index.html
      https://docs.sophos.com/nsg/sophos-firewall/21.5/Help/en-us/webhelp/onlinehelp/AdministratorHelp/Administration/DeviceAccess/index.html

คำสั่งตรวจ:
ตรวจใน GUI: ไปที่ Administration > Device access — MFA ต้องเปิดสำหรับ default admin
ตรวจใน GUI: ไปที่ Authentication > Multi-factor authentication — ต้องเห็น web admin console ถูกเลือกเป็น MFA service

วิธีแก้:
1. MFA สำหรับ admin ทั่วไป — ไปที่ Authentication > Multi-factor authentication
   - เลือก Specific users and groups (ทดสอบก่อน, ใช้ All users เฉพาะหลังทดสอบแล้ว)
   - Enable Generate OTP token with next sign-in สำหรับ authenticator app
   - Require MFA for: เลือก Web admin console
      หมายเหตุ: รายการ Require MFA for (VPN portal, SSL VPN, IPsec remote access, Web application firewall) มาจากเอกสาร SFOS 22 — ต้องตรวจสอบว่ามีใน 21.5 ก่อนใช้งานจริง
   - Apply แล้วทดสอบด้วย pilot group
2. MFA สำหรับ default admin — ไปที่ Administration > Device access
   - เปิด MFA สำหรับ default admin, เลือก token method
   - software token: สแกน QR code ด้วย authenticator app
   - hardware token: กรอก key ของ hardware token
   - Validate แล้ว Apply
   - ถ้า token หายถาวร (มือถือหาย): CLI Main Menu > 2. System Configuration ตัวเลือก 7 (reset MFA)
   - ถ้า token ใช้ไม่ได้ชั่วคราว: ตัวเลือก 6 (login WebAdmin ครั้งเดียวไม่ต้อง MFA สำหรับ default admin)
3. เปิด public key authentication สำหรับ SSH — ไปที่ Administration > Device access
   - เปิด Enable authentication สำหรับ public key
   - หมายเหตุ: public key authentication ตั้งได้เฉพาะ default admin (admin account)
   - ตรวจชนิด key ที่รองรับกับเวอร์ชันที่ใช้ก่อน — แล้วกรอก authorized keys: RSA >= 2048 bits, DSA >= 2048 bits, ECDSA (ไม่ใช้ ED25519)
   - สร้าง key pair ด้วย PuTTYgen, paste public key, Apply
   - Admin เข้า SSH ด้วย private key

## ส่ง log ไป SIEM ผ่าน syslog / เปิด log ใน firewall rule และ Log settings

Sophos Firewall ส่ง event log ไป syslog server สำหรับเก็บ log ศูนย์กลาง
ส่ง log ทำ 2 ขั้นตอน: เปิด log ใน firewall rule + เลือก log type ใน Log settings

คำค้น:
- เปิด log firewall rule
- Sophos log settings
- log ไม่ออก syslog
- IPS log ไม่ขึ้น SIEM

ที่มา: https://docs.sophos.com/nsg/sophos-firewall/21.0/api/configure/system%20services/syslogservers/operations/AddSyslogServers&UpdateSyslogServers.html
      https://docs.sophos.com/nsg/sophos-firewall/21.5/Help/en-us/webhelp/onlinehelp/AdministratorHelp/SystemServices/LogSettings/index.html

คำสั่งตรวจ:
ตรวจใน GUI: ไปที่ Firewall > Firewall rules > rule ที่ต้องการ log — ต้องเลือก Log firewall traffic
ตรวจใน GUI: ไปที่ System services > Log settings — ต้องเห็น syslog server ที่กำหนด
ตรวจใน GUI: ไปที่ Log viewer — ต้องเห็น log traffic ที่ log ไว้

วิธีแก้:
1. เปิด log ใน firewall rule — ไปที่ Firewall > Firewall rules > เลือก rule > ติ๊ก Log firewall traffic
   - rule ที่ไม่ติ๊กนี้จะไม่ log traffic ที่ผ่าน rule (แม้ Log settings จะเปิดไว้)
   - สำหรับ SSL/TLS inspection rule — เลือก Log connections แทน
2. ไปที่ System services > Log settings — เลือก log type ที่ต้องการ log (ชื่อตาม Sophos):
   - Security policy: traffic matching firewall rules, MAC filtering, DoS
   - IPS: attack signatures ที่ถูก trigger
   - Anti-virus: virus ที่ตรวจพบ (HTTP, SMTP, FTP, IMAP, HTTPS ฯลฯ)
   - Anti-spam: spam ที่ตรวจพบ
   - Content filtering: web/application filtering events
   - Events: configuration changes, authentication, system events
   - Web server protection: WAF events
   - ATP: Advanced Threat Protection events
   - Zero-day protection: zero-day protection events
   - System health: CPU, memory, disk usage
   - Wireless: access point activity
3. ระวัง: firewall rule log + Log settings ต้องเปิดทั้งคู่ — rule ต้องเปิด log + Log settings ต้องเลือกส่ง category นั้นไป syslog (2 ชั้น)
4. ตรวจว่า log ปรากฏ — ไปที่ Log viewer — ดูว่ามี traffic log ที่ log ไว้

## เพิ่ม syslog server / ส่ง log ไป SIEM

Sophos Firewall ส่ง event log ไป syslog server สำหรับเก็บ log ศูนย์กลาง

คำค้น:
- เพิ่ม syslog server
- Sophos syslog server
- SIEM integration
- TLS syslog Sophos

ที่มา: https://docs.sophos.com/nsg/sophos-firewall/21.0/api/configure/system%20services/syslogservers/operations/AddSyslogServers&UpdateSyslogServers.html

คำสั่งตรวจ:
ตรวจใน GUI: ไปที่ System services > Log settings — ต้องเห็น syslog server ที่กำหนด (Name, IP, Port, Secure connection)

วิธีแก้:
1. ไปที่ System services > Log settings > scroll ลงมา
   - คลิก Add
   - กรอก syslog server details: Name, IP Address/Domain ของ SIEM, Port (1-65535)
   - Secure connection: Enable (ถ้า syslog server รองรับ TLS) หรือ Disable
   - Facility: DAEMON / KERNEL / USER / LOCAL0-LOCAL7
   - Severity Level: Emergency / Alert / Critical / Error / Warning / Notification / Information / Debug
   - Format: DeviceStandardFormat
   - เลือก log types ที่ต้องการส่งไป server นี้ (เลือกแยกตามหมวด เช่น Security policy / IPS / Anti-virus ฯลฯ)
   - ติ๊กส่ง log แต่ละหมวด (Enable/Disable) และ sub-category (เช่น IPS มี Anomaly / Signatures)
2. ตรวจว่าส่งออกจริง — ไปที่ Log viewer และตรวจสอบว่า syslog server ได้รับ log จาก IP ของ firewall