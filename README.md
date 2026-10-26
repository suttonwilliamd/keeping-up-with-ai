# Keeping Up With AI — public outline preview

A dependency-free HTML/CSS page showing the six original public titles as a **proposed outline**, not verified finished chapters. No manuscript, chapter excerpts, guide PDF, checkout, payment, download, fulfillment or release date is supplied here. Browser printing produces an outline, not the guide PDF.

## Local use

Open `index.html` in a browser. No install, build, remote fonts, JavaScript or server is required.

```sh
python -m unittest discover -s tests -v
```

The standard-library HTML parser checks the outline/copy contract, unique IDs, valid internal link targets, basic landmarks and focusable section targets. Negative mutations exercise dead links, duplicate IDs, changed titles, lost disclosures, sales promises, dependencies and keyboard targets. This is structural regression coverage, **not proof of accessibility**. The bounded CI matrix runs on Ubuntu and Windows; adding that workflow is not evidence it has run.

## Manual acceptance

- At 320px and desktop: no horizontal overflow, readable six-title list and explicit availability panel.
- Tab from the top: visible skip link, then outline and availability navigation, then the outline CTA and back-to-top link. Enter follows each fragment; skip/section destinations receive focus.
- Reduced motion: no animation or smooth scrolling. Print: legible light outline with availability and original attribution retained; navigation omitted.
- Check no sales/finished-guide promises return. Do not add private manuscript content or imply editorial endorsement.

## Attribution and publication boundary

The original page stated: “Written by Aaron AI | Supervised by William Sutton.” It remains explicitly labeled original project attribution, not verification of authorship, a finished manuscript or current agent capabilities.

This local redesign does not publish anything or change hosting. Existing provider autobuilds, if configured, are separate. Any source PR requires independent engineering review and root approval. No commercial or manuscript release is authorized by this change.
