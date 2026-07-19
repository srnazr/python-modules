*This project has been created as part of the 42 curriculum by szaarour.*

# Born2beRoot

## Table of Contents
- [Description](#description)
- [Project Description](#project-description)
- [Instructions](#instructions)
- [Script and Crontab](#script-and-crontab)
- [Connecting to the Machine](#connecting-to-the-machine)
- [Modified Files](#modified-files)
- [Defense Notes / FAQ](#defense-notes--faq)
- [Resources](#resources)

## Description

Born2beRoot is a system administration project that introduces the fundamentals of
virtualization and Linux server hardening. The goal is to set up a virtual machine
running Debian from scratch, without a graphical interface, and configure it as a
secure, minimal server: encrypted LVM partitioning, a strict password policy, a
hardened sudo configuration, an SSH service restricted to a non-default port with
root login disabled, a firewall limited to that single port, and a monitoring
script that reports the machine's status every 10 minutes via cron.

The point of the project isn't the VM itself, it's understanding every choice made
along the way well enough to explain and defend it: why LVM, why encryption, why
this partition layout, why UFW instead of iptables directly, and so on.

## Project Description

### Operating system: Debian

Debian was chosen over Rocky Linux for this project.

**Debian vs Rocky Linux**
- Debian uses `apt`/`dpkg` and a very stable, well-documented release cycle. Rocky
  Linux (a RHEL rebuild) uses `dnf`/`rpm` and leans on SELinux and firewalld by
  default, which is more complex to configure correctly for a first system
  administration project.
- Debian is explicitly recommended in the subject for people new to system
  administration, and its security stack (AppArmor, UFW) maps more directly onto
  the project's requirements.
- Rocky's advantage is that it's closer to what's used in enterprise/production
  environments (RHEL-family distros are common in corporate infrastructure), and
  SELinux's mandatory access control is stricter than AppArmor's. For a first
  project focused on learning the concepts rather than enterprise parity, Debian's
  lower setup friction made it the better choice here.

### Design choices

- **Partitioning**: manual partitioning with LVM on top of a LUKS-encrypted
  volume, so the disk layout can be split into purpose-specific logical volumes
  (see the partition table below) instead of one giant `/`.
- **Security policy**: password aging (30 day expiry, 2 day minimum between
  changes, 7 day warning), `libpam-pwquality` complexity rules, a locked-down
  sudoers file with logging, and SSH restricted to port 4242 with root login
  disabled.
- **User management**: a non-root user (`szaarour`) is created in addition to
  root, and added to both the `sudo` and `user42` groups, so day-to-day work
  happens outside the root account.
- **Services installed**: only what's strictly required — `openssh-server`,
  `ufw`, `sudo`, `libpam-pwquality`, and `cron` for the monitoring script. No
  X.org, no Wayland, no display manager.

**AppArmor vs SELinux**
Both are Mandatory Access Control (MAC) systems that restrict what a process can
do beyond standard Unix permissions, limiting damage if one application is
compromised. AppArmor (Debian's default) confines programs by file *path*, using
readable profiles that are easier to write and audit. SELinux (Rocky's default) is
more granular, it labels resources with security *contexts* and enforces policy
based on that labeling, which is more powerful but considerably harder to
configure correctly. Debian's subject requirement is simply that AppArmor is
active at startup; Rocky additionally requires SELinux enforcing mode adapted to
the project.

**UFW vs firewalld (vs iptables)**
iptables is the low-level Linux kernel firewall interface; both UFW and firewalld
are front ends that generate iptables/nftables rules so the user doesn't have to
write raw rule syntax. UFW (Debian, "Uncomplicated Firewall") favors a short,
readable command syntax (`ufw allow 4242`) and is aimed at simple, mostly static
rule sets, which fits a project that only needs one port open. firewalld (Rocky)
is built around "zones" and supports reloading rules without dropping active
connections, which is more useful on systems where the rule set changes often.
For this project's single-port requirement, UFW's simplicity was the deciding
factor.

**VirtualBox vs UTM**
VirtualBox is a full type-2 hypervisor available on Windows/Linux/Intel Mac, using
its own virtualization engine; it's what the subject asks for by default. UTM is
based on QEMU and is the practical alternative on Apple Silicon Macs, where
VirtualBox historically has weak or no support, and it can either emulate x86 or
run ARM Debian natively through Apple's Hypervisor framework. This project used
VirtualBox.

### Partitioning layout

```
NAME                MAJ:MIN RM  SIZE RO TYPE  MOUNTPOINT
sda                   8:0    0  30.8G  0 disk
├─sda1                8:1    0   500M  0 part  /boot
├─sda2                8:2    0     1K  0 part
└─sda5                8:5    0  30.3G  0 part
  └─sda5_crypt       254:0    0  30.3G  0 crypt
     ├─LVMGroup-root  254:1    0    10G  0 lvm   /
     ├─LVMGroup-swap  254:2    0   2.3G  0 lvm   [SWAP]
     ├─LVMGroup-home  254:3    0     5G  0 lvm   /home
     ├─LVMGroup-var   254:4    0     3G  0 lvm   /var
     ├─LVMGroup-srv   254:5    0     3G  0 lvm   /srv
     ├─LVMGroup-tmp   254:6    0     3G  0 lvm   /tmp
     └─LVMGroup-var-log 254:7  0     4G  0 lvm   /var/log
```

What each partition is for:

| Mount point | Purpose |
|---|---|
| `/boot` | Kernel, initrd and GRUB files needed to start the system. Kept outside the encrypted volume so the bootloader can read it *before* the LUKS passphrase is entered. |
| `/` (root LV) | Core OS: system binaries, libraries, configuration. |
| `/home` | User data. Separating it from `/` means user files survive an OS reinstall or a full root wipe. |
| swap | Overflow space when RAM is exhausted, also used for hibernation. |
| `/var` | Variable data that changes constantly (spool files, caches, package lists). Isolating it stops runaway growth here from filling up `/`. |
| `/var/log` | Log files specifically, split out from `/var` so uncontrolled log growth can't fill the rest of `/var` either. |
| `/srv` | Data served by services hosted on the machine (e.g. the WordPress files for the bonus part). |
| `/tmp` | Temporary files, cleared periodically; isolating it prevents temp-file bloat from affecting `/`. |

## Instructions

### 1. Creating the VM
- VirtualBox → New → name `szaarour42`, stored in `sgoinfre`, Debian ISO attached.
- **Base memory: 1024 MB.** This is enough because the VM never runs a graphical
  environment, only a minimal CLI stack (SSH, UFW, cron, and whatever's needed for
  the bonus). A GUI-less Debian server idles at well under this.
- 1 processor: sufficient for the workload and avoids hogging the host machine's
  resources.
- 30 GB disk: roughly the sum of every partition above, bonus layout included.

### 2. Installing Debian
- **Install** (not "Graphical Install", since no GUI is required or allowed).
- Language: English · Location: Lebanon · Locale: `en_US.UTF-8` · Keymap: American
  English.
- Hostname: `szaarour42` · Domain name: left empty.
- Root password and the `szaarour` user's password are set to a placeholder here
  and changed afterward to comply with the password policy below.

### 3. Manual partitioning
1. Select the disk (`SCSI2 (0,0,0) sda`, 32.2 GB), confirm.
2. On the free space, create `sda1`: 500 MB, primary, at the beginning, mount
   point `/boot`.
3. On the remaining free space, create `sda5`: max size, logical, **do not
   mount**. This becomes the encrypted volume.
4. **Configure encrypted volumes** → create → select `/dev/sda5` → finish →
   confirm → set the encryption passphrase.
5. **Configure the Logical Volume Manager (LVM)**: create a volume group named
   `LVMGroup` on `/dev/mapper/sda5_crypt`.
6. Inside `LVMGroup`, create the logical volumes from the table above (root,
   swap, home, var, srv, tmp, var-log), one at a time, giving each its size.
7. For each logical volume: set "Use as" to Ext4 journaling file system (the
   most common Linux filesystem) and pick its mount point. Swap uses the "swap
   area" type instead of Ext4.
8. Finish partitioning and write changes to disk.

### 4. Package manager configuration
- Scan extra installation media: No.
- Mirror country: France · mirror: `deb.debian.org` · HTTP proxy: empty.
- Participate in package usage survey: No.
- Software selection: deselect everything (no desktop environment, no standard
  system utilities beyond the base).
- Install the **GRUB bootloader**: Yes. GRUB is the small program that runs right
  after the BIOS/UEFI hands off control; its job is to find the Linux kernel on
  disk and load it into memory so the OS can actually start. Without it the
  machine wouldn't know how to boot the installed system at all. Installed to
  `/dev/sda`.

### 5. First login and sudo
- Unlock `sda5_crypt` with the encryption passphrase, log in as `szaarour`.
- `su` to root, then `apt install sudo`.
- `sudo reboot` to apply changes, log back in.
- Check the install with `sudo -V`.

`su` vs `su -`: `su` switches to the target user but keeps the *current* shell's
environment (its `PATH`, working directory, etc.), which can leave root running
with a regular user's environment. `su -` (or `su -l`) starts a clean login shell
for the target user, exactly as if they had logged in directly, with their own
environment reset from scratch. Using `su -` to become root is the safer habit.

### 6. Users and groups
```bash
sudo adduser <name>          # new user, prompts for a password too
sudo addgroup <name>         # new group
sudo adduser <user> <group>  # add a user to a group
```
Check a group exists either with `cat /etc/group` or `getent group <name>`, which
returns `groupname:x:GID:member` (`x` is the password placeholder, the number is
the GID).

`szaarour` was added to both `sudo` and `user42`, as required by the subject.

### 7. SSH
```bash
sudo apt install openssh-server
sudo service ssh status
```
In `/etc/ssh/sshd_config`: `Port 22` → `Port 4242`, `PermitRootLogin` → `no`.
In `/etc/ssh/ssh_config`: uncomment and set the client-side port to 4242 too.
```bash
sudo service ssh restart
```

**What SSH actually does**: SSH (Secure Shell) is a client-server protocol for
remote login and command execution. On first contact the client verifies the
server's host key (stored in `known_hosts` after the first connection) to make
sure it's talking to the right machine, then negotiates an encrypted channel
using asymmetric cryptography. Authentication happens over that encrypted
channel, by password or key pair, and once authenticated every command,
response, and file transfer is encrypted end-to-end, which is what makes it safe
to administer a server remotely over an untrusted network.

### 8. UFW firewall
```bash
sudo apt install ufw
sudo ufw enable
sudo ufw allow 4242
sudo ufw status
```
To add/remove rules: `sudo ufw allow <port>` to add, `sudo ufw status numbered`
to see rules with an index, `sudo ufw delete <number>` to remove one.

### 9. Sudo hardening
```bash
sudo mkdir /var/log/sudo
sudo touch /etc/sudoers.d/sudo_config
sudo nano /etc/sudoers.d/sudo_config
```
Configured in that file:
- `passwd_tries=3` — limits sudo to 3 password attempts.
- `badpass_message` — custom message shown on a wrong password.
- `logfile` — where sudo logs command executions, successes and failures.
- `log_input` / `log_output` — records everything a user types and everything
  the command outputs.
- `iolog_dir=/var/log/sudo` — where those I/O logs are stored.
- `requiretty` — sudo can only be used from an actual terminal.
- `secure_path` — overrides the user's own `PATH` when running commands through
  sudo, so a modified personal `PATH` can't be used to hijack a privileged
  command.

### 10. Password policy
`/etc/login.defs`:
- `PASS_MAX_DAYS 30` — password must be changed every 30 days.
- `PASS_MIN_DAYS 2` — minimum days between changes.
- `PASS_WARN_AGE 7` — warns the user 7 days before expiry.

```bash
sudo apt install libpam-pwquality
sudo nano /etc/pam.d/common-password
```
- `minlen=10` — minimum password length.
- `ucredit=-1` / `dcredit=-1` / `lcredit=-1` — require at least one uppercase
  letter, one digit, one lowercase letter.
- `maxrepeat=3` — no more than 3 identical consecutive characters.
- `reject_username` — password can't contain the username.
- `difok=7` — at least 7 characters must differ from the previous password
  (doesn't apply to root).
- `enforce_for_root` — applies the same policy to the root account.

After setting all of this up, every existing password (including root's) has to
be changed again so it actually complies with the new policy.

## Script and Crontab

`monitoring.sh` is a bash script that prints a system status summary, broadcast
to every open terminal on the server (`wall`) at startup and every 10 minutes:

```bash
arch=$(uname -a)
cpuf=$(grep "physical id" /proc/cpuinfo | wc -l)
cpuv=$(grep "processor" /proc/cpuinfo | wc -l)
ram_total=$(free --mega | awk '$1 == "Mem:" {print $2}')
ram_use=$(free --mega | awk '$1 == "Mem:" {print $3}')
ram_percent=$(free --mega | awk '$1 == "Mem:" {printf("%.2f"), $3/$2*100}')
disk_total=$(df -m | grep "/dev/" | grep -v "/boot" | awk '{disk_t += $2} END {printf ("%.1fGb\n"), disk_t/1024}')
disk_use=$(df -m | grep "/dev/" | grep -v "/boot" | awk '{disk_u += $3} END {print disk_u}')
disk_percent=$(df -m | grep "/dev/" | grep -v "/boot" | awk '{disk_u += $3} {disk_t += $2} END {printf("%d"), disk_u/disk_t*100}')
cpul=$(vmstat 1 2 | tail -1 | awk '{printf $15}')
cpu_op=$(expr 100 - $cpul)
cpu_fin=$(printf "%.1f" $cpu_op)
lb=$(who -b | awk '$1 == "system" {print $3 " " $4}')
lvmu=$(if [ $(lsblk | grep "lvm" | wc -l) -gt 0 ]; then echo yes; else echo no; fi)
tcpc=$(ss -ta | grep ESTAB | wc -l)
ulog=$(users | wc -w)
ip=$(hostname -I)
mac=$(ip link | grep "link/ether" | awk '{print $2}')
cmnd=$(journalctl _COMM=sudo | grep COMMAND | wc -l)
```

Line by line:
- `arch`: kernel version, OS, and architecture in one line via `uname -a`.
- `cpuf` / `cpuv`: physical and virtual (logical) CPU counts, both pulled from
  `/proc/cpuinfo` and counted with `wc -l`.
- `ram_total` / `ram_use` / `ram_percent`: `free --mega` reports memory in MB;
  `awk` pulls the total (`$2`) and used (`$3`) columns off the `Mem:` line, and
  the percentage divides used by total.
- `disk_total` / `disk_use` / `disk_percent`: `df -m` reports disk usage in MB;
  filtered to real storage devices (`grep "/dev/"`) excluding `/boot`, then
  summed with `awk`.
- `cpul` / `cpu_fin`: `vmstat 1 2` samples CPU stats twice one second apart; the
  15th column of the last line is idle time, so `100 - idle` gives active CPU
  usage.
- `lb`: `who -b` reports the last boot time; `awk` extracts just the date and
  time fields.
- `lvmu`: checks `lsblk` for any device of type `lvm` to determine whether LVM is
  active.
- `tcpc`: `ss -ta` lists TCP sockets; filtered to `ESTAB` (established)
  connections and counted.
- `ulog`: `users` lists logged-in usernames; `wc -w` counts them.
- `ip` / `mac`: `hostname -I` for the IPv4 address, `ip link` filtered to
  `link/ether` for the MAC address.
- `cmnd`: `journalctl _COMM=sudo` filters system logs to sudo's activity, and
  counting `COMMAND` lines gives the number of commands run through sudo.

### Crontab
```bash
sudo crontab -u root -e
```
```
*/10 * * * * sh /home/szaarour/monitoring.sh
```
The five fields are: minute (`0-59`), hour (`0-23`), day of month, day of week
(`0-7` or `mon`-`sun`), and then the user and command to run. `*/10` in the
minute field means "every 10 minutes".

**Interrupting the script without modifying it**: since it's triggered by cron
rather than run directly, the cleanest way to stop it without touching
`monitoring.sh` or the crontab entry is to stop the cron service itself:
```bash
sudo systemctl stop cron
```
and start it again afterward with `sudo systemctl start cron`. This pauses the
schedule entirely without editing any file the evaluator would check.

## Connecting to the Machine

```bash
ssh szaarour@127.0.0.2 -p 4242   # works
ssh root@127.0.0.2 -p 4242       # must be rejected, root login is disabled
```

**Changing passwords**:
```bash
passwd                        # change your own password
sudo passwd <user>            # change another user's password (as root/sudo)
sudo passwd root              # change the root password
sudo cryptsetup luksChangeKey /dev/sda5   # change the LUKS encryption passphrase
```

**Changing the hostname** (needed during peer review):
```bash
sudo hostnamectl set-hostname <newname>42
sudo nano /etc/hosts   # update the matching line
```
A relogin (or reboot) is needed for the new hostname to show up in the shell
prompt.

## Modified Files
- `/etc/ssh/sshd_config` — port 4242, root login disabled.
- `/etc/ssh/ssh_config` — port 4242.
- `/var/log/sudo/` — created, holds sudo's input/output logs.
- `/etc/sudoers.d/sudo_config` — sudo hardening rules.
- `/etc/login.defs` — password aging (MAX/MIN/WARN days).
- `/etc/pam.d/common-password` — password complexity rules.
- `monitoring.sh` — the monitoring script (run manually with `sh monitoring.sh`).
- `sudo crontab -u root -e` — schedules the script every 10 minutes.

## Defense Notes / FAQ

**What is LVM encryption, exactly?** LUKS encrypts the physical partition
(`/dev/sda5`) as a raw block device. Once unlocked with the passphrase at boot,
it's exposed as `/dev/mapper/sda5_crypt`, and LVM is layered *on top* of that
decrypted device. Every logical volume carved out of the volume group therefore
sits on encrypted storage, so `/`, `/home`, swap, etc. are all encrypted at rest,
and a single passphrase unlocks the whole group at once.

**apt vs aptitude**: `apt` is the modern, simplified CLI front end for `dpkg`
that Debian uses by default; it has cleaner progress output and generally good
automatic dependency resolution, but no interactive mode. `aptitude` is older and
more powerful, with both a CLI and a text-based (ncurses) interface; it resolves
complex dependency conflicts more thoroughly and distinguishes manually-installed
from automatically-installed packages more explicitly, at the cost of being
heavier and less beginner-friendly.

## Resources
- [Debian Administrator's Handbook](https://debian-handbook.info/)
- [Debian Wiki – LVM](https://wiki.debian.org/LVM)
- [ArchWiki – dm-crypt/LUKS](https://wiki.archlinux.org/title/Dm-crypt/Device_encryption) (distro-agnostic reference for how LUKS works)
- [UFW – Debian Wiki](https://wiki.debian.org/Uncomplicated%20Firewall%20%28ufw%29)
- [OpenSSH manual (`man sshd_config`)](https://man.openbsd.org/sshd_config)
- [Debian Wiki – AppArmor](https://wiki.debian.org/AppArmor)
- [crontab.guru](https://crontab.guru/) for building/checking cron schedule syntax

**AI usage**: an AI assistant (Claude) was used to reorganize my own raw setup
notes into this structured README following the subject's required format, and
to help word the conceptual explanations (partition roles, AppArmor vs SELinux,
UFW vs firewalld, SSH internals, LVM-over-LUKS, apt vs aptitude, GRUB's role,
`su` vs `su -`). The actual VM installation, partitioning, SSH/UFW/sudo
configuration, password policy, and `monitoring.sh` script were built and tested
by hand by following the subject.