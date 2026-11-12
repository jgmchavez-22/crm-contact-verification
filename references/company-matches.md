# Company-match guidance (counts as "still employed", not Resigned)

When the LinkedIn current employer differs from the CRM company name, decide whether
they are the SAME organization. Count these as a match (tag Yes/continue, add a comment):

## Parent / subsidiary / brand (a division of the CRM company)
- DNA Plc  ->  Telenor Group
- Albert Heijn / Etos / Gall&Gall  ->  Ahold Delhaize
- R.D.M. Arnsberg GmbH  ->  RdM Group
- Buhler Alzenau GmbH  ->  Buhler
- Liebherr Components Biberach / Liebherr EMtec  ->  Liebherr Group
- KIRCHHOFF Automotive  ->  KIRCHHOFF Group
- PassionFroid  ->  Groupe Pomona   (emails at @passionfroid.fr)
- Kingspan Light + Air  ->  Kingspan Group
- Orientis  ->  Kusmi Tea (parent)
- Fisher Clinical Services  ->  Thermo Fisher (emails @thermofisher.com)
- ITM Equipement de la Maison  ->  Les Mousquetaires (emails @mousquetaires.com)

## Renamed / rebranded companies (same entity, new name)
- Telecom New Zealand  ->  Spark New Zealand (renamed 2014)
- Infigen Energy  ->  Iberdrola Australia (acquired/rebranded; new domain iberdrola.com.au)
- Dako  ->  Agilent Technologies (acquired; emails @agilent.com)
- Sunderland College  ->  Education Partnership North East
- thyssenkrupp nucera  ->  part of thyssenkrupp

## Company SPLITS create SEPARATE companies -> if CRM says one and they are at the
## other, that is RESIGNED
- TechnipFMC  vs  Technip Energies  (split 2021 - different companies)

## Government departments (esp. AU) merge/rename frequently
- The email-domain cluster can confirm: e.g. education.gov.au routed via
  employment.gov.au MX means the same government cluster.

## Legacy email domains
A contact may still be employed but their CRM email uses an old/acquired domain that now
bounces or greylists. Search for the current company domain and re-derive the address
(e.g. mat.beynon@infigenenergy.com [legacy] -> mat.beynon@iberdrola.com.au [current]).

When in doubt, add a cell comment explaining the judgment so the user can override.
