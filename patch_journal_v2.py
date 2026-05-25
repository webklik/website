#!/usr/bin/env python3
# patch_journal_v2.py — Mister Wok Journal Article Overwrite
# Restores four articles after git-HEAD / PowerShell encoding regression (UTF-8 safe)
# Run from: Mister_Wok_MNFVSS/
# Idempotent: safe to re-run at any time

import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(BASE, 'journal', 'decade-at-the-flame.html')

ARTICLE_CSS_EXTRA = """
    .article-cta-note{font-size:.72rem;color:var(--color-text-3);margin-top:var(--s-3);line-height:1.5;}
"""

# ── HEAD BLOCKS (title through JSON-LD, before <style>) ─────────────────

HEAD_SPRING = """  <title>Spring Rolls: Nairobi's Little Gold Bars | The Wok Journal</title>
  <meta name="description" content="A ritual object, not a snack — hand-rolled daily, fried at the precise Maillard threshold. Four per plate. Mister Wok, Nairobi since 2004.">
  <!-- Google Tag Manager -->
  <script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
  new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
  j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
  'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
  })(window,document,'script','dataLayer','GTM-WGQ2FPZR');</script>
  <!-- End Google Tag Manager -->

  <!-- DataLayer Initialization -->
  <script>
  window.dataLayer = window.dataLayer || [];
  window.dataLayer.push({
    event: 'page_view',
    page_title: document.title,
    page_url: window.location.href,
    page_type: 'article',
    article_id: 'spring-rolls-gold-prosperity',
    article_published: '2026-01-24',
    branch_selected: null,
    timestamp: new Date().toISOString()
  });
  </script>

  <link rel="canonical" href="https://misterwok.net/journal/spring-rolls-gold-prosperity.html">
  <link rel="icon" href="/favicon.ico">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="preload" href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700&family=DM+Sans:wght@300;400;500;700&display=swap" as="style" onload="this.onload=null;this.rel='stylesheet'">
  <noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700&family=DM+Sans:wght@300;400;500;700&display=swap"></noscript>

  <meta property="og:title" content="Spring Rolls: Nairobi's Little Gold Bars — Mister Wok">
  <meta property="og:description" content="A ritual object, not a snack. Four per plate, hand-rolled daily, fried at the precise Maillard threshold.">
  <meta property="og:url" content="https://misterwok.net/journal/spring-rolls-gold-prosperity.html">
  <meta property="og:type" content="article">
  <meta property="og:image" content="https://misterwok.net/images/food/spring-rolls.webp">
  <meta property="og:image:alt" content="Mister Wok spring rolls — four per plate, hand-rolled daily">
  <meta property="og:site_name" content="Mister Wok">
  <meta property="og:locale" content="en_KE">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Spring Rolls: Nairobi's Little Gold Bars">
  <meta name="twitter:description" content="Hand-rolled daily. Fried at the precise Maillard threshold. Four per plate.">
  <meta name="twitter:image" content="https://misterwok.net/images/food/spring-rolls.webp">
  <script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "Spring Rolls: Nairobi's Little Gold Bars",
  "description": "A ritual object, not a snack — hand-rolled daily, fried at the precise Maillard threshold. Four per plate. Mister Wok, Nairobi since 2004.",
  "url": "https://misterwok.net/journal/spring-rolls-gold-prosperity.html",
  "datePublished": "2026-01-24",
  "dateModified": "2026-05-22",
  "inLanguage": "en-KE",
  "image": "https://misterwok.net/images/food/spring-rolls.webp",
  "author": { "@type": "Organization", "name": "Mister Wok", "url": "https://misterwok.net" },
  "publisher": {
    "@type": "Organization",
    "name": "Mister Wok",
    "logo": { "@type": "ImageObject", "url": "https://misterwok.net/favicon.ico" }
  },
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "https://misterwok.net/journal/spring-rolls-gold-prosperity.html"
  },
  "keywords": ["spring rolls", "Chinese New Year", "Nairobi food", "Mister Wok", "wok cuisine", "gold ingots", "halal"],
  "articleSection": "The Wok Journal · Craft",
  "wordCount": "820"
}
</script>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://misterwok.net/" },
    { "@type": "ListItem", "position": 2, "name": "The Journal", "item": "https://misterwok.net/journal/" },
    { "@type": "ListItem", "position": 3, "name": "Spring Rolls: Nairobi's Little Gold Bars", "item": "https://misterwok.net/journal/spring-rolls-gold-prosperity.html" }
  ]
}
</script>
"""

HEAD_WOK_HEI = """  <title>The Physics of the Flame: Why You Can't Replicate Wok Hei at Home | The Wok Journal</title>
  <meta name="description" content="A technical investigation into wok cooking — seasoned steel, thermal mass, aerosolized oil, and why industrial infrastructure produces flavours a home kitchen cannot. Mister Wok, Nairobi.">
  <!-- Google Tag Manager -->
  <script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
  new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
  j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
  'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
  })(window,document,'script','dataLayer','GTM-WGQ2FPZR');</script>
  <!-- End Google Tag Manager -->

  <!-- DataLayer Initialization -->
  <script>
  window.dataLayer = window.dataLayer || [];
  window.dataLayer.push({
    event: 'page_view',
    page_title: document.title,
    page_url: window.location.href,
    page_type: 'article',
    article_id: 'wok-hei-physics',
    article_published: '2026-02-14',
    branch_selected: null,
    timestamp: new Date().toISOString()
  });
  </script>

  <link rel="canonical" href="https://misterwok.net/journal/wok-hei-physics.html">
  <link rel="icon" href="/favicon.ico">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="preload" href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700&family=DM+Sans:wght@300;400;500;700&display=swap" as="style" onload="this.onload=null;this.rel='stylesheet'">
  <noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700&family=DM+Sans:wght@300;400;500;700&display=swap"></noscript>

  <meta property="og:title" content="The Physics of the Flame: Why You Can't Replicate Wok Hei at Home">
  <meta property="og:description" content="Seasoned steel, thermal mass, aerosolized oil, kinetic rhythm — the engineering behind Wok Hei explained.">
  <meta property="og:url" content="https://misterwok.net/journal/wok-hei-physics.html">
  <meta property="og:type" content="article">
  <meta property="og:image" content="https://misterwok.net/images/food/wok-toss-rice.webp">
  <meta property="og:image:alt" content="Mister Wok — wok toss at 300°C, Nairobi">
  <meta property="og:site_name" content="Mister Wok">
  <meta property="og:locale" content="en_KE">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="The Physics of the Flame — Wok Hei Explained">
  <meta name="twitter:description" content="Why thermal mass, aerosolization, and kinetic rhythm make Wok Hei impossible to replicate at home.">
  <meta name="twitter:image" content="https://misterwok.net/images/food/wok-toss-rice.webp">
  <script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "The Physics of the Flame: Why You Can't Replicate Wok Hei at Home",
  "description": "A technical investigation into wok cooking — seasoned steel, thermal mass, aerosolized oil, and why industrial infrastructure produces flavours a home kitchen cannot.",
  "url": "https://misterwok.net/journal/wok-hei-physics.html",
  "datePublished": "2026-02-14",
  "dateModified": "2026-05-22",
  "inLanguage": "en-KE",
  "image": "https://misterwok.net/images/food/wok-toss-rice.webp",
  "author": { "@type": "Organization", "name": "Mister Wok", "url": "https://misterwok.net" },
  "publisher": {
    "@type": "Organization",
    "name": "Mister Wok",
    "logo": { "@type": "ImageObject", "url": "https://misterwok.net/favicon.ico" }
  },
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "https://misterwok.net/journal/wok-hei-physics.html"
  },
  "keywords": ["wok hei", "wok cooking", "thermal mass", "Maillard reaction", "aerosolization", "carbon steel wok", "Mister Wok", "Nairobi"],
  "articleSection": "The Wok Journal · Technique",
  "wordCount": "950"
}
</script>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://misterwok.net/" },
    { "@type": "ListItem", "position": 2, "name": "The Journal", "item": "https://misterwok.net/journal/" },
    { "@type": "ListItem", "position": 3, "name": "The Physics of the Flame", "item": "https://misterwok.net/journal/wok-hei-physics.html" }
  ]
}
</script>
"""

HEAD_BIRTHDAY = """  <title>The Architecture of a Celebration | Private Dining & Events · The Wok Journal</title>
  <meta name="description" content="How Mister Wok became the quiet partner behind Nairobi's most significant tables — from four-generation family lunches to board-level client dinners. Fresh-on-site wok cooking for every occasion.">
  <!-- Google Tag Manager -->
  <script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
  new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
  j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
  'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
  })(window,document,'script','dataLayer','GTM-WGQ2FPZR');</script>
  <!-- End Google Tag Manager -->

  <!-- DataLayer Initialization -->
  <script>
  window.dataLayer = window.dataLayer || [];
  window.dataLayer.push({
    event: 'page_view',
    page_title: document.title,
    page_url: window.location.href,
    page_type: 'article',
    article_id: 'birthday-catering-guide',
    article_published: '2026-05-22',
    branch_selected: null,
    timestamp: new Date().toISOString()
  });
  </script>

  <link rel="canonical" href="https://misterwok.net/journal/birthday-catering-guide.html">
  <link rel="icon" href="/favicon.ico">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="preload" href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700&family=DM+Sans:wght@300;400;500;700&display=swap" as="style" onload="this.onload=null;this.rel='stylesheet'">
  <noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700&family=DM+Sans:wght@300;400;500;700&display=swap"></noscript>

  <meta property="og:title" content="The Architecture of a Celebration — Mister Wok Private Dining & Events">
  <meta property="og:description" content="From first birthdays to eighty-eighth-year celebrations. From corporate dinners to four-generation Sunday lunches. Mister Wok brings the flame to you.">
  <meta property="og:url" content="https://misterwok.net/journal/birthday-catering-guide.html">
  <meta property="og:type" content="article">
  <meta property="og:image" content="https://misterwok.net/images/food/prawn-sizzler.webp">
  <meta property="og:image:alt" content="Mister Wok prawn sizzler — fresh on-site catering, Nairobi">
  <meta property="og:site_name" content="Mister Wok">
  <meta property="og:locale" content="en_KE">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="The Architecture of a Celebration — Mister Wok Events">
  <meta name="twitter:description" content="From first birthdays to eighty-eighth-year celebrations. Mister Wok brings the flame to you.">
  <meta name="twitter:image" content="https://misterwok.net/images/food/prawn-sizzler.webp">
  <script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "The Architecture of a Celebration",
  "description": "How Mister Wok became the quiet partner behind Nairobi's most significant tables — four-generation family lunches, corporate client dinners, and everything in between.",
  "url": "https://misterwok.net/journal/birthday-catering-guide.html",
  "datePublished": "2026-05-22",
  "dateModified": "2026-05-22",
  "inLanguage": "en-KE",
  "image": "https://misterwok.net/images/food/prawn-sizzler.webp",
  "author": { "@type": "Organization", "name": "Mister Wok", "url": "https://misterwok.net" },
  "publisher": {
    "@type": "Organization",
    "name": "Mister Wok",
    "logo": { "@type": "ImageObject", "url": "https://misterwok.net/favicon.ico" }
  },
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "https://misterwok.net/journal/birthday-catering-guide.html"
  },
  "keywords": ["Mister Wok catering", "private dining Nairobi", "corporate events Nairobi", "birthday catering Nairobi", "fresh on-site cooking", "wok catering", "halal catering Nairobi"],
  "articleSection": "The Wok Journal · Private Dining & Events",
  "wordCount": "850",
  "about": {
    "@type": "Service",
    "name": "Mister Wok Private Dining & Events",
    "provider": { "@type": "Restaurant", "name": "Mister Wok", "url": "https://misterwok.net" },
    "areaServed": { "@type": "City", "name": "Nairobi" },
    "contactPoint": {
      "@type": "ContactPoint",
      "email": "events@misterwok.net",
      "contactType": "reservations"
    }
  }
}
</script>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://misterwok.net/" },
    { "@type": "ListItem", "position": 2, "name": "The Journal", "item": "https://misterwok.net/journal/" },
    { "@type": "ListItem", "position": 3, "name": "The Architecture of a Celebration", "item": "https://misterwok.net/journal/birthday-catering-guide.html" }
  ]
}
</script>
"""

HEAD_HALAL = """  <title>Halal-Assured: A Kitchen Standard, Not a Certificate | The Wok Journal</title>
  <meta name="description" content="Twenty-two years of halal assurance at Mister Wok — a sourcing discipline and kitchen protocol that predates the conversation about it. Capital Centre, Parklands, Two Rivers.">
  <!-- Google Tag Manager -->
  <script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
  new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
  j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
  'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
  })(window,document,'script','dataLayer','GTM-WGQ2FPZR');</script>
  <!-- End Google Tag Manager -->

  <!-- DataLayer Initialization -->
  <script>
  window.dataLayer = window.dataLayer || [];
  window.dataLayer.push({
    event: 'page_view',
    page_title: document.title,
    page_url: window.location.href,
    page_type: 'article',
    article_id: 'halal-wok-nairobi',
    article_published: '2026-02-14',
    branch_selected: null,
    timestamp: new Date().toISOString()
  });
  </script>

  <link rel="canonical" href="https://misterwok.net/journal/halal-wok-nairobi.html">
  <link rel="icon" href="/favicon.ico">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="preload" href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700&family=DM+Sans:wght@300;400;500;700&display=swap" as="style" onload="this.onload=null;this.rel='stylesheet'">
  <noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700&family=DM+Sans:wght@300;400;500;700&display=swap"></noscript>

  <meta property="og:title" content="Halal-Assured: A Kitchen Standard, Not a Certificate — Mister Wok">
  <meta property="og:description" content="Twenty-two years. Three branches. One uninterrupted standard.">
  <meta property="og:url" content="https://misterwok.net/journal/halal-wok-nairobi.html">
  <meta property="og:type" content="article">
  <meta property="og:image" content="https://misterwok.net/images/food/dim-sum-main-index.webp">
  <meta property="og:image:alt" content="Mister Wok halal-assured kitchen — Nairobi">
  <meta property="og:site_name" content="Mister Wok">
  <meta property="og:locale" content="en_KE">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Halal-Assured: A Kitchen Standard, Not a Certificate">
  <meta name="twitter:description" content="Twenty-two years of a discipline that begins before the wok is lit.">
  <meta name="twitter:image" content="https://misterwok.net/images/food/dim-sum-main-index.webp">
  <script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "Halal-Assured: A Kitchen Standard, Not a Certificate",
  "description": "Twenty-two years of halal assurance at Mister Wok — a sourcing discipline and kitchen protocol across three Nairobi branches.",
  "url": "https://misterwok.net/journal/halal-wok-nairobi.html",
  "datePublished": "2026-02-14",
  "dateModified": "2026-05-22",
  "inLanguage": "en-KE",
  "image": "https://misterwok.net/images/food/dim-sum-main-index.webp",
  "author": { "@type": "Organization", "name": "Mister Wok", "url": "https://misterwok.net" },
  "publisher": {
    "@type": "Organization",
    "name": "Mister Wok",
    "logo": { "@type": "ImageObject", "url": "https://misterwok.net/favicon.ico" }
  },
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "https://misterwok.net/journal/halal-wok-nairobi.html"
  },
  "keywords": ["halal Nairobi", "halal restaurant Nairobi", "halal Chinese food Nairobi", "Mister Wok halal", "Capital Centre halal", "halal wok cooking"],
  "articleSection": "The Wok Journal · Values",
  "wordCount": "720"
}
</script>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://misterwok.net/" },
    { "@type": "ListItem", "position": 2, "name": "The Journal", "item": "https://misterwok.net/journal/" },
    { "@type": "ListItem", "position": 3, "name": "Halal-Assured: A Kitchen Standard", "item": "https://misterwok.net/journal/halal-wok-nairobi.html" }
  ]
}
</script>
"""

HEAD_LONG_GRAIN = """  <title>Aromatic Long-Grain Rice: The First Technical Decision | The Wok Journal</title>
  <meta name="description" content="Why the grain determines the dish — and why wok fried rice begins at the supply level, not at the flame. Mister Wok, Nairobi since 2004.">
  <!-- Google Tag Manager -->
  <script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
  new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
  j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
  'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
  })(window,document,'script','dataLayer','GTM-WGQ2FPZR');</script>
  <!-- End Google Tag Manager -->

  <!-- DataLayer Initialization -->
  <script>
  window.dataLayer = window.dataLayer || [];
  window.dataLayer.push({
    event: 'page_view',
    page_title: document.title,
    page_url: window.location.href,
    page_type: 'article',
    article_id: 'long-grain-aromatic-rice',
    article_published: '2026-02-14',
    branch_selected: null,
    timestamp: new Date().toISOString()
  });
  </script>

  <link rel="canonical" href="https://misterwok.net/journal/long-grain-aromatic-rice.html">
  <link rel="icon" href="/favicon.ico">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="preload" href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700&family=DM+Sans:wght@300;400;500;700&display=swap" as="style" onload="this.onload=null;this.rel='stylesheet'">
  <noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700&family=DM+Sans:wght@300;400;500;700&display=swap"></noscript>

  <meta property="og:title" content="Aromatic Long-Grain Rice: The First Technical Decision — Mister Wok">
  <meta property="og:description" content="Why the grain determines the dish — and why wok fried rice begins at the supply level, not at the flame.">
  <meta property="og:url" content="https://misterwok.net/journal/long-grain-aromatic-rice.html">
  <meta property="og:type" content="article">
  <meta property="og:image" content="https://misterwok.net/images/food/wok-toss-rice.webp">
  <meta property="og:image:alt" content="Mister Wok Yong Chow fried rice — aged aromatic long-grain rice, wok-tossed at 300°C">
  <meta property="og:site_name" content="Mister Wok">
  <meta property="og:locale" content="en_KE">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Aromatic Long-Grain Rice: The First Technical Decision">
  <meta name="twitter:description" content="Wok fried rice is not a technique problem. It is a grain problem first.">
  <meta name="twitter:image" content="https://misterwok.net/images/food/wok-toss-rice.webp">
  <script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "Aromatic Long-Grain Rice: The First Technical Decision",
  "description": "Why the grain determines the dish — and why wok fried rice begins at the supply level, not at the flame.",
  "url": "https://misterwok.net/journal/long-grain-aromatic-rice.html",
  "datePublished": "2026-02-14",
  "dateModified": "2026-05-24",
  "inLanguage": "en-KE",
  "image": "https://misterwok.net/images/food/wok-toss-rice.webp",
  "author": { "@type": "Organization", "name": "Mister Wok", "url": "https://misterwok.net" },
  "publisher": {
    "@type": "Organization",
    "name": "Mister Wok",
    "logo": { "@type": "ImageObject", "url": "https://misterwok.net/favicon.ico" }
  },
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "https://misterwok.net/journal/long-grain-aromatic-rice.html"
  },
  "keywords": ["aromatic rice", "long grain rice", "wok fried rice", "aged rice", "Mister Wok", "Nairobi", "wok technique"],
  "articleSection": "The Wok Journal · Ingredients",
  "wordCount": "780"
}
</script>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://misterwok.net/" },
    { "@type": "ListItem", "position": 2, "name": "The Journal", "item": "https://misterwok.net/journal/" },
    { "@type": "ListItem", "position": 3, "name": "Aromatic Long-Grain Rice", "item": "https://misterwok.net/journal/long-grain-aromatic-rice.html" }
  ]
}
</script>
"""

# ── MAIN BLOCKS ───────────────────────────────────────────────────────
MAIN_SPRING = """<main class="article-wrap" id="main-content">
  <article itemscope itemtype="https://schema.org/BlogPosting">
    <meta itemprop="url" content="https://misterwok.net/journal/spring-rolls-gold-prosperity.html">
    <meta itemprop="datePublished" content="2026-01-24">
    <meta itemprop="dateModified" content="2026-05-22">

    <header class="article-header">
      <nav class="article-breadcrumb" aria-label="Breadcrumb">
        <a href="/">Home</a>
        <span aria-hidden="true">›</span>
        <a href="/journal/">The Journal</a>
        <span aria-hidden="true">›</span>
        <span aria-current="page">Spring Rolls</span>
      </nav>
      <div class="article-kicker">The Wok Journal · Craft</div>
      <h1 class="article-title" itemprop="headline">Spring Rolls: Nairobi's Little Gold Bars</h1>
      <p class="article-subtitle">A ritual object, not a snack. Four per plate, hand-rolled daily, fried at the precise Maillard threshold.</p>
      <p class="article-lead" itemprop="description">The spring roll is not a snack. It is a work of structural integrity — a thing made with care, rolled by hand, and fried at the precise Maillard threshold. It does not compete with anything else on the plate. It exists in a category defined by its own craft.</p>
      <div class="article-meta">
        <span class="article-meta-item">The Wok Journal · Craft</span>
        <span class="article-meta-dot" aria-hidden="true">·</span>
        <time class="article-meta-item" datetime="2026-01-24" itemprop="datePublished">January 2026</time>
      </div>
      <div class="article-hero-wrap" aria-label="Spring rolls at Mister Wok">
        <img
          src="/images/food/spring-rolls.webp"
          alt="Mister Wok chicken spring rolls — four per plate, crisp gold, hand-rolled daily"
          width="900"
          height="506"
          loading="eager"
          decoding="async"
          itemprop="image"
          class="article-hero-img">
      </div>
    </header>

    <div class="article-body" itemprop="articleBody">

      <h2 class="article-section-head">The Gold Bar</h2>

      <p>In ancient China, spring rolls were shaped to resemble gold ingots — the currency of the imperial treasury. To eat one was to hold, briefly, the form of wealth between your fingers. The symbolism was not accidental. It was the point.</p>

      <p>Chinese New Year falls in spring — the season of new growth, new beginnings, new accounts. Families across Sichuan, Guangdong and Fujian have served spring rolls on the first day of the lunar calendar for centuries, arranged on platters, gleaming under lamplight, because food that carries the shape of a gold bar carries intention. You are not eating a starter. You are opening the year.</p>

      <p>Mister Wok has been rolling spring rolls by hand since 2004. Four per plate. The shape is the same. The intention is the same. The proof is in the eating — no words have ever improved a spring roll. The heat of the wok has already justified it in the kitchen.</p>

      <h2 class="article-section-head">What Is Inside</h2>

      <p>The Mister Wok spring roll is defined as much by what is not in it as by what is.</p>

      <p>No sweetcorn. Sweetcorn adds moisture where there should be none, and sweetness where the flavour profile asks for clean, savoury restraint. The filling is built around the finest, densest cabbage leaves — sourced specifically for their structural integrity and their complete absence of stringiness. A stringy cabbage leaf breaks down in the fryer. It releases water. The water softens the pastry from the inside before the exterior has had time to set. The result is a roll that looks correct and eats incorrectly — yielding where it should snap.</p>

      <p>The correct interior is dry at the core. Firm. Built to survive the heat of the oil without losing its character. The cabbage we use holds because it was chosen to hold — the selection criterion is not cost or volume but density and crunch, tested and sourced accordingly.</p>

      <p>For the vegetable roll, garden vegetables are diced fine and combined with carefully balanced seasoning. The chicken roll adds minced chicken. Both versions are measured in their flavour — the filling is a supporting structure, not the main event. The main event is the pastry, the fry, and the silence between the bite and the heat.</p>

      <h2 class="article-section-head">The Roll</h2>

      <p>The pastry sheet is laid flat. The filling is placed in a precise line — not too much, not centred, positioned so the taper of the roll is even from end to end. The rolling begins at the filling end, tight and without air pockets. A loose roll steams from the inside. A tight roll fries clean. The seal is pressed before the roll goes into holding.</p>

      <p>Each roll is examined before it enters the oil. This is not quality control in the corporate sense. It is craft in the artisanal sense — the person who rolled it knows what it should look like, and anything that does not meet that standard does not leave the preparation surface.</p>

      <h2 class="article-section-head">The Fry</h2>

      <p>Oil temperature is not approximate. A spring roll dropped into oil that is ten degrees too cool absorbs fat before the pastry has sealed. A roll dropped into oil that is ten degrees too hot burns the exterior before the filling is cooked through. The window is narrow. The kitchen knows it because the kitchen has fried this roll ten thousand times and the sound of the entry tells you, within seconds, whether the temperature is correct.</p>

      <p>The correct entry sound is a sustained, immediate sizzle — sharp, not aggressive. The roll settles. The pastry begins to colour within the first thirty seconds. The turn happens at the precise moment the underside has reached the correct gold. Two minutes, total. Out, drained, held briefly, then plated.</p>

      <p>Four per plate. KES 600 for chicken. KES 500 for vegetable.</p>

      <h2 class="article-section-head">The Proof</h2>

      <p>The gold bar analogy holds not because of shape alone but because of what both things share: the sense that something of this quality, this precision, this accumulated craft, should not cost what it costs. That you are receiving more than the price suggests.</p>

      <p>The proof of the spring roll is in the eating. It requires no further argument.</p>

    </div>

    <footer class="article-footer">
      <div class="article-cta-block">
        <div class="article-cta-label">Order from your branch</div>
        <div class="article-cta-row">
          <a href="https://www.foodbooking.com/api/fb/67_y_m" class="article-cta-btn" target="_blank" rel="noopener" data-order-btn="true" data-branch="Parklands">ðŸ® Parklands</a>
          <a href="https://www.foodbooking.com/api/fb/d_yq_g" class="article-cta-btn" target="_blank" rel="noopener" data-order-btn="true" data-branch="Capital Centre">ðŸ•Œ Capital Centre</a>
          <a href="https://www.foodbooking.com/api/fb/k8_d_z" class="article-cta-btn" target="_blank" rel="noopener" data-order-btn="true" data-branch="Two Rivers">ðŸ¬ Two Rivers</a>
        </div>
      </div>
      <div class="article-related">
        <div class="article-related-label">Continue reading</div>
        <div class="article-related-grid">
          <a href="/journal/wok-hei-physics.html" class="article-related-card">
            <div class="article-related-kicker">Technique</div>
            <div class="article-related-title">Wok Hei Physics — 300°C</div>
          </a>
          <a href="/journal/long-grain-aromatic-rice.html" class="article-related-card">
            <div class="article-related-kicker">Ingredients</div>
            <div class="article-related-title">Aromatic Long-Grain Rice</div>
          </a>
          <a href="/journal/halal-wok-nairobi.html" class="article-related-card">
            <div class="article-related-kicker">Values</div>
            <div class="article-related-title">Halal-Assured · 22 Years</div>
          </a>
        </div>
      </div>
    </footer>

  </article>
</main>"""

MAIN_WOK_HEI = """<main class="article-wrap" id="main-content">
  <article itemscope itemtype="https://schema.org/BlogPosting">
    <meta itemprop="url" content="https://misterwok.net/journal/wok-hei-physics.html">
    <meta itemprop="datePublished" content="2026-02-14">
    <meta itemprop="dateModified" content="2026-05-22">

    <header class="article-header">
      <nav class="article-breadcrumb" aria-label="Breadcrumb">
        <a href="/">Home</a>
        <span aria-hidden="true">›</span>
        <a href="/journal/">The Journal</a>
        <span aria-hidden="true">›</span>
        <span aria-current="page">The Physics of the Flame</span>
      </nav>
      <div class="article-kicker">The Wok Journal · Technique</div>
      <h1 class="article-title" itemprop="headline">The Physics of the Flame</h1>
      <p class="article-subtitle">Why you cannot replicate Wok Hei at home</p>
      <p class="article-lead" itemprop="description">A wok at operating temperature is not a cooking vessel in the conventional sense. It is a controlled environment — a set of thermal, chemical, and mechanical conditions that exist briefly, at great intensity, and produce results that cannot be approximated by different equipment running at different parameters.</p>
      <div class="article-meta">
        <span class="article-meta-item">The Wok Journal · Technique</span>
        <span class="article-meta-dot" aria-hidden="true">·</span>
        <time class="article-meta-item" datetime="2026-02-14" itemprop="datePublished">February 2026</time>
      </div>
      <div class="article-hero-wrap" aria-label="Wok toss at 300°C — Mister Wok kitchen">
        <img
          src="/images/food/wok-toss-rice.webp"
          alt="Wok toss at 300°C — Mister Wok kitchen, Nairobi"
          width="900"
          height="506"
          loading="eager"
          decoding="async"
          itemprop="image"
          class="article-hero-img">
      </div>
    </header>

    <div class="article-body" itemprop="articleBody">

      <p>Understanding why the food tastes the way it does begins with understanding the physics of how it was made.</p>

      <h2 class="article-section-head">I. The Seasoned Surface</h2>

      <p>A carbon steel wok is not a pan. That distinction is not semantic — it is structural. Over months and years of use, the interior surface of a carbon steel wok develops a polymerized oil layer: cooking oil, driven into the steel's microscopic pores by repeated high-heat cycles, oxidizing and carbonizing into a patina that is simultaneously non-stick, heat-conductive, and chemically reactive in ways that bare metal is not.</p>

      <p>This is not coating. It is not Teflon. It is not a manufactured surface applied in a factory. It is the accumulated record of every meal the wok has ever made — a living interface that food scientists classify as a seasoned surface and that any experienced cook would describe more simply as memory.</p>

      <p>The wok remembers. Each cycle of heat and oil adds another molecular layer, darkening the steel, narrowing the surface pores, making the boundary between metal and ingredient more precise and more responsive. A new wok cannot produce the same food as one that has been in continuous service for five years. The surface is too young. It has not yet developed the thermal characteristics that come from ten thousand meals. The Mister Wok woks are not new.</p>

      <h2 class="article-section-head">II. The Heat Gradient</h2>

      <p>A domestic gas hob delivers approximately three to five kilowatts of heat through a single burner ring. The flame is uniform, circular, and distributed across the base of the pan. There is one temperature zone: whatever the burner produces.</p>

      <p>An industrial wok burner operates on a different architecture entirely. At its centre — the blast zone — the metal surface temperature exceeds 300°C, sometimes reaching 350°C at peak loading. The outer rim of the wok, away from the central blast, sits 80 to 120°C cooler. This differential is not a manufacturing flaw. It is the design.</p>

      <p>A cook who understands the wok uses both zones simultaneously. Proteins go to the centre — flash-seared at maximum temperature, crust forming in seconds. Aromatics — the garlic, the ginger, the spring onion — are held at the edge, alive and fragrant, warmed but not incinerated. Final assembly travels across both zones in a single motion. The food experiences two different thermal environments within the space of one pan and thirty seconds. No domestic hob can create this gradient. The single-zone limitation of a home burner is not a matter of technique — it is a hard constraint of the hardware.</p>

      <h2 class="article-section-head">III. Wok Hei — The Breath of the Wok</h2>

      <p>Wok Hei is frequently mistranslated as smoky flavour. It is more chemically specific than that.</p>

      <p>When cooking oil contacts a wok surface at 300°C and above, it does not simply heat. It partially aerosolizes — fine oil droplets become airborne in the convective column above the flame, briefly combust in contact with the burner, and deposit as oxidized lipid compounds back onto the surface of the food. This is the chemistry of Wok Hei: not passive smoke but a flash of controlled combustion, measurable in milliseconds, that leaves a distinct chemical signature on every protein and carbohydrate it touches.</p>

      <blockquote class="article-pullquote">
        <p>The Maillard reaction operates at wok temperatures not over minutes but over seconds. The result is a crust that forms before the interior protein has time to tighten. Tender inside. Seared outside. A textural outcome that should not, by the logic of slower cooking, be possible.</p>
      </blockquote>

      <p>It is possible because of thermal mass. The industrial wok — thick carbon steel, preheated continuously through a full service — carries sufficient stored heat to absorb the temperature drop of cold, wet ingredients and recover to operating temperature within seconds. A thin domestic pan loses 50 to 80°C on contact and cannot recover fast enough. The food releases moisture. The moisture converts to steam. The steam drops the surface below the Maillard threshold. The crust does not form. The Wok Hei window closes before it has opened. This is not a failure of technique. It is a failure of infrastructure.</p>

      <h2 class="article-section-head">IV. Kinetic Rhythm</h2>

      <p>The toss is not theatrical. It is a mechanical input with a specific thermal function.</p>

      <p>When a cook lifts and returns the wok in the characteristic forward-up-back motion, the food follows a calculated arc. Every ingredient briefly leaves the metal surface, passes through the superheated air column above the blast zone, and returns to a different contact point on the pan. This rotation serves two simultaneous purposes: it ensures even exposure to the maximum-temperature zone, and it prevents surface moisture accumulation that would drop the pan below the Maillard threshold.</p>

      <p>This is kinetic rhythm — a repeated, calibrated mechanical input that maintains the thermal and moisture conditions necessary for correct cooking. Noodles take three passes. Proteins take two. Vegetables, depending on cell density and water content, take one pass at centre and one at the edge. The sequence is not purely instinct. It is a learned mechanical process, refined through repetition, governed by the physics of heat transfer and the chemistry of the ingredients in the pan. The motion is as purposeful as a machinist's cut. It looks simple because it has been performed correctly ten thousand times.</p>

      <h2 class="article-section-head">V. Craft Versus Showmanship</h2>

      <p>There is a category of restaurant that has turned the wok into scenery. Open kitchens with jets of controlled flame, dramatic tosses timed for the dining room, fire that rises not because the thermal process demands it but because the guest has been conditioned to expect it. The wok functions in these settings as a prop — the spectacle of technique substituted for its substance.</p>

      <p>The chemistry of Wok Hei is indifferent to observation. It requires the correct surface temperature, the correct oil aerosolization conditions, and the correct kinetic input at the correct moment. These are quiet variables. They produce no visible drama. The result arrives in a bowl: a crust on the chicken that should not coexist with the tenderness of the interior, a fried rice where each grain of aged long-grain aromatic rice is separate and carries a faint carbonized depth that reads as complexity rather than damage. We do not cook for the fire-show. We cook for the chemical result. The distinction is apparent only when you eat the difference.</p>

      <h2 class="article-section-head">The Infrastructure Argument</h2>

      <p>You cannot install an industrial wok burner in a residential kitchen. The gas supply infrastructure does not support it. The ventilation required to handle aerosolized oil at operating volume exceeds domestic building codes. The thermal mass of a carbon steel wok preheated through a full service cannot be approximated by equipment purchased from a homeware shop.</p>

      <p>This is not a criticism of home cooking. It is a different discipline operating under different constraints, producing different and entirely valid results. It is simply an explanation of why the food at Mister Wok tastes the way it does, and why it tastes different everywhere else.</p>

      <p>The infrastructure exists at three addresses in Nairobi. The seasoned surface is ready. The blast zone is at temperature. The kinetic rhythm begins the moment the order arrives.</p>

    </div>

    <footer class="article-footer">
      <div class="article-cta-block">
        <div class="article-cta-label">Experience the difference</div>
        <div class="article-cta-row">
          <button type="button"
            class="article-cta-btn article-cta-primary"
            data-modal-trigger="order"
            data-order-btn="true"
            aria-haspopup="dialog"
            aria-controls="modal">
            <span class="cta-flame" aria-hidden="true">ðŸ”¥</span> Order Now
          </button>
          <a href="/parklands/menu.html" class="article-cta-btn article-cta-secondary">
            ðŸœ Full Menu
          </a>
        </div>
      </div>
      <div class="article-related">
        <div class="article-related-label">Continue reading</div>
        <div class="article-related-grid">
          <a href="/journal/long-grain-aromatic-rice.html" class="article-related-card">
            <div class="article-related-kicker">Ingredients</div>
            <div class="article-related-title">Aromatic Long-Grain Rice</div>
          </a>
          <a href="/journal/spring-rolls-gold-prosperity.html" class="article-related-card">
            <div class="article-related-kicker">Culture</div>
            <div class="article-related-title">Spring Rolls &amp; Gold Ingots</div>
          </a>
          <a href="/journal/decade-at-the-flame.html" class="article-related-card">
            <div class="article-related-kicker">Retrospective</div>
            <div class="article-related-title">Still at the Flame · Ten Years</div>
          </a>
        </div>
      </div>
    </footer>

  </article>
</main>"""

MAIN_LONG_GRAIN = """<main class="article-wrap" id="main-content">
  <article itemscope itemtype="https://schema.org/BlogPosting">
    <meta itemprop="url" content="https://misterwok.net/journal/long-grain-aromatic-rice.html">
    <meta itemprop="datePublished" content="2026-02-14">
    <meta itemprop="dateModified" content="2026-05-24">

    <header class="article-header">
      <nav class="article-breadcrumb" aria-label="Breadcrumb">
        <a href="/">Home</a>
        <span aria-hidden="true">›</span>
        <a href="/journal/">The Journal</a>
        <span aria-hidden="true">›</span>
        <span aria-current="page">Aromatic Long-Grain Rice</span>
      </nav>
      <div class="article-kicker">The Wok Journal · Ingredients</div>
      <h1 class="article-title" itemprop="headline">Aromatic Long-Grain Rice: The First Technical Decision</h1>
      <p class="article-subtitle">Why the grain determines the dish — and why wok fried rice begins at the supply level, not at the flame</p>
      <p class="article-lead" itemprop="description">There is a version of fried rice that is technically correct and culinarily wrong. The technique is sound. The wok temperature is correct. The timing is precise. The grain is fresh. That last variable undoes everything else. Wok fried rice is not a technique problem. It is a grain problem first.</p>
      <div class="article-meta">
        <span class="article-meta-item">The Wok Journal · Ingredients</span>
        <span class="article-meta-dot" aria-hidden="true">·</span>
        <time class="article-meta-item" datetime="2026-02-14" itemprop="datePublished">February 2026</time>
      </div>
      <div class="article-hero-wrap" aria-label="Mister Wok wok-tossed aromatic long-grain fried rice">
        <img
          src="/images/food/wok-toss-rice.webp"
          alt="Mister Wok Yong Chow fried rice — aged aromatic long-grain rice, wok-tossed at 300°C"
          width="900"
          height="506"
          loading="eager"
          decoding="async"
          itemprop="image"
          class="article-hero-img">
      </div>
    </header>

    <div class="article-body" itemprop="articleBody">

      <h2 class="article-section-head">What the Selection Criteria Are</h2>

      <p>Most rice is selected and sold at its freshest. Fresh rice has high moisture content, high surface starch, and high gelatinisation potential — characteristics that make it excellent for steaming and for absorbing sauce. These same characteristics make it the wrong rice for a wok.</p>

      <p>At Mister Wok, the rice used across every fried rice dish on the menu — from Plain Fried Rice to the Shrimp Egg and Chicken Yong Chow Rice — is an aged aromatic long-grain variety selected specifically for its behaviour under high-heat wok conditions. The selection is not a matter of flavour preference. It is a technical specification.</p>

      <h2 class="article-section-head">Why Age Changes the Grain</h2>

      <p>Rice loses moisture as it ages. This is generally considered a storage problem. In the context of wok cooking, it is a performance specification.</p>

      <p>A grain of fresh rice carries approximately 13 to 14 percent moisture content by weight. An aged grain, stored correctly over six months to a year, drops below 12 percent. That two percent difference does not sound significant. At 300°C, it is the difference between a grain that steams and a grain that sears.</p>

      <blockquote class="article-pullquote">
        <p>When high-moisture rice enters a hot wok, the surface water flashes to steam before the Maillard reaction can occur. The grain softens before it colours. The exterior never develops the faint carbonised depth that distinguishes correctly made fried rice from rice that was merely heated with other ingredients.</p>
      </blockquote>

      <p>The aged grain enters the wok dry. The surface contacts the metal at operating temperature. The Maillard reaction begins within seconds. The exterior sets before the interior loses its structure. The grain stays separate because there is no surface moisture binding it to its neighbours.</p>

      <h2 class="article-section-head">The Separation Standard</h2>

      <p>The benchmark of a correctly fired fried rice is grain separation. Every grain independent. No clumping. No starch paste binding the mass together. Each piece of egg distinct. Each fragment of protein sitting alongside the grain rather than fused to it.</p>

      <p>This standard is not achievable with fresh rice regardless of technique. A skilled cook using fresh rice will produce a competent dish. They will not produce grain separation at this level, because the physics do not allow it. Surface moisture binds. Steam softens. The window for correct searing closes before it opens.</p>

      <h2 class="article-section-head">Technique and Grain as Co-Dependents</h2>

      <p>The wok technique — the blast zone, the kinetic rhythm, the thermal mass of preheated carbon steel — was developed in conjunction with aged rice, not independently of it. Chinese wok cookery evolved around aged long-grain precisely because the technique demands it.</p>

      <p>A cook who understands the wok and uses the wrong rice is operating half a system. The equipment and the motion are present. The raw material cannot respond correctly. The result will be edible and it will fall short of what the technique is designed to produce. This is why the grain does not change. It is not a premium ingredient in the decorative sense. It is a functional component of the dish. Changing it changes the dish.</p>

      <h2 class="article-section-head">What This Means at the Table</h2>

      <p>The guest does not need to know any of this to appreciate the result. The separation is visible before the first forkful. The texture is apparent in the first bite — each grain with its own integrity, the slight resistance that comes from a correctly seared exterior, the faint char that reads as depth rather than damage.</p>

      <p>This is what correct wok fried rice tastes like. It tastes like a decision made at the supply level, enforced through technique, and delivered at 300°C.</p>

    </div>

    <footer class="article-footer">
      <div class="article-cta-block">
        <div class="article-cta-label">Order the Yong Chow Rice</div>
        <div class="article-cta-row">
          <button type="button"
            class="article-cta-btn article-cta-primary"
            data-modal-trigger="order"
            data-order-btn="true"
            aria-haspopup="dialog"
            aria-controls="modal">
            <span class="cta-flame" aria-hidden="true">🔥</span> Order Now
          </button>
          <a href="/parklands/menu.html" class="article-cta-btn article-cta-secondary">
            🍜 Full Menu
          </a>
        </div>
      </div>
      <div class="article-related">
        <div class="article-related-label">Continue reading</div>
        <div class="article-related-grid">
          <a href="/journal/wok-hei-physics.html" class="article-related-card">
            <div class="article-related-kicker">Technique</div>
            <div class="article-related-title">The Physics of the Flame</div>
          </a>
          <a href="/journal/spring-rolls-gold-prosperity.html" class="article-related-card">
            <div class="article-related-kicker">Craft</div>
            <div class="article-related-title">Spring Rolls &amp; Gold Ingots</div>
          </a>
          <a href="/journal/decade-at-the-flame.html" class="article-related-card">
            <div class="article-related-kicker">Retrospective</div>
            <div class="article-related-title">Still at the Flame · Ten Years</div>
          </a>
        </div>
      </div>
    </footer>

  </article>
</main>"""

MAIN_BIRTHDAY = """<main class="article-wrap" id="main-content">
  <article itemscope itemtype="https://schema.org/BlogPosting">
    <meta itemprop="url" content="https://misterwok.net/journal/birthday-catering-guide.html">
    <meta itemprop="datePublished" content="2026-05-22">
    <meta itemprop="dateModified" content="2026-05-22">

    <header class="article-header">
      <nav class="article-breadcrumb" aria-label="Breadcrumb">
        <a href="/">Home</a>
        <span aria-hidden="true">›</span>
        <a href="/journal/">The Journal</a>
        <span aria-hidden="true">›</span>
        <span aria-current="page">The Architecture of a Celebration</span>
      </nav>
      <div class="article-kicker">The Wok Journal · Private Dining &amp; Events</div>
      <h1 class="article-title" itemprop="headline">The Architecture of a Celebration</h1>
      <p class="article-subtitle">How Mister Wok became the quiet partner behind Nairobi's most significant tables</p>
      <p class="article-lead" itemprop="description">There is a photograph that surfaces occasionally — a table at the Parklands branch, set for twelve, where the youngest guest is one year old and the eldest is somewhere in her late eighties. Four generations. One table. The adults at the centre of that image first came to Mister Wok when they were young professionals, sometime in the years after the restaurant opened on Valentine's Day 2004. They have not stopped coming since.</p>
      <div class="article-meta">
        <span class="article-meta-item">The Wok Journal · Private Dining &amp; Events</span>
        <span class="article-meta-dot" aria-hidden="true">·</span>
        <time class="article-meta-item" datetime="2026-05-22" itemprop="datePublished">May 2026</time>
      </div>
      <div class="article-hero-wrap" aria-label="Mister Wok sizzler platter — fresh on-site catering">
        <img
          src="/images/food/prawn-sizzler.webp"
          alt="Mister Wok prawn sizzler — the centrepiece dish for celebrations and private dining events in Nairobi"
          width="900"
          height="506"
          loading="eager"
          decoding="async"
          itemprop="image"
          class="article-hero-img">
      </div>
    </header>

    <div class="article-body" itemprop="articleBody">

      <h2 class="article-section-head">An Inheritance, Not a Loyalty Programme</h2>

      <p>They came first as a couple — a recommendation from a colleague, a restaurant on Kolobot Road that someone said was worth trying. They came back because the food was correct, and because correct food at a table you trust becomes, over time, a ritual.</p>

      <p>They called ahead on the evenings of pregnancy cravings — the Tom Yum at eleven weeks, the Dim Sum at thirty-two, the Hot and Sour Soup on a rainy Thursday night because there are cravings that only a specific bowl resolves and no substitution will satisfy them. They brought their children when the children were old enough to hold chopsticks. Now those children bring their own children, and the table is larger than it has ever been.</p>

      <p>This is not a loyalty story. It is an inheritance story. Mister Wok has become, for certain families in this city, a permanent fixture in the architecture of how significant moments are marked — as expected and as reliable as any other constant in a life well-lived. We did not design this. We simply remained at the same standard, at the same address, for long enough that the city grew its memories around us.</p>

      <h2 class="article-section-head">The Professional Standard</h2>

      <p>The corporate table operates by a different logic, but it arrives at the same requirement: the quality of the hospitality must reflect the seriousness of the host.</p>

      <p>A law firm hosting a client appreciation dinner has spent months building the relationship being celebrated that evening. A multinational engineering team marking the close of a major infrastructure contract is recognising twelve months of precision under pressure. A banking division gathering to acknowledge a quarter well-executed is sending a message to the people in that room about how they are valued. In each case, the food is not incidental to the occasion. It is part of the statement.</p>

      <blockquote class="article-pullquote">
        <p>Pre-made food, delivered and reheated, is efficient. It is also visible as such to anyone who has eaten well before. It signals that the logistics were managed, not that the evening was considered.</p>
      </blockquote>

      <p>Fresh-on-site cooking signals something different. When the Mister Wok equipment arrives at your venue and the cooking begins in the room — the heat building, the first garlic hitting the wok surface, the aroma of ginger and high-heat oil reaching the guests before any plate has been set — it communicates that the host took this seriously. That this particular table was worth doing properly. Mister Wok has cooked for board-level dinners, product launches for a hundred guests, and intimate client appreciation tables of twelve in Gigiri living rooms. The standard does not change between scales.</p>

      <h2 class="article-section-head">The Ritual of the Flame</h2>

      <p>There is a quality to food cooked in the presence of the people who will eat it that no logistics chain can replicate. The aroma arrives before the plate does. The sound of the wok at correct temperature — that sustained, confident sizzle — creates an anticipation that pre-plated food cannot manufacture.</p>

      <p>Dishes arrive in sequence because the kitchen is on-site and responsive, not because a delivery schedule was optimised three hours earlier. The Tom Yum comes out hot because it was made hot. The spring rolls are crisp because they came off the flame sixty seconds ago. The sizzler arrives at the table still sizzling, because the table is forty metres from the wok, not forty kilometres from a central kitchen. These are not small distinctions. They are the entire distinction.</p>

      <p>The guests notice the food. That is the point.</p>

      <h2 class="article-section-head">The Spectrum of the Table</h2>

      <p>We have cooked for first birthdays and eighty-eighth-year celebrations. The youngest guest at a Mister Wok catered event was twelve months old. The eldest, at a Muthaiga garden lunch that ran well past its original booking, was eighty-eight and requested the Tom Kha Soup before anyone else had been seated.</p>

      <p>Both guests ate well. The menu accommodates every generation at the same table without the compromises that a single-demographic approach implies. The Dim Sum for the children. The Lamb Ribs for the table's established preferences. The Ginger Crab for the guest who knows Parklands well enough to know it is worth ordering. The Hot Beverages for the end of the evening, when the conversation has slowed to the kind that only happens at tables where everyone has eaten well.</p>

      <p>A celebration is not a single course. It is the arc of an evening — arrival, anticipation, the meal, the settling. We cook for the whole arc, not just the centrepiece.</p>

      <h2 class="article-section-head">The Invitation</h2>

      <p>Whether you are hosting a board-level appreciation dinner, a four-generation Sunday lunch, a product launch for a hundred guests, or something the categories do not quite cover — the process begins with a conversation. We plan the menu around the occasion. We bring the flame to you.</p>

    </div>

    <footer class="article-footer">
      <div class="article-cta-block">
        <div class="article-cta-label">Plan your event</div>
        <div class="article-cta-row">
          <a href="mailto:events@misterwok.net"
            class="article-cta-btn article-cta-primary"
            aria-label="Email Mister Wok events team">
            âœ‰ events@misterwok.net
          </a>
          <a href="/parklands/menu.html" class="article-cta-btn article-cta-secondary">
            ðŸœ View Full Menu
          </a>
        </div>
        <p class="article-cta-note">Tell us the occasion, the guest count, and the date. We take it from there.</p>
      </div>
      <div class="article-related">
        <div class="article-related-label">Continue reading</div>
        <div class="article-related-grid">
          <a href="/journal/decade-at-the-flame.html" class="article-related-card">
            <div class="article-related-kicker">Retrospective</div>
            <div class="article-related-title">Still at the Flame · Ten Years</div>
          </a>
          <a href="/journal/halal-wok-nairobi.html" class="article-related-card">
            <div class="article-related-kicker">Values</div>
            <div class="article-related-title">Halal-Assured · 22 Years</div>
          </a>
          <a href="/journal/wok-hei-physics.html" class="article-related-card">
            <div class="article-related-kicker">Technique</div>
            <div class="article-related-title">The Physics of the Flame</div>
          </a>
        </div>
      </div>
    </footer>

  </article>
</main>"""

MAIN_HALAL = """<main class="article-wrap" id="main-content">
  <article itemscope itemtype="https://schema.org/BlogPosting">
    <meta itemprop="url" content="https://misterwok.net/journal/halal-wok-nairobi.html">
    <meta itemprop="datePublished" content="2026-02-14">
    <meta itemprop="dateModified" content="2026-05-22">

    <header class="article-header">
      <nav class="article-breadcrumb" aria-label="Breadcrumb">
        <a href="/">Home</a>
        <span aria-hidden="true">›</span>
        <a href="/journal/">The Journal</a>
        <span aria-hidden="true">›</span>
        <span aria-current="page">Halal-Assured</span>
      </nav>
      <div class="article-kicker">The Wok Journal · Values</div>
      <h1 class="article-title" itemprop="headline">Halal-Assured: A Kitchen Standard, Not a Certificate</h1>
      <p class="article-subtitle">Twenty-two years of a discipline that begins before the wok is lit</p>
      <p class="article-lead" itemprop="description">The halal assurance at Mister Wok is not a sticker on the door. It is not a certificate renewed annually and filed in a folder. It is a sourcing discipline, a procurement standard, and a kitchen protocol that has operated without interruption across three branches and twenty-two years of service. It predates the conversation about it.</p>
      <div class="article-meta">
        <span class="article-meta-item">The Wok Journal · Values</span>
        <span class="article-meta-dot" aria-hidden="true">·</span>
        <time class="article-meta-item" datetime="2026-02-14" itemprop="datePublished">February 2026</time>
      </div>
      <div class="article-hero-wrap" aria-label="Mister Wok halal-assured kitchen">
        <img
          src="/images/food/dim-sum-main-index.webp"
          alt="Mister Wok dim sum — halal-assured, hand-crafted, served across three Nairobi branches"
          width="900"
          height="506"
          loading="eager"
          decoding="async"
          itemprop="image"
          class="article-hero-img">
      </div>
    </header>

    <div class="article-body" itemprop="articleBody">

      <h2 class="article-section-head">Where It Begins</h2>

      <p>Halal assurance in a professional kitchen begins at the supply chain, not at the point of cooking. The question is not whether the cooking method is correct — it is whether the ingredient that enters the kitchen meets the standard before it arrives. Mister Wok sources all meat and poultry from suppliers whose halal certification is verified and current. This is not a request made at the point of order. It is a standing requirement of the supplier relationship.</p>

      <p>The discipline runs in one direction only. There is no tiered system — no halal-on-request, no separate preparation area activated for certain tables. The standard applies to every ingredient, every station, every plate, every service. A kitchen that maintains halal assurance selectively is not maintaining it. It is managing a perception.</p>

      <h2 class="article-section-head">The Capital Centre Standard</h2>

      <p>Capital Centre on Mombasa Road is the halal flagship. This designation reflects the community the branch was built to serve, and the standard has been maintained consistently since the branch opened. The guest who comes to Capital Centre does not need to ask whether the kitchen is halal-assured. That question was answered before the branch opened.</p>

      <p>The Parklands and Two Rivers branches operate under the same sourcing standards. The halal assurance is not branch-specific in its discipline — it is site-specific in its community significance. Capital Centre carries the certification prominently because that community has carried Mister Wok prominently in return.</p>

      <h2 class="article-section-head">What It Means in a Wok Kitchen</h2>

      <p>A wok kitchen operates at high heat, high speed, and high volume. The discipline of halal assurance in this environment is not ceremonial — it is structural. Cross-contamination in a wok kitchen can happen faster than in a conventional kitchen because of the shared surface, the shared flame, and the pace of service.</p>

      <blockquote class="article-pullquote">
        <p>Twenty-two years of this practice has made the protocol invisible — it runs in the background of every service, unremarked and uninterrupted, the way any standard that has been properly embedded should operate.</p>
      </blockquote>

      <p>The Mister Wok kitchen manages this through protocol, not hope. Separate utensils, designated preparation surfaces, consistent supplier verification, and a kitchen culture in which the standard is not an imposition but a baseline.</p>

      <h2 class="article-section-head">The Guest's Position</h2>

      <p>The guest who chooses Mister Wok on the basis of halal assurance is making a decision that requires trust. They cannot see the supply chain. They cannot observe the procurement documentation. They are extending trust to a kitchen and expecting that trust to be honoured.</p>

      <p>Mister Wok has honoured it since 2004. That is the only claim worth making. Not the certification. Not the language. The twenty-two-year record.</p>

      <h2 class="article-section-head">A Permanent Standard</h2>

      <p>Halal assurance at Mister Wok is not a feature. It was part of the kitchen's identity before the vocabulary around it became commercially useful. It will remain part of the kitchen's identity after the conversation has moved on to whatever the next certification trend produces.</p>

      <p>The wok is lit the same way every morning. The sourcing standard is the same. The protocol is the same. The plate that arrives at the table is the product of a kitchen that has never needed to be reminded why the standard matters.</p>

    </div>

    <footer class="article-footer">
      <div class="article-cta-block">
        <div class="article-cta-label">Visit your nearest branch</div>
        <div class="article-cta-row">
          <button type="button"
            class="article-cta-btn article-cta-primary"
            data-modal-trigger="order"
            data-order-btn="true"
            aria-haspopup="dialog"
            aria-controls="modal">
            <span class="cta-flame" aria-hidden="true">ðŸ”¥</span> Order Now
          </button>
          <a href="/parklands/menu.html" class="article-cta-btn article-cta-secondary">
            ðŸœ Full Menu
          </a>
        </div>
      </div>
      <div class="article-related">
        <div class="article-related-label">Continue reading</div>
        <div class="article-related-grid">
          <a href="/journal/decade-at-the-flame.html" class="article-related-card">
            <div class="article-related-kicker">Retrospective</div>
            <div class="article-related-title">Still at the Flame · Ten Years</div>
          </a>
          <a href="/journal/wok-hei-physics.html" class="article-related-card">
            <div class="article-related-kicker">Technique</div>
            <div class="article-related-title">The Physics of the Flame</div>
          </a>
          <a href="/journal/spring-rolls-gold-prosperity.html" class="article-related-card">
            <div class="article-related-kicker">Craft</div>
            <div class="article-related-title">Spring Rolls &amp; Gold Ingots</div>
          </a>
        </div>
      </div>
    </footer>

  </article>
</main>"""


def load_template():
    with open(TEMPLATE_PATH, encoding='utf-8') as f:
        return f.read()


def fix_shell_encoding(html):
    """Normalize shell encoding and stale nav copy."""
    html = html.replace('138 dishes', '229 dishes')
    replacements = [
        ('4.3—', '4.3★ ·'),
        ('4.2—', '4.2★ ·'),
        ('4.1—', '4.1★ ·'),
        ('? Halal-Assured', '✓ Halal-Assured'),
        ('? Edit My Details', '✎ Edit My Details'),
        ('<span class="modal-opt-arrow" aria-hidden="true">?</span>', '<span class="modal-opt-arrow" aria-hidden="true">→</span>'),
        ('Explore the full Journal ?', 'Explore the full Journal →'),
        ('Parklands <span>?</span>', 'Parklands <span>→</span>'),
        ('Capital Centre <span>?</span>', 'Capital Centre <span>→</span>'),
        ('Two Rivers <span>?</span>', 'Two Rivers <span>→</span>'),
        ('— 2004—2026', '© 2004–2026'),
    ]
    for old, new in replacements:
        html = html.replace(old, new)
    return html


def assemble(template, head, main, extra_css=None):
    html = fix_shell_encoding(template)
    html = re.sub(
        r'<title>.*?(?=<style>)',
        head.strip() + '\n  ',
        html,
        count=1,
        flags=re.DOTALL,
    )
    html = re.sub(
        r'<main class="article-wrap"[^>]*>.*?</main>',
        main.strip(),
        html,
        count=1,
        flags=re.DOTALL,
    )
    if extra_css and 'article-cta-note' not in html:
        html = html.replace('  </style>', extra_css.rstrip() + '\n  </style>', 1)
    return html


def build_articles():
    template = load_template()
    return {
        'SPRING_ROLLS': assemble(template, HEAD_SPRING, MAIN_SPRING),
        'WOK_HEI': assemble(template, HEAD_WOK_HEI, MAIN_WOK_HEI),
        'LONG_GRAIN': assemble(template, HEAD_LONG_GRAIN, MAIN_LONG_GRAIN),
        'BIRTHDAY': assemble(template, HEAD_BIRTHDAY, MAIN_BIRTHDAY, ARTICLE_CSS_EXTRA),
        'HALAL': assemble(template, HEAD_HALAL, MAIN_HALAL),
    }


SPRING_ROLLS, WOK_HEI, LONG_GRAIN, BIRTHDAY, HALAL = build_articles().values()

articles = {
    'journal/spring-rolls-gold-prosperity.html': SPRING_ROLLS,
    'journal/wok-hei-physics.html': WOK_HEI,
    'journal/long-grain-aromatic-rice.html': LONG_GRAIN,
    'journal/birthday-catering-guide.html': BIRTHDAY,
    'journal/halal-wok-nairobi.html': HALAL,
}


def write(rel_path, content):
    path = os.path.join(BASE, rel_path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'  WRITTEN  {rel_path}')


if __name__ == '__main__':
    print('patch_journal_v2.py — Mister Wok Journal Overwrite')
    print('=' * 52)
    for rel, content in articles.items():
        write(rel, content)
    print('=' * 52)
    print(f'Done. {len(articles)} files written.')
