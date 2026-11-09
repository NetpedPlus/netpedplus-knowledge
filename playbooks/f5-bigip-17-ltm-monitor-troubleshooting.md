---
id: f5-bigip-17-ltm-monitor-troubleshooting
title: F5 BIG-IP 17.x — ตรวจและแก้ Monitor ไม่ผ่าน (False Positive)
families: f5_tmsh
triggers: f5 monitor false positive, f5 pool member down but up, f5 http monitor receive string, f5 monitor logging, f5 https legacy tls
versions: BIG-IP 17.5.x
sources: https://my.f5.com/manage/s/article/K12531, https://my.f5.com/manage/s/article/K000158134, https://my.f5.com/manage/s/article/K22435108, https://my.f5.com/manage/s/article/K28103688
---

# F5 BIG-IP 17.x — ตรวจและแก้ Monitor ไม่ผ่าน (False Positive)

## 1. ตรวจ pool และ monitor status

คำค้น: f5 monitor false positive, f5 show ltm pool, f5 show ltm node

อาการ: Pool member ถูกแสดงว่า DOWN แต่จริงๆ ทำงานอยู่

คำสั่งตรวจ:
```
show ltm pool
show ltm node
list ltm monitor http
```

อ่านผล — GUI status table:

"Network map — Summary of pools, pool members, and nodes — Local Traffic > Network Map"

"Pools — Current status of pool/members — Local Traffic > Pools > Statistics"

"Pool members — Current status of pool/members — Local Traffic > Pools > Statistics"

"Nodes — Current status of nodes — Local Traffic > Nodes > Statistics"

อ่านผล — /var/log/ltm:

"monitor status down"

"monitor status up"

อ่านผล — interval/timeout:

"F5 recommends that in most cases the timeout value should be equal to three times the interval value, plus one. For example, the default timeout/interval ratio is 5/16 (three times 5 plus one equals 16). This setting prevents the monitor from marking the node as down before sending the last check."

ที่มา: https://my.f5.com/manage/s/article/K12531 (Identifying a failing health monitor, Logs, Verifying monitor settings)

อ้างอิง:

- "A monitor is a BIG-IP feature that verifies connections to pool members or nodes. A health monitor is designed to report the status of a pool, pool member, or node on an ongoing basis, at a set interval." — K12531, Issue section

- "Displays statistics and status for all Local Traffic Manager pools in the system configuration." — tmsh reference v17.0.0 (ltm_pool.html, EXAMPLES section)

- "Displays statistics and status for all nodes in the system configuration." — tmsh reference v17.0.0 (ltm_node.html, EXAMPLES section)

- "Displays the properties of all of the HTTP monitors." — tmsh reference v17.0.0 (ltm_monitor_http.html, EXAMPLES section)

- "F5 recommends that in most cases the timeout value should be equal to three times the interval value, plus one. For example, the default timeout/interval ratio is 5/16 (three times 5 plus one equals 16). This setting prevents the monitor from marking the node as down before sending the last check." — K12531, Verifying monitor settings section

หมายเหตุ: รูปที่เขียนในหน้าคือ `show pool`, `show node` (ตัด module ltm) คำสั่ง tmsh เต็มคือ `show ltm pool`, `show ltm node`

---

## 2. HTTP/HTTPS: Send/Receive String ผิด

คำค้น: f5 http monitor send receive string, f5 http monitor false negative, f5 default http monitor

อาการ: Pool members configured with HTTP/HTTPS health monitors are unexpectedly marked down or are not being marked down when it should be

คำสั่งตรวจ:
```
list ltm monitor http
```

วิธีแก้:

"review and update HTTP or HTTPS monitor configurations to ensure both Send and Receive Strings are properly set to match expected application responses."

"creating a custom HTTP or HTTPS monitor with the proper Send and Receive String is needed."

อ่านผล — TCP vs HTTP monitor:

"A TCP monitor is a connectivity check that occurs before any data is exchanged. The HTTP/HTTPS monitor is a check for the ability to exchange data after the connectivity has been established."

อ่านผล — default monitors:

"Without a Receive String the BIG-IP has no way to know what a proper Layer 7 response is and thus will assume that any Layer 7 response is valid and mark the pool member as available."

ที่มา: https://my.f5.com/manage/s/article/K000158134

อ้างอิง:

- "Pool members configured with HTTP/HTTPS health monitors are unexpectedly marked down or are not being marked down when it should be." — K000158134, Description section

- "The absence of the Receive String." — K000158134, Cause section

- "The Receive String presented by the pool member does not match what is configured in the monitor." — K000158134, Cause section

- "Using the default Http or Https monitors." — K000158134, Cause section

- "review and update HTTP or HTTPS monitor configurations to ensure both Send and Receive Strings are properly set to match expected application responses." — K000158134, Recommended Actions section

- "creating a custom HTTP or HTTPS monitor with the proper Send and Receive String is needed." — K000158134, Recommended Actions section

- "A TCP monitor is a connectivity check that occurs before any data is exchanged. The HTTP/HTTPS monitor is a check for the ability to exchange data after the connectivity has been established." — K000158134, Recommended Actions section

- "Without a Receive String the BIG-IP has no way to know what a proper Layer 7 response is and thus will assume that any Layer 7 response is valid and mark the pool member as available." — K000158134, Recommended Actions section

---

## 3. Monitor Logging + FQDN

คำค้น: f5 monitor logging, f5 monitor logging fqdn

อาการ: ต้องการตรวจ verbose log ของ monitor สำหรับแต่ละ pool member

คำสั่งตรวจ:
```
show ltm pool
```

วิธีแก้ — เปิด Monitor Logging (pool member):

1. Log in to the Configuration utility.
2. Go to Local Traffic > Pools > Pool List.
3. Select the name of the pool that contains the pool member for which you want to enable monitor logging.
4. Select the Members tab.
5. In the Current Members, select the Member name of the pool member for which you want to enable monitor logging.
6. For Monitor Logging, select the Enable check box.
7. Select Update.

วิธีแก้ — เปิด Monitor Logging (node):

1. Log in to the Configuration utility.
2. Go to Local Traffic > Nodes > Node List.
3. Select the name of the node for which you want to enable monitor logging.
4. For Monitor Logging, select the Enable check box.
5. Select Update.

Impact of procedure:

"The /var/log directory may become full if you leave monitor logging enabled for a long period of time. Be sure to disable monitor logging after troubleshooting."

อ่านผล — Monitor Logging log:

"The BIG-IP system stores the log of the respective pool member or node in the /var/log/monitors/ directory."

หมายเหตุ — FQDN:

"It is very important to note here that Monitor Logging will not work on FQDN pool members. The BIG-IP device does not allow modifications made to the individual FQDN ephemeral pool member, you can only make changes to the parent FQDN pool member."

ที่มา: https://my.f5.com/manage/s/article/K12531 (Monitor logging), https://my.f5.com/manage/s/article/K000158134

อ้างอิง:

- "In BIG-IP 11.5.0 and later, the Monitor Logging option is available to allow the system to log more verbose messages for each pool member and node level." — K12531, Monitor logging section

- "The /var/log directory may become full if you leave monitor logging enabled for a long period of time. Be sure to disable monitor logging after troubleshooting." — K12531, Monitor logging section

- "It is very important to note here that Monitor Logging will not work on FQDN pool members. The BIG-IP device does not allow modifications made to the individual FQDN ephemeral pool member, you can only make changes to the parent FQDN pool member." — K000158134, Recommended Actions section

---

## 4. Active Connections เมื่อ pool member ถูก monitor mark down

คำค้น: f5 active connections pool member down, f5 monitor offline active connections

อาการ: ต้องการทราบผลต่อ active connections เมื่อ pool member ถูก monitor mark down

คำสั่งตรวจ:
```
show ltm pool
```

อ่านผล — Active connections:

"Existing active connections that were already established with that pool member before it was marked offline will continue to function normally. The system will allow these active connections to complete their transactions or sessions without interruption."

ที่มา: https://my.f5.com/manage/s/article/K28103688

อ้างอิง:

- "Existing active connections that were already established with that pool member before it was marked offline will continue to function normally. The system will allow these active connections to complete their transactions or sessions without interruption." — K28103688, Description section

---

## 5. HTTPS Legacy TLS Fallback

คำค้น: f5 https monitor tls fallback, f5 monitor legacy mode, f5 monitor tls v1

อาการ:

"HTTPS monitors to mark a TLS v1.2-configured pool member down and never mark it back up again, even if the pool member is up."

"After the handshake fails for some reason, the monitor falls back to TLS v1.1 or TLS v1 by triggering the legacy mode."

คำสั่งตรวจ:
```
show ltm pool
```

วิธีแก้:

"As a workaround to restore the state of the member, remove it, and add it back to the pool."

ที่มา: https://my.f5.com/manage/s/article/K22435108

อ้างอิง:

- "HTTPS monitors to mark a TLS v1.2-configured pool member down and never mark it back up again, even if the pool member is up." — K22435108, Symptoms section

- "After the handshake fails for some reason, the monitor falls back to TLS v1.1 or TLS v1 by triggering the legacy mode." — K22435108, Symptoms section

- "The server does not send an SSL alert message, the server just sent a Reset packet instead after the client hello. By design, the system expects a TLS layer response to versions with the wrong request. But there is no SSL alert from the server, so it just can stay in fallback mode using TLS1.0." — K22435108, Cause section

- "As a workaround to restore the state of the member, remove it, and add it back to the pool." — K22435108, Recommended Actions section

---

หมายเหตุ — ไม่พบที่มา:

- สาเหตุ network latency — KME 4.2 อ้างแต่ไม่มีที่มาใน 4 บทความ
- การเปลี่ยน monitor type — KME 4.2 อ้างแต่ไม่มีที่มาใน 4 บทความ
- ขั้นตอน tcpdump เต็ม — ใช้เฉพาะที่ quote ได้ (K12531 มีขั้นตอนและ Impact แต่ไม่มีคำสั่งตัวอย่างในบล็อก)
- อาการ/สาเหตุ monitor ไม่ผ่านอื่นนอกเหนือจากที่ 4 บทความระบุ
