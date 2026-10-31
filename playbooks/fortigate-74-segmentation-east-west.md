---
id: fortigate-74-segmentation-east-west
title: FortiGate 7.4 Segmentation: Server Zone (East-West)
families:
triggers: fortigate server zone, fortigate segmentation, fortigate east-west, fortigate intrazone, fortigate web app db, fortigate zone-based policy, fortigate east-west traffic, fortigate server separation, fortigate intra-zone, fortigate asymmetric routing, fortigate iprope lookup, fortigate diagnose flow
versions: FortiOS 7.4.x
sources: https://docs.fortinet.com/document/fortigate/7.4.2/administration-guide/656084/firewall-policy, https://docs.fortinet.com/document/fortigate/7.4.2/administration-guide/538358/using-ssl-vpn-interfaces-in-zones, https://docs.fortinet.com/document/fortigate/7.4.7/cli-reference/84620/config-system-zone, https://docs.fortinet.com/document/fortigate/7.4.2/administration-guide/139692/routing-concepts, https://docs.fortinet.com/document/fortigate/7.4.0/best-practices/862226/policies, https://docs.fortinet.com/document/fortigate/7.4.1/fortios-release-notes/743723/new-features-or-enhancements, https://docs.fortinet.com/document/fortigate/7.4.0/administration-guide/116821/zone, https://docs.fortinet.com/document/fortigate/7.4.2/administration-guide/498347/profile-groups
---

# FortiGate 7.4 Segmentation: Server Zone (East-West)

คำค้น: fortigate server zone, fortigate segmentation, fortigate east-west, fortigate intrazone, fortigate zone-based policy, fortigate intra-zone
อาการ: ต้องออกแบบและติดตั้ง zone-based segmentation สำหรับ server (เช่น web → app → db) บน FortiGate 7.4.x, ตั้งค่า intra-zone traffic, ผูก security profileeast-west, ตรวจ policy ด้วย diagnose flow, และระวัง asymmetric routing

---

## 1. สร้าง Zone สำหรับแยกโซน Server

คำค้น: fortigate system zone, fortigate zone server, fortigate config system zone, fortigate zone VLAN
อาการ: ต้องแยก server ออกเป็น zone ตาม tier (web / app / db) เพื่อควบคุม east-west traffic
คำสั่งตรวจ:
```
show system zone
```
อ่านผล:
- ต้องเห็น zone name, list of interfaces ใน zone, intrazone setting
- หากไม่พบ = ยังไม่ได้สร้าง zone
ที่มา: [config system zone — FortiOS 7.4.7 CLI Reference](https://docs.fortinet.com/document/fortigate/7.4.7/cli-reference/84620/config-system-zone)
วิธีแก้:
- สร้าง zone สำหรับ tier แต่ละระดับด้วย `config system zone`, `edit "WEB-ZONE"`, `set interface <web-vlan-if1>, <web-vlan-if2>`, `set intrazone deny`, `next`, `end` (ค่า default ของ intrazone คือ deny หากไม่ตั้งค่า)
- สร้าง zone APP: `config system zone`, `edit "APP-ZONE"`, `set interface <app-vlan-if1>, <app-vlan-if2>`, `set intrazone deny`, `next`, `end`
- สร้าง zone DB: `config system zone`, `edit "DB-ZONE"`, `set interface <db-vlan-if1>`, `set intrazone deny`, `next`, `end`
- หมายเหตุ: interfaces ใน zone ต้องไม่ถูกผูกกับ policy อื่นก่อน และต้องไม่ belong to another zone
- ดู zone ทั้งหมด: `show system zone`

---

## 2. สร้าง Firewall Policy East-West (เฉพาะ port ที่ใช้)

คำค้น: fortigate east-west policy, fortigate web app db, fortigate inter-zone policy, fortigate policy log
อาการ: ต้องสร้าง policy อนุญาต traffic ระหว่าง zone server แบบเจาะจง port และ log ทุก policy
คำสั่งตรวจ:
```
show firewall policy
```
อ่านผล:
- ต้องเห็น policy name, srcintf (จาก zone), dstintf (target zone), srcaddr, dstaddr, service, action, utm-status, logtraffic
- ต้องเห็นลำดับ policy (policy-id) — FortiGate match ตามลำดับจากน้อยไปมาก
ที่มา: [Firewall policy — FortiOS 7.4.2 Admin Guide](https://docs.fortinet.com/document/fortigate/7.4.2/administration-guide/656084/firewall-policy)
วิธีแก้:
- สร้าง policy Web → App (เช่น HTTP/HTTPS port 80, 443): `config firewall policy`, `edit 0`, `set name "POLICY-WEB-TO-APP"`, `set srcintf "WEB-ZONE"`, `set dstintf "APP-ZONE"`, `set srcaddr "all"`, `set dstaddr "all"`, `set service HTTPS HTTP`, `set action accept`, `set schedule always`, `set logtraffic all`, `set logsession disable`, `next`, `end`
- สร้าง policy App → DB (เช่น port 1433, 3306, 5432): `config firewall policy`, `edit 0`, `set name "POLICY-APP-TO-DB"`, `set srcintf "APP-ZONE"`, `set dstintf "DB-ZONE"`, `set srcaddr "all"`, `set dstaddr "all"`, `set service MSSQL MYSQL POSTGRESQL`, `set action accept`, `set schedule always`, `set logtraffic all`, `set logsession disable`, `next`, `end`
- สร้าง policy กลับทาง (reply): FortiGate ไม่ทำ reverse-path check — session established จะถูก auto-allow ใน policy เดียวกัน (ไม่ต้องสร้าง policy กลับทางแยก)
- สร้าง policy Deny ทั้งหมดท้ายสุด: `config firewall policy`, `edit 0`, `set name "DENY-ALL-SERVER"`, `set srcintf "all"`, `set dstintf "all"`, `set srcaddr "all"`, `set dstaddr "all"`, `set service "ALL"`, `set action deny`, `set schedule always`, `set logtraffic all`, `next`, `end`
- ตั้งค่า UTM: `utm-status` ต้องเป็น `enable` ถ้าต้องการใช้ security profiles
- ห้ามใช้ `any` ใน srcintf/dstintf/srvaddr (best practice): ใช้ zone และ address object เฉพาะเจาะจง

---

## 3. Intra-Zone Traffic (ภายใน zone เดียว)

คำค้น: fortigate intrazone, fortigate intra-zone, fortigate intra-zone traffic, fortigate intrazone allow
อาการ: ต้องตรวจว่า server ใน zone เดียวกันคุยกันได้อย่างไร (intra-zone traffic)
คำสั่งตรวจ:
```
show system zone
```
อ่านผล:
- ต้องเห็น `intrazone` setting ใน zone — ค่า default คือ `deny`
- หาก `intrazone deny` = interfaces ใน zone เดียวกันจะ blocked traffic จากกัน (default behavior)
- หาก `intrazone allow` = interfaces ใน zone เดียวกันคุยกันได้ (ต้องระวัง)
ที่มา: [Zone — FortiOS 7.4.x Admin Guide](https://docs.fortinet.com/document/fortigate/7.4.0/administration-guide/116821/zone), [config system zone — FortiOS 7.4.7 CLI Reference](https://docs.fortinet.com/document/fortigate/7.4.7/cli-reference/84620/config-system-zone)
วิธีแก้:
- ค่า default ของ intrazone คือ `deny` — traffic ระหว่าง interfaces ใน zone เดียวกันจะถูก block
- หากต้องการให้ zone เดียวกันคุยกันได้: `config system zone`, `edit "WEB-ZONE"`, `set intrazone allow`, `next`, `end`
- หากต้องการอนุญาตเฉพาะบาง subnet ใน zone เดียวกัน: ตั้ง intrazone เป็น `deny` แล้วสร้าง policy ที่ srcintf = zone เดียวกัน และ dstintf = zone เดียวกัน (intra-zone policy) เช่น `set srcintf "WEB-ZONE"`, `set dstintf "WEB-ZONE"`, `set srcaddr "<subnet-src>"`, `set dstaddr "<subnet-dst>"`
- intra-zone blocking จะใช้ default deny และต้อง override ด้วย intra-zone policy เฉพาะที่ต้องการ

---

## 4. ผูก Security Profile กับ Policy East-West

คำค้น: fortigate security profile east-west, fortigate profile group server, fortigate IPS AV app control สำหรับ zone
อาการ: ต้องผูก security profiles (IPS, AV, Application Control, DNS Filter) กับ policyeast-west ของ server zone
คำสั่งตรวจ:
```
show firewall policy
show firewall profile-group
```
อ่านผล:
- ต้องเห็น security profiles ที่ผูกกับ policy (av-profile, ips-sensor, application-list, dnsfilter-profile, profile-group, ssl-ssh-profile, inspection-mode)
- หากไม่มี = traffic จะไม่ถูกตรวจสอบ
ที่มา: [config firewall policy — FortiOS 7.4.4 CLI Reference](https://docs.fortinet.com/document/fortigate/7.4.4/cli-reference/333889629/config-firewall-policy), [Profile groups — FortiOS 7.4.1 Admin Guide](https://docs.fortinet.com/document/fortigate/7.4.1/administration-guide/498347/profile-groups)
วิธีแก้:
- อ้าง playbook: `fortigate-74-security-profiles` สำหรับรายละเอียดการสร้าง IPS sensor, AV profile, Application list, DNS filter profile, และ Profile group
- สร้าง Profile Group สำหรับ server: `config firewall profile-group`, `edit "PG-SERVER"`, `set av-profile "AV-Server"`, `set ips-sensor "IPS-Server"`, `set application-list "App-List-Server"`, `set dnsfilter-profile "DNS-Filter-Server"`, `next`, `end`
- ผูกกับ policy East-West: `config firewall policy`, `edit <policy-id>`, `set utm-status enable`, `set profile-type group`, `set profile-group "PG-SERVER"`, `next`, `end`
- หรือผูกทีละ profile: `set av-profile "AV-Server"`, `set ips-sensor "IPS-Server"`, `set application-list "App-List-Server"`, `set dnsfilter-profile "DNS-Filter-Server"`, `set ssl-ssh-profile "deep-inspection"`
- ระวัง: `utm-status` ต้องเป็น `enable` ถึงจะใช้ security profiles ได้
- ระวัง: `ssl-ssh-profile` ต้องระบุ (เช่น `deep-inspection`) ถึง IPS/AV จะเห็นข้างใน HTTPS traffic

---

## 5. ตรวจว่า Traffic ผ่าน Policy ไหน (Policy Lookup)

คำค้น: fortigate policy lookup, fortigate iprope lookup, fortigate diagnose flow, fortigate traffic policy check
อาการ: ต้องตรวจว่า traffic จาก <src> ไป <dst> ตรงกับ policy ไหน
คำสั่งตรวจ:
```
diagnose firewall iprope lookup <src_ip> <src_port> <dst_ip> <dst_port> <protocol> <src_intf> policy
diagnose debug flow test enable
diagnose debug flow filter daddr <dst_ip>
diagnose debug flow filter dport <dst_port>
diagnose debug flow filter proto <protocol>
diagnose debug flow show flow_list 0
diagnose debug enable
```
อ่านผล:
- `diagnose firewall iprope lookup` จะแสดง policy index (policy ID) ที่ match, uuid, action, zone info, source/destination address/service ที่ match
- `diagnose debug flow` จะแสดง session ที่สร้าง, policy ID ที่ match, security profiles ที่ถูกใช้
ที่มา: [Policy lookup — FortiOS 7.4.x Admin Guide](https://docs.fortinet.com/document/fortigate/7.4.2/administration-guide/656084/firewall-policy), [diagnose firewall iprope lookup — FortiOS 7.6.4 CLI Reference](https://docs.fortinet.com/document/fortigate/7.6.4/cli-reference/253375604/diagnose-firewall)
วิธีแก้:
- ตรวจ policy match: `diagnose firewall iprope lookup <src-ip> <src-port> <dst-ip> <dst-port> <protocol> <src-intf> policy` (เปลี่ยน <src_intf> เป็น interface name ที่ traffic เข้า)
- ผลลัพธ์จะแสดง policy index (เช่น `policy index=2 uuid_idx=1300 action=accept`) — ต้องตรงกับ policy ที่ตั้งใจ
- ใช้ `diagnose debug flow test enable` แล้วส่ง traffic จริง: FortiGate จะแสดง debug output ว่า traffic ผ่าน policy ไหน, security profiles อะไรถูกใช้
- `diagnose debug flow filter daddr <dst_ip>` แล้ว `diagnose debug flow show flow_list 0` จะแสดง session ที่ match
- `diagnose debug enable` — เปิด debug (ระวัง: จะ verbose)
- ตรวจสอบว่า security profiles ถูกผูก: ใน debug flow ต้องเห็น IPS/AV profile names ที่ถูกใช้

---

## 6. ระวัง Asymmetric Routing และ Server Gateway อยู่นอก FortiGate

คำค้น: fortigate asymmetric routing, fortigate server bypass, fortigate server gateway external, fortigate asymroute
อาการ: server มี gateway อยู่นอก FortiGate ทำให้ response traffic bypass FortiGate
คำสั่งตรวจ:
```
get route all
get system settings | grep asymroute
```
อ่านผล:
- ต้องเห็น routing table — ตรวจสอบว่า default gateway ของ server ชี้ไป FortiGate หรือ interface อื่น
- `asymroute` default คือ `disable` — หาก enable = FortiGate จะยอม asymmetric routing (ไม่แนะนำ)
ที่มา: [Routing concepts — FortiOS 7.4.2 Admin Guide](https://docs.fortinet.com/document/fortigate/7.4.2/administration-guide/139692/routing-concepts)
วิธีแก้:
- ตรวจสอบ routing table: `get route all` — ต้องเห็นว่า route ไปยัง server subnet ผ่าน interface ที่ FortiGate control
- หาก server gateway ชี้ไป interface อื่น (bypass FortiGate) — response traffic จะไม่ผ่าน FortiGate
- ใน TCP: FortiGate จะบล็อก packet เพราะ TCP handshake ไม่ผ่าน FortiGate (SYN ผ่าน FortiGate แต่ SYN/ACK bypass)
- แก้: ตั้ง server gateway ให้ชี้มาที่ FortiGate interface (preferred solution)
- หากแก้ routing ไม่ได้: สามารถเปิด `set asymroute enable` ใน `config system settings` ได้ แต่ต้องระวัง: FortiGate จะไม่ inspect traffic ที่ bypass, อาจมี malicious traffic ผ่านได้
- ระวัง: asymmetric routing ไม่กระทบ UDP — UDP packets จะถูก check ด้วย session table แม้จะ asymmetric
- กรณี server ที่มี external gateway: ต้องทำ policy ทั้งสองทาง (symmetric) — หรือใช้ static route เพื่อบังคับให้ traffic ผ่าน FortiGate ทั้งขาไปและขากลับ

---
