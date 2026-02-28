from pathlib import Path
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

from src.models import CheckResult
from src.scorer import overall_score, naver_score, grade, naver_label, status_emoji


TEMPLATES_DIR = Path(__file__).parent.parent / "templates"


def generate_report(
    domain: str,
    results: list[CheckResult],
    output_path: Path,
) -> Path:
    env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)), autoescape=True)
    template = env.get_template("report.html.j2")

    score = overall_score(results)
    n_score = naver_score(results)
    n_emoji, n_label = naver_label(n_score)

    html = template.render(
        domain=domain,
        scan_time=datetime.now().strftime("%Y년 %m월 %d일 %H:%M"),
        results=results,
        overall=score,
        grade=grade(score),
        naver_score=n_score,
        naver_emoji=n_emoji,
        naver_label=n_label,
        status_emoji=status_emoji,
        grade_color=_grade_color(grade(score)),
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")
    return output_path


def _grade_color(g: str) -> str:
    return {"A": "#16a34a", "B": "#65a30d", "C": "#d97706", "D": "#ea580c", "F": "#dc2626"}.get(g, "#6b7280")
