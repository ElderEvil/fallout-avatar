from enum import StrEnum


class Race(StrEnum):
    HUMAN = "Human"
    GHOUL = "Ghoul"
    SUPER_MUTANT = "Super Mutant"
    SYNTH = "Synth"


class Gender(StrEnum):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"


class GhoulFeralness(StrEnum):
    SANE = "Sane"
    PARTIALLY_FERAL = "Partially Feral"
    FULLY_FERAL = "Fully Feral"


class SuperMutantMutation(StrEnum):
    MILD = "Mild Mutation"
    SEVERE = "Severe Mutation"
    BEHEMOTH = "Behemoth-Level Mutation"


class SynthType(StrEnum):
    GEN_3 = "Gen 3 (Human-like)"
    GEN_2 = "Gen 2 (Cyborg-like)"
    GEN_1 = "Gen 1 (Metallic Android)"


race_descriptions = {
    Race.GHOUL: "A Ghoul is a human with visible radiation scarring and leathery, slightly decayed skin.Their facial features are worn and aged, but they still retain human expressions and emotions. Their eyes may appear sunken, and their skin tone varies from pale to ashen, but they remain distinctly humanoid.",
    Race.SUPER_MUTANT: "A Super Mutant is a large, muscular humanoid with green or dark green skin.Their body appears strengthened by mutation, giving them a powerful and bulky frame. They have rough skin and battle scars but still maintain an expressive, intelligent face.",
    Race.SYNTH: "A Synth is a humanoid with artificial skin, appearing almost indistinguishable from a human.Some areas may have subtle seams or metallic plating, but their expressions and body language are fully natural, resembling a person with advanced cybernetic enhancements.",
}
