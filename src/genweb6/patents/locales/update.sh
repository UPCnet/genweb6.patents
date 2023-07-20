#!/bin/bash
# i18ndude should be available in current $PATH (eg by running
# ``export PATH=$PATH:$BUILDOUT_DIR/bin`` when i18ndude is located in your buildout's bin directory)
#
# For every language you want to translate into you need a
# locales/[language]/LC_MESSAGES/genweb6.patents.po
# (e.g. locales/de/LC_MESSAGES/genweb6.patents.po)



dom=
while getopts "d:" opt; do
    case "$opt" in
        d)
            dom="$OPTARG";;
        ?)
           exit 1;;
    esac
done


if [[ -z "$dom" ]]; then
    dom="genweb6.patents"
fi

echo $dom

i18ndude rebuild-pot --pot $dom.pot --create $dom ../
i18ndude sync --pot $dom.pot */LC_MESSAGES/$dom.po
