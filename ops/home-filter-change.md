# Preview-only homepage filtering repair, Nov10

Home render() marks matching cards with filter-show but original CSS never hid nonmatching regular cards. Added two grid-scoped rules: hide all cards when articleGrid.filtering; display:flex only matching cards. No article content or archive row selector changed. Cache bumped to v21.

36 actual tests across320/390/1440: default, category, history category, category+query zero, old hidden-card search, saved, saved+category, saved+category+query zero, clear/reset, empty favorites, favorites toggle. Actual pixels checked phone saved/zero and desktop oldarticle search. Archive search regression checked390/1440.

This site correction is gh-only; official main approval not yet established. Do not carry this CSS patch automatically when promoting daily024. Preview board change also remains gh-only separately. Known pre-existing320homepage overflow persists (350document width); not claimed fixed here. Default currently14non-extra cards, not six; also not changed in this scoped repair.
