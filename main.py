#Andrei Ramos Lopes e Marcelo Antonio Carvalho Florentino
import json
import os

with open("game.json", "r", encoding="utf-8") as file:
    game_data = json.load(file)

player = {
    "location": game_data["startLocationId"],
    "attack": game_data["attack"],
    "defense": game_data["defense"],
    "life": game_data["life"],
    "usable_items": game_data["usable_items"],
    "inventory": []
}


def get_name_usableItems(id):
    for item in player["usable_items"]:
        if id == item["id"]:
            return item["name"]


def get_current_location():
    return next((loc for loc in game_data["locations"] if loc["id"] == player["location"]), None)

def get_location(id):
    return next((loc for loc in game_data["locations"] if loc["id"] == id), None)


def apply_puzzle_result(puzzle, result):
    if result["lose_life"] > 0:
        player["life"] -= result["lose_life"]
        print(
            f"Você perdeu {result['lose_life']} pontos de vida. Vida restante: {player['life']}")

    for item in result["lose_item"]:
        if item in player["inventory"]:
            player["inventory"].remove(item)
            print(f"Você perdeu o item: {item}")

    for activation in result["active"]:
        collect_item(activation)

    location = get_current_location()
    location["puzzles"].remove(puzzle)


def interact_with_puzzle(puzzle):
    print(f"\nEnigma: {puzzle['description']}")
    required_items = puzzle["solution"]["requiredItems"]
    has_required_items = all(
        item in player["inventory"] for item in required_items)

    if has_required_items:
        print(
            f"Você usa {', '.join([game_data['usable_items'][int(item)-1]['name'] for item in required_items])} e resolve o enigma!")
        apply_puzzle_result(puzzle, puzzle["result"])
    else:
        missing_items = [game_data["usable_items"][int(
            item)-1]["name"] for item in required_items if item not in player["inventory"]]
        print(
            f"Para resolver esse enigma, você precisa de {', '.join(missing_items)}.")


def collect_item(item_name):
    location = get_current_location()
    item = next(
        (i for i in location["items"] if i["name"].lower() == item_name.lower()), None)

    if item and item["can_take"]:
        if len(player["inventory"]) < int(game_data["max_itens"]):
            player["inventory"].append(item["id"])
            location["items"].remove(item)
            print(f"Você coletou: {item['name']}")

            print(
                f"Você recebeu um aprimoramento de defesa = {item["up_defense"]} - ataque = {item["up_attack"]} - vida = {item["up_life"]}")

            player["attack"] += item["up_attack"]
            player["defense"] += item["up_defense"]
            player["life"] += item["up_life"]

            item["can_take"] = False

        else:
            print("Seu inventário está cheio!")
    else:
        item = next((i for i in player["usable_items"]
                    if i["name"].lower() == item_name.lower()), None)
        if item and item["can_take"]:
            if len(player["inventory"]) < int(game_data["max_itens"]):
                player["inventory"].append(item["id"])
                # player["usable_items"].remove(item)
                print(f"Você coletou: {item['name']}")

                print(
                    f"Você recebeu um aprimoramento de defesa = {item["up_defense"]} - ataque = {item["up_attack"]} - vida = {item["up_life"]}")

                player["attack"] += item["up_attack"]
                player["defense"] += item["up_defense"]
                player["life"] += item["up_life"]

                item["can_take"] = False
            else:
                print("Seu inventário está cheio!")
        else:
            print("Esse item não pode ser coletado ou não está aqui.")


def show_location():
    location = get_current_location()
    if location:
        print(f"\nVocê está em: {location['name']}")
        print(location["description"])

        if location["exits"]:
            print("\nSaída(s):")
            print("Use 'ir direção' para se movimentar pelo mapa)")
            for exit in location["exits"]:
                if not exit["inactive"]:
                    print(
                        f"- {exit['direction']} -> {exit['targetLocationId']}")

        if location["enemies"]:
            print("\nInimigos:")
            print("\nUse 'atacar' para interagir")
            for enemy in location["enemies"]:
                print(
                    f"-Nome: {enemy['name']} Ataque: {enemy['attack']}, Defesa: {enemy['defense']}")

        if location["items"]:
            print("\nItens disponíveis:")
            for item in location["items"]:
                print(
                    f"- {item['name']} (use 'pegar {item['name'].lower()}' para coletar)")

        if location["puzzles"]:
            print("\nPuzzles disponíveis:")
            for puzzle in location["puzzles"]:
                print(
                    f"- {puzzle['description']} (use 'resolver {puzzle['id']}' para interagir)")

        if location["npcs"]:
            print("\n Npcs Disponíveis:")
            for npc in location["npcs"]:
                print(
                    f"- {npc["name"]} (use 'falar {npc["name"]}' para interagir) ")


def move(direction):
    location = get_current_location()
    for exit in location["exits"]:
        if exit["direction"].lower() == direction.lower() and not exit["inactive"]:
            player["location"] = exit["targetLocationId"]
            return True
    return False


def combat():
    location = get_current_location()
    if not location["enemies"]:
        print("Não há inimigos aqui.")
        return

    enemy = location["enemies"][0]
    print(
        f"\nVocê entrou em combate contra um inimigo! (Nome: {enemy['name']}, ATK: {enemy['attack']}, DEF: {enemy['defense']})")

    if enemy["attack"] > player["defense"]:
        dano = enemy["attack"] - player["defense"]
        player["life"] -= dano
        print(
            f"O inimigo ataca! Você recebe {dano} de dano. Vida atual: {player['life']}")
    else:
        print("Você bloqueou o ataque do inimigo!")

    if player["life"] <= 0:
        print("Você foi derrotado! Game Over.")
        exit()

    if player["attack"] > enemy["defense"]:
        print("Você derrotou o inimigo!")
        location["enemies"].remove(enemy)

        result = enemy["result"]

    else:
        print(f"O inimigo resistiu ao seu ataque! (DEF: {enemy['defense']})")


def talk_to_npc(npc_name):
    location = get_current_location()
    npc = None
    for x in location["npcs"]:
        if x["name"].lower() == npc_name.lower():
            npc = x
            break

    if not npc:
        print("Não existe ninguém com esse nome aqui")
        return

    print(f"\n{npc["name"]}: {npc["description"]}")

    for index, dialogue in enumerate(npc["dialogues"], 1):
        print(f"\nDiálogo {index}: {dialogue["text"]}")

        choice = int(input("\nEscolha um número para responder: ").strip())

        if choice in [1, 2, 3]:
            result = dialogue["result"]

            if choice == dialogue["key"]:
                print(f"\n{result[0]["key_text"]}")
                collect_item(result[0]["active"][0])
            else:
                print(f"\n{result[0]["text_error"]}")

        else:
            print("Escolha uma opção válida")


def show_player_stats():
    location = get_current_location()
    print("\n=== Status do Jogador ===")
    print(f"📍 Localização: {location["name"]}")
    print(f"⚔️  Ataque: {player['attack']}")
    print(f"🛡️  Defesa: {player['defense']}")
    print(f"❤️  Vida: {player['life']}")
    print("\n🎒 Inventário:")
    if player["inventory"]:
        for item in player["inventory"]:
            name = get_name_usableItems(item)
            print(f" {item} - {name}")
    else:
        print("  (Vazio)")
    print("=======================\n")


def game_loop():
    print(f"\nBem-vindo ao {game_data['title']}!\n{game_data['description']}")

    while player["life"] > 0:
        if player["location"] == 9:
            print("PARABÉNS! VOCÊ CONCLUIU O JOGO!")
            print("Feito por "+game_data["author"])
            break
        show_player_stats()
        print()
        show_location()
        command = input("\nO que deseja fazer? ").strip().lower()
            

        if command in ["sair", "exit", "quit"]:
            print("Saindo do jogo...")
            break
        elif command.startswith("ir "):
            location8 = get_location("8")
            direction = command.split(" ", 1)[1]
            if player["location"] == "8" and len(location8["enemies"]) > 0 and direction == "norte":
                os.system('cls')
                print("Você precisa derrotar o chefão final!")
                continue
            if move(direction):
                os.system('cls')
                print(f"Você se moveu para {direction}.")
            else:
                print("Movimento inválido.")
        elif command == "atacar":
            os.system('cls')
            combat()
        elif command.startswith("resolver "):
            os.system('cls')
            puzzle_id = command.split(" ", 1)[1]
            location = get_current_location()
            puzzle = next(
                (p for p in location["puzzles"] if p["id"] == puzzle_id), None)

            if puzzle:
                interact_with_puzzle(puzzle)
            else:
                print("Esse enigma não existe aqui.")
        elif command.startswith("pegar "):
            os.system('cls')
            item_name = command.split(" ", 1)[1]
            collect_item(item_name)
        elif command.startswith("falar "):
            os.system('cls')
            npc_name = command.split(" ", 1)[1]
            talk_to_npc(npc_name)
        elif command == "help":
            os.system('cls')
            print('\033[96m'+"Lista de comandos:")
            print("- sair/exit/quit")
            print("- ir")
            print("- atacar")
            print("- resolver")
            print("- pegar")
            print("- falar"+'\x1b[37m')
        else:
            os.system('cls')
            print("Comando não reconhecido.")


game_loop()
