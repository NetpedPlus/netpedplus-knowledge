---
id: f5-bigip-17-security-upgrade-assessment-ha
title: F5 BIG-IP 17.x ประเมินผลกระทบช่องโหว่ + อัปเกรดบนคู่ HA
families: f5_tmsh
triggers: f5 bigip security upgrade, f5 advisory check affected, f5 assess impact before upgrade, f5 upgrade on high availability pair, f5 ha upgrade standby first, f5 ucs backup qkview, f5 rollback upgrade volume, f5 engineering hotfix EHF, f5 tmsh failover-status, f5 force to standby upgrade
versions: BIG-IP 17.1 / 17.5
sources: https://my.f5.com/manage/s/article/K12201527, https://my.f5.com/manage/s/article/K51812227, https://my.f5.com/manage/s/article/K84554955, https://my.f5.com/manage/s/article/K15134306, https://my.f5.com/manage/s/article/K60339442, https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/sys/sys_provision.html, https://my.f5.com/manage/s/article/K13123, https://my.f5.com/manage/s/article/K55025573, https://techdocs.f5.com/en-us/bigip-17-5-1-6/big-ip-release-notes/big-ip-install.html, https://my.f5.com/manage/s/article/K08452454, https://my.f5.com/manage/s/article/K20137641, https://my.f5.com/manage/s/article/K13946, https://my.f5.com/manage/s/article/K4423, https://my.f5.com/manage/s/article/K12878, https://techdocs.f5.com/en-us/bigip-17-5-1-6/big-ip-system-essentials/software-management.html
---

# F5 BIG-IP 17.x ประเมินผลกระทบช่องโหว่ + อัปเกรดบนคู่ HA

คำค้น: f5 bigip security upgrade, f5 advisory check affected, f5 assess impact before upgrade, f5 upgrade on high availability pair, f5 ha upgrade standby first, f5 ucs backup qkview, f5 rollback upgrade volume, f5 engineering hotfix EHF, f5 tmsh failover-status, f5 force to standby upgrade
อาการ: เมื่อมี F5 Security Advisory ออกมา ต้องประเมินว่าเครื่องอยู่ในข่ายไหม, ประเมินผลกระทบก่อน upgrade, เลือก patch type, และลงบนคู่ HA อย่างปลอดภัย

อ้างอิง playbook อื่น:
- `f5-bigip-17` → "ตรวจความปลอดภัยของระบบ (advisory/CVE)" สำหรับวิธีอ่าน advisory เบื้องต้น
- `f5-bigip-17` → "อัปเกรด / volume / สำรอง" สำหรับขั้นตอน upgrade แบบเครื่องเดียว
- `f5-ops-advanced` → HA setup, device trust, ConfigSync

---

## 1. ตรวจว่าเครื่องอยู่ในข่ายช่องโหว่ไหม

คำค้น: f5 bigip check affected vulnerability, f5 tmsh list sys provision, f5 advisory status check
อาการ: ต้องตรวจว่า BIG-IP อยู่ในข่ายช่องโหว่ที่ประกาศใน advisory ไหม

ตรวจใน GUI / CLI:
- **ตรวจเวอร์ชัน:** GUI → **System** → **Platform** → ดู **BIG-IP Version**
- **ตรวจ module ที่ provision:** `tmsh list sys provision`
- **ตรวจ HA status:** `tmsh show cm failover-status`

อ่านผล:
- **BIG-IP Version** → ตัวอย่าง: `17.5.1.3` → ต้องดูว่าอยู่ใน "Versions known to be vulnerable" ของ advisory ไหม
- **tmsh list sys provision** → ดู module ที่เปิด: `ltm`, `asm`, `dns`, `apm` เป็นต้น
  - ดูว่า module มี level เป็น nominal / minimum / dedicated (ไม่ใช่ none) → module นั้น provision แล้ว
  - Module ที่ไม่ได้ provision → อาจไม่ต้องรีบตรวจช่องโหว่นั้น แต่ควรตรวจสอบอย่างละเอียด
- ต้องเปิด F5 Security Advisory → ดู **Affected products** และ **Affected versions**
  - ถ้ามี module ที่เรา provision อยู่ในรายการ affected → เครื่องอยู่ในข่าย

ที่มา: [Overview of F5 security notifications (K12201527)](https://my.f5.com/manage/s/article/K12201527), [Understanding security advisory versioning (K51812227)](https://my.f5.com/manage/s/article/K51812227), [sys provision — TMSH Reference](https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/sys/sys_provision.html)

### 1.1 วิธีอ่าน F5 Security Advisory

ตรวจใน GUI:
- เปิด [F5 Security Advisories](https://my.f5.com/manage/s/article/K12201527) → เลือก advisory ที่สนใจ

วิธีอ่าน:
1. **Evaluated products** → ดูว่ารุ่นของเราถูก F5 ตรวจแล้วหรือไม่
2. **Security Advisory Status** → ตารางแยกตาม product (BIG-IP all modules, BIG-IP ASM, BIG-IP APM ฯลฯ)
   - **Versions known to be vulnerable** → ช่วงเวอร์ชันที่โดน
   - **Fixes introduced in** → เวอร์ชัน/ hotfix ที่ patch แล้ว
3. **Affected versions** → ตรวจสอบว่าเราอยู่ช่วงไหน
   - ถ้าเวอร์ชันอยู่ในช่วง vulnerable และมี fix ใน column "Fixes introduced in" → ต้องอัป
   - ถ้า column "Fixes introduced in" เป็น "None" → ยังไม่มี patch ต้องอัปเป็นรุ่นถัดไป
4. **Vulnerable component** → ดู module ไหนโดน (ASM, APM, DNS, all modules)

ที่มา: [Understanding security advisory versioning (K51812227)](https://my.f5.com/manage/s/article/K51812227)

---

## 2. ประเมินผลกระทบก่อน upgrade: Release Notes Checklist

คำค้น: f5 assess impact before upgrade, f5 release notes behavior change, f5 known issues, f5 upgrade path
อาการ: ต้องประเมินว่า upgrade จะกระทบอะไรบ้าง ก่อนสั่งทำ

ตรวจใน GUI:
- **System → Software Management** → ตรวจ image list

ตรวจใน CLI:
- **ตรวจเวอร์ชันปัจจุบัน:** `tmsh show sys software`

ที่มา: [Overview of BIG-IP system software upgrades (K84554955)](https://my.f5.com/manage/s/article/K84554955)

วิธีดำเนินการ — ทำ checklist กรอก:

**A. Upgrade Path (ต้องผ่านรุ่นกลางไหม):**
- [ ] อ่าน "Upgrading from earlier versions" ใน release notes ของเวอร์ชันเป้าหมาย
- [ ] หากต้องผ่านรุ่นกลาง: ต้องประเมินเวลาและ downtime เพิ่ม

**B. Behavior Changes / ค่า Default ใหม่:**
- [ ] อ่าน "New and Installation" → ดูค่า default ใหม่
- [ ] อ่าน "Fixes and Known Issues" → ดูว่า upgrade จะ overwrite setting อะไร
- [ ] ตัวอย่าง (17.5.1.6): K2152397-2 — BIG-IP support for f5optics packages built after October 2025 → หากใช้ F5OS tenant ต้องตรวจ firmware ของ host ก่อน

**C. Feature ที่ถูกตัด/เปลี่ยน:**
- [ ] อ่าน "New Features" → ดูฟีเจอร์ใหม่ที่ต้องตั้งค่าเพิ่ม
- [ ] อ่านส่วนที่ระบุ deprecated features

**D. Known Issues (สำคัญมาก):**
- [ ] อ่าน "Known Issues" ใน release notes → เปรียบเทียบกับ config ปัจจุบัน
- [ ] ตัวอย่าง known issues ใน release notes ที่พบบ่อย:
  - K935769-8: Upgrading / Rebooting BIG-IP with huge address-list configuration takes a long time (workaround: แปลง address-lists เป็น subnet)

**E. สรุป:**
- [ ] **อัปได้เลย** — ไม่มี known issue ที่กระทบ, upgrade path ตรง
- [ ] **ต้องเตรียม** — มี known issue หรือ behavior change ที่ต้องจัดการก่อน upgrade
- [ ] **ควรรอ** — มี critical bug ใน known issues ที่ยังไม่มี workaround

ที่มา: [BIG-IP 17.5.1.6 Release Notes](https://techdocs.f5.com/en-us/bigip-17-5-1-6/big-ip-release-notes/big-ip-install.html), [Overview of BIG-IP system software upgrades (K84554955)](https://my.f5.com/manage/s/article/K84554955)

---

## 3. Maintenance / Point Release vs Engineering Hotfix (EHF)

คำค้น: f5 maintenance release, f5 engineering hotfix EHF, f5 EHF difference, f5 bigip software types
อาการ: เมื่อมี patch ออก ต้องเลือกว่าจะลง maintenance release / EHF แบบไหน

ตรวจใน GUI:
- **System → Software Management** → ตรวจ image list

ตรวจใน CLI:
- **ตรวจเวอร์ชันปัจจุบัน:** `tmsh show sys software`
- **ตรวจ hotfix ที่ลงแล้ว:** `tmsh show sys software | grep -i hotfix`

ความแตกต่าง:
- **Maintenance / Point Release** (เช่น 17.5.1.6 → 17.5.1.11):
  - มาเป็น ISO image เต็ม → ติดตั้งเหมือน upgrade ทั่วไป
  - รวม fix ทั้งหมดจาก hotfix ก่อนหน้า
  - ดาวน์โหลดได้ฟรีที่ [MyF5 Downloads](https://my.f5.com/manage/s/article/K84554955)
  - เหมาะสำหรับ planned upgrade

- **Engineering Hotfix (EHF):**
  - เป็น patch เพิ่มเติมจาก base ISO → ติดตั้งสองขั้นตอน (ลง ISO base → แล้วลง EHF)
  - มักมีเฉพาะบางรุ่น/บาง platform
  - ตามปกติ: ขอจาก F5 Support ผ่าน case (K13123)
  - สำหรับ CVE วิกฤต: F5 อาจระบุชื่อ EHF ใน advisory และเปิดให้ดาวน์โหลดที่ MyF5 Downloads (K13123)
  - ชื่อไฟล์: เช่น `Hotfix-BIGIP-17.5.1.10.0.7.35-ENG`

วิธีเลือก:
1. **Security vulnerability → มี Maintenance/Point release ที่ patch แล้ว?** → เลือก maintenance release
2. **ไม่มี maintenance release แต่มี EHF สำหรับ CVE นี้ใน advisory?** → เลือก EHF (ด่วนกว่า)
3. **ไม่มีทั้ง maintenance และ EHF → รอ?** → วางแผน upgrade ครั้งหน้า
4. **ตรวจว่า patch ตัวนั้น fix CVE จริงไหม?** → ดู column "Fixes introduced in" ใน advisory

ที่มา: [Managing BIG-IP product hotfixes (K13123)](https://my.f5.com/manage/s/article/K13123), [Engineering hotfix installation overview (K55025573)](https://my.f5.com/manage/s/article/K55025573)

---

## 4. ขั้นตอนลงบนคู่ HA: สำรอง → Standby → Failover → Peer

คำค้น: f5 ha upgrade standby first, f5 bigip ha upgrade procedure, f5 upgrade active standby pair, f5 configsync different version, f5 release offline, f5 force to standby upgrade
อาการ: ต้อง upgrade BIG-IP บนคู่ HA (Active-Standby) โดยไม่ตัด traffic

ตรวจใน GUI:
- **Device Management → Devices** → ตรวจ Active/Standby
- **Device Management → Device Group** → ตรวจ sync status

ที่มา: [Update or upgrade BIG-IP HA systems (K15134306)](https://my.f5.com/manage/s/article/K15134306), [HA upgrade using TMOS (K60339442)](https://my.f5.com/manage/s/article/K60339442), [Failover between different versions (K20137641)](https://my.f5.com/manage/s/article/K20137641)

## 4.1 ขั้นเตรียมการ (ทำบนทั้ง 2 เครื่อง)

คำค้น: f5 ha upgrade prepare, f5 ucs backup before upgrade, f5 qkview before upgrade
อาการ: ต้องเตรียม UCS backup, qkview และตั้งค่า standby offline ก่อน upgrade

ตรวจใน GUI:
- **System → Archives** → ตรวจว่ามี backup ล่าสุดหรือไม่
- **Device Management → Device Group** → ตรวจ sync status
- **Device Management → Devices** → ตรวจ Active/Standby

วิธีดำเนินการ:
1. **ตรวจ HA status:** `tmsh show cm failover-status` → ต้องเห็นสถานะ Active / Standby
2. **UCS backup บนทั้ง 2 เครื่อง:**
   - **CLI:** `tmsh save sys ucs /shared/backup-before-upgrade.ucs`
   - **GUI:** **System** → **Archives** → **Add** → **Save private key** → **Finished**
   - ดาวน์โหลด UCS ไปเก็บใน remote location (ไม่ใช่บนเครื่อง BIG-IP)
3. **สร้าง qkview บนทั้ง 2 เครื่อง:**
   - **GUI:** **System** → **Support** → เลือก **QKView** → **Start** → ดาวน์โหลด
   - อัพโหลด qkview ไป F5 iHealth หากต้องการให้ F5 ช่วยตรวจ
4. **Force Offline standby:** GUI → **Device Management** → **Devices** → เลือก standby → **Force Offline**
   - เพื่อป้องกัน standby กลายเป็น active ระหว่าง upgrade

ที่มา: [Overview of BIG-IP system software upgrades (K84554955)](https://my.f5.com/manage/s/article/K84554955), [UCS archives (K4423)](https://my.f5.com/manage/s/article/K4423), [Generating qkview (K12878)](https://my.f5.com/manage/s/article/K12878)

## 4.2 ขั้นลงที่ Standby

คำค้น: f5 install software standby, f5 reboot to new volume, f5 release offline standby
อาการ: ต้องลง ISO ที่ standby ก่อน แล้วตรวจว่าทำงานปกติ

ตรวจใน GUI:
- **System → Software Management → Image List** → ตรวจ image
- **System → Software Management → Boot Locations** → ตรวจหลัง reboot

ที่มา: [BIG-IP 17.5.1.6 Installation](https://techdocs.f5.com/en-us/bigip-17-5-1-6/big-ip-release-notes/big-ip-install.html), [Upgrade using TMOS (K60339442)](https://my.f5.com/manage/s/article/K60339442)

วิธีดำเนินการ:
1. **ดาวน์โหลด ISO จาก F5:** ไปที่ [MyF5 Downloads](https://my.f5.com/manage/s/article/K84554955) → เลือกเวอร์ชันเป้าหมาย
2. **Upload ISO ไป standby:**
   - **CLI:** scp ISO ไป standby → ไปที่ `/shared/images/`
   - **GUI:** **System** → **Software Management** → **Image List** → **Import** → เลือก ISO
3. **Install ISO บน standby:**
   - **GUI:** **System** → **Software Management** → **Image List** → เลือก image ใหม่ → **Install**
   - **CLI:** `tmsh install sys software image BIGIP-17.5.1.iso volume HD1.2 create-volume`
4. **Reboot ไป volume ใหม่:**
   - **CLI:** `tmsh reboot volume HD1.2`

EHF (Engineering Hotfix) — ถ้ามี hotfix เฉพาะ CVE:
- **GUI:** **System** → **Software Management** → **Hotfix List** → Import → เลือก hotfix → **Install**
- **CLI:** `tmsh install sys software hotfix Hotfix-BIGIP-17.5.1.iso volume HD1.3 create-volume`
- แล้ว reboot ไป volume ใหม่: `tmsh reboot volume HD1.3`
- แหล่ง: [K13123 Managing BIG-IP product hotfixes](https://my.f5.com/manage/s/article/K13123)

5. **ตรวจหลัง reboot:**
   - **GUI:** **System** → **Platform** → ตรวจ **BIG-IP Version**
   - ตรวจ log: `tail -100 /var/log/ltm` / `tail -100 /var/log/restnoded/restnoded.log` → ดู error
6. **สำคัญ:** ระหว่างที่สองเครื่องคนละเวอร์ชัน → **ConfigSync ไม่ทำงาน** และ **ห้าม sync / ห้ามแก้ config**
   - K20137641: "Config sync will not work if devices are in different versions"
   - K13946: "Device group members must run the same BIG-IP software version"
   - รอจนทั้ง 2 เครื่องเวอร์ชันตรงกันก่อนค่อย sync

## 4.3 ขั้น Failover: Release Offline + Force to Standby

คำค้น: f5 release offline, f5 force to standby failover, f5 failover after upgrade
อาการ: ต้อง release standby ที่ upgrade แล้ว และ force active ให้เป็น standby เพื่อ failover traffic

ตรวจใน GUI:
- **Device Management → Devices** → ตรวจสถานะ standby → ควรแสดง **Offline**
- **Device Management → Devices** → ตรวจสถานะ active → ควรแสดง **Online****

ที่มา: [Update or upgrade HA systems (K15134306)](https://my.f5.com/manage/s/article/K15134306), [Upgrade using TMOS (K60339442)](https://my.f5.com/manage/s/article/K60339442)

วิธีดำเนินการ:
1. **Release Offline standby (ที่ upgrade แล้ว):**
   - เข้า GUI ของเครื่องที่ยังไม่ได้ upgrade แล้ว (standby)
   - **Device Management** → **Devices** → เลือกเครื่อง standby → **Release Offline**
   - เครื่องจะกลับมาเป็น standby และพร้อมรับ traffic
2. **Force to Standby ที่ active:**
   - เข้า GUI ของ active machine
   - **Device Management** → **Devices** → เลือก active machine → **Force to Standby**
   - หรือ **CLI:** `tmsh run sys failover standby`
   - traffic จะ failover ไปเครื่องที่ upgrade แล้ว
3. **ตรวจหลัง failover:**
   - ตรวจว่า traffic ทำงานปกติ → ping / browser test
   - ตรวจ log → `/var/log/ltm`
   - ตรวจ pool members → `tmsh list ltm pool`

## 4.4 ขั้นลงที่ Peer (เครื่องเดิม)

คำค้น: f5 upgrade second device, f5 upgrade standby after failover
อาการ: เครื่องเดิมตอนนี้กลายเป็น Standby ต้องทำขั้นตอน upgrade เช่นเดิม

ตรวจใน GUI:
- **System → Software Management** → Import → Install (เช่นเดียวกับ 4.2)

ที่มา: [Update or upgrade HA systems (K15134306)](https://my.f5.com/manage/s/article/K15134306)

วิธีดำเนินการ:
1. เครื่องเดิมตอนนี้กลายเป็น **Standby**
2. ทำขั้นตอนเดียวกับ **4.2** (download → install → reboot) บนเครื่องนี้
3. หลัง reboot เสร็จ → ตรวจ version / log เช่นเดิม

## 4.5 ตรวจหลัง upgrade ทั้งคู่

คำค้น: f5 post upgrade verification, f5 check after upgrade, f5 ucs backup after upgrade
อาการ: หลัง upgrade ทั้งคู่ต้องตรวจว่าทุกอย่างทำงานปกติ

ตรวจใน GUI:
- **System → Platform** → ตรวจ version
- **Device Management → Device Group** → ตรวจ sync status
- **Device Management → Devices** → ตรวจ HA state

ตรวจใน CLI:
- **tmsh show cm failover-status** → ตรวจ HA state
- **tmsh show sys software** → ตรวจ version ทั้ง 2 เครื่อง

ที่มา: [Update or upgrade HA systems (K15134306)](https://my.f5.com/manage/s/article/K15134306), [Overview of BIG-IP system software upgrades (K84554955)](https://my.f5.com/manage/s/article/K84554955)

วิธีดำเนินการ:
1. **ตรวจเวอร์ชัน:** `tmsh show sys software` — ทั้ง 2 เครื่องต้องมี version เดียวกัน
2. **ตรวจ HA status:** `tmsh show cm failover-status` → ต้องเห็น state = Active / Standby
3. **ตรวจ config sync:** GUI → **Device Management** → **Device Group** → sync status = Synchronized
4. **ตรวจ traffic:** test web app / service ที่ผ่าน F5
5. **ตรวจ pool members:** `tmsh list ltm pool` → members ต้องขึ้น up
6. **ตรวจ provision:** `tmsh list sys provision` → module ที่เคย provision ต้องยังอยู่
7. **สร้าง UCS backup ใหม่:** หลัง upgrade เสร็จ → `tmsh save sys ucs /shared/backup-after-upgrade.ucs`

---

## 5. ตรวจหลัง upgrade + วิธี rollback (boot กลับ volume เดิม)

คำค้น: f5 post upgrade check, f5 rollback bigip, f5 boot to previous volume, f5 activate boot location, f5 ucs restore
อาการ: หลัง upgrade ต้องตรวจว่าทุกอย่างทำงานปกติ หากมีปัญหาต้อง rollback ได้

### 5.1 Checklist หลัง upgrade

ตรวจใน GUI:
- **System → Platform** → ตรวจ version

ตรวจใน CLI:
- **เวอร์ชัน:** `tmsh show sys software`
- **HA:** `tmsh show cm failover-status`
- **Provision:** `tmsh list sys provision`
- **Pool members:** `tmsh list ltm pool`

 Checklist:
- [ ] เวอร์ชันตรงกันทั้ง 2 เครื่อง
- [ ] HA Active/Standby ทำงานปกติ
- [ ] ConfigSync sync config แล้ว
- [ ] Pool members ขึ้น up (ตรวจทุก pool)
- [ ] Virtual servers ทำงาน (ตรวจ VS ที่สำคัญ)
- [ ] SSL certificates ยังถูกต้อง
- [ ] SNAT / Auto SNAT ยังทำงาน
- [ ] Log ยังส่งไป syslog / SIEM
- [ ] License ยังถูกต้อง (GUI → System → Licensing)
- [ ] ไม่พบ error ใน log (`/var/log/ltm`, `/var/log/restnoded/restnoded.log`)

### 5.2 Rollback: Activate Boot Location เดิม

ตรวจใน GUI / CLI:
- **Boot Locations:** GUI → **System** → **Software Management** → **Boot Locations** → ดู volume ที่มีอยู่
- **CLI:** `tmsh show sys software` → ดู installed images และ boot location

ที่มา: [Software Management (techdocs.f5.com)](https://techdocs.f5.com/en-us/bigip-17-5-1-6/big-ip-system-essentials/software-management.html), [Upgrade using TMOS (K60339442)](https://my.f5.com/manage/s/article/K60339442)

วิธี rollback:
- **GUI:**
  1. เข้า GUI → **System** → **Software Management** → **Boot Locations**
  2. เลือก volume เดิม → กด **Activate**
  3. ระบบจะ reboot กลับไป volume เดิม
- **CLI:**
  1. `tmsh show sys software` → ดู volume เดิม (เช่น HD1.1)
  2. `tmsh reboot volume HD1.1` → boot กลับ volume เดิม
  3. ตรวจหลัง reboot: `tmsh show sys software` → ต้องเป็นเวอร์ชันเดิม
- หาก upgrade แล้ว config เพี้ยน → restore UCS ที่สำรองไว้:
  - **CLI:** `tmsh load sys ucs /shared/backup-before-upgrade.ucs`
  - **GUI:** **System** → **Archives** → เลือกไฟล์ UCS → **Restore**

หมายเหตุ: UCS restore จะกลับไป config เดิมทั้งหมด — ต้องระวังเรื่อง version mismatch

---

## 6. สรุปลำดับการดำเนินการ (Quick Reference)

ตรวจใน GUI:
- **System → Platform** → ตรวจเวอร์ชัน + HA state
- **Device Management → Devices** → Force Offline / Release Offline / Force to Standby
- **Device Management → Device Group** → ตรวจ sync status

วิธีดำเนินการ:
1. **ตรวจว่าเครื่องโดนช่องโหว่ไหม:** ดู version + module provision → เปรียบเทียบกับ advisory
2. **ประเมินผลกระทบ:** อ่าน release notes → ทำ checklist (upgrade path, behavior change, known issues)
3. **เลือก patch type:** maintenance release หรือ EHF (ตรวจว่า fix CVE นี้จริงใน advisory)
4. **เตรียมการ:** UCS backup + qkview ทั้ง 2 เครื่อง → Force Offline standby
5. **ลง standby ก่อน:** Install ISO → Reboot ไป volume ใหม่ → ตรวจ version/log → **ห้าม sync config**
6. **Failover:** Release Offline standby → Force to Standby active → ตรวจ traffic
7. **ลง peer:** Install ISO → Reboot → ตรวจ version/log → ตรวจ sync
8. **ตรวจหลัง upgrade:** version, HA, sync, pool, VS, provision, license, log
9. **Backup ใหม่:** `save sys ucs` หลัง upgrade เสร็จ

ที่มา: [Overview of BIG-IP system software upgrades (K84554955)](https://my.f5.com/manage/s/article/K84554955), [Update or upgrade HA systems (K15134306)](https://my.f5.com/manage/s/article/K15134306)

---

คำค้น: f5 bigip security upgrade, f5 advisory check affected, f5 assess impact before upgrade, f5 upgrade on high availability pair, f5 ha upgrade standby first, f5 ucs backup qkview, f5 rollback upgrade volume, f5 engineering hotfix EHF, f5 tmsh failover-status, f5 force to standby upgrade
