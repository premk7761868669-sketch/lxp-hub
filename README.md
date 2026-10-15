# LXP Hub — auto-update app system

## Setup (ek baar, free, ~10 min)
1. github.com pe free account banao -> New repository (Private) -> "uploading an existing file" -> is zip ke andar ke SAARE files/folders upload karo.
2. netlify.com -> Add new site -> Import from GitHub -> ye repo chuno -> Deploy. (Settings netlify.toml se apne aap aa jati hain.)
3. Live: `/` = apps ki list, `/lxp-fit/` = app.

## App update karna
GitHub me `apps/lxp-fit/versions/` ke andar naya folder banao (jaise `1.1.0`) -> usme nayi `index.html` upload karo (chaho to `notes.txt` me kya badla likho) -> Commit.
~1 min me Netlify khud latest live kar dega. Users ko hamesha SABSE BADA version number milta hai. Purane folders repo me safe rehte hain (ye tumhari version history hai). Galti ho jaye to Netlify -> Deploys -> purana deploy -> "Publish deploy".

## Naya app add karna
`apps/<naam>/` banao: `app.json`, `icon-192.png`, `icon-512.png`, `versions/1.0.0/index.html`. Hub list me apne aap aa jayega.

## Chrome / phone
User link kholke "Install app" / "Add to Home screen" kare. App har baar khulne par khud latest version le leta hai.

## Play Store (jab $25 ho)
pwabuilder.com me site ka link do -> Android package banao -> Play Console me ek baar upload. Uske baad web update Play Store wale app me bhi apne aap aa jata hai, dobara upload nahi karna. PWABuilder jo `assetlinks.json` de, use `well-known/assetlinks.json` me rakh do.
