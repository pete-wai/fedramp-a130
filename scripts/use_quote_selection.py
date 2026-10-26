"""Manually selected primary-source excerpts for the proposed agency-use workbook."""
import json,hashlib
from pathlib import Path
import fitz
from history_sources import R,S,source,norm
D=R/'data/proposed-fedramp-use';P=R/'site/proposed-fedramp-use'
old=json.loads((R/'data/on-behalf/history-quotations.json').read_text())
keep=['f14-dual','f14-implement','f14-program','a16-contracts','a16-oversight','a16-ato','f200-select','rmf18-external','act22-program','omb24-atu']
quotes=[q for q in old if q['id'] in keep]
print('Reused', [q['id'] for q in quotes])
sources={}
for q in quotes:
 r=source(q['source_id']).copy();r['local']='../on-behalf/'+r['local'];r.pop('text',None);sources[r['id']]=r
for r in json.loads((D/'web-sources.json').read_text()):sources[r['id']]=r

def take(id,sid,pages,start,end,loc):
 if sid not in sources:
  r=source(sid).copy();r['local']='../on-behalf/'+r['local'];r.pop('text',None);sources[sid]=r
 r=sources[sid];file=(P/(r['text'] if sid.startswith('fed-') else r['local'])).resolve()
 if file.suffix=='.pdf':
  with fitz.open(file) as d:t=' '.join(norm(d[p-1].get_text()) for p in pages)
 else:t=norm(file.read_text())
 try: a=t.index(start);b=t.index(end,a)+len(end)
 except ValueError: raise ValueError(f'Missing quote boundary: {id}')
 quotes.append(dict(id=id,source_id=sid,source_file=str(file.relative_to(R)),pages=pages,text=t[a:b],locator=loc,normalization='Whitespace, punctuation spacing and PDF line-end hyphenation only; wording retained.'))

take('act-process','fedramp-act',[1056],'‘‘(1) in consultation with the Secretary','relevant statutes;','44 USC 3609(a)(1)–(3); 136 Stat. 3450')
take('act-reuse','fedramp-act',[1059],'‘‘(3) to the extent practicable','product or service;','44 USC 3613(a)(3); 136 Stat. 3453')
take('act-presume','fedramp-act',[1060],'‘‘(e) PRESUMPTION OF ADEQUACY','for a particular control implementation.','44 USC 3613(e)(1)–(2); 136 Stat. 3454')
take('act-notify','fedramp-act',[1060],'‘‘(c) SUBMISSION OF AUTHORIZATIONS','to the Administrator.','44 USC 3613(c); 136 Stat. 3454')
take('omb-rescind','m-24-15',[1],'As a result, this memorandum rescinds','since the program was established.','Introduction, p. 1')
take('omb-process','m-24-15',[7],'FedRAMP is responsible','receive a FedRAMP authorization.','§IV(b), p. 7; footnote 15 cites 44 USC 3609(a)(2)')
take('omb-scope','m-24-15',[5],'FedRAMP’s goal is','specified as out of scope below.','§III, p. 5; exclusions and unclassified/non-NSS limit follow')
take('omb-presume','m-24-15',[6],'To that end, if a given','that FIPS 199 impact level.','§IV(a), p. 6; continued on p. 7: authorization must be actively maintained')
take('omb-monitor','m-24-15',[14],'For all FedRAMP authorized products','within another information system.','§VI, p. 14')
take('omb-agility','m-24-15',[13],'Redesigns the process','existing FedRAMP authorized products and services;','§VI, p. 13')
take('f199-info','fips199',[7],'The security category of an information type','the particular information type.','§3, printed p. 3')
take('f199-system','fips199',[8],'Determining the security category','resident on the information system.','§3, printed p. 4')
# Second sentence begins with the first sentence's ending; select the full high-water-mark statement separately.
take('f199-highwater','fips199',[8],'For an information system, the potential','resident on the information system.','§3, printed p. 4')
take('rmf-boundary','sp800372',[36],'The authorization boundary establishes','organization’s missions and business functions.','§2.5, printed p. 17; see footnote 42 on direct management')
take('rmf-allocate','sp800372',[72],'The organization designates controls','require that capability.','Task S-3, printed p. 53')
take('rmf-atu','sp800372',[163],'An authorization to use is employed','a common control authorization.','Appendix F, printed p. 144; footnotes 140–141')
take('rmf-atu-condition','sp800372',[163],'A customer organization can issue','provider organization).','Appendix F, p. 144; footnote 142 recognizes a GSA FedRAMP provisional ATO')
take('rmf-atu-decision','sp800372',[167],'The authorization to use is a streamlined','service (if any).','Appendix F, printed p. 148')
take('rmf-integrate','sp800372',[164],'If the customer organization plans','risk in doing so.','Appendix F, printed p. 145')
take('sa9-control','sp800535',[298],'Control: a. Require','organization-defined processes, methods, and techniques].','SA-9(a)–(c), printed p. 271; Rev. 5, December 2020 update')
take('sa9-risk','sp800535',[298],'Discussion: External system services','instances of noncompliance.','SA-9 discussion, printed p. 271')
take('sa4-contract','sp800535',[279],'Control: Include the following','i. Acceptance criteria.','SA-4(a)–(i), printed p. 252; control text, not the later revised discussion')
take('ca3-exchange','sp800535',[114],'b. Document, as part of each exchange agreement','agreements [Assignment: organization-defined frequency].','CA-3(b)–(c), printed p. 87; subsection (a) requires approval and management of the exchange through agreements')
take('fed-premise','fed-use',[],'Agencies use FedRAMP Certifications','responsible for operating.','Opening paragraph; retrieved October 26, 2026')
take('fed-before','fed-initial',[],'The resulting Authorization to Operate','use of the cloud service.','Introduction; retrieved October 26, 2026')
take('fed-class','fed-initial',[],'Certification Classes','security categorization or risk decision.','§2, Compare FedRAMP Certified services')
take('fed-configure','fed-initial',[],'Configure the service according','provider’s capabilities.' if False else "provider's capabilities.",'§4, Configure and assess the agency’s use')
take('fed-notify','fed-rules',[],'Agencies MUST notify FedRAMP upon','form by FedRAMP.','AGU-AGC-NAA; current page labels rules required, effective July 4, 2026')
take('fed-extra','fed-rules',[],'Agencies MUST NOT require additional information','FedRAMP Certification Data.','AGU-AGC-NAR; demonstrable need, notification, clarification exception')
take('fed-monitor','fed-ongoing',[],'FedRAMP provides a minimum standard level','appropriate for the agency’s use.' if False else "appropriate for the agency's use.",'FedRAMP’s Standard Continuous Monitoring')
take('baseline-modern','sp80053b',[4],'This publication provides security and privacy','control selection process.','Abstract, printed p. ii; October 2020, includes December 10, 2020 update')
D.joinpath('quotations.json').write_text(json.dumps(quotes,indent=2,ensure_ascii=False)+'\n')
D.joinpath('sources.json').write_text(json.dumps(list(sources.values()),indent=2,ensure_ascii=False)+'\n')
print('Selected',len(quotes),'quotes from',len(sources),'sources')
