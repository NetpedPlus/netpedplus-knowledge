---
title: Sophos XGS / IPS / Hardening / Syslog
id: sophos-sfos-21-ips-hardening-syslog
topics: 3
families: sophos_sfos
equipment: Sophos XGS 5500
versions: SFOS 21.5
sources: https://docs.sophos.com/nsg/sophos-firewall/21.5/Help/en-us/webhelp/onlinehelp/AdministratorHelp/IntrusionPrevention/IPSPolicies/IPSPolicies/index.html, https://docs.sophos.com/nsg/sophos-firewall/21.5/Help/en-us/webhelp/onlinehelp/AdministratorHelp/Administration/DeviceAccess/index.html, https://docs.sophos.com/nsg/sophos-firewall/21.5/Help/en-us/webhelp/onlinehelp/AdministratorHelp/SystemServices/LogSettings/index.html
triggers: IPS policy, false positive IPS, device access hardening, admin 2FA, send log to SIEM, syslog Sophos
---

# Sophos XGS / IPS / Hardening / Syslog

อุปกรณ์: Sophos XGS 5500 (HA Active-Passive)
SFOS: 21.5

## IPS policy / เลือก/ผูกกับ firewall rule

IPS policy เป็นแพทเทิร์นการตรวจจับ attack signatures (เช่น CVE, exploit kits, botnet) ที่ผูกเข้ากับ firewall rule
IPS policy ไม่ทำงานถ้าไม่ได้ผูกกับ firewall rule (policies set to None ใน firewall rule)

คำค้น:
- สร้าง IPS policy ใหม่
- ผูก IPS policy กับ firewall rule
- IPS policy ไม่ทำงาน
- IPS false positive
- IPS log ไม่ขึ้น

ที่มา: https://docs.sophos.com/nsg/sophos-firewall/21.5/Help/en-us/webhelp/onlinehelp/AdministratorHelp/IntrusionPrevention/IPSPolicies/IPSPolicies/index.html
      https://docs.sophos.com/nsg/sophos-firewall/21.5/Help/en-us/webhelp/onlinehelp/AdministratorHelp/IntrusionPrevention/IPSPolicies/IPSAddRulesToPolicy/index.html

คำสั่งตรวจ:
ตรวจใน GUI: ไปที่ Intrusion prevention > IPS policies — ต้องเห็น policy ที่มี signature rules
ตรวจใน GUI: ไปที่ Firewall > Firewall rules — rule ที่ต้องการให้ IPS ทำงานต้องมี IPS policy ที่เลือกไว้ (ไม่ใช่ None)
ตรวจใน GUI: ไปที่ Logs > Event log > IPS — ต้องเห็น signature ที่ถูก trigger (ถ้า traffic ไปจริง)

วิธีแก้:
1. ถ้าไม่มี IPS policy ให้สร้าง — ไปที่ Intrusion prevention > IPS policies > New
2. เพิ่ม signature rules ลง policy — เลือก individual signature หรือ select all แล้วใช้ smart filter เจอ signature ที่ต้องการ
   - สามารถ filter ตาม category / severity / platform / target
   - เลือก action สำหรับแต่ละ rule: Recommended / Allow packet / Drop packet / Disable / Drop session / Reset / Bypass session
   - ถ้าเจอ false positive ให้เปลี่ยน action เป็น Disable signature (ไม่ block traffic แต่ log ไว้)
3. ผูก policy กับ firewall rule — ไปที่ Firewall > Firewall rules > เลือก rule > Policies > IPS policy เลือก policy ที่สร้างไว้ (ไม่ใช่ None)
4. ระวัง: IPS policy ถูก evaluate จากบนลงล่างของ signature rules — rule ที่อยู่บนก่อนจะจับก่อน
5. ระวัง: signature-based IPS ไม่ตรวจจับ encryption (HTTPS) ได้โดยตรง — traffic HTTPS ต้องใช้ SSL/TLS inspection ก่อน
6. ตรวจว่า IPS ทำงานจริง — ไปที่ Logs > Event log > IPS — ดูว่า signature ที่ตั้งใจ monitor ถูก log เมื่อ traffic เข้ามา

## Hardening การเข้าถึงตัวเครื่อง / Device access ต่อ zone

Device access เป็นหน้าควบคุมว่า service ใด (Web Admin HTTPS, SSH CLI, User Portal ฯลฯ) อนุญาตให้เข้าถึงจาก zone ใดได้บ้าง
Device access ไม่ใช่ firewall rule — ไม่สามารถควบคุมผ่าน firewall rule ได้
การ hardening device access เป็นขั้นตอนพื้นฐานที่จำเป็นสำหรับทุก firewall

คำค้น:
- Device access hardening
- ปิด WAN access Web Admin
- เปลี่ยนพอร์ต admin
- Local service ACL exception
- admin profile

ที่มา: https://docs.sophos.com/nsg/sophos-firewall/21.5/Help/en-us/webhelp/onlinehelp/AdministratorHelp/Administration/DeviceAccess/index.html
      https://docs.sophos.com/nsg/sophos-firewall/21.5/help/en-us/webhelp/onlinehelp/AdministratorHelp/Administration/DeviceAccess/DeviceAccessLocalServiceACL/index.html
      https://docs.sophos.com/nsg/sophos-firewall/21.5/Help/en-us/webhelp/onlinehelp/StartupHelp/SecurityBestPractices/SecurityHardening/index.html

คำสั่งตรวจ:
ตรวจใน GUI: ไปที่ Administration > Device access — ต้องเห็นว่า HTTPS/SSH เปิดเฉพาะ zone ที่ต้องการ (เช่น LAN) ไม่ใช่ WAN
ตรวจใน GUI: ไปที่ Administration > Device access > Local service ACL exception rule — ต้องเห็น rule เฉพาะ IP admin ที่อนุญาตเข้าถึงจาก WAN
ตรวจใน GUI: ไปที่ Profiles > Device access profiles — ต้องเห็น admin profile ที่แยกบทบาท (read-only, full access, network only ฯลฯ)

วิธีแก้:
1. ปิด WAN access สำหรับ HTTPS และ SSH — ไปที่ Administration > Device access แล้วยกเลิกเลือก WAN สำหรับ HTTPS และ SSH (เปิดเฉพาะ LAN / DMZ ที่จำเป็น)
2. เปิด Local service ACL exception rule สำหรับ admin ที่ต้องเข้าถึงจากภายนอก — ไปที่ Administration > Device access > Local service ACL exception rule > Add
   - เลือก rule position: Top
   - Source zone: WAN
   - Source network/host: สร้าง host object หรือใช้ IP admin โดยตรง
   - Destination host: Any
   - Services: เลือก HTTPS (หรือ SSH ตามต้องการ)
   - Action: Accept
3. สร้าง admin profile เฉพาะหน้าที่ — ไปที่ Profiles > Device access profiles > New
   - เลือกสิทธิ์ตามหน้าที่ (read-only, full administrator, network administrator ฯลฯ)
   - กำหนด Login restriction สำหรับ device access: จำกัด IP ที่ admin profile นี้เข้าได้

## Admin 2FA และ public key authentication

เปิด 2FA (MFA) สำหรับ admin และเปิด public key authentication สำหรับ SSH CLI

คำค้น:
- admin 2FA MFA
- public key SSH admin
- token MFA software hardware

ที่มา: https://docs.sophos.com/nsg/sophos-firewall/21.5/Help/en-us/webhelp/onlinehelp/AdministratorHelp/Authentication/OneTimePassword/index.html
      https://docs.sophos.com/nsg/sophos-firewall/21.5/Help/en-us/webhelp/onlinehelp/AdministratorHelp/Administration/DeviceAccess/index.html

คำสั่งตรวจ:
ตรวจใน GUI: ไปที่ Administration > Device access — MFA ต้องเปิดสำหรับ default admin

วิธีแก้:
1. เปิด MFA สำหรับ default admin — ไปที่ Administration > Device access
   - เปิด MFA สำหรับ default admin, เลือก token method
   - software token: สแกน QR code ด้วย authenticator app
   - hardware token: กรอก key ของ hardware token
   - Validate แล้ว Apply
   - สำคัญ: เก็บ passcode ไว้ใน password manager — ถ้ามือถือหายจะเข้าไม่ได้
2. เปิด public key authentication สำหรับ SSH — ไปที่ Administration > Device access
   - เปิด Enable authentication สำหรับ public key
   - กรอก authorized keys: RSA >= 2048 bits, DSA >= 2048 bits, ECDSA (ไม่ใช้ ED25519)
   - สร้าง key pair ด้วย PuTTYgen, paste public key, Apply
   - Admin เข้า SSH ด้วย private key (ไม่ใช่ password)
3. เปลี่ยน port admin — ไปที่ Administration > Device access
   - เปลี่ยน Web Admin port จาก 4443 เป็นพอร์ต custom (เช่น 8445)
   - เปลี่ยน SSH port จาก 22 เป็นพอร์ต custom (เช่น 2022)
   - ระวัง: SSL VPN port, User portal port, Captive portal port เปลี่ยนไม่ได้ (port คงที่ตามโปรโตคอล)
   - ระวัง: ถ้าเปลี่ยน SSL VPN port ไปเป็น 443 (เช่นเดียวกับ HTTPS) การเปิด WAN สำหรับ HTTPS จะเปิด SSL VPN ไปด้วย
4. ตรวจสอบ — เข้า Web Admin ด้วยพอร์ตใหม่ + MFA และ SSH ด้วยพอร์ตใหม่ + software token

## ส่ง log ไป SIEM ผ่าน syslog

Sophos Firewall ส่ง event log ไป syslog server ได้สูงสุด 5 ตัว
Syslog server ใช้ UDP port 514 (หรือ TLS ถ้ารองรับ)
ส่ง log ทำ 2 ขั้นตอน: เปิด log ใน firewall rule + เลือก log type ใน Log settings

คำค้น:
- ส่ง log SIEM syslog
- Sophos log settings
- log ไม่ออก syslog
- IPS log ไม่ขึ้น SIEM

ที่มา: https://docs.sophos.com/nsg/sophos-firewall/21.5/Help/en-us/webhelp/onlinehelp/AdministratorHelp/SystemServices/LogSettings/index.html

คำสั่งตรวจ:
ตรวจใน GUI: ไปที่ Firewall > Firewall rules > rule ที่ต้องการ log — ต้องเลือก Log firewall traffic
ตรวจใน GUI: ไปที่ System services > Log settings — ต้องเห็น syslog server ที่กำหนด (1-5 server)
ตรวจใน GUI: ไปที่ Logs > Event log — ต้องเห็น log traffic ที่ log ไว้

วิธีแก้:
1. เปิด log ใน firewall rule — ไปที่ Firewall > Firewall rules > เลือก rule > ติ๊ก Log firewall traffic
   - rule ที่ไม่ติ๊กนี้จะไม่ log traffic ที่ผ่าน rule (แม้ Log settings จะเปิดไว้)
   - สำหรับ SSL/TLS inspection rule — เลือก Log connections แทน
2. ไปที่ System services > Log settings — เลือก log type ที่ต้องการ log:
   - Firewall: traffic matching firewall rules, MAC filtering, DoS
   - IPS: attack signatures ที่ถูก trigger
   - Antivirus: virus ที่ตรวจพบ (HTTP, SMTP, FTP, IMAP ฯลฯ)
   - Events: configuration changes, authentication, system events
   - Content filtering: web/application filtering events
   - Anti-spam: spam ที่ตรวจพบ
   - Web server protection: WAF events
3. เพิ่ม syslog server — ไปที่ System services > Log settings > scroll ลงมา
   - คลิก Add
   - กรอก syslog server details: hostname / IP ของ SIEM, port (default 514 / UDP)
   - เลือก log types ที่ต้องการส่งไป server นี้ (เลือกแยกตามหมวด)
   - ถ้า SIEM รองรับ TLS ให้เปิด TLS connection — ต้องมี certificate ที่มี CN/SAN ตรงกับ hostname ของ syslog server
   - ถ้าใช้ LINCE mode (TLS) ต้องให้ certificate CN/SAN ตรงกับ domain ของ syslog server
4. ระวัง: firewall rule log ไม่เกี่ยวกับ syslog log settings — firewall rule ต้องเปิด log + Log settings ต้องเลือกส่ง category นั้นไป syslog (2 ชั้น)
5. ระวัง: log suppression — ถ้าเปิด Suppress logs ใน Log settings จะลดจำนวน log entries สำหรับหลายเหตุการณ์ (save space และ processing)
6. ตรวจว่าส่งออกจริง — ไปที่ Logs > Event log — ดูว่ามี traffic log ปรากฏใน SIEM หรือไม่
7. ระวัง: Sophos XGS 88/88w, 108/108w, 118/118w, 128/128w — ใช้ NPU-based FastPath ซึ่ง log จะออกจาก npu_syslog.log (ต่างจากเครื่องอื่นที่ใช้ syslog.log)
