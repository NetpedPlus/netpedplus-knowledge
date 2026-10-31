---
id: server-add-checklist
title: Checklist เพิ่ม server ใหม่ (ToR → FortiGate → F5)
families:
triggers: add server, เพิ่ม server, onboard server, new node, server provision, เพิ่ม node
versions: FortiOS 7.4.x, BIG-IP 17.1 / 17.5, Huawei VRP V200R019 – V200R025, H3C Comware 7, Cisco IOS-XE 17.x
sources: https://support.huawei.com/enterprise/en/doc/EDOC1100463967/4c4b03b5/creating-and-configuring-an-eth-trunk-interface, https://www.h3c.com/en/d_202511/2685240_294551_0.htm, https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-7/configuration_guide/lyr2/b_177_lyr2_9300_cg/configuring_etherchannels.html, https://docs.fortinet.com/document/fortigate/7.4.2/cli-reference/227620/config-firewall-address, https://docs.fortinet.com/document/fortigate/7.4.4/cli-reference/333889629/config-firewall-policy, https://techdocs.f5.com/en-us/bigip-17-0-0/big-ip-local-traffic-manager-implementations/implementing-health-and-performance-monitoring.html, https://techdocs.f5.com/en-us/bigip-21-1-0/big-ip-local-traffic-management-basics/about-nodes.html, https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-networking-8-0/configuring-lacp-on-a-vsphere-distrubuted-switch-in-the-vsphere-web-client.html
---

# Checklist เพิ่ม server ใหม่ (ToR → FortiGate → F5)

คำค้น: เพิ่ม server, เพิ่ม server ใหม่, onboard server, new node, server provision, ToR port, LACP, port-channel, eth-trunk, bridge-aggregation, NIC teaming, ESXi, FortiGate address, F5 node, pool member, health monitor, checklist server

อาการ: ติดตั้ง server ใหม่ (bare-metal หรือ VM) ต้อง config ToR port, ผูก policy Firewall, เพิ่ม pool member ที่ F5, และตรวจว่า traffic ไป-กลับครบทุกจุด

---

## 1. ToR Port Setup / Huawei S5731 (VRP V200)

คำค้น: huawei, s5731, eth-trunk, lacp, port-channel, link aggregation, สร้าง eth-trunk
อาการ: ต้องผูก ToR port ที่ Huawei S5731 เข้ากับ server ใหม่ผ่าน LACP (Eth-Trunk)
คำสั่งตรวจ:
```
display eth-trunk <trunk-id> verbose
```
อ่านผล:
- Status ของ member port ต้องเป็น `Selected` (ไม่ใช่ `Unselected`)
- Working Mode: ต้องเป็น `LACP`
ที่มา: [Creating and Configuring an Eth-Trunk Interface (Huawei)](https://support.huawei.com/enterprise/en/doc/EDOC1100463967/4c4b03b5/creating-and-configuring-an-eth-trunk-interface)
วิธีแก้:
- สร้าง Eth-Trunk แบบ LACP: `system-view`, `interface eth-trunk <trunk-id>`, `mode lacp`, `commit`
- เพิ่ม port: `interface <port-range>`, `eth-trunk <trunk-id>`, `commit`
- ตั้ง LACP fast timeout: `interface eth-trunk <trunk-id>`, `lacp timeout fast`, `commit`

---

## 2. ToR Port Setup / H3C S6520X (Comware 7)

คำค้น: h3c, s6520x, bridge-aggregation, lacp, link aggregation, สร้าง aggregate port
อาการ: ต้องผูก ToR port ที่ H3C S6520X เข้ากับ server ใหม่ผ่าน LACP (Bridge-Aggregation)
คำสั่งตรวจ:
```
display link-aggregation verbose
```
อ่านผล:
- Aggregation Mode: `D` = Dynamic (LACP)
- Flags แสดงตัวอักษรต่อกัน เช่น `ACDEF` (A = LACP Active, C = Aggregatable, D = Synchronized, E = Collecting, F = Distributing)
- Port ที่ใช้งานได้ต้องมี Status = `S` (Selected)
ที่มา: [02-Ethernet link aggregation configuration (H3C)](https://www.h3c.com/en/d_202511/2685240_294551_0.htm)
วิธีแก้:
- สร้าง Bridge-Aggregation: `system-view`, `interface bridge-aggregation <group-id>`, `link-aggregation mode dynamic`
- เพิ่ม port: `interface <port-id>`, `port link-aggregation group <group-id>`

---

## 3. ToR Port Setup / Cisco C9300X (IOS-XE 17.x)

คำค้น: cisco, c9300x, port-channel, etherchannel, lacp, channel-group, สร้าง port-channel
อาการ: ต้องผูก ToR port ที่ Cisco C9300X เข้ากับ server ใหม่ผ่าน LACP (EtherChannel)
คำสั่งตรวจ:
```
show etherchannel summary
```
อ่านผล:
- Flag ของ port-channel ควรเป็น `(SU)` — S = Standby/Selected, U = Up
- Flag ของ port ในกลุ่ม: `P` = bundled in port-channel, `D` = down, `I` = stand-alone, `s` = suspended
- Port assigned: แสดงจำนวน port ที่รวม group แล้ว (≥2)
ที่มา: [Configuring EtherChannels — Catalyst 9300 (Cisco)](https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-7/configuration_guide/lyr2/b_177_lyr2_9300_cg/configuring_etherchannels.html)
วิธีแก้:
- สร้าง EtherChannel LACP: `configure terminal`, `interface range <range>`, `channel-group <group-number> mode active`, `end`
- `mode active` = LACP Active (เริ่ม negotiate)
- คู่ที่ถูกต้อง: active/active (ใช้ได้), active/passive (ใช้ได้), passive/passive (ไม่ขึ้น)

---

## 4. LACP vs ESXi NIC Teaming

คำค้น: esxi, vmware, nic teaming, lacp, vds, vswitch, link aggregation, virtual distributed switch
อาการ: ต้องเลือกรูปแบบ NIC teaming สำหรับ server VMware ESXi
คำสั่งตรวจ:
```
ตรวจใน GUI: vCenter > Hosts and Clusters > เลือก host > Configure > Networking > ตรวจสอบ LAG และ uplink
```
อ่านผล:
- VDS LACP: มี LAG set ไว้, uplink assign ไป LAG, physical ToR ทำ LACP port-channel คู่กัน
- Legacy Teaming: ใช้ vSS, Load balancing = Route based on source virtual port, uplink Primary/Secondary
ที่มา: [LACP Support on a vSphere Distributed Switch — Broadcom/VMware](https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-networking-8-0/configuring-lacp-on-a-vsphere-distrubuted-switch-in-the-vsphere-web-client.html)
วิธีแก้:
- (ก) VDS + LAG: ใช้ vSphere Distributed Switch (vSS ไม่รองรับ LACP), สร้าง LAG บน vDS (vCenter > Distributed Switch > Configure > LACP > New Link Aggregation Group), ตั้ง LACP mode matching กับ ToR (active/active หรือ active/passive), assign uplink ไป LAG
- (ข) vSS + ToR port ธรรมดา: ใช้ vSS + standard teaming แบบ "Route based on originating virtual port" (ไม่ทำ LACP)
- สรุป: ถ้า ToR ทำ LACP จริงและใช้ 2 uplink → ต้องใช้ VDS + LAG, ถ้าใช้ vSS ได้แค่ active/standby เท่านั้น

---

## 5. FortiGate Address Object / ตรวจว่ามีหรือยัง

คำค้น: fortigate, address object, firewall address, set subnet, สร้าง address, fortios 7.4
อาการ: ต้องตรวจว่า address object ของ server ใหม่ถูกสร้างใน FortiGate แล้วหรือยัง
คำสั่งตรวจ:
```
show firewall address "<ชื่อ>"
```
อ่านผล:
- ต้องเห็น name, subnet/IP ที่กำหนด, type, interface
- หากไม่พบ output หรือแสดง "not found" = ยังไม่ได้สร้าง address object
ที่มา: [config firewall address — FortiOS 7.4.2](https://docs.fortinet.com/document/fortigate/7.4.2/cli-reference/227620/config-firewall-address)
วิธีแก้:
- สร้าง address: `config firewall address`, `edit "SRV-<ชื่อ>_<IP>"`, `set subnet <IP>/32`, `next`, `end`
- สร้าง policy ใหม่: `config firewall policy`, `edit 0`, `set srcintf <src-interface>`, `set dstintf <dst-interface>`, `set srcaddr <src-address>`, `set dstaddr "SRV-<ชื่อ>_<IP>"`, `set action accept`, `set schedule always`, `set service <service-list>` (เฉพาะ port ที่ต้องใช้ เช่น HTTP HTTPS), `set logtraffic all`, `next`, `end`
- ระวัง: trafficขาเข้า server ปกติไม่ NAT (ถ้าเปิดจากภายนอกใช้ VIP / port forward)
- ตรวจลำดับ policy: ถ้ามี policy deny กว้างกว่าอยู่ก่อน ให้ใช้ `move <new-policy-id> before <deny-policy-id>`

---

## 6. FortiGate Firewall Policy / ตรวจว่ามีหรือยัง

คำค้น: fortigate, firewall policy, policy lookup, traffic policy, fortios 7.4
อาการ: ต้องตรวจว่า firewall policy ที่อนุญาต traffic ไป server ใหม่ถูกสร้างแล้วหรือยัง
คำสั่งตรวจ:
```
show firewall policy | grep <ชื่อ_server>
```
อ่านผล:
- ต้องเห็น policy ที่ dstaddr = ชื่อ address ของ server, action = accept
- หากไม่มี = traffic จะถูก drop โดย default deny
ที่มา: [config firewall policy — FortiOS 7.4.4](https://docs.fortinet.com/document/fortigate/7.4.4/cli-reference/333889629/config-firewall-policy)
วิธีแก้:
- ใช้ `show firewall policy` ดูลำดับ policy ทั้งหมด, ใช้ `move <id> before <id>` จัดลำดับให้ policy ใหม่อยู่ก่อน default deny
- ตรวจด้วย diagnose flow: `diagnose firewall iprope lookup <src-ip> <src-port> <dst-ip> <dst-port> <protocol> <src-intf>` (เช่น `diagnose firewall iprope lookup 10.0.0.1 12345 10.0.0.2 80 6 port1`)

---

## 7. F5 BIG-IP / Node ตรวจว่ามีหรือยัง

คำค้น: f5, big-ip, node, ltm node, ltm, สร้าง node, f5 node, bigip 17
อาการ: ต้องตรวจว่า F5 BIG-IP node ของ server ใหม่ถูกสร้างแล้วหรือยัง
คำสั่งตรวจ:
```
show ltm node <node_name>
```
อ่านผล:
- ต้องเห็น node name, address (IP)
- `list` แสดงแค่ config ไม่มี state, ต้องใช้ `show` เพื่อดู state (available/down)
- หากไม่พบ = ยังไม่ได้สร้าง node
ที่มา: [About Nodes — BIG-IP](https://techdocs.f5.com/en-us/bigip-21-1-0/big-ip-local-traffic-management-basics/about-nodes.html)
วิธีแก้:
- สร้าง node: `create ltm node <node_name> address <IP>`

---

## 8. F5 BIG-IP / Pool Member ตรวจว่ามีหรือยัง

คำค้น: f5, big-ip, pool member, pool, ltm pool, health monitor, f5 pool, bigip 17
อาการ: ต้องตรวจว่า pool member ของ server ใหม่ถูกผูกและ monitor ทำงานแล้วหรือยัง
คำสั่งตรวจ:
```
show ltm pool <pool_name> members
show ltm monitor <monitor_name>
```
อ่านผล:
- Pool members ต้องแสดง server IP:port และ state (up/down/monitoring)
- หาก status = up = server ใช้งานได้, down = health check ล้ม
- หากไม่พบ member ใน pool = ยังไม่ได้ผูก pool member
ที่มา: [Implementing Health and Performance Monitoring — BIG-IP 17.0](https://techdocs.f5.com/en-us/bigip-17-0-0/big-ip-local-traffic-manager-implementations/implementing-health-and-performance-monitoring.html)
วิธีแก้:
- สร้าง pool + member + monitor: `create ltm pool <pool_name> members add { <node_name>:<port> } monitor <monitor_name>`
- สร้าง monitor ใหม่ถ้าต้องการ: `create ltm monitor icmp <monitor_name>`
- สร้าง Virtual Server ที่ผูก pool: `create ltm virtual <vs_name> destination <VIP>:<port> pool <pool_name>`

---

## 9. ตรวจหลังติดตั้ง / สรุป

คำค้น: ตรวจหลังติดตั้ง, post-installation, verification checklist, ตรวจ server ใหม่, server check, checklist
อาการ: ต้องการรายการตรวจท้ายสุดก่อนเปิดบริการ server ใหม่
คำสั่งตรวจ:
```
display eth-trunk <trunk-id> verbose
display link-aggregation verbose
show etherchannel summary
show firewall address "<ชื่อ>"
show firewall policy | grep <ชื่อ_server>
show ltm node <node_name>
show ltm pool <pool_name> members
show ltm virtual <vs_name>
```
อ่านผล:
- ToR: ทุก member port แสดงสถานะ Selected (ไม่ใช่ Unselected)
- FortiGate: address object มีอยู่, policy ผูก dstaddr ถูก, action = accept
- F5: node มีอยู่, pool member status = up หรือ monitoring, virtual server = available
- Traffic flow: ping จาก client ไป server ผ่านได้, server ตอบกลับผ่าน F5/FortiGate กลับได้
ที่มา: https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-networking-8-0/configuring-lacp-on-a-vsphere-distrubuted-switch-in-the-vsphere-web-client.html
วิธีแก้:
- ToR LACP ไม่ขึ้น: ตรวจ mode ทั้ง 2 ฝั่ง (Huawei: mode lacp, H3C: link-aggregation mode dynamic, Cisco: mode active), ตรวจ VLAN setting ต้องตรงกัน, ESXi: ตรวจ VDS LAG mode matching กับ ToR
- F5 pool member down: ตรวจ service port เปิดจริงที่ server, ping จาก BIG-IP, ตรวจ monitor interval/timeout
- FortiGate policy ไม่จับ: ตรวจลำดับ policy, ชื่อ address ถูกต้อง, interface ผูกตรง
