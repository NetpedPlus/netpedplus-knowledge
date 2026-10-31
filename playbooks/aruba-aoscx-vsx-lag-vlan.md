---
id: aruba-aoscx-vsx-lag-vlan
title: Aruba AOS-CX — VSX, LAG, VLAN ไม่ผ่าน
families: aruba_aoscx
triggers: aruba, aoscx, aos-cx, aos cx, cx 6200, cx 6300, cx 6400, cx 8320, cx 8325, cx 8360, cx 8400, cx 10000, cx6200, cx6300, cx6400, cx8320, cx8325, cx8360, cx8400, cx10000, cx-6200, cx-6300, cx-6400, cx-8320, cx-8325, cx-8360, cx-8400, cx-10000, vsx, virtual switching extension, inter-switch-link, isl, multi-chassis, lacp, lacp mode, lacp hash, lacp port-priority, vlan trunk, vlan access, vlan not passing
vendor: Aruba (HPE)
versions: AOS-CX 10.07 — 10.16
sources: https://arubanetworking.hpe.com/techdocs/AOS-CX/10.07/HTML/5200-7839/Content/VSX_cmds/sho-vsx-sta-10.htm; https://arubanetworking.hpe.com/techdocs/AOS-CX/10.07/HTML/5200-7836/Content/VSX_cmds/sho-vsx-cnf-10.htm; https://www.arubanetworks.com/techdocs/AOS-CX/10.16/HTML/vsx/Content/VSX_cmds/vsx.htm; https://www.arubanetworks.com/techdocs/AOS-CX/10.07/HTML/5200-7888/Content/VSX_cmds/int-swi-lin-10.htm
---
# Aruba AOS-CX — VSX, LAG, VLAN ไม่ผ่าน

## VSX (Virtual Switching Extension) | ISL ไม่ขึ้น / Config Sync ไม่ผ่าน
คำค้น: vsx, virtual switching extension, vsx cluster, cluster, inter-switch-link, isl, isl not up, mclag, mclag not working, config sync not through, split recovery, primary secondary, show vsx status, show vsx configuration, is-in-sync, not-in-sync, vsx split, isl keepalive
อาการ: VSX pair ไม่เชื่อมต่อกัน, ISL ไม่ขึ้น, Config Sync ไม่ผ่าน, VSX Split เกิดขึ้น, Primary/Secondary role ไม่ชัดเจน, MCLAG ไม่ทำงาน
คำสั่งตรวจ:
```
show vsx status
show vsx configuration inter-switch-link
show vsx configuration keepalive
```
อ่านผล:
- `show vsx status`: ดู VSX Operational State — ISL channel ต้องเป็น **In-Sync**, Config Sync Status ต้องเป็น **in-sync**, NAE ต้องเป็น **peer_reachable**, HTTPS Server ต้องเป็น **peer_reachable**
- `show vsx status inter-switch-link`: ดู ISL status — State ต้องเป็น **In-Sync**, Link Status ต้องเป็น **up**
- `show vsx status keepalive`: ดู Keepalive state — ต้องเป็น **Keepalive-Established**
- `show vsx configuration inter-switch-link`: ดู ISL config — Hello, Dead Interval, Hold Time, Peer detect interval
สาเหตุที่พบบ่อย:
1. ISL port ไม่ขึ้น — ตรวจ physical link, port config, allowed VLAN
2. Keepalive ไม่เชื่อมต่อกัน — ตรวจ keepalive interface, source/peer IP, UDP port
3. Config Sync ไม่ผ่าน — ตรวจ vsx-sync configuration, software version ต้องตรงกัน
4. Software version ไม่ตรง — primary และ secondary ต้องใช้ version เดียวกัน
5. Split Recovery — linkup-delay timer ยังทำงานอยู่
วิธีแก้:
- Enable VSX: `config` → `vsx` → `inter-switch-link <port>` (เช่น `inter-switch-link 1/1/43`)
- Set device role: `config` → `vsx` → `role primary` (หรือ `role secondary`)
- Configure keepalive: `config` → `vsx` → `keepalive peer <peer-ip> source <source-ip>` (เช่น `keepalive peer 192.168.1.1 source 192.168.1.5`)
- Enable vsx-sync: `config` → `vsx` → `vsx-sync <feature>` (เช่น `vsx-sync aaa`, `vsx-sync vsx-global`, `vsx-sync mclag-interfaces`)
- Verify: `show vsx status` → ต้องเห็น In-Sync ทุกค่า
ระวัง: หลัง config change บน primary ต้องรอ Config Sync ผ่านก่อนแก้ไข secondary
ที่มา: show vsx status, show vsx configuration (AOS-CX 10.07) https://arubanetworking.hpe.com/techdocs/AOS-CX/10.07/HTML/5200-7839/Content/VSX_cmds/sho-vsx-sta-10.htm

## LAG (Link Aggregation) | LACP ไม่ negotiate / member port ไม่เข้า bond
คำค้น: lacp, link aggregation, lag, port channel, lacp not negotiate, lacp mode, lacp active passive, lacp hash, lacp port-priority, show interface lag, lacp hash l2-src-dst, lacp rate, member port down, lag not up, multi-chassis
อาการ: LAG ไม่ขึ้น, LACP ไม่ negotiate, member port ไม่เข้า bond, port ใน LAG ไม่ balanced, LACP hash ไม่ถูกต้องการ
คำสั่งตรวจ:
```
show interface lag <lag-id>
show interface lag <lag-id> statistics
```
อ่านผล:
- `show interface lag <lag-id>`: ดู LAG status — Aggregate ต้องเป็น **up**, Admin state ต้องเป็น **up**, member count ต้องครบ, Aggregated-interfaces แสดง port member, Aggregate mode (active/passive)
- `show interface lag <lag-id> statistics`: ดู statistics — packets tx/rx, broadcast/multicast, errors
สาเหตุที่พบบ่อย:
1. LACP mode ไม่ตรงกัน — side หนึ่งเป็น **active** อีก side เป็น **passive** หรือ **on** (static)
2. LACP hash type ไม่เหมาะสม — ใช้ l2-src-dst, l3-src-dst, หรือ l4-src-dst
3. Port priority ไม่ถูกต้องการ — port ที่มี priority ต่ำกว่าจะ active เป็นหลัก
4. Partner switch ไม่รองรับ LACP — ต้องเปลี่ยนเป็น static trunk
5. Member port มี speed/duplex ไม่ตรงกัน
วิธีแก้:
- Create LAG: `config` → `interface lag <id>` → `no shutdown` → `lacp mode active` → `lacp hash l2-src-dst`
- Add member port: `config` → `interface <port>` → `no shutdown` → `lag <lag-id>` (เช่น `interface 1/1/11` → `lag 2`)
- Set port priority: `config` → `interface <port>` → `lacp port-priority <priority>` (ค่า default = 1, ค่าต่ำกว่า = ถูกเลือกก่อน)
- Set lacp rate: `config-lag-if` → `lacp rate fast` (หรือ `lacp rate slow`)
- สำหรับ VSX multi-chassis LAG: `config` → `interface lag <id>` → `multi-chassis`
- Verify: `show interface lag 2` → ต้องเห็น Aggregated-interfaces แสดง port member ครบ
ระวัง: ระหว่างแก้ไข LAG, port จะลงชั่วคราว — ทำในช่วง maintenance
ที่มา: show interface lag (AOS-CX) https://www.arubanetworks.com/techdocs/AOS-CX/AOSCX-CLI-Bank/cli_6200/Content/Chp_LAG/LACP_LAG_cmds/sho-int.htm

## VLAN ไม่ผ่าน | traffic ไม่ผ่าน VLAN
คำค้น: vlan, vlan not passing, vlan not working, trunk port not working, access port not working, native vlan, allowed vlan, vlan mapping, show vlan, show vlan port, interface vlan, create vlan, no routing, no shutdown
อาการ: อุปกรณ์ใน VLAN ไม่ ping กัน, VLAN ไม่ผ่าน switch, trunk port ไม่ส่ง traffic, access port ไม่ทำงาน, native VLAN ไม่ตรงกัน, allowed VLAN ไม่ครบ
คำสั่งตรวจ:
```
show vlan <vlan-id>
show vlan port <interface>
show interface vlan <vlan-id>
```
อ่านผล:
- `show vlan <vlan-id>`: ดู VLAN config — status, name, ports ที่อยู่ใน VLAN, mode (access/trunk/native-untagged)
- `show vlan port <interface>`: ดู VLAN ที่ configure บน port — mode (access/trunk), mapping (arp, ipv4, ipv6)
- `show interface vlan <vlan-id>`: ดู SVI status — admin state, protocol state, IP address
สาเหตุที่พบบ่อย:
1. Port mode ไม่ตรงกัน — access port ไม่สามารถรับ trunk traffic ได้
2. Allowed VLAN ไม่ครบ — trunk port ไม่ได้ allow VLAN ที่ต้องการ
3. Native VLAN ไม่ตรงกัน — native VLAN ระหว่าง switch ไม่ตรงกัน → VLAN leak
4. VLAN ไม่ได้สร้าง — `show vlan` → VLAN ไม่อยู่ในรายการ
5. SVI ไม่ได้สร้างหรือ admin down — `show interface vlan` → admin state down
6. Port ไม่ได้ enable — `no shutdown`
7. รุ่น 8xxx/10000 ต้อง disable routing ก่อนเป็น L2 — `no routing`
วิธีแก้:
- Create VLAN: `config` → `vlan <id>` → `name <name>` (เช่น `vlan 100` → `name DATA_VLAN`)
- Configure trunk port: `config` → `interface <port>` → `no shutdown` → `no routing` (ถ้าเป็นรุ่น 8xxx/10000) → `vlan trunk native <id>` → `vlan trunk allowed <list>` (เช่น `vlan trunk allowed 100-200`)
- Configure access port: `config` → `interface <port>` → `no shutdown` → `no routing` (ถ้าเป็นรุ่น 8xxx/10000) → `vlan access <id>`
- Create SVI: `config` → `interface vlan <id>` → `no shutdown` → `ip address <ip>/<mask>`
- Verify: `show vlan port <port>` → ต้องเห็น VLAN ที่ต้องการ
ระวัง: การเปลี่ยน trunk mode ระหว่าง traffic flowing จะทำให้ traffic drop ชั่วคราว
ที่มา: show vlan port (AOS-CX 10.09) https://www.arubanetworks.com/techdocs/AOS-CX/10.09/HTML/cli_832x/Content/Chp_VLANs/VLAN_cmds/sho-vla-por.htm
