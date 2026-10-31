---
id: fortigate-traffic-shaping
title: FortiGate 7.4 Traffic Shaping / QoS (bandwidth ไม่พอ, traffic ไม่ผ่าน)
families: fortinet_fortios
triggers: fortigate, fortios, shaping-profile, shaping-policy, traffic-class, egress-shaping-profile, outbandwidth, traffic-shaper, per-ip-shaper
vendor: Fortinet
versions: FortiOS 7.4.x (7.4.0 - 7.4.13)
sources: https://docs.fortinet.com/document/fortigate/7.4.2/administration-guide/297431/traffic-shaping
---
# FortiGate 7.4 Traffic Shaping / QoS (bandwidth ไม่พอ, traffic ไม่ผ่าน)

## Traffic Shaping | ตรวจว่า traffic ถูก shaping แล้วหรือไม่
คำค้น: traffic shaping, shaping-profile, traffic-class, shaping check, shaping debug, shaping trace, outbandwidth, guaranteed bandwidth, shaping not working, traffic slow
อาการ: traffic ไม่ผ่าน — ต้องการดูว่า shaping config ถูกต้องหรือไม่, bandwidth ไม่พอ — ต้องการดู shaping profile, traffic ช้า — ต้องการดู class ไหนใช้ bandwidth มากสุด
คำสั่งตรวจ:
```
get firewall shaping-profile
get firewall traffic-class
get system interface <interface-name>
show firewall shaping-policy
diagnose firewall shaper traffic-shaper list
```
อ่านผล:
- `get firewall shaping-profile`: ดู shaping profile ทั้งหมด — class-id, guaranteed-bandwidth-percentage, maximum-bandwidth-percentage, priority
- `get firewall traffic-class`: ดู traffic class ทั้งหมด — class-id, class-name
- `get system interface <interface-name>`: ดู interface configuration — egress-shaping-profile, outbandwidth
- `show firewall shaping-policy`: shaping-policy ที่ส่ง traffic เข้า class (ดูเงื่อนไข srcaddr / dstaddr / service / srcintf / dstintf ว่าตรง traffic จริงไหม)
- `diagnose firewall shaper traffic-shaper list`: shared shaper ที่ใช้งาน (ตั้งใน policy / shaping-policy) — bandwidth ปัจจุบัน และ packet ที่ถูก drop
สาเหตุที่พบบ่อย:
1. Interface ยังไม่ได้ config egress-shaping-profile — shaping ไม่ทำงาน
2. Interface ยังไม่ได้ config outbandwidth — shaping ไม่ทำงาน (shaping ใช้ % ของ outbandwidth)
3. Guaranteed bandwidth รวมเกิน 100% — config ผิด
4. Shaping profile type ผิด (policing vs queuing) — policing drop traffic เมื่อเกิน bandwidth, queuing delay traffic
วิธีแก้:
- แก้ shaping-profile: `config firewall shaping-profile` → `edit <name>` → `set type {policing|queuing}` → `config shaping-entries` → `edit <id>` → `set class-id <integer>` → `set priority {top|critical|high|medium|low}` → `set guaranteed-bandwidth-percentage <integer>` → `set maximum-bandwidth-percentage <integer>` → `next end next end` (เอกสาร: Traffic shaping profiles, FortiOS 7.4 Administration Guide)
- แก้ interface: `config system interface` → `edit <name>` → `set egress-shaping-profile <profile-name>` → `set outbandwidth <kbps>` → `next end` (เอกสาร: Interface-based traffic shaping profile, FortiOS 7.4 Administration Guide)
ที่มา: Traffic shaping profiles (FortiOS 7.4 Administration Guide) https://docs.fortinet.com/document/fortigate/7.4.7/administration-guide/626246/traffic-shaping-profiles

## Traffic Shaping | สร้าง shaping policy และ shaping-profile
คำค้น: shaping-profile create, shaping-profile config, traffic-class config, shaping-policy config, create shaping-profile, create traffic-class, create shaping-policy, shaping policy, shaping profile, class-id, guaranteed bandwidth, maximum bandwidth, outbandwidth, egress shaping, interface shaping, polic shaping, queuing shaping
อาการ: ต้องการสร้าง shaping policy ใหม่, ต้องการให้ interface ใช้ shaping, traffic ต้องถูก prioritize, ต้องการให้ shaping profile ทำงาน
คำสั่งตรวจ:
```
get firewall shaping-profile
get firewall traffic-class
```
อ่านผล:
- `get firewall shaping-profile`: ดู shaping profile ทั้งหมด — class-id, guaranteed-bandwidth-percentage, maximum-bandwidth-percentage, priority
- `get firewall traffic-class`: ดู traffic class ทั้งหมด — class-id, class-name
- shaping-profile type: policing (drop traffic เมื่อเกิน bandwidth) / queuing (delay traffic เมื่อเกิน bandwidth)
วิธีแก้:
- สร้าง traffic-class: `config firewall traffic-class` → `edit <integer>` → `set class-name <string>` → `next end` (เอกสาร: Interface-based traffic shaping profile, FortiOS 7.4 Administration Guide)
- สร้าง shaping-profile: `config firewall shaping-profile` → `edit <name>` → `set type {policing|queuing}` → `set default-class-id <class-id>` → `config shaping-entries` → `edit <id>` → `set class-id <integer>` → `set priority {top|critical|high|medium|low}` → `set guaranteed-bandwidth-percentage <integer>` → `set maximum-bandwidth-percentage <integer>` → `next end next end` (เอกสาร: Traffic shaping profiles, FortiOS 7.4 Administration Guide)
- สร้าง shaping-policy: `config firewall shaping-policy` → `edit <id>` → ตั้งเงื่อนไขให้ตรง traffic (srcintf / dstintf / srcaddr / dstaddr / service) → `set class-id <integer>` → `next end` (เอกสาร: config firewall shaping-policy, FortiOS 7.4 CLI Reference)
- Apply shaping-profile ไปยัง interface: `config system interface` → `edit <name>` → `set egress-shaping-profile <profile-name>` → `set outbandwidth <kbps>` → `next end` (เอกสาร: Interface-based traffic shaping profile, FortiOS 7.4 Administration Guide)
ที่มา: Traffic shaping profiles (FortiOS 7.4 Administration Guide) https://docs.fortinet.com/document/fortigate/7.4.7/administration-guide/626246/traffic-shaping-profiles
