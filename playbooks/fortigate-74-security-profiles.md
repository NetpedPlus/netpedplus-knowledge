---
id: fortigate-74-security-profiles
title: FortiGate 7.4 Security Profiles: IPS, AntiVirus, Application Control, DNS Filter
families:
triggers: fortigate security profile, fortigate IPS, fortigate antivirus, fortigate application control, fortigate DNS filter, fortigate profile group, fortigate security profiles, fortigate security profile สำหรับ server, fortigate false positive, ผูก security profile, สร้าง security profile, profile group, security profile ไม่จับ, false positive FortiGate, ตรวจลำดับ policy, fortigate move policy
versions: FortiOS 7.4.x
sources: https://docs.fortinet.com/document/fortigate/7.4.1/administration-guide/680955/security-profiles, https://docs.fortinet.com/document/fortigate/7.4.1/administration-guide/565562/intrusion-prevention, https://docs.fortinet.com/document/fortigate/7.4.1/administration-guide/929997/ssl-ssh-inspection, https://docs.fortinet.com/document/fortigate/7.4.4/cli-reference/333889629/config-firewall-policy, https://docs.fortinet.com/document/fortigate/7.4.1/administration-guide/419589/ips-configuration-options
---

# FortiGate 7.4 Security Profiles: IPS, AntiVirus, Application Control, DNS Filter

คำค้น: fortigate security profile, fortigate IPS, fortigate antivirus, fortigate application control, fortigate DNS filter, fortigate profile group, fortigate security profiles
อาการ: ต้องสร้างหรือแก้ไข security profiles (IPS, AntiVirus, Application Control, DNS Filter) บน FortiGate 7.4.x และผูกกับ firewall policy รวมถึงไล่ false positive

---

## 1. ตรวจ Security Profile ที่มีอยู่

คำค้น: fortigate security profile, fortigate IPS profile, fortigate AV profile, fortigate application list, fortigate DNS filter profile, ตรวจ profile ที่มี
อาการ: ต้องตรวจว่า security profiles มีอยู่แล้วหรือไม่
คำสั่งตรวจ:
```
show ips sensor
show antivirus profile
show application list
show dnsfilter profile
show firewall policy
```
อ่านผล:
- `show ips sensor`: แสดงรายการ IPS sensor profiles ทั้งหมด
- `show antivirus profile`: แสดงรายการ AV profiles ทั้งหมด
- `show application list`: แสดงรายการ application lists ทั้งหมด
- `show dnsfilter profile`: แสดงรายการ DNS filter profiles ทั้งหมด
- `show firewall policy`: แสดง policies ทั้งหมด พร้อม security profiles ที่ผูกอยู่ (av-profile, ips-sensor, application-list, dnsfilter-profile, profile-group, ssl-ssh-profile, utm-status, inspection-mode)
ที่มา: [config firewall policy — FortiOS 7.4.4 CLI Reference](https://docs.fortinet.com/document/fortigate/7.4.4/cli-reference/333889629/config-firewall-policy)
วิธีแก้:
- หากไม่มี profiles ที่ต้องการ ให้สร้างจากขั้นตอนถัดไป
- ตรวจสอบว่า policies มี security profiles ถูกผูกอยู่แล้วหรือไม่

---

## 2. สร้าง IPS Sensor Profile

คำค้น: fortigate IPS sensor, fortigate intrusion prevention, fortigate IPS profile, fortigate IPS sensor profile
อาการ: ต้องสร้าง IPS sensor profile ใหม่หรือเลือก profile ที่มี
คำสั่งตรวจ:
```
show ips sensor "<ชื่อ_sensor>"
```
อ่านผล:
- ต้องเห็น IPS sensor name, entries (signatures/filters) ที่เลือก, action ของแต่ละ entry
- ต้องเห็น setting เช่น block-malicious-url, comment
- หากไม่พบ = ยังไม่ได้สร้าง IPS sensor
ที่มา: [IPS configuration options — FortiOS 7.4.2 Admin Guide](https://docs.fortinet.com/document/fortigate/7.4.2/administration-guide/419589/ips-configuration-options)
วิธีแก้:
- FortiGate มี IPS sensors ที่กำหนดไว้ล่วงหน้า: `default`, `high_security`, `protect_client`, `protect_email_server`, `protect_http_server`, `all_default`, `all_default_pass`, `sniffer-profile`, `wifi-default`
- ใช้ `protect_http_server` สำหรับ server ใหม่: `config ips sensor`, `edit "IPS-Server"`, `set comment "Protect HTTP server"`, `set block-malicious-url enable`, `next`, `end`
- เพิ่ม signature filter ลงใน sensor: `config ips sensor`, `edit "IPS-Server"`, `config entries`, `edit 1`, `set rule 10001`, `set action block`, `set status enable`, `next`, `end`, `next`, `end`
- เพิ่ม filter โดย severity: `config ips sensor`, `edit "IPS-Server"`, `config entries`, `edit 2`, `set severity critical high medium`, `set action block`, `set status enable`, `next`, `end`, `next`, `end`
- ตัด signature ออกจาก sensor: `config ips sensor`, `edit "IPS-Server"`, `config entries`, `edit <filter-id>`, `set status disable`, `next`, `end`, `next`, `end`
- ระวัง: ใช้ `high_security` เป็นจุดเริ่มต้น แล้วค่อยๆ ปิด signatures ที่เกิด false positive

---

## 3. สร้าง Antivirus Profile

คำค้น: fortigate antivirus profile, fortigate AV profile, fortigate anti-virus
อาการ: ต้องสร้าง AV profile ใหม่หรือเลือก profile ที่มี
คำสั่งตรวจ:
```
show antivirus profile "<ชื่อ_av>"
```
อ่านผล:
- ต้องเห็น AV profile name, feature-set (proxy/flow), log setting, quarantine setting
- หากไม่พบ = ยังไม่ได้สร้าง AV profile
ที่มา: [FortiOS CLI Reference — AV section](https://docs.fortinet.com/document/fortigate/7.4.0/cli-reference/12848/file-filter)
วิธีแก้:
- FortiGate มี AV profiles ที่กำหนดไว้ล่วงหน้า: `default`
- ใช้ `default`: `config antivirus profile`, `edit "AV-Server"`, `set comment "AV for server traffic"`, `next`, `end`
- ระวัง: feature-set (proxy หรือ flow) ต้องตรงกับ inspection-mode ของ firewall policy

---

## 4. สร้าง Application List (Application Control)

คำค้น: fortigate application list, fortigate app-list, fortigate application control
อาการ: ต้องสร้าง Application List สำหรับควบคุมแอปพลิเคชันที่อนุญาต/บล็อกใน policy
คำสั่งตรวจ:
```
show application list "<ชื่อ_app_list>"
```
อ่านผล:
- ต้องเห็น application list name, entries (allow/deny/block rules)
- หากไม่พบ = ยังไม่ได้สร้าง application list
ที่มา: [FortiOS CLI Reference — Application section](https://docs.fortinet.com/document/fortigate/7.4.0/cli-reference/12848/file-filter)
วิธีแก้:
- FortiGate มี application lists ที่กำหนดไว้ล่วงหน้า: `default`, `block-high-risk`
- ใช้ `default`: `config application list`, `edit "App-List-Server"`, `set comment "Application list for server"`, `next`, `end`
- เพิ่ม rule ควบคุมแอป: `config application list`, `edit "App-List-Server"`, `config entries`, `edit 1`, `set category 12`, `set action pass`, `set status enable`, `next`, `end`, `next`, `end`
- `set category <id>` ใช้ category ID ของแอป (เช่น 12 = File Sharing)
- ดู application categories: `get system application control categories`

---

## 5. สร้าง DNS Filter Profile

คำค้น: fortigate DNS filter, fortigate dns filter profile, fortigate dnsfilter
อาการ: ต้องสร้าง DNS filter profile สำหรับควบคุม DNS queries
คำสั่งตรวจ:
```
show dnsfilter profile "<ชื่อ_dnsfilter>"
```
อ่านผล:
- ต้องเห็น DNS filter profile name, domain-filter-table, ftgd-dns settings (FortiGuard categories)
- หากไม่พบ = ยังไม่ได้สร้าง DNS filter profile
ที่มา: [config dnsfilter profile — FortiOS 7.4.1 CLI Reference](https://docs.fortinet.com/document/fortigate/7.4.1/cli-reference/490620/config-dnsfilter-profile)
วิธีแก้:
- FortiGate มี DNS filter profiles ที่กำหนดไว้ล่วงหน้า: `default`
- ใช้ `default`: `config dnsfilter profile`, `edit "DNS-Filter-Server"`, `set comment "DNS filter for server"`, `set block-botnet enable`, `next`, `end`
- ตั้งค่า FortiGuard DNS filter: `config dnsfilter profile`, `edit "DNS-Filter-Server"`, `config ftgd-dns`, `set options all`, `config filters`, `edit 1`, `set category 5`, `set action block`, `next`, `end`, `end`, `next`, `end`
- `set category <id>` ใช้ FortiGuard category ID (เช่น 5 = Adult)
- `set options all` = ใช้ทุก FortiGuard category ที่มีการตั้งค่า filter

---

## 6. สร้าง Profile Group (รวมหลาย security profiles)

คำค้น: fortigate profile group, fortigate security profile group
อาการ: ต้องสร้าง profile group เพื่อผูก security profiles หลายตัวพร้อมกันใน policy เดียว
คำสั่งตรวจ:
```
show firewall profile-group "<ชื่อ_profile_group>"
```
อ่านผล:
- ต้องเห็น profile group name, list of profiles ที่ผูก (av-profile, ips-sensor, application-list, dnsfilter-profile, webfilter-profile, ssl-ssh-profile, ฯลฯ)
- หากไม่พบ = ยังไม่ได้สร้าง profile group
ที่มา: [config firewall profile-group — FortiOS 7.4.0 CLI Reference](https://docs.fortinet.com/document/fortigate/7.4.0/cli-reference/12848/file-filter)
วิธีแก้:
- สร้าง profile group: `config firewall profile-group`, `edit "PG-Server"`, `set av-profile "AV-Server"`, `set ips-sensor "IPS-Server"`, `set application-list "App-List-Server"`, `set dnsfilter-profile "DNS-Filter-Server"`, `next`, `end`
- ตรวจสอบ profile group: `show firewall profile-group`
- ระวัง: profile-type ใน policy ต้องเป็น `group` ถ้าจะใช่ profile group

---

## 7. ผูก Security Profiles กับ Firewall Policy

คำค้น: fortigate security policy, fortigate firewall policy, fortigate policy สำหรับ server, fortigate ผูก profile, fortigate policy security profiles, fortigate security profile กับ policy, fortigate ผูก security profile กับ policy
อาการ: ต้องผูก security profiles กับ firewall policy ใหม่หรือ policy ที่มี
คำสั่งตรวจ:
```
show firewall policy
```
อ่านผล:
- ต้องเห็น policy name, srcintf, dstintf, srcaddr, dstaddr, service, action, security profiles ที่ผูกอยู่
- ต้องเห็น `utm-status`, `ssl-ssh-profile`, `inspection-mode` (flow หรือ proxy)
- หากไม่มี security profiles ผูก = traffic จะไม่ถูกตรวจสอบ
- หากไม่มี `ssl-ssh-profile` = IPS/AV จะไม่เห็นข้างใน HTTPS traffic
ที่มา: [config firewall policy — FortiOS 7.4.4 CLI Reference](https://docs.fortinet.com/document/fortigate/7.4.4/cli-reference/333889629/config-firewall-policy)
วิธีแก้:
- FortiGate ใช้ profile-based firewall policies เป็นค่าเริ่มต้น (ไม่ใช่ policy-based ที่ใช้ `config firewall security-policy`)
- ตรวจสอบโหมดด้วย: `get system settings | grep ngfw-mode`
- ถ้าค่าว่าง = profile-based (ใช้ `config firewall policy`), ถ้าเป็น `policy-based` = ใช้ `config firewall security-policy`
- สร้าง policy ใหม่พร้อม security profiles (ค่าเริ่มต้นคือ profile-based):
  ```
  config firewall policy
      edit <policy-id>
          set name "POLICY-SERVER-<ชื่อ>"
          set srcintf "<src-interface>"
          set dstintf "<dst-interface>"
          set srcaddr "<src-address>"
          set dstaddr "<server-address>"
          set service "HTTPS" "HTTP"
          set action accept
          set schedule "always"
          set utm-status enable
          set ssl-ssh-profile "deep-inspection"
          set inspection-mode flow
          set av-profile "AV-Server"
          set ips-sensor "IPS-Server"
          set application-list "App-List-Server"
          set dnsfilter-profile "DNS-Filter-Server"
          set logtraffic all
          next
  end
  ```
- หรือใช้ profile group แทน single profiles: `set profile-type group`, `set profile-group "PG-Server"` (ไม่ต้องระบุแต่ละ profile ทีละตัว)
- ระวัง: `utm-status` ต้องเป็น `enable` ถึงจะใช้ security profiles ได้

## 8. ตรวจลำดับ Policy / SSL-SSH Inspection

คำค้น: fortigate ตรวจลำดับ policy, fortigate move policy, fortigate ssl-ssh-profile, fortigate utm-status, fortigate inspection-mode, fortigate deep-inspection, fortigate certificate-inspection, fortigate fortigate-74-ssl-inspection
อาการ: ต้องตรวจลำดับ policy และ ssl-ssh-profile ก่อน deploy
คำสั่งตรวจ:
```
show firewall policy
```
อ่านผล:
- ต้องเห็นลำดับ policies (policy-id เรียงจากน้อยไปมาก)
- ต้องเห็น `ssl-ssh-profile` ผูกกับ policy (เช่น `deep-inspection`)
- หากไม่พบ ssl-ssh-profile = traffic HTTPS จะไม่ถูก IPS/AV ตรวจ
ที่มา: [SSL & SSH Inspection — FortiOS 7.4.2 Admin Guide](https://docs.fortinet.com/document/fortigate/7.4.2/administration-guide/929997/ssl-ssh-inspection)
วิธีแก้:
- ตรวจลำดับ policy: ใช้ `show firewall policy` ดูลำดับ
- ในโหมด CLI profile-based ให้ใช้คำสั่ง `move <policy-id> before <policy-id>` หรือ `move <policy-id> after <policy-id>` ใน `config firewall policy`
- `ssl-ssh-profile` ที่กำหนดไว้ล่วงหน้า: `certificate-inspection` (เห็นแค่ชื่อเว็บ), `deep-inspection` (เปิด SSL/TLS ตรวจเนื้อหาแล้วเข้ารหัสใหม่), `no-inspection` (ไม่ตรวจ), `custom-deep-inspection` (แก้ไขหรือ clone ได้)
- ระวัง: `ssl-ssh-profile` ต้องระบุ (เช่น `deep-inspection` หรือ `certificate-inspection`) ถึง IPS/AV จะเห็นข้างใน HTTPS, `inspection-mode` (flow หรือ proxy) ต้องตรงกับ feature-set ของ AV profile
- ตรวจด้วย diagnose flow: `diagnose firewall iprope lookup <src-ip> <src-port> <dst-ip> <dst-port> <protocol> <src-intf>`
- อ้าง playbook: `fortigate-74-ssl-inspection` สำหรับหัวข้อ deep-inspection

---

## 9. ไล่ False Positive

คำค้น: fortigate false positive, fortigate false positive IPS, fortigate false positive antivirus, fortigate false positive application control, fortigate false positive DNS filter, fortigate false positive security profile, false positive FortiGate, false positive FortiGate IPS
อาการ: security profiles บล็อก traffic ที่ถูกต้อง (false positive)
คำสั่งตรวจ:
```
show log event log
```
อ่านผล:
- ดู Security Events logs ใน GUI (Log & Report > Security Events)
- รายการที่มี action = "Block" แต่เป็น traffic ที่ถูกต้อง = false positive
- แต่ละรายการมีชื่อ signature, application, domain ที่ถูกบล็อก
- หากไม่มี log = security profiles ไม่ถูกผูกกับ policy ที่ traffic ผ่าน
ที่มา: [IPS security profile — FortiOS 7.4.4 ATP Deployment Guide](https://docs.fortinet.com/document/fortigate/7.4.4/ngfw-atp-deployment-guide/900128/ips-security-profile)
วิธีแก้:
- (ก) ตัด signature/application/Domain ออกจาก profile ที่เกิด false positive
  - IPS: `config ips sensor`, `edit "<profile>"`, `config entries`, `edit <filter-id>`, `set status disable`, `next`, `end`, `next`, `end`
  - AV: ตรวจสอบ log AV ใน GUI และเพิ่มไฟล์ที่เป็น false positive เข้า quarantine เพื่อตรวจสอบ
  - Application Control: เพิ่ม application เข้า allow list: `config application list`, `edit "<app-list>"`, `config entries`, `edit <rule-id>`, `set action pass`, `set status enable`, `next`, `end`, `next`, `end`
  - DNS Filter: เพิ่ม domain เข้า allow list ใน ftgd-dns: `config dnsfilter profile`, `edit "<dnsfilter>"`, `config ftgd-dns`, `config filters`, `edit <id>`, `set action monitor`, `next`, `end`, `end`, `next`, `end`
- (ข) ใช้ exempt-ip สำหรับ IPS (ปลอดภัยกว่าปิด signature ทั้งตัว):
  - `config ips sensor`, `edit "<profile>"`, `config entries`, `edit <filter-id>`, `config exempt-ip`, `edit 1`, `set src-ip <IP>/32`, `set dst-ip <IP>/32`, `next`, `end`, `next`, `end`, `next`, `end`
- (ค) เปลี่ยน action จาก block เป็น monitor ชั่วคราว: `set action pass` ใน IPS entry
- (ง) ใช้ exemption แทนการปิดการป้องกัน — เช่น ใช้ `set action pass` เฉพาะ signature/rule ที่เกิด false positive แทนการปิด profile ทั้งหมด
- ระวัง: อย่าปิดการป้องกันทั้งหมด (เช่น set status disable บนทั้ง profile) — ให้ตัดเฉพาะ signature/rule/IP ที่เกิด false positive
- ตรวจด้วย diagnose flow: `diagnose firewall iprope lookup <src-ip> <src-port> <dst-ip> <dst-port> <protocol> <src-intf>` เพื่อดูว่า traffic ผ่าน policy ไหน และมี security profiles อะไรผูกอยู่
