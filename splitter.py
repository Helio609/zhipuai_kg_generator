import re


def split_sentence(content: str) -> list[str]:
    """Split the content with the specific delims"""
    sentences = re.split("(\.|。|\!|！|\?|？)", content)
    return [
        sentence
        for i, sentence in enumerate(sentences)
        if i % 2 == 0 and len(sentence) != 0
    ]


import unittest


class TestSplitter(unittest.TestCase):

    def test_split_content(self):
        self.assertEqual(
            len(split_sentence("我真的，哭死。你也太厉害了！你怎么这么厉害？哦买噶；")),
            4,
        )
        self.assertEqual(len(split_sentence("哈！哈哈!哈哈哈。哈哈哈哈.")), 4)


if __name__ == "__main__":
    unittest.main()
