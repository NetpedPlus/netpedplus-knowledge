---
id: f5-bigip-17-ltm-pool-member-status
title: F5 BIG-IP 17.x — ตรวจและแก้ไข Pool / Member Down
families: f5_tmsh
triggers: f5 show ltm pool, f5 list ltm pool, f5 show ltm node, f5 pool member user-down user-up, f5 pool member user-disabled, f5 pool member down
versions: BIG-IP 17.5.x
sources: https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/ltm/ltm_pool.html, https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/ltm/ltm_node.html
---

# KME 4.1 — Pool / Member Down

> บทเรียนจาก PR #53: quote จาก tmsh reference ต้องตรงกับ section จริง (NAME, DESCRIPTION, DISPLAY, EXAMPLES, OPTIONS) ห้ามย่อคำสั่งเอง ห้ามแต่งรูปคำสั่ง ถ้าไม่มีในหน้าให้เขียน "ไม่พบที่มา"

---

## 1. ตรวจ pool และ node status

คำค้น: f5 show ltm pool, f5 list ltm pool, f5 show ltm node, f5 list ltm node

อาการ: Pools แสดง status DOWN, pool member icon สีแดง/ดำ

คำสั่งตรวจ:
```
show pool [name] — Displays statistics and status for all Local Traffic Manager pools in the system configuration.
list pool — Displays properties of the pool named my_pool.
show node — Displays statistics and status for all nodes in the system configuration.
list node all-properties — Displays all of the properties of all of the nodes.
```

วิธีแก้: ตรวจสอบ pool members ยังทำงานอยู่

อ่านผล: ตรวจสอบ pool member status, pool state, และ node state

ที่มา: [ltm_pool.html (tmsh ref v17.0.0)](https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/ltm/ltm_pool.html), [ltm_node.html (tmsh ref v17.0.0)](https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/ltm/ltm_node.html)

อ้างอิง:
- "pool - Configures load balancing pools for the Local Traffic Manager." — tmsh reference v17.0.0 (ltm_pool.html, NAME section)
- "You can use this pool component to configure the pool definitions on the Local Traffic Manager. A load balancing pool is a logical set of devices, such as Web servers, that you group together to receive and process traffic." — tmsh reference v17.0.0 (ltm_pool.html, DESCRIPTION section)
- "show pool [name] — Displays statistics and status for all Local Traffic Manager pools in the system configuration." — tmsh reference v17.0.0 (ltm_pool.html, DISPLAY section)
- "node - Configures node addresses and services." — tmsh reference v17.0.0 (ltm_node.html, NAME section)
- "Displays information about nodes, and sets attributes of nodes and node IP addresses." — tmsh reference v17.0.0 (ltm_node.html, DESCRIPTION section)
- "show node — Displays statistics and status for all nodes in the system configuration." — tmsh reference v17.0.0 (ltm_node.html, DISPLAY section)
- "list node all-properties — Displays all of the properties of all of the nodes." — tmsh reference v17.0.0 (ltm_node.html, DISPLAY section)

หมายเหตุ: รูปที่เขียนในหน้าคือ `show pool [name]`, `show node`, `list node` (ตัด module ltm) คำสั่ง tmsh เต็มคือ `show ltm pool [name]`, `show ltm node`, `list ltm node all-properties`

---

## 2. ปิด pool member ทับ monitor (user-down)

คำค้น: f5 pool member user-down, f5 force pool member offline

อาการ: ต้องการปิด pool member โดยไม่กระทบ monitor

คำสั่งตรวจ:
```
show pool [name] — Displays statistics and status for all Local Traffic Manager pools in the system configuration.
```

วิธีแก้: `members > state > user-down` — บังคับ pool member offline ทับ monitor

อ่านผล: member จะถูกบังคับให้ออกไลน์ แม้ monitor จะ pass

ที่มา: [ltm_pool.html (tmsh ref v17.0.0)](https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/ltm/ltm_pool.html)

อ้างอิง:
- "members > state — Forces the pool member offline, overriding monitors. Affects only the pool member, not the pool itself. This property displays the monitor state when set to user-up." — tmsh reference v17.0.0 (ltm_pool.html, OPTIONS section)

คำเตือน: `user-down` บังคับ pool member offline และทับ (override) monitor results — ใช้เมื่อต้องการปิด member ชั่วคราวโดยไม่กระทบ pool configuration

หมายเหตุ: "ไม่พบที่มาของรูปคำสั่งที่ใช้เปลี่ยนค่า" — tmsh reference มีเฉพาะคำอธิบาย OPTIONS ไม่มีตัวอย่างรูปคำสั่ง modify

---

## 3. เปิด pool member หรือ node โดยผู้ใช้

คำค้น: f5 pool member user-up, f5 node user-up, f5 pool member user-disabled

อาการ: ต้องการเปิด pool member หรือ node ที่เคยปิดไว้ หรือ drain session

คำสั่งตรวจ:
```
show pool [name] — Displays statistics and status for all Local Traffic Manager pools in the system configuration.
```

วิธีแก้ที่ 1 — เปิด pool member อีกครั้ง (user-up)
`members > state > user-up` — เปิด member พร้อมแสดง monitor state

อ่านผล: member จะแสดง monitor state จริง

ที่มา: [ltm_pool.html (tmsh ref v17.0.0)](https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/ltm/ltm_pool.html)

อ้างอิง:
- "members > state — Forces the pool member offline, overriding monitors. Affects only the pool member, not the pool itself. This property displays the monitor state when set to user-up." — tmsh reference v17.0.0 (ltm_pool.html, OPTIONS section)

วิธีแก้ที่ 2 — ปิด node โดยผู้ใช้ (node user-down)
`node > state > user-down` — ปิด node ไม่รับ connection ใหม่

อ่านผล: node จะไม่รับ connection ใหม่ จนกว่าจะเปลี่ยนกลับเป็น `user-up`

ที่มา: [ltm_node.html (tmsh ref v17.0.0)](https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/ltm/ltm_node.html)

อ้างอิง:
- "node > state — Use user-down to indicate that the node may not handle any new connections. Use user-up, after using user-down, to indicate that the node may accept new connections." — tmsh reference v17.0.0 (ltm_node.html, OPTIONS section)

วิธีแก้ที่ 3 — ปิด session ของ pool member (user-disabled)
`members > session > user-disabled` — ปิดการรับ session ใหม่ (gentle drain)

อ่านผล: client ที่เคย establish session แล้วยังสร้าง connection ใหม่ได้ แต่ client ใหม่จะไม่สามารถ connect ได้ — ใช้สำหรับ drain connection ขณะ maintenance

ที่มา: [ltm_pool.html (tmsh ref v17.0.0)](https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/ltm/ltm_pool.html)

อ้างอิง:
- "members > session — Establishing a session with a pool member is establishing the ability of the client to persist to the pool member when making new connections. When a pool member is session disabled, clients that have already established sessions with the pool member may create new connections, but a client that has not already established a session may not create a new one. This feature is used to gently drain connections from a node, typically as part of a maintenance operation. The value of this property can be set by system or by user. The values which user can set for this property are user-enabled and user-disabled." — tmsh reference v17.0.0 (ltm_pool.html, OPTIONS section)
