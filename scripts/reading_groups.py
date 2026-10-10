"""Navigation only: groups complete collected sections without changing source text."""
import json
from pathlib import Path
all_sections=json.loads((Path(__file__).resolve().parents[1]/'data/law/sections.json').read_text())
def ids(title,lo,hi):
 return [r['id'] for r in all_sections if r['title']==title and r['number'].isdigit() and lo<=int(r['number'])<=hi]
def group(slug,title,description,scope,sections):
 return dict(slug=slug,title=title,description=description,scope=scope,sections=sections)
READING_GROUPS=[
 group('security','Security programs and oversight','Read the security responsibilities of OMB, DHS, and agencies, followed by independent evaluations, incident response, and national security systems.','44 USC §§3551–3559 and the repealed predecessor entry',ids(44,3551,3559)+['44-3531-to-3549']),
 group('information-policy','Information policy and agency management','Read the Paperwork Reduction Act’s purposes, definitions, and assignments to OMB and agencies, including information privacy and security.','44 USC §§3501–3506',ids(44,3501,3506)),
 group('information-collection','Information collection, data, and public access','Continue through collection approvals, data inventories, public protections, reporting, and Chief Data Officers.','44 USC §§3507–3521',ids(44,3507,3521)+['44-3520A']),
 group('fedramp','Cloud services and FedRAMP','Read the cloud authorization provisions together, from definitions and program structure to assessments, agency responsibilities, and oversight.','44 USC §§3607–3616',ids(44,3607,3616)),
 group('operations','DHS and CISA operations','Read the connected authorities for cybersecurity operations, intrusion detection, agency defenses, and reporting.','Selected provisions of 6 USC',ids(6,650,1525)),
 group('standards','NIST and federal standards','Read NIST’s computer standards responsibilities alongside the authority for issuing federal information-system standards.','15 USC §§278g-3–278g-4; 40 USC §11331',['15-278g-3','15-278g-4','40-11331']),
 group('inspectors-general','Inspectors General','Read the establishment, duties, reporting powers, and authorities of Inspectors General and their coordinating council. The security-specific annual evaluation appears in the security reading.','Selected provisions of 5 USC chapter 4',ids(5,401,424)),
 group('privacy','Privacy and personal records','Read the Privacy Act’s requirements for records about individuals, including access, disclosure, safeguards, and remedies.','5 USC §552a',['5-552a']),
 group('it-management','IT investment and Chief Information Officers','Read the connected assignments for IT planning, acquisition, performance, resources, and agency Chief Information Officers.','Selected provisions of 40 USC',ids(40,11101,11319)),
 group('electronic-government','Electronic government and advisory committees','Read the Office of Electronic Government, CIO Council, funding, innovation, and reporting provisions, followed by the connected advisory-committee termination rule.','44 USC §§3601–3606; 5 USC §1013',ids(44,3601,3606)+['5-1013']),
 group('supply-chain','Acquisition and supply-chain security','Read the Federal Acquisition Security Council’s establishment and authorities, agency responsibilities, review procedures, and termination provision.','41 USC §§1321–1328',ids(41,1321,1328)),
 group('statistics','Statistical data and confidentiality','Read chapter 35’s statistical-policy provisions, confidential-information protections, and rules for access to data assets.','44 USC §§3561–3583',ids(44,3561,3583)),
]
# Keep Code order within the PRA reading, including its lettered section.
READING_GROUPS[2]['sections']=[r['id'] for r in all_sections if r['id'] in READING_GROUPS[2]['sections']]
