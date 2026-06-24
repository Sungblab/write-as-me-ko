from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path


class ProfilePackTests(unittest.TestCase):
    def test_build_profile_pack_writes_v2_artifacts_without_raw_sample_text(self) -> None:
        try:
            from write_as_me.profile_pack import build_profile_pack
        except ModuleNotFoundError as exc:
            self.fail(f"profile pack package is missing: {exc}")

        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            samples = root / "samples"
            output = root / "dist" / "profile-pack"
            (samples / "blog").mkdir(parents=True)
            (samples / "project").mkdir()
            (samples / "private").mkdir()
            (samples / "blog" / "post.md").write_text(
                "나는 처음에는 쉽게 봤다. 그런데 실제로 구현해보니 판단이 바뀌었다.",
                encoding="utf-8",
            )
            (samples / "project" / "readme.md").write_text(
                "구현 결과와 검증 명령을 먼저 적고, 남은 한계를 분리한다.",
                encoding="utf-8",
            )
            (samples / "private" / "journal.md").write_text(
                "이 민감한 원문 문장은 export에 그대로 들어가면 안 된다.",
                encoding="utf-8",
            )

            pack = build_profile_pack(samples, output)

            profile = json.loads((output / "profile.json").read_text(encoding="utf-8"))
            manifest = json.loads((output / "sample-manifest.json").read_text(encoding="utf-8"))
            privacy = (output / "privacy-report.md").read_text(encoding="utf-8")
            coverage = (output / "coverage-report.md").read_text(encoding="utf-8")
            route_map = (output / "route-map.md").read_text(encoding="utf-8")

        self.assertEqual(pack.profile_path.name, "profile.json")
        self.assertEqual(profile["schema_version"], 2)
        self.assertEqual(profile["product"], "write-as-me-ko")
        self.assertEqual(profile["raw_samples_included"], False)
        self.assertEqual(profile["summary"]["sample_count"], 3)
        self.assertEqual(profile["summary"]["confidence"], "medium")
        self.assertIn("blog", profile["routes"])
        self.assertIn("project", profile["routes"])
        self.assertIn("other", profile["routes"])
        self.assertEqual(manifest["raw_samples_included"], False)
        self.assertEqual(len(manifest["samples"]), 3)
        self.assertIn("sha256", manifest["samples"][0])
        self.assertNotIn("민감한 원문 문장", json.dumps(manifest, ensure_ascii=False))
        self.assertIn("private", privacy)
        self.assertIn("Raw sample text included: no", privacy)
        self.assertIn("Coverage Status", coverage)
        self.assertIn("blog", route_map)


if __name__ == "__main__":
    unittest.main()
