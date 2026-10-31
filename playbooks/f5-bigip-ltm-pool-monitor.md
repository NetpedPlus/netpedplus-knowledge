---
id: f5-bigip-ltm-pool-monitor
title: F5 BIG-IP LTM — Pool Member Monitor Down / Pool ไม่ผ่าน
families: f5_tmsh
triggers: f5, bigip, big-ip, BIG-IP, LTM, pool member down, pool member monitor down, monitor not working, pool not passing traffic, health monitor, health monitor down, manual resume, pool availability, traffic not passing, pool is down, pool availability down, member disabled
vendor: F5 Networks
versions: BIG-IP 14.0 — 21.1
sources: https://techdocs.f5.com/en-us/bigip-16-0-0/big-ip-local-traffic-manager-monitors-reference/monitors-settings-reference.html
---
# F5 BIG-IP LTM — Pool Member Monitor Down / Pool ไม่ผ่าน

## Pool Member Monitor Down | traffic ไม่ผ่าน pool
คำค้น: pool member down, pool member monitor down, monitor down, health monitor down, monitor not working, pool is down, pool unavailable, traffic not passing through pool, pool availability, availability down, member disabled, member down, node down, node monitoring, manual resume, forced down, user-down, forced offline
อาการ: pool member status down, traffic ไม่ผ่าน pool, health monitor ไม่ได้ตรวจสอบ pool member, pool availability แสดง down, member status forced down, member status user-disabled, member status down จาก monitor
คำสั่งตรวจ:
```
tmsh show ltm pool <pool-name>
tmsh show ltm monitor <monitor-type> <monitor-name>
tmsh list ltm pool <pool-name>
```
อ่านผล:
- `tmsh show ltm pool <pool-name>`: ดู pool status, availability (All Members Up / One or More Members Down / No Members Up), member list พร้อม status (up/down/disabled/forced-down)
- `tmsh show ltm monitor <type> <name>`: ดู monitor status, interval, timeout, up-interval, state (up/down/unknown) พร้อม state time
- `tmsh list ltm pool <pool-name>`: ดู pool config, member list, monitor associated, load balancing method
สาเหตุที่พบบ่อย:
1. Monitor timeout = 31 sec, interval = 10 sec — ถ้า backend delay เกิน timeout จะ down
2. Manual Resume = Yes — ต้อง manual re-enable หลัง recovery
3. Monitor type ไม่เหมาะสม — HTTP monitor แต่ backend เป็น HTTPS หรือ port ไม่ตรง
4. Backend application crash — service ไม่ respond ที่ port monitor ตรวจสอบ
5. Node/IP ไม่ respond — network issue, firewall block, node down
วิธีแก้:
- ตรวจ monitor status: `tmsh show ltm monitor <type> <name>` → ดู state time, last error
- เปลี่ยน monitor type ให้ตรงกับ backend protocol — HTTP/HTTPS/TCP/Gateway-ICMP
- เพิ่ม timeout (default = 31 sec) ถ้า backend ใช้เวลานานในการ respond
- ตรวจสอบ backend service: `tmsh show ltm monitor <type> <name> detail`
- Enable monitoring logging: `tmsh modify ltm pool <name> members modify { <addr:port> { logging enabled } }`
- Force member up (emergency): `tmsh modify ltm pool <name> members modify { <addr:port> { session user-enabled state forced-up } }`
- Manual resume: ถ้า Manual Resume = Yes ต้องเปลี่ยน state เป็น user-enabled
ที่มา: Monitors Settings Reference (BIG-IP 16.0) https://techdocs.f5.com/en-us/bigip-16-0-0/big-ip-local-traffic-manager-monitors-reference/monitors-settings-reference.html

## Pool Configuration | สร้าง pool/member/monitor ไม่ผ่าน
คำค้น: create pool, create monitor, create pool member, tmsh create ltm pool, tmsh modify ltm pool, tmsh create ltm monitor, pool configuration, member configuration, monitor association, pool member add, pool member modify, pool member delete, monitor type, pool load balancing, pool member weight, pool member ratio, pool session, persist, cookie affinity, source affinity, client persistence, server persistence
อาการ: สร้าง pool แล้ว member ไม่ up, monitor ไม่ทำงานกับ pool, traffic ไม่ผ่าน pool ที่สร้างใหม่, pool member ไม่ respond
คำสั่งตรวจ:
```
tmsh list ltm pool <pool-name>
tmsh list ltm monitor <monitor-type> <monitor-name>
tmsh list ltm node <node-name>
```
อ่านผล:
- `tmsh list ltm pool <pool-name>`: ดู pool members, monitor associated, load balancing method, session status
- `tmsh list ltm monitor <type> <name>`: ดู monitor settings — destination, interval, timeout, send/recv strings (HTTP)
- `tmsh list ltm node <name>`: ดู node address, availability status
สาเหตุที่พบบ่อย:
1. Monitor destination ไม่ตรงกับ pool member port — HTTP monitor ไป port 80 แต่ member serve ที่ 8080
2. Load balancing method ไม่เหมาะสม — round-robin กับ persistent session
3. Node ไม่ได้ associate กับ pool member — member ใช้ node IP ที่ไม่มีอยู่
4. Monitor send/recv string ไม่ถูก — HTTP monitor ต้องมี response string ที่ตรงกับ backend
วิธีแก้:
- Create monitor: `tmsh create ltm monitor http <name> destination *:<port> interval 10 timeout 31`
- Create pool: `tmsh create ltm pool <name> members add { <addr:port> } monitor <monitor-name>`
- Create node: `tmsh create ltm node <name> address <ip-address>`
- Add member: `tmsh modify ltm pool <name> members add { <addr:port> { weight 1 } }`
- Change load balancing: `tmsh modify ltm pool <name> load-balancing-mode <round-robin|least-connections|observed>`
- Verify: `tmsh show ltm pool <name>` → ต้องเห็น member status
ที่มา: Monitors Settings Reference (BIG-IP 16.0) https://techdocs.f5.com/en-us/bigip-16-0-0/big-ip-local-traffic-manager-monitors-reference/monitors-settings-reference.html
