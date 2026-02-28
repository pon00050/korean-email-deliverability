from dataclasses import dataclass, field


@dataclass
class CheckResult:
    name: str
    status: str        # "pass" | "warn" | "fail" | "error"
    score: int         # 0–100
    message_ko: str    # one-line finding shown in summary table
    detail_ko: str = ""        # expanded context
    remediation_ko: str = ""   # what to do about it
    raw: str = ""              # raw DNS record or HTTP snippet
