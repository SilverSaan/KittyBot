# KittyBot

KittyBot is a Discord bot designed to streamline your Cyberpunk Red tabletop role-playing sessions. Whether you're a Game Master trying to improvise a Night Market on the fly or a Player hunting for the meaning of a corporate slur, Kitty has your back.

---

## Features

### Dice Rolling
No need to open a separate app. Kitty handles Cyberpunk Red's specific dice math natively.
*   `/red d10` – Rolls a standard CPR d10. Automatically handles exploding 10s (rolls again and adds) and imploding 1s (rolls again and subtracts).
*   `/red 4d6` – Rolls damage. If two or more 6s are rolled, it flags a Critical Injury automatically.
*   `/roll <n>d<x>` – A standard, universal dice roller for any other gaming needs.

### Reference Lookup
Never get lost in translation in the Time of the Red.
*   `/streetslang <term>` – Direct definition search (e.g., `/streetslang choom`).
*   `/streetslang search <query>` – Searches both keys and descriptions for a keyword.
*   `/streetslang random` – Feeds you a random piece of slang to spice up your roleplay.

### Random Generators
Instantly manifest assets locally.
*   **Character Generation:** Instantly builds an NPC using the *Streetrat* rules from the CPR Core Rulebook.
*   **Net Architecture:** Generates complete Net Architectures (Powered by [NetGenerator](https://github.com/MildarAA/NetGenerator)).
*   **Night Markets:** Spawns a fully stocked Night Market instantly (Powered by [Night Market Generator](https://gitlab.com/shindranel/night-market-generator)).

---

## Support & Feedback

Encountered a bug? Have an idea for a cool new feature? 
*   **Support Server:** [Join our Discord Server](#) *(Link Coming Soon)*
*   **Developer Contact:** pedrohpss@tutamail.com

---

## Legal
*Cyberpunk Red is a trademark of R. Talsorian Games. KittyBot is an independent fan project and is not affiliated with or endorsed by R. Talsorian Games.*
