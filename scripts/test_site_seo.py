"""Regression cases for public metadata and misleading discovery markup."""
import json
from pathlib import Path
import unittest

from check_site import PageParser, Report, check_discovery, check_page_shell


def page(body='<h1>Example</h1>', *, title='Example', description='A specific page.', robots='index, follow', lang='en', locale='en_GB', schema=None):
    parser = PageParser()
    markup = '' if schema is None else '<script type="application/ld+json">' + json.dumps(schema) + '</script>'
    parser.feed(f'<html lang="{lang}"><head><title>{title}</title><meta name="description" content="{description}"><meta name="robots" content="{robots}"><meta property="og:locale" content="{locale}">{markup}</head><body>{body}</body></html>')
    return parser


def errors(pages):
    report = Report()
    check_discovery(report, pages)
    return '\n'.join(message for _, message in report.errors)


def faq():
    return {'@type': 'FAQPage', 'mainEntity': {'@type': 'Question', 'name': 'Can I use it?', 'acceptedAnswer': {'@type': 'Answer', 'text': 'Contact me.'}}}


class SearchMetadataTests(unittest.TestCase):
    def test_valid_bilingual_pages(self):
        self.assertEqual('', errors({Path('index.html'): page(), Path('notes/pt/index.html'): page(title='Português', description='Uma página.', lang='pt-PT', locale='pt_PT')}))

    def test_duplicate_search_metadata(self):
        found = errors({Path('index.html'): page(), Path('work/index.html'): page(title='  EXAMPLE  ', description='a   specific page.')})
        self.assertIn('Duplicate published title', found)
        self.assertIn('Duplicate published description', found)

    def test_missing_or_multiple_h1(self):
        for body in ('<p>No heading</p>', '<h1>One</h1><h1>Two</h1>'):
            with self.subTest(body=body):
                self.assertIn('one H1', errors({Path('index.html'): page(body)}))

    def test_noindex_and_none_block_publication(self):
        for robots in ('noindex,follow', 'NONE', 'index, noindex'):
            with self.subTest(robots=robots):
                self.assertIn('remain indexable', errors({Path('index.html'): page(robots=robots)}))

    def test_intentionally_unindexed_files_exempt(self):
        self.assertEqual('', errors({Path('404.html'): page('', robots='noindex'), Path('notes/_template.html'): page('', robots='noindex')}))

    def test_locale_mismatch(self):
        self.assertIn('locale', errors({Path('index.html'): page(locale='pt_PT')}))


class StructuredContentTests(unittest.TestCase):
    visible = '<h1>Example</h1><details><summary>Can I use it?</summary><p>Contact me.</p></details>'

    def test_accessible_collapsed_faq_in_supported_jsonld_shapes(self):
        variants = [faq(), [faq()], {'@graph': [faq()]}, {'mainEntity': faq()}]
        array_type = faq()
        array_type['@type'] = ['WebPage', 'FAQPage']
        variants.append(array_type)
        for schema in variants:
            with self.subTest(schema=schema):
                self.assertEqual('', errors({Path('index.html'): page(self.visible, schema=schema)}))

    def test_array_questions_answers_and_html_text(self):
        data = faq()
        data['mainEntity']['acceptedAnswer'] = [{'@type': 'Answer', 'text': '<p>Contact <strong>me.</strong></p>'}]
        data['mainEntity'] = [data['mainEntity']]
        self.assertEqual('', errors({Path('index.html'): page(self.visible, schema=data)}))

    def test_script_and_hidden_text_do_not_satisfy_faq(self):
        for wrapper in ('<script>{}</script>', '<style>{}</style>', '<template>{}</template>', '<div hidden><span>{}</span></div>', '<div style="display: none">{}</div>', '<div style="visibility: hidden">{}</div>'):
            with self.subTest(wrapper=wrapper):
                body = '<h1>Example</h1>' + wrapper.format('Can I use it? Contact me.')
                self.assertIn('match visible', errors({Path('index.html'): page(body, schema=faq())}))

    def test_visible_content_after_hidden_block_is_collected(self):
        self.assertEqual('', errors({Path('index.html'): page('<div hidden>Hidden</div>' + self.visible, schema=faq())}))

    def test_missing_malformed_faq_is_reported_without_crash(self):
        for entity in (None, [], 'question', {'name': 'Can I use it?', 'acceptedAnswer': None}, {'name': 'Can I use it?', 'acceptedAnswer': 'text'}):
            with self.subTest(entity=entity):
                self.assertTrue(errors({Path('index.html'): page(schema={'@type': 'FAQPage', 'mainEntity': entity})}))

    def test_non_object_jsonld_does_not_crash_discovery(self):
        for schema in (None, 123, 'text', [None, 'text']):
            with self.subTest(schema=schema):
                self.assertEqual('', errors({Path('index.html'): page(schema=schema)}))

    def test_external_interviews_are_valid_creativeworks(self):
        data = {'@type': 'ItemList', 'itemListElement': [{'@type': 'CreativeWork', 'name': 'Interview', 'url': 'https://example.org/interview'}]}
        self.assertEqual('', errors({Path('index.html'): page(schema=data)}))

    def test_incomplete_nested_video_is_rejected(self):
        found = errors({Path('index.html'): page(schema={'subjectOf': [{'@type': ['CreativeWork', 'VideoObject'], 'name': 'Interview'}]})})
        self.assertIn('thumbnailUrl', found)
        self.assertIn('uploadDate', found)
        self.assertIn('playable video', found)

    def test_incomplete_video_dates_are_rejected(self):
        for value in ('2026-10-28', '2026-10-28T10:00:00', 'not a date', 123):
            with self.subTest(value=value):
                data = {'@type': 'VideoObject', 'name': 'Interview', 'thumbnailUrl': 'https://example.org/poster.jpg', 'uploadDate': value}
                self.assertIn('valid time and timezone', errors({Path('index.html'): page('<h1>Interview</h1><video controls></video>', schema=data)}))

    def test_complete_video_on_watch_page(self):
        data = {'@type': 'VideoObject', 'name': 'Interview', 'thumbnailUrl': 'https://example.org/poster.jpg', 'uploadDate': '2026-10-28T10:00:00+00:00'}
        self.assertEqual('', errors({Path('index.html'): page('<h1>Interview</h1><video controls src="/interview.mp4"></video>', schema=data)}))


class FragmentTests(unittest.TestCase):
    def test_same_page_fragment(self):
        self.assertEqual('', errors({Path('index.html'): page('<h1 id="intro">Example</h1><a href="#intro">Intro</a>')}))

    def test_missing_same_page_fragment(self):
        self.assertIn('Broken internal fragment', errors({Path('index.html'): page('<h1>Example</h1><a href="#missing">Go</a>')}))

    def test_cross_page_encoded_fragment(self):
        pages = {Path('index.html'): page('<h1>Example</h1><a href="/work/#ol%C3%A1">Go</a>'), Path('work/index.html'): page('<h1 id="olá">Olá</h1>', title='Work', description='Work details.')}
        self.assertEqual('', errors(pages))

    def test_absolute_internal_fragment(self):
        self.assertIn('Broken internal fragment', errors({Path('index.html'): page('<h1>Example</h1><a href="https://diogobronzesilva.com/#missing">Go</a>')}))

    def test_external_fragments_and_text_directives_are_not_ids(self):
        self.assertEqual('', errors({Path('index.html'): page('<h1>Example</h1><a href="https://example.org/#missing">External</a><a href="#:~:text=Example">Text</a>')}))


class PageShellTests(unittest.TestCase):
    shell = '<a class="skip" href="#main">Skip</a><a class="wordmark" href="/">Home</a><main id="main"></main>'

    def shell_errors(self, content, path='index.html'):
        parser = PageParser()
        parser.feed(content)
        report = Report()
        check_page_shell(report, Path(path), parser)
        return '\n'.join(message for _, message in report.errors)

    def test_shared_shell(self):
        self.assertEqual('', self.shell_errors(self.shell))

    def test_undefined_skip_and_wordmark_classes(self):
        found = self.shell_errors(self.shell.replace('class="skip"', 'class="skip-link"').replace('class="wordmark"', 'class="brand"'))
        self.assertIn('styled skip link', found)
        self.assertIn('shared wordmark', found)

    def test_every_mailto_needs_protection(self):
        link = '<a href="mailto:hello@diogobronzesilva.com">Email</a>'
        self.assertIn('Unprotected mailto', self.shell_errors(self.shell + link))
        self.assertEqual('', self.shell_errors(self.shell + '<!--email_off-->' + link + '<!--/email_off-->'))
        self.assertIn('Unprotected mailto', self.shell_errors(self.shell + '<!--email_off-->' + link + '<!--/email_off-->' + link))

    def test_inline_or_remote_scripts_rejected(self):
        for script in ('<script>run()</script>', '<script src="https://example.org/tracker.js"></script>'):
            self.assertIn('limited to', self.shell_errors(self.shell + script))

    def test_metadata_scripts_allowed(self):
        self.assertEqual('', self.shell_errors(self.shell + '<script type="application/ld+json">{}</script>'))

    def test_demo_requires_its_deferred_local_script(self):
        script = '<script src="/assets/js/vitachart-demo.js?v=1" defer></script>'
        self.assertEqual('', self.shell_errors(self.shell + script, 'vitachart/index.html'))
        for scripts in ('', script.replace(' defer', ''), script + '<script>run()</script>', script.replace('/assets/js/', 'https://example.org/assets/js/')):
            self.assertIn('only its deferred local script', self.shell_errors(self.shell + scripts, 'vitachart/index.html'))


if __name__ == '__main__':
    unittest.main()
