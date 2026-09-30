# Expiration Cluster Policy

*Rules for managing three or more active option campaigns sharing the same expiration date.*

## 1. Principles
1. **Candidate quality comes first:** Expiration date is never a gate, ranking input, or tiebreaker during initial screening.
2. **Assignment capacity verification:** Before opening any new short put, verify that the unencumbered cash reserve will remain ≥20% of CSP NAV after hypothetical simultaneous assignment of ALL open puts on that expiration date.
3. **Cluster management:**
   - When 3+ positions cluster on one expiry, open the 21-DTE checkpoint evaluation early (at 25 DTE).
   - Stagger roll/close decisions across multiple scheduled passes rather than executing simultaneously.
   - Act first on the position nearest its exit or trigger.
   - If the cluster creates assignment or reserve crowding, prefer closing over rolling (roll the strongest fundamental thesis, close the others).
   - If multiple assignments occur simultaneously, sequence covered calls in order of highest forward expected cash income.
