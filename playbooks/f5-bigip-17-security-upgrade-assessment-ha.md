---
id: f5-bigip-17-security-upgrade-assessment-ha
title: F5 BIG-IP 17.x ประเมินผลกระทบช่องโหว่ + อัปเกรดบนคู่ HA
families: f5_tmsh
triggers: f5 bigip security upgrade, f5 advisory check affected, f5 assess impact before upgrade, f5 hotfix vs engineering hotfix, f5 ha upgrade standby first, f5 upgrade on high availability pair, f5 ucs backup qkview before upgrade, f5 rollback volume, f5 security vulnerability assessment, f5 bigip harden release, f5 bigip EHF installation, f5 tmsh provision check affected module
versions: BIG-IP 17.1 / 17.5
sources: https://my.f5.com/manage/s/article/K12201527, https://my.f5.com/manage/s/article/K51812227, https://my.f5.com/manage/s/article/K84554955, https://techdocs.f5.com/kb/en-us/products/big-ip_ltm/manuals/product/bigip-system-upgrading-software-13-0-0/1.html, https://my.f5.com/manage/s/article/K15134306, https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/sys/sys_provision.html, https://clouddocs.f5.com/products/insight/1-2-2/fleet_management/, https://techdocs.f5.com/kb/en-us/products/big-ip_ltm/releasenotes/related/relnote-supplement-bigip-17-5-1-11.html, https://clouddocs.f5.com/training/community/f5cert/html/class4/module3/lab4.html, https://my.f5.com/manage/s/article/K8665, https://my.f5.com/manage/s/article/K4423, https://my.f5.com/manage/s/article/K12878
---

# F5 BIG-IP 17.x ประเมินผลกระทบช่องโหว่ + อัปเกรดบนคู่ HA

คำค้น: f5 bigip security upgrade, f5 advisory check affected, f5 assess impact before upgrade, f5 hotfix vs engineering hotfix, f5 ha upgrade standby first, f5 upgrade on high availability pair, f5 ucs backup qkview before upgrade, f5 rollback volume, f5 security vulnerability assessment, f5 bigip harden release, f5 bigip EHF installation, f5 tmsh provision check affected module
อาการ: เมื่อมี F5 Security Advisory ออกมา ต้องประเมินว่าเครื่องอยู่ในข่ายไหม, ประเมินผลกระทบก่อน upgrade, เลือก hotfix/EHF/เวอร์ชันใหม่, และลงบนคู่ HA อย่างปลอดภัย

อ้างอิง playbook อื่น:
- `f5-bigip-17` → "ตรวจความปลอดภัยของระบบ (advisory/CVE)" สำหรับวิธีอ่าน advisory เบื้องต้น
- `f5-bigip-17` → "อัปเกรด / volume / สำรอง" สำหรับขั้นตอน upgrade แบบ单机
- `f5-ops-advanced` → HA setup, device trust, ConfigSync

---

## 1. ตรวจว่าเครื่องอยู่ในข่ายช่องโหว่ไหม

คำค้น: f5 bigip check affected vulnerability, f5 tmsh list sys provision, f5 advisory status check
อาการ: ต้องตรวจว่า BIG-IP อยู่ในข่ายช่องโหว่ที่ประกาศใน advisory หรือไม่

ตรวจใน GUI / CLI:
- **ตรวจเวอร์ชัน:** GUI → **System** → **Platform** → ดู **BIG-IP Version**
- **ตรวจ hotfix / build:** `tmsh show sys software`
- **ตรวจ module ที่ provision:** `tmsh list sys provision`
- **ตรวจ HA status:** `tmsh list / sys ha` → ดู state (Active/Standby)

อ่านผล:
- **BIG-IP Version** → ตัวอย่าง: `17.5.1.3` → ต้องดูว่าอยู่ใน "Versions known to be vulnerable" ของ advisory ไหม
- **tmsh list sys provision** → ดู module ที่เปิด: `ltm`, `asm`, `dns`, `apm`, `gtm` เป็นต้น
  - ตรวจว่า module ที่เปิดใช้ตรงกับความเสี่ยงใน advisory ไหม
  - Module ที่ไม่ได้ provision → ไม่มีผลต่อช่องโหว่นั้น
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
   - **Fixes introduced in** → เวอร์ชัน/ hotfix ที่มี patch แล้ว
3. **Affected versions** → ตรวจสอบว่าเราอยู่ช่วงไหน
   - ถ้าเวอร์ชันอยู่ในช่วง vulnerable และมี fix ใน column "Fixes introduced in" → ต้องอัป
   - ถ้า column "Fixes introduced in" เป็น "None" → ยังไม่มี patch ในรุ่นปัจจุบัน ต้องอัปเป็นรุ่นถัดไป
4. **Vulnerable component** → ดูว่า module ไหนโดน (ASM, APM, DNS, all modules)
   - ถ้า module ที่โดนยังไม่ provision → อาจไม่ต้องรีบ แต่ควรตรวจสอบอย่างละเอียด

ที่มา: [Understanding security advisory versioning (K51812227)](https://my.f5.com/manage/s/article/K51812227)

---

## 2. ประเมินผลกระทบก่อน upgrade: Release Notes Checklist

คำค้น: f5 assess impact before upgrade, f5 release notes behavior change, f5 known issues checklist
อาการ: ต้องประเมินว่า upgrade จะกระทบอะไรบ้าง ก่อนสั่งทำ

ตรวจใน GUI:
- **System → Platform** → ดู BIG-IP Version
- **System → Software Management** → ดู image list

ตรวจใน CLI:
- **ตรวจเวอร์ชันปัจจุบัน:** `tmsh show sys software`
- **ตรวจ upgrade path:** `tmsh show sys version`

ที่มา: [Overview of BIG-IP system software upgrades (K84554955)](https://my.f5.com/manage/s/article/K84554955)

วิธีดำเนินการ — ทำ checklist กรอก:

**A. Upgrade Path:**
- [ ] อ่าน "Upgrading from earlier versions" ใน release notes เวอร์ชันเป้าหมาย
- [ ] หากต้องผ่านรุ่นกลาง: ประเมินเวลาและ downtime เพิ่ม

**B. Behavior Changes:**
- [ ] อ่าน "New and Installation" → ค่า default ใหม่
- [ ] อ่าน "Issues when upgrading" → จะ overwrite setting อะไร
- [ ] ตัวอย่าง (17.5.1.11): เปลี่ยนการลงชื่อ Advanced WAF cookies → ปิด cookie violation ก่อน upgrade → เปิดหลัง 24 ชม.

**C. Known Issues:**
- [ ] อ่าน "Known Issues" → เปรียบเทียบกับ config ปัจจุบัน
- [ ] ตัวอย่าง: upgrade ช้าเมื่อมี address-lists ขนาดใหญ่

**D. สรุป:**
- [ ] **อัปได้เลย** — ไม่มี known issue ที่กระทบ
- [ ] **ต้องเตรียม** — มี behavior change ที่ต้องจัดการก่อน
- [ ] **ควรรอ** — มี critical bug ไม่มี workaround

ที่มา: [BIG-IP 17.5.1.11 Release Notes](https://techdocs.f5.com/kb/en-us/products/big-ip_ltm/releasenotes/related/relnote-supplement-bigip-17-5-1-11.html)
## 3. hotfix vs Engineering Hotfix (EHF) vs เวอร์ชันใหม่

คำค้น: f5 hotfix vs engineering hotfix, f5 EHF difference, f5 hardened release, f5 bigip software types
อาการ: เมื่อมี patch ออก ต้องเลือกว่าจะลง hotfix / EHF / เวอร์ชันใหม่ แบบไหน

ตรวจใน GUI:
- **System → Software Management** → ดู image list และ build version
- **System → Platform** → ดู platform info

ตรวจใน CLI:
- **ตรวจเวอร์ชันปัจจุบัน:** `tmsh show sys software`
- **ตรวจ hotfix ที่ลงแล้ว:** `tmsh show sys software | grep -i hotfix`
- **ตรวจเวอร์ชันปัจจุบัน:** `tmsh show sys software`
- **ตรวจ hotfix ที่ลงแล้ว:** `tmsh show sys software | grep -i hotfix`

ความแตกต่าง:
- **Maintenance/Patch Release** (เช่น 17.5.1.8 → 17.5.1.11):
  - มาเป็น ISO image เต็ม → ติดตั้งเหมือน upgrade ทั่วไป
  - รวม fix ทั้งหมดจาก hotfix/ehf ก่อนหน้า
  - เหมาะสำหรับ planned upgrade, ไม่มี pressure ว่าจะต้องเร็ว

- **F5 Hardened Releases (HR):**
  - ออกเมื่อมี security vulnerability สำคัญ
  - รวม security fixes ทั้งหมด + bug fixes ที่จำเป็น
  - ควรเลือกเป็นลำดับแรกเมื่อมี advisory เกี่ยวกับ security

- **Engineering Hotfix (EHF):**
  - เป็น patch เฉพาะกรณี → มักออกมาเร็วกว่า HR
  - ติดตั้งหลังจาก ISO image แล้ว (สองขั้นตอน: ลง ISO → แล้วลง EHF)
  - มักมีเฉพาะบางรุ่น/บาง platform
  - ขอจาก F5 Support ผ่าน case → มีชื่อ EHF เฉพาะ (เช่น `Hotfix-BIGIP-17.5.1.10.0.37.35-ENG`)
  - มี known risks — ต้องถาม F5 ว่า EHF นี้กระทบอะไรบ้าง

วิธีเลือก:
1. **Security vulnerability → มี Hardened Release?** → เลือก HR (ปลอดภัยที่สุด)
2. **ไม่มี HR แต่มี EHF สำหรับ bug นี้โดยเฉพาะ?** → เลือก EHF (เร็ว แต่ต้องตรวจ known risks)
3. **ไม่มี HR/EHF → รอ patch release ถัดไป?** → วางแผน upgrade ครั้งหน้า
4. **ตรวจว่า hotfix/HR/EHF ตัวนั้นมี fix ของ CVE นี้จริงไหม?** → ดู column "Fixes introduced in" ใน advisory

ที่มา: [Overview of BIG-IP system software upgrades (K84554955)](https://my.f5.com/manage/s/article/K84554955), [Fleet management — Engineering Hotfixes](https://clouddocs.f5.com/products/insight/1-2-2/fleet_management/)

---

## 4. ขั้นตอนลงบนคู่ HA: สำรอง → Standby → Failover → Peer

คำค้น: f5 ha upgrade standby first, f5 bigip ha upgrade procedure, f5 upgrade active standby pair, f5 configsync after upgrade, f5 force offline standby
อาการ: ต้อง upgrade BIG-IP บนคู่ HA (Active-Standby) โดยไม่ตัด traffic

ที่มา: [Overview of BIG-IP system software upgrades (K84554955)](https://my.f5.com/manage/s/article/K84554955), f5 bigip ha upgrade procedure, f5 upgrade active standby pair, f5 configsync after upgrade, f5 force offline standby
อาการ: ต้อง upgrade BIG-IP บนคู่ HA (Active-Standby) โดยไม่ตัด traffic

ตรวจใน GUI:
- **HA status:** GUI → **Device Management** → **Device Group** → ดู Active/Standby
- **ConfigSync:** GUI → **Device Management** → **Device Group** → กด **Sync Config to Peer** (หากจำเป็น)

## 4.1 ขั้นเตรียมการ (ทำบนทั้ง 2 เครื่อง)

คำค้น: f5 ha upgrade prepare, f5 ucs backup before upgrade, f5 qkview before upgrade, f5 force offline standby
อาการ: ต้องเตรียม UCS backup, qkview และตั้งค่า standby เป็น offline ก่อน upgrade

ตรวจใน GUI:
- **System → Archives** → ตรวจ backup ล่าสุด
- **Device Management → Device Group** → ตรวจ sync status
- **Device Management → Devices** → ตรวจ Active/Standby

วิธีดำเนินการ:
1. **ตรวจ HA status:** `tmsh list / sys ha` → ต้องเห็น state = Active / Standby
2. **UCS backup บนทั้ง 2 เครื่อง:**
   - **CLI:** `tmsh save sys ucs /shared/backup-before-upgrade.ucs`
   - **GUI:** **System** → **Archives** → **Add** → **Save private key** → **Finished**
   - ดาวน์โหลด UCS ไปเก็บใน remote location (ไม่ใช่บนเครื่อง BIG-IP)
3. **สร้าง qkview บนทั้ง 2 เครื่อง:**
   - **GUI:** **System** → **Support** → เลือก **QKView** → **Start** → ดาวน์โหลด
   - อัพโหลด qkview ไป F5 iHealth หากต้องการให้ F5 ช่วยตรวจ
4. **ตรวจ ConfigSync:** GUI → **Device Management** → **Device Group** → sync status = Synchronized
5. **Force Offline standby:** GUI → **Device Management** → **Devices** → เลือก standby → **Set Force Offline**

ที่มา: [Overview of BIG-IP system software upgrades (K84554955)](https://my.f5.com/manage/s/article/K84554955), [UCS archives (K4423)](https://my.f5.com/manage/s/article/K4423), [Generating qkview (K12878)](https://my.f5.com/manage/s/article/K12878)
## 4.2 ขั้นลงที่ Standby

คำค้น: f5 install software standby, f5 boot to new volume, f5 reboot after upgrade
อาการ: ต้องลง ISO/EHF ที่ standby ก่อน แล้วตรวจว่าทำงานปกติ

ตรวจใน GUI:
- **System → Software Management** → Import → Install image
- **System → Platform** → ตรวจหลัง reboot

วิธีดำเนินการ:
1. **ดาวน์โหลด ISO/EHF จาก F5:** ไปที่ [F5 Downloads](https://my.f5.com/manage/s/article/K84554955) → เลือกเวอร์ชันเป้าหมาย
2. **Upload ISO ไป standby:**
   - **GUI:** **System** → **Software Management** → **Image List** → **Import** → เลือก ISO → **Import**
3. **Install ISO บน standby:**
   - **GUI:** **System** → **Software Management** → **Image List** → เลือก image ใหม่ → **Install**
   - รอให้ติดตั้งเสร็จ (อาจใช้เวลาหลายนาที)
4. **Reboot ไป volume ใหม่:**
   - **GUI:** หลัง install เสร็จ → กด **Reboot** (หรือเลือก **Boot to Selected Location**)
5. **ตรวจหลัง reboot:**
   - เข้า GUI → **System** → **Platform** → ตรวจ **BIG-IP Version** → ต้องเป็นเวอร์ชันใหม่
   - ตรวจ log: `tail -100 /var/log/ltm` / `tail -100 /var/log/restnoded/restnoded.log` → ดู error
   - ตรวจ config: `tmsh load sys config` (หาก config ไม่โหลดอัตโนมัติ)
6. **ตรวจ device group sync:** GUI → **Device Management** → **Device Group** → ตรวจ sync status

ที่มา: [Overview of BIG-IP system software upgrades (K84554955)](https://my.f5.com/manage/s/article/K84554955)
1. **ดาวน์โหลด ISO/EHF จาก F5:** ไปที่ [F5 Downloads](https://my.f5.com/manage/s/article/K84554955) → เลือกเวอร์ชันเป้าหมาย
2. **Upload ISO ไป standby:**
   - **GUI:** **System** → **Software Management** → **Image List** → **Import** → เลือก ISO → **Import**
3. **Install ISO บน standby:**
   - **GUI:** **System** → **Software Management** → **Image List** → เลือก image ใหม่ → **Install**
   - หรือ **CLI:** `tmsh install sys software /shared/filename.iso install`
   - รอให้ติดตั้งเสร็จ (อาจใช้เวลาหลายนาที)
4. **Reboot ไป volume ใหม่:**
   - **GUI:** หลัง install เสร็จ → กด **Reboot** (หรือเลือก **Boot to Selected Location**)
   - หรือ **CLI:** `tmsh modify sys software bootable-iso /shared/filename.iso` → `reboot`
5. **ตรวจหลัง reboot:**
   - เข้า GUI → **System** → **Platform** → ตรวจ **BIG-IP Version** → ต้องเป็นเวอร์ชันใหม่
   - ตรวจ log: `tail -100 /var/log/ltm` / `tail -100 /var/log/restnoded/restnoded.log` → ดู error
   - ตรวจ config: `tmsh load sys config` (หาก config ไม่โหลดอัตโนมัติ)
6. **ตรวจว่า device group sync:** GUI → **Device Management** → **Device Group** → ตรวจ sync status

## 4.3 ขั้น Failover

คำค้น: f5 force offline active, f5 failover after upgrade, f5 traffic test after failover
อาการ: ต้อง failover traffic ไปเครื่องที่ยัง upgrade แล้ว และตรวจว่า traffic ทำงานปกติ

ตรวจใน GUI:
- **Device Management → Devices** → เลือก active device → Set Force Offline
- ตรวจ pool members และ VS status หลัง failover

วิธีดำเนินการ:
1. **Force Offline ที่ active (เครื่องเดิม):**
   - GUI → **Device Management** → **Devices** → เลือก active device → **Force Offline**
   - traffic จะ failover ไป standby (ที่ยัง upgrade แล้ว)
2. **ตรวจหลัง failover:**
   - ตรวจว่า traffic ทำงานปกติ → ping test / browser test
   - ตรวจ log บนเครื่องใหม่ (ที่ย่อหน้าเป็น active) → `/var/log/ltm`
   - ตรวจ pool members → `tmsh list ltm pool` → ดู status
   - ตรวจ config sync → GUI → **Device Management** → **Device Group** → sync status = OK

ที่มา: [Overview of BIG-IP system software upgrades (K84554955)](https://my.f5.com/manage/s/article/K84554955)
1. **Force Offline ที่ active (เครื่องเดิม):**
   - GUI → **Device Management** → **Devices** → เลือก active device (เครื่องเดิม) → **Force Offline**
   - traffic จะ failover ไป standby (ที่ยัง upgrade แล้ว)
2. **ตรวจหลัง failover:**
   - ตรวจว่า traffic ทำงานปกติ → ping test / browser test
   - ตรวจ log บนเครื่องใหม่ (ที่ย่อหน้าเป็น active) → `/var/log/ltm`
   - ตรวจ pool members → `tmsh list ltm pool` → ดู status
   - ตรวจ config sync → GUI → **Device Management** → **Device Group** → ตรวจว่า sync status = OK

## 4.4 ขั้นลงที่ Peer (เครื่องเดิม)

คำค้น: f5 upgrade second device, f5 upgrade standby after failover
อาการ: เครื่องเดิมตอนนี้กลายเป็น Standby ต้องทำขั้นตอน upgrade เช่นเดิม

ตรวจใน GUI:
- **System → Software Management** → Import → Install image (เช่นเดียวกับขั้นตอน 4.2)

วิธีดำเนินการ:
1. เครื่องเดิมตอนนี้กลายเป็น **Standby**
2. ทำขั้นตอนเดียวกับ **4.2** (upload → install → reboot) บนเครื่องนี้
3. หลัง reboot เสร็จ → ตรวจ version / log / config เช่นเดิม
4. ตรวจว่า device group sync กันแล้ว

ที่มา: [Overview of BIG-IP system software upgrades (K84554955)](https://my.f5.com/manage/s/article/K84554955)
1. เครื่องเดิมตอนนี้กลายเป็น **Standby**
2. ทำขั้นตอนเดียวกับ **4.2** (upload → install → reboot) บนเครื่องนี้
3. หลัง reboot เสร็จ → ตรวจ version / log / config เช่นเดิม
4. ตรวจว่า device group sync กันแล้ว

## 4.5 ตรวจหลัง upgrade ทั้งคู่

คำค้น: f5 post upgrade verification, f5 check after upgrade, f5 ucs backup after upgrade
อาการ: หลัง upgrade ทั้งคู่ต้องตรวจว่าทุกอย่างทำงานปกติ

ตรวจใน GUI:
- **System → Platform** → ตรวจ version
- **Device Management → Device Group** → ตรวจ sync status
- **Device Management → Devices** → ตรวจ HA state

วิธีดำเนินการ:
1. **ตรวจเวอร์ชัน:** `tmsh show sys version` — ทั้ง 2 เครื่องต้องมี version เดียวกัน
2. **ตรวจ HA status:** `tmsh list / sys ha` → ต้องเห็น state = Active / Standby
3. **ตรวจ config sync:** GUI → **Device Management** → **Device Group** → sync status = Synchronized
4. **ตรวจ traffic:** test web app / service ที่ผ่าน F5
5. **ตรวจ pool members:** `tmsh list ltm pool` → members ต้องขึ้น up
6. **ตรวจ provision:** `tmsh list sys provision` → module ที่เคย provision ต้องยังอยู่
7. **ตรวจ advanced WAF:** ต้องตั้ง resource provisioning เป็น Nominal (รอ 5 นาทีก่อนทำ config อื่น)
8. **สร้าง UCS backup ใหม่:** หลัง upgrade เสร็จ → `tmsh save sys ucs /shared/backup-after-upgrade.ucs`

ที่มา: [Overview of BIG-IP system software upgrades (K84554955)](https://my.f5.com/manage/s/article/K84554955)
1. **ตรวจเวอร์ชัน:** ทั้ง 2 เครื่องต้องมี version เดียวกัน: `tmsh show sys version`
2. **ตรวจ HA status:** `tmsh list / sys ha` → ต้องเห็น state = Active / Standby
3. **ตรวจ config sync:** GUI → **Device Management** → **Device Group** → sync status = Synchronized
4. **ตรวจ traffic:** test web app / service ที่ผ่าน F5
5. **ตรวจ pool members:** `tmsh list ltm pool` → members ต้องขึ้น up
6. **ตรวจ provision:** `tmsh list sys provision` → module ที่เคย provision ต้องยังอยู่
7. **ตรวจ ASM policy:** หากใช้ ASM → ตรวจว่า policy โหลดและทำงาน
8. **ตรวจ advanced WAF:** ต้องตั้ง resource provisioning เป็น Nominal (รอ 5 นาทีก่อนทำ config อื่น)
9. **สร้าง UCS backup ใหม่:** หลัง upgrade เสร็จ → `tmsh save sys ucs /shared/backup-after-upgrade.ucs`

---

## 5. ตรวจหลัง upgrade + วิธี rollback (boot กลับ volume เดิม)

คำค้น: f5 post upgrade check, f5 rollback bigip, f5 boot to previous volume, f5 ucs restore, f5 rollback upgrade
อาการ: หลัง upgrade ต้องตรวจว่าทุกอย่างทำงานปกติ หากมีปัญหาต้อง rollback ได้

### 5.1 Checklist หลัง upgrade

ตรวจใน GUI / CLI:
- **เวอร์ชัน:** `tmsh show sys version`
- **HA:** `tmsh list / sys ha`
- **Provision:** `tmsh list sys provision`
- **Pool members:** `tmsh list ltm pool`

 Checklist:
- [ ] เวอร์ชันตรงกันทั้ง 2 เครื่อง
- [ ] HA Active/Standby ทำงานปกติ
- [ ] ConfigSync สync config แล้ว
- [ ] Pool members ขึ้น up (ตรวจทุก pool)
- [ ] Virtual servers ทำงาน (ตรวจ VS ที่สำคัญ)
- [ ] ASM policy โหลดและทำงาน (หากใช้)
- [ ] SSL certificates ยังถูกต้อง
- [ ] SNAT / Auto SNAT ยังทำงาน
- [ ] Log ยังส่งไป syslog/FortiAnalyzer
- [ ] License ยังถูกต้อง (GUI → System → Licensing)
- [ ] ไม่พบ error ใน log (`/var/log/ltm`, `/var/log/restnoded/restnoded.log`)

### 5.2 Rollback: Boot กลับ volume เดิม

ตรวจใน GUI:
- **Boot Volume:** GUI → **System** → **Platform** → ดู **Boot Volume**

วิธี rollback:
- **GUI:**
  1. เข้า GUI ของเครื่องที่ยังเป็น standby (หรือเครื่องที่ยัง upgrade ไม่สำเร็จ)
  2. ไปที่ **System** → **Platform**
  3. ดู **Boot Volume** → จะเห็น volume เก่าและใหม่
  4. เลือก **Boot Volume** เดิม → กด **Reboot**
  5. หลัง reboot → ตรวจ version → ต้องเป็นเวอร์ชันเดิม
  6. ทำขั้นตอนเดียวกันกับอีกเครื่อง

- **CLI:**
  1. `tmsh show sys software` → ดู installed images และ boot location
  2. `tmsh modify sys software bootable-iso <volume-name>` → เลือก volume เดิม
  3. `reboot`
  4. ตรวจหลัง reboot: `tmsh show sys version`

หาก rollback ไม่ได้ (ทั้ง 2 เครื่องเป็น version ใหม่):
- **UCS Restore:** หาก upgrade แล้ว config เพี้ยน → restore UCS ที่สำรองไว้
  - **CLI:** `tmsh load sys ucs /shared/backup-before-upgrade-YYYYMMDD.ucs`
  - **GUI:** **System** → **Archives** → เลือกไฟล์ UCS → **Restore**
  - หมายเหตุ: UCS restore จะกลับไป config เดิมทั้งหมด — ต้องระวังเรื่อง version mismatch

ที่มา: [Update or upgrade BIG-IP HA systems (K15134306)](https://my.f5.com/manage/s/article/K15134306), [UCS archives (K4423)](https://my.f5.com/manage/s/article/K4423), [Overview of BIG-IP system software upgrades (K84554955)](https://my.f5.com/manage/s/article/K84554955)

---

## 6. สรุปลำดับการดำเนินการ (Quick Reference)

ตรวจใน GUI:
- **System → Platform** → ตรวจเวอร์ชัน + HA state
- **Device Management → Device Group** → ตรวจ sync status
- **Device Management → Devices** → ตรวจ Force Offline / Set Offline

วิธีดำเนินการ:
1. **ตรวจว่าเครื่องโดนช่องโหว่ไหม:** ดู version + module provision → เปรียบเทียบกับ advisory
2. **ประเมินผลกระทบ:** อ่าน release notes → ทำ checklist (upgrade path, behavior change, known issues)
3. **เลือก patch type:** HR > EHF > patch release (ตรวจว่า fix CVE นี้จริงใน advisory)
4. **เตรียมการ:** UCS backup + qkview ทั้ง 2 เครื่อง → Force Offline standby
5. **ลง standby ก่อน:** Upload ISO → Install → Reboot → ตรวจ version/log → ตรวจ sync
6. **Failover:** Force Offline active → ตรวจ traffic → ทำต่อที่ peer
7. **ลง peer:** Upload ISO → Install → Reboot → ตรวจ version/log → ตรวจ sync
8. **ตรวจหลัง upgrade:** version, HA, sync, pool, VS, ASM, log, license
9. **Backup ใหม่:** `save sys ucs` หลัง upgrade เสร็จ

ที่มา: [Overview of BIG-IP system software upgrades (K84554955)](https://my.f5.com/manage/s/article/K84554955), [Understanding security advisory versioning (K51812227)](https://my.f5.com/manage/s/article/K51812227)

---

คำค้น: f5 bigip security upgrade, f5 advisory check affected, f5 assess impact before upgrade, f5 hotfix vs engineering hotfix, f5 ha upgrade standby first, f5 upgrade on high availability pair, f5 ucs backup qkview before upgrade, f5 rollback volume, f5 security vulnerability assessment, f5 bigip hardened release, f5 bigip EHF installation, f5 tmsh provision check affected module