#!/usr/bin/env python3
"""This script generates the Pokete wiki"""
import os
import release
import scrap_engine as se
from pokete_classes.effects import effects, effect_list
from pokete_data import *


class Wiki:
    """The class in which wiki generation behaviour is defined"""
    @staticmethod
    def start() -> str:
        """The start and title of the wiki

        Returns:
        ---
        The title of the wiki page.
        """
        return f"""v{release.VERSION}

# Pokete wiki
This wiki/documentation is a compilation of all Poketes/attacks/types present in the Pokete game.
This wiki can be generated using ```$ ./gen-wiki.py```.

"""

    @staticmethod
    def table_of_contents() -> str:
        """The table of contents of the pokete wiki

        Returns:
        -------
        A Table of contents for a single page wiki.
        """
        out = """## Table of contents
1. [Poketes](#poketes)
"""

        # Table of contents
        for i, typ in enumerate(sorted(types)):
            out += f"""   {i + 1}. [{typ.capitalize()} Poketes](#{typ}-poketes)\n"""
            for j, poke in enumerate([k for k in sorted(list(pokes)[1:]) if pokes[k]["types"][0] == typ]):
                out += f"""       {j + 1}. [{pokes[poke]["name"]}](#{poke.replace("_", "-")})\n"""
        out += "2. [Attacks](#attacks)\n"
        for i, typ in enumerate(sorted(types)):
            out += f"""   {i + 1}. [{typ.capitalize()} attacks](#{typ}-attacks)\n"""
            for j, atc in enumerate([k for k in sorted(attacks) if attacks[k]["types"][0] == typ]):
                out += f"""       {j + 1}. [{attacks[atc]["name"]}](#{atc.replace("_", "-")})\n"""
        out += """3. [Types](#types)
4. [Items](#items)
"""
        for j, item in enumerate(sorted(items)):
            out += f"""   {j + 1}. [{items[item]["pretty_name"]}](#{item.replace("_", "-")})\n"""
        out += """5. [Effects](#effects)
"""
        for j, effect in enumerate(effect_list):
            out += f"""   {j + 1}. [{effect.c_name.capitalize()}](#{effect.c_name.replace("_", "-")})
"""

        return out

    @staticmethod
    def poketes() -> str:
        """The function to add all poketes and their attributes to the wiki.

        Returns:
        -------
        All poketes and their attributes as a markdown string.
        """
        out = """
## Poketes
In the following all Poketes with their attributes are displayed.

"""
        for typ in sorted(types):
            out += f"### {typ.capitalize()} Poketes"
            for poke in [k for k in sorted(list(pokes)[1:]) if pokes[k]["types"][0] == typ]:
                print(f' -> Adding {pokes[poke]["name"]}')
                out += Wiki.poke_info(poke)
        return out

    @staticmethod
    def poke_info(poke: str) -> str:
        """Generates information about a specific pokete

        Arguments:
        ---------
        - poke (string): The pokete to get the information of.

        Returns:
        -------
        A markdown string of all the attributes and information of the pokete.
        """
        evolve_txt = f"""- Evolves to [{pokes[pokes[poke]["evolve_poke"]]["name"]}](#{pokes[poke]["evolve_poke"]}) at level {pokes[poke]["evolve_lvl"]}""" if \
            pokes[poke]["evolve_poke"] != "" else "- Does not evolve\n"
        md_attacks = ""
        for atc in pokes[poke]["attacks"]:
            md_attacks += f"""\n   + [{attacks[atc]["name"]}](#{atc.replace("_", "-")})"""
        # ico
        ico_map = se.Map(4, 11, background=" ")
        for ico in pokes[poke]["ico"]:
            se.Text(ico["txt"], state="float", ignore=" ").add(ico_map, 0, 0)
        ico = "".join(["".join(arr) + "\n" for arr in ico_map.map])
        return f"""
#### {pokes[poke]["name"]}
{pokes[poke]["desc"]}

```
{ico}
```

- Type: [{pokes[poke]["types"][0].capitalize()}](#types)
- Health points: {pokes[poke]["hp"]}
- Attack factor: {pokes[poke]["atc"]}
- Defense factor: {pokes[poke]["defense"]}
- Initiative: {pokes[poke]["initiative"]}
- Missing chance: {pokes[poke]["miss_chance"]}
- Rarity: {pokes[poke]["rarity"]}
- Loosing experience: {pokes[poke]["lose_xp"]}
- Attacks:{md_attacks}
{evolve_txt}
"""

    @staticmethod
    def attacks() -> str:
        """The function to all attacks to the wiki.

        Returns:
        -------
        A markdown string of all attacks with their attributes and informations.
        """
        out = """
## Attacks
Those are all attacks present in the game.
"""
        for typ in sorted(types):
            out += f"\n### {typ.capitalize()} attacks"
            for atc in [k for k in attacks if attacks[k]["types"][0] == typ]:
                print(f' -> Adding {attacks[atc]["name"]}')
                out += Wiki.attack_info(atc)

        return out

    @staticmethod
    def attack_info(attack: str) -> str:
        """The function to collect information and attributes of a specific attack

        Arguments:
        ---------
        - attacks (string): The attack to collect the information of.

        Returns:
        -------
        A markdown string with the information about the attack.
        """
        eff = None if attacks[attack]["effect"] is None else getattr(effects, attacks[attack]["effect"])
        return f"""
#### {attacks[attack]["name"]}
{attacks[attack]["desc"]}

- Type: [{attacks[attack]["types"][0].capitalize()}](#types)
- Minimum Level: {attacks[attack]["min_lvl"]}
- Attack factor: {attacks[attack]["factor"]}
- Missing chance: {attacks[attack]["miss_chance"]}
- Attack points: {attacks[attack]["ap"]}
- Effect: {"None" if eff is None else f'[{eff.c_name.capitalize()}](#{eff.c_name.replace("_", "-")})'}
"""

    @staticmethod
    def types() -> str:
        """The function to add all types to the wiki.

        Returns:
        -------
        A markdown string of all available types.
        """
        out = """
## Types
Those are all the Pokete/Attack types that are present in the game with all their (in)effectivities against other types.

|Type|Effective against|Ineffective against|
|---|---|---|
"""

        for poke_type in types:
            effective, ineffective = ("".join([i.capitalize() + (", "
                                                                 if i != types[poke_type][j][-1]
                                                                 else "")
                                               for i in types[poke_type][j]])
                                      for j in ["effective", "ineffective"])
            out += f"|{poke_type.capitalize()}|{effective}|{ineffective}|\n"

        return out

    @staticmethod
    def items() -> str:
        """The function to add all items to the wiki.

        Returns:
        -------
        A markdown string that contains information about all items.
        """
        out = """
## Items
Those are all items present in the game, that can be traded or found.
"""

        for item in sorted(items):
            out += Wiki.item_info(item)
        return out

    @staticmethod
    def item_info(item: str) -> str:
        """The function to collect information and attributes of a specific item

        Arguments:
        ---------
        - item (string): The item to collect the information of.

        Returns:
        -------
        A markdown string with the information about the item.
        """
        return f"""
### {items[item]["pretty_name"]}
{items[item]["desc"]}

- Price: {items[item]["price"]}
- Can be used in fights: {"Yes" if items[item]["fn"] is not None else "No"}
"""

    @staticmethod
    def effects() -> str:
        """The function to add all effects to the wiki.

        Returns:
        -------
        A markdown string of all the effects in the game.
        """
        out = """
## Effects
Those effects can be given to a Pokete through an attack.
"""
        out += str.join("", [effect.ret_md() for effect in effect_list])
        return out

    @staticmethod
    def single(filename: str = "wiki.md") -> None:
        """The function to generate a single page wiki.

        This function creates the pokete wiki in a single file and adds the following to it:
        - title
        - table of contents
        - all poketes with information on them
        - all attacks with information on them
        - all types with information on them
        - all items with information on them
        - all effects with information on them

        Arguments:
        ---------
        - filename (string): The file to save the wiki to.
        """
        print(":: Generating wiki.md...")
        print("==> Adding page start...")
        md_str = Wiki.start()
        print("==> Adding table of contents...")
        md_str += Wiki.table_of_contents()
        print("==> Adding poketes...")
        md_str += Wiki.poketes()
        print("==> Adding attacks...")
        md_str += Wiki.attacks()
        print("==> Adding types...")
        md_str += Wiki.types()
        print("==> Adding items...")
        md_str += Wiki.items()
        print("==> Adding effects...")
        md_str += Wiki.effects()

        # writing to file
        print("==> Writing to wiki.md...")
        with open(filename, "w+") as file:
            file.write(md_str)


def gen_pics():
    """The function to generate a markdown file with some example pictures."""
    md_str = "# Example pictures\n"
    md_str += str.join("\n\n", [f"![{i}](ss/{i})" for i in sorted(os.listdir("assets/ss"))])

    # writing to file
    with open("assets/pics.md", "w+") as file:
        file.write(md_str)


if __name__ == "__main__":
    Wiki.single()
    print(":: Generating pics.md...")
    gen_pics()
