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
- [x] shop screen between antes
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

## IDEAS BALATRO LIKE

### Already in place
- score loop = chips x mult, with a single interception hook (relics ~ jokers)
- ante that rises + difficulty curve
- Small/Big/Boss blinds with a target multiplier per blind
- shop between every round, buying relics and a fixed upgrade (extra guess)
- end-of-round reward tied to performance (turns left, margin)

### Partially there (concept exists, very reduced version)
- **Jokers/relics**: Balatro has ~150 jokers with varied triggers (on scored card, on discard, end of round, rarity, negative editions) and a limited number of slots. We have 4 fixed relics, all triggered at the same point (`act()` per guess), no slot limit, no rarity/price variation.
  - [ ] cap the number of relic slots
  - [ ] add rarity tiers with varying price
  - [ ] add more trigger points beyond per-guess (end of round, on shop enter...)
  - [ ] negative/edition-like modifiers on relics
- **Boss Blind**: `Blind.BOSS` exists (`is_boss`) but has no actual effect yet. In Balatro every boss imposes a unique rule (debuff a color, one guess only, double the bar...).
  - [ ] give `Blind.BOSS` a real mutator effect
  - [ ] hook the mutator into `GameState` / scoring
  - [ ] clear announcement of the active boss rule before the round starts
- **Shop**: Balatro has 2 card slots + packs (Arcana/Celestial/Spectral/Standard) + a voucher + a paid reroll. We have a flat list of relics + 1 fixed item, no reroll, no packs.
  - [ ] reroll offer for currency
  - [ ] packs (batch of choices) instead of single items
  - [ ] permanent vouchers (interest, extra hand, bigger inventory...) separate from one-shot buys

### Completely missing
- **Enhanced pegs (deckbuilding)**: in Balatro every card can carry an enhancement (Bonus/Mult/Wild/Glass/Steel/Gold), an edition (Foil/Holo/Polychrome/Negative), and a seal. Our pegs are just a color, no upgrade layer at all — this is the biggest missing piece.
- **Tarot / Spectral / Planet cards**: consumables that modify the deck or level up a hand type. We have no consumable layer at all.
- **Interest on currency**: Balatro rewards holding cash ($1 per $5 held, capped). Our `reward_for` gives no incentive to save currency.
- **Skip blind for a Tag**: no equivalent.
- **Run victory condition**: Balatro ends (or goes endless) after the ante 8 boss. Our `RunState.advance_ante` climbs forever — there is no run-win condition, only a loss condition.
- **Meta-progression across runs** (stakes, persistent unlocks) — already tracked above, nothing implemented yet.
