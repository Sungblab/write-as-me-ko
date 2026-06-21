from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.create_writing_skill import (
    PRESETS,
    WritingSkillSpec,
    create_skill,
    render_skill,
    slugify,
)


class CreateWritingSkillTests(unittest.TestCase):
    def test_slugify_normalizes_user_provided_names(self) -> None:
        self.assertEqual(slugify("Thread Post!!"), "thread-post")
        self.assertEqual(slugify("LinkedIn   Launch 글"), "linkedin-launch")
        self.assertRegex(slugify("교수님 메시지"), r"^writing-skill-[0-9a-f]{8}$")

    def test_render_thread_preset_contains_thread_constraints(self) -> None:
        template = Path("templates/writing-skill/SKILL.md").read_text(encoding="utf-8")
        rendered = render_skill(PRESETS["thread-post"], template)

        self.assertIn('name: "thread-post"', rendered)
        self.assertIn("# thread-post", rendered)
        self.assertIn("Keep each post under 500 Korean characters.", rendered)
        self.assertIn("Default to about 5 posts.", rendered)
        self.assertIn("Do not make the thread sound like generic marketing copy.", rendered)

    def test_create_skill_writes_custom_skill_without_overwriting(self) -> None:
        spec = WritingSkillSpec(
            name="Professor Message",
            description="Draft concise Korean professor messages.",
            purpose="Write a short respectful message.",
            audience="A professor.",
            constraints=("Use polite Korean.",),
            tone=("Concise.",),
            checklist=("No invented excuses.",),
        )
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            written = create_skill(spec, root)

            self.assertTrue(written.exists())
            self.assertIn('name: "professor-message"', written.read_text(encoding="utf-8"))
            self.assertIn("# Professor Message", written.read_text(encoding="utf-8"))
            with self.assertRaises(FileExistsError):
                create_skill(spec, root)

    def test_every_preset_generates_valid_frontmatter_shape(self) -> None:
        template = Path("templates/writing-skill/SKILL.md").read_text(encoding="utf-8")
        for preset in PRESETS.values():
            rendered = render_skill(preset, template)
            self.assertTrue(rendered.startswith('---\nname: "'))
            self.assertIn('\ndescription: "', rendered)
            self.assertIn("\n---\n", rendered)


if __name__ == "__main__":
    unittest.main()
