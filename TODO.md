## Make mastermind rogue-like
### Run/Score loop
- [x] instead of single wins/lost a Score that accumulates each try (chips x multiplier)
- [x] Progression with rising score
- [x] Run state separated from round state (ante counter, builds each round)
- [x] HUD showing ante, score, target score, turns left
- [x] distinct screens for round cleared vs run over

### Relics / Jokers
- [x] passive items that modify the chips/mult calculation
- [x] single hook/event point where relics can intercept scoring
- [x] display of the active relics inventory

### Economy / shop
- [x] currency earned at the end of a round (turns saved, score margin...)
- [ ] shop screen between antes
- [ ] purchases: relics, extra guess, hint, color reroll

### Enhanced pegs (deckbuilding)
- [ ] peg wrapper = color + optional enhancement
- [ ] a few simple enhancements (bonus on exact match, sacrifice for a hint...)
- [ ] way to obtain enhanced pegs (shop, round reward)

### Boss rounds / mutators
- [ ] special one-off rules per ante (hidden white feedback, banned color, two codes at once)
- [ ] clear announcement of the active rule before the round starts

### Meta-progression across runs
- [ ] persistent best ante reached / highscore
- [ ] progressive unlocks (relics, pegs) based on past runs

### Polish
- [ ] visual score feedback accumulating on screen (popups)
- [ ] stronger visual theme (extend ui/palette.py)
