from enum import Enum


class Verdict(Enum):
    AC = 1
    WA = 2
    RE = 3
    MLE = 4
    TLE = 5
    CE = 6

    @staticmethod
    def from_string(s: str):
        s = s.lower()
        if "accepted" in s:
            return Verdict.AC
        if "wrong answer" in s:
            return Verdict.WA
        if "runtime error" in s:
            return Verdict.RE
        if "memory limit exceeded" in s:
            return Verdict.MLE
        if "time limit exceeded" in s:
            return Verdict.TLE
        if "compilation error" in s:
            return Verdict.CE

        raise ValueError(f"Unknown verdict {s}")
