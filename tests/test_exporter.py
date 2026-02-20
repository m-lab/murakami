from murakami.exporter import MurakamiExporter


class DummyExporter(MurakamiExporter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.calls = []

    def _push_single(self, test_name="", data=None, timestamp=None, test_idx=None):
        self.calls.append(
            {
                "test_name": test_name,
                "data": data,
                "timestamp": timestamp,
                "test_idx": test_idx,
            }
        )
        return True


def test_generate_filename_uses_metadata_and_index():
    exporter = DummyExporter(
        location="baltimore",
        network_type="home",
        connection_type="wired",
    )

    filename = exporter._generate_filename(
        test_name="NDT7Custom",
        timestamp="2026-02-20T10:11:12.000000",
        test_idx=2,
    )

    assert (
        filename
        == "ndt7custom-baltimore-home-wired-2-2026-02-20T10:11:12.000000.jsonl"
    )


def test_push_list_dispatches_all_items_with_incrementing_indexes():
    exporter = DummyExporter()

    exporter.push(
        test_name="ndt7custom",
        data=["result-1", "result-2", "result-3"],
        timestamp="2026-02-20T10:11:12.000000",
    )

    assert len(exporter.calls) == 3
    assert [call["test_idx"] for call in exporter.calls] == [0, 1, 2]
    assert all(call["test_name"] == "ndt7custom" for call in exporter.calls)
    assert all(
        call["timestamp"] == "2026-02-20T10:11:12.000000"
        for call in exporter.calls
    )
