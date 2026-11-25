"""Build the standalone full-bin squeeze prototype using committed merge assets."""
from pathlib import Path
import re
root = Path(__file__).resolve().parents[1]
source = (root / "proto-merge.html").read_text(encoding="utf-8")
template = (root / "tools/proto/full-squeeze.tpl.html").read_text(encoding="utf-8")
matter = re.search(r"<script>([\s\S]+?)</script>", source).group(1)
chars = re.search(r"(const CHARS=.*?;)\n", source).group(1)
output = template.replace("/*MATTER*/", matter).replace("/*CHARS*/", chars)
(root / "proto-full-squeeze.html").write_text(output, encoding="utf-8")
