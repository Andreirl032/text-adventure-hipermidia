import json

# Carregar os dados do jogo
with open("game.json", "r", encoding="utf-8") as file:
    game_data = json.load(file)

# Estado do jogador
player = {
    "location": game_data["startLocationId"],
    "attack": game_data["attack"],
    "defense": game_data["defense"],
    "life": game_data["life"],
    "inventory": []
}

# Função para obter a localização atual
def get_current_location():
    return next((loc for loc in game_data["locations"] if loc["id"] == player["location"]), None)

# Função para exibir a localização atual
def show_location():
    location = get_current_location()
    if location:
        print(f"\nVocê está em: {location['name']}")
        print(location["description"])
        
        # Mostrar saídas disponíveis
        if location["exits"]:
            print("\nSaídas:")
            for exit in location["exits"]:
                if not exit["inactive"]:
                    print(f"- {exit['direction']} -> {exit['targetLocationId']}")

        # Mostrar inimigos
        if location["enemies"]:
            print("\nInimigos:")
            for enemy in location["enemies"]:
                print(f"- Ataque: {enemy['attack']}, Defesa: {enemy['defense']}")

        # Mostrar itens
        if location["items"]:
            print("\nItens disponíveis:")
            for item in location["items"]:
                print(f"- {item['name']}")

# Função para movimentar o jogador
def move(direction):
    location = get_current_location()
    for exit in location["exits"]:
        if exit["direction"].lower() == direction.lower() and not exit["inactive"]:
            player["location"] = exit["targetLocationId"]
            return True
    return False

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
                print(f"Você se moveu para {direction}.")
            else:
                print("Movimento inválido.")
        else:
            print("Comando não reconhecido.")

game_loop()
