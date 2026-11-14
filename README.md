# AAA Aussie Carpets — website

A fast, mobile-friendly, SEO-optimised website for AAA Aussie Carpets (Melbourne).
Plain HTML, CSS and JavaScript, so there's nothing to install and no build step.

## Folder layout

```
index.html                      Home page (hero, services, our work, gallery, why us, reviews, areas, FAQ, quote form)
services/index.html             "All services" page
services/<service>/index.html   One page per service (good for Google rankings)
404.html                        "Page not found" page
assets/css/styles.css           All styling (brand colours are at the top in :root)
assets/js/main.js               Menu, Services dropdown, gallery pop-up, quote form
assets/images/                  Web-optimised photos, logo lion and icons
sitemap.xml, robots.txt         Tell Google what to index
images/                         Your original photos (not uploaded to GitHub, see .gitignore)
```

## Preview it on your computer (VS Code)

1. Install the **Live Server** extension in VS Code.
2. Right-click `index.html` and choose **Open with Live Server**.

## Put it online with GitHub Pages

```bash
git init
git add .
git commit -m "First version of the website"
git branch -M main
git remote add origin https://github.com/<your-username>/aaa-aussie-carpets.git
git push -u origin main
```

Then on GitHub: **Settings → Pages → Build and deployment → Deploy from a branch → `main` / root → Save**.

### Use your own domain (www.aaaaussiecarpets.com)

1. In **Settings → Pages → Custom domain**, enter `www.aaaaussiecarpets.com` and tick **Enforce HTTPS**.
2. At your domain registrar, add a `CNAME` record: `www` → `<your-username>.github.io`.
3. The site's SEO tags already point at `https://www.aaaaussiecarpets.com/`. If you use a different domain,
   search-and-replace that address across all files.

## Before you launch — checklist

- [ ] **Quote form**: create a free form at https://formspree.io, copy the form ID, and replace
      `YOUR_FORM_ID` in every HTML file (search the whole project in VS Code: Cmd+Shift+F).
      Until then the form tells people to call.
- [ ] **Reviews**: replace the `[Paste a real customer review here.]` placeholders in `index.html`
      with real reviews from real customers.
- [ ] **Address**: check `114 Dontons Ave, Melbourne VIC` is correct and add your suburb and postcode.
- [ ] **Social links**: check the Instagram, Facebook and X links point to your real pages.
- [ ] **Areas**: edit the suburb lists in the Areas section to the areas you actually cover.
- [ ] **Google**: set up a free **Google Business Profile**, and add the site to **Google Search Console**
      and submit `https://www.aaaaussiecarpets.com/sitemap.xml`.

## Changing things

- **Colours**: edit the variables at the top of `assets/css/styles.css`.
- **Phone number**: search and replace `0415 850 095` and `+61415850095` across the project.
- **Menu**: the header and footer are repeated at the top and bottom of each HTML file, so change
  each one (VS Code's search-and-replace across files makes this quick).
- **Photos**: put new photos in `assets/images/` and keep them under ~300 KB each so the site stays fast.
