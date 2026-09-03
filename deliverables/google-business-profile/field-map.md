# Questionnaire/ICP to Google Business Profile Field Map

Connects the client's ICP (`_templates/icp-profile-template.md`, built from
the intake questionnaire) to Google Business Profile fields. Limits are
authoritative in `limits.json`.

| GBP field | Limit | Primary ICP/questionnaire source |
|---|---|---|
| Business description | 750 (first ~250 shown before truncation) | Differentiation + Ideal Client sections of the ICP; lead with primary specialty and the client-language hook from intake 2.2 within the first 250 characters. |
| Service name | 58 | Intake 2.1 (services offered) + 2.4 (per-service names) - one Service entry per modality/service, not one combined list. |
| Service description | 300 | Intake 2.4 (session length/fee) + ICP niche - what the service is and who it's for. |
| Update post | 1,500 (first ~100 shown before truncation) | Rotate: a differentiation point, a trust asset (2.5 authority), a seasonal/availability note. |
| Q&A answers | no official cap; write for 150-500 chars | Intake 3.2 (questions prospects usually ask, and the reassurance language already used). |

## Notes specific to GBP

- The business description is a single field with no sub-boxes (unlike PT's
  three-part personal statement), so front-load it the way you'd front-load
  PT's first 270 characters.
- Category selection and service-area settings (not character-limited copy)
  are often the single biggest visibility lever here - confirm the primary
  and secondary categories match the ICP's Top Specialties/niche, and that
  virtual/service-area settings match the telehealth states from intake 2.5.
- Photos and Q&A seeding (asking and answering your own likely questions) are
  part of a complete GBP optimization even though they aren't character-limited
  copy blocks; track them on the punch list, same as PT's implementation
  checklist.
