#!/usr/bin/env python3
"""
╔══════════════════════════════════════════╗
║      🌀  LABYRINTHE DES OMBRES  🌀       ║
║         Shadow Maze — Python CLI         ║
╚══════════════════════════════════════════╝
"""

import os
import re

# ─── Rich (optional) ──────────────────────────────────────────────────────────
try:
    from rich.console import Console
    from rich.panel import Panel
    RICH = True
    console = Console()
except ImportError:
    RICH = False

# ─── Maze (1=wall, 0=path, 2=exit) ────────────────────────────────────────────
MAZE = [
    [1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,1,0,0,0,0,0,1],
    [1,0,1,0,1,0,1,1,1,0,1],
    [1,0,1,0,0,0,0,0,1,0,1],
    [1,0,1,1,1,1,1,0,1,0,1],
    [1,0,0,0,0,0,1,0,0,0,1],
    [1,1,1,0,1,0,1,1,1,0,1],
    [1,0,0,0,1,0,0,0,0,0,1],
    [1,0,1,1,1,1,1,0,1,0,1],
    [1,0,0,0,0,0,0,0,1,2,1],
    [1,1,1,1,1,1,1,1,1,1,1],
]
ROWS  = len(MAZE)
COLS  = len(MAZE[0])
START = (1, 1)
EXIT  = (9, 9)

# ─── All direction keywords (always accepted regardless of language) ───────────
DIRECTIONS = {
    "n":(-1,0),"north":(-1,0),"nord":(-1,0),"haut":(-1,0),"up":(-1,0),
    "s":(1,0),"south":(1,0),"sud":(1,0),"bas":(1,0),"down":(1,0),
    "e":(0,1),"east":(0,1),"est":(0,1),"droite":(0,1),"right":(0,1),
    "w":(0,-1),"west":(0,-1),"ouest":(0,-1),"gauche":(0,-1),"left":(0,-1),
}

# ─── Localisation strings ──────────────────────────────────────────────────────
LANG = {
    "fr": {
        "menu_title":    "🌀  LABYRINTHE DES OMBRES  🌀",
        "menu_sub":      "Choisissez votre langue / Choose your language",
        "menu_opt1":     "1  🇫🇷  Français",
        "menu_opt2":     "2  🇬🇧  English",
        "menu_prompt":   "Votre choix (1 ou 2) : ",
        "menu_invalid":  "⚠  Entrée invalide. Tapez 1 ou 2.",
        "maze_title":    "🌀 Labyrinthe des Ombres",
        "how_to_play":   "📖 MODE D'EMPLOI",
        "welcome_rich":  (
            "[bold magenta]Bienvenue dans le Labyrinthe des Ombres ![/bold magenta]\n\n"
            "[cyan]Déplacements :[/cyan] nord | sud | est | ouest | haut | bas | gauche | droite\n"
            "[yellow]aide[/yellow] — indice  |  [yellow]position[/yellow] — où suis-je ?\n"
            "[yellow]recommencer[/yellow] — rejouer  |  [red]quitter[/red] — quitter\n"
            "[dim]menu[/dim] — changer de langue"
        ),
        "welcome_plain": (
            "  Bienvenue !\n"
            "  Déplacements: nord sud est ouest haut bas gauche droite\n"
            "  aide | position | recommencer | quitter | menu"
        ),
        "guide":         "🤖 Guide",
        "you":           "🧭 Vous ",
        "dirs_label":    "Directions libres",
        "dir_names":     ["Nord ↑","Sud  ↓","Est  →","Ouest←"],
        "moved":         "✅ Déplacement !  Pas",
        "wall":          "🧱 Mur ! Tu ne peux pas aller par là.",
        "no_dir":        "Aucune direction libre !",
        "pos_msg":       "📍 Ligne {r}, colonne {c}  |  Pas : {steps}",
        "hint_prefix":   "💡 Indice",
        "hint_default":  "Explore chaque couloir ! La sortie est en bas à droite.",
        "already_won":   "Tu as déjà gagné ! Tape 'recommencer'.",
        "reset":         "🔄 Labyrinthe réinitialisé !",
        "won_title":     "🎉  BRAVO — TU AS GAGNÉ !  🎉",
        "won_rich":      "Sortie en [bold yellow]{steps}[/bold yellow] pas !\nTape [cyan]'recommencer'[/cyan] ou [cyan]'quitter'[/cyan].",
        "won_plain":     "🎉 BRAVO ! Sortie en {steps} pas ! recommencer / quitter",
        "bye":           "Au revoir ! 👋",
        "unknown":       (
            "❓ Commande inconnue. Essaie :\n"
            "   nord | sud | est | ouest | haut | bas | gauche | droite\n"
            "   aide | position | recommencer | quitter | menu"
        ),
        "hint_keys":    {"aide","indice","help","hint","?"},
        "restart_keys": {"recommencer","restart","reset","rejouer","retry","again"},
        "pos_keys":     {"position","pos","ou","ou","where","loc"},
        "quit_keys":    {"quitter","sortir","quit","exit","bye","q"},
        "menu_keys":    {"menu","langue","language","changer"},
    },
    "en": {
        "menu_title":    "🌀  SHADOW MAZE  🌀",
        "menu_sub":      "Choose your language / Choisissez votre langue",
        "menu_opt1":     "1  🇫🇷  Français",
        "menu_opt2":     "2  🇬🇧  English",
        "menu_prompt":   "Your choice (1 or 2): ",
        "menu_invalid":  "⚠  Invalid input. Type 1 or 2.",
        "maze_title":    "🌀 Shadow Maze",
        "how_to_play":   "📖 HOW TO PLAY",
        "welcome_rich":  (
            "[bold magenta]Welcome to the Shadow Maze![/bold magenta]\n\n"
            "[cyan]Move with:[/cyan] north | south | east | west | up | down | left | right\n"
            "[yellow]hint[/yellow] — get a clue  |  [yellow]position[/yellow] — where am I?\n"
            "[yellow]restart[/yellow] — play again  |  [red]quit[/red] — leave\n"
            "[dim]menu[/dim] — change language"
        ),
        "welcome_plain": (
            "  Welcome!\n"
            "  Move: north south east west up down left right\n"
            "  hint | position | restart | quit | menu"
        ),
        "guide":         "🤖 Guide",
        "you":           "🧭 You  ",
        "dirs_label":    "Open directions",
        "dir_names":     ["North ↑","South ↓","East  →","West  ←"],
        "moved":         "✅ You moved!  Steps",
        "wall":          "🧱 Wall! You can't go that way.",
        "no_dir":        "No open direction!",
        "pos_msg":       "📍 Row {r}, col {c}  |  Steps: {steps}",
        "hint_prefix":   "💡 Hint",
        "hint_default":  "Explore every corridor! The exit is bottom-right.",
        "already_won":   "You already won! Type 'restart'.",
        "reset":         "🔄 Maze reset!",
        "won_title":     "🎉  CONGRATULATIONS — YOU WON!  🎉",
        "won_rich":      "Exit found in [bold yellow]{steps}[/bold yellow] steps!\nType [cyan]'restart'[/cyan] or [cyan]'quit'[/cyan].",
        "won_plain":     "🎉 You won in {steps} steps! restart / quit",
        "bye":           "Goodbye! 👋",
        "unknown":       (
            "❓ Unknown command. Try:\n"
            "   north | south | east | west | up | down | left | right\n"
            "   hint | position | restart | quit | menu"
        ),
        "hint_keys":    {"hint","aide","help","indice","?"},
        "restart_keys": {"restart","reset","again","retry","recommencer","rejouer"},
        "pos_keys":     {"position","pos","where","loc","ou","où"},
        "quit_keys":    {"quit","exit","bye","q","quitter","sortir"},
        "menu_keys":    {"menu","language","langue","change"},
    },
}

HINTS = {
    "fr": {
        (1,1):"Tu es au départ ! Dirige-toi vers l'est ou le sud.",
        (1,5):"Bon chemin ! Continue d'explorer.",
        (3,3):"Des murs partout… cherche bien !",
        (5,3):"Mi-chemin ! La sortie est en bas à droite.",
        (7,1):"Tu descends bien. La sortie est à l'est.",
        (9,7):"Presque là ! La sortie est juste à l'est.",
    },
    "en": {
        (1,1):"You're at the start! Head east or south.",
        (1,5):"Good path! Keep exploring.",
        (3,3):"Walls everywhere — look carefully!",
        (5,3):"Halfway there! The exit is bottom-right.",
        (7,1):"Going down nicely. Exit is east.",
        (9,7):"Almost there! Exit is just east of you!",
    },
}

# ─── UI helpers ───────────────────────────────────────────────────────────────

def clr():
    os.system("cls" if os.name == "nt" else "clear")

def sep():
    if RICH: console.rule(style="dark_violet")
    else: print("─" * 50)

def strip_rich(text):
    return re.sub(r"\[.*?\]", "", text)

def bot(text, L, style="cyan"):
    if RICH:
        console.print(f"[bold {style}]{L['guide']} ›[/bold {style}] {text}")
    else:
        print(f"{L['guide']} > {strip_rich(text)}")

def you(text, L):
    if RICH:
        console.print(f"[bold white]{L['you']} ›[/bold white] {text}")
    else:
        print(f"{L['you']} > {text}")

def render_maze(player):
    lines = []
    for ri, row in enumerate(MAZE):
        line = ""
        for ci, cell in enumerate(row):
            if (ri, ci) == player:        line += "🔮"
            elif (ri, ci) == EXIT:        line += "🚪"
            elif (ri,ci)==START!=player:  line += "✦ "
            elif cell == 1:               line += "██"
            else:                         line += "  "
        lines.append(line)
    return lines

def print_maze(player, L):
    lines = render_maze(player)
    if RICH:
        console.print(Panel(
            "\n".join(lines),
            title=f"[bold magenta]{L['maze_title']}[/bold magenta]",
            border_style="dark_violet", padding=(0,1),
        ))
    else:
        print("┌" + "─"*24 + "┐")
        for l in lines: print("│ " + l + " │")
        print("└" + "─"*24 + "┘")

def avail_dirs(r, c, L):
    deltas = [(-1,0),(1,0),(0,1),(0,-1)]
    names  = L["dir_names"]
    return [(names[i], deltas[i]) for i in range(4)
            if 0<=r+deltas[i][0]<ROWS and 0<=c+deltas[i][1]<COLS
            and MAZE[r+deltas[i][0]][c+deltas[i][1]] != 1]

def show_dirs(r, c, L):
    dirs = avail_dirs(r, c, L)
    if not dirs: bot(L["no_dir"], L, "red"); return
    bot(f"{L['dirs_label']}: {' | '.join(n for n,_ in dirs)}", L, "yellow")

def parse(raw, L):
    for tok in raw.lower().strip().split():
        if tok in DIRECTIONS:         return ("move", DIRECTIONS[tok])
        if tok in L["hint_keys"]:     return ("hint",)
        if tok in L["restart_keys"]:  return ("restart",)
        if tok in L["pos_keys"]:      return ("pos",)
        if tok in L["quit_keys"]:     return ("quit",)
        if tok in L["menu_keys"]:     return ("menu",)
    return ("unknown", raw)

# ─── Language menu ────────────────────────────────────────────────────────────

def language_menu():
    clr()
    M = LANG["fr"]   # menu strings are language-agnostic
    if RICH:
        console.print(Panel(
            f"[bold cyan]{M['menu_sub']}[/bold cyan]\n\n"
            f"  [bold green]{M['menu_opt1']}[/bold green]\n"
            f"  [bold blue ]{M['menu_opt2']}[/bold blue ]",
            title=f"[bold magenta]{M['menu_title']}[/bold magenta]",
            border_style="magenta", padding=(1,4),
        ))
    else:
        print("=" * 50)
        print(f"  {M['menu_title']}")
        print("=" * 50)
        print(f"\n  {M['menu_sub']}\n")
        print(f"    {M['menu_opt1']}")
        print(f"    {M['menu_opt2']}\n")

    while True:
        try:
            choice = input(f"  {M['menu_prompt']}").strip()
        except (EOFError, KeyboardInterrupt):
            print(); return "fr"
        if choice == "1": return "fr"
        if choice == "2": return "en"
        print(M["menu_invalid"]) if not RICH else console.print(f"[red]{M['menu_invalid']}[/red]")

# ─── Game loop ────────────────────────────────────────────────────────────────

def game_loop(lang_code):
    L   = LANG[lang_code]
    H   = HINTS[lang_code]
    pos, steps, won = START, 0, False

    clr(); sep()
    if RICH:
        console.print(Panel(L["welcome_rich"],
            title=f"[bold yellow]{L['how_to_play']}[/bold yellow]",
            border_style="magenta"))
    else:
        print(L["welcome_plain"])
    sep(); print_maze(pos, L); show_dirs(*pos, L); sep()

    while True:
        try:
            raw = input("  ▶  ").strip()
        except (EOFError, KeyboardInterrupt):
            bot(L["bye"], L, "magenta"); return "quit"

        if not raw: continue
        you(raw, L)
        action = parse(raw, L)

        if action[0] == "quit":
            bot(L["bye"], L, "magenta"); return "quit"

        elif action[0] == "menu":
            return "menu"

        elif action[0] == "restart":
            pos, steps, won = START, 0, False
            clr(); bot(L["reset"], L, "yellow")
            print_maze(pos, L); show_dirs(*pos, L)

        elif action[0] == "hint":
            bot(f"{L['hint_prefix']} : {H.get(pos, L['hint_default'])}", L, "yellow")

        elif action[0] == "pos":
            bot(L["pos_msg"].format(r=pos[0], c=pos[1], steps=steps), L, "blue")
            show_dirs(*pos, L)

        elif action[0] == "move":
            if won:
                bot(L["already_won"], L, "green")
            else:
                dr, dc = action[1]
                nr, nc = pos[0]+dr, pos[1]+dc
                if 0<=nr<ROWS and 0<=nc<COLS and MAZE[nr][nc] != 1:
                    pos = (nr, nc); steps += 1
                    if pos == EXIT:
                        won = True; clr(); print_maze(pos, L); sep()
                        if RICH:
                            console.print(Panel(L["won_rich"].format(steps=steps),
                                title=f"[bold green]{L['won_title']}[/bold green]",
                                border_style="green"))
                        else:
                            print(L["won_plain"].format(steps=steps))
                    else:
                        clr(); print_maze(pos, L)
                        bot(f"{L['moved']} : {steps}", L, "green")
                        if h := H.get(pos): bot(f"💬 {h}", L, "yellow")
                        show_dirs(*pos, L)
                else:
                    bot(L["wall"], L, "red")

        else:
            bot(L["unknown"], L, "red")

        sep()

# ─── Entry point ──────────────────────────────────────────────────────────────

def main():
    while True:
        lang   = language_menu()
        result = game_loop(lang)
        if result == "quit":
            break
        # result == "menu" → back to language selection

if __name__ == "__main__":
    main()
