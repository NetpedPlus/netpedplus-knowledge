---
id: fortigate-74-sdwan-bgp
title: FortiGate 7.4 SD-WAN + BGP troubleshooting: SD-WAN member, SD-WAN rule, BGP neighbor, BGP route, ลำดับการเลือกเส้นทาง
families: fortinet_fortios
triggers: fortigate sd-wan member status, sd-wan health-check sla, sd-wan member out of sla, sd-wan health-check fix, sd-wan rule not working, sd-wan traffic steering, fortigate bgp neighbor not up, bgp idle active opensent established, bgp route not learned, bgp next-hop unreachable, sd-wan vs static route priority, fortigate sd-wan policy route order
versions: FortiOS 7.4.x
sources: https://docs.fortinet.com/document/fortigate/7.4.0/administration-guide/867342/performance-sla-overview, https://docs.fortinet.com/document/fortigate/7.4.0/administration-guide/942095/sd-wan-members-and-zones, https://docs.fortinet.com/document/fortigate/7.4.0/cli-reference/76620/config-system-sdwan, https://docs.fortinet.com/document/fortigate/7.4.4/administration-guide/763341/basic-bgp-example, https://docs.fortinet.com/document/fortigate/7.4.0/cli-reference/528620/config-router-bgp, https://docs.fortinet.com/document/fortigate/7.4.2/administration-guide/139692/routing-concepts
---

# FortiGate 7.4 SD-WAN + BGP troubleshooting

## SD-WAN member / health-check (SLA) / สถานะและทำไม member ถูกตัด
ที่มา: [Performance SLA overview (FortiOS 7.4)](https://docs.fortinet.com/document/fortigate/7.4.0/administration-guide/867342/performance-sla-overview)
คำค้น: fortigate sd-wan member out of sla, sd-wan health-check status, sd-wan member dead, sd-wan sla
อาการ: member ถูกตัด / out of SLA, SD-WAN rule ใช้ member อื่นแทน, traffic ไม่ออก link ที่ตั้งใจ
คำสั่งตรวจ:
```
diagnose sys sdwan health-check
diagnose sys sdwan member
show system sdwan
```
อ่านผล:
- `diagnose sys sdwan health-check`: ต่อ health-check และต่อ member เห็น alive / dead, latency, jitter, packet loss และ SLA ที่ผ่าน / ไม่ผ่าน
- `diagnose sys sdwan member`: member, interface, gateway, priority, cost
- `show system sdwan`: ค่า health-check (server, protocol, interval, failtime, recoverytime, sla threshold) และ member / zone
สาเหตุที่พบบ่อย:
1. latency / jitter / packet loss เกิน threshold ของ SLA
2. probe server ไปไม่ถึง (route ไป server ผิด / interface down / server ไม่ตอบ ping) = member dead ทั้งที่ link ใช้งานได้
3. member interface down (link หลุด, SFP, admin down)
4. failtime / recoverytime ตั้งไว้ไวเกินไป ทำให้ member สลับไปมา
วิธีแก้:
- ดูว่า dead เพราะ probe หรือเพราะ link: `execute ping-options source <member-ip>` แล้ว `execute ping <probe-server>`
- probe server ควรเป็นปลายทางที่เสถียรและไปผ่าน member นั้นจริง (อย่าใช้ IP ที่ ISP block ICMP)
- ปรับ SLA ให้ตรงกับคุณภาพ link จริง: `config system sdwan`, `config health-check`, `edit <name>`, `config sla`, `edit <id>`, `set latency-threshold <ms>`, `set jitter-threshold <ms>`, `set packetloss-threshold <%>`, `next`, `end`, `next`, `end`, `end`
- กันสลับไปมา: ใน health-check เดียวกัน `set failtime <ครั้ง>` / `set recoverytime <ครั้ง>`

---

## SD-WAN rule ไม่ทำงาน / traffic ไม่ออก member ที่ตั้งใจ
ที่มา: [config system sdwan (FortiOS 7.4 CLI)](https://docs.fortinet.com/document/fortigate/7.4.0/cli-reference/76620/config-system-sdwan)
คำค้น: fortigate sd-wan rule not working, sd-wan traffic steering, sd-wan rule order, sd-wan manual mode, sd-wan service
อาการ: traffic ออก link ผิด / SD-WAN rule ไม่ match / traffic ออกตาม implicit rule
คำสั่งตรวจ:
```
diagnose firewall proute list
show system sdwan
get router info routing-table all
```
อ่านผล:
- `diagnose firewall proute list`: SD-WAN rule (และ policy route) ที่ลงตารางจริง พร้อมเงื่อนไข และ member ที่เลือกอยู่ตอนนี้ ถ้า rule ไม่อยู่ในรายการ = ไม่มีผล
- `show system sdwan` ส่วน `config service`: เงื่อนไขของ rule (src / dst / protocol / port / internet-service), mode, member
- routing table: ต้องมี route ไปปลายทางผ่าน member นั้น (เช่น default route ไป SD-WAN zone) ไม่งั้น member นั้นจะไม่ถูกเลือก
วิธีแก้:
- SD-WAN rule ตรวจตามลำดับในรายการ ข้อแรกที่ตรงใช้ ไม่ตรงข้อไหน = ใช้ implicit rule (ตาม load-balance ของ SD-WAN)
- เงื่อนไขของ rule ต้องตรงกับ traffic จริง (src / dst / port) และ member ที่เลือกต้องผ่าน SLA ถ้าใช้ mode ที่อิง SLA
- บังคับ member เฉพาะ: `config system sdwan`, `config service`, `edit <id>`, `set mode manual`, `set priority-members <member-id>`, `next`, `end`, `end`
- traffic ต้องผ่าน firewall policy ที่ออก SD-WAN zone ด้วย

---

## BGP neighbor ไม่ขึ้น / ไล่ทีละสถานะ (Idle / Connect / Active / OpenSent / OpenConfirm)
ที่มา: [Basic BGP example (FortiOS 7.4.4)](https://docs.fortinet.com/document/fortigate/7.4.4/administration-guide/763341/basic-bgp-example)
คำค้น: fortigate bgp neighbor not up, bgp idle connect active opensent established, bgp tcp 179, bgp update-source
อาการ: neighbor ไม่ถึง Established / ค้างสถานะใดสถานะหนึ่ง
คำสั่งตรวจ:
```
get router info bgp summary
get router info bgp neighbors <neighbor-ip>
diagnose sniffer packet any 'tcp port 179' 4 20
```
อ่านผล:
- `summary`: สถานะ (Idle / Active / ...) หรือจำนวน prefix ที่รับ (ถ้าเป็นตัวเลข = Established)
- `neighbors <ip>`: remote AS, เหตุผลที่หลุดครั้งล่าสุด, hold time / keepalive ที่ตกลงกัน
- sniffer: เห็น SYN ไป / กลับบน TCP 179 หรือไม่
ไล่ตามสถานะ:
1. Idle: ยังไม่เริ่ม หรือถูกปิด ตรวจ neighbor IP / remote-as ใน `config router bgp` และ route ไป neighbor (`get router info routing-table details <neighbor-ip>`)
2. Connect / Active: เปิด TCP 179 ไม่สำเร็จ ตรวจ route ไป-กลับ, source IP (`set update-source <interface>` ต้องตรงกับที่อีกฝั่งตั้ง neighbor ไว้), ACL / firewall ระหว่างทาง, eBGP ข้ามหลาย hop ต้อง `set ebgp-enforce-multihop enable`
3. OpenSent / OpenConfirm: TCP ขึ้นแล้วแต่ตกลงกันไม่ได้ ตรวจ remote AS ตรงกันทั้งสองฝั่ง, router-id ไม่ชน, รหัส MD5 (ถ้าใช้) ตรงกัน
4. หลุดบ่อย: ดูเหตุผลใน `neighbors <ip>` (hold timer expired = keepalive หาย มักมาจาก link / CPU / MTU)
วิธีแก้:
- BGP ที่ peer กับตัว FortiGate เองเป็น traffic เข้าตัวเครื่อง (ไม่ผ่าน firewall policy) ถ้ามี local-in policy ต้องอนุญาต TCP 179 จาก neighbor
- BGP ที่วิ่ง**ผ่าน** FortiGate (สองเครื่องข้างนอก peer กัน) ต้องมี firewall policy อนุญาต TCP 179 ทั้งสองทิศ

---

## BGP ขึ้นแล้วแต่ route ไม่เข้า / prefix-list, route-map, next-hop
ที่มา: [config router bgp (FortiOS 7.4 CLI)](https://docs.fortinet.com/document/fortigate/7.4.0/cli-reference/528620/config-router-bgp)
คำค้น: fortigate bgp route not learned, bgp next-hop unreachable, bgp route-map filter, bgp next-hop-self, bgp received-routes
อาการ: neighbor Established แต่ route ไม่ลง routing table / ไม่ได้ prefix ที่คาด
คำสั่งตรวจ:
```
get router info bgp neighbors <neighbor-ip> received-routes
get router info bgp neighbors <neighbor-ip> routes
get router info bgp network
get router info routing-table bgp
show router route-map
show router prefix-list
```
อ่านผล:
- `received-routes`: route ที่ peer ส่งมาก่อนกรอง (ต้องเปิด `set soft-reconfiguration enable` ที่ neighbor ก่อน ไม่งั้นไม่มีข้อมูล)
- `routes`: route ที่รับไว้หลังกรอง
- `get router info bgp network`: ตาราง BGP (เลือก best path แล้วหรือยัง ดูเครื่องหมาย `>`)
- `routing-table bgp`: route จาก BGP ที่ลงตารางจริง
สาเหตุที่พบบ่อย:
1. ถูกกรองด้วย route-map / prefix-list ขาเข้า (มีใน received-routes แต่ไม่มีใน routes)
2. next-hop ไปไม่ถึง: route จาก iBGP ที่ next-hop เป็นเราเตอร์ภายนอก แก้ที่ peer ฝั่งส่งด้วย `set next-hop-self enable` หรือทำ route ไป next-hop
3. แพ้ route อื่นที่ distance ต่ำกว่า (static 10, eBGP 20, OSPF 110, iBGP 200)
4. iBGP ไม่ส่งต่อ route ที่ได้จาก iBGP peer อื่น (ต้อง full-mesh หรือ route-reflector)
วิธีแก้:
- เปิดดู route ก่อนกรอง: `config router bgp`, `config neighbor`, `edit <neighbor-ip>`, `set soft-reconfiguration enable`, `next`, `end`, `end`
- แก้ route-map / prefix-list ที่ผูกกับ neighbor (`route-map-in`, `prefix-list-in`) ให้ permit prefix ที่ต้องการ
- หลังแก้ policy: `execute router clear bgp ip <neighbor-ip> soft in` (soft = ไม่ตัด session)

---

## ลำดับการเลือกเส้นทาง / policy route, SD-WAN rule, routing table
ที่มา: [Routing concepts (FortiOS 7.4.2)](https://docs.fortinet.com/document/fortigate/7.4.2/administration-guide/139692/routing-concepts)
คำค้น: fortigate sd-wan vs static route, sd-wan vs policy route, sd-wan route priority, fortigate routing order, policy route ไม่ทำงาน
อาการ: traffic ออก interface ผิด, SD-WAN rule ไม่ทำงาน, policy route ไม่ match, static route ชนะ SD-WAN
คำสั่งตรวจ:
```
diagnose firewall proute list
show router policy
show router static
get router info routing-table details <dst-ip>
```
อ่านผล:
- `diagnose firewall proute list`: policy route และ SD-WAN rule ที่ลงตาราง (ตรวจก่อน routing table) เรียงตามลำดับที่ใช้จริง
- `get router info routing-table details <dst-ip>`: route ที่ชนะสำหรับปลายทางนั้นใน routing table
ลำดับที่ FortiGate ใช้:
1. policy route (`config router policy`) ตรวจก่อน
2. SD-WAN rule (`config system sdwan` → `config service`)
3. ไม่ตรงข้อไหน: routing table (route ที่ distance / priority ดีที่สุด รวม route ที่ชี้ไป SD-WAN zone)
วิธีแก้:
- policy route ที่กว้างเกินไปจะทำให้ SD-WAN rule ไม่เคยทำงาน ให้ตรวจ `diagnose firewall proute list` ว่าข้อไหนอยู่บนสุดและตรงก่อน
- SD-WAN rule เลือก member ได้เฉพาะเมื่อ routing table มี route ไปปลายทางผ่าน member นั้น
- static route ที่ชี้ออก interface ที่ไม่ใช่ SD-WAN member จะไม่ผ่าน SD-WAN เลย
