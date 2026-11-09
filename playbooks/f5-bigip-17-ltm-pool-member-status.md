---
id: f5-bigip-17-ltm-pool-member-status
title: F5 BIG-IP 17.x — ตรวจและแก้ไข Pool / Member Down
families: f5_tmsh
triggers: f5 show ltm pool, f5 list ltm pool, f5 show ltm node, f5 pool member user-down user-up, f5 pool member user-disabled, f5 pool member down
versions: BIG-IP 17.5.x
sources: https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/ltm/ltm_pool.html, https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/ltm/ltm_node.html
---

# F5 BIG-IP 17.x — ตรวจและแก้ไข Pool / Member Down

---

## 1. ตรวจ pool และ node status

คำค้น: f5 show ltm pool, f5 list ltm pool, f5 show ltm node, f5 list ltm node

อาการ: ต้องการตรวจ status ของ pool และ node

คำสั่งตรวจ:
```
show ltm pool
show ltm node
list ltm node all-properties
list ltm pool
```

อ่านผล:
- `show ltm pool` — Displays statistics and status for all Local Traffic Manager pools in the system configuration.
- `show ltm node` — Displays statistics and status for all nodes in the system configuration.
- `list ltm node all-properties` — Displays all of the properties of all of the nodes.
- `list ltm pool` — แสดง properties ของ pool (รูป `list pool my_pool` ในหน้า: "Displays properties of the pool named my_pool.")

ที่มา: [ltm_pool.html (tmsh ref v17.0.0)](https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/ltm/ltm_pool.html), [ltm_node.html (tmsh ref v17.0.0)](https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/ltm/ltm_node.html)

อ้างอิง:
- "pool - Configures load balancing pools for the Local Traffic Manager." — tmsh reference v17.0.0 (ltm_pool.html, NAME section)
- "You can use this pool component to configure the pool definitions on the Local Traffic Manager. A load balancing pool is a logical set of devices, such as Web servers, that you group together to receive and process traffic." — tmsh reference v17.0.0 (ltm_pool.html, DESCRIPTION section)
- "node - Configures node addresses and services." — tmsh reference v17.0.0 (ltm_node.html, NAME section)
- "Displays information about nodes, and sets attributes of nodes and node IP addresses." — tmsh reference v17.0.0 (ltm_node.html, DESCRIPTION section)
- "show pool — Displays statistics and status for all Local Traffic Manager pools in the system configuration." — tmsh reference v17.0.0 (ltm_pool.html, EXAMPLES section)
- "show pool all-properties — Displays statistics and status for all Local Traffic Manager pools in the system configuration." — tmsh reference v17.0.0 (ltm_pool.html, EXAMPLES section)
- "list pool my_pool — Displays properties of the pool named my_pool." — tmsh reference v17.0.0 (ltm_pool.html, EXAMPLES section)
- "show node — Displays statistics and status for all nodes in the system configuration." — tmsh reference v17.0.0 (ltm_node.html, EXAMPLES section)
- "list node all-properties — Displays all of the properties of all of the nodes." — tmsh reference v17.0.0 (ltm_node.html, EXAMPLES section)

หมายเหตุ: รูปที่เขียนในหน้าคือ `show pool`, `show node`, `list node`, `list pool` (ตัด module ltm) คำสั่ง tmsh เต็มคือ `show ltm pool`, `show ltm node`, `list ltm node all-properties`, `list ltm pool`

---

## 2. pool member: state และ session

คำค้น: f5 pool member user-down user-up user-disabled, f5 pool member state session

อาการ: ต้องการควบคุม pool member state (user-down/user-up) หรือ session (user-enabled/user-disabled)

คำสั่งตรวจ:
```
show ltm pool
```

วิธีแก้ที่ 1 — ปิด pool member ทับ monitor (user-down)
`user-down` — บังคับ pool member offline, overriding monitors

อ่านผล: pool member จะถูกบังคับให้ออกไลน์

ที่มา: [ltm_pool.html (tmsh ref v17.0.0)](https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/ltm/ltm_pool.html)

อ้างอิง:
- "state — user-down forces the pool member offline, overriding monitors. user-up reverts the user-down. When user-up, this displays the monitor state." — tmsh reference v17.0.0 (ltm_pool.html, OPTIONS section)

วิธีแก้ที่ 2 — เปิด pool member อีกครั้ง (user-up)
`user-up` — เปิด pool member พร้อมแสดง monitor state

อ่านผล: pool member จะแสดง monitor state จริง

ที่มา: [ltm_pool.html (tmsh ref v17.0.0)](https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/ltm/ltm_pool.html)

อ้างอิง:
- "state — user-down forces the pool member offline, overriding monitors. user-up reverts the user-down. When user-up, this displays the monitor state." — tmsh reference v17.0.0 (ltm_pool.html, OPTIONS section)

วิธีแก้ที่ 3 — ปิด session ของ pool member (user-disabled)
`user-disabled` — ปิดการรับ session ใหม่ (gentle drain)

อ่านผล: client ที่เคย establish session แล้วยังสร้าง connection ใหม่ได้ แต่ client ใหม่จะไม่สามารถ connect ได้ — ใช้สำหรับ drain connection ขณะ maintenance

ที่มา: [ltm_pool.html (tmsh ref v17.0.0)](https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/ltm/ltm_pool.html)

อ้างอิง:
- "session — Establishing a session with a pool member is establishing the ability of the client to persist to the pool member when making new connections. When a pool member is session disabled, clients that have already established sessions with the pool member may create new connections, but a client that has not already established a session may not create a new one (or make a connection which would create a new session). This feature is used to gently drain connections from a node, typically as part of a maintenance operation. The default value is user-enabled. The value of this property can be set by system or by user. If the value is set by system, the property will not be displayed in "Edit" command. But, users can add this field in if they need to modify this property. The values which user can set for this property are user-enabled and user-disabled." — tmsh reference v17.0.0 (ltm_pool.html, OPTIONS section)

---

## 3. node state: user-down / user-up

คำค้น: f5 node user-down user-up

อาการ: ต้องการปิด node โดยผู้ใช้ ไม่รับ connection ใหม่

คำสั่งตรวจ:
```
show ltm node
```

วิธีแก้: `user-down` — ปิด node ไม่รับ connection ใหม่

อ่านผล: node จะไม่รับ connection ใหม่ จนกว่าจะเปลี่ยนกลับเป็น `user-up`

ที่มา: [ltm_node.html (tmsh ref v17.0.0)](https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/ltm/ltm_node.html)

อ้างอิง:
- "state — Specifies the current state of the node. Use user-down to indicate that the node may not handle any new connections. Use user-up, after using user-down, to indicate that the node may accept new connections." — tmsh reference v17.0.0 (ltm_node.html, OPTIONS section)

---

หมายเหตุ — ไม่พบที่มา:
- สาเหตุ pool member DOWN จาก "monitor ไม่ผ่าน" — ตรวจแล้ว: ltm_pool.html, ltm_node.html ไม่พบ quote เกี่ยวกับ monitor state ที่ทำให้ pool member DOWN (มีเฉพาะ state / session options เท่านั้น)
- "network unreachable" — ไม่พบ quote จาก ltm_pool.html, ltm_node.html
- ความหมายไอคอนสี GUI (เขียว/แดง/ดำ) — ไม่พบจาก tmsh ref (KME อ้าง techdocs 13.0/14.1 ไม่ใช่ tmsh reference)
- `show ltm monitor <name> instance` — ไม่พบใน ltm_pool.html, ltm_node.html, ltm_monitor_http.html
- `cat /var/log/ltm` — ไม่พบ quote จากหน้าใด
- "ตรวจสอบ monitor configuration" / "adjust monitor config" — ไม่พบ quote เกี่ยวกับวิธีแก้ monitor config
- "troubleshoot network" — ไม่พบ quote จากหน้าใด
- รูปคำสั่งที่ใช้เปลี่ยนค่า (modify pool members / modify node) — tmsh reference มีเฉพาะคำอธิบาย OPTIONS ไม่มีตัวอย่างรูปคำสั่ง modify
