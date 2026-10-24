# Troubleshooting

## Integration not found

Confirm `custom_components/recall_watch/manifest.json` exists beneath your Home Assistant configuration directory. Restart Home Assistant. For custom repository installations, verify the repository is public and that the HACS/Marketplace category is **Integration**.

## Setup fails or sensor becomes unavailable

The remote feed may block the request, return HTTP errors, time out or produce invalid XML. This integration does not bypass upstream restrictions. Check Home Assistant logs with sensitive information removed, verify normal access to the official RSS page in a browser and check provider availability. Failures must not be interpreted as zero recalls.

## A recalled product is not displayed

The source feed may have a limited current window, the user's keyword filter may exclude the record or the product data may appear only on the linked webpage. Clear or broaden keywords and compare with the official notice. **No matching alert does not mean a product is safe.**

## Product / batch / brand shows Unknown

This is expected when the RSS title and summary do not explicitly state the information in a supported form. A company making an announcement is not automatically treated as the product's brand. The integration intentionally avoids inferring missing fields.

## How to retrieve more than the preview

Use `recall_watch.get_notices` with a supported response-data consumer, set `limit` up to 100 and paginate with `offset`. This returns cached results, not a historical archive.

## Before opening a bug report

Check the current version, install method and whether the issue happens in a real Home Assistant runtime. Use the supplied bug-report form; do not paste access tokens, full logs or private Home Assistant addresses.
