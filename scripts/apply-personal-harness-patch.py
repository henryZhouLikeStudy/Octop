"""Retain the personal memory-stream guard on octop-harness 1.0.7."""
from __future__ import annotations

import argparse
import importlib.metadata
from pathlib import Path


def replacement(text: str, before: str, after: str) -> str:
    if after in text:
        return text
    if text.count(before) != 1:
        raise RuntimeError("Harness source differs from the verified 1.0.7 baseline")
    return text.replace(before, after, 1)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Validate the patch without writing")
    args = parser.parse_args()
    dist = importlib.metadata.distribution("octop-harness")
    if dist.version != "1.0.7":
        raise RuntimeError(f"Expected octop-harness 1.0.7, found {dist.version}")
    base = Path(dist.locate_file(""))
    changes = {}
    path = base / "octop_harness/memory/llm_client.py"
    text = path.read_text(encoding="utf-8")
    text = replacement(text, "import httpx\n", "import httpx\nfrom langchain_core.runnables.config import ensure_config\n")
    text = replacement(text, 'ThinkingMode = Literal["auto", "off", "on"]', 'AUX_LC_SOURCE = "memory_aux"\n\nThinkingMode = Literal["auto", "off", "on"]')
    text = replacement(text, 'bound_model.invoke(messages, config={"callbacks": []})', 'bound_model.invoke(messages, config=_aux_invoke_config())')
    helper = '''def _aux_invoke_config() -> dict[str, Any]:
    """Keep auxiliary memory model output out of the parent chat stream."""
    metadata = dict(ensure_config().get("metadata") or {})
    metadata["lc_source"] = AUX_LC_SOURCE
    return {"callbacks": [], "metadata": metadata}


'''
    text = replacement(text, "def _is_temperature_rejection(", helper + "def _is_temperature_rejection(") if "def _aux_invoke_config()" not in text else text
    changes[path] = text
    path = base / "octop_harness/protocols/langgraph.py"
    text = path.read_text(encoding="utf-8")
    text = replacement(text, '_INTERNAL_LC_SOURCES = frozenset({"summarization"})', '_INTERNAL_LC_SOURCES = frozenset({"summarization", "memory_aux"})')
    changes[path] = text
    for path, text in changes.items():
        compile(text, str(path), "exec")
    for path, text in changes.items():
        if not args.check:
            with path.open("w", encoding="utf-8", newline="\n") as output:
                output.write(text)
        print(("checked " if args.check else "patched ") + str(path.relative_to(base)))


if __name__ == "__main__":
    main()
