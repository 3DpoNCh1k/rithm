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
        if s == "accepted":
            return Verdict.AC
        if s == "wrong answer":
            return Verdict.WA
        if s == "runtime error":
            return Verdict.RE
        if s == "memory limit exceeded":
            return Verdict.MLE
        if s == "time limit exceeded":
            return Verdict.TLE
        if s == "compilation error":
            return Verdict.CE

        raise ValueError(f"Unknown verdict {s}")
