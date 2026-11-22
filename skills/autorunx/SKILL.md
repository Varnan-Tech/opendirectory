---
name: autorunx
description: Use when the user wants to make a film, video clip, picture, song or storyboard on AutorunX, or work on an AutorunX Studio Mix project (plan, script, storyboard, timeline) through the AutorunX MCP tools.
author: bluehans-agency
version: 1.0.0
---

## Setup (once)

This skill drives the AutorunX MCP server. If the AutorunX tools (`list_models`,
`submit_plan`, …) are not available, help the user connect it:

1. Sign in at https://autorunx.com and make an API key (profile picture → API keys). It starts
   with `axk_`.
2. Add the server. Claude Code:
   `claude mcp add --transport http autorunx https://autorunx.com/api/mcp --header "Authorization: Bearer axk_..."`
   Other agents: a streamable-HTTP MCP server at `https://autorunx.com/api/mcp` with the header
   `Authorization: Bearer axk_...`.
3. Restart the agent and call `list_models` to check it works.

Never print or store the user's key anywhere except the agent's MCP config.


# Making films with AutorunX

AutorunX makes the media; you plan it. Everything you make lands in a **Studio Mix project** on
autorunx.com (tagged "API"), where the user can open and edit it.

## Before you start

1. Call `list_models`. It shows the user's running GPUs (`AXG-…`), the video models on each,
   the cloud picture and music models, and the credit balance.
   - **Video runs only on the user's rented GPU.** No ready GPU means no video: tell the user to
     rent one on autorunx.com (Rent GPU) and stop there. Never retry in a loop.
   - Pictures and music use cloud models and are paid from credits.
2. Pick the project: `list_projects` to continue one, or `create_project` for a new one.

## Two ways to work

**Whole plan (best for a film).** Write the story, then send it in one `submit_plan` call:
items with prompts, frame pictures and scripts. With `start: true` AutorunX checks every item
first (GPU ready, credits, no voice) and starts nothing if one fails, so fix what it names and
send again. Pictures and music start at once; each video waits for its frame pictures. Use
`start_item` to start a video item yourself once its frames are done.

**Piece by piece.** `generate_image`, `generate_music` and `generate_video` each return a
`job_id`. Pass `item_id` to `get_job` when the job belongs to a plan item, so the item is ticked.

## Waiting for jobs

Poll `get_job` every 15–30 seconds; a video can take several minutes. A finished job gives
`url` (use it as a timeline `sourceUrl`) and `downloadUrl` (a direct file link, no login).

## Editing

- `get_storyboard` / `set_storyboard`, `get_script` / `set_script`: change only the items you
  name. `set_prompt` sets the project's prompt box.
- `get_timeline` / `edit_timeline`: ops `add`, `move`, `trim`, `remove` on lanes
  `video`, `audio`, `image`, `text`.
- `post_to_thread`: leave a script, story, shot or note card in the project's chat.
- Read before you write, and pass the read's `updatedAt` as `expected_updated_at`. If the user
  changed the project on the website meanwhile, the write is refused: read again and redo it.
- AutorunX saves a checkpoint before every change, so the user can undo it on the website.

## Pictures you already have

`upload_reference` takes a base64 PNG, JPEG or WebP (up to 20 MB) and returns an `asset_id`
you can use as a frame. AutorunX never downloads a URL for you.

## Good habits

- Tell the user what each step will cost before starting many jobs (`list_models` shows the
  balance).
- A loop clip: pass the start picture as `end_asset_id` to `generate_video` (LTX models).
- When something is refused, show the user the message as it is; it says what to do.

## Expert know-how (skills)

AutorunX carries expert notes you can open: `list_skills` shows them, `get_skill` returns one.
Open the matching one before the work: `tool-playbook` (which tools for which job) when you are
new here, `content-strategy` or `ad-strategy` before planning, `reel-hooks` and
`storytelling-script` before writing (score hooks with `score_hooks`),
`directing-cinematography` and `image-direction` before shot and picture prompts,
`video-editing` before cutting, `static-ads`, `brand-identity`, `thumbnail-design` and
`animated-design` before designing, `platform-specs` for sizes, and `creative-review` before
you hand work to the user.

Designs are drawn, not generated: `save_design` takes your SVG, and `motion.effects` names the
editor's ready-made animation styles (`list_design_effects`). `ask_expert` hands one change to
an AutorunX expert (video, image, 3d, design, voice).
