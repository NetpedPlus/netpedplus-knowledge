---
id: fortigate-74-harden-admin
title: FortiGate 7.4 Hardening Checklist: Admin Access & Local-in
families: fortinet_fortios
triggers: fortigate hardening admin, trusted host config, admin MFA OTP, admin port change, allowaccess wan, local-in policy virtual-patch, fortigate trusted host, fortigate trusthost1, fortigate admin access restricted, fortigate MFA admin, fortigate two-factor authentication, fortigate OTP admin, fortigate fortitoken mobile admin, fortigate RSA admin, fortigate change admin port, fortigate admin-sport, fortigate admin-ssh-port, fortigate non-standard admin port, fortigate allowaccess wan, fortigate block https wan, fortigate restrict management interface, fortigate local-in policy, fortigate local-in check, fortigate local-in status, fortigate local-in list, fortigate local-in virtual-patch
versions: FortiOS 7.4.x
sources: https://docs.fortinet.com/document/fortigate/7.4.0/cli-reference/13620/config-system-admin, https://docs.fortinet.com/document/fortigate/7.4.0/cli-reference/001620/config-system-global, https://docs.fortinet.com/document/fortigate/7.4.2/cli-reference/297620/config-firewall-local-in-policy, https://docs.fortinet.com/document/fortigate/7.4.0/cli-reference/8620/config-system-interface, https://docs.fortinet.com/document/fortigate/7.4.4/cli-reference/196223761/config-log-setting
---

# FortiGate 7.4 Hardening Checklist: Admin Access & Local-in

คำค้น: fortigate hardening admin, trusted host config, admin MFA OTP, admin port change, allowaccess wan, local-in policy virtual-patch
อาการ: ต้องตรวจและแก้ไขการตั้งค่า admin access + local-in policy ของ FortiGate 7.4 ให้ปลอดภัย

---

## 1. ตรวจ Trusted Hosts ของผู้ดูแลระบบ

คำค้น: fortigate trusted host, fortigate trusthost1, fortigate admin access restricted, fortigate system admin trusthost
อาการ: ต้องจำกัด IP ที่ผู้ดูแลระบบเข้าได้จาก trusted hosts

คำสั่งตรวจ:
```
show system admin
```
อ่านผล:
- ดูว่า admin account ใดบ้างมี `set trusthost1` / `trusthost2` ... / `trusthost10`
- หากไม่มี = ผู้ดูแลระบบสามารถ login จาก IP ใดๆ (ถ้า allowaccess เปิดไว้)
- หากมี ให้ตรวจสอบว่า IP ที่กำหนดเป็น management subnet จริงหรือไม่
ที่มา: [config system admin — FortiOS 7.4 CLI Reference](https://docs.fortinet.com/document/fortigate/7.4.0/cli-reference/13620/config-system-admin)
วิธีแก้:
- กำหนด trusted hosts สำหรับ admin account ที่สำคัญ: `config system admin`, `edit "<admin_name>"`, `set trusthost1 <MGMT-subnet> 255.255.255.0`, `set trusthost2 <DR-subnet> 255.255.255.0`, `set trusthost3 <remote-branch> 255.255.255.0`, `next`, `end`
- บัญชีฉุกเฉิน (break-glass) ที่ไม่เปิด MFA ต้องมี trusthost จำกัดเสมอ และเก็บรหัสไว้ใน vault / ตู้นิรภัย
- ระวัง: ตั้ง trusthost ให้บัญชีที่กำลัง login อยู่ ต้องใส่ IP ของตัวเองด้วย ไม่งั้นจะหลุดและเข้าไม่ได้

---

## 2. เปิด Admin MFA: FortiToken / Email / SMS

คำค้น: fortigate MFA admin, fortigate two-factor authentication, fortigate OTP admin, fortigate fortitoken mobile admin, fortigate fortitoken cloud admin
อาการ: ต้องเปิด MFA สำหรับผู้ดูแลระบบทุก account

คำสั่งตรวจ:
```
show system admin
```
อ่านผล:
- ดูว่า admin account ใดบ้างมี `set two-factor fortitoken|fortitoken-cloud|email|sms`
- ไม่มีบรรทัด `two-factor` = ปิดอยู่ (ค่าเริ่มต้น disable)
ที่มา: [config system admin — FortiOS 7.4 CLI Reference](https://docs.fortinet.com/document/fortigate/7.4.0/cli-reference/13620/config-system-admin)
วิธีแก้:
- FortiToken (hardware / mobile ที่ลงทะเบียนในเครื่องแล้ว): `config system admin`, `edit "<admin_name>"`, `set two-factor fortitoken`, `set fortitoken <serial>`, `set email-to "<admin_email>"` (ใช้ส่ง activation code ของ mobile token), `next`, `end`
- FortiToken Cloud: `set two-factor fortitoken-cloud` แล้วเลือกช่องทางด้วย `set two-factor-authentication fortitoken|email|sms` (ต้องมี license FortiToken Cloud)
- Email OTP: `set two-factor email`, `set email-to "<admin_email>"` (เครื่องต้องตั้ง email server ได้)
- SMS: `set two-factor sms`, `set sms-server fortiguard`, `set sms-phone <phone-number>`
- ระวัง: ทำทีละบัญชี และเปิด session ที่ login ค้างไว้อีกหน้าต่างจนทดสอบ login ใหม่ผ่าน
- ระวัง: บัญชีฉุกเฉิน (break-glass) ที่ไม่เปิด MFA ต้องมี trusthost จำกัด และเก็บรหัสไว้ใน vault
- ระวัง: OTP แบบ token ต้องใช้เวลาตรงกัน ตรวจ NTP ก่อน

---

## 3. เปลี่ยน Admin Port (HTTPS / SSH)

คำค้น: fortigate change admin port, fortigate admin-sport, fortigate admin-ssh-port, fortigate non-standard admin port
อาการ: ต้องเปลี่ยน HTTPS/SSH admin port จาก default เพื่อลด automated attack

คำสั่งตรวจ:
```
get system global
```
อ่านผล:
- ดูค่า `set admin-sport` (HTTPS, default 443) และ `set admin-ssh-port` (SSH, default 22)
- หากยังอยู่ใน default port = ต้องเปลี่ยน
ที่มา: [config system global — FortiOS 7.4 CLI Reference](https://docs.fortinet.com/document/fortigate/7.4.0/cli-reference/001620/config-system-global)
วิธีแก้:
- เปลี่ยน HTTPS admin port เป็น 8443 และ SSH admin port เป็น 2222: `config system global`, `set admin-sport 8443`, `set admin-ssh-port 2222`, `end`
- **ระวัง:** ต้องบันทึก port ใหม่ใน documented runbook และแจ้งผู้ดูแลระบบทุกคน

---

## 4. ตั้งค่า Allowaccess บน WAN Interface

คำค้น: fortigate allowaccess wan, fortigate block https wan, fortigate restrict management interface, fortigate allowaccess list
อาการ: ต้องจำกัดบริการที่อนุญาตบน WAN interface ให้เฉพาะที่จำเป็น

คำสั่งตรวจ:
```
show system interface "<wan-interface>"
```
อ่านผล:
- ดูว่า interface WAN มี service อะไรใน `set allowaccess`
- หากมี `ping https ssh snmp http` ทั้งหมด = ต้องจำกัด
- หากมี `fgfm` (FortiManager) และ `radius-acct` = อาจจำเป็น
ที่มา: [config system interface — FortiOS 7.4 CLI Reference](https://docs.fortinet.com/document/fortigate/7.4.0/cli-reference/8620/config-system-interface)
วิธีแก้:
- เปิดเฉพาะที่จำเป็นบน WAN (ส่วนใหญ่ไม่ต้องมี https / ssh / http / snmp บน WAN ให้จัดการผ่าน interface ภายในหรือ MGMT แทน): `config system interface`, `edit "<wan-interface>"`, `set allowaccess ping`, `next`, `end`
- `set allowaccess` จะแทนที่ค่าเดิมทั้งหมด ต้องใส่ทุก service ที่ยังต้องใช้ในบรรทัดเดียว (เช่น `fgfm` ถ้าใช้ FortiManager ผ่าน WAN)
- **ระวัง:** การตั้งค่า allowaccess จะควบคุม traffic ที่เข้า interface แต่ไม่ควบคุม IPsec VPN (UDP 500/4500) — หากต้องการปิด IPsec บน WAN ให้ใช้ local-in policy

---

## 5. ตรวจสอบและตั้งค่า Local-in Policy

คำค้น: fortigate local-in policy, fortigate local-in check, fortigate local-in status, fortigate local-in list, fortigate local-in virtual-patch
อาการ: ต้องตรวจว่ามี local-in policy ที่ตั้งอยู่แล้วหรือไม่ และต้องเปิด virtual-patching

คำสั่งตรวจ:
```
show firewall local-in-policy
```
อ่านผล:
- หากไม่มี local-in policies = เข้าตัวเครื่องได้ทุก service ที่เปิดใน allowaccess
- หากมี local-in policy แล้ว ดูว่ามี `set virtual-patch enable` หรือไม่
ที่มา: [config firewall local-in-policy — FortiOS 7.4 CLI Reference](https://docs.fortinet.com/document/fortigate/7.4.2/cli-reference/297620)
วิธีแก้:
- สร้าง local-in policy เพื่อจำกัดบริการที่เข้าถึง FortiGate จาก WAN (ตัวอย่าง: อนุญาตเฉพาะ HTTPS จาก trusted subnet): `config firewall address`, `edit "MGMT-SUBNET"`, `set subnet <MGMT-IP> 255.255.255.0`, `next`, `end`, `config firewall local-in-policy`, `edit 1`, `set intf "wan-interface"`, `set srcaddr "MGMT-SUBNET"`, `set dstaddr "all"`, `set service "HTTPS" "SSH"`, `set action accept`, `set schedule "always"`, `set virtual-patch enable`, `next`, `edit 2`, `set intf "wan-interface"`, `set srcaddr "all"`, `set dstaddr "all"`, `set service "HTTPS" "SSH" "SNMP" "HTTP"`, `set action deny`, `set schedule "always"`, `next`, `end`
- `virtual-patch` ใส่ใน policy ที่ accept (ตรวจ traffic ที่ยอมให้เข้า admin) ไม่มีผลกับ policy deny
- ลำดับสำคัญ: local-in ตรงข้อแรกแล้วหยุด ต้องวาง accept จาก MGMT ก่อน deny
- เปิด log เพื่อติดตามการถูก deny: `config log setting`, `set local-in-deny-unicast enable`, `end`
- **ระวัง:** local-in policy จะตัด traffic ที่เข้าตัว FortiGate เอง (ไม่ใช่ traffic ที่ไหลผ่าน) — ดังนั้นการตั้งค่าผิดอาจทำให้ HA heartbeat, BGP, OSPF, IPsec, FortiGuard, FortiAnalyzer ขาดการเชื่อมต่อ — ห้ามใช้ `deny all` บน `intf any`

---
