import requests


class WzPilot:
    def __init__(self, wzstring):
        ws = wzstring.split(":")
        (self.callsign, self.vid, self.name, self.type, self.dummy1,
         self.latitude, self.longitude, self.altitude, self.groundspeed,
         self.fpl_aircraft, self.fpl_speed, self.departure, self.fpl_fl,
         self.destination, self.server, self.proto, self.dummyrating,
         self.squawk, self.facility, self.range, self.fpl_seq,
         self.fpl_rules, self.dep_time, self.actual_deptime, self.eeth,
         self.eetm, self.enduranceh, self.endurancem, self.alt1, self.remarks,
         self.route, self.dummy2, self.dummy3, self.atis, self.atistime,
         self.dummy4, self.dummy5, self.sessiontime, self.software,
         self.software_version, self.adm_version, self.rating, self.sec_alt,
         self.flight_type, self.pob, self.heading, self.onground, self.simulator, self.mtl) = ws

    def all_data(self):
        return self.__dict__


class WhazzupParser:
    def __init__(self, config):
        self.raw_whazzupdata = ""
        self.config = config

    @staticmethod
    def get_wz():
        data = requests.get("https://api.ivao.aero/getdata/whazzup").text.split("\n")[8:]
        return [i for i in data if ":" in i and i.split(":")[3] == "PILOT"]

    def get_pilots(self):
        wz = [WzPilot(p) for p in self.get_wz()]
        return [pilot for pilot in wz if pilot.callsign.startswith(self.config['airline']['callsign_prefix'])]
