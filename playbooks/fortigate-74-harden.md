---
id: fortigate-74-harden
title: FortiGate 7.4 Hardening Checklist: Trusted Hosts, Local-in Policy, Admin MFA, ปิด WAN Service, ตรวจ PSIRT
families: fortinet_fortios
triggers: fortigate hardening checklist, fortigate trusted host, fortigate local-in policy, fortigate admin MFA two-factor, ปิด service บน WAN port, fortigate check PSIRT security rating, fortigate wan port hardening, fortigate disable https ssh wan, fortigate virtual patching, fortigate HA hardening
versions: FortiOS 7.4.x
sources: https://docs.fortinet.com/document/fortigate/7.4.0/best-practices/555436/hardening, https://docs.fortinet.com/document/fortigate/7.4.1/administration-guide/14906/administrator-account-options, https://docs.fortinet.com/document/fortigate/7.4.4/administration-guide/363127/local-in-policy, https://docs.fortinet.com/document/fortigate/7.4.2/administration-guide/292634/security-rating
---

# FortiGate 7.4 Hardening Checklist

คำค้น: fortigate hardening, fortigate trusted host, fortigate local-in, fortigate admin MFA, fortigate two-factor, ปิด WAN port, fortigate PSIRT, fortigate security rating, fortigate virtual patching, fortigate wan hardening, fortigate disable service WAN, fortigate secure admin, fortigate password policy, fortigate strong crypto
อาการ: ต้องทำ hardening checklist ให้ FortiGate 7.4.x ตามมาตรฐานความปลอดภัย — ตั้ง trusted hosts, local-in policy, admin MFA, ปิด service บน WAN port, ตรวจ PSIRT vulnerability

---

## 1. ตรวจสภาพ hardening ปัจจุบัน

คำค้น: fortigate hardening status, fortigate security baseline, ตรวจ hardening FortiGate
อาการ: ต้องตรวจว่า hardening ต่างๆ ตั้งอยู่แล้วหรือไม่

คำสั่งตรวจ:
```
get system settings
get system administrator
get system interface "port1"
get router info config route
diagnose report-runner vuln-read
```
อ่านผล:
- `get system settings`: ดู strong-crypto, admin port, SNMP settings, auto-install (ต้อง disable)
- `get system administrator`: ดูผู้ดูแลทั้งหมด, profile, two-factor, trusted hosts, admin port, ssh
- `get system interface "port1"` (WAN): ดู allowaccess — ควรเป็น `ping` เท่านั้น หรือไม่มีเลย
- `diagnose report-runner vuln-read`: แสดงรายการ critical vulnerability ที่ตรวจพบ
- หาก allowaccess บน WAN มี `https ssh snmp http` = ยังไม่ได้ hardening WAN port
- หากผู้ดูแลไม่มี two-factor = ยังไม่ได้เปิด MFA
- หาก trusted host ของ admin = ยังไม่ได้จำกัด source IP
- หากมี critical vulnerability ใน vuln-read = ต้องอัปเดต firmware
ที่มา: [FortiOS Hardening — Best Practices](https://docs.fortinet.com/document/fortigate/7.4.0/best-practices/555436/hardening)
วิธีแก้:
- ดำเนินการตามขั้นตอนที่ 2–6 เพื่อ hardening ทั้งระบบ

---

## 2. ตั้ง Trusted Hosts สำหรับผู้ดูแลทุกคน

คำค้น: fortigate trusted host, fortigate admin trusted host, restrict admin source IP, fortigate restricted hosts, admin source IP
อาการ: ต้องจำกัด source IP ที่เข้าถึง admin panel (HTTPS / SSH / CLI)

คำสั่งตรวจ:
```
get system administrator
```
อ่านผล:
- ดูแต่ละ admin user ว่ามี `set trustedhost` หรือ `set trustedhost6` หรือไม่
- หากไม่มี trusted host = ผู้ดูแลสามารถ login จาก IP ใดๆ ที่เข้าถึงพอร์ตจัดการได้
ที่มา: [Administrator account options — Administrator account options](https://docs.fortinet.com/document/fortigate/7.4.1/administration-guide/14906/administrator-account-options)
วิธีแก้:
- สำหรับผู้ดูแลแต่ละคน (โดยเฉพาะ super_admin) ให้ตั้ง trusted host:
  ```
  config system admin
      edit "admin"
          set trustedhost <IP>/32
          set trustedhost <IP>/24
      next
      edit "backup-admin"
          set trustedhost <IP>/32
      next
  end
  ```
- ตั้ง trusted host ได้สูงสุด 10 host/subnet ต่อผู้ดูแล (IPv4 + IPv6)
- เมื่อ trusted host ถูกตั้งสำหรับการผู้ดูแลทุกคน การเข้าถึงทุก interface จะจำกัดเฉพาะ trusted host ที่ตั้งไว้ (ยกเว้น ping)
- **ระวัง:** ต้องตั้ง trusted host สำหรับผู้ดูแลทุกคนใน FortiGate เพื่อให้เกิดการจำกัดการเข้าถึงอย่างแท้จริง — หากมีผู้ดูแลคนใดไม่มี trusted host จะเปิดช่องให้เข้าถึงจาก IP ใดๆ ผ่านผู้ดูแลนั้น
- **ระวัง:** หากตั้งค่าแล้วแต่ยังเข้าถึงไม่ได้ ให้ตรวจสอบว่า IP ของคุณตรงกับ trusted host ที่ตั้งไว้หรือไม่ และตรวจสอบ firewall policy ระหว่างคุณกับ FortiGate

---

## 3A. ตรวจ Local-in Policy

คำค้น: fortigate local-in policy, fortigate local-in check, fortigate local-in status, fortigate local-in list
อาการ: ต้องตรวจว่ามี local-in policy ที่ตั้งอยู่แล้วหรือไม่

คำสั่งตรวจ:
```
get firewall local-in-policy
```
อ่านผล:
- หากไม่มี local-in policies = FortiGate ยังไม่ได้กำหนดกฎควบคุม traffic เข้า interface โดยตรง
- หากมี policy แล้ว ดูว่ามีการ deny PING/HTTPS/SSH/SNMP บน WAN interface หรือไม่
- หากมีแต่ไม่มีการ implicit deny rule ที่ด้านล่าง = อาจมีช่องโหว่
ที่มา: [Local-in policy — FortiOS 7.4.4 Admin Guide](https://docs.fortinet.com/document/fortigate/7.4.4/administration-guide/363127/local-in-policy)
วิธีแก้:
- ดูขั้นตอนที่ 3C

---

## 3B. Advanced Local-in: Geo-IP / ISDB Block

คำค้น: fortigate geo-ip local-in, fortigate ISDB local-in, fortigate bad country block, fortigate threat feed local-in, fortigate deny local-in
อาการ: ต้องบล็อก traffic เข้า FortiGate จากประเทศที่ไม่เกี่ยวข้อง หรือจาก threat feed

คำสั่งตรวจ:
```
get firewall address
get firewall local-in-policy
```
อ่านผล:
- ดูว่ามี address object ประเภท geo หรือ ISDB หรือไม่
- ดูว่ามี local-in policy ที่ใช้ geo/ISDB address เป็น srcaddr หรือไม่
ที่มา: [Local-in policy — FortiOS 7.4.4 Admin Guide](https://docs.fortinet.com/document/fortigate/7.4.4/administration-guide/363127/local-in-policy)
วิธีแก้:
- สร้าง Geo-IP address สำหรับประเทศที่ไม่เกี่ยวข้อง:
  ```
  config firewall address
      edit "Bad-Country"
          set type geo
          set country XX,YY
      next
  end
  ```
- สร้าง local-in policy สำหรับบล็อก geo-IP:
  ```
  config firewall local-in-policy
      edit 5
          set intf "wan-interface"
          set srcaddr "Bad-Country"
          set dstaddr "all"
          set service "ALL"
          set schedule "always"
          set action deny
      next
  end
  ```
- ใช้ ISDB (Internet Service Database) บล็อก traffic จาก malicious server:
  ```
  config firewall local-in-policy
      edit 6
          set intf "wan-interface"
          set internet-service-src enable
          set internet-service-src-name "Malicious-Malicious.Server"
          set service "ALL"
          set schedule "always"
          set action deny
      next
  end
  ```
- ใช้ IP address threat feed ใน local-in policy: ดู [Applying an IP address threat feed in a local-in policy](https://docs.fortinet.com/document/fortigate/7.4.4/administration-guide/891236/ip-address-threat-feed)

---

## 3C. วิธีแก้: สร้าง Local-in Policy สำหรับ WAN

คำค้น: fortigate local-in policy config, fortigate block WAN admin, fortigate local-in deny wan, fortigate WAN security policy, fortigate local-in policy example
อาการ: ต้องสร้าง local-in policy เพื่อปิด admin service บน WAN และจำกัดเฉพาะ trusted hosts

คำสั่งตรวจ:
```
get firewall local-in-policy
```
อ่านผล:
- หลังจากทำตามวิธีแก้แล้ว ให้รันคำสั่งนี้เพื่อตรวจสอบว่า policy ถูกสร้างแล้วหรือไม่
ที่มา: [Local-in policy — FortiOS 7.4.4 Admin Guide](https://docs.fortinet.com/document/fortigate/7.4.4/administration-guide/363127/local-in-policy)
วิธีแก้:
- สร้าง address object สำหรับ MGMT-SUBNET (trusted management network):
  ```
  config firewall address
      edit "MGMT-SUBNET"
          set subnet <management-ip> 255.255.255.0
          set allowedaccess "ping https ssh"
      next
  end
  ```
- สร้าง local-in policy เพื่อปฏิเสธ service ที่ไม่จำเป็นบน WAN:
  ```
  config firewall local-in-policy
      edit 1
          set intf "wan-interface"
          set srcaddr "all"
          set dstaddr "all"
          set service "HTTPS" "SSH" "SNMP" "HTTP" "PING"
          set schedule "always"
          set action deny
          set comments "Block all admin access on WAN"
      next
      edit 2
          set intf "wan-interface"
          set srcaddr "MGMT-SUBNET"
          set dstaddr "all"
          set service "HTTPS" "SSH"
          set schedule "always"
          set action accept
          set comments "Allow management from trusted subnet"
      next
      edit 3
          set intf "wan-interface"
          set srcaddr "MGMT-SUBNET"
          set dstaddr "all"
          set service "PING"
          set schedule "always"
          set action accept
          set comments "Allow ping from management subnet"
      next
      edit 4
          set intf "any"
          set srcaddr "all"
          set dstaddr "all"
          set service "ALL"
          set schedule "always"
          set action deny
          set comments "Implicit deny all local-in"
      next
  end
  ```
- **ระวัง:** implicit deny policy ต้องวางไว้ล่างสุดของรายการ local-in policies — หากไม่มี policy นี้ traffic ที่ไม่ตรงกับ policy ข้างบนจะ **ถูกปฏิเสธ** (default action = deny) เมื่อมี policy ใดๆ ถูกสร้างแล้ว
- **ระวัง:** การตั้งค่า local-in policy บน WAN interface อาจส่งผลต่อ HA heartbeat และ IPsec VPN หาก WAN เป็น interface ที่ใช้ทำ HA — ตรวจสอบว่า HA และ VPN ไม่ได้ใช้ WAN interface
- อนุญาตเฉพาะ HTTPS + SSH จาก management subnet เท่านั้น, ปิด PING บน WAN (ไม่จำเป็นต่อการใช้งาน), ปิด SNMP/HTTP ทั้งหมด

---

## 4. ปิด service บน WAN Interface (allowaccess)

คำค้น: fortigate disable wan port, fortigate wan security, fortigate allowaccess wan, fortigate no https ssh wan, fortigate wan hardening
อาการ: ต้องปิด HTTPS, SSH, HTTP, SNMP บน WAN port — ให้เหลือแค่ PING เท่านั้น

คำสั่งตรวจ:
```
get system interface "wan-port-name"
```
อ่านผล:
- ดูบรรทัด `set allowaccess ping https ssh snmp http` — หากมี `https ssh snmp http` แสดงว่ายังเปิดอยู่
- หากมีแต่ `ping` = ถูกต้องแล้ว
ที่มา: [FortiOS Best Practices — Hardening](https://docs.fortinet.com/document/fortigate/7.4.0/best-practices/555436/hardening)
วิธีแก้:
- สำหรับ WAN interface ทุกตัว ให้ลด allowaccess ให้เหลือเฉพาะ `ping`:
  ```
  config system interface
      edit "port1"  (WAN interface name)
          set allowaccess ping
      next
  end
  ```
- หรือหากต้องการเปิด HTTPS/SSH เฉพาะ management interface (เช่น port5 สำหรับ LAN management):
  ```
  config system interface
      edit "port1"
          set allowaccess ping
      next
      edit "port5"
          set allowaccess ping https ssh snmp
      next
  end
  ```
- **ระวัง:** หากเปิดใช้ VPN บน WAN interface (เช่น IPsec) ต้องยังคงเปิด UDP 500, UDP 4500, และ ESP protocol ไว้ — การปิดทั้งหมดจะทำให้ VPN หยุดทำงาน
- **ระวัง:** หากเปิดใช้ SD-WAN health check (probes) บน WAN interface การปิด ICMP (PING) อาจทำให้ health check ล้ม — ตรวจสอบว่า health check ใช้ protocol ไหน
- หากใช้ FortiGate รุ่นที่มี management interface พิเศษ (เช่น MGMT port) ให้ใช้ port นี้แทน port ธรรมดาในการจัดการ — ไปที่ *Network > Interfaces* และเปิด `set allowaccess` เฉพาะบน management port

---

## 5. เปิด Admin MFA (Two-Factor Authentication)

คำค้น: fortigate MFA, fortigate two-factor, fortigate 2FA, fortigate admin MFA, fortigate fortitoken MFA, fortigate admin authentication
อาการ: ต้องเปิด MFA สำหรับผู้ดูแลทุกคน เพื่อป้องกัน credential theft

คำสั่งตรวจ:
```
get system administrator
```
อ่านผล:
- ดูแต่ละ admin user ว่ามี `set two-factor` หรือไม่มี
- หาก `two-factor` = ยังไม่ได้เปิด MFA — ต้องเปิด
- หากมีแต่ไม่ได้ตั้งค่า fortitoken/email/sms อย่างถูกต้อง = ต้องตรวจสอบการตั้งค่า
ที่มา: [Administrator account options — Administrator account options](https://docs.fortinet.com/document/fortigate/7.4.1/administration-guide/14906/administrator-account-options)
วิธีแก้:
- **ก่อนเปิด MFA:** ต้องสร้างผู้ดูแลสำรองที่ **ไม่มี** MFA เพื่อไว้กู้คืนกรณี MFA ล้มเหลว (สำคัญมาก — หากเปิด MFA แล้ว reset token จะไม่สามารถ login ได้)
  ```
  config system admin
      edit "emergency-admin"
          set accprofile "super_admin"
          set trusthost1 <your-IP>/32
          set password \"<strong-password>\"
      next
  end
  ```
- สำหรับ MFA ด้วย FortiToken:
  ```
  config system admin
      edit "admin"
          set two-factor fortitoken
          set fortitoken <serial_number>
          set email-to "admin@company.com"
      next
  end
  ```
- สำหรับ MFA ด้วย FortiToken Cloud:
  ```
  config system admin
      edit "admin"
          set two-factor fortitoken-cloud
          set fortitoken-cloud <cloud_token_serial>
          set email-to "admin@company.com"
      next
  end
  ```
- สำหรับ MFA ด้วย Email (SMS หรือ email):
  ```
  config system admin
      edit "admin"
          set two-factor email
          set email-to "admin@company.com"
      next
  end
  ```
- สำหรับ MFA ด้วย SMS:
  ```
  config system admin
      edit "admin"
          set two-factor sms
          set sms-phone <phone-number>
      next
  end
  ```
- **ระวัง:** ก่อนเปิด MFA ต้องสร้าง emergency admin account ไว้แล้ว (ขั้นตอนแรก) — มิฉะนั้นจะ lock ตัวเองออกจาก FortiGate
- **ระวัง:** หากใช้ FortiToken จะต้องมี clock synchronization ผ่าน NTP เพื่อป้องกัน time-based OTP ไม่ตรงกัน

---

## 6. ตั้งค่า Strong Crypto และ Secure Password

คำค้น: fortigate strong crypto, fortigate encryption, fortigate cipher, fortigate ssl, fortigate dh params, fortigate password hash
อาการ: ต้องเปิดใช้งาน strong crypto, DH params 8192, และเข้ารหัสข้อมูลที่ละเอียดอ่อน

คำสั่งตรวจ:
```
get system global
```
อ่านผล:
- ดู `set strong-crypto` — ต้องเป็น `enable`
- ดู `set ssl-static-key-ciphers` — ต้องเป็น `disable` (ห้ามใช้ static key cipher)
- ดู `set dh-params` — ควรเป็น `8192`
ที่มา: [FortiOS Best Practices — Hardening](https://docs.fortinet.com/document/fortigate/7.4.0/best-practices/555436/hardening)
วิธีแก้:
- เปิด strong crypto และตั้งค่า cipher ที่ปลอดภัย:
  ```
  config system global
      set strong-crypto enable
      set ssl-static-key-ciphers disable
      set dh-params 8192
  end
  ```
- ตั้งค่า private data encryption key (optional แต่แนะนำ):
  ```
  config system global
      set private-data-encryption enable
  end
  ```
  (ระบบจะขอ hex key 32 หลัก — ใช้สำหรับเข้ารหัส config backup)
- **ระวัง:** หากใช้ `private-data-encryption` config backup จะ restore ได้เฉพาะบน FortiGate ที่มี key เดียวกันเท่านั้น — ให้เก็บ key ไว้ในสถานที่ปลอดภัย

---

## 7. ตั้งค่า Virtual Patching สำหรับ Local-in Management Interface

คำค้น: fortigate virtual patching, fortigate local-in virtual patch, fortigate mitigate CVE, fortigate emergency patch
อาการ: ต้องใช้ virtual patching เพื่อป้องกัน vulnerability เฉพาะที่กระทบ interface ที่เปิด admin

คำสั่งตรวจ:
```
get firewall local-in-policy
```
อ่านผล:
- ดูว่า local-in policy ใดๆ มี `set virtual-patch enable` หรือไม่
- หากไม่มี = ยังไม่ได้เปิด virtual patching
ที่มา: [Local-in policy — FortiOS 7.4.4 Admin Guide](https://docs.fortinet.com/document/fortigate/7.4.4/administration-guide/363127/local-in-policy)
วิธีแก้:
- เปิด virtual patching บน local-in policy ของ management interface:
  ```
  config firewall local-in-policy
      edit 1
          set intf "mgmt-interface"
          set virtual-patch enable
      next
  end
  ```
- Virtual patching จะ scan local-in traffic บน management interface และ drop traffic ที่ตรงกับ vulnerability rules
- **ระวัง:** virtual patching ใช้เฉพาะ local-in traffic ( traffic ไปยังตัว FortiGate เอง) — ไม่สามารถใช้ตรวจสอบ traffic ที่วิ่งผ่าน FortiGate (forwarding)
- **ระวัง:** virtual patching เป็น workaround ชั่วคราว — วิธีแก้ถาวรคืออัปเดต firmware ให้ล่าสุด

---

## 8. ตรวจ PSIRT และอัปเดต Firmware

คำค้น: fortigate PSIRT, fortigate security rating, fortigate critical vulnerability, fortigate firmware check, fortigate upgrade path
อาการ: ต้องตรวจว่า FortiGate มี critical vulnerability และต้องอัปเดต firmware

คำสั่งตรวจ:
```
execute version
diagnose report-runner vuln-read
diagnose autoupdate versions
get system information
```
อ่านผล:
- `execute version`: ดูเวอร์ชัน firmware ปัจจุบัน
- `diagnose report-runner vuln-read`: แสดงรายการ critical vulnerability (FG-IR-xxxx)
- `diagnose autoupdate versions`: ดู FortiGuard database versions
- หากมี output จาก `vuln-read` = มี critical vulnerability ที่ต้องอัปเดต
- หากไม่มี `Security Rating Data Package` หรือ expired = ต้อง renew license
ที่มา: [Security rating — FortiOS 7.4.2 Admin Guide](https://docs.fortinet.com/document/fortigate/7.4.2/administration-guide/292634/security-rating)
วิธีแก้:
- ตรวจสอบ vulnerability บน *Security Fabric > Security Rating*
- หากพบ critical vulnerability:
  - ไปที่ *System > Firmware & Registration* และตรวจสอบว่า license ของ PSIRT Package Definitions เป็น valid หรือไม่
  - หาก license valid: อัปเดต firmware เป็น patch version ล่าสุดของ minor version เดียวกัน (เช่น 7.4.x → 7.4.y)
  - หาก license ไม่ valid: ติดต่อ Fortinet support เพื่อ renew
- ตรวจสอบ PSIRT advisories บน <https://www.fortiguard.com/psirt> ว่ารุ่นที่ใช้อยู่มี CVE ใดๆ หรือไม่
- สำหรับ standalone FortiGate ให้เปิด automatic firmware updates:
  ```
  config system auto-update
      set firmware-update enable
      set firmware-version 7.4
  end
  ```
- สำหรับ HA cluster ให้ใช้ federated update (ผ่าน FortiManager หรือ manual upgrade ทั้งคู่)
- **ระวัง:** ก่อนอัปเดต firmware ต้อง backup config ทุกครั้ง และตรวจสอบ release notes ว่ามี known issues ที่กระทบระบบหรือไม่
- **ระวัง:** หาก upgrade cross minor version (เช่น 7.4 → 7.6) ต้องตรวจสอบ upgrade path ใน release notes — อาจต้อง upgrade ทีละ version

---

## 9. ปิด USB Firmware/Config Install (Physical Security)

คำค้น: fortigate disable USB, fortigate physical security, fortigate auto-install, fortigate unauthorized firmware
อาการ: ต้องปิดการติดตั้ง firmware/config ผ่าน USB เพื่อป้องกัน unauthorized access ทางกายภาพ

คำสั่งตรวจ:
```
get system auto-install
```
อ่านผล:
- หาก `auto-install-config` และ `auto-install-image` = `disable` = ถูกต้องแล้ว (ค่า default)
- หากค่าใดๆ = `enable` = ต้องปิด
ที่มา: [FortiOS Best Practices — Hardening](https://docs.fortinet.com/document/fortigate/7.4.0/best-practices/555436/hardening)
วิธีแก้:
- ปิด USB install ทั้ง config และ firmware:
  ```
  config system auto-install
      set auto-install-config disable
      set auto-install-image disable
  end
  ```
- **ระวัง:** ค่านี้เป็น `disable` โดย default — แต่หากมีผู้ดูแลเปลี่ยนค่าไว้ต้องตรวจสอบทุกครั้ง

---

## 10. ใช้ Encrypted Protocol แทน Plaintext

คำค้น: fortigate encrypted protocol, fortigate SNMPv3, fortigate SSH, fortigate LDAPS, fortigate SCP, fortigate RADSEC, fortigate NTP auth
อาการ: ต้องเปลี่ยนโปรโตکلที่ไม่เข้ารหัส (plaintext) ให้เป็นแบบเข้ารหัส

คำสั่งตรวจ:
```
get system global
get system ldap
show
get system radius
show
get system snmp community
show
```
อ่านผล:
- ดูว่า LDAP ใช้ port 389 (plaintext) หรือ 636 (LDAPS) — ต้องเป็น 636
- ดูว่า RADIUS ใช้ port 1812/1645 (plaintext) หรือ 18123 (RADSEC/TLS) — ควรเป็น 18123
- ดูว่า SNMP ใช้ community string (plaintext) — ต้องเป็น SNMPv3
- ดูว่า SSH เปิดอยู่ — ต้องใช้ SSHv2 เท่านั้น
ที่มา: [FortiOS Best Practices — Hardening](https://docs.fortinet.com/document/fortigate/7.4.0/best-practices/555436/hardening)
วิธีแก้:
- เปลี่ยน RADIUS เป็น RADSEC (port 18123/TLS):
  ```
  config system radius
      edit "NPS-Server"
          set port 18123
          set ssl min-version tls1-2
      next
  end
  ```
- เปลี่ยน LDAP เป็น LDAPS (port 636):
  ```
  config system ldap
      edit "AD-Server"
          set server <ldap-server-ip>
          set port 636
          set type enterpriseldap
          set ssl min-version tls1-2
      next
  end
  ```
- เปลี่ยน SNMP v2c เป็น SNMP v3 (มี encryption + authentication):
  ```
  config system snmp v3 user
      edit "zabbix"
          set auth-protocol sha256
          set auth-passphrase <strong-auth-pass>
          set privacy-protocol aes256
          set privacy-passphrase <strong-privacy-pass>
          set security-level auth-priv
      next
  end
  ```
- ใช้ NTP authentication:
  ```
  config system ntp
      edit "<server-name>"
          set ntpv3 enable
          set keyid <key-id>
      next
  end
  config system ntp authkey
      edit <key-id>
          set key <secret-key>
      next
  end
  ```
- ใช้ SCP แทน FTP/TFTP สำหรับ backup/restore ไฟล์

---

## 11. ตั้งค่า Non-Standard Admin Port

คำค้น: fortigate change admin port, fortigate custom https port, fortigate ssh port, fortigate non-standard port
อาการ: ต้องเปลี่ยน admin port จาก default (443, 22) เป็น port อื่นเพื่อลด attack surface

คำสั่งตรวจ:
```
get system global
```
อ่านผล:
- ดู `set https-port` — หากเป็น `443` = ยังเป็นค่า default
- ดู `set ssh-port` — หากเป็น `22` = ยังเป็นค่า default
ที่มา: [FortiOS Best Practices — Hardening](https://docs.fortinet.com/document/fortigate/7.4.0/best-practices/555436/hardening)
วิธีแก้:
- เปลี่ยน admin port เป็น port ที่ไม่ทั่วไป:
  ```
  config system global
      set https-port <custom-port>
      set ssh-port <custom-port>
  end
  ```
- เปลี่ยน admin username ที่ไม่ใช้ "admin":
  ```
  config system admin
      edit "admin"
          set accprofile "super_admin"
          set trusthost1 <your-IP>/32
      next
  end
  ```
- **ระวัง:** หากเปลี่ยน port ต้องอัปเดต URL ของ browser เป็น `https://<fgt-ip>:<custom-port>` และ SSH client ต้องระบุ port ใหม่
- **ระวัง:** firewall policy ระหว่างคุณกับ FortiGate ต้องอนุญาต traffic ไปยัง port ใหม่ด้วย

---

## 12. ตรวจ DoS Protection

คำค้น: fortigate DoS policy, fortigate anomaly protection, fortigate tcp_syn_flood, fortigate port scan, fortigate host protection
อาการ: ต้องเปิด DoS policy เพื่อป้องกัน DoS attacks

คำสั่งตรวจ:
```
get firewall dos-policy
get system global
```
อ่านผล:
- หากไม่มี DoS policies = ยังไม่ได้เปิด DoS protection
- ดูว่า `fortitrace-dos` log ถูกเปิดอยู่หรือไม่
ที่มา: [FortiOS Best Practices — Hardening](https://docs.fortinet.com/document/fortigate/7.4.0/best-practices/555436/hardening)
วิธีแก้:
- สร้าง DoS policy สำหรับป้องกัน anomaly:
  ```
  config firewall dos-policy
      edit 1
          set name "TCP-SYN-Flood"
          set srcaddr "all"
          set dstaddr "all"
          set service "ALL"
          set protocol 6  (TCP)
          config anomaly
              set tcp-syn-flood enable
          end
          set action monitor
      next
      edit 2
          set name "TCP-Port-Scan"
          set srcaddr "all"
          set dstaddr "all"
          set service "ALL"
          set protocol 6
          config anomaly
              set tcp-port-scan enable
          end
          set action monitor
      next
      edit 3
          set name "IP-Source-Session"
          set srcaddr "all"
          set dstaddr "all"
          set service "ALL"
          set protocol 6
          config anomaly
              set-ip-src-session enable
          end
          set action monitor
      next
  end
  ```
- หากมี NP6/NP7 ASIC เปิดอยู่ ให้ enable ASIC DoS offload:
  - NP6: ดู Hardware Acceleration Guide สำหรับ `np6 anomaly protection`
  - NP7: ดู `host protection engine (HPE)` ใน Hardware Acceleration Guide

---

## 13. ตรวจ Backup และ Configuration Security

คำค้น: fortigate backup encryption, fortigate config backup, fortigate secure backup, fortigate password masking
อาการ: ต้องตรวจว่า config backup ถูกเข้ารหัสหรือไม่

คำสั่งตรวจ:
```
get system backup
```
อ่านผล:
- ตรวจสอบว่า config backup มีการเข้ารหัส (encryption) หรือไม่
- ตรวจสอบว่ามี config backup เก่าที่ไม่ได้ใช้หรือไม่ — ต้องลบออก
ที่มา: [FortiOS Best Practices — Hardening](https://docs.fortinet.com/document/fortigate/7.4.0/best-practices/555436/hardening)

วิธีแก้:
- เปิด encryption เมื่อ backup config:
  ```
  config system backup
      set encryption enable
  end
  ```
- เปิด password masking เมื่อ backup:
  ```
  config system backup
      set password-masking enable
  end
  ```
- ลบ config backup เก่าที่ไม่ได้ใช้ — เก็บไว้แค่ version ล่าสุด
- หากใช้ `private-data-encryption` (ตั้งค่าแล้วในข้อ 6): เก็บ encryption key ไว้ในสถานที่ปลอดภัย — config backup จะ restore ได้เฉพาะบน FortiGate ที่มี key เดียวกัน

---

## 14. ตรวจ Log และ Monitoring

คำค้น: fortigate log hardening, fortigate remote syslog, fortigate security rating log, fortigate monitoring
อาการ: ต้องตรวจว่า log ถูกส่งไปยัง remote syslog/SIEM อย่างถูกต้อง และ security rating ถูกตรวจตาม schedule

คำสั่งตรวจ:
```
get log syslogd setting
get log eventfilter
diagnose report-runner status
```
อ่านผล:
- ดูว่า remote syslog ถูกตั้งค่าไว้หรือไม่ (SIEM เช่น QRadar)
- ดูว่า security rating event log ถูกเปิดอยู่หรือไม่
- ดูว่า local-in deny log ถูกเปิดอยู่หรือไม่
ที่มา: [Security rating — FortiOS 7.4.2 Admin Guide](https://docs.fortinet.com/document/fortigate/7.4.2/administration-guide/292634/security-rating)
วิธีแก้:
- เปิด local-in deny logging สำหรับ forensic analysis:
  ```
  config log setting
      set local-in-deny-unicast enable
  end
  ```
- เปิด security rating event log:
  ```
  config log eventfilter
      set security-rating enable
  end
  ```
- ตรวจสอบว่า remote syslog ส่ง log ไปยัง SIEM อย่างถูกต้อง (QRadar)
