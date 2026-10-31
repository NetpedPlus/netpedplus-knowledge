---
id: fortigate-74-security-profiles
title: FortiGate 7.4 Security Profiles: IPS, AntiVirus, Application Control, DNS Filter
families:
triggers: fortigate security profile, fortigate IPS, fortigate antivirus, fortigate application control, fortigate DNS filter, fortigate profile group, fortigate security profiles, fortigate security profile สำหรับ server, fortigate false positive, ผูก security profile, สร้าง security profile, profile group, security profile ไม่จับ, false positive FortiGate
versions: FortiOS 7.4.x
sources: https://docs.fortinet.com/document/fortigate/7.4.2/administration-guide/680955/security-profiles, https://docs.fortinet.com/document/fortigate/7.4.4/ngfw-atp-deployment-guide/900128/ips-security-profile, https://docs.fortinet.com/document/fortigate/7.4.4/ngfw-atp-deployment-guide/520351/av-security-profile, https://docs.fortinet.com/document/fortigate/7.4.4/cli-reference/333889629/config-firewall-policy, https://docs.fortinet.com/document/fortigate/7.4.1/cli-reference/292620/config-firewall-policy, https://docs.fortinet.com/document/fortigate/7.4.4/cli-reference/131776/config-firewall-ips, https://docs.fortinet.com/document/fortigate/7.4.4/cli-reference/60218/config-firewall-av, https://docs.fortinet.com/document/fortigate/7.4.4/cli-reference/201229/config-firewall-application-list, https://docs.fortinet.com/document/fortigate/7.4.4/cli-reference/109993161/config-firewall-profile-group, https://docs.fortinet.com/document/fortigate/7.4.4/cli-reference/299890/config-dnsfilter-profile
---

# FortiGate 7.4 Security Profiles: IPS, AntiVirus, Application Control, DNS Filter

คำค้น: fortigate security profile, fortigate IPS, fortigate antivirus, fortigate application control, fortigate DNS filter, fortigate profile group, fortigate security profiles, fortigate security profile สำหรับ server, fortigate false positive, ผูก security profile, สร้าง security profile, profile group, security profile ไม่จับ, false positive FortiGate, fortigate security profiles สำหรับ server
อาการ: ต้องสร้างหรือแก้ไข security profiles (IPS, AntiVirus, Application Control, DNS Filter) บน FortiGate 7.4.x และผูกกับ firewall policy รวมถึงไล่ false positive

---

## 1. ตรวจ Security Profile ที่มีอยู่

คำค้น: fortigate security profile, fortigate IPS profile, fortigate AV profile, fortigate application list, fortigate DNS filter profile, ตรวจ profile ที่มี, fortigate show profile
อาการ: ต้องตรวจว่า security profiles มีอยู่แล้วหรือไม่
คำสั่งตรวจ:
```
get firewall profile ips-sensor
get firewall profile antivirus
get firewall policy
```
อ่านผล:
- `get firewall profile ips-sensor`: แสดงรายการ IPS sensor profiles ทั้งหมด พร้อมสถานะ (enable/disable)
- `get firewall profile antivirus`: แสดงรายการ AV profiles ทั้งหมด
- `get firewall policy`: แสดง policies ทั้งหมด พร้อม security profiles ที่ผูกอยู่ (av-profile, ips-sensor, application-list, dnsfilter-profile, profile-group)
ที่มา: [config firewall policy — FortiOS 7.4.1](https://docs.fortinet.com/document/fortigate/7.4.1/cli-reference/292620/config-firewall-policy)
วิธีแก้:
- หากไม่มี profiles ที่ต้องการ ให้สร้างจากขั้นตอนถัดไป
- ตรวจสอบว่า policies มี security profiles ถูกผูกอยู่แล้วหรือไม่

---

## 2. สร้าง IPS Sensor Profile

คำค้น: fortigate IPS sensor, fortigate intrusion prevention, fortigate IPS profile, fortigate IPS sensor profile, fortigate IPS sensor, fortigate security profile IPS, fortigate IPS สำหรับ server
อาการ: ต้องสร้าง IPS sensor profile ใหม่หรือเลือก profile ที่มี
คำสั่งตรวจ:
```
show firewall ips-sensor "<ชื่อ_sensor>"
```
อ่านผล:
- ต้องเห็น IPS sensor name, list of signatures ที่เลือก, action (block/monitor/allow)
- หากไม่พบ = ยังไม่ได้สร้าง IPS sensor
ที่มา: [IPS security profile — FortiOS 7.4.4 ATP Deployment Guide](https://docs.fortinet.com/document/fortigate/7.4.4/ngfw-atp-deployment-guide/900128/ips-security-profile)
วิธีแก้:
- สร้าง IPS sensor: `config firewall ips-sensor`, `edit "IPS-Server"`, `set status enable`, `edit 1`, `set proto 6`, `set attack-name <signature-name>`, `next`, `next`
- ใช้ pre-defined profile: `config firewall ips-sensor`, `edit "Fortinet-Recommended"`, `set status enable`, `next`, `end`
- FortiGate มาพร้อม pre-defined IPS profiles: Fortinet-Recommended, Fortinet-Critical, Fortinet-Monitor, Custom
- ระวัง: ใช้ Fortinet-Recommended เป็นจุดเริ่มต้น แล้วค่อยๆ ปิด signatures ที่เกิด false positive
- ตัด signature ออก: `config firewall ips-sensor`, `edit "IPS-Server"`, `edit <signature-id>`, `set status disable`, `next`, `next`, `end`
- ตรวจ signature database version: `diag ips db-check`

---

## 3. สร้าง Antivirus Profile

คำค้น: fortigate antivirus profile, fortigate AV profile, fortigate anti-virus, fortigate antivirus profile สำหรับ server, fortigate AV สำหรับ server
อาการ: ต้องสร้าง AV profile ใหม่หรือเลือก profile ที่มี
คำสั่งตรวจ:
```
show firewall av-profile "<ชื่อ_av>"
```
อ่านผล:
- ต้องเห็น AV profile name, scan-mode (default/legacy), feature-set (proxy/flow), quarantine action
- หากไม่พบ = ยังไม่ได้สร้าง AV profile
ที่มา: [AV security profile — FortiOS 7.4.4 ATP Deployment Guide](https://docs.fortinet.com/document/fortigate/7.4.4/ngfw-atp-deployment-guide/520351/av-security-profile)
วิธีแก้:
- สร้าง AV profile: `config firewall av-profile`, `edit "AV-Server"`, `set feature-set proxy`, `set scan-mode default`, `next`, `end`
- ใช้ pre-defined profile: `config firewall av-profile`, `edit "Fortinet-Recommended"`, `set feature-set proxy`, `set scan-mode default`, `next`, `end`
- FortiGate มาพร้อม pre-defined AV profiles: Fortinet-Recommended, Fortinet-Critical, Fortinet-Monitor, Custom
- ระวัง: feature-set ต้องตรงกับ inspection mode ของ firewall policy (proxy หรือ flow)
- ตรวจสอบ log AV: `execute log filter category 2`, `execute log display`

---

## 4. สร้าง Application List (Application Control)

คำค้น: fortigate application list, fortigate app-list, fortigate application control, fortigate application control profile, fortigate application control สำหรับ server, fortigate app control
อาการ: ต้องสร้าง Application List สำหรับควบคุมแอปพลิเคชันที่อนุญาต/บล็อกใน policy
คำสั่งตรวจ:
```
show firewall application-list "<ชื่อ_app_list>"
```
อ่านผล:
- ต้องเห็น application list name, list of application rules (allow/deny/block/monitor)
- หากไม่พบ = ยังไม่ได้สร้าง application list
ที่มา: [FortiOS CLI Reference — search command (Application)](https://docs.fortinet.com/document/fortigate/7.4.1/cli-reference/292620/config-firewall-policy)
วิธีแก้:
- สร้าง application list: `config firewall application-list`, `edit "App-List-Server"`, `edit 1`, `set action allow`, `set application <app-id1> <app-id2>`, `next`, `next`, `end`
- ใช้ pre-defined application list: `config firewall application-list`, `edit "Fortinet-Recommended"`, `set status enable`, `next`, `end`
- ดู application list ที่มีอยู่แล้ว: `get firewall application-list`
- ดู application ID: `get firewall application <keyword>` (เช่น `get firewall application web-browser`)
- ระวัง: ถ้าไม่ตั้งค่า application list ใน policy จะไม่มีการควบคุมแอปพลิเคชัน

---

## 5. สร้าง DNS Filter Profile

คำค้น: fortigate DNS filter, fortigate dns filter profile, fortigate dnsfilter, fortigate DNS filter สำหรับ server, fortigate DNS filter สำหรับ server
อาการ: ต้องสร้าง DNS filter profile สำหรับควบคุม DNS queries
คำสั่งตรวจ:
```
show dnsfilter profile "<ชื่อ_dnsfilter>"
```
อ่านผล:
- ต้องเห็น DNS filter profile name, domain filters, action (allow/block/monitor/nxdomain)
- หากไม่พบ = ยังไม่ได้สร้าง DNS filter profile
ที่มา: [FortiOS CLI Reference — search command (dnsfilter)](https://docs.fortinet.com/document/fortigate/7.4.1/cli-reference/292620/config-firewall-policy)
วิธีแก้:
- สร้าง DNS filter profile: `config dnsfilter profile`, `edit "DNS-Filter-Server"`, `edit 1`, `set domain <domain-name>`, `set action <allow|block|monitor>`, `next`, `next`, `end`
- ใช้ pre-defined profile: `config dnsfilter profile`, `edit "Fortinet-Recommended"`, `set status enable`, `next`, `end`
- ตรวจสอบ DNS query log: `execute log filter category 4`, `execute log display`
- ระวัง: DNS filter profile ใช้สำหรับป้องกัน domain ที่ไม่ปลอดภัยและจำกัด domain ที่ไม่จำเป็น

---

## 6. สร้าง Profile Group (รวมหลาย security profiles)

คำค้น: fortigate profile group, fortigate security profile group, fortigate profile group สำหรับ server, fortigate security profile group, fortigate profile group สำหรับ server
อาการ: ต้องสร้าง profile group เพื่อผูก security profiles หลายตัวพร้อมกันใน policy เดียว
คำสั่งตรวจ:
```
show firewall profile-group "<ชื่อ_profile_group>"
```
อ่านผล:
- ต้องเห็น profile group name, list of profiles ที่ผูก (av-profile, ips-sensor, application-list, dnsfilter-profile, webfilter-profile, ฯลฯ)
- หากไม่พบ = ยังไม่ได้สร้าง profile group
ที่มา: [Profile groups — FortiOS Administration Guide](https://docs.fortinet.com/document/fortigate/7.0.15/administration-guide/814292/profile-groups)
วิธีแก้:
- สร้าง profile group: `config firewall profile-group`, `edit "PG-Server"`, `set av-profile "AV-Server"`, `set ips-sensor "IPS-Server"`, `set application-list "App-List-Server"`, `set dnsfilter-profile "DNS-Filter-Server"`, `next`, `end`
- Profile group ช่วยลดความซับซ้อนในการผูก profiles หลายตัวใน policy เดียว
- ตรวจสอบ profile group: `get firewall profile-group`
- ระวัง: profile-type ใน policy ต้องเป็น `group` ถ้าจะใช่ profile group

---

## 7. ผูก Security Profiles กับ Firewall Policy

คำค้น: fortigate security policy, fortigate firewall policy, fortigate policy สำหรับ server, fortigate ผูก profile, fortigate policy security profiles, fortigate security profile กับ policy, fortigate ผูก security profile กับ policy, fortigate security profile สำหรับ server
อาการ: ต้องผูก security profiles กับ firewall policy ใหม่หรือ policy ที่มี
คำสั่งตรวจ:
```
show firewall security-policy
```
อ่านผล:
- ต้องเห็น policy name, srcintf, dstintf, srcaddr, dstaddr, service, action, security profiles ที่ผูกอยู่
- หากไม่มี security profiles ผูก = traffic จะไม่ถูกตรวจสอบ
ที่มา: [config firewall security-policy — FortiOS 7.4.1](https://docs.fortinet.com/document/fortigate/7.4.1/cli-reference/292620/config-firewall-policy)
วิธีแก้:
- สร้าง policy ใหม่พร้อม security profiles:
  ```
  config firewall security-policy
      edit <policy-id>
          set name "POLICY-SERVER-<ชื่อ>"
          set srcintf "<src-interface>"
          set dstintf "<dst-interface>"
          set srcaddr "<src-address>"
          set dstaddr "<server-address>"
          set service "HTTPS" "HTTP" "SSH"
          set action accept
          set schedule "always"
          set utm-status enable
          set profile-type single
          set av-profile "AV-Server"
          set ips-sensor "IPS-Server"
          set application-list "App-List-Server"
          set dnsfilter-profile "DNS-Filter-Server"
          set logtraffic all
          next
  end
  ```
- หรือใช้ profile group แทน single profiles: `set profile-type group`, `set profile-group "PG-Server"`
- ตรวจลำดับ policy: ใช้ `show firewall security-policy` ดูลำดับ, ใช้ `diagnose firewall policy reorder <policy-id> after <policy-id>` จัดลำดับ
- ระวัง: ถ้า profile-type = `single` ต้องระบุแต่ละ profile ทีละตัว. ถ้า profile-type = `group` ให้ระบุเฉพาะ profile-group
- ตรวจด้วย diagnose flow: `diagnose firewall iprope lookup <src-ip> <src-port> <dst-ip> <dst-port> <protocol> <src-intf>`

---

## 8. ไล่ False Positive

คำค้น: fortigate false positive, fortigate false positive IPS, fortigate false positive antivirus, fortigate false positive application control, fortigate false positive DNS filter, fortigate false positive security profile, false positive FortiGate, false positive FortiGate IPS
อาการ: security profiles บล็อก traffic ที่ถูกต้อง (false positive)
คำสั่งตรวจ:
```
execute log filter device 0
execute log filter category 4
execute log display
```
อ่านผล:
- ดู security event logs ใน Log & Report > Security Events
- รายการที่มี action = "Block" แต่เป็น traffic ที่ถูกต้อง = false positive
- แต่ละรายการมีชื่อ signature, application, domain ที่ถูกบล็อก
- หากไม่มี log = security profiles ไม่ถูกผูกกับ policy ที่ traffic ผ่าน
ที่มา: [IPS security profile — FortiOS 7.4.4 ATP Deployment Guide](https://docs.fortinet.com/document/fortigate/7.4.4/ngfw-atp-deployment-guide/900128/ips-security-profile)
วิธีแก้:
- (ก) ตัด signature/application/Domain ออกจาก profile ที่เกิด false positive
  - IPS: `config firewall ips-sensor`, `edit "<profile>"`, `edit <signature-id>`, `set status disable`, `next`, `next`, `end`
  - AV: เพิ่ม file type หรือ URL เข้า AV exemption list: `config antivirus exempt-list`, `edit <id>`, `set file <file-pattern>`, `next`, `end`
  - Application Control: เพิ่ม application เข้า allow list ใน application list: `config firewall application-list`, `edit "<app-list>"`, `edit <rule-id>`, `set action allow`, `set application <app-id>`, `next`, `next`, `end`
  - DNS Filter: เพิ่ม domain เข้า allow list: `config dnsfilter profile`, `edit "<dnsfilter>"`, `edit <id>`, `set domain <domain>`, `set action allow`, `next`, `next`, `end`
- (ข) เปลี่ยน action จาก block เป็น monitor ชั่วคราว: `set action monitor` แล้วดูว่าเกิด false positive บ่อยหรือไม่
- (ค) ใช้ exemption แทนการปิดการป้องกัน:
  - AV: ตั้ง scan-mode เป็น legacy สำหรับไฟล์บางประเภท
  - IPS: ใช้ filter เพื่อตัด signatures ที่ไม่จำเป็นออกจาก profile
  - DNS Filter: ใช้ domain filter แบบ allow list แทน block list
- ระวัง: อย่าปิดการป้องกันทั้งหมด (เช่น set status disable บนทั้ง profile) — ให้ตัดเฉพาะ signature/rule ที่เกิด false positive
- ตรวจด้วย diagnose flow: `diagnose firewall iprope lookup <src-ip> <src-port> <dst-ip> <dst-port> <protocol> <src-intf>` เพื่อดูว่า traffic ผ่าน policy ไหน และมี security profiles อะไรผูกอยู่
