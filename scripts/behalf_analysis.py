"""Quoted authorities and authored interpretation for the private-services report."""
TITLE = 'Federal information in private services'
DECK = 'Buying a service, operating a system, and protecting information are different responsibilities. The wording tells us which duties travel with the information.'
SUMMARY = 'An agency can remain responsible for information without operating the private system that handles it. Some requirements follow the information; others attach to a covered system, a particular service, or an agreement. The distinction is real. It is not a blanket exemption for commercially sold services.'
# Each item: ID, heading, quote IDs, explanation paragraphs, additional references.
WORDS = [
 ('information-first','FISMA assigns two duties under one protection standard',['law-risk','law-info','law-system'],[
  'These are separate objects of the agency head’s duty, joined by “and.” The first is information collected or maintained by or on behalf of the agency. The second is systems used or operated by the specified parties. Neither limb says that the agency must own the equipment.',
  'The information clause does not first require declaring a recipient’s entire system federal. Conversely, the system clause does not say only “operated”: it also says “used,” and expressly includes contractor and other-organization operation. This text alone does not resolve which part of a purchased service constitutes the covered system.',
  'The excerpts are from the 2014 enactment. The collected current Code retains these two clauses. The phrases “created,” “processed,” and “disposed of” belong to the broader information lifecycle language in A-130, not this sentence of FISMA.'
 ],[('usc3554','44 USC 3554(a)(1)(A)(i)–(ii); collected Code through September 30, 2026'),('a130-2016','§10(22)–(23)')]),
 ('risk-and-rules','Risk management is a duty, not the only duty',['law-comply','law-test','law-program'],[
  'Section 3554(a)(2) assigns officials risk assessment, selection of appropriate protection, risk reduction, and testing. Section 3554(b) requires an agency-wide program that includes outside support. The agency cannot satisfy all of this merely by acknowledging that a private service is risky.',
  'These are obligations imposed on the agency. A provider’s particular obligations must be traced to an applicable law, regulation, contract, or other agreement. An agency’s accountability does not itself confer ownership of the provider or unlimited authority over its business.'
 ],[('usc3554','44 USC 3554(a)(2)(A)–(D), (b)(1)–(8)')]),
]
ROLES = [
 ('private-business','Buying access is different from commissioning operation',['owner','ao'],[
  'A supplier may independently design, own, run, and sell a standard service. The agency buys access and controls its own users and content. A different contract may require a company to build and operate a specified agency application. Those arrangements distribute operational responsibility differently.',
  'NIST’s system owner is a management role, not a statement about legal title to equipment. Its authorizing official may accept responsibility for operation OR for use of an external service. An agency authorization to use therefore need not mean that the agency operates the provider’s platform.',
  'The presence of an authorizing official does not prove government operation. The absence of a government operator does not prove that a system falls outside FISMA. The statutory classification and the authorization arrangement must each be supported, rather than inferred from the other.'
 ],[('fisma2014','§2, 44 USC 3554(a)(1)(A)(ii)'),('m-24-15','§IV, footnote 7')]),
 ('tenant-test','Information stewardship can remain with the agency',['steward'],[
  'This is the clearest practical distinction: the agency can set the permitted purpose, recipients, retention, and protection needs for its information while a private company runs the service. Its information owner and the service’s system owner need not be the same person.',
  'The agency can directly control accounts, sharing, exports, endpoint protection, and some tenant settings. For provider-managed functions, it may need agreed commitments, assurance evidence, technical safeguards, or limits on what information may enter the service. Those mechanisms allocate responsibility; they do not transfer operation of the whole platform.'
 ],[('a130-2016','Appendix I §4(j)(1)–(2)'),('sp800535','SA-9; AC-20; CA-3')]),
 ('separate-predicates','The difficult boundary is the work being supplied',['management','external','cui-outsourced'],[
  'Direct agency control is relevant, but NIST does not make it an absolute condition of authorization. Its management concept includes budgetary and programmatic authority, and it recognizes external systems outside direct control.',
  'The CUI rule goes further within its own scope: outsourced information-processing services can be systems operated on behalf of an agency, including systems with private customers. Selling a shared service and performing work on behalf of an agency are therefore not mutually exclusive under that rule.',
  'This does not settle the government-wide definition for every use of ordinary information. DHS’s 2023 response expressly declined to adopt the CUI definition as the general FISMA definition. But it prevents treating “commercial service” as an established categorical exclusion. The report distinguishes this unresolved classification issue from the agency’s independently stated information duties.'
 ],[('dhs2023','§II.B.7, 88 FR 40571'),('a130-2016','§10(23); Appendix I §5(r)')]),
]
DUTIES = [
 ('duty-contracts','1. Put the required protections into the arrangement',['contracts'],[
  'Actor: the agency. Trigger: contracts or other agreements involving the listed activities with federal information. This obligation reaches information handling; its text is not limited to a contract to operate an agency system.',
  'The agency must identify its security and privacy requirements and obtain terms sufficient to meet them. A normal subscription can leave the vendor in operational control, but the agency still has to determine whether the arrangement permits lawful use. This clause does not grant an agency unlimited power to rewrite a supplier’s business practices.'
 ],[]),
 ('duty-oversight','2. Apply the separate information-handling trigger',['oversight'],[
  'The word “or” matters. OMB covers systems used or operated on behalf of government OR systems that collect or maintain federal information on its behalf. Calling the provider’s platform nonfederal does not, by itself, answer whether this second trigger applies.',
  'The heading is “Non-Federal Entities.” That is a description of the counterparties, not a declaration that all of their systems are nonfederal. The following requirements attach to the systems described in this sentence. They should not be silently extended to unrelated corporate systems or every private recipient of public information.'
 ],[]),
 ('duty-access','3. Establish access oversight and verify protections',['access','controls'],[
  'Actor: the agency, for systems meeting §4(j)(2). The duties include access and vetting oversight and ensuring that controls are effective and comply with the stated requirements. Practical evidence can come from the provider, assessments, and the agreed service arrangements; the agency need not operate every control itself.',
  'This is stronger than a risk assessment alone. It also does not mean every private system receives an identical control set: the applicable standard, information, service, and agreement must be identified.'
 ],[('sp800372','Appendix G, pp. 159–160'),('sp800535','SA-9')]),
 ('duty-inventory','4. Inventory covered systems and document their connections',['inventory','interfaces','agreements'],[
  'Actor: the agency, when §4(j)(2) applies. The circular expressly requires inventory inclusion and documentation of interfaces, security requirements, and communicated information. The interface-agreement requirement concerns connections with agency-owned or operated systems.',
  'Inventory is not ownership. An agency can record a service it uses without taking control of its provider. These clauses nevertheless contradict a universal claim that externally handled information creates no system-level oversight duties.'
 ],[]),
 ('duty-incidents','5. Arrange incident response',['incidents'],[
  'Actor: the agency, for the covered systems. Establish response procedures and applicable reporting and notification timelines. The agency needs a workable route for learning about incidents and obtaining the information it must report; provider cooperation should be addressed in the arrangement.',
  'This quote does not prescribe one universal vendor reporting deadline. The relevant OMB guidance, information, incident, and contract determine the specific obligations.'
 ],[('usc3554','44 USC 3554(b)(7)')]),
 ('duty-incidental','6. Protect information even on incidental equipment',['incidental'],[
  'This sentence expressly locates continuing FISMA accountability in the information. It follows a discussion of contractor equipment acquired incidentally to a contract, which the Clinger–Cohen IT definition excluded.',
  'It supports the distinction you are investigating: excluding equipment from one statutory definition does not remove the agency’s information-protection duty. It does not say that the whole equipment environment becomes an agency system or that every safeguard for an agency system applies unchanged.'
 ],[('a130-2016','Appendix I §5(r), pp. 25–26'),('clinger','Division E §5002(3), now 40 USC 11101(6)')]),
]
# Topic, federal-system column, information-in-nonfederal column, limitation, references.
COMPARISON = [
 ('What triggers protection','Covered federal systems and their information fall within the agency security program.','The agency’s information duty can survive outside an agency-operated system.','Generally applicable agency duty; §3554(a)(1)(A) does not make every recipient an agency.', [('usc3554','§3554(a)(1)(A), (b)')]),
 ('Control of operations','The system owner and operator have defined lifecycle and implementation responsibilities.','The provider may retain platform operation; the agency governs its use and the information it provides.','Role allocation differs. Ownership, service purchase, and system classification are separate questions.', [('sp800372','Appendix D, pp. 114, 119, 123; Appendix G')]),
 ('Categorization and safeguards','FIPS 199/200 and applicable agency requirements guide categorization, minimum safeguards, and control selection.','Select protections for the information and actual arrangement. CUI, covered contract information, and privacy have additional triggers.','No universal lighter baseline for all nonfederal handling is established here. SP 800-171 is not the general ordinary-information baseline.', [('fips199','§§2–3'),('fips200','§§2–3'),('sp8001713','§1.1')]),
 ('Authorization','Agency-system authorization addresses the specified system, controls, and risk.','An agency may authorize use of an external service. That decision does not give it operational control of the provider.','Conditional: a FedRAMP-covered service has its own authorization obligations; a program exclusion is not an exemption from all duties.', [('sp800372','Appendix D, p. 114; Appendix G, p. 160'),('m-24-15','§§III–IV, footnote 7')]),
 ('Assessment and monitoring','The agency assesses controls and monitors the system under its applicable authorization process.','The agency must obtain sufficient assurance for its information and use. §4(j)(2)(b) expressly requires effective controls when its trigger is met.','External evidence and inherited controls can change who performs the work. They do not eliminate the agency’s accountability.', [('usc3554','§3554(a)(2)(D), (b)(5)'),('a130-2016','Appendix I §4(j)(2)(b)'),('sp800372','Appendix G')]),
 ('Inventory and interfaces','Agency inventory and system connections have specified management requirements.','§4(j)(2)(c)–(f) also covers systems collecting or maintaining information on behalf, including inventory and interface agreements.','Conditional on the wording of that provision. Not a finding that every private recipient’s system belongs in the agency inventory.', [('a130-2016','Appendix I §4(j)(2)(c)–(f)')]),
 ('Incident response','Agency detection, response, and reporting obligations apply to covered incidents.','Protecting information externally requires response arrangements; covered external systems have explicit procedures under §4(j)(2)(e).','The agency’s reporting duty and a supplier’s contractual notification duty are distinct.', [('usc3554','§3554(b)(7)'),('a130-2016','Appendix I §4(j)(2)(e)')]),
 ('CUI confidentiality','Under the CUI rule, on-behalf systems are treated as agency systems and can receive additional agency requirements.','The rule prohibits treating qualifying nonfederal systems as agency systems and directs SP 800-171 for CUI confidentiality, with exceptions.','A real difference, expressly scoped to CUI. Read the outsourcing definition, exceptions, and incorporated edition together.', [('cui2025','32 CFR 2002.14(h)(1)–(2); 2002.2'),('sp8001713','§1.1 and footnote 8')]),
 ('Retention, disclosure, and exit','The agency follows applicable records, disclosure, and disposal requirements.','Those information duties can remain when a private service holds copies. Arrange access, preservation, return, and lawful disposal.','Conditional on the particular information and law; not every company record becomes an agency record.', [('records2024','44 USC 3301'),('foia2024','5 USC 552(f)(2)(B)'),('records-cloud','Questions 6–8')]),
]
EXTRA = [
 ('nist-nonfederal','CUI: an express limit on treating private systems as agency systems',['cui-limit','cui-incidental'],[
  'These are binding regulatory words within the CUI program. They expressly distinguish the protection of information on a qualifying nonfederal system from treating that system as the agency’s own.',
  'The same paragraph directs agencies to SP 800-171 for CUI confidentiality, unless the listed authority prescribes specific safeguards or an agreement establishes protection above moderate confidentiality for CUI Basic. The preceding paragraph covers outsourced processing, including mixed public/private customer systems. Both sides of the rule must be retained.',
  'An entity receiving specifications to manufacture a product is different from an entity hired to process or host the agency’s records under this rule. “Incidental” describes the purpose of the receipt, not simply that the service is commercially available.'
 ],[('cui2025','32 CFR 2002.14(h)(1)–(2); 2002.4(hh)')]),
 ('nist-controls','SP 800-171 is a bounded branch, not a substitute for every external service',['scope171','components171','agreements171'],[
  'Revision 3 states that its requirements do not apply to organizations collecting or maintaining information on behalf of an agency, as well as those using or operating a system on its behalf. Footnote 8 directs those activities to FISMA. The information limb therefore cannot simply be assigned wholesale to SP 800-171.',
  'For the branch where SP 800-171 does apply, component scope and a separate security domain can limit implementation to CUI-handling and protecting components. The document focuses on CUI confidentiality; it is not a general exemption from other applicable laws or agreements.',
  'The collected 2025 CFR incorporates the June 2015 publication with January 2016 updates. Revision 3 is current NIST guidance in this review, not proof that every contract or regulation automatically adopted it. Identify the governing edition for the actual arrangement.'
 ],[('sp8001713','§1.1, footnote 8; §2'),('cui2025','32 CFR 2002.2(b)(5), 2002.14(h)(2)')]),
 ('nist-lineage','Cloud-program requirements can follow information handling',['clouds','fedramp-scope','fedramp-authorization'],[
  'M-24-15 uses information-handling verbs to set FedRAMP’s scope, subject to express exclusions. It does not limit that scope to services the government itself operates. Its footnote distinguishes agency authorization to use from authorization to operate.',
  'This is why service purchase versus delegated operation matters without resolving everything. An external service can remain provider-run and still require a specified assessment or authorization for agency use. The relevant offering is not automatically the provider’s entire company.',
  'Figma-style design work must be examined against the service, information, and exclusions. An agency application on IaaS requires separate analysis of the workload and the hosting service. The retrieved program guidance informs these decisions; it does not amend FISMA.'
 ],[('scope2026','Agency Use Case Indicators; Social Media & Communications; Single Agency Systems'),('m-24-15','§III exclusions')]),
 ('not-interchangeable','NIST also contains broad external-provider language',['external-requirements','exchange-risk'],[
  'The first passage is NIST’s description of FISMA and OMB policy, not statutory text. It is broader than a claim that external information handling requires only a risk acknowledgment. The second describes an alternative based on information-exchange risk in the same discussion.',
  'Read these passages with A-130’s actual triggers and the CUI rule’s express limits. “Same requirements” does not mean that unrelated corporate systems become federal systems, nor does a risk-based alternative waive a binding obligation. The report does not resolve these different scopes by silently choosing one quotation.'
 ],[('sp800372','Appendix G, pp. 159–160'),('a130-2016','Appendix I §4(j), §5(r)'),('cui2025','32 CFR 2002.14(h)')]),
]
EXTRA += [
 ('private-contract-duties','Additional duties need their own trigger',['fci','fci-duty','privacy'],[
  'Federal contract information: FAR 52.204-21 applies through the covered contract clause. Its definition excludes publicly released information and simple payment transactions. A company’s covered contractor system receives specified safeguards, not an automatic conversion of its entire business into an agency system.',
  'Personal information: Privacy Act subsection (m) has a specific trigger—contracting for operation of a system of records to accomplish an agency function. Not every document with a person’s name is such a system; subsection (a)(5) concerns records retrieved by an individual’s name or other identifying particular. Other privacy obligations may apply even where (m) does not.',
  'These provisions illustrate why an obligation matrix must name its authority and trigger. “Federal information” alone does not make every rule in every information regime applicable.'
 ],[('usc552a','5 USC 552a(a)(5), (b), (e), (m)'),('far5220421','FAR 52.204-21(a)–(c)')]),
 ('records-and-exit','Records duties follow qualifying records into a service',['records','foia'],[
  'NARA recognizes that agency control varies by service model and directs attention to negotiated responsibilities. Determine which content is a federal record, whether it remains accessible, how preservation and legal holds work, and how it will be returned or disposed of.',
  'The FOIA quotation is part of its definition of a record. It reaches qualifying information held under a government records-management contract; it does not turn every private company record into an agency record. Records status, access rights, and disclosure restrictions require their own analysis.'
 ],[('records2024','44 USC 3301'),('records-cloud','Questions 6–8'),('foia2024','5 USC 552(f)(2)(B)')]),
]
HISTORY_NOTE = [
 ('omb-distinction-quote','OMB expressly distinguished agency and contractor duties',['omb-history'],[
  'This 1993 explanation is strong evidence for distinguishing an agency’s obligations from a counterparty’s. It does not say private services cannot handle information on behalf of an agency. The later security, CUI, and cloud provisions must be read on their own terms.',
  'The selected chronology below preserves the relevant legislative and comment history. Comments express their authors’ positions; they are not adopted law. The incomplete 2015 comment docket remains a stated research gap.'
 ],[('a130-1996','Appendix IV, Government Information'),('a130-2000-app-iv','§3, Government Information')]),
]
ROLES.insert(1, (
 'agency-authorization','A federal decision maker does not become the platform operator',['federal-ao','fips-controls'],[
  'A-130 requires a senior Federal official to authorize operation. FIPS 200 imposes minimum-security requirements on agencies through control selection. These are concrete governance and safeguard requirements; a provider’s commercial status is not a substitute for analyzing their applicability.',
  'The role of the federal official is to make the agency’s authorization decision. NIST’s external-service model separately recognizes provider operation and agency authorization to use. The cited provisions do not establish that a system must have a pre-existing government-appointed system owner before it can meet the statutory system clause. Failure to assign a required role is not itself an exemption.',
  'For a purchased service, record the agency official who accepts the use risk, the provider accountable for service operation, the agency information owner, and the responsibilities the agreement actually grants. Do not describe an agency use authorization as operational control over a private company.'
 ],[('a130-2016','Appendix I §4(d)(1)–(8)'),('sp800372','Appendix D, p. 114; Appendix G, pp. 159–160'),('fips200','Announcement §§6, 8; standard §4')]))
# Keep the regulatory exceptions adjacent to the prohibition.
EXTRA[0][2].append('cui171')
