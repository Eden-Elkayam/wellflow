import unittest
import pandas as pd
import wellflow.plate as wf


class TestPlate(unittest.TestCase):

    def setUp(self):
        self.rawData = pd.DataFrame([[pd.to_timedelta("0:15:00"),37,1.100,0.100,1.00,0.090],
                                     [pd.to_timedelta("0:30:00"),37,1.150,0.120,1.200,0.100],
                                     [pd.to_timedelta("0:45:00"),37,1.200,0.125,1.300,0.150,],
                                     [pd.to_timedelta("01:00:00"),37,1.300,0.130,1.152,0.095]],
                                    columns=["time","temperature_c","A1","A2","B1","B2"])
        self.tidy = pd.DataFrame([[pd.to_timedelta("0:15:00"), 37, "A1", 1.1],
            [pd.to_timedelta("0:15:00"), 37, "A2", 0.1],
            [pd.to_timedelta("0:15:00"), 37, "B1", 1.0],
            [pd.to_timedelta("0:15:00"), 37, "B2", 0.09],
            [pd.to_timedelta("0:30:00"), 37, "A1", 1.15],
            [pd.to_timedelta("0:30:00"), 37, "A2", 0.12],
            [pd.to_timedelta("0:30:00"), 37, "B1", 1.2],
            [pd.to_timedelta("0:30:00"), 37, "B2", 0.10],
            [pd.to_timedelta("0:45:00"), 37, "A1", 1.2],
            [pd.to_timedelta("0:45:00"), 37, "A2", 0.125],
            [pd.to_timedelta("0:45:00"), 37, "B1", 1.3],
            [pd.to_timedelta("0:45:00"), 37, "B2", 0.15],
            [pd.to_timedelta("1:00:00"), 37, "A1", 1.3],
            [pd.to_timedelta("1:00:00"), 37, "A2", 0.13],
            [pd.to_timedelta("1:00:00"), 37, "B1", 1.152],
            [pd.to_timedelta("1:00:00"), 37, "B2", 0.095],
        ], columns=["time", "temperature_c", "well", "od"])

        self.tidy_with_time = self.tidy.copy()
        self.tidy_with_time["time_hours"] = [0.25,0.25,0.25,0.25, 0.5, 0.5, 0.5, 0.5, 0.75,0.75,0.75,0.75,1,1,1,1]

        self.rawDesign = self.meta = pd.DataFrame([["column", 1,2,1,2],
        ["A", "WT", "ΔCA", 88,  89],
        ["B", "WT", "ΔCA", 88,  89]
    ],
    columns=["value_type", "strain.1", "strain.2", "bio_rep.1", "bio_rep.2"]
)
        self.design = pd.DataFrame([["A1", "WT",  88],
        ["A2", "ΔCA", 89],
        ["B1", "WT",  88],
        ["B2", "ΔCA", 89],],
    columns=["well", "strain", "bio_rep"])

        self.full_raw = self.tidy_with_time.merge(self.design, on="well", how="left")

        self.full_with_blanks = self.full_raw.copy().sort_values(by=["well", "time"])
        self.full_with_blanks["od_blank"] = [0,0.025,0.075,0.175,0,0.01,0.015,0.02,0,0.1,0.2,0.052,0,0.005,0.055,0]
        self.full_with_blanks.sort_values(by=["time_hours", "well"], inplace=True)

        self.full_with_smooth = self.full_with_blanks.copy().sort_values(by=["well", "time_hours"])
        self.full_with_smooth["od_smooth"] = [0.0125,0.033333333,0.091666667,0.125,0.005,0.008333333,0.015,0.0175,0.05,0.1,0.117333333,0.126,0.0025,0.02,0.02,0.0275]
        self.full_with_smooth.sort_values(by=["time_hours", "well"], inplace=True)
        self.full_with_smooth["od_smooth"] = self.full_with_smooth["od_smooth"].round(6)

        self.full_with_gr = self.full_with_smooth.copy().sort_values(by=["well", "time_hours"])
        self.full_with_gr["mu"] = [3.923277012,3.984867602,2.64353168,1.240605168,2.043142492,2.197224578,1.483954692,0.61660272,2.772588724,1.705986082,0.462223442,0.285063444,8.317766168,4.158883084,0.636907462,1.273814924]
        self.full_with_gr.sort_values(by=["time_hours", "well"], inplace=True)
        self.full_with_gr["mu"] = self.full_with_gr["mu"].round(6)


    def test_wide_to_tidy(self):
        before = self.rawData.copy()
        after = wf._convert_wide_to_tidy(before, ["time", "temperature_c"])
        expected_after = self.tidy.sort_values(by=["time", "well"])
        pd.testing.assert_frame_equal(after, expected_after)

    def test_add_time_hours(self):
        after = wf._add_time_hours_from_timedelta(self.tidy)
        pd.testing.assert_frame_equal(after, self.tidy_with_time)

    def test_plate_design(self):
        raw = self.rawDesign.copy()
        after = wf.read_plate_design(raw)
        expected = self.design
        pd.testing.assert_frame_equal(after, expected)

    def test_blank(self):
        actual = wf.with_blank_corrected_od(self.full_raw, 2)
        pd.testing.assert_frame_equal(actual,self.full_with_blanks)

    def test_smooth(self):
        actual = wf.add_smoothed_od(self.full_with_blanks,window=3)
        actual["od_smooth"] = actual["od_smooth"].round(6)
        pd.testing.assert_frame_equal(actual,self.full_with_smooth)

    def test_mu(self):
        actual = wf.add_growth_rate(self.full_with_smooth, window=3)
        actual["mu"] = actual["mu"].round(6)
        pd.testing.assert_frame_equal(actual[["well","mu"]],self.full_with_gr[["well","mu"]])


if __name__ == "__main__":
    unittest.main()

