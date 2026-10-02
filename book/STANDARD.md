# Smoke on the Mediterranean — spread standard

Read this before you touch a chapter. The prose in `book/chapters/` is the book. Do not replace it with a shorter version.

Signer tags for this lane: `COS`, `PR`, `A`, `GROK`. `CHATGPT` writes `book/ai-isms/` only and does not generate pictures.

## What you are making

One chapter. One spread. Two halves.

Left: the whole chapter, the prose as it stands in `book/chapters/`, set so a person can read it. Place and years under the title.

Right: eight graphic-novel panels, in the order the chapter tells the story. No captions. No speech balloons. No letters painted into the picture. Ink line, ochre and soot, the same family as chapters 1–3.

A person opens the page and sees both at once.

Live examples:

- https://qv4rk.github.io/GrokBotPlayground/chapter-01/
- https://qv4rk.github.io/GrokBotPlayground/chapter-02/
- https://qv4rk.github.io/GrokBotPlayground/chapter-03/

## Where it lands

On `main` of `qv4rk/GrokBotPlayground` only.

```
chapter-NN/
  index.html
  Title_of_Chapter.pptx
  panels/01-....jpg
  ...
  panels/08-....jpg
```

`NN` is `04` through `27`. Match the number in `book/ASSIGNMENTS.md`.

Also commit a note:

`agent-conference/YYYYMMDDTHHMMZ__SIGNER__chapter-NN.md`

Do not edit another agent's note. Answer with a new file.

Do not write into `qv4rk/V`. Do not touch feisttech.com.

## Claim before you draw

1. Read `book/ASSIGNMENTS.md` and the latest `agent-conference/` notes.
2. If your next chapter is already `claimed` by someone else, skip to the next open number in your lane.
3. Push a note with `status: claimed` and the chapter number before you generate pictures.
4. When the page is on `main` and Pages has it, push a second note with `status: done` and the URL.

Two people do not draw the same chapter.

## The page

- Paper `#ede4d4`. Ink `#2a2218`. Rust `#6b3a2a` for the place line.
- Type: Palatino Linotype, then Palatino, then Georgia.
- Header bar: book name, chapter number, a link to the previous chapter, a link to `../book/`, a link to the `.pptx`.
- Left column is the chapter. Do not summarize it. Do not cut it in half. Do not add a moral at the end that the chapter did not already earn.
- Right column is a two-by-four grid of the panels.
- On a narrow screen the pictures go under the prose.

## The PowerPoint

- One slide. 20 inches wide by 14.25 inches tall.
- Same paper, same type, same split: prose left, eight panels right, a hairline between them.
- Author: MJF.
- The file sits next to `index.html` and the page links to it.

## Pictures are not ChatGPT's job

ChatGPT does not generate panels, does not call an image tool, and does not build the `.pptx`. That work burned a full usage window and put no file on `main`.

GROK draws chapters 07, 11, 15, 19, 23, and 27.

ChatGPT may write `book/ai-isms/NN.md` for those numbers only. If a session has already started making images, stop it.

## The pictures

Eight panels. 3:2. Order follows the prose, top-left to bottom-right.

Each panel is a thing a person could have seen: a room, a boat, a desk, a street, a well, a fort. Not a diagram of the thesis.

Hold these:

- No readable modern English in the image. Period paper may carry illegible script.
- No speech balloons, no captions, no watermarks, no panel numbers burned into the art.
- No modern weapons, engines, clothing, or furniture in a scene dated before they existed. A swivel gun is a short barrel on a yoke. It is not a machine gun.
- Faces are specific and dignified. No caricature of Irish, Chinese, Arab, or Jewish people, and none of clergy or officials.
- No gore. A taking, a refusal, a crowd, a closed door — stop there.
- If a panel is wrong, redraw that panel. Do not ship it because the other seven are fine.

## The prose

Use the file in `book/chapters/` for that number. Chapters 1–3 on the site are the spreads already built. Your source text is still the markdown.

Do not:

- Halve the word count to make it "tighter."
- Open on an object and close on the same object as a frame.
- Stack "not this, but that" as the way the paragraph moves.
- Invent a named person, a sum of money, or a quotation the chapter does not already contain.
- Resolve a source the chapter leaves open.
- Lecture the reader in a last line about what the chapter "really means."

`book/AI-PATTERNS-CHECKLIST.md` is the pass for prose you do change. This assignment does not ask you to rewrite the chapter. It asks you to show it.

## Done means

- The URL returns the spread.
- The left side is the chapter.
- The right side is eight panels in story order.
- The `.pptx` downloads from that page.
- Your conference note says `done` and gives the URL.
- `book/ASSIGNMENTS.md` has your chapter marked done in the same commit. Edit only your own rows.


## AI-isms, same push

`book/ai-isms/NN.md`

Quote what you noticed. Name the pattern from `book/AI-GUIDE.md`. Under it, the sentence you would write, or "cut".

You do not edit `book/chapters/` to try the sentence. You do not edit the spread to try the sentence. The chapter stays. The note is the whole deliverable on this point.

If the fragment count makes you hesitate, use the spiral in the guide: one fragment near the center, then the golden ratio outward. Report the hits. Do not thin the page yourself.

## Language, behind you

Hebrew, Arabic, and Chinese start when your spread is on `main`. You do not wait on them, and you do not translate. Their rule is `book/LANGUAGE.md`.
