class CoffeeMachine:
    state = 'choosing an action'
    index = 0
    refill_value = []
    machine_count = 0

    def __new__(cls):
        if cls.machine_count != 1:
            cls.machine_count += 1
            return object.__new__(cls)
        return None

    def __init__(self):
        self.water = 400
        self.milk = 540
        self.coffee_beans = 120
        self.cups = 9
        self.money = 550
        self.user_handler()

    def __str__(self):
        """always return -> string"""
        return f'water: {self.water} ml, milk: {self.milk} ml,' \
               f' coffee beans: {self.coffee_beans} g, cups: {self.cups},' \
               f'money: {self.money}'

    def __repr__(self):
        """always return -> string
            Decide how the string to be printed on screen"""
        return f'An object of CoffeeMachine class'

    def manage_supply(self, required_supply, coffee):
        """Increase and decrease supplies and inventory: money, cups"""
        # current_supply = [self.water, self.milk, self.coffee_beans]
        # for i in range(len(required_supply)):
        #     current_supply[i] -= required_supply[i]

        self.water -= required_supply[0]
        self.milk -= required_supply[1]
        self.coffee_beans -= required_supply[2]

        # reduce the number of cups
        self.cups -= 1
        if coffee == 'espresso':
            self.money += 4
        elif coffee == 'latte':
            self.money += 7
        else:
            self.money += 6

        # after successfully making coffee return to action menu
        CoffeeMachine.state = 'choosing an action'

    def check_supply(self, required_supply, coffee):
        """check if we have required supply to make coffee"""
        is_less = False  # assuming we have required amount of supply to make the specified coffee
        current_supply = [self.water, self.milk, self.coffee_beans]

        for i in range(len(required_supply)):
            if required_supply[i] > current_supply[i]:
                is_less = True
                if i == 0:
                    print('Sorry, not enough water!')
                elif i == 1:
                    print('Sorry, not enough milk!')
                else:
                    print('Sorry, not enough coffee beans!')

                # after displaying message return to action menu
                CoffeeMachine.state = 'choosing an action'
                break

        if not is_less:
            print('I have enough resources, making you a coffee!')
            self.manage_supply(required_supply,  coffee)

    def make_coffee(self, coffee):
        """Provide required supply to make coffee"""
        espresso_supply = [250, 0, 16]
        latte_supply = [350, 75, 20]
        cappuccino_supply = [200, 100, 12]

        # check if we have enough supply to make that coffee
        if coffee == 'espresso':
            self.check_supply(espresso_supply, coffee)
        elif coffee == 'latte':
            self.check_supply(latte_supply, coffee)
        else:
            self.check_supply(cappuccino_supply, coffee)

    def buy_coffee(self, choice):
        """choose the coffee to be made"""
        if choice == '1':
            self.make_coffee('espresso')
        elif choice == '2':
            self.make_coffee('latte')
        elif choice == '3':
            self.make_coffee('cappuccino')
        else:
            CoffeeMachine.state = 'choosing an action'

    def refill_supply(self, value):
        print()

        supplies_question = ['Write how many ml of water do you want to add: ',
              'Write how many ml of milk do you want to add: ',
              'Write how many grams of coffee beans do you want to add: ',
              'Write how many disposable cups of coffee do you want to add: ']

        print(supplies_question[self.index])
        values.append(value)
        CoffeeMachine.index += 1
        print(values)

        # if len(values) == 4:
        #     self.water += values[0]
        #     self.milk += values[1]
        #     self.cups += values[2]
        #     self.coffee_beans += values[3]
        #
        #     CoffeeMachine.state = 'choosing an action'
        #

    def show_supply(self):
        print('\nThe coffee machine has: ')
        print(f'{self.water} of water')
        print(f'{self.milk} of milk')
        print(f'{self.coffee_beans} of coffee beans')
        print(f'{self.cups} of disposable cups')
        print(f'${self.money} of money')

        CoffeeMachine.state = 'choosing an action'

    def withdraw_money(self):
        amount = self.money
        self.money -= amount
        print(f'\nI gave you ${amount}')

        CoffeeMachine.state = 'choosing an action'

    # method to handle user entered string
    def handle_states(self, user_choice):

        if user_choice == 'buy':
            CoffeeMachine.state = 'choosing coffee'
        elif user_choice == 'fill':
            CoffeeMachine.state = 'refilling inventory'
            self.refill_supply(user_choice)
        elif user_choice == 'take':
            self.withdraw_money()
        elif user_choice == 'remaining':
            self.show_supply()
        elif user_choice == 'exit':
            CoffeeMachine.state = 'exiting'
        else:
            print('Invalid input!')  # not necessary

    # method to handle user choice string
    def choice_handler(self, user_choice):
        if self.state == 'choosing an action':
            self.handle_states(user_choice)
        elif self.state == 'choosing coffee':
            self.buy_coffee(user_choice)
        else:
            self.refill_supply(user_choice)

    def user_handler(self):
        # if self.state == 'refilling inventory':
        #     value = int(input())
        #     return value
        # else:
        while self.state != 'exiting':
            self.display_menu()
            user_choice = input()
            self.choice_handler(user_choice)

    def display_menu(self):

        if self.state == 'choosing an action':
            print('\nWrite action(buy, fill, take, remaining, exit):')
        elif self.state == 'choosing coffee':
            print('\nWhat do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino, back - to main menu:')


b = CoffeeMachine()

