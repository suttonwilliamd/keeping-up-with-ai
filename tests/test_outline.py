"""Structural/copy contract, not a substitute for browser accessibility testing."""
from html.parser import HTMLParser
from pathlib import Path
import unittest

TITLES = ["The Evolution of AI", "How Neural Networks Work", "Transformers and Attention",
          "Large Language Models Explained", "The Agent Revolution", "What's Coming Next"]
SOURCE = Path(__file__).resolve().parents[1] / "index.html"


class Document(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.ids, self.links, self.tags, self.text, self.headings = [], [], [], [], []
        self.heading = None
        self.feed(source)
        self.close()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append((tag, attrs))
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag == 'a':
            self.links.append(attrs.get('href', ''))
        if tag in ('h1', 'h2', 'h3'):
            self.heading = [tag, '']

    def handle_endtag(self, tag):
        if self.heading and tag == self.heading[0]:
            self.headings.append(tuple(self.heading))
            self.heading = None

    def handle_data(self, data):
        self.text.append(data)
        if self.heading:
            self.heading[1] += data


def validate(source):
    doc = Document(source)
    errors = []
    if len(doc.ids) != len(set(doc.ids)):
        errors.append('duplicate id')
    if any(not href.startswith('#') or not href[1:] or href[1:] not in doc.ids for href in doc.links):
        errors.append('dead or external link')
    for target in ('#main', '#outline', '#availability'):
        if target not in doc.links:
            errors.append('missing navigation ' + target)
    if [text for tag, text in doc.headings if tag == 'h3'] != TITLES:
        errors.append('outline changed')
    tags = [tag for tag, _ in doc.tags]
    if tags.count('main') != 1 or tags.count('nav') != 1 or tags.count('h1') != 1:
        errors.append('missing landmarks or main heading')
    for target in ('main', 'outline', 'availability'):
        if not any(a.get('id') == target and a.get('tabindex') == '-1' for _, a in doc.tags):
            errors.append('unfocusable navigation target')
    if not any(t == 'html' and a.get('lang') == 'en' for t, a in doc.tags):
        errors.append('missing language')
    if any(tag in ('script', 'iframe', 'form', 'input', 'button', 'img', 'link') for tag in tags):
        errors.append('unexpected dependency or interaction')
    text = ' '.join(' '.join(doc.text).split()).lower()
    for required in ('proposed chapter titles, not verified finished chapters',
                     'this page is an outline only',
                     'no purchase, download or fulfillment is available here',
                     'a printed outline is not the guide pdf',
                     'written by aaron ai | supervised by william sutton'):
        if required not in text:
            errors.append('missing disclosure: ' + required)
    for unsupported in ('$19', 'get the pdf', 'money-back', '30-day', 'clear explanations',
                        'practical knowledge', 'this guide cuts through', 'buy now', 'checkout'):
        if unsupported in text:
            errors.append('unsupported promise: ' + unsupported)
    return errors


class OutlineContract(unittest.TestCase):
    def setUp(self):
        self.source = SOURCE.read_text(encoding='utf-8')

    def test_public_outline(self):
        self.assertEqual(validate(self.source), [])

    def test_dead_cta(self):
        self.assertIn('dead or external link', validate(self.source.replace('href="#outline"', 'href="#"', 1)))

    def test_missing_target(self):
        self.assertIn('dead or external link', validate(self.source.replace('id="outline"', 'id="lost"')))

    def test_duplicate_anchor(self):
        self.assertIn('duplicate id', validate(self.source.replace('id="top"', 'id="main"')))

    def test_changed_or_reordered_outline(self):
        for old, new in [(TITLES[0], 'New chapter'), (TITLES[1], TITLES[0])]:
            with self.subTest(old=old):
                self.assertIn('outline changed', validate(self.source.replace(old, new)))

    def test_lost_disclosure(self):
        self.assertTrue(any(e.startswith('missing disclosure') for e in validate(self.source.replace('This page is an outline only.', 'Available soon.'))))

    def test_sales_regression(self):
        for claim in ('$19', 'Get the PDF', '30-day money-back guarantee', 'Buy now', 'Checkout'):
            with self.subTest(claim=claim):
                self.assertTrue(any(e.startswith('unsupported promise') for e in validate(self.source.replace('</main>', claim + '</main>'))))

    def test_external_dependency(self):
        self.assertIn('unexpected dependency or interaction', validate(self.source.replace('</head>', '<script src="https://example.invalid/a.js"></script></head>')))

    def test_keyboard_target_regression(self):
        self.assertIn('unfocusable navigation target', validate(self.source.replace('class="shell" tabindex="-1"', 'class="shell"', 1)))

    def test_landmark_regression(self):
        self.assertIn('missing landmarks or main heading', validate(self.source.replace('<main ', '<div ').replace('</main>', '</div>')))


if __name__ == '__main__':
    unittest.main()
