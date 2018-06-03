import struct
import sys
import datetime

class Buffer:
  """Byte array which types can be pulled from"""
  def __init__(self, data):
    self._data = data
    self._ptr  = 0
  
  def __del__(self):
    # Check that all data has been consumed
    assert self._ptr == len(self._data)

  def _get_bytes(self, ln):
    ptr = self._ptr
    self._ptr += ln
    assert self._ptr <= len(self._data)
    return self._data[ptr:self._ptr]

  def get_uint32(self):
    return struct.unpack("<L", self._get_bytes(4))[0]

  def get_int32(self):
    return struct.unpack("<l", self._get_bytes(4))[0]

  def get_float32(self):
    return struct.unpack("<f", self._get_bytes(4))[0]

  def get_str(self):
    ln = self.get_uint32()
    return self._get_bytes(ln).decode('ascii')

  def get_date(self):
    return datetime.date(self.get_uint32(), self.get_uint32(), self.get_uint32())

  def get_time(self):
    return datetime.time(self.get_uint32(), self.get_uint32(), self.get_uint32())

  def get_coord(self):
    return (self.get_float32(), self.get_float32(), self.get_float32())

with open(sys.argv[1], "rb") as f:
  while True:
    data = f.read(7)
    if not data:
      break

    (time, atype, size) = struct.unpack("<LBH", data)

    buf = Buffer(f.read(size))
    if atype == 0:
      # MissionStart
      gdate  = buf.get_date()
      gtime  = buf.get_time()
      mfile  = buf.get_str()
      mid    = buf.get_str()
      gtype  = buf.get_int32()
      cntrs  = buf.get_str()
      setts  = buf.get_str()
      mods   = buf.get_int32()
      preset = buf.get_int32()
      aqmid  = buf.get_int32()
      rounds = buf.get_int32()
      points = buf.get_int32()
      print("T:%d AType:%d GDate:%d.%d.%d GTime:%d:%d:%d MFile:%s MID:%s GType:%d CNTRS:%s SETTS:%s MODS:%d PRESET:%d AQMID:%d ROUNDS: %d POINTS: %d" %
            (time, atype, gdate.year, gdate.month, gdate.day, gtime.hour, gtime.minute, gtime.second, mfile, mid, gtype, cntrs, setts, mods, preset, aqmid, rounds, points))
    elif atype == 1:
      # Hit
      ammo = buf.get_str()
      aid  = buf.get_int32()
      tid  = buf.get_int32()
      print("T:%d AType:%d AMMO:%s AID:%d TID:%d" % (time, atype, ammo, aid, tid))
    elif atype == 2:
      # Damage
      dmg = buf.get_float32()
      aid = buf.get_int32()
      tid = buf.get_int32()
      pos = buf.get_coord()
      print("T:%d AType:%d DMG:%.3f AID:%d TID:%d POS(%.3f,%.3f,%.3f)" % (time, atype, dmg, aid, tid, pos[0], pos[1], pos[2]))
    elif atype == 3:
      # Kill
      aid = buf.get_int32()
      tid = buf.get_int32()
      pos = buf.get_coord()
      print("T:%d AType:%d AID:%d TID:%d POS(%.3f,%.3f,%.3f)" % (time, atype, aid, tid, pos[0], pos[1], pos[2]))
    elif atype == 4:
      # PlayerMissionEnd
      plid = buf.get_int32()
      pid  = buf.get_int32()
      bul  = buf.get_int32()
      sh   = buf.get_int32()
      bomb = buf.get_int32()
      rct  = buf.get_int32()
      pos  = buf.get_coord()
      print("T:%d AType:%d PLID:%d PID:%d BUL:%d SH:%d BOMB:%d RCT:%d (%.3f,%.3f,%.3f)" %
            (time, atype, plid, pid, bul, sh, bomb, rct, pos[0], pos[1], pos[2]))
    elif atype == 5:
      # TakeOff
      pid = buf.get_int32()
      pos = buf.get_coord()
      print("T:%d AType:%d PID:%d POS(%.3f, %.3f, %.3f)" % (time, atype, pid, pos[0], pos[1], pos[2]))
    elif atype == 6:
      # Landing
      pid = buf.get_int32()
      pos = buf.get_coord()
      print("T:%d AType:%d PID:%d POS(%.3f, %.3f, %.3f)" % (time, atype, pid, pos[0], pos[1], pos[2]))
    elif atype == 7:
      # MissionEnd
      print("T:%d AType:%d " % (time, atype))
    elif atype == 8:
      # MissionObjective
      objid  = buf.get_int32()
      pos    = buf.get_coord()
      coal   = buf.get_int32()
      otype  = buf.get_int32()
      res    = buf.get_int32()
      ictype = buf.get_int32()
      print("T:%d AType:%d OBJID:%d POS(%.3f,%.3f,%.3f) COAL:%d TYPE:%d RES:%d ICTYPE:%d" % (time, atype, objid, pos[0], pos[1], pos[2], coal, otype, res, ictype))
    elif atype == 9:
      # AirfieldInfo
      aid     = buf.get_int32()
      country = buf.get_str()
      pos     = buf.get_coord()
      ids     = buf.get_str()
      print("T:%d AType:%d AID:%d COUNTRY:%s POS(%.3f, %.3f, %.3f) IDS(%s)" % (time, atype, aid, country, pos[0], pos[1], pos[2], ids))
    elif atype == 10:
      # PlayerPlane
      plid     = buf.get_int32()
      pid      = buf.get_int32()
      bul      = buf.get_int32()
      sh       = buf.get_int32()
      bomb     = buf.get_int32()
      rct      = buf.get_int32()
      pos      = buf.get_coord()
      ids      = buf.get_str()
      login    = buf.get_str()
      name     = buf.get_str()
      ptype    = buf.get_str()
      country  = buf.get_str()
      form     = buf.get_int32()
      field    = buf.get_int32()
      inair    = buf.get_int32()
      parent   = buf.get_int32()
      ispl     = buf.get_int32()
      iststart = buf.get_int32()
      payload  = buf.get_int32()
      fuel     = buf.get_float32()
      skin     = buf.get_str()
      wm       = buf.get_int32()
      print("T:%d AType:%d PLID:%d PID:%d BUL:%d SH:%d BOMB:%d RCT:%d (%.3f,%.3f,%.3f) IDS:%s LOGIN:%s NAME:%s TYPE:%s COUNTRY:%s FORM:%d FIELD:%d INAIR:%d PARENT:%d ISPL:%d ISTSTART:%d PAYLOAD:%d FUEL:%.3f SKIN:%s WM:%d " %
            (time, atype, plid, pid, bul, sh, bomb, rct, pos[0], pos[1], pos[2], ids, login, name, ptype, country, form, field, inair, parent, ispl, iststart, payload, fuel, skin, wm))
    elif atype == 11:
      # GroupInit
      gid = buf.get_int32()
      ids = buf.get_str()
      lid = buf.get_int32()
      print("T:%d AType:%d GID:%d IDS:%s LID:%d" % (time, atype, gid, ids, lid))
    elif atype == 12:
      # ObjectSpawned
      oid     = buf.get_int32()
      otype   = buf.get_str()
      country = buf.get_str()
      name    = buf.get_str()
      pid     = buf.get_int32()
      pos     = buf.get_coord()
      print("T:%d AType:%d ID:%d TYPE:%s COUNTRY:%s NAME:%s PID:%d POS(%.3f,%.3f,%.3f)" % (time, atype, oid, otype, country, name, pid, pos[0], pos[1], pos[2]))
    elif atype == 15:
      # LogVersion
      ver = buf.get_uint32()
      assert ver == 17
      print("T:%d AType:%d VER:%d" % (time, atype, ver))
    elif atype == 16:
      # BotUninit
      botid    = buf.get_int32()
      pos      = buf.get_coord()
      print("T:%d AType:%d BOTID:%d POS(%.3f,%.3f,%.3f)" % (time, atype, botid, pos[0], pos[1], pos[2]))
    elif atype == 18:
      # BotEjectLeave
      botid    = buf.get_int32()
      parentid = buf.get_int32()
      pos      = buf.get_coord()
      print("T:%d AType:%d BOTID:%d PARENTID:%d POS(%.3f,%.3f,%.3f)" % (time, atype, botid, parentid, pos[0], pos[1], pos[2]))
    elif atype == 20:
      # Join
      userid     = buf.get_str()
      usernickid = buf.get_str()
      print("T:%d AType:%d USERID:%s USERNICKID:%s" % (time, atype, userid, usernickid))
    else:
      # Dump remaining data
      buf._get_bytes(size)
      raise Warning("Unknown AType %d encountered" % (atype))

    # Record always ends with 0x0A
    assert f.read(1) == b'\n'
    

