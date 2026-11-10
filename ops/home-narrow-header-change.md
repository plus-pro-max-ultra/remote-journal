# Separate preview-only320px homepage header fix

Root cause:320CSSpixels topbar keeps brand139.4px + navigation210.8px in one nonwrapping row, right edge350.22px. Mobile innerWidth also inflated350, so prior checks comparing scrollWidth to innerWidth missed the real visualViewport320 discrepancy. At390 and1440 no overflow. Filtering CSS neither caused nor fixed it.

Added homepage-only @media(max-width:360px) header flex-wrap with10px row gap; action row remains right-aligned. Brand stays first row, navigation second. No controls hidden, no card count changed. Actual320viewport and document now both320, zero elements past viewport.390 and1440 unchanged. Inspected actual top screenshots at all three widths. Homepage filter combinations rerun all pass. Cache v22.

As with filter repairf42bd3a and boardd1d97ad, this change is gh-only under preview grant. Main remains unchanged pending explicit site-change approval; daily article promotion must exclude the three site patches.
