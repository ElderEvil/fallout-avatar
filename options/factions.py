from enum import StrEnum

from options.races import Race


class Faction(StrEnum):
    VAULT_DWELLER = "Vault Dweller"
    BROTHERHOOD_OF_STEEL = "Brotherhood of Steel"
    ENCLAVE = "Enclave"
    MINUTEMEN = "Minutemen"
    RAIDERS = "Raiders"
    SUPER_MUTANT_TRIBE = "Super Mutant Tribe"
    CHILDREN_OF_ATOM = "Children of Atom"
    THE_INSTITUTE = "The Institute"
    RAILROAD = "Railroad"
    NCR = "New California Republic (NCR)"
    CAESARS_LEGION = "Caesar's Legion"
    NONE = "Not affiliated with any faction"


faction_options = list(Faction)

faction_restrictions = {
    Race.HUMAN: [
        Faction.VAULT_DWELLER,
        Faction.BROTHERHOOD_OF_STEEL,
        Faction.ENCLAVE,
        Faction.MINUTEMEN,
        Faction.RAIDERS,
        Faction.CHILDREN_OF_ATOM,
        Faction.THE_INSTITUTE,
        Faction.RAILROAD,
        Faction.NCR,
        Faction.CAESARS_LEGION,
        Faction.NONE,
    ],
    Race.GHOUL: [
        Faction.VAULT_DWELLER,
        Faction.RAIDERS,
        Faction.CHILDREN_OF_ATOM,
        Faction.NONE,
    ],
    Race.SUPER_MUTANT: [
        Faction.SUPER_MUTANT_TRIBE,
        Faction.RAIDERS,
        Faction.NONE,
    ],
    Race.SYNTH: [
        Faction.THE_INSTITUTE,
        Faction.RAILROAD,
        Faction.NONE,
    ],
}
