# CBAM Knowledge Base

Source: Regulation (EU) 2023/956, attached PDF `CELEX_32023R0956_EN_TXT.pdf`.

## Definitions

- `goods`: goods listed in Annex I.
- `greenhouse_gases`: greenhouse gases specified in Annex I for each listed good.
- `importation`: release for free circulation under Article 201 of Regulation (EU) No 952/2013.
- `customs_territory_of_union`: territory defined in Article 4 of Regulation (EU) No 952/2013.
- `third_country`: country or territory outside the customs territory of the Union.
- `importer`: person lodging a customs declaration for release for free circulation in its own name and behalf, or the person on whose behalf an indirect customs representative lodges it.
- `customs_declarant`: declarant lodging a customs declaration for release for free circulation in its own name or the person in whose name the declaration is lodged.
- `authorised_cbam_declarant`: person authorised by a competent authority under Article 17.
- `direct_emissions`: emissions from production processes, including production of heating and cooling consumed during production.
- `indirect_emissions`: emissions from production of electricity consumed during production processes.
- `embedded_emissions`: direct emissions and indirect emissions from electricity consumed during production, calculated under Annex IV and implementing acts under Article 7(7).
- `actual_emissions`: emissions calculated from primary data from production processes and electricity consumed, determined under Annex IV.
- `default_value`: value calculated or drawn from secondary data representing embedded emissions.
- `cbam_certificate`: electronic certificate corresponding to one tonne of CO2e of embedded emissions in goods.
- `surrender`: offsetting CBAM certificates against declared embedded emissions or embedded emissions that should have been declared.
- `carbon_price`: monetary amount paid in a third country under a carbon emissions reduction scheme for greenhouse gases released during production.
- `installation`: stationary technical unit where a production process is carried out.
- `operator`: person who operates or controls an installation in a third country.

## Covered Goods

- Scope key: Regulation applies to Annex I goods originating in a third country and imported into the customs territory of the Union.
- Origin rule: imported goods are considered originating in third countries under non-preferential origin rules in Article 59 of Regulation (EU) No 952/2013.
- Annex I sectors and CN codes:
  - Cement: `2507 00 80`, `2523 10 00`, `2523 21 00`, `2523 29 00`, `2523 30 00`, `2523 90 00`.
  - Electricity: `2716 00 00`.
  - Fertilisers: `2808 00 00`, `2814`, `2834 21 00`, `3102`, `3105` except `3105 60 00`.
  - Iron and steel: chapter `72` except listed ferro-alloys and `7204`; plus `2601 12 00`, `7301`, `7302`, `7303 00`, `7304`, `7305`, `7306`, `7307`, `7308`, `7309 00`, `7310`, `7311 00`, `7318`, `7326`.
  - Aluminium: `7601`, `7603`, `7604`, `7605`, `7606`, `7607`, `7608`, `7609 00 00`, `7610`, `7611 00 00`, `7612`, `7613 00 00`, `7614`, `7616`.
  - Chemicals: `2804 10 00` hydrogen.
- Annex I greenhouse gases:
  - Cement, electricity, iron and steel, hydrogen: carbon dioxide.
  - Fertilisers: carbon dioxide and nitrous oxide.
  - Aluminium: carbon dioxide and perfluorocarbons.
- Annex II goods: listed iron and steel, aluminium, and hydrogen goods for which only direct emissions are taken into account under Article 7(1).
- Annex III countries outside scope: Iceland, Liechtenstein, Norway, Switzerland.
- Annex III territories outside scope: Busingen, Heligoland, Livigno, Ceuta, Melilla.
- Annex III electricity list: third countries or territories may be added or removed by the Commission under Article 2(11).

## Business Rules

* Rule ID: CBAM-001
* Rule Name: Annex I Goods Scope
* Business Rule: IF goods are listed in Annex I AND originate in a third country AND are imported into the customs territory of the Union THEN Regulation (EU) 2023/956 applies, unless an Article 2 derogation applies.
* Required Inputs: CN code, country or territory of origin, customs procedure, import destination.
* Expected Output: Applicable / Not Applicable / Check Derogation
* Regulation Article(s): Article 2(1), Article 3(1), Annex I

* Rule ID: CBAM-002
* Rule Name: Inward Processing Scope
* Business Rule: IF Annex I goods or processed products from Annex I goods result from inward processing under Article 256 of Regulation (EU) No 952/2013 and are imported into the customs territory of the Union THEN Regulation (EU) 2023/956 applies, unless an Article 2 derogation applies.
* Required Inputs: CN code of input goods, inward processing status, processed product status, import destination.
* Expected Output: Applicable / Not Applicable / Check Inward Processing
* Regulation Article(s): Article 2(1), Article 6(3), Article 34(1)

* Rule ID: CBAM-003
* Rule Name: Continental Shelf and Exclusive Economic Zone Scope
* Business Rule: IF Annex I goods originating in a third country are brought to an artificial island, fixed or floating structure, or other structure on the continental shelf or in the exclusive economic zone of a Member State adjacent to the customs territory of the Union THEN Regulation (EU) 2023/956 applies, subject to implementing acts for detailed conditions.
* Required Inputs: CN code, country or territory of origin, destination structure type, Member State continental shelf or exclusive economic zone status.
* Expected Output: Applicable / Not Applicable / Implementing Act Required
* Regulation Article(s): Article 2(2)

* Rule ID: CBAM-004
* Rule Name: Negligible Value Exemption
* Business Rule: IF Annex I goods are imported into the customs territory of the Union AND intrinsic value per consignment does not exceed the value for goods of negligible value under Article 23 of Council Regulation (EC) No 1186/2009 THEN Regulation (EU) 2023/956 does not apply.
* Required Inputs: CN code, intrinsic value per consignment, negligible-value threshold under Council Regulation (EC) No 1186/2009.
* Expected Output: Exempt / Not Exempt / Threshold Lookup Required
* Regulation Article(s): Article 2(3)(a)

* Rule ID: CBAM-005
* Rule Name: Personal Luggage Exemption
* Business Rule: IF Annex I goods are contained in personal luggage of travellers from a third country AND intrinsic value does not exceed the negligible-value threshold under Article 23 of Council Regulation (EC) No 1186/2009 THEN Regulation (EU) 2023/956 does not apply.
* Required Inputs: CN code, personal luggage flag, traveller from third country flag, intrinsic value, negligible-value threshold.
* Expected Output: Exempt / Not Exempt / Threshold Lookup Required
* Regulation Article(s): Article 2(3)(b)

* Rule ID: CBAM-006
* Rule Name: Military Activity Exemption
* Business Rule: IF goods are to be moved or used in the context of military activities under Article 1(49) of Commission Delegated Regulation (EU) 2015/2446 THEN Regulation (EU) 2023/956 does not apply.
* Required Inputs: military activity flag, legal basis under Commission Delegated Regulation (EU) 2015/2446.
* Expected Output: Exempt / Not Exempt / External Definition Required
* Regulation Article(s): Article 2(3)(c)

* Rule ID: CBAM-007
* Rule Name: Annex III Origin Exclusion
* Business Rule: IF goods originate in a country or territory listed in Annex III point 1 THEN Regulation (EU) 2023/956 does not apply.
* Required Inputs: country or territory of origin, Annex III point 1 lookup.
* Expected Output: Exempt / Not Exempt
* Regulation Article(s): Article 2(4), Annex III

* Rule ID: CBAM-008
* Rule Name: Origin Determination
* Business Rule: IF origin must be determined for imported goods THEN use non-preferential origin rules under Article 59 of Regulation (EU) No 952/2013.
* Required Inputs: origin evidence, customs origin determination data.
* Expected Output: Country or Territory of Origin / Origin Undetermined
* Regulation Article(s): Article 2(5)

* Rule ID: CBAM-009
* Rule Name: Electricity Exclusion
* Business Rule: IF electricity is imported from a third country or territory listed in Annex III point 2 THEN CBAM does not apply to that electricity import.
* Required Inputs: CN code `2716 00 00`, country or territory of origin, Annex III point 2 lookup.
* Expected Output: Exempt / Not Exempt / Annex III Point 2 Lookup Required
* Regulation Article(s): Article 2(7)-(11), Annex III

* Rule ID: CBAM-010
* Rule Name: Authorised Declarant Requirement
* Business Rule: IF goods are imported into the customs territory of the Union under CBAM THEN goods shall be imported only by an authorised CBAM declarant.
* Required Inputs: importer identity, authorised CBAM declarant status, CBAM account number.
* Expected Output: Import Allowed / Import Not Allowed / Authorisation Required
* Regulation Article(s): Article 4, Article 25(1)

* Rule ID: CBAM-011
* Rule Name: Authorisation Applicant
* Business Rule: IF importer is established in a Member State THEN importer applies for authorised CBAM declarant status; IF importer appoints an indirect customs representative that agrees to act as authorised CBAM declarant THEN that representative applies; IF importer is not established in a Member State THEN indirect customs representative applies.
* Required Inputs: importer establishment status, indirect customs representative appointed flag, representative agreement flag.
* Expected Output: Applicant = Importer / Applicant = Indirect Customs Representative
* Regulation Article(s): Article 5(1)-(3)

* Rule ID: CBAM-012
* Rule Name: Electricity Explicit Capacity Allocation
* Business Rule: IF transmission capacity for electricity import is allocated through explicit capacity allocation THEN the person allocated capacity and nominating that capacity for import is regarded as authorised CBAM declarant in the Member State where electricity importation is declared.
* Required Inputs: electricity import flag, explicit capacity allocation flag, capacity holder, nomination status, customs declaration Member State.
* Expected Output: Deemed Authorised CBAM Declarant / Standard Authorisation Path
* Regulation Article(s): Article 5(4)

* Rule ID: CBAM-013
* Rule Name: CBAM Declaration
* Business Rule: IF authorised CBAM declarant imported goods in a calendar year THEN by 31 May of the following year, first in 2027 for year 2026, it must submit a CBAM declaration through the CBAM registry.
* Required Inputs: authorised CBAM declarant, import year, imported goods records.
* Expected Output: Declaration Required / Not Yet Required
* Regulation Article(s): Article 6(1)

* Rule ID: CBAM-014
* Rule Name: CBAM Declaration Content
* Business Rule: IF CBAM declaration is required THEN declaration must include total quantity by goods type, total embedded emissions, total CBAM certificates to surrender after Article 9 and Article 31 adjustments, and verification report copies.
* Required Inputs: quantity by type, embedded emissions, carbon price reduction data, Article 31 adjustment data, verification reports.
* Expected Output: Declaration Data Complete / Declaration Data Incomplete
* Regulation Article(s): Article 6(2)

* Rule ID: CBAM-015
* Rule Name: Returned Goods in Definitive Declaration
* Business Rule: IF imported goods are returned goods under Article 203 of Regulation (EU) No 952/2013 THEN authorised CBAM declarant reports zero embedded emissions separately for those goods in the CBAM declaration.
* Required Inputs: returned goods status, CN code, goods quantity.
* Expected Output: Report Zero Embedded Emissions / Standard Emissions Reporting
* Regulation Article(s): Article 6(5)

* Rule ID: CBAM-016
* Rule Name: Embedded Emissions Calculation
* Business Rule: IF embedded emissions are calculated THEN use Annex IV methods; for Annex II goods only direct emissions are calculated and taken into account.
* Required Inputs: CN code, Annex II lookup, direct emissions, indirect emissions where applicable, production data, electricity consumption data.
* Expected Output: Embedded Emissions Value / Calculation Data Missing
* Regulation Article(s): Article 7(1), Annex II, Annex IV

* Rule ID: CBAM-017
* Rule Name: Actual and Default Emissions
* Business Rule: IF goods are not electricity THEN determine embedded emissions from actual emissions under Annex IV points 2 and 3; IF actual emissions cannot be adequately determined or indirect emissions are being determined THEN use default values under Annex IV point 4.1.
* Required Inputs: product type, actual emissions availability, direct emissions, indirect emissions, default values.
* Expected Output: Actual Emissions Used / Default Values Used / Data Missing
* Regulation Article(s): Article 7(2), Annex IV

* Rule ID: CBAM-018
* Rule Name: Electricity Embedded Emissions
* Business Rule: IF imported good is electricity THEN determine embedded emissions by default values under Annex IV point 4.2 unless criteria for actual emissions under Annex IV point 5 are met.
* Required Inputs: CN code `2716 00 00`, default value, actual emissions criteria evidence.
* Expected Output: Default Values Used / Actual Emissions Used / Criteria Missing
* Regulation Article(s): Article 7(3), Annex IV

* Rule ID: CBAM-019
* Rule Name: Verification of Embedded Emissions
* Business Rule: IF embedded emissions are declared in a CBAM declaration THEN authorised CBAM declarant must ensure total embedded emissions are verified by an accredited verifier using Annex VI principles.
* Required Inputs: embedded emissions, verifier accreditation status, verification report.
* Expected Output: Verified / Not Verified
* Regulation Article(s): Article 8(1), Annex VI

* Rule ID: CBAM-020
* Rule Name: Carbon Price Reduction
* Business Rule: IF carbon price has been effectively paid in the country of origin for declared embedded emissions THEN authorised CBAM declarant may claim a reduction in CBAM certificates to surrender; rebates or compensation available in that country must be taken into account.
* Required Inputs: country of origin, carbon price paid, proof of actual payment, rebate or compensation data, independent certification documentation.
* Expected Output: Reduction Claimable / Reduction Not Claimable / Evidence Missing
* Regulation Article(s): Article 9

* Rule ID: CBAM-021
* Rule Name: Third-Country Operator Registration
* Business Rule: IF an operator of an installation in a third country requests registration THEN Commission registers operator and installation information in the CBAM registry.
* Required Inputs: operator name, address, contact information, installation complete address, geographical coordinates, main economic activity.
* Expected Output: Registration Request Data Complete / Registration Request Data Incomplete
* Regulation Article(s): Article 10(1)-(3)

* Rule ID: CBAM-022
* Rule Name: Operator Verified Emissions Disclosure
* Business Rule: IF third-country operator is registered and determines embedded emissions under Annex IV and verifies them under Annex VI THEN operator may disclose verification information to an authorised CBAM declarant, and the declarant may use it for Article 8 verification obligations.
* Required Inputs: operator registration status, embedded emissions by goods type, verification status, disclosure to declarant.
* Expected Output: Declarant May Use Disclosed Data / Declarant May Not Use Data
* Regulation Article(s): Article 8(2), Article 10(5)-(7)

* Rule ID: CBAM-023
* Rule Name: CBAM Certificate Purchase
* Business Rule: IF authorised CBAM declarant purchases CBAM certificates THEN certificates are sold on the common central platform at the price calculated under Article 21 and registered in the declarant account.
* Required Inputs: authorised CBAM declarant, Member State of establishment, purchase request, weekly CBAM certificate price.
* Expected Output: Certificate Purchased / Purchase Not Available
* Regulation Article(s): Article 20, Article 21

* Rule ID: CBAM-024
* Rule Name: CBAM Certificate Surrender
* Business Rule: IF authorised CBAM declarant has declared embedded emissions for the previous calendar year THEN by 31 May it must surrender CBAM certificates corresponding to the declared and verified embedded emissions.
* Required Inputs: declared embedded emissions, verified emissions status, available CBAM certificates, declaration year.
* Expected Output: Surrender Required / Surrender Complete / Surrender Deficit
* Regulation Article(s): Article 22(1)

* Rule ID: CBAM-025
* Rule Name: Quarterly Certificate Holding
* Business Rule: IF authorised CBAM declarant has imported goods since the start of a calendar year THEN at the end of each quarter certificates in its CBAM registry account must correspond to at least 80 percent of embedded emissions determined by default values under Annex IV.
* Required Inputs: imported goods since start of year, default-value embedded emissions, certificates held at quarter end.
* Expected Output: Holding Sufficient / Holding Insufficient
* Regulation Article(s): Article 22(2)

* Rule ID: CBAM-026
* Rule Name: Certificate Repurchase
* Business Rule: IF authorised CBAM declarant requests repurchase by 30 June after surrender THEN Member State repurchases excess certificates, limited to one third of certificates purchased by that declarant during the previous calendar year, at the purchase price.
* Required Inputs: repurchase request date, surrendered certificates, excess certificates, certificates purchased in previous calendar year, purchase price.
* Expected Output: Repurchase Eligible / Repurchase Not Eligible / Repurchase Limit
* Regulation Article(s): Article 23

* Rule ID: CBAM-027
* Rule Name: Certificate Cancellation
* Business Rule: IF CBAM certificates were purchased during the year before the previous calendar year and remain in the declarant account on 1 July THEN Commission cancels them without compensation, except where surrender quantity is contested in a pending dispute.
* Required Inputs: certificate purchase year, account balance on 1 July, pending dispute flag, disputed amount.
* Expected Output: Cancel / Do Not Cancel / Suspend Cancellation for Disputed Amount
* Regulation Article(s): Article 24

* Rule ID: CBAM-028
* Rule Name: Transitional Period Scope
* Business Rule: IF import occurs from 1 October 2023 through 31 December 2025 THEN importer obligations are limited to reporting obligations in Articles 33, 34 and 35.
* Required Inputs: import date, importer establishment status, indirect customs representative status.
* Expected Output: Transitional Reporting Applies / Transitional Reporting Does Not Apply
* Regulation Article(s): Article 32

* Rule ID: CBAM-029
* Rule Name: Transitional Report Submission
* Business Rule: IF importer or applicable indirect customs representative imported goods during a quarter in the transitional period THEN submit a CBAM report for that quarter to the Commission no later than one month after quarter end.
* Required Inputs: import quarter, imported goods records, importer or indirect customs representative identity.
* Expected Output: Quarterly Report Required / Report Not Required
* Regulation Article(s): Article 35(1)

* Rule ID: CBAM-030
* Rule Name: Transitional Report Content
* Business Rule: IF CBAM report is required THEN report total quantity by goods type, actual total embedded emissions, total indirect emissions, and carbon price due in country of origin taking rebates or compensation into account.
* Required Inputs: quantity by goods type and installation, actual embedded emissions, indirect emissions, country-of-origin carbon price, rebates or compensation.
* Expected Output: Report Data Complete / Report Data Incomplete
* Regulation Article(s): Article 35(2)

* Rule ID: CBAM-031
* Rule Name: Transitional Customs Procedure Reporting
* Business Rule: IF processed products resulting from inward processing are imported during the transitional period THEN Article 35 report includes information on goods placed under inward processing that resulted in the imported processed products; IF import is processed products from outward processing or returned goods under Article 203 of Regulation (EU) No 952/2013 THEN Article 35 reporting obligation does not apply.
* Required Inputs: customs procedure, inward processing flag, outward processing flag, returned goods status, goods data.
* Expected Output: Report Required / Report Not Required
* Regulation Article(s): Article 34

* Rule ID: CBAM-032
* Rule Name: Definitive Penalty for Failure to Surrender
* Business Rule: IF authorised CBAM declarant fails to surrender by 31 May the required number of CBAM certificates for preceding-year embedded emissions THEN penalty applies for each certificate not surrendered; payment does not release the surrender obligation.
* Required Inputs: required certificates, surrendered certificates, surrender deadline, import year.
* Expected Output: Penalty Applies / No Penalty / Outstanding Surrender Obligation
* Regulation Article(s): Article 26(1), Article 26(3)

* Rule ID: CBAM-033
* Rule Name: Unauthorised Import Penalty
* Business Rule: IF a person other than an authorised CBAM declarant introduces goods into the customs territory of the Union without complying with Regulation (EU) 2023/956 THEN penalty is three to five times the Article 26(1) penalty for each certificate not surrendered.
* Required Inputs: importer authorisation status, goods introduced, certificate deficit, non-compliance facts.
* Expected Output: Penalty Applies / No Penalty
* Regulation Article(s): Article 26(2)

* Rule ID: CBAM-034
* Rule Name: Transitional Reporting Penalty
* Business Rule: IF importer or applicable indirect customs representative fails to submit a CBAM report or fails to take necessary steps to correct a CBAM report after correction procedure THEN competent authority imposes an effective, proportionate and dissuasive penalty.
* Required Inputs: report submission status, correction procedure status, correction action status.
* Expected Output: Penalty Applies / No Penalty
* Regulation Article(s): Article 35(5)

## Required Data

- Scope data:
  - CN code.
  - Goods description.
  - Country or territory of origin.
  - Customs procedure.
  - Importation or destination status.
  - Intrinsic value per consignment.
  - Personal luggage status.
  - Military activity status.
  - Annex III country or territory status.
- Authorisation data:
  - Applicant name, address, contact information.
  - EORI number.
  - Main economic activity in the Union.
  - Tax authority certification on no outstanding national tax debt recovery order.
  - Declaration of honour on serious or repeated infringements and serious criminal offences.
  - Financial and operational capacity information.
  - Estimated monetary value and volume of imports by type of goods for current and following calendar year.
  - Names and contact information of persons represented, if applicable.
- Customs data communicated under Article 25:
  - EORI number.
  - CBAM account number.
  - Eight-digit CN code.
  - Quantity.
  - Country of origin.
  - Customs declaration date.
  - Customs procedure.
- Declaration data:
  - Total quantity of each type of goods.
  - Total embedded emissions.
  - Total CBAM certificates to surrender.
  - Verification report copies.
- Emissions records under Annex V:
  - Authorised CBAM declarant name.
  - CBAM account number.
  - Type and quantity of each goods type.
  - Country of origin.
  - Actual emissions or default values.
  - Installation identification, if actual emissions are used.
  - Installation operator contact information, if actual emissions are used.
  - Verification reports, if actual emissions are used.
  - Specific embedded emissions, if actual emissions are used.

## Importer Obligations

- Definitive period:
  - Goods may be imported only by an authorised CBAM declarant.
  - Apply for authorised CBAM declarant status before importing, unless an indirect customs representative applies where permitted or required.
  - Submit annual CBAM declaration by 31 May, first in 2027 for year 2026.
  - Ensure embedded emissions are calculated, recorded, and verified.
  - Keep Article 7 records and verifier report until the end of the fourth year after the year the declaration was or should have been submitted.
  - Surrender CBAM certificates by 31 May.
  - Maintain quarterly certificate balance of at least 80 percent of embedded emissions determined by default values.
- Transitional period:
  - From 1 October 2023 through 31 December 2025, obligations are limited to reporting under Articles 33, 34 and 35.
  - Submit quarterly CBAM report no later than one month after quarter end.

## Exporter Obligations

- No exporter-specific obligation is defined in the attached Regulation text.
- Third-country operator provisions:
  - Operator may request registration of operator and installation information in the CBAM registry.
  - Registered operator must determine embedded emissions by goods type under Annex IV, ensure verification under Annex VI, and keep verification records for four years after verification.
  - Operator may disclose verified embedded emissions information to an authorised CBAM declarant.

## Embedded Emissions

- Embedded emissions are calculated under Annex IV.
- Annex II goods: only direct emissions are calculated and taken into account.
- Goods other than electricity:
  - Use actual emissions under Annex IV points 2 and 3.
  - Use default values under Annex IV point 4.1 where actual emissions cannot be adequately determined and for indirect emissions.
- Electricity:
  - Use default values under Annex IV point 4.2 unless Annex IV point 5 criteria for actual emissions are met.
- Indirect emissions:
  - Calculated under Annex IV point 4.3 and implementing acts under Article 7(7), unless Annex IV point 6 criteria for actual emissions are met.
- Simple goods formula:
  - `specific_embedded_emissions = attributed_emissions / activity_level`
  - `attributed_emissions = direct_emissions + indirect_emissions`
- Complex goods formula:
  - `specific_embedded_emissions = (attributed_emissions + embedded_emissions_of_input_materials) / activity_level`

## CBAM Certificates

- One CBAM certificate corresponds to one tonne of CO2e embedded emissions.
- Certificates are sold by Member States on a common central platform to authorised CBAM declarants established in that Member State.
- Certificate price is the weekly average of EU ETS allowance closing prices on the auction platform; if no auction occurs in a week, use the average of the last auction week.
- Commission publishes the average price on the first working day of the following calendar week; it applies from the first working day after publication to the first working day of the following week.
- Certificates must be surrendered by 31 May each year, first in 2027 for year 2026.
- At each quarter end, account certificates must correspond to at least 80 percent of embedded emissions determined by default values for goods imported since start of year.
- Repurchase request deadline: 30 June of each year during which certificates were surrendered.
- Repurchase cap: one third of certificates purchased by the authorised CBAM declarant during the previous calendar year.
- Cancellation date: 1 July each year for certificates purchased during the year before the previous calendar year and remaining in the account, without compensation, subject to pending dispute suspension.

## Carbon Price Deduction

- Authorised CBAM declarant may claim a certificate reduction for carbon price effectively paid in the country of origin for declared embedded emissions.
- Any rebate or other compensation available in the country of origin that would reduce that carbon price must be taken into account.
- Required records:
  - Documentation showing declared embedded emissions were subject to carbon price effectively paid.
  - Evidence of rebates or compensation, including references to relevant country-of-origin legislation.
  - Certification of documentation by a person independent from the authorised CBAM declarant and country-of-origin authorities.
  - Name and contact information of the independent certifier.
  - Evidence of actual carbon price payment.
- Retention: records kept until end of the fourth year after the year in which the CBAM declaration was or should have been submitted.
- Conversion into certificate reduction is subject to implementing acts under Article 9(4).

## Reporting Requirements

- Definitive CBAM declaration:
  - Due by 31 May each year.
  - First due in 2027 for year 2026.
  - Submitted by authorised CBAM declarant through CBAM registry.
  - Includes quantity, embedded emissions, certificates to surrender, and verification report copies.
- Transitional CBAM report:
  - Applies from 1 October 2023 through 31 December 2025.
  - Submitted quarterly by importer or applicable indirect customs representative.
  - Due no later than one month after quarter end.
  - Includes total quantity by goods type and installation, actual total embedded emissions, total indirect emissions, and carbon price due in country of origin after rebates or compensation.
- Transitional customs exceptions:
  - Inward processing processed products: report information on goods placed under inward processing that resulted in imported processed products.
  - Outward processing processed products and returned goods under Article 203 of Regulation (EU) No 952/2013: Article 35 reporting obligation does not apply.

## Penalties

- Failure to surrender required CBAM certificates by 31 May:
  - Penalty identical to excess emissions penalty under Article 16(3) of Directive 2003/87/EC and increased under Article 16(4) of that Directive.
  - Applies per certificate not surrendered.
  - Payment does not release the obligation to surrender outstanding certificates.
- Unauthorised introduction of goods:
  - Person other than authorised CBAM declarant introducing goods without complying with Regulation (EU) 2023/956 is liable for an effective, proportionate and dissuasive penalty.
  - Penalty amount is three to five times the Article 26(1) penalty for each certificate not surrendered.
- Transitional reporting non-compliance:
  - Failure to submit a CBAM report or failure to correct a report after correction procedure triggers an effective, proportionate and dissuasive penalty.
  - Indicative range and criteria are to be set by implementing acts under Article 35(7).

## Article Mapping

- Article 1: subject matter; CBAM applies to embedded greenhouse gas emissions in Annex I goods on importation.
- Article 2: scope, derogations, Annex III exclusions, origin rule, electricity exclusion mechanism.
- Article 3: definitions used by decision engine.
- Article 4: goods imported only by authorised CBAM declarant.
- Article 5: application for authorised CBAM declarant status and required application data.
- Article 6: CBAM declaration timing and contents; inward/outward processing and returned goods declaration rules.
- Article 7: embedded emissions calculation and recordkeeping.
- Article 8: verification of embedded emissions.
- Article 9: carbon price paid in third country and certificate reduction.
- Article 10: registration of third-country operators and installations; verified emissions disclosure.
- Article 14: CBAM registry data.
- Article 16: CBAM account number and account access.
- Article 17: authorisation criteria, refusal, guarantee, revocation.
- Article 20: sale of CBAM certificates.
- Article 21: CBAM certificate price.
- Article 22: surrender and quarterly certificate holding.
- Article 23: repurchase of certificates.
- Article 24: cancellation of certificates.
- Article 25: customs import controls and customs data communication.
- Article 26: definitive-period penalties.
- Article 31: adjustment of CBAM certificates to reflect EU ETS free allocation.
- Article 32: transitional period scope.
- Article 33: transitional customs notification and customs data communication.
- Article 34: transitional reporting for customs procedures.
- Article 35: transitional CBAM report content, correction, and penalties.
- Annex I: covered goods and greenhouse gases.
- Annex II: goods for which only direct emissions are counted.
- Annex III: countries and territories outside scope.
- Annex IV: methods for calculating embedded emissions.
- Annex V: bookkeeping requirements.
- Annex VI: verification principles and verification report content.
