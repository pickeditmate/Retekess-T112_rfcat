#!/usr/bin/env python

# Control Retekess T112 / T1XX Pagers with everyone's favourite yardstick 
# Massive thanks as always to at1as for creating rfcat, Great Scott Gadgets for the Yardstick One, sub ghz for existing
#
# It turns out the retekess pagers use the EV1527 protocol, 24 bits PWM encoded
# ie: 1110 = 1, 1000 = 0.
#
# bits 14 to 23 are for the pager ID (giving space for 1023 pager addresses with only 999 being allowed.)
# 000101011101010001000000 = PID_69
# Pager addressing is done in reverse with bin 1 being 1000000000, 2 being 0100000000, 4 being 0010000000 ... you get the gist...
# Restaurant addressing is bits 1 to 13 maybe???
# 
# I am in the process of fuzzing the protocol and will update this repo with further info, hoping for an "all pagers activate" function :)
#
# 327us equates to 3060 baud so we will use that.
# Flipper is preset to 
# {CC1101_MDMCFG3, 0x32}, // Data rate is 3.79372 kBaud



import sys
import re
import struct
from rflib import *
from struct import *
import argparse
import bitstring
from bitarray import bitarray
import binascii


d = RfCat()


def ConfigureD(d):
    d.setModeIDLE()
    d.setFreq(433920000)
    d.setMdmModulation(MOD_ASK_OOK)
    d.setMdmDRate(3060)
    #d.setMaxPower()
    d.setAmpMode(1)
    d.lowball(0)


ConfigureD(d)
try:
    #d.RFxmit(b'\x88\x88\x88\x88\xee\x8e\x88\x88\x88\xe8\x88\x88\x80\x00'*10) #D020
    #d.RFxmit(b'\x88\x88\x88\x88\xee\x8e\x88\x88\x8e\xe8\x88\x88\x80\x00'*10) #D060
    #d.RFxmit(b'\x88\x88\x88\x88\xee\x8e\x88\x88\xe8\xe8\x88\x88\x80\x00'*10) #D0A0
    #d.RFxmit(b'\x8e\x88\xee\xee\x8e\xee\xee\x88\x88\x8e\x88\x88\x80\x00'*10) #4F7C10
    d.RFxmit((b'\x00\xaa\x88\x8e\x8e\x8e\xee\x8e\x8e\x88\x8e\x88\x88\x88\x88'*1))
    d.setModeIDLE()

except Exception as e:
    print ("Lost communication to USB device.. waiting 3 seconds, then retrying.")
    time.sleep(3)
    ConfigureD(d)
