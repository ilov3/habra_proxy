# -*- coding: utf-8 -*-
# Owner: Bulat <bulat.kurbangaliev@cinarra.com>
import logging
import unittest
from proxy import process_habr_page

__author__ = 'ilov3'
logger = logging.getLogger(__name__)


class TestHabrPageProcess(unittest.TestCase):
    def test_tm_append(self):
        """
        Description: Test for checking trade mark symbol appendance
        """
        source = """<div>Сейчас на фоне уязвимости Logjam все в индустрии в очередной раз обсуждают 
        проблемы и особенности TLS. Я хочу воспользоваться этой возможностью, чтобы 
        поговорить об одной из них, а именно — о настройке ciphersuites.</div>"""
        expected = """<div>Сейчас™ на фоне уязвимости Logjam™ все в индустрии в очередной раз обсуждают 
        проблемы и особенности TLS. Я хочу воспользоваться этой возможностью, чтобы 
        поговорить об одной из них, а именно™ — о настройке ciphersuites.</div>"""
        assert expected == process_habr_page(source), f'Expected:\n{expected}\nGot:\n{process_habr_page(source)}'

    def test_url_replace(self):
        """
        Description: Test for checking host:port replacement
        """
        source = """<span><a href="https://habr.com/some/path">Link1</a>
        <a href="https://habr.com/another/path">Link2</a>
        <use xlink:href="https://habr.com/xlink/href/path"></use></span>"""
        expected = """<span><a href="http://127.0.0.1:8080/some/path">Link1</a>
        <a href="http://127.0.0.1:8080/another/path">Link2</a>
        <use xlink:href="http://127.0.0.1:8080/xlink/href/path"></use></span>"""
        assert expected == process_habr_page(source), f'Expected:\n{expected}\nGot:\n{process_habr_page(source)}'

    def test_text_inside_br_tag(self):
        """
        Description: Test for checking br tag handling
        """
        source = """<div>Сейчас на фоне уязвимости Logjam все в индустрии в очередной раз обсуждают 
                проблемы и особенности TLS. <br>Я хочу воспользоваться этой возможностью, чтобы 
                поговорить об одной из них, а именно — о настройке ciphersuites.</div>"""
        expected = """<div>Сейчас™ на фоне уязвимости Logjam™ все в индустрии в очередной раз обсуждают 
                проблемы и особенности TLS. <br>Я хочу воспользоваться этой возможностью, чтобы 
                поговорить об одной из них, а именно™ — о настройке ciphersuites.</div>"""
        assert expected == process_habr_page(source), f'Expected:\n{expected}\nGot:\n{process_habr_page(source)}'


if __name__ == '__main__':
    unittest.main()
