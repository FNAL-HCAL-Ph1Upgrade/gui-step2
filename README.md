#  gui-step2
## GUI for Teststand 2

HCAL Phase 1 upgrade: HB QIE card testing at FNAL, summer 2018.

The HB_Master branch diverges from HE_Master. The HE_Master branch used an ngCCM emulator. A server running on a Raspberry Pi was used for communiating with the ngCCM emulator and QIE cards. For HB_Master we will use a production ngCCM and a development ngccm server (developed by Alan James Campbell, alan.campbell@desy.de and alan.james.campbell@cern.ch).


* Register tests: test all Bridge, Igloo, QIE, and vTTx registers for each QIE card, all communication with ngccm server logged
* Quality Control: data taken with run contorl using sequencer, different scans (phase, charge injection, shunt)
