"""Offline behavior checks for the personal memory-stream guard."""
from unittest.mock import patch

from octop_harness.memory import llm_client
from octop_harness.protocols.langgraph import _is_internal_model_stream

with patch.object(llm_client, "ensure_config", return_value={"metadata": {"trace": "kept"}}):
    config = llm_client._aux_invoke_config()
assert config["callbacks"] == []
assert config["metadata"] == {"trace": "kept", "lc_source": "memory_aux"}
assert _is_internal_model_stream(config["metadata"])
assert _is_internal_model_stream({"lc_source": "summarization"})
assert not _is_internal_model_stream({"lc_source": "user_chat"})
assert not _is_internal_model_stream(None)
print("PASS: memory metadata preserved, parent callbacks isolated, internal streams filtered")
