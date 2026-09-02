---
name: writing-for-agents
description: "Writing agent-facing documents — skills, steering, policies, and any doc an agent reaches by a pointer. Use when creating or editing such documents."
metadata:
  domain: ai-framework
  version: "1.0.0"
  source: ai-framework
---

# Writing for Agents

Reference for writing any document an agent consumes: a skill, a steering file, a policy, a doc reached by a pointer. The packaging differs; the writing does not. The same levers make each one predictable — the agent takes the same _process_ every run rather than producing the same output.

When the document is a skill, also read [SKILL-CONVENTIONS.md](../ai-framework-skill/references/SKILL-CONVENTIONS.md) for frontmatter, directory layout, and naming.

---

## Context Pointers

A **context pointer** is a reference in the agent's context that names out-of-context material and encodes the condition for reaching it. A skill's description is one; a steering line naming a doc is the same object. The pointer's _wording_, not its target, decides when the agent reaches the material and how reliably.

A pointer does two jobs: state what the material is, and list the **branches** that should trigger reaching it. Every word of an always-loaded pointer costs on every turn:

- **Front-load the leading word** — the pointer is where it does its triggering work.
- **One trigger per branch.** Synonyms that rename a single branch are duplication — collapse them; keep only genuinely distinct branches.
- **Cut identity the body already carries.**

---

## The Two Loads

Every document and pointer spends one of two budgets:

- **Context load** — the cost of always-loaded material on the agent's window: a description, an always-on steering, anything sitting in context every turn whether or not it fires.
- **Cognitive load** — the cost on the human: which documents exist and when to reach for each. The human is the index. Not a cost to minimise — it is the price of human agency.

Material reached only through a pointer escapes context load at the price of the pointer's own line; material with no pointer at all rides entirely on cognitive load.

---

## Information Hierarchy

A document is built from two content types: **steps** (ordered actions) and **reference** (definitions, rules, facts consulted on demand). The core decision is where each piece sits on the hierarchy, ranked by how immediately the agent needs it:

1. **In-file step** — what the agent does, in order.
2. **In-file reference** — consulted on demand. A flat peer-set (every rule of a review on one rung) is fine, not a smell.
3. **Disclosed reference** — pushed out into a separate file, reached by a context pointer, loaded only when the pointer fires.

Push too little down and the top bloats; push too much and you hide material the agent needs. That tension is the whole decision.

**Progressive disclosure** is the move down the ladder so the top stays legible. Branching is the cleanest disclosure test: inline what every branch needs, push behind a pointer what only some branches reach.

**Co-location** decides what sits beside a piece once placed: keep a concept's definition, rules, and caveats under one heading rather than scattered.

---

## Steps and Completion Criteria

Every step ends on a **completion criterion** — the condition that tells the agent the work is done. Two properties make it a lever:

- **Clarity** — can the agent tell done from not-done? A vague bound invites **premature completion**: ending the step before it is genuinely done. Defence: sharpen the bound first; only if irreducibly fuzzy, hide post-completion steps by splitting.
- **Demand** — how much it requires. "Every modified model accounted for" forces thorough work where "produce a change list" does not. Demand drives **legwork** (the digging the agent does within the work).

The strongest criteria are both checkable and exhaustive.

---

## When to Split

Splitting spends one of the two loads, so split only when the cut earns it:

- **By sequence** — split a run of steps where post-completion steps tempt the agent to rush the current one. Keeping them out of view drives more legwork.
- **By invocation** — split off a model-invoked skill when you have a distinct leading word that should trigger it on its own.

---

## Leading Words

A **leading word** is a compact concept already in the model's pretraining that the agent thinks with while running the document (_lesson_, _fog of war_, _tracer bullets_). It anchors a whole region of behaviour in the fewest tokens, recruiting priors the model already holds.

It serves twice: in the body it anchors _execution_; in a pointer it anchors _invocation_.

Hunt for circumlocutions that collapse into a single token:
- "fast, deterministic, low-overhead" → _tight_
- "a loop you believe in" → _red_

---

## Negation

Steering by prohibition drags the forbidden behaviour into context and makes it _more_ available. "Don't think of an elephant" names the elephant. Prompt the **positive**: state the target behaviour so the banned one is never spoken.

Keep a prohibition only as a hard guardrail you cannot phrase positively, and pair it with what to do instead.

---

## Pruning

- **Single source of truth** — keep each meaning in one authoritative place. Duplication costs maintenance, tokens, and inflates prominence past real rank.
- **Environment as source** — `package.json` scripts, config files, directory layout are sources of truth too. Cache only what the agent cannot find by looking: the unwritten convention, the reason behind a choice.
- **Relevance** — every line must bear on what the document does. Without a pruning discipline the default fate is **sediment**: stale layers that settle because adding feels safe and removing feels risky.
- **No-ops** — an instruction the model already obeys by default pays load to say nothing. Test: does it change behaviour? When a sentence fails, delete the whole sentence. A weak leading word is a no-op; the fix is a stronger word, not a different technique.

---

## Override Strength

When a directive must **replace** a client's default behavior, weak phrasing fails silently. Escalation ladder:

1. **Suggestion** — "prefer X over Y" → agent may ignore
2. **Constraint** — "NEVER do X" → avoids X but doesn't actively do Y
3. **Directive** — "ALWAYS do X when Y" → often complies, sometimes forgets
4. **Override** — "OVERRIDE: replace [default] with [exact structure]" → reliably replaces

Use OVERRIDE when replacing a built-in tool call structure, changing default output format, or substituting a standard workflow. Include the exact payload — never describe it abstractly. Name the behavior being replaced explicitly.
