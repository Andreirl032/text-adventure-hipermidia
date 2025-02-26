import json
import os

# Carregar os dados do jogo
with open("game.json", "r", encoding="utf-8") as file:
    game_data = json.load(file)

# Estado do jogador
player = {
    "location": game_data["startLocationId"],
    "attack": game_data["attack"],
    "defense": game_data["defense"],
    "life": game_data["life"],
    "usable_items": game_data["usable_items"],
    "inventory": []
}

print(player)

# Função para obter a localização atual
def get_current_location():
    return next((loc for loc in game_data["locations"] if loc["id"] == player["location"]), None)

# Função para aplicar os efeitos da solução do puzzle
def apply_puzzle_result(puzzle, result):
    if result["lose_life"] > 0:
        player["life"] -= result["lose_life"]
        print(f"Você perdeu {result['lose_life']} pontos de vida. Vida restante: {player['life']}")
    
    for item in result["lose_item"]:
        if item in player["inventory"]:
            player["inventory"].remove(item)
            print(f"Você perdeu o item: {item}")
    
    for activation in result["active"]:
        print(f"Algo mudou no mundo do jogo... ({activation})")
    
    # Remover puzzle após ser resolvido
    location = get_current_location()
    location["puzzles"].remove(puzzle)

# Função para interagir com puzzles
def interact_with_puzzle(puzzle):
    print(f"\nEnigma: {puzzle['description']}")
    required_items = puzzle["solution"]["requiredItems"]
    has_required_items = all(item in player["inventory"] for item in required_items)

    if has_required_items:
        print(f"Você usa {', '.join([game_data['usable_items'][int(item)-1]['name'] for item in required_items])} e resolve o enigma!")
        apply_puzzle_result(puzzle, puzzle["result"])
    else:
        missing_items = [game_data["usable_items"][int(item)-1]["name"] for item in required_items if item not in player["inventory"]]
        print(f"Para resolver esse enigma, você precisa de {', '.join(missing_items)}.")

# Função para coletar itens
def collect_item(item_name):
    location = get_current_location()
    item = next((i for i in location["items"] if i["name"].lower() == item_name.lower()), None)
    
    if item and item["can_take"]:
        if len(player["inventory"]) < int(game_data["max_itens"]):
            player["inventory"].append(item["id"])
            location["items"].remove(item)
            print(f"Você coletou: {item['name']}")
        else:
            print("Seu inventário está cheio!")
    else:
        print("Esse item não pode ser coletado ou não está aqui.")

# Função para exibir a localização atual
def show_location():
    location = get_current_location()
    if location:
        print(f"\nVocê está em: {location['name']}")
        print(location["description"])
        
        if location["exits"]:
            print("\nSaídas:")
            for exit in location["exits"]:
                if not exit["inactive"]:
                    print(f"- {exit['direction']} -> {exit['targetLocationId']}")

        if location["enemies"]:
            print("\nInimigos:")
            for enemy in location["enemies"]:
                print(f"- Ataque: {enemy['attack']}, Defesa: {enemy['defense']}")

        if location["items"]:
            print("\nItens disponíveis:")
            for item in location["items"]:
                print(f"- {item['name']} (use 'pegar {item['name'].lower()}' para coletar)")

        if location["puzzles"]:
            print("\nPuzzles disponíveis:")
            for puzzle in location["puzzles"]:
                print(f"- {puzzle['description']} (use 'resolver {puzzle['id']}' para interagir)")

# Função para movimentar o jogador
def move(direction):
    location = get_current_location()
    for exit in location["exits"]:
        if exit["direction"].lower() == direction.lower() and not exit["inactive"]:
            player["location"] = exit["targetLocationId"]
            return True
    return False

# Função para iniciar combate
def combat():
    location = get_current_location()
    if not location["enemies"]:
        print("Não há inimigos aqui.")
        return
    
    enemy = location["enemies"][0]  # Assume-se que haja apenas um inimigo por vez
    print(f"\nVocê entrou em combate contra um inimigo! (ATK: {enemy['attack']}, DEF: {enemy['defense']})")
    
    if enemy["attack"] > player["defense"]:
        dano = enemy["attack"] - player["defense"]
        player["life"] -= dano
        print(f"O inimigo ataca! Você recebe {dano} de dano. Vida atual: {player['life']}")
    else:
        print("Você bloqueou o ataque do inimigo!")
    
    if player["life"] <= 0:
        print("Você foi derrotado! Game Over.")
        exit()
    
    if player["attack"] > enemy["defense"]:
        print("Você derrotou o inimigo!")
        location["enemies"].remove(enemy)
    else:
        print(f"O inimigo resistiu ao seu ataque! (DEF: {enemy['defense']})")

# Loop principal do jogo
def game_loop():
    print(f"\nBem-vindo ao {game_data['title']}!\n{game_data['description']}")
    
    while player["life"] > 0:
        show_location()
        command = input("\nO que deseja fazer? ").strip().lower()

        if command in ["sair", "exit", "quit"]:
            print("Saindo do jogo...")
            break
        elif command.startswith("ir "):
            direction = command.split(" ", 1)[1]
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
            puzzle = next((p for p in location["puzzles"] if p["id"] == puzzle_id), None)
            
            if puzzle:
                interact_with_puzzle(puzzle)
            else:
                print("Esse enigma não existe aqui.")
        elif command.startswith("pegar "):
            item_name = command.split(" ", 1)[1]
            collect_item(item_name)
        else:
            print("Comando não reconhecido.")

game_loop()
