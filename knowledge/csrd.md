# CSRD Scope Knowledge Base

Source: Directive (EU) 2022/2464, attached PDF `CELEX_32022L2464_EN_TXT.pdf`.

# Rule ID: CSRD-001

## Rule Name

Entity categories covered by Articles 19a and 29a

## Required Inputs

- entity_legal_form
- entity_type
- is_insurance_undertaking
- is_credit_institution
- is_large_undertaking_under_directive_2013_34_article_3_4
- is_small_or_medium_undertaking_under_directive_2013_34_article_3_2_or_3_3
- is_micro_undertaking_under_directive_2013_34_article_3_1
- is_public_interest_entity_article_2_1_a

## Decision Logic

- IF entity is an insurance undertaking within Article 1(3)(a) OR a credit institution within Article 1(3)(b), THEN Articles 19a, 29a, 29d, 30, 33, 34 and 51 apply regardless of legal form, PROVIDED the undertaking is either:
  - a large undertaking; OR
  - a small or medium-sized undertaking, except a micro-undertaking, which is a public-interest entity as defined in Article 2(1)(a).
- Member States may choose not to apply those coordination measures to undertakings listed in Article 2(5), points (2) to (23), of Directive 2013/36/EU.

## Output

- covered_entity_category
- not_covered_entity_category
- member_state_option_required

## Regulatory Reference

- Article 1(1), adding Article 1(3) to Directive 2013/34/EU

# Rule ID: CSRD-002

## Rule Name

EU large undertaking annual sustainability reporting

## Required Inputs

- is_large_undertaking_under_directive_2013_34_article_3_4
- financial_year_start_date

## Decision Logic

- IF undertaking is a large undertaking within Article 3(4) of Directive 2013/34/EU THEN it is subject to Article 19a sustainability reporting, subject to applicable exemptions and application dates.

## Output

- annual_sustainability_reporting_in_scope
- not_in_scope_under_this_rule

## Regulatory Reference

- Article 1(4), replacing Article 19a(1) of Directive 2013/34/EU
- Article 5(2)(a)-(b)

# Rule ID: CSRD-003

## Rule Name

Listed SME annual sustainability reporting

## Required Inputs

- is_small_or_medium_undertaking_under_directive_2013_34_article_3_2_or_3_3
- is_micro_undertaking_under_directive_2013_34_article_3_1
- is_public_interest_entity_article_2_1_a
- financial_year_start_date

## Decision Logic

- IF undertaking is a small or medium-sized undertaking AND is not a micro-undertaking AND is a public-interest entity as defined in Article 2(1)(a), THEN it is subject to Article 19a sustainability reporting, subject to applicable exemptions and application dates.
- IF undertaking is a micro-undertaking, THEN it is not in scope under this rule.

## Output

- annual_sustainability_reporting_in_scope
- not_in_scope_micro_undertaking
- not_in_scope_under_this_rule

## Regulatory Reference

- Article 1(4), replacing Article 19a(1) of Directive 2013/34/EU
- Article 5(2)(c)(i)

# Rule ID: CSRD-004

## Rule Name

Listed SME temporary opt-out

## Required Inputs

- is_small_or_medium_undertaking_under_directive_2013_34_article_3_2_or_3_3
- is_public_interest_entity_article_2_1_a
- financial_year_start_date
- management_report_states_reason_for_non_reporting

## Decision Logic

- IF a small or medium-sized undertaking referred to in Article 19a(1) has a financial year starting before 1 January 2028, THEN it may decide not to include Article 19a(1) sustainability reporting in its management report.
- IF this opt-out is used, THEN the undertaking must briefly state in its management report why sustainability reporting was not provided.

## Output

- temporary_opt_out_available
- temporary_opt_out_not_available
- opt_out_statement_required

## Regulatory Reference

- Article 1(4), replacing Article 19a(7) of Directive 2013/34/EU

# Rule ID: CSRD-005

## Rule Name

Annual sustainability reporting subsidiary exemption

## Required Inputs

- is_subsidiary_undertaking
- is_large_undertaking_under_directive_2013_34_article_3_4
- is_public_interest_entity_article_2_1_a
- parent_established_in_member_state
- parent_established_in_third_country
- subsidiary_and_its_subsidiaries_included_in_parent_consolidated_management_report
- third_country_parent_consolidated_sustainability_reporting_equivalent_or_article_29b
- exempted_subsidiary_management_report_contains_required_parent_information
- parent_report_weblinks_available
- assurance_opinion_available
- third_country_parent_report_published_under_article_30
- article_8_regulation_2020_852_disclosures_included_if_third_country_parent

## Decision Logic

- IF undertaking is a subsidiary undertaking AND the undertaking and its subsidiaries are included in the consolidated management report of a parent undertaking drawn up under Articles 29 and 29a, THEN it may be exempt from Article 19a(1)-(4), subject to Article 19a(9) conditions.
- IF subsidiary's parent is established in a third country, THEN exemption is available only where the undertaking and its subsidiaries are included in consolidated sustainability reporting of that third-country parent carried out under Article 29b standards or equivalent standards determined under Directive 2004/109/EC.
- IF parent is established in a third country, THEN publication, assurance opinion, and Article 8 of Regulation (EU) 2020/852 disclosure conditions in Article 19a(9)(b)-(c) must be satisfied.
- IF undertaking is a large undertaking which is a public-interest entity defined in Article 2(1)(a), THEN the Article 19a(9) exemption does not apply.

## Output

- exempt_from_article_19a
- not_exempt_from_article_19a
- exemption_conditions_incomplete

## Regulatory Reference

- Article 1(4), replacing Article 19a(9)-(10) of Directive 2013/34/EU

# Rule ID: CSRD-006

## Rule Name

Parent undertaking consolidated sustainability reporting

## Required Inputs

- is_parent_undertaking
- is_large_group_under_directive_2013_34_article_3_7
- financial_year_start_date

## Decision Logic

- IF undertaking is a parent undertaking of a large group referred to in Article 3(7) of Directive 2013/34/EU THEN it is subject to Article 29a consolidated sustainability reporting, subject to applicable exemptions and application dates.

## Output

- consolidated_sustainability_reporting_in_scope
- not_in_scope_under_this_rule

## Regulatory Reference

- Article 1(7), replacing Article 29a(1) of Directive 2013/34/EU
- Article 5(2)(a)-(b)

# Rule ID: CSRD-007

## Rule Name

Consolidated sustainability reporting parent exemption

## Required Inputs

- is_parent_undertaking
- is_subsidiary_undertaking
- is_large_undertaking_under_directive_2013_34_article_3_4
- is_public_interest_entity_article_2_1_a
- parent_and_subsidiaries_included_in_another_parent_consolidated_management_report
- higher_parent_established_in_member_state
- higher_parent_established_in_third_country
- third_country_parent_consolidated_sustainability_reporting_equivalent_or_article_29b
- exempted_parent_management_report_contains_required_parent_information
- parent_report_weblinks_available
- assurance_opinion_available
- third_country_parent_report_published_under_article_30
- article_8_regulation_2020_852_disclosures_included_if_third_country_parent

## Decision Logic

- IF parent undertaking is itself a subsidiary undertaking AND that parent undertaking and its subsidiaries are included in the consolidated management report of another undertaking drawn up under Article 29 and Article 29a, THEN it may be exempt from Article 29a(1)-(5), subject to Article 29a(8) conditions.
- IF higher parent is established in a third country, THEN exemption is available only where consolidated sustainability reporting is carried out under Article 29b standards or equivalent standards determined under Directive 2004/109/EC.
- IF higher parent is established in a third country, THEN publication, assurance opinion, and Article 8 of Regulation (EU) 2020/852 disclosure conditions in Article 29a(8)(b)-(c) must be satisfied.
- IF undertaking is a large undertaking which is a public-interest entity defined in Article 2(1)(a), THEN the Article 29a(8) exemption does not apply.

## Output

- exempt_from_article_29a
- not_exempt_from_article_29a
- exemption_conditions_incomplete

## Regulatory Reference

- Article 1(7), replacing Article 29a(8)-(9) of Directive 2013/34/EU

# Rule ID: CSRD-008

## Rule Name

Third-country undertaking with EU subsidiary

## Required Inputs

- ultimate_parent_governed_by_third_country_law
- eu_subsidiary_established_in_member_state
- eu_subsidiary_is_large_undertaking_under_directive_2013_34_article_3_4
- eu_subsidiary_is_small_or_medium_undertaking_under_directive_2013_34_article_3_2_or_3_3
- eu_subsidiary_is_micro_undertaking_under_directive_2013_34_article_3_1
- eu_subsidiary_is_public_interest_entity_article_2_1_a
- third_country_undertaking_union_net_turnover_year_1
- third_country_undertaking_union_net_turnover_year_2
- financial_year_start_date

## Decision Logic

- IF ultimate parent undertaking is governed by the law of a third country AND has a subsidiary undertaking established in a Member State AND that subsidiary is either:
  - a large subsidiary undertaking; OR
  - a small or medium-sized subsidiary undertaking, except a micro-undertaking, which is a public-interest entity as defined in Article 2(1)(a);
  AND the third-country undertaking generated net turnover of more than EUR 150 million in the Union for each of the last two consecutive financial years, THEN Article 40a reporting applies.

## Output

- third_country_parent_reporting_in_scope_via_subsidiary
- not_in_scope_under_this_rule

## Regulatory Reference

- Article 1(14), inserting Article 40a(1) into Directive 2013/34/EU
- Article 5(2), application of Article 1(14)

# Rule ID: CSRD-009

## Rule Name

Third-country undertaking with EU branch

## Required Inputs

- branch_located_in_member_state
- branch_of_undertaking_governed_by_third_country_law
- third_country_undertaking_has_article_40a_eu_subsidiary
- third_country_undertaking_group_status
- branch_net_turnover_preceding_financial_year
- third_country_undertaking_union_net_turnover_year_1
- third_country_undertaking_union_net_turnover_year_2
- financial_year_start_date

## Decision Logic

- IF a branch is located in a Member State AND is a branch of an undertaking governed by the law of a third country AND the third-country undertaking does not have a subsidiary undertaking referred to in Article 40a(1) first subparagraph AND the branch generated net turnover of more than EUR 40 million in the preceding financial year AND the third-country undertaking generated net turnover of more than EUR 150 million in the Union for each of the last two consecutive financial years, THEN Article 40a reporting applies.

## Output

- third_country_reporting_in_scope_via_branch
- not_in_scope_under_this_rule

## Regulatory Reference

- Article 1(14), inserting Article 40a(1) into Directive 2013/34/EU
- Article 5(2), application of Article 1(14)

# Rule ID: CSRD-010

## Rule Name

Third-country undertaking missing information

## Required Inputs

- article_40a_reporting_in_scope
- required_third_country_reporting_information_available
- subsidiary_or_branch_requested_information_from_third_country_undertaking

## Decision Logic

- IF Article 40a reporting applies AND not all required information is provided by the third-country undertaking, THEN the subsidiary undertaking or branch must draw up, publish and make accessible the sustainability report containing all information in its possession, obtained or acquired, and issue a statement that the third-country undertaking did not make the necessary information available.

## Output

- publish_available_information_and_missing_information_statement
- standard_article_40a_report

## Regulatory Reference

- Article 1(14), inserting Article 40a(2) into Directive 2013/34/EU

# Rule ID: CSRD-011

## Rule Name

Third-country undertaking publication deadline

## Required Inputs

- article_40a_reporting_in_scope
- balance_sheet_date
- report_publication_date

## Decision Logic

- IF Article 40a reporting applies, THEN the subsidiary undertaking or branch must publish the sustainability report with assurance opinion and any required statement within 12 months of the balance sheet date of the financial year for which the report is drawn up.

## Output

- publication_required
- publication_deadline_met
- publication_deadline_not_met

## Regulatory Reference

- Article 1(14), inserting Article 40d(1)-(2) into Directive 2013/34/EU

# Rule ID: CSRD-012

## Rule Name

2024 first application group

## Required Inputs

- financial_year_start_date
- is_large_undertaking_under_directive_2013_34_article_3_4
- is_public_interest_entity_article_2_1
- average_employees_financial_year
- is_parent_undertaking
- is_large_group_under_directive_2013_34_article_3_7
- average_employees_financial_year_consolidated

## Decision Logic

- IF financial year starts on or after 1 January 2024 AND undertaking is a large undertaking that is a public-interest entity and exceeds 500 employees on its balance sheet date during the financial year, THEN CSRD measures apply.
- IF financial year starts on or after 1 January 2024 AND undertaking is a public-interest entity that is a parent undertaking of a large group and exceeds 500 employees on its balance sheet date on a consolidated basis during the financial year, THEN CSRD measures apply.

## Output

- applies_from_financial_year_2024
- does_not_apply_from_financial_year_2024

## Regulatory Reference

- Article 5(2)(a)

# Rule ID: CSRD-013

## Rule Name

2025 application group

## Required Inputs

- financial_year_start_date
- is_large_undertaking_under_directive_2013_34_article_3_4
- is_parent_undertaking
- is_large_group_under_directive_2013_34_article_3_7
- already_in_2024_first_application_group

## Decision Logic

- IF financial year starts on or after 1 January 2025 AND undertaking is a large undertaking other than those in the 2024 first application group, THEN CSRD measures apply.
- IF financial year starts on or after 1 January 2025 AND undertaking is a parent undertaking of a large group other than those in the 2024 first application group, THEN CSRD measures apply.

## Output

- applies_from_financial_year_2025
- does_not_apply_from_financial_year_2025

## Regulatory Reference

- Article 5(2)(b)

# Rule ID: CSRD-014

## Rule Name

2026 application group

## Required Inputs

- financial_year_start_date
- is_small_or_medium_undertaking_under_directive_2013_34_article_3_2_or_3_3
- is_public_interest_entity_article_2_1_a
- is_micro_undertaking_under_directive_2013_34_article_3_1
- is_small_and_non_complex_institution
- is_captive_insurance_undertaking
- is_captive_reinsurance_undertaking
- is_large_undertaking_under_directive_2013_34_article_3_4

## Decision Logic

- IF financial year starts on or after 1 January 2026 AND undertaking is a small or medium-sized undertaking that is a public-interest entity under Article 2(1)(a) and is not a micro-undertaking, THEN CSRD measures apply, subject to the Article 19a(7) temporary opt-out.
- IF financial year starts on or after 1 January 2026 AND undertaking is a small and non-complex institution, captive insurance undertaking, or captive reinsurance undertaking, THEN CSRD measures apply only if it is either:
  - a large undertaking; OR
  - a small or medium-sized undertaking that is a public-interest entity under Article 2(1)(a) and is not a micro-undertaking.

## Output

- applies_from_financial_year_2026
- does_not_apply_from_financial_year_2026
- check_temporary_opt_out

## Regulatory Reference

- Article 5(2)(c)
- Article 1(4), replacing Article 19a(7) of Directive 2013/34/EU

# Rule ID: CSRD-015

## Rule Name

Third-country undertaking application date

## Required Inputs

- financial_year_start_date
- article_40a_reporting_in_scope

## Decision Logic

- IF Article 40a reporting applies, THEN Member States apply the measures necessary to comply with Article 1(14) for financial years starting on or after 1 January 2028.

## Output

- applies_from_financial_year_2028
- does_not_apply_before_financial_year_2028

## Regulatory Reference

- Article 5(2), application of Article 1(14)

# Rule ID: CSRD-016

## Rule Name

Union subsidiary consolidated reporting transition

## Required Inputs

- current_date
- union_subsidiary_subject_to_article_19a_or_29a
- parent_undertaking_governed_by_member_state_law
- union_subsidiaries_subject_to_article_19a_or_29a
- union_subsidiary_turnover_rank_in_union_last_five_financial_years

## Decision Logic

- UNTIL 6 January 2030, IF a Union subsidiary undertaking is subject to Article 19a or 29a AND its parent undertaking is not governed by the law of a Member State, THEN Member States shall permit that Union subsidiary undertaking to prepare consolidated sustainability reporting under Article 29a that includes all Union subsidiary undertakings of that parent undertaking subject to Article 19a or 29a.
- The Union subsidiary undertaking preparing the reporting must be one of the Union subsidiaries of the group that generated the greatest turnover in the Union in at least one of the preceding five financial years, on a consolidated basis where applicable.
- Reporting under this transition is considered parent-level group reporting for the Article 19a(9) and Article 29a(8) exemptions.

## Output

- transitional_union_subsidiary_group_reporting_available
- transitional_union_subsidiary_group_reporting_not_available
- may_support_article_19a_or_29a_exemption

## Regulatory Reference

- Article 1(16), inserting Article 48i into Directive 2013/34/EU

# Rule ID: CSRD-017

## Rule Name

Issuer management report sustainability reporting

## Required Inputs

- is_issuer_under_directive_2004_109_article_2_1_d
- securities_admitted_to_trading_on_eu_regulated_market
- is_large_undertaking_under_directive_2013_34_article_3_4
- is_parent_undertaking
- is_large_group_under_directive_2013_34_article_3_7
- is_small_or_medium_undertaking_under_directive_2013_34_article_3_2_or_3_3
- is_micro_undertaking_under_directive_2013_34_article_3_1
- financial_year_start_date

## Decision Logic

- IF issuer is required to draw up a management report AND is an undertaking referred to in Articles 19a or 29d(1), THEN the management report shall be drawn up in accordance with Articles 19, 19a and 20, and Article 29d(1), and include specifications adopted under Article 8(4) of Regulation (EU) 2020/852.
- IF issuer is required to prepare consolidated accounts AND is an undertaking referred to in Articles 29a or 29d(2), THEN the consolidated management report shall be drawn up in accordance with Articles 29 and 29a and Article 29d(2), and include specifications adopted under Article 8(4) of Regulation (EU) 2020/852.
- Application dates for issuers follow Article 5 measures for Article 2.

## Output

- issuer_article_19a_reporting_in_scope
- issuer_article_29a_reporting_in_scope
- issuer_not_in_scope_under_this_rule

## Regulatory Reference

- Article 2(2), amending Article 4(5) of Directive 2004/109/EC
- Article 5(2), application of Article 2

# Decision Flow

1. Determine whether the entity is governed by Member State law, is an EU subsidiary of a third-country undertaking, or is an EU branch of a third-country undertaking.
2. Determine whether the entity is a large undertaking, medium-sized undertaking, small undertaking, or micro-undertaking under Article 3 of Directive 2013/34/EU.
3. Determine whether the entity is a public-interest entity under Article 2(1), and where relevant Article 2(1)(a), of Directive 2013/34/EU.
4. Determine whether the entity is an issuer under Article 2(1)(d) of Directive 2004/109/EC with securities admitted to trading on an EU regulated market.
5. For EU undertakings, check Article 19a scope:
   - large undertaking; or
   - small or medium-sized undertaking, except micro-undertaking, that is a public-interest entity under Article 2(1)(a).
6. For EU parent undertakings, check Article 29a scope:
   - parent undertaking of a large group under Article 3(7) of Directive 2013/34/EU.
7. For issuers, check whether the management report or consolidated management report must be drawn up under Articles 19a or 29a via Directive 2004/109/EC Article 4(5).
8. Check whether Article 19a(9) subsidiary exemption applies; do not apply it to large undertakings that are public-interest entities under Article 2(1)(a).
9. Check whether Article 29a(8) parent-undertaking exemption applies; do not apply it to large undertakings that are public-interest entities under Article 2(1)(a).
10. If parent is not governed by Member State law and date is before or on 6 January 2030, check Article 48i transitional Union subsidiary consolidated reporting.
11. Check application date:
   - financial years starting on or after 1 January 2024 for large public-interest undertakings over 500 employees and public-interest parent undertakings of large groups over 500 employees on a consolidated basis;
   - financial years starting on or after 1 January 2025 for other large undertakings and other parent undertakings of large groups;
   - financial years starting on or after 1 January 2026 for listed SMEs except micro-undertakings, small and non-complex institutions, captive insurance undertakings, and captive reinsurance undertakings meeting Article 5(2)(c) conditions;
   - financial years starting on or after 1 January 2028 for Article 40a third-country undertaking reporting.
12. For listed SMEs before financial years starting 1 January 2028, check whether Article 19a(7) temporary opt-out is used with the required management-report statement.
13. For third-country undertakings, check Article 40a subsidiary route:
   - EU subsidiary is large; or
   - EU subsidiary is a listed SME except micro-undertaking;
   - third-country undertaking generated more than EUR 150 million net turnover in the Union for each of the last two consecutive financial years.
14. If no Article 40a subsidiary route applies, check Article 40a branch route:
   - EU branch of third-country undertaking;
   - no Article 40a qualifying EU subsidiary;
   - branch generated more than EUR 40 million net turnover in the preceding financial year;
   - third-country undertaking generated more than EUR 150 million net turnover in the Union for each of the last two consecutive financial years.
15. Return one of:
   - `CSRD_IN_SCOPE_ARTICLE_19A`
   - `CSRD_IN_SCOPE_ARTICLE_29A`
   - `CSRD_IN_SCOPE_ISSUER_ARTICLE_4_5`
   - `CSRD_IN_SCOPE_ARTICLE_40A`
   - `CSRD_EXEMPT_SUBSIDIARY`
   - `CSRD_EXEMPT_PARENT`
   - `CSRD_TEMPORARY_OPT_OUT_AVAILABLE`
   - `CSRD_NOT_YET_APPLICABLE_BY_DATE`
   - `CSRD_OUT_OF_SCOPE`
   - `CHECK_EXTERNAL_DIRECTIVE_DEFINITION`

# Input Variables

## Company Information

- undertaking_name
- entity_legal_form
- entity_type
- is_insurance_undertaking
- is_credit_institution
- is_small_and_non_complex_institution
- is_captive_insurance_undertaking
- is_captive_reinsurance_undertaking
- is_public_interest_entity_article_2_1
- is_public_interest_entity_article_2_1_a
- financial_year_start_date
- balance_sheet_date

## Financial Information

- is_large_undertaking_under_directive_2013_34_article_3_4
- is_small_or_medium_undertaking_under_directive_2013_34_article_3_2_or_3_3
- is_micro_undertaking_under_directive_2013_34_article_3_1
- is_large_group_under_directive_2013_34_article_3_7
- average_employees_financial_year
- average_employees_financial_year_consolidated
- third_country_undertaking_union_net_turnover_year_1
- third_country_undertaking_union_net_turnover_year_2
- branch_net_turnover_preceding_financial_year
- union_subsidiary_turnover_rank_in_union_last_five_financial_years

## Listing Information

- securities_admitted_to_trading_on_eu_regulated_market
- issuer_under_directive_2004_109_article_2_1_d

## EU Presence

- governed_by_member_state_law
- governed_by_third_country_law
- established_in_member_state
- eu_subsidiary_established_in_member_state
- branch_located_in_member_state
- third_country_undertaking_has_article_40a_eu_subsidiary

## Group Structure

- is_parent_undertaking
- is_subsidiary_undertaking
- ultimate_parent_governed_by_third_country_law
- parent_established_in_member_state
- parent_established_in_third_country
- higher_parent_established_in_member_state
- higher_parent_established_in_third_country
- subsidiary_and_its_subsidiaries_included_in_parent_consolidated_management_report
- parent_and_subsidiaries_included_in_another_parent_consolidated_management_report
- third_country_parent_consolidated_sustainability_reporting_equivalent_or_article_29b
- exempted_subsidiary_management_report_contains_required_parent_information
- exempted_parent_management_report_contains_required_parent_information
- parent_report_weblinks_available
- assurance_opinion_available
- third_country_parent_report_published_under_article_30
- article_8_regulation_2020_852_disclosures_included_if_third_country_parent
- union_subsidiaries_subject_to_article_19a_or_29a

# Excluded Information

- Sustainability reporting content under Article 19a(2)-(6), except where needed to identify scope, opt-out, or exemption.
- Consolidated sustainability reporting content under Article 29a(2)-(7), except where needed to identify scope or exemption.
- Sustainability reporting standards under Articles 29b, 29c, and 40b.
- Digital tagging and publication format requirements not needed for applicability.
- Assurance requirements, except where an assurance opinion is a condition for exemption or Article 40a publication.
- Auditor independence, audit committee, and assurance-provider rules.
- Sustainability matters definitions beyond scope classification.
- Reporting standards adoption process and delegated-act procedures.
- Recitals, objectives, policy rationale, and background.
- Detailed disclosure topics such as business model, strategy, due diligence, targets, governance, risks, indicators, and value-chain reporting.
- Penalties and enforcement measures not used to determine whether an entity is in scope.
