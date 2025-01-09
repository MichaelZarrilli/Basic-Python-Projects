MENU = {
    "espresso": {
        "ingredients": {
            "water": 50,
            "coffee": 18,
        },
        "cost": 1.5,
    },
    "latte": {
        "ingredients": {
            "water": 200,
            "milk": 150,
            "coffee": 24,
        },
        "cost": 2.5,
    },
    "cappuccino": {
        "ingredients": {
            "water": 250,
            "milk": 100,
            "coffee": 24,
        },
        "cost": 3.0,
    }
}

resources = {"water": 300, "milk": 200, "coffee": 100, "money": 0}

QUARTER = 0.25
DIME = 0.10
NICKLE = 0.05
PENNY = 0.01

def report():
  print(f"Water: {resources['water']}ml\nMilk: {resources['milk']}ml\nCoffee: "
        f"{resources['coffee']}ml\nMoney: ${resources['money']}")

def collect_money():
    quarters = int(input("How many quarters?: ")) * 0.25
    dimes = int(input("How many dimes?: ")) * 0.10
    nickles = int(input("How many nickles?: ")) * 0.05
    pennies = int(input("How many pennies?: ")) * 0.01
    total = quarters + dimes + nickles + pennies
    if total >= MENU[request]['cost']:
        resources['money'] = resources['money'] + MENU[request]['cost']
        print(f"Here is ${total - MENU[request]['cost']} in change.")
    else:
        print("Sorry that's not enough money. Money refunded.")

def coffee():
  if resources['water'] <= MENU[request]['ingredients']['water']:
      print("Sorry there is not enough water.")
  if resources['coffee'] <= MENU[request]['ingredients']['coffee']:
      print("Sorry there is not enough coffee.")
  if resources['milk'] <= MENU[request]['ingredients']['milk'] and request != 'espresso':
      print("Sorry there is not enough milk.")
  if resources['water'] >= MENU[request]['ingredients']['water'] and resources['coffee'] >= MENU[request]['ingredients']['coffee'] and resources['milk'] >= MENU[request]['ingredients']['milk']:
    resources['water'] = resources['water'] - MENU[request]['ingredients']['water']
    resources['coffee'] = resources['coffee'] - MENU[request]['ingredients']['coffee']
    resources['milk'] = resources['milk'] - MENU[request]['ingredients']['milk']
    print(f"Here is your {request}. Enjoy!")


machine_on = True

while machine_on:
  request = input("What would you like? (espresso/latte/cappuccino) ")
  if request == 'report':
    report()
  elif request == 'off':
    machine_on = False
  elif request == 'espresso':
    collect_money()
    coffee()

  elif request == 'latte':
    collect_money()
    coffee()

  elif request == 'cappuccino':
    collect_money()
    coffee()

  else:
    print("command not recognized, please try again")
