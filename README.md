# AAA Aussie Carpets — website

A fast, mobile-friendly, SEO-optimised website for AAA Aussie Carpets (Melbourne).
Plain HTML, CSS and JavaScript, so there's nothing to install and no build step.

## Folder layout

```
index.html                      Home page (short previews of each section, linking to the full pages)
services/index.html             "All services" page              -> /services/
carpet-supply-installation/     Service page                     -> /carpet-supply-installation/
carpet-repairs-restretching/    Service page                     -> /carpet-repairs-restretching/
carpet-tiles/                   Service page                     -> /carpet-tiles/
stairs-custom-work/             Service page                     -> /stairs-custom-work/
commercial-carpet/              Service page                     -> /commercial-carpet/
our-work/                       Our Work page                    -> /our-work/
gallery/                        Gallery page                     -> /gallery/
why-us/                         Why Us page                      -> /why-us/
reviews/                        Reviews page                     -> /reviews/
areas/                          Areas page                       -> /areas/
questions/                      Questions (FAQ) page             -> /questions/
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

- [ ] **Quote form (EmailJS)**: paste your Public Key, Service ID and Template ID into the
      `EMAILJS` settings near the bottom of `assets/js/main.js`. Until then the form tells people to call.
      See "Quote form emails" below for the template to use.
- [ ] **Reviews**: replace the `[Paste a real customer review here.]` placeholders in `reviews/index.html`
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

## Quote form emails (EmailJS)

The quote form at the bottom of every page is sent to your inbox by EmailJS (free plan: 200 emails/month).

1. **Email Services**: connect your email account (e.g. Gmail) and note the **Service ID**.
2. **Email Templates → Create New Template**, then set:
   - **Subject:** `New quote request from {{name}} ({{suburb}})`
   - **Content:**
     ```
     Name: {{name}}
     Phone: {{phone}}
     Email: {{email}}
     Suburb: {{suburb}}
     Service: {{service}}

     Message:
     {{message}}

     Sent from: {{page}}
     ```
   - **To Email:** your email address
   - **Reply To:** `{{email}}` (so you can just hit Reply to answer the customer)
   - Save, and note the **Template ID**.
3. **Account → General**: copy your **Public Key**.
4. Paste all three into `assets/js/main.js`:
   ```js
   var EMAILJS = {
     publicKey: "your public key",
     serviceId: "your service id",
     templateId: "your template id"
   };
   ```
5. **Account → Security**: add your website address (e.g. `https://www.aaaaussiecarpets.com`) to the
   allowed domains so nobody else can send emails using your keys.

The public key is meant to be visible in website code. Never paste your EmailJS **Private Key** into the site.
