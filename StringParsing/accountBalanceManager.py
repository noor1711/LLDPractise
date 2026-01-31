class StripeP2P:
    BANKS = ["HDFC", "AXIS"]
    TRANSACTION_STATUS={
        "FAILURE": "FAILURE", 
        "SUCCESS": "SUCCESS",
    }
    def __init__(self):
        self.userBalance = {}
        self.userBanks = {}

    @staticmethod
    def preprocess_command(command):
        return [arg.strip() for arg in command.split(",")]

    def handle_init(self, name, balance, *banks):
        # how do we diff between two users with the same name
        self.userBalance[name] = int(balance)
        self.userBanks[name] = [banks]

    def handle_post(self, timestamp, sender, receiver, amount):
        amount = int(amount)
        if sender in StripeP2P.BANKS:
            # deposit
            if receiver not in self.userBalance or sender not in self.userBanks.get(receiver):
                return "FAILURE"
            
            self.userBalance[receiver] += amount
            print(f"${amount} deposited in {receiver}'s account")
        elif receiver in StripeP2P.BANKS:
            if sender not in self.userBalance or receiver not in self.userBanks.get(receiver):
                return "FAILURE"
            
            if self.userBalance[sender] - amount < 0:
                return "FAILURE"
            
            self.userBalance[sender] -= amount
        else:
            if sender not in self.userBalance or receiver not in self.userBalance:
                return "FAILUE"
            
            if self.userBalance[sender] - amount < 0:
                return "FAILURE"
            
            self.userBalance[sender] -= amount
            self.userBalance[receiver] += amount
        return "SUCCESS"

    def handle_get(self, timestamp, name):
        return self.userBalance.get(name, "FAILURE")

    def command_handler(self, command_list):
        get_and_post_commands = []
        response = []
        for index, command in enumerate(command_list):
            arr = StripeP2P.preprocess_command(command)

            # we should add the logic for validating command lengths for get and post
            if arr[0] == "INIT":
                self.handle_init(*arr[1:])
            else:
                get_and_post_commands.append(*arr, index)
            response.append(None)
        
        get_and_post_commands.sort(key=lambda x: x[1])
        
        for command in get_and_post_commands:
            index = command[-1]
            if arr[0] == "POST":
                response[index] = self.handle_post(command[1:])
            else:
                response[index] = self.handle_get(command[1:])

        return response

# execute them in chronological order
# there can be at max on request per sec - we can use an array for timeline
# init does not have a timestamp so I am assuming all INITs come at t=0
# we remove the INITs from the list and then sort get and post
# also we are assuming that banks have unlimited money
