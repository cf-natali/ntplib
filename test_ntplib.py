"""Python NTP library tests."""


import datetime
import socket
import time
import unittest

import ntplib


class TestNTPLib(unittest.TestCase):
    """ Main test. """

    NTP_SERVER = "pool.ntp.org"
    """test NTP server"""

    POLL_DELAY = 1
    """delay between NTP polls, in seconds"""

    DELTA_TOLERANCE = 0.5
    """tolerance for offset/delay comparisons, in seconds"""

    def test_basic(self):
        """Basic tests."""
        self.assertTrue(issubclass(ntplib.NTPException, Exception))

        ntplib.NTPClient()

    def test_request(self):
        """Request tests."""
        client = ntplib.NTPClient()

        t_1 = time.time()
        info = client.request(self.NTP_SERVER)
        t_2 = time.time()

        # check response
        self.assertTrue(isinstance(info, ntplib.NTPStats))
        self.assertTrue(0 < info.version <= 4)
        self.assertTrue(isinstance(info.offset, float))
        self.assertTrue(0 <= info.stratum < 0xff)
        self.assertTrue(-0x7f <= info.precision < 0x7f)
        self.assertTrue(isinstance(info.root_delay, float))
        self.assertTrue(isinstance(info.root_dispersion, float))
        self.assertTrue(isinstance(info.delay, float))
        self.assertTrue(isinstance(info.leap, int))
        self.assertIn(info.leap, ntplib.NTP.LEAP_TABLE)
        self.assertTrue(0 <= info.poll < 0xfff)
        self.assertTrue(isinstance(info.mode, int))
        self.assertIn(info.mode, ntplib.NTP.MODE_TABLE)
        self.assertTrue(0 <= info.ref_id < 0xffffffff)
        self.assertTrue(isinstance(info.tx_time, float))
        self.assertTrue(isinstance(info.ref_time, float))
        self.assertTrue(isinstance(info.orig_time, float))
        self.assertTrue(isinstance(info.recv_time, float))
        self.assertTrue(isinstance(info.dest_time, float))

        time.sleep(self.POLL_DELAY)

        new_info = client.request(self.NTP_SERVER)

        # check timestamps
        self.assertTrue(t_1 < info.orig_time < info.dest_time < t_2)
        self.assertTrue(info.orig_time < new_info.orig_time)
        self.assertTrue(info.recv_time < new_info.recv_time)
        self.assertTrue(info.tx_time < new_info.tx_time)
        self.assertTrue(info.dest_time < new_info.dest_time)

        # check the offset and delay
        self.assertLess(abs(new_info.offset - info.offset),
                        self.DELTA_TOLERANCE)
        self.assertLess(abs(new_info.delay - info.delay), self.DELTA_TOLERANCE)

        # try reaching a non existent server
        self.assertRaises(ntplib.NTPException,
                          client.request, "localhost", port=42)

        # try reaching a non existent server with a custom timeout
        t_before = time.time()
        self.assertRaises(ntplib.NTPException,
                          client.request, "localhost", port=42, timeout=1)
        self.assertTrue(0.7 < time.time() - t_before < 1.3)

    def test_helpers(self):
        """Helper methods tests."""
        client = ntplib.NTPClient()

        time.sleep(self.POLL_DELAY)
        info = client.request(self.NTP_SERVER)

        self.assertEqual(int(info.tx_time), ntplib.ntp_to_system_time(
                         ntplib.system_to_ntp_time(int(info.tx_time))))

        self.assertTrue(isinstance(ntplib.leap_to_text(info.leap), str))
        self.assertTrue(isinstance(ntplib.mode_to_text(info.mode), str))
        self.assertTrue(isinstance(ntplib.stratum_to_text(info.stratum), str))
        self.assertTrue(isinstance(ntplib.ref_id_to_text(info.ref_id,
                                                         info.stratum), str))

    def test_rollover(self):
        """ Test for rollover - see
            https://en.wikipedia.org/wiki/Network_Time_Protocol#Timestamps.
        """
        epoch = datetime.datetime.utcfromtimestamp(0)
        timestamp = (datetime.datetime(2022, 8, 5, 19, 8, 42) - epoch).total_seconds()
        self.assertEqual(
                ntplib.ntp_to_system_time(ntplib.system_to_ntp_time(timestamp)),
                timestamp)

        timestamp = (datetime.datetime(2036, 2, 7) - epoch).total_seconds()
        self.assertEqual(
                ntplib.ntp_to_system_time(ntplib.system_to_ntp_time(timestamp)),
                timestamp)

        timestamp = (datetime.datetime(2036, 2, 7, 12) - epoch).total_seconds()
        self.assertRaises(ntplib.NTPRolloverException,
                          ntplib.system_to_ntp_time, timestamp)

    def test_address_family(self):
        """ Test support of socket address family. """
        for address_family in [socket.AF_UNSPEC, socket.AF_INET]:
            client = ntplib.NTPClient()
            info = client.request(self.NTP_SERVER, address_family=address_family)
            self.assertLessEqual(info.offset, self.DELTA_TOLERANCE)


if __name__ == "__main__":
    unittest.main()
