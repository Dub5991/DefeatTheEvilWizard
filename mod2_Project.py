import random as r
import os
# ----------------------------------------------------------------------------------------------------
# Base Character class Flow
class Character:
    def __init__(self, name, health, attack_power, description):
        self.name = name 
        self.health = health
        self.attack_power = attack_power
        self.max_health = health  # Store the original health for maximum limit
        self.description = description
    
    def rand_attack(self, opponent): #Pulls from a random Multiplier
        multiplier = r.uniform(0.95, 1.15) #uniform manages our floats
        attack_damage = int(self.attack_power * multiplier)
        
        #Check if the opponent is in Defensive Stance:
        if isinstance(opponent, Warrior) and opponent.defense_active: #opponent is used in perspective of the Wizard
            attack_damage = int(attack_damage * 0.5) #reduced attack damage by 50%
          
        #Check if the opponent has Mana Shield Activated:    
        if isinstance(opponent,Mage) and opponent.mana_shield_active:
            damage_absorbed = min(self.attack_power, opponent.mana)
            opponent.mana -= damage_absorbed
            remaining_damage = self.attack_power = damage_absorbed
            opponent.health -= remaining_damage            
        
        
        opponent.health -= attack_damage
      
        
        if opponent.health <= 0:
            print(f"{opponent.name} has been defeated!")
        
    

    def display_stats(self, opponent):
        print(f"{opponent.name}'s Stats : \nHealth: {opponent.health}/{opponent.max_health}, Attack Power {opponent.attack_power}") #Boss's Stats for full understanding.
        print(f"{self.name}'s Stats : \nHealth: {self.health}/{self.max_health}, Attack Power: {self.attack_power}")
        
        
    def heal(self):
        heal_amount = self.max_health/2
        self.health = min(self.health + heal_amount, self.max_health)
        print(f"{self.name} regenerates {heal_amount} health! Current health: {self.health}/{self.max_health}") # num/num for clean format
        
                

# ----------------------------------------------------------------------------------------------------
#Create a list of Characters and 2 abilities:

# 1. Warrior class (inherits from Character)


class Warrior(Character):
    def __init__(self, name):
        super().__init__(name, health=140, attack_power= 30, description = "\nA lost soul on the road to find home, or what's left of it... ")  
        self.defense_active = False  #Default position is Offensive
        self.health = min(self.health, self.max_health) 
        
    
    #Special Abilities
    def Rage(self,name):
        self.attack_power = int(self.attack_power * 2)
       
        

    def Defensive_Stance(self):
        print(f"{self.name} assumes Defensive Stance! Damage is reduced: x0.5")
        self.defense_active = True
        
    def end_defence(self):
        if self.defense_active:
            print(f"{self.name} resumes offensive stance")
            self.defense_active = False

# 2. Mage class (inherits from Character)


class Mage(Character):
    def __init__(self, name):
        super().__init__(name, health=75, attack_power=18, description= "\nAn Alchemist on the prowl for exotic Flora and Fauna to craft new recipies... ") 
        self.mana = 50 #Add Mana Pool
        self.mana_shield_active = False #Add Mana Shield Status
        
    def mana_shield(self):
        if not self.mana_shield_active:
            self.mana_shield_active = True
            print(f"{self.name} has activated Mana Shield! Incoming damage will consume mana instead of health.")
        else:
            print(f"{self.name} already has Mana Shield active!") 
    
    def deactivate_mana_shield(self): #what goes up must come down - deactivation
        if self.mana_shield_active:
            self.mana_shield_active = False
            print("Deactivate Mana Shield")
        
    
    #Special Abilities
    def Fireball(self, opponent):
        print(f"{self.name} uses Fire Ball! An explosion occurs! Critial Damage x 3!")
        damage = int(self.attack_power * 3)
        opponent.health -= damage
        print(f"{opponent.name} takes {damage} damage from the Fireball!")
        
# 3. Spy Class (inherits from character)

class Spy(Character):
    def __init__(self, name):
        super().__init__(name, health = 60, attack_power = 50, description="\nThis sly fox has a knack for snooping about... ")
        
    def Thieving(self, opponent):
        print("Do you hear that?")
        print(f"A looming sensation leaves {opponent.name} confused!")
    
    def Confuse(self, opponent):
        print(f"{opponent.name} 'accidently' falls in near-by pit.. vanishing to safety...")
        opponent.health -= 500
        
 # 4. Clown (inherits from character)       
       
class Clown(Character):
    def __init__(self, name):
        super().__init__(name, health = 140, attack_power= 20, description="\nThis haphazardous fool will go anywhere.. if you let 'em... ")
        
    def Jesters_Trick(self, opponent):
        damage = int(self.attack_power * 1.5)
        opponent.health -= damage
        opponent.health -= damage
        opponent.health -= damage
        print(f"Very Effective! {self.name} Attacks 3 Times!!")
        

    def Laughing_Gas(self, opponent):
        heal_amount =opponent.max_health - 50
        self.health = self.health + heal_amount
        
        
# 5. EvilWizard class (inherits from Character)

class EvilWizard(Character):
    def __init__(self, name):
        super().__init__(name, health=350, attack_power=15, description="\nThis wizard was cleaning outside his home, when all of a sudden an intruder...")  
        
    # Evil Wizard's special ability: it can regenerate health
    def regenerate(self):
        heal_amount = 10
        self.health = min(self.health + heal_amount, self.max_health)  # Lower regeneration amount
       
               

#Character Creation Menu and logic

def create_character():                    
    print("\n    Choose your experience:") 
    print("|-----------------------------|")
    print("|    1. Warrior               |")
    print("|    2. Mage                  |")
    print("|    3. Spy                   |")  # Add Spy
    print("|    4. Clown                 |")  # Add Clown
    print(" vvvvvvvvvvvvvvvvvvvvvvvvvvvvv ")
    print(  )
    print(  )
    class_choice = input("Enter the number of your class choice: ")
    print(  )
    name = input("Enter your character's name: ")
    print(  )
    os.system('cls')
        
    if class_choice == '1':
        return Warrior(name)
    elif class_choice == '2':
        return Mage(name)
    elif class_choice == '3':
        return Spy(name)
    elif class_choice == '4':
        return Clown(name)
    else:
        print("Invalid choice. Defaulting to Warrior.")
        return Warrior(name)

# User Menu for actions:

def battle(player, opponent): # Choosing opponent instead of Wizard allows any character to fit the bill once called in main().
    while opponent.health > 0 and player.health > 0:
        print(f"\n{player.name}'s Health: {player.health}") #Display Health
        print(f"{opponent.name}'s Health: {opponent.health}") #Display Health
        print("\nI=====> Make Your Move! <=====I ")
        print("|-----------------------------|")
        print("|  1. Attack                  |")
        print("|  2. Use Special Abiliy      |")
        print("|  3. Heal                    |")
        print("|  4. View Stats              |")
        print("|  5. Too Difficult?          |")
        print(" vvvvvvvvvvvvvvvvvvvvvvvvvvvvv ")
        choice = input("Choose an action: ")
        os.system('cls')

#Logic Process:

        if choice == '1':
            player.rand_attack(opponent)
            os.system('cls')
        elif choice == '2':
           
            if isinstance(player, Warrior): # allow choices for Warrior
                ability_choice = input("Choose ability: \n1. RAGE\n2. Defensive Stance \ninput: ")
                if ability_choice == '1':
                    player.Rage(opponent)
                    player.rand_attack(opponent) 
                elif ability_choice == '2':
                    player.Defensive_Stance()
                        
        
            elif isinstance(player, Mage): # allow choices for Mage
                ability_choice = input("Choose an ability: \n1. Fireball \n2. Mana Shield \ninput: ")
                if ability_choice == '1':
                    player.Fireball(opponent)
                elif ability_choice == '2':
                    player.mana_shield()

             
            elif isinstance(player, Spy): # allow choices for Spy
                ability_choice = input("Choose an ability: \n1. Confuse \n2. Stealth \ninput: ")
                if ability_choice == '1':
                    player.Confuse(opponent)
                elif ability_choice == '2':
                    player.Thieving(opponent)

                  
            elif isinstance(player, Clown): # allow choices for Clown
                ability_choice = input("Choose an ability: \n1. Jester's Trick \n2. Laughing Gas \ninput: ")
                if ability_choice == '1':
                    player.Jesters_Trick(opponent)
                elif ability_choice == '2':
                    player.Laughing_Gas(opponent)
           
              
        elif choice == '3':
            player.heal()
            os.system('cls')
            pass
      
        elif choice == '4':
            player.display_stats(opponent)
            print(player.description)
            os.system('cls')
            continue

        elif choice == '5':
            print(f"\n.  .  . {opponent.name} has been removed from the yard.  .  . ")
            os.system('cls')
            break
       
        else:
            print("Invalid choice, try again.")
            os.system('cls')
            continue
#----------------------------------------------------------------------------------------------------
        # Start of Evil Wizard's turn: Attack and Regenerate!!!
        
        if opponent.health > 0:
            opponent.regenerate()
            opponent.rand_attack(player)
            
            # We must end Warrior's Defensive stance after one attack
            if isinstance(player, Warrior):
                player.end_defence
          

        if player.health <= 0:
            print(f"{player.name} has lost!")
            break

    if opponent.health <= 0:
        print(f"Defeated by {player.name}, {opponent.name} retreats to the near by Crypt!")

# ----------------------------------------------------------------------------------------------------

# Main function to handle the flow of the game
def main():
    # Character creation phase
    player = create_character()
#----------------------------------------------------------------------------------------------------
    # Evil Wizard is created
    opponent = EvilWizard("The Dark Wizard")
    
#----------------------------------------------------------------------------------------------------
    # Start the battle
    battle(player, opponent)
    
#----------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()