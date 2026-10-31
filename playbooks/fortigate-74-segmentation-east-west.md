---
id: fortigate-74-segmentation-east-west
title: FortiGate 7.4 Segmentation: Server Zone (East-West)
families: fortinet_fortios
triggers: fortigate server zone, fortigate segmentation, fortigate east-west, fortigate intrazone, fortigate web app db, fortigate zone-based policy, fortigate east-west traffic, fortigate server separation, fortigate intra-zone, fortigate asymmetric routing, fortigate iprope lookup, fortigate diagnose flow
versions: FortiOS 7.4.x
sources: https://docs.fortinet.com/document/fortigate/7.4.2/administration-guide/656084/firewall-policy, https://docs.fortinet.com/document/fortigate/7.4.7/cli-reference/84620/config-system-zone, https://docs.fortinet.com/document/fortigate/7.4.2/administration-guide/139692/routing-concepts, https://docs.fortinet.com/document/fortigate/7.4.0/best-practices/862226/policies, https://docs.fortinet.com/document/fortigate/7.4.0/administration-guide/116821/zone, https://docs.fortinet.com/document/fortigate/7.4.2/administration-guide/498347/profile-groups
---

# FortiGate 7.4 Segmentation: Server Zone (East-West)

คำค้น: fortigate server zone, fortigate segmentation, fortigate east-west, fortigate intrazone, fortigate zone-based policy, fortigate intra-zone
อาการ: ต้องออกแบบและติดตั้ง zone-based segmentation สำหรับ server (เช่น web → app → db) บน FortiGate 7.4.x, ตั้งค่า intra-zone traffic, ผูก security profile กับ east-west, ตรวจ policy ด้วย diagnose flow, และระวัง asymmetric routing

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
- สร้าง zone สำหรับ tier แต่ละระดับด้วย `config system zone`, `edit "WEB-ZONE"`, `set interface "<web-vlan-if1>" "<web-vlan-if2>"`, `set intrazone deny`, `next`, `end` (ค่า default ของ intrazone คือ deny หากไม่ตั้งค่า)
- สร้าง zone APP: `config system zone`, `edit "APP-ZONE"`, `set interface "<app-vlan-if1>" "<app-vlan-if2>"`, `set intrazone deny`, `next`, `end`
- สร้าง zone DB: `config system zone`, `edit "DB-ZONE"`, `set interface "<db-vlan-if1>"`, `set intrazone deny`, `next`, `end`
- หมายเหตุ: interface ที่จะใส่ใน zone ต้องยังไม่ถูกอ้างใน policy / config อื่น และอยู่ได้แค่ zone เดียว
- ระวัง: segmentation ใช้ได้เฉพาะ server ที่อยู่**ต่าง subnet / VLAN** และใช้ FortiGate เป็น gateway server ใน subnet เดียวกันคุยกันตรงผ่าน switch โดยไม่ผ่าน FortiGate
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
- FortiGate match ตาม**ลำดับในรายการ** (บนลงล่าง) ไม่ใช่ตามเลข policy-id
ที่มา: [Firewall policy — FortiOS 7.4.2 Admin Guide](https://docs.fortinet.com/document/fortigate/7.4.2/administration-guide/656084/firewall-policy)
วิธีแก้:
- สร้าง policy Web → App (เปิดเฉพาะ port ที่ app ใช้จริง): `config firewall policy`, `edit 0`, `set name "POLICY-WEB-TO-APP"`, `set srcintf "WEB-ZONE"`, `set dstintf "APP-ZONE"`, `set srcaddr "<web-servers>"`, `set dstaddr "<app-servers>"`, `set service "<app-service>"`, `set action accept`, `set schedule always`, `set logtraffic all`, `next`, `end`
- สร้าง policy App → DB (เฉพาะ port ของฐานข้อมูลที่ใช้จริง): `config firewall policy`, `edit 0`, `set name "POLICY-APP-TO-DB"`, `set srcintf "APP-ZONE"`, `set dstintf "DB-ZONE"`, `set srcaddr "<app-servers>"`, `set dstaddr "<db-servers>"`, `set service "<db-service>"`, `set action accept`, `set schedule always`, `set logtraffic all`, `next`, `end`
- ไม่ต้องสร้าง policy ขากลับ: FortiGate เป็น stateful reply ของ session ที่อนุญาตแล้วผ่านอัตโนมัติ
- ท้ายรายการมี implicit deny อยู่แล้ว ถ้าต้องการ log สิ่งที่ถูก implicit deny ให้เปิด `config log setting`, `set fwpolicy-implicit-log enable`, `end`
- ชื่อ service ให้ตรวจจากเครื่องก่อนใช้ (`show firewall service custom`) หรือสร้าง custom service ตาม port จริง
- สร้าง policy Deny ทั้งหมดท้ายสุด: `config firewall policy`, `edit 0`, `set name "DENY-ALL-SERVER"`, `set srcintf "SERV-ZONE"`, `set dstintf "SERV-ZONE"`, `set srcaddr "all"`, `set dstaddr "all"`, `set service "ALL"`, `set action deny`, `set schedule always`, `set logtraffic all`, `next`, `end`
- ตั้งค่า UTM: `utm-status` ต้องเป็น `enable` ถ้าต้องการใช้ security profiles
- ห้ามใช้ `any` ใน srcintf/dstintf และ `all` ใน srcaddr/dstaddr ของ policy east-west: ใช้ zone และ address object เฉพาะเจาะจง

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
อาการ: ต้องผูก security profiles (IPS, AV, Application Control, DNS Filter) กับ policy east-west ของ server zone
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
- หรือผูกทีละ profile: `set av-profile "AV-Server"`, `set ips-sensor "IPS-Server"`, `set application-list "App-List-Server"`, `set dnsfilter-profile "DNS-Filter-Server"`, `set ssl-ssh-profile <profile>`
- ระวัง: `utm-status` ต้องเป็น `enable` ถึงจะใช้ security profiles ได้
- ระวัง: traffic ที่ไป server ของเราเอง ห้ามใช้ `deep-inspection` สำเร็จรูป (client จะเห็น cert ของ FortiGate) ให้ใช้ profile ที่ `server-cert-mode replace` + cert ของ server หรือ `certificate-inspection` (ดู fortigate-74-security-profiles)

---

## 5. ตรวจว่า Traffic ผ่าน Policy ไหน (Policy Lookup)

คำค้น: fortigate policy lookup, fortigate iprope lookup, fortigate diagnose flow, fortigate traffic policy check
อาการ: ต้องตรวจว่า traffic จาก <src> ไป <dst> ตรงกับ policy ไหน
คำสั่งตรวจ:
```
diagnose firewall iprope lookup <src_ip> <src_port> <dst_ip> <dst_port> <protocol> <src_intf> policy
```
อ่านผล:
- `diagnose firewall iprope lookup` จะแสดง policy index (policy ID) ที่ match, uuid, action, zone info, source/destination address/service ที่ match
- ถ้า lookup ไม่ match ที่คาดไว้ ให้ใช้ debug flow (ในวิธีแก้) ดูทีละ packet ว่าเจอ route / policy ไหน
ที่มา: [Policy lookup — FortiOS 7.4.x Admin Guide](https://docs.fortinet.com/document/fortigate/7.4.2/administration-guide/656084/firewall-policy), [diagnose firewall iprope lookup — FortiOS 7.6.4 CLI Reference](https://docs.fortinet.com/document/fortigate/7.6.4/cli-reference/253375604/diagnose-firewall)
วิธีแก้:
- ตรวจ policy match: `diagnose firewall iprope lookup <src-ip> <src-port> <dst-ip> <dst-port> <protocol> <src-intf> policy` (เปลี่ยน <src_intf> เป็น interface name ที่ traffic เข้า)
- ผลลัพธ์จะแสดง policy index (เช่น `policy index=2 uuid_idx=1300 action=accept`) — ต้องตรงกับ policy ที่ตั้งใจ
- debug flow (ส่ง traffic จริงแล้วดู): `diagnose debug flow filter clear`, `diagnose debug flow filter addr <dst_ip>`, `diagnose debug flow show function-name enable`, `diagnose debug enable`, `diagnose debug flow trace start 20`
- ในผล debug ดูบรรทัด `find a route` (ออก interface ไหน) และ `Allowed by Policy-<id>` หรือ `Denied by forward policy check`
- ระวัง: ปิดทุกครั้งหลังใช้: `diagnose debug flow trace stop`, `diagnose debug disable` (debug ค้างไว้กิน CPU)
- ตรวจสอบว่า security profiles ถูกผูก: ใน debug flow ต้องเห็น IPS/AV profile names ที่ถูกใช้

---

## 6. ระวัง Asymmetric Routing และ Server Gateway อยู่นอก FortiGate

คำค้น: fortigate asymmetric routing, fortigate server bypass, fortigate server gateway external, fortigate asymroute
อาการ: server มี gateway อยู่นอก FortiGate ทำให้ response traffic bypass FortiGate
คำสั่งตรวจ:
```
get router info routing-table all
get system settings | grep asymroute
```
อ่านผล:
- ต้องเห็น routing table — ตรวจสอบว่า default gateway ของ server ชี้ไป FortiGate หรือ interface อื่น
- `asymroute` default คือ `disable` — หาก enable = FortiGate จะยอม asymmetric routing (ไม่แนะนำ)
ที่มา: [Routing concepts — FortiOS 7.4.2 Admin Guide](https://docs.fortinet.com/document/fortigate/7.4.2/administration-guide/139692/routing-concepts)
วิธีแก้:
- ตรวจสอบ routing table: `get router info routing-table all` — ต้องเห็นว่า route ไปยัง server subnet ผ่าน interface ที่ FortiGate control
- หาก server gateway ชี้ไป interface อื่น (bypass FortiGate) — response traffic จะไม่ผ่าน FortiGate
- อาการ: FortiGate เห็น packet แค่ทางเดียว ขาที่ไม่มี session (เช่น SYN/ACK ที่ไม่เคยเห็น SYN) จะถูก drop การเชื่อมต่อจะค้าง / timeout
- แก้: ตั้ง server gateway ให้ชี้มาที่ FortiGate interface (preferred solution)
- หากแก้ routing ไม่ได้: สามารถเปิด `set asymroute enable` ใน `config system settings` ได้ แต่**ไม่แนะนำ**: เป็นการปิด stateful inspection ของทั้ง VDOM ไม่ใช่เฉพาะ server นั้น ใช้แค่ชั่วคราวตอนแก้ปัญหา
- กรณี server มีหลาย NIC / gateway อยู่ที่อุปกรณ์อื่น: ใส่ static route บน server ให้ subnet ของ server zone อื่นวิ่งกลับทาง FortiGate เพื่อให้ขาไปและขากลับผ่าน FortiGate ทั้งคู่

---
