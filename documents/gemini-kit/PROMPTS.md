# Gemini prompts for the Chimalaya flyer (Elephant House)

Two prompts, one per side. For each side, start a chat in Gemini (image model
"Nano Banana"), upload **every file in that side's folder, in numbered order**,
then paste the prompt. Gemini sees the images as "image 1, image 2, ..." in the
order you uploaded them, not by file name, so the order matters.

- Front: upload `front/01` … `front/06`, then paste **Prompt 1**.
- Back: upload `back/01` … `back/07`, then paste **Prompt 2**. Doing the back in
  the same chat as the front, after the front came out well, keeps the two
  sides consistent; then also say "same style as the front you just made".

All facts and figures below come from chimalayanepal.org and the programme
register (to 31 August 2026). Do not let Gemini change them.

---

## Prompt 1: front

```
Design the FRONT of a printed A5 flyer, portrait, ratio 1:1.41 (148 × 210 mm). Keep all text and logos at least 8 mm from every edge. Output at the highest resolution you can.

WHO IT IS FOR: Chimalaya Nepal, a charity that improves maternal and child health in Bode, Bhaktapur, near Kathmandu. The flyer sits next to Chimalaya products sold at Elephant House, a shop in Kathmandu, whose sales support the charity.

IMAGES I UPLOADED:
- Image 1: the Chimalaya Nepal logo. Use it exactly as supplied, do not redraw or recolour it.
- Image 2: the Elephant House logo (a black elephant). Use it exactly as supplied; it may be white if placed on a dark background.
- Image 3: a real photo of a mother in Nepal holding her newborn, with the navy Chimalaya "Bag4Life" bag in front of her. This is the main photo.
- Images 4, 5 and 6: STYLE REFERENCES ONLY (UNICEF/WHO campaign material). Copy their look, not their content: do NOT copy their logos, text, people or the organisations' names.

STYLE (from images 4–6): a full-bleed, warm, dignified photo of mother and baby fills most of the page; the side where the text sits is darkened with a soft gradient so white text reads clearly. Big, bold, uppercase, left-aligned sans-serif headline (like Montserrat ExtraBold), with one key phrase highlighted in colour. One large statistic shown in a solid colour box, as in image 5. Calm, hopeful, respectful, never pitiful. Lots of breathing room.

COLOURS: navy #123F6B, crimson #E50046, white. Dark gradient in deep navy #0B2A49.

PHOTO RULES: use image 3 as the real photograph. You may crop it, extend the background at the edges, and darken it for text, but do NOT change, redraw or replace the people, their faces, the baby or the bag. Do not add any other people.

TEXT, exactly as written, nothing else:
1. Headline (white, with the second line in crimson #E50046):
   "A BETTER START IN LIFE"
   "FOR MOTHERS AND NEWBORNS"
2. Short line under it (white, regular weight, smaller):
   "Since 2013, Chimalaya's clinic in Bode, Bhaktapur has cared for mothers and babies in a community of brick and carpet factory workers."
3. Statistic in a crimson box (large number, small caption):
   "1,815" — "newborns visited at home by our nurses since 2017"
4. Bottom strip, white background, across the full width:
   - left: the Chimalaya Nepal logo (image 1)
   - right: the Elephant House elephant (image 2), with next to it:
     "Thank you for shopping at Elephant House." (bold)
     "Sales of these products support Chimalaya's work." (regular)

Spell every word exactly as above. No other text, no hashtags, no website, no QR code on this side.
```

---

## Prompt 2: back

```
Design the BACK of the same printed A5 flyer, portrait, ratio 1:1.41 (148 × 210 mm). Keep all text and logos at least 8 mm from every edge. Output at the highest resolution you can. It must look like a set with the front: same colours, same bold uppercase headline style, same typeface.

IMAGES I UPLOADED:
- Image 1: the Chimalaya Nepal logo. Use it exactly as supplied.
- Image 2: the real Bag4Life bag (navy bag with the Chimalaya star roundel), cut out on a transparent background.
- Image 3: a real photo of a home visit after birth.
- Image 4: a real photo of a mothers' group meeting.
- Image 5: a real photo of an outreach camp at a brick factory.
- Images 6 and 7: STYLE REFERENCES ONLY (WHO/UNICEF). Copy their look, not their content, logos or text.

PHOTO RULES: use images 2–5 as real photographs. Crop them as needed, but do NOT change, redraw or replace any person, face, baby or the bag. Do not add any other people. Do not invent other logos.

COLOURS: navy #123F6B, crimson #E50046, deep navy #0B2A49, white, light grey #F4F7FA.

LAYOUT, top to bottom:
1. Small crimson uppercase label "WHAT WE DO", then the headline in navy, bold uppercase: "CARE THAT REACHES MOTHERS AT HOME".
2. A 2 × 2 grid of four cards, each with its photo on top, a bold navy title and one short sentence:
   - photo image 3 — "HOME VISITS" — "Our nurses visit newborns at home in their first days, and follow them up to six months."
   - photo image 2 (the bag on a light grey background) — "BAG4LIFE" — "Every family gets a bag with a towel, changing mat, reusable nappies, thermometer, and soap and oil made in Nepal."
   - photo image 4 — "MOTHERS' GROUPS" — "Twice a week, mothers meet at the clinic for growth checks and advice on feeding, play and sleep."
   - photo image 5 — "OUTREACH CAMPS" — "We screen for illness and malnutrition at brick and carpet factories."
3. A full-width deep navy band with four big white numbers and small captions:
   "1,815" — "newborns visited at home since 2017"
   "93.5%" — "received a Bag4Life bag"
   "88.6%" — "had all three newborn visits"
   "25,000" — "people in the clinic's area"
4. "HOW YOU CAN HELP" (bold navy), with three short lines:
   "Buy Chimalaya products here at Elephant House"
   "Follow @chimalayacharity on Facebook and Instagram"
   "Learn more or volunteer at chimalayanepal.org"
   To the right of these lines, leave an EMPTY plain white square about 30 × 30 mm with a thin light grey border. Do not draw a QR code or anything inside it.
5. Footer in small grey text, with the Chimalaya Nepal logo (image 1) small on the left:
   "Chimalaya Charity Nepal · Bode, Madhyapur Thimi-8, Bhaktapur, Nepal"
   "+977-01-6631122 · chimalayanepal2014@gmail.com"

Spell every word and number exactly as above. No other text.
```

---

## If something comes out wrong

Reply in the same chat, one fix at a time, for example:

- `Some words are misspelled. Keep the design and photos exactly, and correct the text to match my prompt word for word.`
- `You changed the woman's face. Use image 3 exactly as the original photo, only cropped and darkened.`
- `Remove every logo except the two I supplied.`
- `The square for the QR code must stay empty and white.`

## Before printing

- Proofread every word, number and the phone number against this file.
- The QR code goes into the empty square afterwards (the one on the current
  flyer points to https://chimalayanepal.org).
- Gemini's images are usually around 2,000 px tall. That is enough for a
  shop flyer, but small text can look soft. For sharp print, the design can
  be rebuilt in `chimalaya-flyer-a5.typ` with Gemini's version as the layout.
- The people in the photos should be happy for their pictures to be used on
  material shown in a shop.
