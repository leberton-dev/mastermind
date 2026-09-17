# Wanted structure

Target layout for the roguelike conversion: three **separate installable
packages** in a `uv` workspace, not just folders in one package. Not built
yet — this is the plan `src/mastermind/` should converge toward as
[[TODO.md]] items land. Naming pass via `lowlevel-namer` (kernel/overlay/shell
scheme, chosen over a genre-jargon and a plain/literal alternative).

Dependency direction is enforced by packaging, not just discipline:
`mastermind-kernel` declares zero internal dependencies, `mastermind-overlay`
depends on `mastermind-kernel`, `mastermind-shell` depends on
`mastermind-overlay` (and transitively `mastermind-kernel`). A package cannot
import from a package it hasn't declared as a dependency — the boundary
can't be broken by accident, unlike a same-package folder convention.

```
mastermind/                        # repo root
  pyproject.toml                   # workspace root: [tool.uv.workspace] members = ["packages/*"]

  packages/
    mastermind-kernel/             # classic mastermind puzzle rules, invariant, zero internal deps
      pyproject.toml               # name = "mastermind-kernel"
      src/mastermind_kernel/
        colors.py                  # peg color enum
        code.py                    # the secret code type
        feedback.py                # black/white peg feedback calculation
      tests/

    mastermind-overlay/            # everything that only exists because of the roguelike layer
      pyproject.toml               # name = "mastermind-overlay", dependencies = ["mastermind-kernel"]
      src/mastermind_overlay/
        pegs/
          peg.py                   # wrapper type: color + optional enhancement
          enhancement/
            enhancement.py         # enhancement concept
            catalog/                # one file per concrete enhancement (exact_bonus.py, sacrifice_hint.py, ...)

        scoring/
          points.py                # Points type + apply_multiplier/compute_points
          events.py                # hook/event bus: on_guess, on_round_end, on_shop_enter, ...

        relics/
          relic.py                  # Relic + RelicSpec + RelicGrade kept together (matches current core/relic.py)
          catalog/                  # one file per concrete relic (11 today, room to grow toward ~150)

        consumables/                # not built yet — Tarot/Spectral/Planet-like one-shot items
          consumable.py
          catalog/

        economy/
          currency.py                # currency type + reward_for calculation
          shop_rules.py              # purchase logic: buy/sell relics, buy fixed upgrades
          vouchers.py                # not built yet — permanent one-time unlocks bought in the shop

        run/
          run_state.py                # RunState: ante counter, advance_ante, max_relics cap
          round_tier.py               # RoundTier enum: STANDARD/HARDENED/FINAL
          boss_mutators/              # not built yet — unique one-off rule per FINAL round
            mutator.py
            catalog/                  # banned_color.py, hidden_feedback.py, ...
          best_ante.py                # not built yet — persistent best-ante/highscore across runs
      tests/

    mastermind-shell/              # runs/renders the game, no game-rule knowledge
      pyproject.toml               # name = "mastermind-shell", dependencies = ["mastermind-overlay"]
      src/mastermind_shell/
        main.py                     # entry point
        engine/                     # backend-agnostic contracts: Screen, Renderer, InputSource, ScreenQueue/Stack, Transition
        screens/                    # concrete screens: menu, gameplay, shop, game_over
        curses_backend/             # curses implementation of the engine/ contracts: renderer, input_source, keymap, palette
        persistence/                 # not built yet — save/load run state to disk
          save.py
      tests/
```

## Why packages, not just folders

A folder boundary (`kernel/` vs `overlay/` vs `shell/` inside one package)
relies on everyone remembering not to cross it. A package boundary is
enforced by the dependency graph itself: `mastermind-kernel`'s
`pyproject.toml` lists no internal dependencies, so nothing inside it can
`import mastermind_overlay` even by accident — the import would just fail.
Each package also gets its own `tests/`, its own version, and could in
principle be published or reused independently of the other two.

## Naming notes

- Scheme: **kernel / overlay / shell** — systems/kernel metaphor, picked over
  a genre-jargon scheme (`rules`/`meta`/`app`) and a plain/literal scheme
  (`puzzle`/`roguelike`/`tui`).
  - `kernel` — nothing depends on anything, everyone depends on it (echoes
    "nothing below this layer").
  - `overlay` — mutates/extends behavior on top of the kernel (echoes
    overlayfs / device-tree-overlay usage, unambiguous in systems contexts).
  - `shell` — hosts and drives the kernel+overlay stack, user-facing.
  - Known risk, flagged and accepted: "kernel"/"shell" carry OS connotations
    (privilege separation, process boundaries) the code doesn't actually
    have — a contributor unfamiliar with the metaphor could over-read it.
  - Rejected plain-scheme option `mastermind-tui` for the shell package on
    purpose: it would become a lie if a non-curses (GUI/web) backend is ever
    added; `shell` doesn't carry that trap.
- `relic.py` stays flat (`Relic`/`RelicSpec`/`RelicGrade` together) rather
  than splitting into one file per class — matches the codebase's existing
  convention (`core/relic.py` today already does this), only the *catalog* of
  concrete relics gets one-file-per-item treatment.
- `best_ante.py` replaces the more literal `meta_progression.py`/
  `progression.py`: it names what it actually tracks instead of a vague
  genre term.
- Rejected `mastermind-run`/`mastermind_run` as a package name candidate: it
  would stutter against the `run/` subfolder already planned inside the
  overlay package (`mastermind_overlay/run/run_state.py`).

## Migration notes

- Today everything lives in one package (`mastermind`, `src/mastermind/`,
  see `pyproject.toml`). Moving to this layout means introducing a
  `[tool.uv.workspace]` root and giving each of the three packages its own
  `pyproject.toml` + `hatchling` build config — `uv` handles workspace
  member resolution natively, no extra tooling needed.
- Grep the repo for anything importing `mastermind.core.*` or
  `mastermind.*` more broadly before the actual move — `core/`, `engine/`,
  `curses_backend/`, `screens/` are being fully replaced/redistributed
  across the three new packages, not kept alongside them.
