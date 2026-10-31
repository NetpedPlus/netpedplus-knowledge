---
id: huawei-acl-traffic-filter
title: Huawei S12700E / S5731 ACL / traffic-filter (traffic ถูกบล็อก)
families: huawei_vrp_s
triggers: huawei acl, traffic-filter, display acl, s12700e, s5731
vendor: Huawei
versions: VRP V200R019C00 ขึ้นไป (S12700, S12700E, S5731, S5735)
sources: https://support.huawei.com/enterprise/doc/EDOC1100213165/configuring-acl-based-packet-filtering
---
# Huawei S12700E / S5731 ACL / traffic-filter (traffic ถูกบล็อก)

## ACL / traffic-filter | ตรวจว่า traffic ถูกบล็อกโดย ACL rule ไหน
คำค้น: acl rule match, acl match counter, acl rule hit, traffic blocked by acl, acl permit deny, traffic-filter check, display acl, acl hit counter, acl match order, acl 2001, acl 3000, acl 4000, acl number range
อาการ: traffic ไม่ผ่าน — ไม่แน่ใจว่า rule ไหน match, ต้องการดูว่า acl rule ไหน match traffic, traffic ถูกบล็อกโดยรู้ตัว, traffic-filter config แล้ว traffic ไม่ผ่าน, ต้องการดู match counter ของ acl rule
คำสั่งตรวจ:
```
display acl all
display acl name <acl-name>
display traffic-filter applied-record
display traffic-filter statistics interface <interface> inbound
```
อ่านผล:
- `display acl all`: ดู acl ทุกตัว — จำนวน rule, rule ID, match-counter, time-range (Active/Inactive)
- `display acl name <acl-name>`: ดู acl เฉพาะตัว — rule ID, source/destination IP, permit/deny, match-counter
- `display traffic-filter applied-record`: ดูว่า ACL ไหนถูก apply ที่ interface / VLAN ไหน ทิศทางไหน
- `display traffic-filter statistics interface <interface> inbound`: ดูจำนวน packet ที่ match / ถูก deny ของ traffic-filter บน interface นั้น (outbound ใช้ outbound)
สาเหตุที่พบบ่อย:
1. ACL rule 5 deny ip source/destination — traffic ตรงกับ condition แล้วถูก deny
2. ACL rule มี time-range ที่ active/ inactive — traffic ถูกบล็อกเฉพาะเวลา
3. ACL rule match-order auto — rule ไหน match ก่อน จะถูกใช้ก่อน
4. traffic-filter ยังไม่ได้ apply ไปยัง interface ที่ต้องการ
วิธีแก้:
- แก้ ACL rule: `acl 3000` → `rule 5 permit ip source 10.0.0.0 0.0.0.255` → `quit` (เอกสาร: Configuring ACL-based Packet Filtering, Huawei S12700 Configuration Guide V200)
- ลำดับการ match ของ rule: `acl number 3000 match-order { config | auto }` (config = ตามเลข rule, auto = เฉพาะเจาะจงก่อน; ตั้งได้ตอนสร้าง ACL) (เอกสาร: Configuring ACL-based Packet Filtering, Huawei S12700 Configuration Guide V200)
- ลบ rule: `acl 3000` → `undo rule 5` → `quit` (เอกสาร: Configuring ACL-based Packet Filtering, Huawei S12700 Configuration Guide V200)
- ตรวจสอบ traffic-filter: `display traffic-filter statistics interface <interface> inbound` (เอกสาร: Configuring ACL-based Packet Filtering, Huawei S12700 Configuration Guide V200)
ที่มา: Configuring ACL-based Packet Filtering (Huawei S12700 Configuration Guide V200) https://support.huawei.com/enterprise/doc/EDOC1100213165/configuring-acl-based-packet-filtering

## ACL / traffic-filter | สร้าง ACL และ apply traffic-filter บน interface
คำค้น: acl configuration, traffic-filter apply, acl create, acl 3000, acl permit, acl deny, acl rule, traffic-filter interface, acl 2001, acl 3000, acl 4000, acl number, acl number 2001, acl number 3000, acl number 4000, acl 6000
อาการ: ต้องการสร้าง ACL ใหม่, traffic ต้องถูก filter, ต้องการให้ interface filter traffic, traffic-filter config แล้ว traffic ไม่ผ่าน, traffic ถูกบล็อกโดยรู้ตัว
คำสั่งตรวจ:
```
display acl all
display traffic-filter applied-record
display traffic-filter statistics interface <interface> inbound
```
อ่านผล:
- `display acl all`: ดู acl ทุกตัว — จำนวน rule, rule ID, source/destination IP, permit/deny, match-counter
- `display traffic-filter applied-record`: ดูว่า ACL ไหนถูก apply ที่ interface / VLAN ไหน ทิศทางไหน
- `display traffic-filter statistics interface <interface> inbound`: ดูจำนวน packet ที่ match / ถูก deny ของ traffic-filter บน interface นั้น (outbound ใช้ outbound)
- acl number range (IPv4):
  - 2000-2999: Basic ACL (source IP only)
  - 3000-3031: Advanced ACL (source+destination IP+port)
  - 6000-6031: User-defined ACL
  - 4000-4031: Layer 2 ACL
วิธีแก้:
- สร้าง basic ACL: `acl number 2001` → `rule 5 permit source 10.0.0.0 0.0.0.255` → `quit` (เอกสาร: Configuring ACL-based Packet Filtering, Huawei S12700 Configuration Guide V200)
- สร้าง advanced ACL: `acl 3000` → `rule 5 permit ip source 10.0.0.0 0.0.0.255 destination 10.0.0.0 0.0.0.255` → `quit` (เอกสาร: Configuring ACL-based Packet Filtering, Huawei S12700 Configuration Guide V200)
- Apply traffic-filter: `interface gigabitethernet 1/0/1` → `traffic-filter inbound acl 3000` → `quit` (เอกสาร: Configuring ACL-based Packet Filtering, Huawei S12700 Configuration Guide V200)
- Apply traffic-filter outbound: `interface gigabitethernet 1/0/1` → `traffic-filter outbound acl 3000` → `quit` (เอกสาร: Configuring ACL-based Packet Filtering, Huawei S12700 Configuration Guide V200)
- ลบ traffic-filter: `interface gigabitethernet 1/0/1` → `undo traffic-filter inbound acl 3000` → `quit` (เอกสาร: Configuring ACL-based Packet Filtering, Huawei S12700 Configuration Guide V200)
ที่มา: Configuring ACL-based Packet Filtering (Huawei S12700 Configuration Guide V200) https://support.huawei.com/enterprise/doc/EDOC1100213165/configuring-acl-based-packet-filtering
