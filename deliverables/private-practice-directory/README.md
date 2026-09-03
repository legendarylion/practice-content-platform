# Private Practice Directory - module status: internal product, schema TBD

The intake questionnaire notes that "the Clinician Roster in Stage 2 maps
one-to-one to the Private Practice Directory profile schema - every roster
field is a listing field," which means this is (or will be) an MHM-controlled
directory rather than a third party with published limits.

Before running an engagement against this module:

1. Confirm the current field list and any character limits with whoever owns
   the Private Practice Directory product/schema - they're authoritative
   here, not a public source.
2. Once confirmed, add `limits.json` (only if fields are actually capped) and
   `field-map.md` here, following the shape of the
   `deliverables/psychology-today/` module.

Because the questionnaire was designed so the Clinician Roster (section 2.5)
maps directly to this listing, this module's field map should be closer to a
1:1 passthrough than a rewrite - confirm with product whether copy needs
adaptation at all versus just population.
