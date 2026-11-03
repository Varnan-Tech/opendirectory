---
name: transcript-quote-sheet
description: Find timestamped passages across indexed YouTube and podcast transcripts with Arcmira and assemble a source-linked quote sheet for an article, interview brief or clip shortlist.
compatibility: [codex]
author: zealous1
version: 1.0.0
---

# Transcript quote sheet

Use the connected Arcmira MCP server to turn a topic into a shortlist of passages the reader can check against the recording. If the connection is missing, give the reader the [MCP setup guide](https://arcmira.com/docs/mcp-server).

1. Read the current search reference with `arcmira_describe`. Search for the user's phrase and one or two ways a speaker might express the idea aloud. Preserve any show, speaker or date constraint. Combine hits from the same moment before choosing clips.
2. Read enough surrounding transcript to recover the complete thought. Keep a speaker's qualification or negation with the claim. Quote the transcript verbatim, and mark a speaker as unidentified when the evidence only names the channel. Use the source link and timestamp returned for the passage.
3. Return one row per distinct moment: quotation, speaker if established, show or channel, timestamped source, and a short reason the passage fits. If the reader asks for five and only three qualify, return three. State the search scope so they can distinguish an empty result from an unsearched archive.

For a clip shortlist, include the end cue only if the returned transcript establishes it. Caption times are review points. Invite the editor to listen at the link before making the cut.
