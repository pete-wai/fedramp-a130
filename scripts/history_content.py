"""Reviewed narrative. Excerpts live separately and are checked against originals."""
TITLE='Protecting federal information and systems'
DECK='What Congress required, what OMB directed, and how NIST turned those duties into standards and guidance. A source-led history from 2000 to 2026, with the earlier foundations.'
ERAS=[('foundations','Before 2000','The information duty came first'),('early','2000–2004','Two duties, then a standards program'),('standards','2005–2009','Controls, boundaries, and external services'),('services','2010–2013','Purchased services and continuing oversight'),('split','2014–2016','The statutory continuity and the CUI split'),('risk','2018–2021','Information owners, external systems, and exchanges'),('current','2022–2026','Cloud legislation and current guidance')]
EVENTS=[]
def event(id,era,date,kind,title,summary,origin,change,quotes,edition=''):
    EVENTS.append(dict(id=id,era=era,date=date,kind=kind,title=title,summary=summary,origin=origin,change=change,quotes=quotes,edition=edition))

event('pra-foundation','foundations','1980','Law','PRA: give OMB responsibility for information policy',
'The Paperwork Reduction Act gave OMB an information-management role that included security. The quoted duty belongs to OMB’s Director. Its object is information collected or maintained by or on behalf of agencies.',
'Congress assigned the policy function in the PRA. OMB later identified the PRA as the authority behind A-130.',
'This is an early information-based duty. It does not depend on the government owning the equipment that holds the information.', ['pra-omb'])
event('csa-foundation','foundations','1988','Law','The Computer Security Act includes processing services',
'The Computer Security Act of 1987 was enacted on January 8, 1988. Its definition joined system operation to processing information for a federal function. It also assigned standards work to the National Bureau of Standards, later renamed NIST.',
'Congress directed the Bureau to develop standards and send them to Commerce for promulgation. The Act also required agency security plans and training (§§5–6).',
'Private operation was already within the statutory definition in specified circumstances. “On behalf of” did not start with cloud computing or FISMA.', ['csa-definition','csa-standards'])
event('a130-1993-history','foundations','1993','OMB policy','A-130 explains its PRA roots—and the role of agreements',
'OMB’s 1993 revision focused on information management, dissemination, and records. Its explanatory appendix cautioned that agencies’ information responsibilities were not automatically identical to those of grantees and contractors.',
'The notice expressly says OMB issued the original 1985 circular to fulfill its PRA responsibilities. The second quotation is OMB’s analysis of “Government Information,” not a later FISMA exemption.',
'Agency duties could be carried into grants and contracts. Read this historically: later security statutes and policies added requirements, and the 2016 circular replaced this edition.', ['a93-authority','a93-contract'])
event('pra-1995-history','foundations','1995','Law','PRA: agencies must protect information “by or for” them',
'The 1995 PRA restated agency responsibilities. Section 3506(g) combined compliance, accountability, and protection proportionate to risk. It expressly referred to the Computer Security Act.',
'This is Congress’s agency-level duty, separate from the Director’s policy role quoted above.',
'Notice the different phrases: paragraph (1) says “by or for the agency”; paragraph (3) says “by or on behalf of an agency.” Both concern information. Later amendments changed the cross-references; this is the 1995 enactment.', ['pra-agencies'])
event('a130-1996-history','foundations','1996','OMB policy','A-130 requires risk-based protection, not one method of analysis',
'A-130 §8(a)(1)(g) directed agencies to protect government information in proportion to risk. The revised security appendix also addressed system plans, controls, reviews, and authorization.',
'In its response to public comments, OMB linked risk-based controls to the Computer Security Act. Some commenters opposed removing formal risk analyses; others found them too costly.',
'OMB kept risk assessment essential while declining to require a formal risk analysis for every system. Risk-based judgment concerned how to meet the duty; it did not remove the duty.', ['a96-risk','a96-response'])
event('gisra-2000','early','2000','Law','GISRA makes security an agency-wide program',
'The Government Information Security Reform provisions required protections for information and systems supporting agency operations. They also required an agency-wide program, periodic assessments, testing, and independent evaluation.',
'Congress enacted these provisions in the FY2001 defense authorization law, Public Law 106–398. Former 44 USC 3534 supplied the agency duties; §3535 supplied independent evaluations.',
'The law quoted here uses “information collected or maintained by or for the agency.” It predates the two separately numbered objects of protection in FISMA 2002. The temporary GISRA framework was followed by FISMA.', ['gisra-duty'])
event('a130-2000-history','early','2000','OMB policy','The 2000 A-130 revision chiefly implements Clinger–Cohen',
'The 2000 revision addressed IT investment and management. Its existing security appendix also explained how agencies should decide whether to interconnect systems.',
'The final notice expressly identifies Clinger–Cohen as the reason for this revision. Its timing near GISRA does not establish that GISRA caused the revision.',
'Information moving between systems already called for safeguards and a management decision about risk. This is a connection decision, not a statement that every connected system becomes an agency system.', ['a00-origin','a00-connections'])
event('fisma-2002-history','early','2002','Law','FISMA writes the two duties side by side',
'The December 2002 Federal Information Security Management Act required agency heads to protect two things: information collected or maintained by or on behalf of the agency, and systems used or operated by the agency or for it. The same risk standard governs both.',
'Title III of the E-Government Act, Public Law 107–347, enacted former 44 USC 3544. November’s Homeland Security Act also contained FISMA provisions; this report quotes the December enactment that supplied this framework.',
'The agency-wide program expressly includes information and systems provided or managed by another agency, a contractor, or another source. The statute does not say “only the components the agency directly controls.” Nor does it define every external service as a federal system.', ['f02-dual','f02-program'])
event('nist-mandate-2002','early','2002','Law','Congress sends work directly to NIST and Commerce',
'FISMA did more than tell OMB to issue policy. It directly assigned NIST standards and guideline work and set deadlines for categorization standards, mapping guidance, and minimum requirements.',
'FISMA §303 amended the NIST Act. Section 302 amended 40 USC 11331 on Commerce’s prescription of standards. NIST develops; Commerce approves binding standards under the statutory process.',
'This is why the history is not simply law → OMB → NIST. There is also a direct law → NIST/Commerce path. FIPS 199, SP 800-60, and FIPS 200 identify themselves as responses to the assigned tasks.', ['f02-nist','f02-categories','f02-deliver','f02-binding'])
event('omb-2003-2004','early','2003–2004','OMB policy','OMB explains incidental equipment and NIST’s role',
'OMB’s first FISMA reporting instructions already said an agency remained responsible for federal information used on incidentally acquired equipment. In 2004, OMB also distinguished mandatory FIPS from NIST guidance.',
'M-03-19 and M-04-25 implemented FISMA reporting and interpretation. They referred agencies to A-130 Appendix III for appropriate controls.',
'An equipment exclusion in procurement law did not erase information-security responsibility. The 2004 answer also cautions against treating every sentence in a NIST publication as if it had the same status as a FIPS requirement.', ['omb03-incidental','omb04-nist'])
event('fips199-2004','early','2004','Mandatory standard','FIPS 199: categorize information and systems',
'FIPS 199 supplies low, moderate, and high impact categories for confidentiality, integrity, and availability. The impact of losing information helps determine the protection a system needs.',
'The standard explicitly identifies FISMA’s first task: categorization. Its applicability section distinguishes information from federal information systems and states the classified-information and national-security-system exceptions.',
'Categorization is a required input to decisions. It does not itself choose every control or decide whether an external system operates on an agency’s behalf.', ['f199-origin','f199-scope'])
event('rmf-2004','early','2004','NIST guidance','SP 800-37: evidence for an authorization decision',
'The first SP 800-37 explained security certification and accreditation. Certification assessed controls; accreditation was a senior official’s decision to authorize operation and accept the resulting risk.',
'The publication cites its FISMA responsibilities and says it is consistent with A-130 §8(b)(3). It expressly attributes the accreditation requirement to A-130 Appendix III.',
'This connects statutory responsibility and OMB policy to a practical system-level decision. Risk acceptance follows evidence about controls; it is not permission to disregard applicable requirements.', ['rmf04-authority','rmf04-authorization'])
event('types-2004','early','2004','NIST guidance','SP 800-60: map information types to impact categories',
'The second FISMA task was guidance on which information and systems belong in each category. SP 800-60 provided a method and provisional impact levels for information types.',
'Its executive summary explicitly says it responds to the second task and assumes familiarity with FIPS 199.',
'The information and the system are linked: the system’s use, connectivity, and aggregate information content inform its category. The mapping is a starting point to review, not an automatic answer for every agency.', ['types04'])
event('controls-2005','standards','2005','NIST guidance','SP 800-53: outsourced services have control obligations',
'The first SP 800-53 supplied a catalog and baselines of controls. SA-9 addressed outsourced information-system services and required the organization to monitor compliance.',
'This was part of NIST’s FISMA standards-and-guidelines work. The following year, FIPS 200 expressly required control selection using SP 800-53.',
'The original SA-9 guidance described the same control and documentation requirements as internal systems. That wording matters historically; later editions describe external services and trust in more detail.', ['sa9-2005'])
event('fips200-2006','standards','2006','Mandatory standard','FIPS 200: use the impact category to select controls',
'FIPS 200 established minimum security requirements. Agencies meet them through appropriately tailored SP 800-53 baselines, using the FIPS 199 categorization.',
'The standard’s announcement identifies FISMA as its authority and Commerce as the approving authority. Section 4 explicitly connects FIPS 199 to SP 800-53; footnote 5 calls for the current SP 800-53, as amended.',
'Risk assessment and tailoring are part of compliance. They do not turn minimum requirements into optional advice. FIPS 200’s applicability covers federal information and federal systems, with stated exceptions; the standard does not declare every private system federal.', ['f200-select'])
event('plans-2006','standards','2006','NIST guidance','SP 800-18 Revision 1: define the system being planned for',
'The system-security-plan guide tells agencies to categorize the system and its information before drawing boundaries and selecting controls. A boundary identifies the resources covered by the plan.',
'The revision connects system planning to FIPS 199 and the SP 800-53 baseline process.',
'“Direct management control” is a guide for grouping resources. The text expressly allows intervening management. It is not a statutory test that excludes every resource an agency cannot administer directly.', ['plan06-boundary'])
event('external-2006-2007','standards','2006–2007','NIST guidance','SP 800-53 Revisions 1 and 2: outside the boundary still matters',
'SA-9 changed from “Outsourced” to “External Information System Services.” Its explanation covered services used by a system but outside its accreditation boundary, including several forms of business relationship.',
'These are revisions of the control catalog used through FIPS 200. The two quotations below are from Revision 1 and Revision 2 respectively.',
'The quoted passages are identical in the collected editions. The important distinction is between the authorization boundary and responsibility for risks arising from an external service. Being outside the boundary does not end that responsibility.', ['sa9-2006','sa9-2007'])
event('types-2008','standards','2008','NIST guidance','SP 800-60 Revision 1 keeps information as the basis for categorization',
'The revised mapping guide still starts with information types and their consequences. It retains the explicit link to FISMA’s second task and FIPS 199.',
'This updates the 2004 mapping guidance. The excerpt shows the retained method rather than a new rule for outsourcing.',
'The reference to the system’s use, connectivity, and aggregate information content remains. This edition does not replace the separate legal inquiry about who uses or operates a system and for what purpose.', ['types08'])
event('controls-2009','standards','2009 / updated 2010','NIST guidance','SP 800-53 Revision 3 makes oversight roles explicit',
'SA-9 now lists three duties: require compliant controls, document government oversight and user roles, and monitor the provider’s compliance.',
'This continues the external-services control in Revisions 1 and 2. The catalog supports the FIPS 200 control-selection process.',
'The control text makes the oversight allocation explicit. The saved Revision 3 PDF incorporates an August 2010 update, so this quotation is evidence for that edition, not proof of the precise day each word first appeared.', ['sa9-2009'],'Revision 3 first published August 2009; saved file identifies August 2010 updates and includes an archive cover.')
event('rmf-2010','services','2010','NIST guidance','SP 800-37 Revision 1 extends the risk framework across the life cycle',
'The revised guide organized categorization, control selection, implementation, assessment, authorization, and monitoring into the Risk Management Framework. Its discussion of complex systems expressly addresses external subsystems.',
'The passage cites SP 800-53 Appendix I, “Security Controls in External Environments,” and attributes its requirement to FISMA and OMB policy.',
'NIST applies federal security requirements to external subsystems handling federal information and their associated services. Its surrounding discussion acknowledges limited direct control and the need for evidence and trust. This wording predates the 2016 A-130 revision.', ['rmf10-external'])
event('omb-2010','services','2010','OMB policy','OMB expressly includes subscribed and outsourced services',
'The FY2010 instructions connect FISMA’s agency-program requirement to fully or partly provided services, expressly including software as a service. They separately retain agency accountability for information on incidental equipment.',
'M-10-15 questions 36–38 interpret the existing FISMA framework and refer back to A-130 and NIST. This extends the earlier reporting guidance into more explicit service language.',
'The historical instruction to use “identical, not equivalent” procedures is particularly strong. It belongs to these 2010 instructions. Later FedRAMP policy provides reuse and authorization paths; do not treat this sentence alone as the complete current process.', ['omb10-services','omb10-incidental','omb10-contract'])
event('records-2010','services','2010','Guidance','Records obligations also follow information into a service',
'NARA explained that records-management responsibilities need to be addressed in cloud contracts. Information security does not replace recordkeeping, retention, access, or lawful disposal.',
'NARA Bulletin 2010-05 applies records-management responsibilities to cloud environments. This is a related information-management stream, not the origin of FISMA or the RMF.',
'An agency can retain records responsibilities even when another organization supplies the service. The security authorization alone does not settle those duties.', ['records10'])
event('cloud-2011','services','2011','OMB policy','FedRAMP provides a common assessment and authorization process',
'OMB’s December memorandum established FedRAMP policy for agencies procuring cloud services. Its scope expressly included commercial and non-commercial services, public and other deployment models, and the principal service models.',
'The memorandum built a reusable approach around existing FISMA and NIST requirements. NIST SP 800-144 separately explained why security and privacy accountability remains with the agency.',
'A shared service and an external operator did not, by themselves, remove the service from the policy. The memorandum contained a specific on-premises, agency-only private-cloud exception; that exception still required FISMA and NIST compliance.', ['fedramp11','cloud11-accountability'])
event('controls-2013','services','2013 / updated 2015','NIST guidance','SP 800-53 Revision 4 ties external services to federal requirements',
'SA-9 again distinguishes the service from the organizational system’s authorization boundary. It expressly covers providers processing, storing, or transmitting federal information, or operating systems for the government.',
'The guidance states its connection to FISMA and OMB policy. Revision 4 also brought privacy controls into the catalog.',
'The requirement is not limited to systems inside an agency-drawn boundary. The organization must establish what the external service protects and how compliance will be monitored. This is guidance about applying duties, not a new act of Congress.', ['sa9-2013'],'Revision 4 published April 2013; this saved PDF includes updates through January 22, 2015.')
event('monitoring-2013','services','2013','OMB policy','OMB requires a strategy for continuing authorization and monitoring',
'M-14-03 directed agencies to implement continuous monitoring of controls in phases through FY2017. The strategy had to address ongoing authorizations and environments of operation.',
'The memorandum explicitly cites the RMF and NIST guidance, including SP 800-37, 800-39, 800-53, 800-53A, and 800-137.',
'The management task continues after initial approval. Agencies need a way to learn about changing risks and control performance, including where they rely on shared controls.', ['omb13-monitor'])
event('rmf-2014-update','split','June 2014','NIST guidance','The RMF update retains its external-services wording',
'The June update to SP 800-37 Revision 1 retained the passage about external providers, subsystems, and associated services.',
'The original February 2010 text and the June 2014 updated edition are preserved separately. Their quoted passages match.',
'This update preceded the December 2014 FISMA law. It cannot be described as implementing that later enactment.', ['rmf14-external'])
event('fisma-2014-history','split','December 2014','Law','FISMA modernization retains the two objects of protection',
'The Federal Information Security Modernization Act of 2014 retained the information/system distinction in 44 USC 3554. Compare the first quotation with 2002: the shared duty and both objects have the same wording.',
'Public Law 113–283 replaced the prior subchapter and revised federal oversight and operational responsibilities, including OMB and DHS roles. The quoted agency provisions are §§3554(a) and (b).',
'Agencies must assess harm, determine appropriate security, implement risk-reducing policies, and test controls. The agency-wide program still includes externally provided or managed information and systems. Risk management and compliance are concurrent duties.', ['f14-dual','f14-implement','f14-program'])
event('cui-2015','split','2015','NIST guidance','SP 800-171 creates a tailored path for CUI in nonfederal systems',
'SP 800-171 addressed the confidentiality of controlled unclassified information held in qualifying nonfederal systems. CUI is information requiring safeguards under a law, regulation, or government-wide policy; it is not a synonym for all federal information.',
'The publication was developed for the CUI program established by Executive Order 13556. Its requirements were derived from federal standards and SP 800-53, tailored for this narrower setting. The 2015 text referred to a proposed CUI rule.',
'The distinction was already express: the main scope excluded systems used or operated for agencies, while footnote 8 also excluded organizations collecting or maintaining information for them. Read the footnote with the main text. SP 800-171 was never a general substitute for federal-system requirements.', ['cui15-scope','cui15-footnote','cui15-tailor'],'June 2015 publication; saved PDF incorporates January 2016 updates. Do not read its references to a proposed rule as final 2016 rule text.')
event('a130-2016-history','split','July 2016','OMB policy','A-130 separates definitions and spells out agency oversight',
'The revised circular defines federal information with lifecycle verbs and federal information systems with use/operation language. Appendix I then addresses agreements and oversight of non-federal entities.',
'Section 9 cites the PRA, E-Government Act, FISMA 2014, Clinger–Cohen, and other authorities. Appendix I §5(r) expressly explains FISMA applicability; §4(j) gives the operative agency directions.',
'Section 4(j)(1) covers agreements involving the lifecycle of federal information. Section 4(j)(2) has an “or”: systems used or operated for government, OR systems collecting or maintaining federal information for it. Its oversight duties include controls, inventory, interfaces, access, and incident response. An information-handling arrangement can therefore trigger more than a general instruction to understand risk.', ['a16-definitions','a16-contracts','a16-oversight','a16-incidents','a16-applicability','a16-incidental','a16-ato'])
event('cui-2016-rule','split','September–November 2016','Regulation','The CUI rule states an explicit federal/nonfederal split',
'NARA’s final rule distinguishes systems operated for an agency from other nonfederal systems holding CUI. The first category includes outsourced processing services, even when the system serves both government and private users.',
'The rule implements Executive Order 13556 and incorporates FIPS 199, FIPS 200, SP 800-53, and SP 800-171. It was published September 14 and effective November 14, 2016.',
'For qualifying nonfederal systems, the rule prohibits treating them as agency systems and directs agencies to use SP 800-171 for CUI confidentiality, with stated exceptions. Its incidental-handling language expressly excludes processing services from that example. This is a scoped CUI rule, not a blanket exemption for commercial systems.', ['cui16-federal','cui16-nonfederal','nara16-comments'])
event('cui-2016-revision','split','December 2016 / updated 2018','NIST guidance','SP 800-171 Revision 1 makes both exclusions explicit in the main scope',
'Revision 1’s scope says both “not collecting or maintaining information” for an agency and not using or operating a system for one. The earlier edition put the information condition in a footnote; the revised main paragraph makes it visible.',
'The revision responds to the now-final CUI framework and continues the FIPS/SP 800-53 tailoring approach.',
'Compared with the collected 2015 edition, Revision 1 also includes requirement 3.12.4 on system security plans. A nonfederal system can have a documented plan and connections without becoming an agency system. The applicable authority and agreement determine the obligation.', ['cui16-revision','cui16-plans'],'The quoted Revision 1 file includes updates through June 7, 2018. Intermediate 2017/2018 update wording is not separately reconstructed here.')
event('rmf-2018','risk','2018','NIST guidance','SP 800-37 Revision 2 distinguishes information stewardship from system ownership',
'The revised RMF integrates security and privacy and adds organizational preparation. Its role descriptions make a useful distinction: the information owner retains protection responsibilities when sharing information, while the authorizing official can authorize use of an external service.',
'The publication cites FISMA 2014 and the 2016 A-130. Appendix G continues the external-provider discussion from the earlier RMF and control catalog.',
'NIST pairs a strong statement about applicable requirements with practical risk responses where direct control is limited. “Authorization to use” and an acceptable exchange risk do not make statutory or policy requirements disappear. They describe how the agency decides whether to rely on the service.', ['rmf18-steward','rmf18-ao','rmf18-external','rmf18-risk'])
event('cui-2020','risk','2020 / updated 2021','NIST guidance','SP 800-171 Revision 2 explains agreements and bounded protection',
'The front matter states when these recommended requirements apply to a nonfederal organization: when an agency mandates them in a contract, grant, or other agreement. The scope remains CUI confidentiality in qualifying nonfederal systems.',
'Revision 2 continues the CUI rule and SP 800-53-based approach. Its §1.1 retains the information-handling and system-operation exclusions.',
'The publication expressly permits a separate CUI security domain to limit the components that must satisfy these requirements. That is a concrete scoping provision. It is not a rule limiting all FISMA duties to an agency-controlled tenant.', ['cui20-agreement','cui20-boundary'],'February 2020 edition, including January 28, 2021 updates; later withdrawal cover is retained.')
event('controls-2020','risk','2020','NIST guidance','SP 800-53 Revision 5: controls for organizations and services',
'Revision 5’s SA-9 requires external providers to meet organizational security and privacy requirements, documents oversight roles, and calls for ongoing monitoring. Its discussion expressly contemplates that the organization has no direct control over implementation or assessment.',
'Revision 5 is the successor control catalog. Baselines moved to the companion SP 800-53B; FIPS 200 continues to connect federal minimum requirements to control selection.',
'The catalog supports federal and nonfederal uses. A control’s presence in it is not, by itself, proof that every private company must implement it. Selection, applicable law and policy, and agreements supply that link.', ['sa9-2020'],'September 2020 publication, including December 10, 2020 updates. Later release changes are addressed below.')
event('exchanges-2021','risk','2021','NIST guidance','SP 800-47 Revision 1 centers the information exchange',
'The revised guide addresses information before, during, and after an exchange. It is technology-neutral and applies across different organizations or different authorization boundaries within one organization.',
'It expands the earlier interconnection-security focus into management of information exchanges. Its guidance complements the RMF and A-130’s interface and agreement duties.',
'Protecting exchanged information and authorizing the systems are related but distinct work. Participating organizations need to identify risks, required protections, responsible officials, and suitable agreements. Connectivity alone does not decide whether one organization operates for another.', ['exchange21','exchange21-scope'])
event('fedramp-2022','current','2022','Law','Congress codifies FedRAMP and directs OMB to define its scope',
'The FedRAMP Authorization Act establishes a reusable assessment and authorization program for cloud products and services processing unclassified information used by agencies. It imports A-130’s definitions of federal information and authorization to operate.',
'Public Law 117–263 §5921 adds 44 USC 3607–3616. Section 3614 specifically directs OMB to issue scope and authorization guidance.',
'The statute’s reference to services operated as federal information systems must be read with OMB’s ensuing scope policy. Reusing a FedRAMP package also does not remove an agency’s FISMA responsibility: §3613(e)(2) preserves it expressly.', ['act22-definitions','act22-program','act22-omb','act22-duty'])
event('dhs-2023','current','2023','Comment response','DHS declines to adopt NARA’s definition for all of its FISMA rule',
'Public comments on DHS’s safeguarding rule questioned how it distinguished federal and nonfederal systems and how it used “on behalf of an agency.” DHS intentionally declined to import the CUI rule’s definition.',
'This is DHS’s response in the final-rule preamble, 88 FR 40571. The agency argued that a general FISMA definition should come from OMB after interagency coordination.',
'The response is evidence of an unresolved difference in agency interpretation. It does not repeal NARA’s CUI rule, supply a court holding, or establish a universal commercial-service exemption. Its immediate context is DHS acquisition rules.', ['dhs23-response'])
event('cui-2024','current','May 2024','NIST guidance','SP 800-171 Revision 3 retains the narrower scope',
'Revision 3 continues to exclude organizations collecting or maintaining information for an agency, or using or operating its systems. Its requirements apply to components handling CUI or protecting those components and are intended for agreements with agencies.',
'The revision updates the requirements using the SP 800-53 Revision 5 catalog. NIST’s February 2024 public-comment analysis discusses alignment with source controls and tailoring for CUI confidentiality.',
'This is the current final SP 800-171 edition checked for this report. The component limit is express. The publication’s information-handling exclusion is equally express; neither should be omitted when deciding whether this is the right requirements set.', ['cui24-scope'])
event('omb-2024','current','July 2024','OMB policy','OMB defines FedRAMP scope using information-handling verbs',
'M-24-15 describes in-scope cloud products and services as those creating, collecting, processing, storing, or maintaining federal information for an agency, subject to the memorandum’s exclusions.',
'The memorandum implements the FedRAMP Authorization Act and replaces the 2011 cloud authorization memorandum. The statute directed OMB to specify the categories and characteristics in scope.',
'FedRAMP scope is a program decision with express exclusions, not a universal definition for every law. Agencies use the package for their own authorization to operate or use; other information-management, privacy, records, and security duties remain.', ['omb24-scope','omb24-exclusions','omb24-atu'])
event('controls-2025','current','2025','NIST guidance','SP 800-53 Release 5.2.0 updates controls without replacing the basic framework',
'The August release targets software updates, patches, development, and resilience. Its official change list identifies the affected controls and assessment procedures.',
'NIST explicitly attributes this release to Executive Order 14306. This is a different authority link from FISMA’s original instruction to develop the catalog.',
'The release does not amend FISMA or A-130. The checked change list does not revise SA-9; the discussion above quotes the preserved 2020 catalog. SP 800-53B’s release number changed for consistency, with no baseline changes in this release.', ['release25'])
event('plans-2026','current','2026','NIST guidance','SP 800-18 Revision 2 puts data flows into system plans',
'The June revision combines planning guidance for security, privacy, and cybersecurity supply-chain risk. It says plans should describe the data lifecycle, responsible people, components and flows, and risks from information shared outside the system.',
'Its executive summary explicitly connects the planning duty to A-130 and its planning activities to SP 800-37. Its authority statement cites FISMA 2014.',
'The latest planning guide still treats information and systems together without making their boundaries identical. Nonfederal organizations may use this guide voluntarily; a separate legal, policy, or agreement requirement must be identified where its use is compulsory.', ['plans26','plans26-origin'])

RELATIONSHIPS=[
('PRA → A-130','implements','OMB says it issued A-130 to fulfill the PRA responsibilities.','a93-authority'),
('FISMA → NIST / Commerce','requires','Congress assigns standards work and directs submission to Commerce.','f02-deliver'),
('FISMA → FIPS 199','implements','FIPS 199 identifies the first statutory task it addresses.','f199-origin'),
('FISMA → SP 800-60','implements','The mapping guide identifies the second task.','types04'),
('FIPS 200 → SP 800-53','incorporates','The standard requires selection using the control catalog.','f200-select'),
('A-130 → SP 800-37','implements','NIST attributes the authorization requirement to A-130.','rmf04-authorization'),
('SP 800-53 → SP 800-37','cites','The 2010 RMF cites the catalog’s external-environment appendix.','rmf10-external'),
('CUI rule → SP 800-171','incorporates','The rule directs use of 800-171 for qualifying nonfederal CUI confidentiality.','cui16-nonfederal'),
('SP 800-53 → SP 800-171','derived from','NIST describes tailoring requirements from the federal standards and guidelines.','cui15-tailor'),
('FedRAMP Act → A-130 definitions','incorporates','Congress imports two definitions from the circular.','act22-definitions'),
('FedRAMP Act → OMB scope policy','requires','Congress directs OMB to specify program scope.','act22-omb'),
('A-130 → SP 800-18 Revision 2','implements','The planning guide identifies A-130’s system-plan requirement.','plans26-origin'),
('Records guidance ↔ cloud security','related context','Records duties coexist with security duties; this is not a claimed chain of authority.','records10')]

COMPARISONS=[
('What must be protected?','Information collected or maintained by or on behalf of the agency, with protections proportionate to harm.','Systems used or operated by the agency or by another organization on its behalf, under the same statutory risk standard.','f14-dual'),
('What does the agency have to do?','Assess harm, determine needed protection, implement risk-reducing policies, test controls, and carry applicable security and privacy duties into agreements.','Include covered systems in the agency program; categorize, select and assess controls, authorize, and monitor under the applicable standards and policy.','f14-implement'),
('What if another organization handles the information?','A-130 §4(j)(1) requires suitable terms in lifecycle agreements. Section 4(j)(2) also reaches systems that collect or maintain federal information on behalf of government.','The same §4(j)(2) covers systems used or operated on behalf of government. Its listed oversight duties include controls, inventory, access, interfaces, and incident response.','a16-oversight'),
('What changes for qualifying nonfederal CUI systems?','The CUI rule directs confidentiality requirements through SP 800-171, with its exceptions. Requirements apply to relevant components, including components protecting the CUI.','The CUI rule treats systems operated for the agency as agency systems and allows the agency’s additional internal requirements. It explicitly includes outsourced processing for mixed users.','cui16-nonfederal'),
('Who accepts the risk?','The information owner or steward retains responsibility for appropriate use and protection when information is shared.','The authorizing official may authorize system operation, common controls, or use of an external system, service, or application.','rmf18-steward'),
('Does a boundary settle the legal scope?','No. Information can leave a system boundary while protection and agreement duties continue.','No. An external service may be outside one authorization boundary while still subject to applicable controls, assurance, and oversight.','sa9-2020')]

COVERAGE=[
('Law','PRA 1980/1995; Computer Security Act; GISRA 2000; FISMA 2002/2014; FedRAMP Act 2022','Original enactments quoted. Current-code cross-check uses the existing OLRC release 119-118 through September 30, 2026. No claim that all intervening amendments or later October enactments were exhaustively checked.'),
('A-130','1985 origin; 1993, 1996, 2000, 2016','1985 origin is quoted from OMB’s 1993 explanation. Earlier notices and original circulars remain in the main library. The 2016 circular remains the listed current circular checked October 25; not every proposed draft or comment is recovered.'),
('OMB instructions','2003, 2004, 2010, 2011, 2013, 2024','Selected instructions establish the relevant interpretation and program changes. The larger site contains the broader memorandum search; this report is not a quote-by-quote comparison of every annual FISMA reporting memorandum.'),
('FIPS','199 (2004), 200 (2006)','Both directly quoted. The report distinguishes mandatory standards from supporting NIST guidance. Specialized cryptography and identity FIPS are outside this scope.'),
('SP 800-37','2004; Revision 1 original 2010 and June 2014 update; Revision 2 (2018)','Original and updated Revision 1 files compared. Quoted external-service wording is unchanged. Revision 2 is the current final edition checked; drafts do not replace it.'),
('SP 800-53','2005; Revisions 1 (2006), 2 (2007), 3 (2009/2010), 4 (2013/2015), 5 (2020); Release 5.2.0 (2025)','SA-9 and its context are compared. Saved Revision 3/4/5 files include later updates. This does not establish the first appearance of every changed word. The 2025 change list is preserved; it does not change SA-9. Intermediate maintenance releases are not reconstructed individually.'),
('SP 800-60','2004 and Revision 1 (2008), Volume I','The statutory connection and method are quoted from both editions. The many category-specific mappings in Volume II are outside this report’s comparison.'),
('SP 800-171','2015 with January 2016 updates; Revision 1 with June 2018 updates; Revision 2 with January 2021 updates; Revision 3 (2024)','Scope, information/system exclusions, agreement triggers, component scoping, and planning are compared. Intermediate corrections are not all separate milestones. Revision 3 is the current final publication checked.'),
('Other NIST guidance','SP 800-18 Revision 1 (2006) and Revision 2 (2026); SP 800-144 (2011); SP 800-47 Revision 1 (2021)','Selected for boundary, service, exchange, and planning questions. This is not a complete history of every NIST risk, assessment, privacy, or supply-chain publication.'),
('Regulations and public comments','NARA final rule and responses (2016); DHS final-rule response (2023); OMB 1996 response; NIST 2024 comment analysis','Government responses are quoted in their own context. The full A-130 2015 comment docket was not recovered. The retained EPIC and RAND submissions are examples of comments in the archive, not representative of all commenters or adopted policy.'),
('Research method','Inforegs original-source archive plus official web publications','Inforegs semantic indexing was complete when checked. Search results guided discovery; quotations were checked against originals. A complete index is not proof that the archive contains every relevant authority. Research and editorial review were self-review, not independent legal review.')]
