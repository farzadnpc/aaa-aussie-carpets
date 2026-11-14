#!/usr/bin/env python3
"""
Builds every page of the AAA Aussie Carpets website.

    python3 tools/build.py                      rebuild all pages
    python3 tools/build.py ~/Downloads/x.csv    import a new suburbs CSV from Google Sheets, then rebuild

Edit the text in this file (services, FAQs, etc.) and rebuild rather than editing the HTML files,
because a rebuild overwrites them.
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://www.aaaaussiecarpets.com"
NAME = "AAA Aussie Carpets"
PHONE = "0415 850 095"
PHONE_TEL = "+61415850095"
STREET = "114 Dontons Ave"
CITY = "Melbourne"
REGION = "VIC"
SOCIAL = "aaaaussiecarpets"
TODAY = "2026-11-14"
CUR = ' aria-current="page"'

# ---------------------------------------------------------------- icons
I = {
 "phone": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/></svg>',
 "chev": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg>',
 "check": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12l5 5L20 7"/></svg>',
 "arrow": '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
 "pin": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22s7-6.2 7-12a7 7 0 0 0-14 0c0 5.8 7 12 7 12z"/><circle cx="12" cy="10" r="2.6"/></svg>',
 "globe": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15 15 0 0 1 0 20M12 2a15 15 0 0 0 0 20"/></svg>',
 "insta": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor"/></svg>',
 "fb": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M14 8V6.2c0-.8.2-1.2 1.4-1.2H17V2h-2.6C11.3 2 10 3.5 10 6v2H8v3h2v11h4V11h2.6l.4-3z"/></svg>',
 "x": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.8 3h3.1l-6.8 7.7L22 21h-6.2l-4.9-6.4L5.3 21H2.2l7.2-8.3L1.8 3h6.4l4.4 5.8L17.8 3zm-1.1 16.2h1.7L7.4 4.7H5.6l11.1 14.5z"/></svg>',
 "roll": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><ellipse cx="6" cy="8" rx="3" ry="5"/><path d="M6 3h12a3 5 0 0 1 0 10H6M9 8h12M18 13v8H3v-3"/></svg>',
 "tools": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L3 18l3 3 6.3-6.3a4 4 0 0 0 5.4-5.4l-2.5 2.5-2.4-.6-.6-2.4 2.5-2.5z"/></svg>',
 "tiles": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="3" width="8" height="8" rx="1"/><rect x="13" y="3" width="8" height="8" rx="1"/><rect x="3" y="13" width="8" height="8" rx="1"/><rect x="13" y="13" width="8" height="8" rx="1"/></svg>',
 "stairs": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 21h5v-5h5v-5h5V6h3"/><path d="M3 21V3"/></svg>',
 "building": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="4" y="2" width="16" height="20" rx="1"/><path d="M9 22v-4h6v4M8 6h2M14 6h2M8 10h2M14 10h2M8 14h2M14 14h2"/></svg>',
}

# ---------------------------------------------------------------- services
SERVICES = [
 {
  "slug": "carpet-supply-installation", "nav": "Carpet supply & installation", "icon": "roll",
  "title": "Carpet Supply & Installation Melbourne",
  "h1": "Carpet supply & installation in Melbourne",
  "desc": "Quality carpet supplied and professionally installed across Melbourne. Wool, nylon and blends, new underlay, tight stretches and clean seams. Free quotes — call 0415 850 095.",
  "card": "New carpet for bedrooms, living areas and whole homes — supplied, measured and installed by our own team.",
  "img": "grey-carpet-living-room", "img_w": 1242, "img_h": 929, "img_alt": "Grey carpet installed in a bright Melbourne living room",
  "lead": "From a single bedroom to the whole house, we help you choose the right carpet, then install it properly — tight, flat and finished cleanly at every doorway.",
  "body": """
<h2>Carpet that suits the way you live</h2>
<p>Every home is different. A busy family room with kids and pets needs something tougher than a guest bedroom, and a rental property needs something different again. We'll talk you through the options and bring samples so you can see and feel them in your own light.</p>
<ul class="check-list">
  <li><strong>Wool</strong> — natural, soft underfoot and long-lasting</li>
  <li><strong>Nylon &amp; solution-dyed nylon</strong> — hard-wearing and stain resistant</li>
  <li><strong>Polyester &amp; blends</strong> — great value with a soft feel</li>
  <li><strong>Loop pile, cut pile, twist &amp; plush</strong> styles in a wide range of colours</li>
</ul>
<h2>What's included in a carpet installation</h2>
<ul class="check-list">
  <li>Measure and free, no-obligation quote</li>
  <li>Uplift and removal of old carpet and underlay</li>
  <li>New underlay matched to your carpet and traffic</li>
  <li>Power-stretched installation so the carpet stays flat</li>
  <li>Neat seams, trims and transitions to tiles or timber</li>
  <li>Clean-up when we're done</li>
</ul>
<h2>Why the installation matters</h2>
<p>Even the best carpet will ripple, fray or show seams if it's laid poorly. Our installers stretch every room properly, plan seams away from traffic and light, and finish doorways and edges so they look sharp and last. Tough floors, built to last.</p>
""",
  "faqs": [
   ("How long does carpet installation take?", "Most single rooms are done in a few hours, and a typical house is usually finished in one to two days. We'll give you a time frame with your quote."),
   ("Do you remove the old carpet?", "Yes. We can uplift and take away your old carpet and underlay as part of the job — just let us know when you ask for a quote."),
   ("Do I need new underlay?", "In most cases, yes. Old underlay is often flattened or worn, and fresh underlay makes new carpet feel better and last longer. We'll advise you on site."),
  ],
 },
 {
  "slug": "carpet-repairs-restretching", "nav": "Repairs & restretching", "icon": "tools",
  "title": "Carpet Repairs & Re-stretching Melbourne",
  "h1": "Carpet repairs & re-stretching in Melbourne",
  "desc": "Rippled, loose or damaged carpet? We re-stretch, patch burns and stains, fix pet damage and repair seams across Melbourne. Call AAA Aussie Carpets on 0415 850 095.",
  "card": "Rippled or loose carpet, burns, pet damage and split seams — repaired so you don't have to replace the whole room.",
  "img": "soft-plush-carpet-texture", "img_w": 800, "img_h": 999, "img_alt": "Close-up of soft plush carpet after a professional repair",
  "lead": "Bumps, ripples, burns and torn seams don't always mean new carpet. Our repairs bring your floors back to looking right — for a fraction of the cost.",
  "body": """
<h2>Carpet re-stretching</h2>
<p>Ripples and loose carpet are trip hazards and wear out quickly. They usually come from carpet that wasn't stretched properly when it was laid, or from heavy furniture and humidity over time. We use a power stretcher to pull the carpet tight and re-fix it, leaving it flat and safe again.</p>
<h2>Carpet repairs we do</h2>
<ul class="check-list">
  <li>Patch repairs for burns, stains and holes</li>
  <li>Pet damage — scratched doorways and chewed edges</li>
  <li>Split or lifting seams re-joined</li>
  <li>Frayed edges and doorway trims replaced</li>
  <li>Re-laying carpet after water damage or plumbing work</li>
  <li>Lifting and re-laying carpet for other trades</li>
</ul>
<h2>Repair or replace?</h2>
<p>If your carpet is in good condition overall, a repair is usually the smart choice. If it's worn through in several spots, we'll tell you honestly whether replacing it makes more sense. Keeping offcuts from your original install makes patch repairs almost invisible.</p>
""",
  "faqs": [
   ("Can rippled carpet be fixed?", "Yes. Most ripples can be removed by re-stretching the carpet with a power stretcher and re-fixing it to the gripper strips."),
   ("Can you match a patch to my carpet?", "If you have an offcut from the original carpet we can usually make a near-invisible patch. If not, we can often take a piece from inside a wardrobe."),
   ("Is it worth repairing old carpet?", "If the carpet is otherwise in good shape, a repair costs far less than replacing a whole room. We'll give you an honest opinion when we see it."),
  ],
 },
 {
  "slug": "carpet-tiles", "nav": "Carpet tiles", "icon": "tiles",
  "title": "Carpet Tiles Supply & Installation Melbourne",
  "h1": "Carpet tiles in Melbourne",
  "desc": "Hard-wearing carpet tiles supplied and installed for offices, shops, home offices and rumpus rooms across Melbourne. Easy to maintain and replace. Free quotes.",
  "card": "Hard-wearing modular carpet tiles for offices, shops, home offices and rumpus rooms. Easy to replace one tile at a time.",
  "img": "carpet-samples-selection", "img_w": 800, "img_h": 1005, "img_alt": "Carpet tile and carpet samples laid out for selection",
  "lead": "Carpet tiles are tough, quick to install and easy to look after. If one gets damaged, you replace one tile — not the whole floor.",
  "body": """
<h2>Why choose carpet tiles?</h2>
<ul class="check-list">
  <li><strong>Hard-wearing</strong> — built for heavy foot traffic and office chairs</li>
  <li><strong>Easy to replace</strong> — swap out a stained or damaged tile in minutes</li>
  <li><strong>Fast installation</strong> — less disruption for your business or home</li>
  <li><strong>Design options</strong> — mix colours and lay patterns like quarter-turn, brick or ashlar</li>
  <li><strong>Access to services</strong> — lift tiles to get at floor-box cabling</li>
</ul>
<h2>Where carpet tiles work best</h2>
<p>Offices, shops, medical and professional suites, schools, gyms and community spaces — and at home in home offices, rumpus rooms, garages and home theatres. We'll help you choose a tile with the right backing and pile for your space.</p>
<h2>Proper floor preparation</h2>
<p>A carpet tile floor is only as good as what's under it. We check and prepare the subfloor, set out the room from the centre so cuts are even at the walls, and use the right adhesive so tiles stay put but can still be lifted later.</p>
""",
  "faqs": [
   ("Are carpet tiles good for homes?", "Yes — they're popular for home offices, rumpus rooms, garages and home theatres, where durability and easy replacement matter."),
   ("Can carpet tiles go over concrete?", "Yes. Carpet tiles are commonly installed straight over a clean, flat, dry concrete slab. We'll check the floor first."),
   ("Can you install outside business hours?", "For commercial jobs we can work around your trading hours to keep disruption to a minimum. Ask us when you request a quote."),
  ],
 },
 {
  "slug": "stairs-custom-work", "nav": "Stairs & custom work", "icon": "stairs",
  "title": "Carpet for Stairs & Custom Work Melbourne",
  "h1": "Stair carpet & custom work in Melbourne",
  "desc": "Specialist carpet installation for staircases, winders and landings in Melbourne — waterfall or wrapped finishes, runners and custom cuts. Call 0415 850 095.",
  "card": "Straight stairs, winders, landings and runners — carpeted with tight, crisp edges that look sharp and wear well.",
  "img": "carpeted-winder-staircase-melbourne", "img_w": 800, "img_h": 999, "img_alt": "Carpeted winder staircase with neat wrapped nosings in a Melbourne home",
  "lead": "Stairs are where a carpet layer's skill really shows. We take the time to get every tread, riser and winder tight and crisp.",
  "body": """
<h2>Stairs done properly</h2>
<p>Stairs take the most wear in a house and are the first place poor workmanship shows. Every step is measured, cut and fitted individually, with the carpet stretched hard over each nosing so it stays tight for years.</p>
<ul class="check-list">
  <li>Straight stairs, open stairs and curved or winder stairs</li>
  <li>Landings matched seamlessly to hallway carpet</li>
  <li>Waterfall finish or wrapped (Hollywood-style) finish</li>
  <li>Stair runners with exposed timber edges</li>
  <li>Heavy-duty underlay suited to stair wear</li>
</ul>
<h2>Waterfall or wrapped?</h2>
<p>A <strong>waterfall</strong> finish runs the carpet over the nosing and straight down to the next tread — quick and clean. A <strong>wrapped</strong> finish tucks the carpet tightly under each nosing for a tailored look. We'll show you both and recommend what suits your stairs and carpet.</p>
<h2>Custom work</h2>
<p>Odd-shaped rooms, bay windows, curved walls, built-in robes and joining carpet to other floors all need careful planning and cutting. Tell us what you've got and we'll make it work.</p>
""",
  "faqs": [
   ("Can you carpet winder stairs?", "Yes. Winder (turning) stairs are fitted step by step, with each winder cut and stretched individually for a tight, neat finish."),
   ("What carpet is best for stairs?", "A dense, hard-wearing carpet such as a tight loop or short cut pile in wool or nylon, over a firm underlay, holds up best on stairs."),
   ("Can you do stairs only?", "Yes. We regularly carpet just the stairs and landing, and can match them to existing carpet where possible."),
  ],
 },
 {
  "slug": "commercial-carpet", "nav": "Commercial properties", "icon": "building",
  "title": "Commercial Carpet Installation Melbourne",
  "h1": "Commercial carpet in Melbourne",
  "desc": "Commercial carpet and carpet tiles for offices, retail, rentals and strata across Melbourne. Reliable scheduling, after-hours installs and fast turnarounds. Free quotes.",
  "card": "Offices, shops, rentals and strata. Carpet tiles and broadloom installed on schedule, with minimal disruption.",
  "img": "carpet-samples-selection", "img_w": 800, "img_h": 1005, "img_alt": "Commercial carpet samples ready for a client to choose",
  "lead": "Reliable carpet supply and installation for businesses, property managers, landlords and builders — on time and with minimal disruption.",
  "body": """
<h2>Who we work with</h2>
<ul class="check-list">
  <li>Offices and professional suites</li>
  <li>Retail shops and showrooms</li>
  <li>Real estate agents, landlords and property managers</li>
  <li>Strata and owners corporations — common areas and hallways</li>
  <li>Builders and renovators</li>
</ul>
<h2>Built around your business</h2>
<p>We know downtime costs money. We'll plan the job with you, work in stages or outside trading hours where possible, and leave the space clean and ready to use.</p>
<h2>Rental &amp; end-of-lease carpet</h2>
<p>Need carpet replaced between tenants? We can turn rental properties around quickly with durable, good-value carpet that suits the property and the budget.</p>
""",
  "faqs": [
   ("Do you work after hours?", "For commercial jobs we can work around your trading hours where possible. Let us know your requirements when you ask for a quote."),
   ("Do you work with property managers?", "Yes. We work with landlords, real estate agents and property managers on rental properties, including end-of-lease carpet replacement."),
   ("Broadloom or carpet tiles for an office?", "Carpet tiles are usually the better choice for offices because they're hard-wearing and easy to replace. Broadloom can suit boardrooms and reception areas."),
  ],
 },
]

HOME_FAQS = [
 ("How much does carpet installation cost in Melbourne?", "The price depends on the carpet you choose, the underlay, the size and shape of the rooms and whether there are stairs. We give free, no-obligation quotes with a clear price before any work starts — call 0415 850 095 or send us a quote request."),
 ("Do you supply the carpet as well as install it?", "Yes. We supply and install, so you deal with one team from choosing your carpet through to the final clean-up."),
 ("How long does it take to carpet a house?", "Most single rooms take a few hours. A typical house is usually finished in one to two days, depending on size and stairs."),
 ("Do you remove and dispose of old carpet?", "Yes. We can uplift and take away old carpet and underlay as part of your job."),
 ("Can you fix carpet that has rippled or come loose?", "Yes. We re-stretch rippled and loose carpet with a power stretcher so it lies flat again, and repair seams, burns and pet damage."),
 ("Do you carpet stairs?", "Yes — straight stairs, winders and landings, with a waterfall or wrapped finish."),
 ("What areas do you service?", "We install carpet right across Melbourne, including the inner city and the northern, eastern, south-eastern, western and bayside suburbs."),
]

AREAS = [
 ("Melbourne CBD & inner city", "Southbank, Docklands, Richmond, Carlton, Fitzroy, South Yarra, St Kilda"),
 ("Northern suburbs", "Brunswick, Coburg, Preston, Reservoir, Thomastown, Epping, Craigieburn"),
 ("Eastern suburbs", "Box Hill, Doncaster, Ringwood, Glen Waverley, Croydon, Boronia"),
 ("South-eastern suburbs", "Dandenong, Narre Warren, Berwick, Clayton, Springvale, Cranbourne"),
 ("Western suburbs", "Footscray, Sunshine, Werribee, Point Cook, Caroline Springs, Melton"),
 ("Bayside", "Brighton, Sandringham, Cheltenham, Mentone, Mordialloc, Frankston"),
]

GALLERY = [
 ("carpeted-winder-staircase-melbourne", 800, 999, "Carpeted winder staircase with wrapped nosings", "Winder staircase"),
 ("grey-carpet-living-room", 1242, 929, "Grey carpet in a modern living room", "Living room carpet"),
 ("staircase-carpet-installation", 800, 1422, "Staircase carpet installation in progress with floor protection", "Staircase install in progress"),
 ("woven-loop-carpet-closeup", 800, 993, "Close-up of a woven loop pile carpet", "Woven loop pile"),
 ("carpeted-stair-landing", 800, 1083, "Carpeted stair landing in a light neutral tone", "Stair landing"),
 ("soft-plush-carpet-texture", 800, 999, "Hand resting on soft plush carpet", "Soft plush carpet"),
 ("carpet-samples-selection", 800, 1005, "Carpet samples laid out for choosing", "Choosing your carpet"),
]

def small(name):
    return f"{name}-640.jpg" if name == "grey-carpet-living-room" else f"{name}-480.jpg"

def small_w(name):
    return 640 if name == "grey-carpet-living-room" else 480

# ---------------------------------------------------------------- schema
BUSINESS = {
 "@type": "HomeAndConstructionBusiness",
 "@id": f"{SITE}/#business",
 "name": NAME,
 "slogan": "Tough floors. Built to last.",
 "description": "Carpet supply and installation, carpet repairs and re-stretching, carpet tiles, stairs and commercial carpet across Melbourne, Victoria.",
 "url": f"{SITE}/",
 "telephone": PHONE_TEL,
 "image": f"{SITE}/assets/images/og-image.jpg",
 "logo": f"{SITE}/assets/images/icon-192.png",
 "address": {"@type": "PostalAddress", "streetAddress": STREET, "addressLocality": CITY, "addressRegion": REGION, "addressCountry": "AU"},
 "areaServed": {"@type": "City", "name": "Melbourne"},
 "sameAs": [f"https://www.instagram.com/{SOCIAL}", f"https://www.facebook.com/{SOCIAL}", f"https://x.com/{SOCIAL}"],
}

def ld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False, indent=1) + "</script>"

def faq_schema(faqs):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}

def crumbs_schema(items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(items)]}

# ---------------------------------------------------------------- shared parts
def head(p, title, desc, path, schema_graph, preload=None):
    url = f"{SITE}/{path}"
    pre = f'\n  <link rel="preload" as="image" href="{p}assets/images/{preload}">' if preload else ""
    return f"""<!DOCTYPE html>
<html lang="en-AU">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{url}">
  <meta name="robots" content="index, follow, max-image-preview:large">
  <meta name="theme-color" content="#0d0d0d">
  <meta name="geo.region" content="AU-VIC">
  <meta name="geo.placename" content="Melbourne">

  <meta property="og:type" content="website">
  <meta property="og:locale" content="en_AU">
  <meta property="og:site_name" content="{NAME}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{SITE}/assets/images/og-image.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image" content="{SITE}/assets/images/og-image.jpg">

  <link rel="icon" type="image/png" sizes="32x32" href="{p}assets/images/favicon-32.png">
  <link rel="apple-touch-icon" href="{p}assets/images/apple-touch-icon.png">
  <link rel="manifest" href="{p}site.webmanifest">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow:wght@400;500;600;700&family=Barlow+Condensed:wght@600;700&family=Black+Ops+One&display=swap">
  <link rel="stylesheet" href="{p}assets/css/styles.css">{pre}

  {ld({"@context": "https://schema.org", "@graph": schema_graph})}
</head>
"""

def header(p, home_prefix, current=None):
    """p = path back to site root; home_prefix = how to reach homepage sections."""
    links = [("Our Work", "our-work"), ("Gallery", "gallery"), ("Why Us", "why-us"),
             ("Reviews", "reviews"), ("Areas", "areas"), ("Questions", "questions")]
    sub = "\n".join(
        f'            <li><a href="{p}{s["slug"]}/"{CUR if current == s["slug"] else ""}>{s["nav"]}</a></li>'
        for s in SERVICES)
    nav_links = "\n".join(
        f'        <li><a class="nav-link" href="{p}{h}/"{CUR if current == h else ""}>{t}</a></li>' for t, h in links)
    return f"""<body>
<a class="skip-link" href="#main">Skip to content</a>

<header class="site-header">
  <div class="header-inner">
    <a class="logo" href="{p or './'}" aria-label="{NAME} — home">
      <img src="{p}assets/images/apple-touch-icon.png" alt="" width="52" height="52">
      <span class="logo-text"><span class="logo-aaa">AAA</span><span class="logo-sub">Aussie Carpets</span></span>
    </a>

    <nav class="main-nav" id="main-nav" aria-label="Main">
      <ul class="nav-list">
        <li class="has-dropdown">
          <button class="nav-toggle-sub" type="button" aria-expanded="false" aria-controls="services-menu">Services {I["chev"]}</button>
          <ul class="dropdown" id="services-menu">
{sub}
            <li class="divider" role="presentation"></li>
            <li><a class="all-services" href="{p}services/"{CUR if current == "services" else ""}>All services</a></li>
          </ul>
        </li>
{nav_links}
      </ul>
      <div class="mobile-nav-cta mobile-only">
        <a class="btn btn--gold" href="#quote">Get a free quote</a>
        <a class="btn btn--outline" href="tel:{PHONE_TEL}">{I["phone"]} Call {PHONE}</a>
      </div>
    </nav>

    <div class="header-actions">
      <a class="header-phone" href="tel:{PHONE_TEL}" aria-label="Call {PHONE}">{I["phone"]}<span class="phone-text">{PHONE}</span></a>
      <a class="btn btn--gold header-cta" href="#quote">Get a free quote</a>
    </div>

    <button class="burger" type="button" aria-expanded="false" aria-controls="main-nav" aria-label="Open menu"><span></span></button>
  </div>
</header>
"""

def quote_section(suburb=""):
    sub_val = f' value="{suburb}"' if suburb else ""
    opts = "\n".join(f'              <option>{s["nav"]}</option>' for s in SERVICES)
    return f"""
<section class="section quote" id="quote" aria-labelledby="quote-title">
  <div class="wrap quote-grid">
    <div>
      <span class="eyebrow">Free, no-obligation quote</span>
      <h2 id="quote-title">Let's get your <span class="gold">floors sorted</span></h2>
      <p>Tell us a little about your job and we'll get back to you with a clear, upfront quote. Prefer to talk? Give us a call — we're happy to help.</p>
      <ul class="contact-list">
        <li><span class="ci">{I["phone"]}</span><div><strong>Call us</strong><a href="tel:{PHONE_TEL}">{PHONE}</a></div></li>
        <li><span class="ci">{I["pin"]}</span><div><strong>Visit us</strong><span>{STREET}, {CITY} {REGION}</span></div></li>
        <li><span class="ci">{I["insta"]}</span><div><strong>Follow us</strong><a href="https://www.instagram.com/{SOCIAL}" rel="noopener" target="_blank">@{SOCIAL}</a></div></li>
      </ul>
    </div>

    <!-- This form is emailed to you by EmailJS. Your keys go at the top of the quote form section in assets/js/main.js -->
    <form class="quote-form" method="POST">
      <div class="form-row">
        <div class="field"><label for="q-name">Name</label><input id="q-name" name="name" autocomplete="name" required></div>
        <div class="field"><label for="q-phone">Phone</label><input id="q-phone" name="phone" type="tel" autocomplete="tel" required></div>
      </div>
      <div class="form-row">
        <div class="field"><label for="q-email">Email</label><input id="q-email" name="email" type="email" autocomplete="email"></div>
        <div class="field"><label for="q-suburb">Suburb</label><input id="q-suburb" name="suburb" autocomplete="address-level2" required{sub_val}></div>
      </div>
      <div class="field">
        <label for="q-service">What do you need?</label>
        <select id="q-service" name="service">
{opts}
              <option>Something else</option>
        </select>
      </div>
      <div class="field"><label for="q-msg">Tell us about the job</label><textarea id="q-msg" name="message" placeholder="Rooms, stairs, rough size, when you'd like it done…"></textarea></div>
      <div class="hp" aria-hidden="true"><label>Leave this empty <input name="website_url" tabindex="-1" autocomplete="off"></label></div>
      <button class="btn btn--gold" type="submit">Request my free quote</button>
      <p class="form-status" role="status" aria-live="polite"></p>
      <p class="form-note">We'll only use your details to reply to your enquiry.</p>
    </form>
  </div>
</section>
"""

def footer(p, home_prefix):
    svc = "\n".join(f'          <li><a href="{p}{s["slug"]}/">{s["nav"]}</a></li>' for s in SERVICES)
    return f"""
<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <a class="logo" href="{p or './'}" aria-label="{NAME} — home">
          <img src="{p}assets/images/apple-touch-icon.png" alt="" width="52" height="52" loading="lazy">
          <span class="logo-text"><span class="logo-aaa">AAA</span><span class="logo-sub">Aussie Carpets</span></span>
        </a>
        <p class="footer-tag">Tough floors. Built to last.</p>
        <p>100% Australian owned carpet supply &amp; installation, servicing all of Melbourne.</p>
        <div class="socials">
          <a href="https://www.instagram.com/{SOCIAL}" aria-label="Instagram" rel="noopener" target="_blank">{I["insta"]}</a>
          <a href="https://www.facebook.com/{SOCIAL}" aria-label="Facebook" rel="noopener" target="_blank">{I["fb"]}</a>
          <a href="https://x.com/{SOCIAL}" aria-label="X (Twitter)" rel="noopener" target="_blank">{I["x"]}</a>
        </div>
      </div>
      <div>
        <h2>Services</h2>
        <ul>
{svc}
          <li><a href="{p}services/">All services</a></li>
        </ul>
      </div>
      <div>
        <h2>Explore</h2>
        <ul>
          <li><a href="{p}our-work/">Our work</a></li>
          <li><a href="{p}gallery/">Gallery</a></li>
          <li><a href="{p}why-us/">Why us</a></li>
          <li><a href="{p}reviews/">Reviews</a></li>
          <li><a href="{p}areas/">Areas we service</a></li>
          <li><a href="{p}questions/">Questions</a></li>
        </ul>
      </div>
      <div>
        <h2>Contact</h2>
        <ul>
          <li><a href="tel:{PHONE_TEL}">{PHONE}</a></li>
          <li>{STREET}<br>{CITY} {REGION}</li>
          <li><a href="#quote">Get a free quote</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; <span data-year>2026</span> {NAME}. All rights reserved.</span>
      <span>Carpet supply &amp; installation in Melbourne, Victoria</span>
    </div>
  </div>
</footer>

<div class="mobile-bar">
  <a class="btn btn--outline" href="tel:{PHONE_TEL}">{I["phone"]} Call</a>
  <a class="btn btn--gold" href="#quote">Free quote</a>
</div>

<script src="{p}assets/js/main.js" defer></script>
</body>
</html>
"""

def faq_html(faqs):
    return "\n".join(
        f'      <details>\n        <summary>{q}</summary>\n        <div class="answer"><p>{a}</p></div>\n      </details>' for q, a in faqs)

def write(rel, html):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", rel)

# ---------------------------------------------------------------- shared page pieces
LIGHTBOX = """
<div class="lightbox" role="dialog" aria-modal="true" aria-label="Photo viewer">
  <button class="lightbox-close" type="button" aria-label="Close">&times;</button>
  <img src="data:image/gif;base64,R0lGODlhAQABAAAAACw=" alt="">
</div>
"""

WORK = [
    ("carpeted-winder-staircase-melbourne", 800, 999, "Carpeted winder staircase with tightly wrapped nosings", "Stairs", "Winder staircase", "Each turning step cut and stretched individually for a tight, crisp finish on every nosing."),
    ("staircase-carpet-installation", 800, 1422, "Staircase carpet being installed with floor protection laid down", "Installation", "Full staircase install", "Floors protected, stairs carpeted from bottom to top and finished cleanly against the balustrade."),
    ("carpeted-stair-landing", 800, 1083, "Light neutral carpet on a stair landing", "Stairs & landing", "Landing & hallway", "Landing and stairs laid in one carpet so the colour and pile run seamlessly through the house."),
]

WHY = [
    ("Done right first time", "Power-stretched, flat carpet with seams you won't notice."),
    ("Quality materials", "Carpet and underlay chosen to suit your rooms and how you use them."),
    ("Upfront pricing", "Free quotes with a clear price before we start — no hidden extras."),
    ("Clean &amp; tidy", "We protect your home, take the old carpet away and clean up after."),
    ("Stair specialists", "Winders, landings, runners and wrapped finishes done with care."),
    ("Homes &amp; businesses", "From a single room to offices, rentals and strata common areas."),
]

STEPS = """    <ol class="steps">
      <li><h3>Get in touch</h3><p>Call us or send a quote request with a few details about your job.</p></li>
      <li><h3>Measure &amp; choose</h3><p>We measure up and help you pick the right carpet and underlay for each room.</p></li>
      <li><h3>Clear, upfront quote</h3><p>You get a clear price with no surprises before any work is booked.</p></li>
      <li><h3>Expert installation</h3><p>We remove the old carpet, install the new and leave everything clean and tidy.</p></li>
    </ol>"""

def work_html(p):
    return "\n".join(f"""      <article class="work-card">
        <img src="{p}assets/images/{n}-480.jpg" srcset="{p}assets/images/{n}-480.jpg 480w, {p}assets/images/{n}.jpg {w}w" sizes="(max-width: 600px) 100vw, (max-width: 900px) 50vw, 33vw" width="{w}" height="{h}" alt="{alt}" loading="lazy" decoding="async">
        <div class="work-body"><span class="tag">{tag}</span><h3>{t}</h3><p>{d}</p></div>
      </article>""" for n, w, h, alt, tag, t, d in WORK)

def gallery_html(p, items):
    return "\n".join(f"""      <figure>
        <button type="button" data-full="{p}assets/images/{n}.jpg" aria-label="View larger: {alt}">
          <img src="{p}assets/images/{small(n)}" srcset="{p}assets/images/{small(n)} {small_w(n)}w, {p}assets/images/{n}.jpg {w}w" sizes="(max-width: 640px) 100vw, 33vw" width="{w}" height="{h}" alt="{alt}" loading="lazy" decoding="async">
        </button>
        <figcaption>{cap}</figcaption>
      </figure>""" for n, w, h, alt, cap in items)

def why_list(items):
    return "\n".join(f'        <li><span class="num">{i+1:02d}</span><div><h3>{t}</h3><p>{d}</p></div></li>' for i, (t, d) in enumerate(items))

def reviews_html():
    card = """      <figure class="review">
        <blockquote><p>[Paste a real customer review here.]</p></blockquote>
        <figcaption><cite>[Customer first name]<span>[Suburb] · [Service]</span></cite></figcaption>
      </figure>"""
    return "\n".join([card] * 3)

def cta_band(h, sub):
    return f"""
<section class="cta-band">
  <div class="wrap">
    <div><h2>{h}</h2><p>{sub}</p></div>
    <div class="actions"><a class="btn btn--dark" href="#quote">Get a free quote</a><a class="btn btn--outline" href="tel:{PHONE_TEL}">Call {PHONE}</a></div>
  </div>
</section>
"""

def page_hero(p, crumb, eyebrow, h1, lead):
    return f"""
<section class="page-hero" aria-labelledby="page-title">
  <div class="wrap page-hero-solo">
    <nav class="breadcrumbs" aria-label="Breadcrumb">
      <ol><li><a href="{p}">Home</a></li><li><span aria-current="page">{crumb}</span></li></ol>
    </nav>
    <span class="eyebrow">{eyebrow}</span>
    <h1 id="page-title">{h1}</h1>
    <p class="lead">{lead}</p>
  </div>
</section>
"""

def simple_page(slug, crumb, title, desc, eyebrow, h1, lead, body, extra_graph=(), lightbox=False):
    p = "../"
    url = f"{SITE}/{slug}/"
    graph = [BUSINESS,
             {"@type": "WebPage", "@id": url, "url": url, "name": title, "description": desc,
              "isPartOf": {"@id": f"{SITE}/#website"}, "about": {"@id": f"{SITE}/#business"}},
             crumbs_schema([("Home", f"{SITE}/"), (crumb, url)])] + list(extra_graph)
    html = head(p, title, desc, f"{slug}/", graph) + header(p, p, current=slug) + f"""
<main id="main">
{page_hero(p, crumb, eyebrow, h1, lead)}
{body}
{quote_section()}
</main>
{LIGHTBOX if lightbox else ""}""" + footer(p, p)
    write(f"{slug}/index.html", html)

# ---------------------------------------------------------------- HOME
def home(rows=()):
    p = ""
    title = "Melbourne Carpet Layers — Supply & Installation | AAA Aussie Carpets"
    desc = "AAA Aussie Carpets supplies and installs quality carpet across Melbourne — homes, stairs, carpet tiles, repairs and commercial. 100% Australian owned. Free quotes: 0415 850 095."
    graph = [BUSINESS,
             {"@type": "WebSite", "@id": f"{SITE}/#website", "url": f"{SITE}/", "name": NAME, "publisher": {"@id": f"{SITE}/#business"}, "inLanguage": "en-AU"}]
    cards = "\n".join(f"""      <a class="service-card" href="{s['slug']}/">
        <span class="service-icon">{I[s['icon']]}</span>
        <h3>{s['nav']}</h3>
        <p>{s['card']}</p>
        <span class="card-link">Learn more {I['arrow']}</span>
      </a>""" for s in SERVICES)
    popular = ["melbourne", "werribee", "point-cook", "frankston", "dandenong", "box-hill", "ringwood", "footscray",
               "craigieburn", "berwick", "cranbourne", "glen-waverley", "st-kilda", "brunswick", "doncaster", "sunbury"]
    by_slug = {r["url_slug"]: r for r in rows}
    region_chips = "\n".join(f'      <li><a href="{x}/">{by_slug[x]["suburb"]}</a></li>' for x in popular if x in by_slug) \
        or "\n".join(f'      <li>{a}</li>' for a, _ in AREAS)

    html = head(p, title, desc, "", graph) + header(p, p) + f"""
<main id="main">

<section class="hero" aria-labelledby="hero-title">
  <div class="hero-bg">
    <img src="assets/images/grey-carpet-living-room.jpg" srcset="assets/images/grey-carpet-living-room-640.jpg 640w, assets/images/grey-carpet-living-room.jpg 1242w" sizes="100vw" width="1242" height="929" alt="" fetchpriority="high">
  </div>
  <div class="hero-content">
    <span class="eyebrow">Melbourne carpet specialists</span>
    <h1 id="hero-title">Carpet supply &amp; installation in <span>Melbourne</span></h1>
    <p class="hero-lead">From one bedroom to the whole house, AAA Aussie Carpets supplies quality carpet and installs it properly — tight stretches, clean seams and a tidy finish every time.</p>
    <div class="hero-actions">
      <a class="btn btn--gold" href="#quote">Get a free quote</a>
      <a class="btn btn--outline" href="tel:{PHONE_TEL}">{I["phone"]} {PHONE}</a>
    </div>
    <ul class="hero-points">
      <li>{I["check"]} 100% Australian owned</li>
      <li>{I["check"]} Free, no-obligation quotes</li>
      <li>{I["check"]} Homes &amp; businesses</li>
    </ul>
  </div>
</section>

<div class="strip"><div class="strip-inner"><span>Tough floors. Built to last.</span><span>Supply &amp; installation</span><span>Servicing all of Melbourne</span></div></div>

<section class="section section--stone" aria-labelledby="services-title">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">What we do</span>
      <h2 id="services-title">Carpet services across Melbourne</h2>
      <p>Supply, installation, repairs and specialist work — one local team that looks after the whole job.</p>
    </div>
    <div class="services-grid">
{cards}
    </div>
    <div class="section-more"><a class="btn btn--dark" href="services/">All services</a></div>
  </div>
</section>

<section class="section section--dark" aria-labelledby="work-title">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">Our work</span>
      <h2 id="work-title">Recent carpet installations</h2>
      <p>Stairs are where workmanship shows. Here's a look at some of the jobs we're proud of.</p>
    </div>
    <div class="work-grid">
{work_html(p)}
    </div>
    <div class="section-more"><a class="btn btn--gold" href="our-work/">See our work</a></div>
  </div>
</section>

<section class="section section--stone" aria-labelledby="process-title">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">How it works</span>
      <h2 id="process-title">New carpet in four simple steps</h2>
    </div>
{STEPS}
  </div>
</section>

<section class="section" aria-labelledby="gallery-title">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">Gallery</span>
      <h2 id="gallery-title">Carpet styles &amp; finishes</h2>
      <p>Wool, nylon, loop pile, plush and more. Tap any photo to see it larger.</p>
    </div>
    <div class="gallery">
{gallery_html(p, GALLERY[:3])}
    </div>
    <div class="section-more"><a class="btn btn--dark" href="gallery/">View the full gallery</a></div>
  </div>
</section>

<section class="section section--dark" aria-labelledby="why-title">
  <div class="wrap why-grid">
    <div class="why-mascot">
      <img src="assets/images/aaa-aussie-carpets-lion.jpg" width="420" height="440" alt="AAA Aussie Carpets lion mascot with arms crossed" loading="lazy" decoding="async">
      <span class="why-badge">100% Australian owned</span>
    </div>
    <div>
      <span class="eyebrow">Why choose us</span>
      <h2 id="why-title">Tough floors. <span class="gold">Built to last.</span></h2>
      <p>We're a local Melbourne carpet business that takes pride in doing the job properly the first time. No shortcuts, no mess, no surprises.</p>
      <ul class="why-list">
{why_list(WHY[:4])}
      </ul>
      <div class="section-more"><a class="btn btn--gold" href="why-us/">Why choose us</a></div>
    </div>
  </div>
</section>

<section class="section section--stone" aria-labelledby="reviews-title">
  <div class="wrap teaser">
    <div>
      <span class="eyebrow">Reviews</span>
      <h2 id="reviews-title">Our customer promise</h2>
      <p>Every job comes with the same promise: carpet laid right, a clean and tidy site, and a clear price upfront.</p>
    </div>
    <a class="btn btn--dark" href="reviews/">See our promise</a>
  </div>
</section>

<section class="section section--dark" aria-labelledby="areas-title">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">Areas we service</span>
      <h2 id="areas-title">Carpet installation across Melbourne</h2>
      <p>We supply and install carpet right across Melbourne and surrounds. Popular areas:</p>
    </div>
    <ul class="chips chips--links">
{region_chips}
    </ul>
    <div class="section-more"><a class="btn btn--gold" href="areas/">See all areas</a></div>
  </div>
</section>

<section class="section" aria-labelledby="faq-title">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">Questions</span>
      <h2 id="faq-title">Frequently asked questions</h2>
    </div>
    <div class="faq">
{faq_html(HOME_FAQS[:3])}
    </div>
    <div class="section-more"><a class="btn btn--dark" href="questions/">All questions</a></div>
  </div>
</section>
{quote_section()}
</main>
{LIGHTBOX}""" + footer(p, p)
    write("index.html", html)

# ---------------------------------------------------------------- SECTION PAGES
def our_work():
    body = f"""
<section class="section section--dark" aria-labelledby="work-title">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">Recent jobs</span>
      <h2 id="work-title">Carpet installations we're proud of</h2>
      <p>Stairs are where a carpet layer's skill really shows. Every tread, riser and winder is measured, cut and stretched individually.</p>
    </div>
    <div class="work-grid">
{work_html("../")}
    </div>
  </div>
</section>

<section class="section section--stone" aria-labelledby="process-title">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">How it works</span>
      <h2 id="process-title">How every job runs</h2>
    </div>
{STEPS}
  </div>
</section>
{cta_band("Want results like these?", "Tough floors. Built to last. Get your free quote today.")}"""
    simple_page("our-work", "Our work", f"Our Work — Carpet Installations in Melbourne | {NAME}",
                "See recent carpet installations by AAA Aussie Carpets in Melbourne — winder staircases, landings and full home carpet. Free quotes on 0415 850 095.",
                "Our work", "Our carpet work in Melbourne",
                "A look at recent stair and carpet installations by our team — tight, crisp and built to last.", body)

def gallery():
    body = f"""
<section class="section" aria-labelledby="gallery-title">
  <div class="wrap">
    <div class="gallery">
{gallery_html("../", GALLERY)}
    </div>
  </div>
</section>
{cta_band("Found a style you like?", "We'll bring samples to you and give you a free quote.")}"""
    simple_page("gallery", "Gallery", f"Carpet Gallery — Styles & Finishes | {NAME}",
                "Browse photos of carpet styles and finishes from AAA Aussie Carpets — staircases, landings, wool and nylon, loop pile and plush carpet in Melbourne homes.",
                "Gallery", "Carpet gallery",
                "Staircases, landings, loop pile, plush and more. Tap any photo to see it larger.", body, lightbox=True)

def why_us():
    body = f"""
<section class="section section--dark" aria-labelledby="why-title">
  <div class="wrap why-grid">
    <div class="why-mascot">
      <img src="../assets/images/aaa-aussie-carpets-lion.jpg" width="420" height="440" alt="AAA Aussie Carpets lion mascot with arms crossed" loading="lazy" decoding="async">
      <span class="why-badge">100% Australian owned</span>
    </div>
    <div>
      <h2 id="why-title">Tough floors. <span class="gold">Built to last.</span></h2>
      <p>We're a local Melbourne carpet business that takes pride in doing the job properly the first time. No shortcuts, no mess, no surprises.</p>
      <ul class="why-list">
{why_list(WHY)}
      </ul>
    </div>
  </div>
</section>

<section class="section section--stone" aria-labelledby="process-title">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">How it works</span>
      <h2 id="process-title">New carpet in four simple steps</h2>
    </div>
{STEPS}
  </div>
</section>
{cta_band("Ready for new floors?", "Talk to a local, Australian-owned team today.")}"""
    simple_page("why-us", "Why us", f"Why Choose Us — Melbourne Carpet Layers | {NAME}",
                "Why Melbourne homes and businesses choose AAA Aussie Carpets: 100% Australian owned, quality materials, upfront pricing and carpet laid right the first time.",
                "Why choose us", "Why choose AAA Aussie Carpets",
                "100% Australian owned and proud of our workmanship. Here's what you can expect when you work with us.", body)

def reviews():
    promise = [
        ("Carpet laid right", "Power-stretched, flat and finished cleanly at every doorway and seam."),
        ("A clean, tidy job", "We protect your home while we work, take the old carpet away and leave the place clean."),
        ("A clear price upfront", "Free, no-obligation quotes with the full price before we start. No surprise extras."),
    ]
    cards = "\n".join(f"""      <div class="review">
        <span class="num-badge">{i+1:02d}</span>
        <h3>{t}</h3>
        <p>{d}</p>
      </div>""" for i, (t, d) in enumerate(promise))
    body = f"""
<!-- =====================================================================
     ADDING REAL REVIEWS: when customers give you reviews (e.g. on Google),
     add a section like this above "Our promise", one <figure> per review,
     copied word-for-word with the customer's permission:

<section class="section">
  <div class="wrap">
    <div class="reviews-grid">
      <figure class="review">
        <div class="stars" aria-label="5 out of 5 stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
        <blockquote><p>Review text here.</p></blockquote>
        <figcaption><cite>First name<span>Suburb · Service</span></cite></figcaption>
      </figure>
    </div>
  </div>
</section>
     ===================================================================== -->
<section class="section section--stone" aria-labelledby="promise-title">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">Our promise</span>
      <h2 id="promise-title">What every customer can expect</h2>
      <p>Whether it's one bedroom or a whole office, every job gets the same standard of work.</p>
    </div>
    <div class="reviews-grid">
{cards}
    </div>
  </div>
</section>

<section class="section" aria-labelledby="feedback-title">
  <div class="wrap teaser">
    <div>
      <span class="eyebrow">Had us in?</span>
      <h2 id="feedback-title">Tell us how we did</h2>
      <p>Your feedback helps other Melbourne families and businesses choose with confidence. Send us a message on Instagram or give us a call.</p>
    </div>
    <div class="section-more" style="margin-top:0">
      <a class="btn btn--dark" href="https://www.instagram.com/{SOCIAL}" rel="noopener" target="_blank">Message us on Instagram</a>
    </div>
  </div>
</section>
{cta_band("Ready for new floors?", "Get your free, no-obligation quote today.")}"""
    simple_page("reviews", "Reviews", f"Customer Reviews & Our Promise | {NAME} Melbourne",
                "Customer reviews and the workmanship promise behind every AAA Aussie Carpets job — carpet laid right, a tidy site and a clear price upfront.",
                "Reviews", "Customer reviews",
                "We're proud of our work. Here's the promise behind every job — and where to share your own experience.", body)

def questions():
    groups = "\n".join(f"""    <h2 style="margin-top:56px">{s['nav']}</h2>
    <div class="faq">
{faq_html(s['faqs'])}
    </div>""" for s in SERVICES)
    body = f"""
<section class="section">
  <div class="wrap" style="max-width:920px">
    <h2>General questions</h2>
    <div class="faq">
{faq_html(HOME_FAQS)}
    </div>
{groups}
  </div>
</section>
{cta_band("Still have a question?", "Call us — we're happy to help.")}"""
    simple_page("questions", "Questions", f"Carpet FAQs — Questions & Answers | {NAME}",
                "Answers to common carpet questions — installation costs, timing, underlay, stairs, repairs and carpet tiles — from AAA Aussie Carpets in Melbourne.",
                "Questions", "Frequently asked questions",
                "Everything you might want to know about new carpet, stairs, repairs and carpet tiles.", body,
                extra_graph=[faq_schema(HOME_FAQS)])

# ---------------------------------------------------------------- SERVICE PAGES
def service_page(s):
    p = "../"
    path = f"{s['slug']}/"
    url = f"{SITE}/{path}"
    title = f"{s['title']} | {NAME}"
    crumbs = [("Home", f"{SITE}/"), ("Services", f"{SITE}/services/"), (s["nav"], url)]
    graph = [BUSINESS,
             {"@type": "Service", "@id": f"{url}#service", "name": s["h1"].replace("&amp;", "&"), "serviceType": s["nav"],
              "description": s["desc"], "provider": {"@id": f"{SITE}/#business"},
              "areaServed": {"@type": "City", "name": "Melbourne"}, "url": url},
             crumbs_schema(crumbs),
             faq_schema(s["faqs"])]
    others = "\n".join(
        f'          <li><a href="../{o["slug"]}/"{CUR if o is s else ""}>{o["nav"]}</a></li>' for o in SERVICES)
    img = s["img"]
    html = head(p, title, s["desc"], path, graph) + header(p, p, current=s["slug"]) + f"""
<main id="main">
<section class="page-hero" aria-labelledby="page-title">
  <div class="wrap page-hero-inner">
    <div>
      <nav class="breadcrumbs" aria-label="Breadcrumb">
        <ol><li><a href="{p}">Home</a></li><li><a href="{p}services/">Services</a></li><li><span aria-current="page">{s["nav"]}</span></li></ol>
      </nav>
      <span class="eyebrow">AAA Aussie Carpets</span>
      <h1 id="page-title">{s["h1"]}</h1>
      <p class="lead">{s["lead"]}</p>
      <div class="hero-actions">
        <a class="btn btn--gold" href="#quote">Get a free quote</a>
        <a class="btn btn--outline" href="tel:{PHONE_TEL}">{I["phone"]} {PHONE}</a>
      </div>
    </div>
    <div class="page-hero-img">
      <img src="{p}assets/images/{img}.jpg" srcset="{p}assets/images/{small(img)} {small_w(img)}w, {p}assets/images/{img}.jpg {s['img_w']}w" sizes="(max-width: 860px) 100vw, 45vw" width="{s['img_w']}" height="{s['img_h']}" alt="{s['img_alt']}" fetchpriority="high">
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap content-grid">
    <article class="prose">
{s["body"]}
      <h2>Common questions</h2>
      <div class="faq">
{faq_html(s["faqs"])}
      </div>
    </article>
    <aside class="sidebar">
      <div class="side-card">
        <h3>Free quote</h3>
        <p>Clear, upfront pricing for {s["nav"].lower()} anywhere in Melbourne.</p>
        <a class="btn btn--gold" href="#quote">Request a quote</a>
        <a class="btn btn--outline" href="tel:{PHONE_TEL}">{I["phone"]} {PHONE}</a>
      </div>
      <nav class="side-links" aria-label="Our services">
        <h3>Our services</h3>
        <ul>
{others}
          <li><a href="{p}services/">All services</a></li>
        </ul>
      </nav>
    </aside>
  </div>
</section>
{cta_band("Ready for new floors?", "Tough floors. Built to last. Get your free quote today.")}
{quote_section()}
</main>
""" + footer(p, p)
    write(f"{path}index.html", html)

def services_index():
    p = "../"
    path = "services/"
    url = f"{SITE}/{path}"
    title = f"Carpet Services Melbourne | {NAME}"
    desc = "All carpet services from AAA Aussie Carpets: supply & installation, repairs & re-stretching, carpet tiles, stairs and commercial carpet across Melbourne. Free quotes."
    graph = [BUSINESS,
             crumbs_schema([("Home", f"{SITE}/"), ("Services", url)]),
             {"@type": "ItemList", "name": "Carpet services", "itemListElement": [
                 {"@type": "ListItem", "position": i + 1, "url": f"{SITE}/{s['slug']}/", "name": s["nav"]} for i, s in enumerate(SERVICES)]}]
    cards = "\n".join(f"""      <a class="service-card" href="{p}{s['slug']}/">
        <span class="service-icon">{I[s['icon']]}</span>
        <h2 class="card-title">{s['nav']}</h2>
        <p>{s['card']}</p>
        <span class="card-link">Learn more {I['arrow']}</span>
      </a>""" for s in SERVICES)
    html = head(p, title, desc, path, graph) + header(p, p, current="services") + f"""
<main id="main">
{page_hero(p, "Services", "What we do", "Carpet services in Melbourne", "Everything from brand-new carpet throughout your home to fixing a single ripple. Supplied, installed and repaired by one local, Australian-owned team.")}
<section class="section section--stone">
  <div class="wrap">
    <div class="services-grid">
{cards}
    </div>
  </div>
</section>
{cta_band("Not sure what you need?", "Give us a call and we'll point you in the right direction.")}
{quote_section()}
</main>
""" + footer(p, p)
    write("services/index.html", html)

def not_found():
    p = "/"
    html = head(p, f"Page not found | {NAME}", "Sorry, that page could not be found.", "404.html", [BUSINESS]).replace(
        '<meta name="robots" content="index, follow, max-image-preview:large">', '<meta name="robots" content="noindex">') + header(p, p) + f"""
<main id="main">
<section class="page-hero">
  <div class="wrap" style="padding:100px 20px;text-align:center">
    <span class="eyebrow">Error 404</span>
    <h1>Page not found</h1>
    <p class="lead">Sorry, we couldn't find that page. It may have moved.</p>
    <div class="hero-actions" style="justify-content:center">
      <a class="btn btn--gold" href="/">Back to home</a>
      <a class="btn btn--outline" href="/services/">Our services</a>
    </div>
  </div>
</section>
{quote_section()}
</main>
""" + footer(p, p)
    write("404.html", html)

PAGES = ["our-work", "gallery", "why-us", "reviews", "areas", "questions"]

# ---------------------------------------------------------------- SUBURB DATA
import csv, math, html as _html

CSV_PATH = os.path.join(ROOT, "data", "suburbs.csv")
KEEP_COLS = ["url_slug", "suburb", "postcode", "council", "region", "latitude", "longitude", "unique_intro"]
CBD = (-37.8136, 144.9631)

def import_csv(src):
    """Copy a CSV downloaded from Google Sheets into data/suburbs.csv, keeping only the columns the site uses."""
    with open(src, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    missing = [c for c in KEEP_COLS if c not in rows[0]]
    if missing:
        sys.exit(f"CSV is missing columns: {', '.join(missing)}")
    os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)
    with open(CSV_PATH, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=KEEP_COLS)
        w.writeheader()
        for r in rows:
            w.writerow({c: r[c].strip() for c in KEEP_COLS})
    print(f"imported {len(rows)} suburbs into data/suburbs.csv")

def load_suburbs():
    if not os.path.exists(CSV_PATH):
        return []
    with open(CSV_PATH, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        r["lat"], r["lng"] = float(r["latitude"]), float(r["longitude"])
    return rows

def km(a_lat, a_lng, b_lat, b_lng):
    r = 6371
    p1, p2 = math.radians(a_lat), math.radians(b_lat)
    dp, dl = p2 - p1, math.radians(b_lng - a_lng)
    h = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(h))

def compass(a_lat, a_lng, b_lat, b_lng):
    """Direction of b as seen from a."""
    y = math.sin(math.radians(b_lng - a_lng)) * math.cos(math.radians(b_lat))
    x = math.cos(math.radians(a_lat)) * math.sin(math.radians(b_lat)) - math.sin(math.radians(a_lat)) * math.cos(math.radians(b_lat)) * math.cos(math.radians(b_lng - a_lng))
    deg = (math.degrees(math.atan2(y, x)) + 360) % 360
    return ["north", "north-east", "east", "south-east", "south", "south-west", "west", "north-west"][int((deg + 22.5) // 45) % 8]

def e(s):
    return _html.escape(s, quote=True)

def nice_list(names):
    names = list(names)
    return names[0] if len(names) == 1 else ", ".join(names[:-1]) + " and " + names[-1]

SUBURB_IMAGES = [
    ("grey-carpet-living-room", 1242, 929, "Grey carpet installed in a bright living room"),
    ("carpeted-winder-staircase-melbourne", 800, 999, "Carpeted winder staircase with neat wrapped nosings"),
    ("carpeted-stair-landing", 800, 1083, "Neutral carpet on a stair landing"),
    ("woven-loop-carpet-closeup", 800, 993, "Close-up of woven loop pile carpet"),
    ("soft-plush-carpet-texture", 800, 999, "Soft plush carpet texture"),
]

def suburb_page(r, all_rows):
    p = "../"
    slug, name, pc = r["url_slug"], r["suburb"], r["postcode"]
    council, region = r["council"], r["region"]
    path = f"{slug}/"
    url = f"{SITE}/{path}"

    others = [o for o in all_rows if o is not r]
    nearest = sorted(others, key=lambda o: km(r["lat"], r["lng"], o["lat"], o["lng"]))[:8]
    same_council = sorted([o for o in others if o["council"] == council and o not in nearest], key=lambda o: o["suburb"])[:12]
    d_cbd = km(CBD[0], CBD[1], r["lat"], r["lng"])
    if d_cbd < 2:
        where = f"{e(name)} is right in the heart of Melbourne, in the {e(council)}"
    else:
        where = f"{e(name)} is about {round(d_cbd)} km {compass(CBD[0], CBD[1], r['lat'], r['lng'])} of the Melbourne CBD, in the {e(council)}"
    near3 = nice_list(e(o["suburb"]) for o in nearest[:3])

    title = f"Carpet Installation {name} {pc} | {NAME}"
    desc = f"Carpet supply & installation in {name} {pc}. Repairs, re-stretching, stairs & carpet tiles from a local, 100% Australian owned team. Free quotes: {PHONE}."
    img = SUBURB_IMAGES[sum(map(ord, slug)) % len(SUBURB_IMAGES)]

    place = {"@type": "Place", "name": f"{name} VIC {pc}",
             "address": {"@type": "PostalAddress", "addressLocality": name, "postalCode": pc, "addressRegion": "VIC", "addressCountry": "AU"},
             "geo": {"@type": "GeoCoordinates", "latitude": r["lat"], "longitude": r["lng"]}}
    graph = [BUSINESS,
             {"@type": "WebPage", "@id": url, "url": url, "name": title, "description": desc,
              "isPartOf": {"@id": f"{SITE}/#website"}, "about": {"@id": f"{SITE}/#business"}},
             {"@type": "Service", "@id": f"{url}#service", "name": f"Carpet supply & installation in {name}",
              "serviceType": "Carpet installation", "provider": {"@id": f"{SITE}/#business"},
              "areaServed": place, "url": url},
             crumbs_schema([("Home", f"{SITE}/"), ("Areas", f"{SITE}/areas/"), (name, url)])]

    svc_cards = "\n".join(f"""      <a class="service-card" href="{p}{s['slug']}/">
        <span class="service-icon">{I[s['icon']]}</span>
        <h3>{s['nav']}</h3>
        <p>{s['card']}</p>
        <span class="card-link">{s['nav']} in {e(name)} {I['arrow']}</span>
      </a>""" for s in SERVICES)
    near_links = "\n".join(
        f'      <li><a href="../{o["url_slug"]}/">{e(o["suburb"])} <span>{km(r["lat"], r["lng"], o["lat"], o["lng"]):.0f} km</span></a></li>' for o in nearest)
    council_links = "\n".join(f'      <li><a href="../{o["url_slug"]}/">{e(o["suburb"])}</a></li>' for o in same_council)
    council_block = f"""
    <h3 class="links-title">More suburbs in the {e(council)}</h3>
    <ul class="link-cols">
{council_links}
    </ul>""" if same_council else ""

    faqs = [
        (f"Do you install carpet in {name}?",
         f"Yes. We supply and install carpet throughout {name} {pc} and the surrounding {region} area, including {nice_list(o['suburb'] for o in nearest[:3])}."),
        (f"How much does carpet installation cost in {name}?",
         f"It depends on the carpet and underlay you choose, the size of the rooms and whether there are stairs. We give free, no-obligation quotes in {name} with a clear price before any work starts."),
        (f"Can you repair or re-stretch carpet in {name}?",
         f"Yes. We re-stretch rippled carpet and repair burns, pet damage and split seams in {name} homes and businesses — often for far less than replacing the carpet."),
        (f"Do you do commercial carpet in {name}?",
         f"Yes. We install carpet tiles and broadloom for offices, shops, rentals and strata properties in {name} and across the {council}."),
    ]
    bbox = f"{r['lng'] - 0.03:.4f}%2C{r['lat'] - 0.02:.4f}%2C{r['lng'] + 0.03:.4f}%2C{r['lat'] + 0.02:.4f}"
    map_src = f"https://www.openstreetmap.org/export/embed.html?bbox={bbox}&amp;layer=mapnik&amp;marker={r['lat']:.4f}%2C{r['lng']:.4f}"

    html = head(p, e(title), e(desc), path, graph) + header(p, p, current="areas") + f"""
<main id="main">
<section class="page-hero" aria-labelledby="page-title">
  <div class="wrap page-hero-inner">
    <div>
      <nav class="breadcrumbs" aria-label="Breadcrumb">
        <ol><li><a href="{p}">Home</a></li><li><a href="../areas/">Areas</a></li><li><span aria-current="page">{e(name)}</span></li></ol>
      </nav>
      <span class="eyebrow">{e(region)} · {pc}</span>
      <h1 id="page-title">Carpet installation in <span class="gold">{e(name)}</span></h1>
      <p class="lead">{e(r["unique_intro"])}</p>
      <div class="hero-actions">
        <a class="btn btn--gold" href="#quote">Get a free quote</a>
        <a class="btn btn--outline" href="tel:{PHONE_TEL}">{I["phone"]} {PHONE}</a>
      </div>
      <ul class="hero-points">
        <li>{I["check"]} Free measure &amp; quote in {e(name)}</li>
        <li>{I["check"]} 100% Australian owned</li>
      </ul>
    </div>
    <div class="page-hero-img">
      <img src="{p}assets/images/{img[0]}.jpg" srcset="{p}assets/images/{small(img[0])} {small_w(img[0])}w, {p}assets/images/{img[0]}.jpg {img[1]}w" sizes="(max-width: 860px) 100vw, 45vw" width="{img[1]}" height="{img[2]}" alt="{img[3]} — carpet installation in {e(name)}" fetchpriority="high">
    </div>
  </div>
</section>

<section class="section section--stone" aria-labelledby="svc-title">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">Our services</span>
      <h2 id="svc-title">Carpet services in {e(name)}</h2>
      <p>Everything from new carpet throughout your home to fixing a single ripple — supplied, installed and repaired by one local team.</p>
    </div>
    <div class="services-grid">
{svc_cards}
    </div>
  </div>
</section>

<section class="section section--dark" aria-labelledby="local-title">
  <div class="wrap suburb-local">
    <div>
      <span class="eyebrow">Local carpet layers</span>
      <h2 id="local-title">Your {e(name)} carpet specialists</h2>
      <p>{where}. We install carpet right across {e(region)}, including {near3}, so organising a measure and quote in {e(name)} is easy.</p>
      <ul class="facts">
        <li><strong>Suburb</strong><span>{e(name)} VIC {pc}</span></li>
        <li><strong>Council</strong><span>{e(council)}</span></li>
        <li><strong>Region</strong><span>{e(region)}</span></li>
        <li><strong>Call</strong><span><a href="tel:{PHONE_TEL}">{PHONE}</a></span></li>
      </ul>
    </div>
    <div class="map-embed">
      <iframe title="Map of {e(name)}, Victoria" src="{map_src}" loading="lazy" referrerpolicy="no-referrer"></iframe>
      <a href="https://www.openstreetmap.org/?mlat={r['lat']:.4f}&amp;mlon={r['lng']:.4f}#map=14/{r['lat']:.4f}/{r['lng']:.4f}" rel="noopener" target="_blank">View larger map</a>
    </div>
  </div>
</section>

<section class="section section--stone" aria-labelledby="process-title">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">How it works</span>
      <h2 id="process-title">New carpet in {e(name)} in four simple steps</h2>
    </div>
{STEPS}
  </div>
</section>

<section class="section" aria-labelledby="near-title">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">Nearby areas</span>
      <h2 id="near-title">We also lay carpet near {e(name)}</h2>
    </div>
    <ul class="link-cols link-cols--near">
{near_links}
    </ul>
{council_block}
    <div class="section-more"><a class="btn btn--dark" href="../areas/">All areas we service</a></div>
  </div>
</section>

<section class="section section--stone" aria-labelledby="faq-title">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">Questions</span>
      <h2 id="faq-title">Carpet questions from {e(name)} customers</h2>
    </div>
    <div class="faq">
{faq_html([(e(q), e(a)) for q, a in faqs])}
    </div>
  </div>
</section>
{cta_band(f"New carpet for your {e(name)} home?", "Tough floors. Built to last. Get your free quote today.")}
{quote_section(name)}
</main>
""" + footer(p, p)
    write(f"{path}index.html", html)

def areas(rows):
    by_region = {}
    for r in rows:
        by_region.setdefault(r["region"], []).append(r)
    order = sorted(by_region, key=lambda k: (-len(by_region[k]), k))
    def rid(k):
        return "region-" + "".join(c if c.isalnum() else "-" for c in k.lower()).strip("-")
    jump = "\n".join(f'      <li><a href="#{rid(k)}">{e(k)} <span>{len(by_region[k])}</span></a></li>' for k in order)
    blocks = "\n".join(f"""    <div class="region-block" id="{rid(k)}">
      <h2>{e(k)}</h2>
      <ul class="link-cols">
{chr(10).join(f'        <li data-name="{e(x["suburb"].lower())} {x["postcode"]}"><a href="../{x["url_slug"]}/">{e(x["suburb"])} <span>{x["postcode"]}</span></a></li>' for x in sorted(by_region[k], key=lambda x: x["suburb"]))}
      </ul>
    </div>""" for k in order)
    body = f"""
<section class="section section--dark" aria-labelledby="regions-title">
  <div class="wrap">
    <h2 id="regions-title" class="sr-only">Regions</h2>
    <ul class="chips chips--links">
{jump}
    </ul>
  </div>
</section>

<section class="section" aria-labelledby="all-title">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">{len(rows)} suburbs</span>
      <h2 id="all-title">Find your suburb</h2>
      <p>Choose your suburb to see our local carpet services. Can't see it? Call us on <a href="tel:{PHONE_TEL}">{PHONE}</a> — if you're in or around Melbourne, chances are we cover it.</p>
    </div>
    <div class="area-search">
      <label for="suburb-search" class="sr-only">Search suburbs</label>
      <input id="suburb-search" type="search" placeholder="Search your suburb or postcode…" autocomplete="off">
      <p class="area-search-empty" hidden>No suburbs match — give us a call, we probably still cover you.</p>
    </div>
{blocks}
  </div>
</section>
{cta_band("Is your suburb on the list?", "Call us or request a free quote — we'll come to you.")}"""
    simple_page("areas", "Areas", f"Areas We Service in Melbourne | {NAME}",
                f"AAA Aussie Carpets installs carpet in {len(rows)} suburbs across Melbourne — find your suburb for local carpet supply, installation, repairs and stairs. Free quotes: {PHONE}.",
                "Areas we service", "Carpet installation across Melbourne",
                "We supply and install carpet right across Melbourne and surrounds. Find your suburb below.", body)

def sitemap(rows):
    urls = [("", "1.0"), ("services/", "0.9")] + [(f"{s['slug']}/", "0.9") for s in SERVICES] + [(f"{x}/", "0.7") for x in PAGES] \
        + [(f"{r['url_slug']}/", "0.6") for r in rows]
    body = "\n".join(f"  <url>\n    <loc>{SITE}/{u}</loc>\n    <lastmod>{TODAY}</lastmod>\n    <priority>{pr}</priority>\n  </url>" for u, pr in urls)
    write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{body}\n</urlset>\n')

# ---------------------------------------------------------------- RUN
if len(sys.argv) > 1:
    import_csv(sys.argv[1])
SUBURBS = load_suburbs()
QUIET = True
home(SUBURBS)
services_index()
for s in SERVICES:
    service_page(s)
our_work(); gallery(); why_us(); reviews(); areas(SUBURBS); questions()
for r in SUBURBS:
    suburb_page(r, SUBURBS)
not_found()
sitemap(SUBURBS)
print(f"done: {len(SUBURBS)} suburb pages + main pages")
