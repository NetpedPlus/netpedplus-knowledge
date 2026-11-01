---
id: fortigate-74-sdwan-bgp
title: FortiGate 7.4 SD-WAN + BGP troubleshooting: SD-WAN member, SD-WAN rule, BGP neighbor, BGP route, SD-WAN vs routing
families: fortinet_fortios
triggers: fortigate sd-wan member status, sd-wan health-check sla, sd-wan member out of sla, sd-wan health-check fix, sd-wan rule not working, sd-wan traffic steering, fortigate bgp neighbor not up, bgp idle active opensent established, bgp route not learned, bgp next-hop unreachable, sd-wan vs static route priority, fortigate sd-wan policy route order
versions: FortiOS 7.4.x
sources: https://docs.fortinet.com/document/fortigate/7.4.0/administration-guide/867342/performance-sla-overview, https://docs.fortinet.com/document/fortigate/7.4.0/administration-guide/942095/sd-wan-members-and-zones, https://docs.fortinet.com/document/fortigate/7.4.0/cli-reference/76620/config-system-sdwan, https://docs.fortinet.com/document/fortigate/7.4.4/administration-guide/763341/basic-bgp-example, https://docs.fortinet.com/document/fortigate/7.4.0/cli-reference/528620/config-router-bgp
---

# FortiGate 7.4 SD-WAN + BGP troubleshooting / หัวข้อ: SD-WAN member, SD-WAN rule, BGP neighbor, BGP route, SD-WAN vs routing

## SD-WAN member / zone / health-check (SLA) / สถานะ และทำไม member ถูกตัด
ที่มา:
- https://docs.fortinet.com/document/fortigate/7.4.0/administration-guide/867342/performance-sla-overview (Performance SLA overview)
- https://docs.fortinet.com/document/fortigate/7.4.0/administration-guide/942095/sd-wan-members-and-zones (SD-WAN members and zones)
- https://docs.fortinet.com/document/fortigate/7.4.0/cli-reference/76620/config-system-sdwan (config system sdwan)

อาการ: member ถูก out of SLA / SD-WAN rule ใช้ member อื่นแทน / traffic ไม่ออก link ที่ตั้งใจ
คำค้น: fortigate sd-wan member out of sla, sd-wan health-check status, sd-wan zone status
คำสั่งตรวจ:
```
get system sdwan health-check
get system sdwan zone
diagnose sdwan health-check show
```
อ่านผล:
- `get system sdwan health-check` — ดู health-check status, members, pass/fail
- `get system sdwan zone` — ดู SD-WAN zone, members, in/out of SLA
- `diagnose sdwan health-check show` — ดูผลลัพธ์ SLA probe (latency, jitter, packet loss, timestamp)
สาเหตุที่ member ถูก out of SLA:
1. Health-check SLA target ไม่ผ่าน — latency/jitter/packet loss เกิน threshold
2. Health-check server เข้าไม่ได้ — unreachable (route ผิด, interface down)
3. Member interface down — link หลุด, SFP มีปัญหา, admin shutdown
4. Probe timeout / failtime เกิน — probe-timeout / failtime ตั้งสั้นเกินไป
5. SD-WAN zone out of SLA — `minimum-sla-meet-members` ตั้งสูงเกิน
## SD-WAN member / health-check / วิธีแก้ member ถูกตัด
ที่มา:
- https://docs.fortinet.com/document/fortigate/7.4.0/cli-reference/76620/config-system-sdwan (config system sdwan)
คำค้น: fortigate sd-wan health-check fix, set failtime recoverytime, sd-wan member threshold
คำสั่งตรวจ:
```
get system sdwan health-check
get system sdwan zone
```
วิธีแก้:
- ตรวจ health-check status: `get system sdwan health-check` ดูว่า member ใดออกนอก SLA แล้วตรวจค่า latency/jitter/packet loss
- ถ้า server เข้าไม่ได้ — ตรวจ routing ไปยัง server (`get router info routing-table <server-ip>`) / ตรวจ interface (`ping <server-ip> source <interface>`)
- ถ้า latency/jitter สูงเกิน — ปรับ threshold ให้เหมาะสมกับ link หรือเปลี่ยน probe server ให้ใกล้กว่า
- ถ้า member interface down — ไล่ปัญหา interface แยก
- ถ้า failtime/recoverytime ตั้งไม่เหมาะสม — ปรับ `set failtime <count>` `set recoverytime <count>` `set probe-timeout <ms>`
- `config system sdwan` → `config health-check` → `edit <name>` → `set failtime <count>` → `set recoverytime <count>` → `set probe-timeout <ms>`
- ตรวจ SD-WAN zone status: `get system sdwan zone` ดู zone-level status ถ้า zone out of SLA ทุก member จะ out SLA ทั้งที่บาง member ยังปกติ

## SD-WAN rule ไม่ทำงาน / traffic ไม่ออก member ที่ตั้งใจ
ที่มา:
- https://docs.fortinet.com/document/fortigate/7.4.0/cli-reference/76620/config-system-sdwan (config system sdwan — config service)
- https://docs.fortinet.com/document/fortigate/7.4.0/administration-guide/942095/sd-wan-members-and-zones (SD-WAN members and zones)

อาการ: traffic ออก link ผิด / SD-WAN rule ไม่ match traffic / traffic ไม่ใช้ SD-WAN
คำค้น: fortigate sd-wan rule not working, sd-wan traffic steering, sd-wan rule order, sd-wan manual mode
คำสั่งตรวจ:
```
get system sdwan service
get system sdwan member
diagnose sdwan service list
```
- `get system sdwan service` — ดู service rules ทั้งหมด, status, mode (auto/manual/SLA), members, priority
- `get system sdwan member` — ดู SD-WAN members, status in/out of SLA
- `diagnose sdwan service list` — ดู service rule detail
วิธีแก้:
- ตรวจว่า SD-WAN rule match traffic จริงหรือไม่ — ดู src/dst address, protocol, port, internet-service, zone ที่กำหนดใน rule ให้ตรงกับ traffic จริง
- ตรวจ order ของ SD-WAN rules — rule 1 มีผลก่อน rule 2 traffic ที่ match rule 1 จะไม่ผ่าน rule 2
- ตรวจว่า zone ที่ member อยู่ มีสถานะ in/out of SLA ถ้า out of SLA และ rule เป็น SLA mode จะใช้ member อื่นแทน
- ตรวจว่า rule เป็น mode auto (เลือก member จาก cost/SLA) หรือ manual (บังคับใช้ member เฉพาะ) ให้เลือกให้เหมาะกับสถานการณ์
- ถ้าต้องการบังคับใช้ member เฉพาะ: `config system sdwan` → `config service` → `edit <id>` → `set mode manual` → `set priority-members 1` (หรือ member ID ที่ตั้งใจ)
- ตรวจ firewall policy — traffic ต้องผ่าน firewall policy อนุญาตถึงจะถูก SD-WAN rule handle
- ตรวจว่า traffic ออกผ่าน interface ใน SD-WAN zone จริง — `get router info routing-table all` ดูว่า default route / route ไปยัง dst point ไปทาง SD-WAN member

## BGP neighbor ไม่ขึ้น / ไล่ทีละสถานะ (Idle / Connect / Active / OpenSent / OpenConfirm / Established)
ที่มา:
- https://docs.fortinet.com/document/fortigate/7.4.4/administration-guide/763341/basic-bgp-example (Basic BGP example)
- https://docs.fortinet.com/document/fortigate/7.4.0/cli-reference/528620/config-router-bgp (config router bgp)

อาการ: BGP neighbor ไม่ขึ้น / ค้างที่สถานะใดสถานะหนึ่ง
คำค้น: fortigate bgp neighbor not up, bgp idle connect active opensent established, bgp tcp 179, bgp update-source
คำสั่งตรวจ:
```
get router info bgp summary
get router info bgp neighbors
diagnose sniffer packet any 'tcp and port 179'
```
อ่านผล:
- `get router info bgp summary` — ดู neighbor status, AS, uptime, prefixes
- `get router info bgp neighbors` — ดู detail ของแต่ละ neighbor
ไล่ตามสถานะ:
1. Idle — ยังไม่เริ่ม BGP process กับ neighbor
   - ตรวจ `config router bgp` → `set as <local-as>` enabled
   - ตรวจ neighbor IP / remote AS ถูกต้อง
   - eBGP multiple hops ต้องเปิด `set ebgp-enforce-multihop enable`
   - ตรวจ routing: `ping <neighbor-ip> source <interface>`
2. Connect — BGP process เริ่มแล้ว แต่ยังไม่มี TCP connection
   - ตรวจ routing ไปยัง neighbor IP (TCP 179 ต้องไปถูกทาง)
   - ตรวจ firewall policy อนุญาต TCP 179
   - ระวัง: stateful inspection อาจบล็อก TCP handshake
3. Active — เริ่ม TCP connection แล้ว แต่ไม่มี response
   - neighbor ไม่ส่ง response — ตรวจ BGP config ถูกต้อง / neighbor ไม่ shutdown
   - ตรวจ TCP port 179 เปิดทั้งสองฝั่ง: `diagnose sniffer packet any 'tcp and port 179'`
   - ระวัง: `update-source` ไม่ตรง — ใช้ source IP ผิด interface
4. OpenSent — TCP connection สำเร็จแล้ว แต่รอ BGP message
   - ตรวจ AS number ตรงกัน, router-id ไม่ชน
   - ตรวจ BGP capabilities (MD5 auth, TTL security) ตรงทั้งสองฝั่ง
5. OpenConfirm — Open message แลกเปลี่ยนแล้ว รอ Keepalive
   - ตรวจ keepalive / hold-timer ตรงกัน (hold-time 180s, keepalive 60s)
   - ตรวจ TCP session ยัง alive
6. Established — BGP fully up — ตรวจ prefix: `get router info bgp neighbors <ip> received-routes` / `advertised-routes`

## BGP neighbor ขึ้นแล้ว แต่ route ไม่เข้า / ตรวจ prefix-list, route-map, next-hop, recursive
ที่มา:
- https://docs.fortinet.com/document/fortigate/7.4.4/administration-guide/763341/basic-bgp-example (Basic BGP example)
- https://docs.fortinet.com/document/fortigate/7.4.0/cli-reference/528620/config-router-bgp (config router bgp)

อาการ: BGP neighbor = Established แต่ไม่มี routes ใน routing-table
คำค้น: fortigate bgp route not learned, bgp next-hop unreachable, bgp route-map filter, bgp next-hop-self, bgp split horizon
คำสั่งตรวจ:
```
get router info bgp neighbors <ip> received-routes
get router info bgp network
get router info routing-table all
```
อ่านผล:
- `received-routes` — neighbor ส่ง prefix มาหรือไม่
- `get router info bgp network` — BGP network table
- `get router info routing-table all` — routing-table (prefix ที่ลง table)
สาเหตุที่ route ไม่ลง routing-table:
1. Next-hop unreachable — next-hop ไม่มีการ routing path ไปถึง
   - ตรวจ: `get router info routing-table <next-hop-ip>`
   - แก้: เพิ่ม static route ไปยัง next-hop / ตรวจ IPsec VPN / interface up
2. prefix-list / route-map filter — BGP filter ตัด route
   - ตรวจ: `get system router-policy` ดู prefix-list / route-map ทั้งหมด
   - ตรวจ neighbor config: ดู `route-map-in` / `prefix-list-in`
   - แก้: แก้ filter rule (permit/deny) / ลบ filter
3. AS path filter / community list filter — BGP filter ตัด route
   - ตรวจ: `config router aspath-list` / `config router community-list`
4. iBGP split-horizon — iBGP ไม่ advertise route ที่ได้มาจาก iBGP peer
   - แก้: route-reflector / confederation / redistribution เป็น OSPF / full-mesh iBGP
5. iBGP ไม่เปลี่ยน next-hop — next-hop เป็น ISP router ที่ FortiGate ไม่ได้
   - แก้: `set next-hop-self enable` บน neighbor ที่ advertise route ไปยัง iBGP peer
   - `config router bgp` → `config neighbor` → `edit <ip>` → `set next-hop-self enable`
6. Local pref / MED / AS path — route path แย่กว่า static route (dist 10) / OSPF (dist 110)
   - BGP eBGP dist 20, iBGP dist 200 — route เหล่านี้จะลงก่อน
   - แก้: เปลี่ยน local preference / MED / administrative distance

## SD-WAN vs static route vs policy route / ลำดับความสำคัญเวลา traffic เลือกทางออก
ที่มา:
- FortiOS 7.4 Administration Guide — SD-WAN, Policy Route, Static Route
- FortiOS CLI Reference — `config system policy-route`, `config router static`

อาการ: traffic ออก interface ผิด, SD-WAN rule ไม่ทำงาน, policy route ไม่ match, static route ชนะ SD-WAN
คำค้น: fortigate sd-wan vs static route, sd-wan vs policy route, sd-wan route priority, fortigate routing order
คำสั่งตรวจ:
```
get system sdwan service
get router info routing-table all
get system policy-route
get system routing static
diagnose ip route filter <dst-ip>
```
อ่านผล:
- `get system sdwan service` — ดู SD-WAN service rules
- `get router info routing-table all` — ดู routing-table ทั้งหมด
- `get system policy-route` — ดู policy route rules
- `diagnose ip route filter <dst-ip>` — ดูว่า traffic ไปทาง route ไหน (แทน static route, policy route, SD-WAN)
1. VDOM-local traffic — traffic stay ใน VDOM เดียวกัน (inter-VLAN, loopback)
2. Policy route (policy-based routing) — `config system policy-route` บังคับเส้นทางเฉพาะ traffic ที่ match policy
3. SD-WAN rule — traffic ที่ match SD-WAN service rule จะใช้ SD-WAN member เลือกทางออก
4. Policy route fallback — หาก policy route ไม่มี interface ที่ match จะตกไปใช้ route ธรรมดา
5. Static route — เส้นทางที่กำหนดเอง (admin distance 10)
6. BGP/OSPF route — learned จาก routing protocol
7. Default route — `0.0.0.0/0` (ถ้าวางเป็น static จะอยู่ลำดับเดียวกับ static route)

ระวังสำคัญ:
- SD-WAN rule จะทำงานก็ต่อเมื่อ traffic เลือก interface ที่เป็น SD-WAN member อยู่แล้ว — ถ้า static route / policy route บังคับออก interface อื่น SD-WAN rule ไม่เคยทำงาน
- Policy route มีผลเหนือ SD-WAN rule — ถ้ามี policy route match traffic นั้น traffic จะถูกบังคับออก interface ที่ policy กำหนด (ไม่ผ่าน SD-WAN)
- Static route ที่ชี้ไป SD-WAN interface — traffic จะเข้า SD-WAN rule ถ้ามี rule match แต่ถ้าไม่มี rule match จะออกตาม cost ของ SD-WAN member (auto selection)
- ถ้ามีทั้ง SD-WAN และ policy route match traffic เดียวกัน → policy route ชนะ
- SD-WAN rule ไม่ทำงานบน interface ที่เป็น input ของ policy route (policy route จัดการออกก่อน)
- ใช้ `diagnose ip route filter <dst-ip>` หรือ `get router info routing-table <dst-ip>` ดูว่า traffic ไปทาง route ไหนก่อน
- ตรวจ SD-WAN rule order: `get system sdwan service` — rule แรกที่มี match จะใช้งาน (first-match)
