"""Regression cases from the historical source formats."""
import re,unittest
from readers import paragraphs
class Headings(unittest.TestCase):
 def test_numbered_and_inline(self):
  self.assertIn('<h2 class="document-heading">1. Introduction</h2>',paragraphs('1. Introduction\nInformation is important.'))
  self.assertIn('<h2 class="document-heading">1. Purpose:</h2><p>This Circular establishes policy.</p>',paragraphs('1. Purpose: This Circular establishes policy.'))
  self.assertIn('<h3 class="document-heading">a. Planning and Budgeting</h3>',paragraphs('a. Planning and Budgeting'))
 def test_ocr_question(self):
  self.assertIn('>1. What is contingency planning?</h2>',paragraphs('1.\nWhat is contingency planning?\nPlanning helps.'))
 def test_not_headings(self):
  for text in ['52730 Federal Register / Vol. 50','136 STAT. 3449','44 USC 3607.','FIPS PUB 12','Appendix IV to emphasize the','(ADP)','contents','1. focusing information resource planning to support their strategic missions;']:
   self.assertNotRegex(paragraphs(text),r'<h[23]',text)
 def test_named_and_wrapped(self):
  self.assertIn('>FOREWORD</h2>',paragraphs('FOREWORD'))
  self.assertIn('>OFFICE OF MANAGEMENT AND BUDGET</h2>',paragraphs('OFFICE OF MANAGEMENT AND\nBUDGET'))
if __name__=='__main__':unittest.main()
